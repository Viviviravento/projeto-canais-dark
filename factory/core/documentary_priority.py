"""Fail-closed checks for Testemunha do Tempo's documentary-first edit."""

from __future__ import annotations

from typing import Any, Mapping


class DocumentaryPriorityError(ValueError):
    """Raised when source dialogue is being treated as decorative B-roll."""


def validate_documentary_timeline(payload: Mapping[str, Any]) -> None:
    """Require a declared audio role and captions for every spoken record.

    This intentionally has no maximum duration for a documentary dialogue.
    A real, translated, relevant exchange may run as long as the story needs.
    """
    if payload.get("schema") != "DocumentaryTimeline.v1":
        raise DocumentaryPriorityError("Timeline documental sem schema reconhecido")
    blocks = payload.get("blocks")
    if not isinstance(blocks, list) or not blocks:
        raise DocumentaryPriorityError("Timeline documental sem blocos")
    for block in blocks:
        block_id = str(block.get("id") or "sem-id")
        role = block.get("role")
        if role not in {"narration", "documentary_dialogue", "documentary_observation", "transition"}:
            raise DocumentaryPriorityError(f"{block_id}: papel audiovisual inválido")
        if not str(block.get("why_it_matters") or "").strip():
            raise DocumentaryPriorityError(f"{block_id}: falta a função narrativa")
        if role == "documentary_dialogue":
            if block.get("narration_over_dialogue") is not False:
                raise DocumentaryPriorityError(f"{block_id}: diálogo documental não pode receber narração sobreposta")
            if block.get("source_audio") != "audible":
                raise DocumentaryPriorityError(f"{block_id}: diálogo documental precisa manter áudio original audível")
            captions = block.get("captions")
            if not isinstance(captions, list) or not captions:
                raise DocumentaryPriorityError(f"{block_id}: diálogo documental exige legenda PT-BR")
            for caption in captions:
                if not str(caption.get("pt_br") or "").strip():
                    raise DocumentaryPriorityError(f"{block_id}: legenda PT-BR vazia")
                if not isinstance(caption.get("start"), (int, float)) or not isinstance(caption.get("end"), (int, float)):
                    raise DocumentaryPriorityError(f"{block_id}: timing de legenda ausente")
                if caption["end"] <= caption["start"]:
                    raise DocumentaryPriorityError(f"{block_id}: timing de legenda inválido")
        if role == "narration" and block.get("source_audio") not in {"muted_broll", "none"}:
            raise DocumentaryPriorityError(f"{block_id}: narração só pode usar registro sem fala concorrente")
