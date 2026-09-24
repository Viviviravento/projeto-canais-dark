"""Fail-closed boundary between public narration and production feedback."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ALLOWED_ORIGINS = frozenset(
    {"documentary_source", "approved_script", "explicit_narration_text"}
)
PROHIBITED_ORIGINS = frozenset(
    {
        "production_notes",
        "meta_instructions",
        "review_feedback",
        "qa_notes",
        "implementation_notes",
        "conversation_production_feedback",
    }
)


def load_public_narration(path: Path, text_ids: tuple[str, ...]) -> dict[str, str]:
    """Load only declared public-facing narration entries from a whitelist.

    Production notes may coexist beside a video project, but can never be
    selected here. Callers must request every line by its stable whitelist ID.
    """

    payload: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("schema") != "NarrationWhitelist.v1":
        raise ValueError("Whitelist de narração inválida")

    entries = {entry.get("id"): entry for entry in payload.get("entries", [])}
    selected: dict[str, str] = {}
    for text_id in text_ids:
        entry = entries.get(text_id)
        if not entry:
            raise ValueError(f"Texto de narração não autorizado: {text_id}")
        origin = str(entry.get("origin_type") or "")
        if origin in PROHIBITED_ORIGINS or origin not in ALLOWED_ORIGINS:
            raise ValueError(f"Origem proibida para narração: {text_id} ({origin})")
        if entry.get("content_layer") != "publicable":
            raise ValueError(f"Texto fora da camada publicável: {text_id}")
        if not entry.get("source_refs"):
            raise ValueError(f"Texto sem fonte autorizada: {text_id}")
        text = str(entry.get("text") or "").strip()
        if not text:
            raise ValueError(f"Texto vazio: {text_id}")
        selected[text_id] = text
    return selected
