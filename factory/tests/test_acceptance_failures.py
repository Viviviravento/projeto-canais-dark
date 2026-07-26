from __future__ import annotations

import unittest

from factory.core.browser_state import SelectorBreak, SelectorCandidate, classify_session, resolve_selector
from factory.core.incidents import IntegrationIncident


class FailureAcceptanceTests(unittest.TestCase):
    def test_expired_login_is_human_gate_not_unknown_page(self) -> None:
        health = classify_session(
            expected_account="channel-account",
            observed_account=None,
            studio_navigation_visible=False,
            login_visible=True,
        )
        self.assertEqual(health, "expired")

    def test_selector_break_uses_semantic_fallback_or_freezes(self) -> None:
        candidates = [
            SelectorCandidate("role_name", "button:Export"),
            SelectorCandidate("label", "Exportar dados"),
        ]
        resolved = resolve_selector(candidates, {"label": {"Exportar dados"}})
        self.assertEqual(resolved.strategy, "label")
        with self.assertRaises(SelectorBreak):
            resolve_selector(candidates, {})

    def test_paid_failure_resumes_without_repeating_side_effect(self) -> None:
        incident = IntegrationIncident(
            "paid-1", "video-provider", "generate", ["HTTP 402 after request submission"],
            "request_submitted", "provider-request-123", paid_call=True,
        )
        incident.freeze()
        hypothesis = incident.add_hypothesis("Provider recorded the job before returning the error")
        incident.confirm_cause(hypothesis, ["read-only-provider-history:job-456"])
        incident.apply_fix("Adopt the existing job ID instead of issuing another generation")
        incident.verify(["read-only-job-status", "artifact-download-check"], True)
        incident.resume()
        contract = incident.as_contract()
        self.assertTrue(contract["side_effect_guard"]["paid_call"])
        self.assertEqual(contract["resume_point"]["checkpoint"], "request_submitted")
        self.assertEqual(contract["state"], "resumed")


if __name__ == "__main__":
    unittest.main()

