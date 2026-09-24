from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from .contracts import validate_contract
from .gates import GatePolicy


MISSING = "<missing>"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def configuration_fingerprint(configuration: dict[str, Any]) -> str:
    canonical = json.dumps(configuration, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def load_operation_manifest(path: str | Path) -> dict[str, Any]:
    payload = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("Manifesto de operacao deve ser um objeto YAML")
    validate_contract("OperationManifest", payload)
    return payload


def validate_baseline(payload: dict[str, Any]) -> None:
    validate_contract("Baseline", payload)
    if payload["clean_runs"] != len(payload["clean_run_refs"]):
        raise ValueError("clean_runs deve corresponder a clean_run_refs")
    fingerprint = payload.get("configuration_fingerprint")
    if fingerprint and fingerprint != configuration_fingerprint(payload["parameters"]):
        raise ValueError("configuration_fingerprint nao corresponde aos parametros")


def _value_at(payload: dict[str, Any], dotted_path: str) -> Any:
    current: Any = payload
    for component in dotted_path.split("."):
        if not isinstance(current, dict) or component not in current:
            return MISSING
        current = current[component]
    return current


@dataclass(frozen=True)
class BaselineChange:
    path: str
    approved: Any
    current: Any


@dataclass(frozen=True)
class BaselineAssessment:
    baseline_id: str
    reusable: bool
    status: str
    required_gate_state: str
    changes: tuple[BaselineChange, ...]

    def as_dict(self) -> dict[str, Any]:
        return {
            "baseline_id": self.baseline_id,
            "reusable": self.reusable,
            "status": self.status,
            "required_gate_state": self.required_gate_state,
            "changes": [asdict(change) for change in self.changes],
        }


def compare_baseline_configuration(
    baseline: dict[str, Any], current_configuration: dict[str, Any]
) -> BaselineAssessment:
    validate_baseline(baseline)
    if baseline["state"] != "approved":
        return BaselineAssessment(
            baseline_id=baseline["baseline_id"],
            reusable=False,
            status="baseline_not_approved",
            required_gate_state="restored",
            changes=(),
        )

    changes = tuple(
        BaselineChange(
            path=path,
            approved=_value_at(baseline["parameters"], path),
            current=_value_at(current_configuration, path),
        )
        for path in baseline["invalidation_triggers"]
        if _value_at(baseline["parameters"], path) != _value_at(current_configuration, path)
    )
    return BaselineAssessment(
        baseline_id=baseline["baseline_id"],
        reusable=not changes,
        status="approved" if not changes else "revalidation_required",
        required_gate_state="unchanged" if not changes else "restored",
        changes=changes,
    )


def enforce_baseline_assessment(
    assessment: BaselineAssessment,
    gate: GatePolicy,
    *,
    evidence_ref: str,
) -> str | None:
    """Restaura o gate quando a baseline nao pode ser reutilizada."""
    if assessment.reusable:
        return None
    changed = ", ".join(change.path for change in assessment.changes) or assessment.status
    return gate.restore(
        f"Baseline {assessment.baseline_id} exige revalidacao: {changed}.",
        evidence_ref,
        critical=True,
    )


def assess_clean_run(
    *,
    run_id: str,
    operation_id: str,
    evidence_artifacts: list[str],
    known_regression_accepted: bool = False,
    user_recalled_existing_rule: bool = False,
    avoidable_paid_retry: bool = False,
    gate_bypassed: bool = False,
    baseline_diverged_without_revalidation: bool = False,
    fundamental_defect_detected_only_in_final: bool = False,
    canonical_state_matches_execution: bool = True,
    recorded_at: str | None = None,
) -> dict[str, Any]:
    checks = {
        "known_regression_accepted": known_regression_accepted,
        "user_recalled_existing_rule": user_recalled_existing_rule,
        "avoidable_paid_retry": avoidable_paid_retry,
        "gate_bypassed": gate_bypassed,
        "baseline_diverged_without_revalidation": baseline_diverged_without_revalidation,
        "fundamental_defect_detected_only_in_final": fundamental_defect_detected_only_in_final,
        "canonical_state_mismatch": not canonical_state_matches_execution,
        "evidence_missing": not evidence_artifacts,
    }
    disqualifiers = [name for name, failed in checks.items() if failed]
    payload = {
        "schema_version": "1.0.0",
        "run_id": run_id,
        "operation_id": operation_id,
        "recorded_at": recorded_at or utc_now(),
        "clean": not disqualifiers,
        "disqualifiers": disqualifiers,
        "evidence_artifacts": list(evidence_artifacts),
        "canonical_state_matches_execution": canonical_state_matches_execution,
    }
    validate_contract("CleanRun", payload)
    return payload
