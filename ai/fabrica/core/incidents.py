from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Literal


IncidentState = Literal["detected", "frozen", "investigating", "fixed", "verified", "blocked", "resumed"]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class Hypothesis:
    statement: str
    status: str = "untested"
    evidence_refs: list[str] = field(default_factory=list)


@dataclass
class IntegrationIncident:
    incident_id: str
    integration: str
    operation: str
    symptoms: list[str]
    checkpoint: str
    idempotency_key: str
    paid_call: bool = False
    publication: bool = False
    deletion: bool = False
    opened_at: str = field(default_factory=utc_now)
    closed_at: str | None = None
    state: IncidentState = "detected"
    hypotheses: list[Hypothesis] = field(default_factory=list)
    root_cause: str | None = None
    correction: str | None = None
    cycles_without_new_evidence: int = 0
    regression_status: str = "pending"
    regression_checks: list[str] = field(default_factory=list)

    def freeze(self) -> None:
        self.state = "frozen"

    def add_hypothesis(self, statement: str) -> Hypothesis:
        if self.state not in {"frozen", "investigating"}:
            raise ValueError("A operacao deve estar congelada antes do diagnostico")
        hypothesis = Hypothesis(statement=statement)
        self.hypotheses.append(hypothesis)
        self.state = "investigating"
        return hypothesis

    def conclude_cycle(self, *, new_evidence: bool) -> None:
        self.cycles_without_new_evidence = 0 if new_evidence else self.cycles_without_new_evidence + 1
        if self.cycles_without_new_evidence >= 3:
            self.state = "blocked"

    def confirm_cause(self, hypothesis: Hypothesis, evidence_refs: list[str]) -> None:
        if not evidence_refs:
            raise ValueError("Causa nao pode ser confirmada sem evidencia")
        hypothesis.status = "confirmed"
        hypothesis.evidence_refs = evidence_refs
        self.root_cause = hypothesis.statement

    def apply_fix(self, correction: str) -> None:
        if not self.root_cause:
            raise ValueError("Correcao exige causa comprovada")
        self.correction = correction
        self.state = "fixed"

    def verify(self, checks: list[str], passed: bool) -> None:
        if self.state != "fixed":
            raise ValueError("Regressao so pode ser executada depois da correcao")
        self.regression_checks = checks
        self.regression_status = "passed" if passed else "failed"
        self.state = "verified" if passed else "investigating"

    def resume(self) -> None:
        if self.state != "verified":
            raise ValueError("Operacao so pode retomar depois da regressao aprovada")
        self.state = "resumed"
        self.closed_at = utc_now()

    def as_contract(self) -> dict:
        return {
            "schema_version": "1.0.0",
            "incident_id": self.incident_id,
            "integration": self.integration,
            "operation": self.operation,
            "opened_at": self.opened_at,
            "closed_at": self.closed_at,
            "state": self.state,
            "symptoms": self.symptoms,
            "hypotheses": [hypothesis.__dict__ for hypothesis in self.hypotheses],
            "root_cause": self.root_cause,
            "correction": self.correction,
            "cycles_without_new_evidence": self.cycles_without_new_evidence,
            "resume_point": {"checkpoint": self.checkpoint, "idempotency_key": self.idempotency_key},
            "side_effect_guard": {
                "paid_call": self.paid_call,
                "publication": self.publication,
                "deletion": self.deletion,
            },
            "regression": {"status": self.regression_status, "checks": self.regression_checks},
        }

