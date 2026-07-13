"""OpenRouter-spezifische Request-Parameter (z. B. Reasoning aus)."""

from __future__ import annotations

from typing import Any

import config


def openrouter_reasoning() -> dict[str, Any]:
    return {
        "effort": config.OPENROUTER_REASONING_EFFORT,
        "exclude": config.OPENROUTER_REASONING_EXCLUDE,
    }


def openrouter_generation_extra() -> dict[str, Any]:
    """Zusatzfelder für direkte JSON-Requests (requests.post an OpenRouter)."""
    return {"reasoning": openrouter_reasoning()}


def openrouter_llm_additional_kwargs() -> dict[str, Any]:
    """Zusatzfelder für LlamaIndex OpenAILike über das OpenAI-Python-SDK.

    OpenRouter-spezifische Felder wie ``reasoning`` dürfen nicht top-level an
    ``Completions.create()`` / ``ChatCompletions.create()`` — nur via extra_body.
    """
    return {"extra_body": {"reasoning": openrouter_reasoning()}}
