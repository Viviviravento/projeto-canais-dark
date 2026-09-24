from __future__ import annotations

import unittest

from factory.core.documentary_priority import DocumentaryPriorityError, validate_documentary_timeline


def valid_timeline() -> dict:
    return {
        "schema": "DocumentaryTimeline.v1",
        "blocks": [
            {"id": "context", "role": "narration", "why_it_matters": "prepara", "source_audio": "muted_broll"},
            {
                "id": "record", "role": "documentary_dialogue", "why_it_matters": "mostra a evidência",
                "source_audio": "audible", "narration_over_dialogue": False,
                "captions": [{"start": 0, "end": 2, "pt_br": "Fala traduzida."}],
            },
        ],
    }


class DocumentaryPriorityTests(unittest.TestCase):
    def test_accepts_captioned_documentary_dialogue(self) -> None:
        validate_documentary_timeline(valid_timeline())

    def test_rejects_narration_over_original_dialogue(self) -> None:
        payload = valid_timeline()
        payload["blocks"][1]["narration_over_dialogue"] = True
        with self.assertRaisesRegex(DocumentaryPriorityError, "narração sobreposta"):
            validate_documentary_timeline(payload)

    def test_rejects_uncaptioned_original_dialogue(self) -> None:
        payload = valid_timeline()
        payload["blocks"][1]["captions"] = []
        with self.assertRaisesRegex(DocumentaryPriorityError, "legenda PT-BR"):
            validate_documentary_timeline(payload)
