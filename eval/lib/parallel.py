"""Begrenzte Parallelität für I/O-lastige Eval-Aufgaben (ThreadPool + Semaphore).

Wichtig: Semaphore-Wartezeit darf NICHT in Pool-Threads passieren (sonst Deadlock,
wenn z. B. langsame/hängende RAG-B-Tasks alle Worker blockieren). Ein Dispatcher
(`pump`) vergibt Slots per try_acquire und startet neue Tasks erst, wenn ein Slot frei ist.
"""

from __future__ import annotations

import threading
from collections import defaultdict, deque
from concurrent.futures import FIRST_COMPLETED, Future, ThreadPoolExecutor, wait
from typing import Callable, TypeVar

T = TypeVar("T")
R = TypeVar("R")


def run_bounded_parallel(
    tasks: list[T],
    worker: Callable[[T], R],
    *,
    limit_key: Callable[[T], str],
    limits: dict[str, int],
    max_workers: int | None = None,
    pause_s: float = 0.0,
    should_cancel: Callable[[], bool] | None = None,
    on_success: Callable[[T, R], None] | None = None,
    on_error: Callable[[T, Exception], None] | None = None,
) -> tuple[int, int]:
    """Führt `tasks` parallel aus; pro `limit_key` gilt ein Semaphore-Limit.

    Returns (ok_count, error_count).
    """
    if not tasks:
        return 0, 0

    keyed_queues: dict[str, deque[T]] = defaultdict(deque)
    for task in tasks:
        keyed_queues[limit_key(task)].append(task)

    eff_limits = {k: max(1, v) for k, v in limits.items()}
    for key in keyed_queues:
        eff_limits.setdefault(key, 1)

    semaphores = {k: threading.Semaphore(eff_limits[k]) for k in eff_limits}
    keys = list(keyed_queues.keys())
    pool_size = max_workers or max(sum(eff_limits[k] for k in keys), 1)

    ok = 0
    err = 0
    stats_lock = threading.Lock()
    pump_lock = threading.Lock()
    futures_lock = threading.Lock()
    futures: set[Future[None]] = set()

    def pump(executor: ThreadPoolExecutor) -> None:
        """Neue Tasks starten, solange Slots frei sind (blockiert Pool-Threads nicht)."""
        with pump_lock:
            if should_cancel and should_cancel():
                return
            progress = True
            while progress:
                progress = False
                for key in keys:
                    if not keyed_queues[key]:
                        continue
                    if not semaphores[key].acquire(blocking=False):
                        continue
                    task = keyed_queues[key].popleft()

                    def run_task(
                        task: T = task,
                        key: str = key,
                        sem: threading.Semaphore = semaphores[key],
                    ) -> None:
                        nonlocal ok, err
                        try:
                            if should_cancel and should_cancel():
                                return
                            result = worker(task)
                        except Exception as exc:  # noqa: BLE001
                            with stats_lock:
                                err += 1
                            if on_error:
                                on_error(task, exc)
                        else:
                            with stats_lock:
                                ok += 1
                            if on_success:
                                on_success(task, result)
                        finally:
                            if pause_s > 0:
                                import time

                                time.sleep(pause_s)
                            sem.release()
                            pump(executor)

                    fut = executor.submit(run_task)
                    with futures_lock:
                        futures.add(fut)
                    progress = True

    with ThreadPoolExecutor(max_workers=pool_size) as executor:
        pump(executor)
        while True:
            with futures_lock:
                if not futures:
                    pending = any(keyed_queues[k] for k in keys)
                    if not pending:
                        break
                    snapshot = set(futures)
                else:
                    snapshot = set(futures)

            if should_cancel and should_cancel():
                break

            if not snapshot:
                pump(executor)
                continue

            done, _ = wait(snapshot, timeout=0.5, return_when=FIRST_COMPLETED)
            for fut in done:
                try:
                    fut.result()
                except Exception:  # noqa: BLE001
                    pass
                with futures_lock:
                    futures.discard(fut)
            pump(executor)

    return ok, err
