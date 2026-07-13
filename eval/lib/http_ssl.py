"""Zentrale TLS-/HTTP-Client-Konfiguration (Windows-CA-Fix + optional verify off)."""

from __future__ import annotations

import certifi
import httpx

import config


def requests_verify() -> bool | str:
    """verify-Argument für requests.get/post."""
    if config.HTTP_VERIFY_SSL:
        return certifi.where()
    return False


def make_httpx_client(timeout: float = 180.0) -> httpx.Client:
    """httpx-Client für OpenAI/LlamaIndex."""
    verify: bool | str = certifi.where() if config.HTTP_VERIFY_SSL else False
    return httpx.Client(verify=verify, timeout=timeout)


def apply_ssl_env() -> None:
    """CA-Bundle setzen oder — bei verify off — urllib3-Warnungen unterdrücken."""
    if not config.HTTP_VERIFY_SSL:
        import urllib3

        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        return
    import os

    ca = certifi.where()
    os.environ.setdefault("SSL_CERT_FILE", ca)
    os.environ.setdefault("REQUESTS_CA_BUNDLE", ca)
