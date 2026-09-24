from __future__ import annotations

import unittest

from factory.core.visual_semantic_sync import (
    VisualSemanticSyncError,
    validate_narration_visual_script,
)


def valid_plan() -> dict:
    return {
        "schema": "NarrationVisualScript.v1",
        "sources": {"doorbell": "door.mp4", "bodycam": "body.mp4"},
        "blocks": [
            {"id": "open", "narrative_focus": "chegada", "visual_reason": "registro", "units": [["doorbell", 0, 8]]},
            {"id": "search", "narrative_focus": "busca", "visual_reason": "bodycam", "units": [["bodycam", 12, 8]]},
            {"id": "outro", "narrative_focus": "fim", "visual_reason": "moldura", "units": [["doorbell", 0, 8]]},
        ],
    }
class VisualSemanticSyncTests(unittest.TestCase):
    def test_accepts_explicit_mapping(self) -> None:
        validate_narration_visual_script(valid_plan())

    def test_rejects_doorbell_as_intermediate_transition(self) -> None:
        plan = valid_plan()
        plan["blocks"][1]["units"].append(["doorbell", 0, 4])
        with self.assertRaisesRegex(VisualSemanticSyncError, "Câmera da porta"):
            validate_narration_visual_script(plan)

    def test_rejects_block_without_semantic_reason(self) -> None:
        plan = valid_plan()
        plan["blocks"][1]["visual_reason"] = ""
        with self.assertRaisesRegex(VisualSemanticSyncError, "justificativa"):
            validate_narration_visual_script(plan)
