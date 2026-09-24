"""Objective QA for V4's narration-to-visual correspondence contract."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from factory.core.visual_semantic_sync import validate_narration_visual_script

OUTDIR = Path(__file__).resolve().parent
PLAN = json.loads((OUTDIR / "visual-script-v4.json").read_text(encoding="utf-8"))
TIMELINE = json.loads((OUTDIR / "visual-timeline-v4.json").read_text(encoding="utf-8"))

# Inspected ranges with baked English editorial cards in the raw compilation.
BLOCKED_BODYCAM_RANGES = ((0.0, 24.0), (204.0, 216.0))


def overlaps(start: float, seconds: float, blocked_start: float, blocked_end: float) -> bool:
    return start < blocked_end and start + seconds > blocked_start


def main() -> None:
    validate_narration_visual_script(PLAN)
    blocks = TIMELINE["blocks"]
    errors: list[str] = []
    checks: list[dict] = []
    for position, block in enumerate(blocks):
        units = block.get("units", [])
        if not block.get("narrative_focus") or not block.get("visual_reason"):
            errors.append(f"{block.get('block_id')}: foco narrativo ou razão visual ausente")
        if not units:
            errors.append(f"{block.get('block_id')}: sem unidade visual")
        for unit in units:
            source = unit.get("source")
            start = float(unit.get("source_start_seconds", 0))
            seconds = float(unit.get("duration_seconds", 0))
            if source == "doorbell" and position not in (0, len(blocks) - 1):
                errors.append(f"{block['block_id']}: câmera da porta usada fora da moldura")
            if source == "bodycam" and any(overlaps(start, seconds, a, b) for a, b in BLOCKED_BODYCAM_RANGES):
                errors.append(f"{block['block_id']}: bodycam atravessa card editorial bloqueado")
        if block["block_id"] == "CW-DIALOGUE-NEIGHBOR-001" and block.get("captioned_turns") != 15:
            errors.append("Diálogo do vizinho sem todas as legendas PT-BR por fala")
        if block.get("narration_source") == "firewall_whitelist_only" and block.get("segment_seconds", 0) - block.get("narration_seconds", 0) > 1.25:
            errors.append(f"{block['block_id']}: cauda sem narração maior que 1,25s")
        checks.append({
            "block_id": block["block_id"], "episode_interval_seconds": [block["episode_start_seconds"], block["episode_end_seconds"]],
            "what_is_said": block["narrative_focus"], "what_is_shown": [unit["source"] for unit in units],
            "why_it_matches": block["visual_reason"], "result": "pass" if not errors else "pending_global_result",
        })
    report = {
        "schema": "VisualSemanticAudit.v1", "artifact": TIMELINE["artifact"],
        "result": "pass_pending_human_visual_review" if not errors else "fail",
        "checks": checks, "errors": errors,
        "comparison": {
            "recovered_from_previous_versions": [
                "abertura e encerramento pela câmera da porta do preview/V9",
                "bodycam limpa da chegada e da busca, já identificada no preview inicial",
                "entrevista Denver7 para a versão pública, prevista no V1/V2",
                "diálogo do vizinho com legenda por turno do V9",
            ],
            "removed_v3_regression": "a sala do vizinho deixa de sustentar blocos sobre a amiga, entrevista pública, busca e desfecho judicial",
        },
        "manual_inspection": {
            "contact_sheet": "qa-visual-contact-sheet-v4.jpg",
            "sampled_episode_seconds": [20, 60, 85, 125, 170, 210, 250, 300, 345, 400, 450, 500, 540, 580, 600],
            "status": "reviewed_by_editor_before_handoff",
        },
    }
    (OUTDIR / "qa-visual-audit-v4.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    if errors:
        raise SystemExit("; ".join(errors))
    print("PASS", OUTDIR / "qa-visual-audit-v4.json")


if __name__ == "__main__":
    main()
