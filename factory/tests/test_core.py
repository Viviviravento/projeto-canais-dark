from __future__ import annotations

import json
import tempfile
import unittest
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

from jsonschema import Draft202012Validator

from factory.core.contracts import list_contracts, load_schema, validate_contract
from factory.core.costs import CostLedger, PricePoint
from factory.core.gates import GatePolicy
from factory.core.genesis import ChannelThesis, exploratory_theses, thesis_ready_for_pilot
from factory.core.incidents import IntegrationIncident
from factory.core.media import select_cost_optimized_eligible
from factory.core.metrics import ImmutableRecordStore
from factory.core.pipeline import CONTENT_STAGES, OPERATION_STAGES, FactoryRun, validate_run_payload
from factory.core.qa import audit_package


NOW = datetime.now(timezone.utc).isoformat()


class StaticPriceSource:
    def current_price(self, provider: str, model: str, operation: str) -> PricePoint:
        return PricePoint(provider, model, operation, "second", "USD", Decimal("0.07"), NOW, "https://prices.example/model")


class ContractTests(unittest.TestCase):
    def test_all_public_schemas_are_valid(self) -> None:
        self.assertEqual(len(list_contracts()), 14)
        for contract in list_contracts():
            Draft202012Validator.check_schema(load_schema(contract))

    def test_research_claim_requires_one_source_object(self) -> None:
        payload = {
            "schema_version": "1.0.0",
            "claim_id": "claim-1",
            "statement": "A platform exposes a metric.",
            "classification": "research",
            "recorded_at": NOW,
            "scope": "platform",
            "confidence": 0.9,
            "decision_refs": [],
        }
        with self.assertRaises(Exception):
            validate_contract("ClaimRecord", payload)
        payload["source"] = {"kind": "primary", "locator": "https://example.test/docs", "accessed_at": NOW}
        validate_contract("ClaimRecord", payload)

    def test_universal_schemas_do_not_contain_channel_specific_rules(self) -> None:
        banned = ("biblia", "bible", "versiculo", "religio", "mulher", "10 a 12", "10-12", "avatar")
        for contract in list_contracts():
            text = json.dumps(load_schema(contract), ensure_ascii=False).lower()
            for term in banned:
                self.assertNotIn(term, text, f"{term} vazou para {contract}")


class PipelineTests(unittest.TestCase):
    def test_operation_and_content_have_all_fixed_stages(self) -> None:
        self.assertEqual(tuple(FactoryRun("o1", "operation").stages), OPERATION_STAGES)
        self.assertEqual(tuple(FactoryRun("c1", "content").stages), CONTENT_STAGES)

    def test_legacy_channel_and_video_kinds_remain_compatible(self) -> None:
        self.assertEqual(tuple(FactoryRun("c1", "channel").stages), OPERATION_STAGES)
        self.assertEqual(tuple(FactoryRun("v1", "video").stages), CONTENT_STAGES)

    def test_not_applicable_requires_reason(self) -> None:
        run = FactoryRun("v1", "video")
        with self.assertRaises(ValueError):
            run.mark("aquisicao", "not_applicable")
        run.mark("aquisicao", "not_applicable", reason="Captura original ja fornecida.")

    def test_mukbang_dry_run_crosses_same_macro_stages(self) -> None:
        path = Path(__file__).resolve().parents[2] / "operations" / "mukbang-ensaio-seco" / "run.json"
        validate_run_payload(json.loads(path.read_text(encoding="utf-8")), require_terminal=True)


class GenesisAndMediaTests(unittest.TestCase):
    def test_user_thesis_is_deepened_first(self) -> None:
        supplied = ChannelThesis("one", "supplied", "user_input", ("claim-1",), "angle")
        result = exploratory_theses(supplied, [ChannelThesis("two", "a", "research"), ChannelThesis("three", "b", "research")])
        self.assertEqual([item.depth for item in result], ["deep", "scan", "scan"])
        self.assertTrue(thesis_ready_for_pilot(result[0]))

    def test_cost_optimization_only_after_quality_gates(self) -> None:
        checks = {key: True for key in ("meaning", "fidelity", "authenticity", "quality", "license")}
        choice = select_cost_optimized_eligible([
            {"id": "cheap-bad", "eligible": True, "estimated_cost": 0, "checks": {**checks, "meaning": False}},
            {"id": "stock-good", "eligible": True, "estimated_cost": 0.1, "checks": checks},
            {"id": "generated-good", "eligible": True, "estimated_cost": 1.0, "checks": checks},
        ])
        self.assertEqual(choice["id"], "stock-good")

    def test_total_cost_can_justify_higher_direct_spend(self) -> None:
        checks = {key: True for key in ("meaning", "fidelity", "authenticity", "quality", "license")}
        choice = select_cost_optimized_eligible([
            {"id": "cheap-with-rework", "eligible": True, "estimated_cost": 0.1, "expected_total_cost": 1.1, "checks": checks},
            {"id": "reliable", "eligible": True, "estimated_cost": 0.5, "expected_total_cost": 0.5, "checks": checks},
        ])
        self.assertEqual(choice["id"], "reliable")

    def test_higher_expected_value_requires_evidence(self) -> None:
        checks = {key: True for key in ("meaning", "fidelity", "authenticity", "quality", "license")}
        with self.assertRaises(ValueError):
            select_cost_optimized_eligible([
                {"id": "unsupported", "eligible": True, "estimated_cost": 0.5, "expected_value": 2, "checks": checks},
            ])


