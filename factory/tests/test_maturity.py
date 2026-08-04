from __future__ import annotations

import json
import unittest
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

from factory.core.contracts import load_schema, validate_contract
from factory.core.gates import GatePolicy
from factory.core.maturity import (
    assess_clean_run,
    compare_baseline_configuration,
    configuration_fingerprint,
    enforce_baseline_assessment,
    load_operation_manifest,
    validate_baseline,
)


NOW = datetime.now(timezone.utc).isoformat()
ROOT = Path(__file__).resolve().parents[2]


def operation_payload(*, surfaces: list[str], formats: list[dict] | None = None) -> dict:
    return {
        "schema_version": "1.0.0",
        "operation_id": "example-operation",
        "display_name": "Example operation",
        "lifecycle": "incubating",
        "purpose": "Exercise contract composition.",
        "surfaces": surfaces,
        "formats": formats if formats is not None else [{"id": "short", "description": "A short artifact."}],
        "capabilities": {
            "publication": {
                "state": "not_exercised",
                "baseline": None,
                "evidence_refs": [],
                "notes": "No publication has been attempted.",
            }
        },
        "parameters": {},
        "policies": {},
    }


def baseline_payload() -> dict:
    parameters = {
        "provider": "provider-a",
        "model": "model-1",
        "text": {"preparation": "semantic-blocks"},
        "postprocess": {"tempo": 1.05},
    }
    return {
        "schema_version": "1.0.0",
        "baseline_id": "voice.example.v1",
        "capability": "voice",
        "version": 1,
        "scope": "example-operation/voice",
        "state": "approved",
        "input_conditions": {"language": "pt-BR"},
        "parameters": parameters,
        "configuration_fingerprint": configuration_fingerprint(parameters),
        "evidence_artifacts": ["evidence/review.json"],
        "tests": ["semantic-human-review"],
        "approval_gate": {"kind": "human", "status": "passed", "evidence_ref": "evidence/review.json"},
        "clean_runs": 1,
        "clean_run_refs": ["runs/run-001.json"],
        "invalidation_triggers": ["provider", "model", "text.preparation", "postprocess.tempo"],
        "known_regressions": [],
        "recorded_at": NOW,
        "run_refs": ["runs/run-001.json"],
        "experiment_refs": ["experiments/voice-001.json"],
    }


class OperationManifestTests(unittest.TestCase):
    def test_current_operation_manifest_loads(self) -> None:
        manifest = load_operation_manifest(ROOT / "operations" / "a-palavra-que-cuida" / "manifest.yaml")
        self.assertEqual(manifest["lifecycle"], "stabilizing")
        self.assertEqual(manifest["capabilities"]["longform_voice"]["state"], "regression_detected")
        self.assertIsNone(manifest["capabilities"]["longform_voice"]["baseline"])

    def test_incubating_operation_manifest_loads(self) -> None:
        manifest = load_operation_manifest(ROOT / "operations" / "mukbang-ensaio-seco" / "manifest.yaml")
        self.assertEqual(manifest["lifecycle"], "incubating")

    def test_manifest_policy_paths_resolve(self) -> None:
        for operation in ("a-palavra-que-cuida", "mukbang-ensaio-seco"):
            manifest_path = ROOT / "operations" / operation / "manifest.yaml"
            manifest = load_operation_manifest(manifest_path)
            for policy_path in manifest["policies"].values():
                self.assertTrue((manifest_path.parent / policy_path).resolve().is_file(), policy_path)

    def test_invalid_lifecycle_is_rejected(self) -> None:
        payload = operation_payload(surfaces=["surface-a"])
        payload["lifecycle"] = "done"
        with self.assertRaises(Exception):
            validate_contract("OperationManifest", payload)

    def test_invalid_capability_state_is_rejected(self) -> None:
        payload = operation_payload(surfaces=["surface-a"])
        payload["capabilities"]["publication"]["state"] = "almost_ready"
        with self.assertRaises(Exception):
            validate_contract("OperationManifest", payload)

    def test_unstable_capability_cannot_claim_a_baseline(self) -> None:
        payload = operation_payload(surfaces=["surface-a"])
        payload["capabilities"]["publication"]["baseline"] = "publication-v1"
        with self.assertRaises(Exception):
            validate_contract("OperationManifest", payload)

    def test_stable_capability_requires_a_baseline(self) -> None:
        payload = operation_payload(surfaces=["surface-a"])
        payload["capabilities"]["publication"]["state"] = "stable"
        with self.assertRaises(Exception):
            validate_contract("OperationManifest", payload)

    def test_one_surface_without_longform_is_valid(self) -> None:
        validate_contract("OperationManifest", operation_payload(surfaces=["surface-a"]))

    def test_multiple_surfaces_are_valid(self) -> None:
        validate_contract("OperationManifest", operation_payload(surfaces=["surface-a", "surface-b"]))

    def test_exploring_operation_can_leave_surfaces_and_formats_open(self) -> None:
        payload = operation_payload(surfaces=[], formats=[])
        payload["lifecycle"] = "exploring"
        validate_contract("OperationManifest", payload)

    def test_piloting_operation_must_declare_surface_and_format(self) -> None:
        payload = operation_payload(surfaces=[], formats=[])
        payload["lifecycle"] = "piloting"
        with self.assertRaises(Exception):
            validate_contract("OperationManifest", payload)


