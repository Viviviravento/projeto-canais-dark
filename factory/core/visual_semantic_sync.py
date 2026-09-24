"""Fail-closed validation for narrated documentary visual scripts.

The validator deliberately checks intent, not just media duration: a source may
belong to the case and still be wrong for the sentence that is being narrated.
"""

from __future__ import annotations

from typing import Any, Mapping


class VisualSemanticSyncError(ValueError):
    """Raised when a narration/visual mapping is not ready for rendering."""


def validate_narration_visual_script(payload: Mapping[str, Any]) -> None:
    """Validate the minimum contract for a semantic audiovisual edit.

    The renderer must receive an explicit rationale and one or more planned
    visual units for every narrative block.  Doorbell footage is a framing
    device in this operation, therefore it is valid only at the first and last
    blocks.  This keeps a generic asset from silently becoming a background.
    """

    if payload.get("schema") != "NarrationVisualScript.v1":
        raise VisualSemanticSyncError("Roteiro visual sem schema reconhecido")
    blocks = payload.get("blocks")
    if not isinstance(blocks, list) or len(blocks) < 2:
        raise VisualSemanticSyncError("Roteiro visual requer pelo menos abertura e encerramento")
    ids: set[str] = set()
    sources = payload.get("sources")
    if not isinstance(sources, Mapping):
        raise VisualSemanticSyncError("Roteiro visual sem catálogo de fontes")

    doorbell_blocks: list[int] = []
    for index, block in enumerate(blocks):
        if not isinstance(block, Mapping):
            raise VisualSemanticSyncError(f"Bloco visual inválido na posição {index}")
        block_id = str(block.get("id") or "")
        if not block_id or block_id in ids:
            raise VisualSemanticSyncError(f"ID visual ausente ou repetido: {block_id!r}")
        ids.add(block_id)
        if not str(block.get("narrative_focus") or "").strip():
            raise VisualSemanticSyncError(f"{block_id}: falta o foco narrativo")
        if not str(block.get("visual_reason") or "").strip():
            raise VisualSemanticSyncError(f"{block_id}: falta a justificativa semântica visual")
        units = block.get("units")
        if not isinstance(units, list) or not units:
            raise VisualSemanticSyncError(f"{block_id}: falta uma evidência visual planejada")
        for unit in units:
            if not isinstance(unit, list) or len(unit) != 3:
                raise VisualSemanticSyncError(f"{block_id}: unidade visual inválida")
            source, start, seconds = unit
            if source not in sources:
                raise VisualSemanticSyncError(f"{block_id}: fonte não catalogada: {source}")
            if not isinstance(start, (int, float)) or start < 0:
                raise VisualSemanticSyncError(f"{block_id}: início de fonte inválido")
            maximum_seconds = 60 if block.get("source_dialogue") else 20
            if not isinstance(seconds, (int, float)) or seconds <= 0 or seconds > maximum_seconds:
                raise VisualSemanticSyncError(
                    f"{block_id}: duração visual deve ficar entre 0 e {maximum_seconds} segundos"
                )
            if source == "doorbell":
                doorbell_blocks.append(index)

    if doorbell_blocks != [0, len(blocks) - 1]:
        raise VisualSemanticSyncError(
            "Câmera da porta só pode enquadrar a abertura e o encerramento do episódio"
        )
