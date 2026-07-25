from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Literal


GateState = Literal["full", "sampled", "automatic", "restored"]
PERMANENT_HUMAN_SCOPES = {
    "credentials",
    "captcha_2fa",
    "account_ownership",
    "destructive_action",
    "deletion",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class GatePolicy:
    gate_id: str
    scope: str
    state: GateState = "full"
    permanent_human: bool = False
    reason: str = "Gate criado sem historico suficiente."
    evidence: list[str] = field(default_factory=list)
    clean_runs: int = 0
    sampled_approvals: int = 0
    clean_runs_to_sampled: int = 3
    sampled_approvals_to_automatic: int = 6
    updated_at: str = field(default_factory=utc_now)
    notifications: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.scope in PERMANENT_HUMAN_SCOPES:
            self.permanent_human = True
            self.state = "full"

    def _transition(self, state: GateState, reason: str) -> str | None:
        if self.permanent_human and state != "full":
            return None
        if self.state == state:
            return None
        previous = self.state
        self.state = state
        self.reason = reason
        self.updated_at = utc_now()
        message = f"Gate {self.gate_id}: {previous} -> {state}. {reason}"
        self.notifications.append(message)
        return message

    def record_clean_run(self, evidence_ref: str, *, sampled_approved: bool = False) -> str | None:
        self.evidence.append(evidence_ref)
        self.updated_at = utc_now()
        if self.permanent_human:
            return None

        if self.state in {"full", "restored"}:
            self.clean_runs += 1
            if self.clean_runs >= self.clean_runs_to_sampled:
                self.sampled_approvals = 0
                return self._transition("sampled", f"{self.clean_runs} execucoes comparaveis limpas.")
            return None

        if self.state == "sampled" and sampled_approved:
            self.sampled_approvals += 1
            if self.sampled_approvals >= self.sampled_approvals_to_automatic:
                return self._transition("automatic", f"{self.sampled_approvals} aprovacoes amostradas.")
        return None

    def restore(self, reason: str, evidence_ref: str, *, critical: bool = False) -> str | None:
        self.evidence.append(evidence_ref)
        self.clean_runs = 0
        self.sampled_approvals = 0
        if self.permanent_human:
            self.reason = reason
            self.updated_at = utc_now()
            return None
        if critical or self.state in {"sampled", "automatic"}:
            return self._transition("restored", reason)
        self.reason = reason
        self.updated_at = utc_now()
        return None

    def as_contract(self) -> dict:
        return {
            "schema_version": "1.0.0",
            "gate_id": self.gate_id,
            "scope": self.scope,
            "state": self.state,
            "permanent_human": self.permanent_human,
            "evidence": list(self.evidence),
            "reason": self.reason,
            "promotion": {
                "clean_runs_to_sampled": self.clean_runs_to_sampled,
                "sampled_approvals_to_automatic": self.sampled_approvals_to_automatic,
            },
            "restoration": {
                "critical_defect_immediate": True,
                "triggers": ["critical_defect", "model_change", "price_change", "confidence_loss"],
            },
            "counters": {
                "clean_runs": self.clean_runs,
                "sampled_approvals": self.sampled_approvals,
            },
            "updated_at": self.updated_at,
        }

    def snapshot(self) -> dict:
        return asdict(self)

