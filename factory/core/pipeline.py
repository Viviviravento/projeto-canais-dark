from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Iterable, Literal


StageStatus = Literal["pending", "in_progress", "completed", "not_applicable", "blocked"]

OPERATION_STAGES = (
    "entrada",
    "evidencias",
    "tese",
    "desenho_do_piloto",
    "instanciacao",
    "piloto",
    "publicacao_observacao",
    "cristalizacao",
)

CONTENT_STAGES = (
    "tema",
    "pesquisa",
    "blueprint",
    "artefato_performatico",
    "plano_producao_custo",
    "aquisicao",
    "composicao",
    "qa_pacote",
    "publicacao_distribuicao",
    "aprendizado",
)

# Aliases v1 preservados para contratos e execucoes historicas.
CHANNEL_STAGES = OPERATION_STAGES
VIDEO_STAGES = CONTENT_STAGES


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class StageRecord:
    id: str
    status: StageStatus = "pending"
    reason: str | None = None
    artifacts: list[str] = field(default_factory=list)
    updated_at: str = field(default_factory=utc_now)

    def validate(self) -> None:
        if self.status == "not_applicable" and not (self.reason or "").strip():
            raise ValueError(f"Etapa {self.id}: not_applicable exige justificativa")
        if self.status == "blocked" and not (self.reason or "").strip():
            raise ValueError(f"Etapa {self.id}: blocked exige justificativa")


class FactoryRun:
    """Checkpoint explicito para uma execucao generica ou um fluxo v1 legado."""

    def __init__(
        self,
        run_id: str,
        kind: Literal["operation", "content", "channel", "video"],
        metadata: dict[str, Any] | None = None,
    ):
        self.run_id = run_id
        self.kind = kind
        self.created_at = utc_now()
        self.updated_at = self.created_at
        self.metadata = metadata or {}
        stage_ids = OPERATION_STAGES if kind in {"operation", "channel"} else CONTENT_STAGES
        self.stages = {stage_id: StageRecord(stage_id) for stage_id in stage_ids}

    @property
    def required_stages(self) -> tuple[str, ...]:
        return OPERATION_STAGES if self.kind in {"operation", "channel"} else CONTENT_STAGES

    def mark(
        self,
        stage_id: str,
        status: StageStatus,
        *,
        reason: str | None = None,
        artifacts: Iterable[str] = (),
    ) -> StageRecord:
        if stage_id not in self.stages:
            raise KeyError(f"Etapa desconhecida para {self.kind}: {stage_id}")
        record = self.stages[stage_id]
        record.status = status
        record.reason = reason
        record.artifacts = list(artifacts)
        record.updated_at = utc_now()
        record.validate()
        self.updated_at = record.updated_at
        return record

    def validate(self, *, require_terminal: bool = False) -> None:
        if tuple(self.stages) != self.required_stages:
            raise ValueError("A execucao perdeu, reordenou ou adicionou macroetapas")
        for record in self.stages.values():
            record.validate()
            if require_terminal and record.status not in {"completed", "not_applicable"}:
                raise ValueError(f"Etapa ainda nao terminal: {record.id} ({record.status})")

    def as_dict(self) -> dict[str, Any]:
        self.validate()
        return {
            "schema_version": "1.0.0",
            "run_id": self.run_id,
            "kind": self.kind,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "metadata": self.metadata,
            "stages": [asdict(self.stages[stage_id]) for stage_id in self.required_stages],
        }


def validate_run_payload(payload: dict[str, Any], *, require_terminal: bool = False) -> None:
    kind = payload.get("kind")
    if kind not in {"operation", "content", "channel", "video"}:
        raise ValueError(f"Tipo de execucao invalido: {kind}")
    required = OPERATION_STAGES if kind in {"operation", "channel"} else CONTENT_STAGES
    stages = payload.get("stages") or []
    ids = tuple(stage.get("id") for stage in stages)
    if ids != required:
        raise ValueError("A execucao perdeu, reordenou ou adicionou macroetapas")
    allowed = {"pending", "in_progress", "completed", "not_applicable", "blocked"}
    for stage in stages:
        status = stage.get("status")
        if status not in allowed:
            raise ValueError(f"Estado invalido em {stage.get('id')}: {status}")
        if status in {"not_applicable", "blocked"} and not str(stage.get("reason") or "").strip():
            raise ValueError(f"Etapa {stage.get('id')}: {status} exige justificativa")
        if require_terminal and status not in {"completed", "not_applicable"}:
            raise ValueError(f"Etapa ainda nao terminal: {stage.get('id')} ({status})")
