from __future__ import annotations

import unittest
from datetime import datetime, timezone
from pathlib import Path

from jsonschema import ValidationError
import yaml

from factory.core.contracts import validate_contract
from factory.core.maturity import compare_baseline, revalidation_status
from factory.core.pipeline import CONTENT_STAGES, OPERATION_STAGES, FactoryRun


NOW = datetime.now(timezone.utc).isoformat()


def baseline_payload() -> dict:
    return {
        "schema_version": "1.0.0",
        "baseline_id": "voice-v1",
        "capability": "longform_voice",
        "version": "1.0.0",
        "scope": "narracao em português brasileiro",
        "state": "active",
        "conditions": {"review": "human"},
        "parameters": {"voice": {"model": "model-a", "tempo": 1.05}},
        "evidence_refs": ["review.json"],
        "tests": ["factory.tests.test_maturity"],
        "human_gate": {"required": True, "result": "approved"},
        "clean_runs": [{"run_id": "run-001", "verified_at": NOW, "evidence_refs": ["review.json"]}],
        "invalidation": {"tracked_parameter_paths": ["voice.model", "voice.tempo"], "policy": "revalidar antes de promover"},
    }


class MaturityContractTests(unittest.TestCase):
    def test_generic_operation_accepts_multiple_surfaces_and_formats(self) -> None:
        payload = {
            "schema_version": "1.0.0",
            "operation_id": "podcast-example",
            "display_name": "Podcast Example",
            "lifecycle": "piloting",
            "surfaces": ["site", "feed"],
            "formats": [
                {"id": "article", "description": "Texto editorial"},
                {"id": "audio", "description": "Episódio em áudio"},
            ],
            "capabilities": {
                "delivery": {"state": "validating", "baseline": None, "evidence_refs": ["run-001.json"]}
            },
        }
        validate_contract("OperationManifest", payload)

    def test_stable_capability_requires_a_baseline_reference(self) -> None:
        payload = {
            "schema_version": "1.0.0",
            "operation_id": "example",
            "display_name": "Example",
            "lifecycle": "stabilizing",
            "surfaces": ["surface"],
            "formats": [{"id": "format", "description": "Formato"}],
            "capabilities": {"voice": {"state": "stable", "baseline": None, "evidence_refs": ["review.json"]}},
        }
        with self.assertRaises(ValidationError):
            validate_contract("OperationManifest", payload)

    def test_current_operation_manifest_declares_capabilities_without_false_baseline(self) -> None:
        path = Path(__file__).resolve().parents[2] / "operations" / "a-palavra-que-cuida" / "operation.yaml"
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        validate_contract("OperationManifest", payload)
        self.assertEqual(payload["lifecycle"], "piloting")
        self.assertFalse(any(item["state"] == "stable" for item in payload["capabilities"].values()))

    def test_parameter_change_invalidates_baseline_and_requires_revalidation(self) -> None:
        baseline = baseline_payload()
        validate_contract("Baseline", baseline)
        comparison = compare_baseline(baseline, {"voice": {"model": "model-b", "tempo": 1.05}})
        result = revalidation_status({"state": "stable"}, comparison)
        self.assertFalse(comparison.compatible)
        self.assertEqual(comparison.changed_paths, ("voice.model",))
        self.assertEqual(result["state"], "validating")
        self.assertTrue(result["revalidation_required"])

    def test_factory_runtime_has_no_required_platform_or_format(self) -> None:
        source_root = Path(__file__).resolve().parents[1]
        source = "\n".join(path.read_text(encoding="utf-8").lower() for path in (source_root / "core").glob("*.py"))
        self.assertNotIn("youtube", source)
        self.assertNotIn("tiktok", source)
        self.assertNotIn("religio", source)

    def test_generic_run_kinds_preserve_complete_stage_sets(self) -> None:
        self.assertEqual(tuple(FactoryRun("operation-1", "operation").stages), OPERATION_STAGES)
        self.assertEqual(tuple(FactoryRun("content-1", "content").stages), CONTENT_STAGES)


if __name__ == "__main__":
    unittest.main()
