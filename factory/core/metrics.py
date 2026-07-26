from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .contracts import validate_contract


class ImmutableRecordStore:
    """Armazena fatos e diagnosticos em JSONL somente por append."""

    def __init__(self, root: Path | str):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.observations = self.root / "metric_observations.jsonl"
        self.decisions = self.root / "learning_decisions.jsonl"

    def append_observation(self, payload: dict[str, Any]) -> None:
        validate_contract("MetricObservation", payload)
        self._append_unique(self.observations, "observation_id", payload)

    def append_decision(self, payload: dict[str, Any]) -> None:
        validate_contract("LearningDecision", payload)
        self._append_unique(self.decisions, "decision_id", payload, composite=("decision_id", "version"))

    @staticmethod
    def _append_unique(path: Path, key: str, payload: dict[str, Any], composite: tuple[str, ...] | None = None) -> None:
        identity = tuple(payload[field] for field in composite) if composite else payload[key]
        if path.exists():
            for line in path.read_text(encoding="utf-8").splitlines():
                existing = json.loads(line)
                existing_identity = tuple(existing[field] for field in composite) if composite else existing[key]
                if existing_identity == identity:
                    raise ValueError(f"Registro imutavel duplicado: {identity}")
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")

