"""RAG-Index: einmalig bauen/laden, ohne NLTK-Abhängigkeit.

Vektoren liegen in ChromaDB (`rag_chroma/`), Metadaten/Docstore in `rag_index/`.
Der alte LlamaIndex-Default (eine riesige default__vector_store.json) wird nicht mehr
geladen — bei >50 MB wird ein Chroma-Neuaufbau ausgelöst.
"""

from __future__ import annotations

import shutil
import threading
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError
from pathlib import Path

import config
from lib.http_ssl import make_httpx_client

_RAG_QUERY_ENGINE = None
_RAG_INDEX_READY = False
_RAG_QUERY_LOCK = threading.Lock()
_ENGINE_INIT_LOCK = threading.Lock()
_CHROMA_COLLECTION = "wifa_rag"

# README und andere Nicht-Wissensdateien vom Index ausschließen
RAG_EXCLUDE_FILES = {"README.md", ".gitkeep"}
RAG_ALLOWED_SUFFIXES = {".pdf", ".txt", ".md", ".html", ".htm", ".docx", ".csv", ".json"}


def list_indexable_docs() -> list[Path]:
    if not config.DOCS_DIR.exists():
        return []
    docs: list[Path] = []
    for path in sorted(config.DOCS_DIR.iterdir()):
        if not path.is_file():
            continue
        if path.name in RAG_EXCLUDE_FILES:
            continue
        if path.suffix.lower() not in RAG_ALLOWED_SUFFIXES:
            continue
        docs.append(path)
    return docs


def _configure_llama_settings() -> None:
    from llama_index.core import Settings
    from llama_index.core.node_parser import TokenTextSplitter
    from llama_index.embeddings.openai import OpenAIEmbedding
    from llama_index.llms.openai_like import OpenAILike

    from lib.openrouter_params import openrouter_llm_additional_kwargs

    if not config.OPENROUTER_API_KEY_B:
        raise ValueError("OPENROUTER_API_KEY_B ist nicht gesetzt (Config B: RAG-LLM)")
    if not config.OPENAI_API_KEY:
        raise ValueError(
            "OPENAI_API_KEY ist nicht gesetzt (Embeddings laufen direkt über OpenAI, "
            "da OpenRouter Embeddings i.d.R. nicht proxyt)"
        )

    Settings.llm = OpenAILike(
        model=config.GENERATION_MODEL,
        api_base="https://openrouter.ai/api/v1",
        api_key=config.OPENROUTER_API_KEY_B,
        is_chat_model=True,
        temperature=config.GENERATION_TEMPERATURE,
        http_client=make_httpx_client(timeout=180.0),
        additional_kwargs=openrouter_llm_additional_kwargs(),
    )
    Settings.embed_model = OpenAIEmbedding(
        model=config.EMBEDDING_MODEL,
        api_key=config.OPENAI_API_KEY,
        http_client=make_httpx_client(timeout=180.0),
    )
    Settings.transformations = [
        TokenTextSplitter(chunk_size=512, chunk_overlap=20),
    ]


def _chroma_ready() -> bool:
    if not config.RAG_CHROMA_DIR.exists():
        return False
    return any(config.RAG_CHROMA_DIR.iterdir())


def _legacy_vector_store_bytes() -> int:
    legacy = config.RAG_INDEX_DIR / "default__vector_store.json"
    return legacy.stat().st_size if legacy.exists() else 0


def _needs_chroma_rebuild() -> bool:
    """Alter SimpleVectorStore-JSON (>50 MB) blockiert beim Laden — Chroma nötig."""
    return _legacy_vector_store_bytes() > 50 * 1024 * 1024 and not _chroma_ready()


def _reset_runtime() -> None:
    global _RAG_QUERY_ENGINE, _RAG_INDEX_READY
    _RAG_QUERY_ENGINE = None
    _RAG_INDEX_READY = False


def _wipe_index_dirs() -> None:
    for path in (config.RAG_INDEX_DIR, config.RAG_CHROMA_DIR):
        if not path.exists():
            continue
        try:
            shutil.rmtree(path)
        except PermissionError as exc:
            raise PermissionError(
                f"{exc}\n\n"
                f"Index-Ordner {path} ist gesperrt (Windows). "
                "Bitte Eval-Server und alle hängenden Python/RAG-Prozesse beenden, "
                "dann erneut: python build_rag_index.py --rebuild"
            ) from exc


def _chroma_vector_store():
    import chromadb
    from llama_index.vector_stores.chroma import ChromaVectorStore

    config.RAG_CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(config.RAG_CHROMA_DIR))
    collection = client.get_or_create_collection(_CHROMA_COLLECTION)
    return ChromaVectorStore(chroma_collection=collection)


def _load_chroma_index():
    from llama_index.core import StorageContext, load_index_from_storage

    vector_store = _chroma_vector_store()
    storage_context = StorageContext.from_defaults(
        vector_store=vector_store,
        persist_dir=str(config.RAG_INDEX_DIR),
    )
    return load_index_from_storage(storage_context)