class GateAndIncidentTests(unittest.TestCase):
    def test_gate_promotes_and_restores_without_user_command(self) -> None:
        gate = GatePolicy("qa-sync", "qa")
        for index in range(3):
            gate.record_clean_run(f"run-{index}")
        self.assertEqual(gate.state, "sampled")
        for index in range(6):
            gate.record_clean_run(f"sample-{index}", sampled_approved=True)
        self.assertEqual(gate.state, "automatic")
        message = gate.restore("Dessincronia critica.", "defect-1", critical=True)
        self.assertEqual(gate.state, "restored")
        self.assertIn("automatic -> restored", message or "")

    def test_permanent_human_gate_never_promotes(self) -> None:
        gate = GatePolicy("secrets", "credentials")
        for index in range(20):
            gate.record_clean_run(f"run-{index}", sampled_approved=True)
        self.assertEqual(gate.state, "full")
        self.assertTrue(gate.permanent_human)

    def test_incident_preserves_resume_and_requires_cause(self) -> None:
        incident = IntegrationIncident("i-1", "browser", "publish", ["selector missing"], "before_submit", "key-1", publication=True)
        incident.freeze()
        hypothesis = incident.add_hypothesis("Selector changed")
        with self.assertRaises(ValueError):
            incident.apply_fix("Use alternate selector")
        incident.confirm_cause(hypothesis, ["dom-snapshot-1"])
        incident.apply_fix("Use semantic locator")
        incident.verify(["dry-run-no-submit"], True)
        incident.resume()
        self.assertEqual(incident.as_contract()["resume_point"]["idempotency_key"], "key-1")

    def test_incident_blocks_after_three_cycles_without_new_evidence(self) -> None:
        incident = IntegrationIncident("i-2", "api", "query", ["shape changed"], "request_built", "key-2")
        incident.freeze()
        for _ in range(3):
            incident.conclude_cycle(new_evidence=False)
        self.assertEqual(incident.state, "blocked")


class CostMetricAndQATests(unittest.TestCase):
    def test_paid_retry_creates_new_quote(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            ledger = CostLedger(Path(directory) / "costs.jsonl")
            quote = ledger.quote(StaticPriceSource(), provider="provider", model="model", operation="video", quantity=5)
            ledger.reserve(quote.quote_id)
            ledger.fail(quote.quote_id, "remote failure")
            retry = ledger.retry_quote(quote.quote_id, StaticPriceSource())
            self.assertNotEqual(retry.quote_id, quote.quote_id)
            self.assertEqual(retry.parent_quote_id, quote.quote_id)
            validate_contract("CostQuote", retry.as_contract())

    def test_metric_observation_is_append_only(self) -> None:
        payload = {
            "schema_version": "1.0.0", "observation_id": "obs-1", "channel_id": "channel-1",
            "content_id": "video-1", "platform": "platform-a", "window": "24h", "observed_at": NOW,
            "source": "mock-api", "values": {"views": 10}, "raw_hash": "a" * 64, "raw_artifact": None,
        }
        with tempfile.TemporaryDirectory() as directory:
            store = ImmutableRecordStore(directory)
            store.append_observation(payload)
            with self.assertRaises(ValueError):
                store.append_observation(payload)

    def test_qa_checks_scenes_not_frames(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "video.mp4"
            output.write_bytes(b"mock")
            report = audit_package({
                "output": {"path": str(output)},
                "captions": {"required": True, "artifact": "captions.srt"},
                "visual_policy": {"max_asset_reuse": 2},
                "scenes": [{
                    "id": "scene-1", "asset_id": "a", "keyframes": ["kf-1.jpg"],
                    "sync_events": [{"visual_start": 1.0, "audio_start": 1.1}],
                    "contains_diegetic_text": False,
                }],
                "end_screen": {"required": True, "duration_seconds": 10, "minimum_seconds": 5, "maximum_seconds": 20, "slots": 2},
            })
            self.assertTrue(report.passed)

    def test_qa_catches_voice_static_text_and_avatar_failures(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "video.mp4"
            output.write_bytes(b"mock")
            report = audit_package({
                "output": {"path": str(output)},
                "audio": {"required": True, "artifact": "voice.mp3", "semantic_review": "pending"},
                "captions": {"required": False},
                "visual_policy": {"max_asset_reuse": 2, "maximum_static_seconds": 7},
                "scenes": [
                    {"id": "still", "asset_id": "a", "mode": "still", "continuous_seconds": 8, "keyframes": ["kf.jpg"]},
                    {"id": "avatar", "asset_id": "b", "mode": "avatar", "avatar_is_speaking": False, "keyframes": ["kf.jpg"]},
                    {
                        "id": "avatar-composite",
                        "asset_id": "b2",
                        "mode": "avatar",
                        "avatar_is_speaking": True,
                        "composited": True,
                        "physical_coherence_review": "pending",
                        "keyframes": ["kf.jpg"],
                    },
                    {"id": "text", "asset_id": "c", "mode": "still", "continuous_seconds": 2, "keyframes": ["kf.jpg"], "exact_text_expected": "required", "exact_text_observed": "partial"},
                ],
                "end_screen": {"required": False},
            })
            checks = {finding.check for finding in report.findings}
            self.assertFalse(report.passed)
            self.assertTrue({"voice", "visual_pacing", "avatar", "physical_coherence", "exact_text"}.issubset(checks))


if __name__ == "__main__":
    unittest.main()