class BaselineGovernanceTests(unittest.TestCase):
    def test_valid_baseline_contract(self) -> None:
        validate_baseline(baseline_payload())

    def test_relevant_change_restores_gate(self) -> None:
        baseline = baseline_payload()
        current = deepcopy(baseline["parameters"])
        current["model"] = "model-2"
        assessment = compare_baseline_configuration(baseline, current)
        self.assertFalse(assessment.reusable)
        self.assertEqual(assessment.status, "revalidation_required")
        self.assertEqual(assessment.required_gate_state, "restored")
        self.assertEqual([change.path for change in assessment.changes], ["model"])
        gate = GatePolicy("voice-regression", "quality", state="automatic")
        enforce_baseline_assessment(assessment, gate, evidence_ref="config-diff.json")
        self.assertEqual(gate.state, "restored")

    def test_irrelevant_change_does_not_invalidate_baseline(self) -> None:
        baseline = baseline_payload()
        current = deepcopy(baseline["parameters"])
        current["diagnostic_label"] = "not-an-invalidation-trigger"
        assessment = compare_baseline_configuration(baseline, current)
        self.assertTrue(assessment.reusable)
        self.assertEqual(assessment.required_gate_state, "unchanged")

    def test_clean_run_rejects_gate_bypass(self) -> None:
        run = assess_clean_run(
            run_id="run-1",
            operation_id="operation-1",
            evidence_artifacts=["evidence.json"],
            gate_bypassed=True,
        )
        self.assertFalse(run["clean"])
        self.assertIn("gate_bypassed", run["disqualifiers"])

    def test_clean_run_requires_preserved_evidence(self) -> None:
        run = assess_clean_run(run_id="run-2", operation_id="operation-1", evidence_artifacts=[])
        self.assertFalse(run["clean"])
        self.assertIn("evidence_missing", run["disqualifiers"])


class UniversalIsolationTests(unittest.TestCase):
    def test_factory_does_not_require_specific_surfaces_or_formats(self) -> None:
        text = json.dumps(load_schema("OperationManifest"), ensure_ascii=False).lower()
        for term in ("youtube", "tiktok", "horizontal", "longform", "shorts"):
            self.assertNotIn(term, text)

    def test_factory_implementation_has_no_religious_rules(self) -> None:
        banned = ("biblia", "bible", "versiculo", "religio", "acf")
        files = [
            *list((ROOT / "factory" / "core").glob("*.py")),
            *list((ROOT / "factory" / "policies").glob("*.yaml")),
            *list((ROOT / "factory" / "contracts").rglob("*.json")),
        ]
        for path in files:
            text = path.read_text(encoding="utf-8").lower()
            for term in banned:
                self.assertNotIn(term, text, f"{term} vazou para {path.relative_to(ROOT)}")

    def test_active_python_uses_new_imports_and_operation_paths(self) -> None:
        files = [
            *list((ROOT / "factory" / "core").rglob("*.py")),
            *list((ROOT / "operations" / "a-palavra-que-cuida").rglob("*.py")),
        ]
        for path in files:
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("ai.fabrica", text, str(path.relative_to(ROOT)))
            self.assertNotIn('"Canal Religioso"', text, str(path.relative_to(ROOT)))


if __name__ == "__main__":
    unittest.main()