def ensure_rag_index(*, force_rebuild: bool = False) -> None:
    """Index einmal bauen oder aus Chroma + rag_index/ laden."""
    global _RAG_INDEX_READY

    doc_files = list_indexable_docs()
    if not doc_files:
        raise FileNotFoundError(
            f"Keine indexierbaren Dokumente in {config.DOCS_DIR}. "
            f"Erlaubt: {', '.join(sorted(RAG_ALLOWED_SUFFIXES))}. "
            "Bitte dieselben Rohdokumente wie für Config A ablegen."
        )

    if _needs_chroma_rebuild() and not force_rebuild:
        legacy_mb = _legacy_vector_store_bytes() / (1024 * 1024)
        print(
            f"RAG: Legacy-Vektorstore ({legacy_mb:.0f} MB JSON) — "
            "starte Chroma-Neuaufbau (einmalig, kann dauern) …"
        )
        force_rebuild = True

    if force_rebuild:
        _wipe_index_dirs()
        _reset_runtime()

    if (
        not force_rebuild
        and _chroma_ready()
        and config.RAG_INDEX_DIR.exists()
        and (config.RAG_INDEX_DIR / "docstore.json").exists()
    ):
        print(f"RAG: Chroma-Index bereit ({config.RAG_CHROMA_DIR})")
        _RAG_INDEX_READY = True
        return

    from llama_index.core import SimpleDirectoryReader, StorageContext, VectorStoreIndex

    _configure_llama_settings()

    print(f"RAG: Baue Chroma-Index aus {len(doc_files)} Datei(en) in {config.DOCS_DIR} …")
    for path in doc_files[:10]:
        print(f"  - {path.name}")
    if len(doc_files) > 10:
        print(f"  … und {len(doc_files) - 10} weitere")

    reader = SimpleDirectoryReader(
        input_dir=str(config.DOCS_DIR),
        exclude=list(RAG_EXCLUDE_FILES),
        filename_as_id=True,
    )
    documents = reader.load_data()
    if not documents:
        raise FileNotFoundError(f"SimpleDirectoryReader konnte keine Inhalte aus {config.DOCS_DIR} laden")

    print(f"RAG: {len(documents)} Dokument(e) geladen, erstelle Embeddings …")
    if not config.HTTP_VERIFY_SSL:
        print("RAG: HTTP_VERIFY_SSL=false — TLS-Verifikation deaktiviert")

    vector_store = _chroma_vector_store()
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        show_progress=True,
    )
    config.RAG_INDEX_DIR.mkdir(parents=True, exist_ok=True)
    index.storage_context.persist(persist_dir=str(config.RAG_INDEX_DIR))
    print(f"RAG: Index persistiert (Chroma: {config.RAG_CHROMA_DIR}, Meta: {config.RAG_INDEX_DIR})")
    _RAG_INDEX_READY = True


def get_rag_query_engine():
    """Query Engine für Config B (lazy, thread-safe initialisiert)."""
    global _RAG_QUERY_ENGINE

    if _RAG_QUERY_ENGINE is not None:
        return _RAG_QUERY_ENGINE

    with _ENGINE_INIT_LOCK:
        if _RAG_QUERY_ENGINE is not None:
            return _RAG_QUERY_ENGINE

        if not _RAG_INDEX_READY:
            ensure_rag_index()

        from llama_index.core.prompts import PromptTemplate
        from llama_index.core.prompts.prompt_type import PromptType

        from lib.prompts import rag_refine_prompt_template, rag_text_qa_prompt_template

        _configure_llama_settings()
        print("RAG: Lade Query-Engine …", flush=True)
        index = _load_chroma_index()

        text_qa_template = PromptTemplate(
            rag_text_qa_prompt_template(),
            prompt_type=PromptType.QUESTION_ANSWER,
        )
        refine_template = PromptTemplate(
            rag_refine_prompt_template(),
            prompt_type=PromptType.REFINE,
        )

        _RAG_QUERY_ENGINE = index.as_query_engine(
            similarity_top_k=config.RAG_SIMILARITY_TOP_K,
            response_mode=config.RAG_RESPONSE_MODE,
            text_qa_template=text_qa_template,
            refine_template=refine_template,
        )
        print("RAG: Query-Engine bereit.", flush=True)
        return _RAG_QUERY_ENGINE


def query_rag(frage: str) -> str:
    """Thread-sicherer RAG-Aufruf mit Timeout."""
    engine = get_rag_query_engine()
    with _RAG_QUERY_LOCK:
        with ThreadPoolExecutor(max_workers=1) as pool:
            fut = pool.submit(lambda: str(engine.query(frage)))
            try:
                return fut.result(timeout=config.RAG_QUERY_TIMEOUT_S)
            except FuturesTimeoutError as exc:
                raise TimeoutError(
                    f"RAG-Query Timeout nach {config.RAG_QUERY_TIMEOUT_S}s"
                ) from exc
