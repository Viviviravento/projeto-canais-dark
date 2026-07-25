from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CHANNEL_ROOT = PROJECT_ROOT / "Canal Religioso"
sys.path.insert(0, str(PROJECT_ROOT))

from ai.fabrica.core.contracts import validate_contract  # noqa: E402


def load(relative: str) -> dict:
    return json.loads((CHANNEL_ROOT / relative).read_text(encoding="utf-8"))


def check(condition: bool, label: str, failures: list[str], passes: list[str]) -> None:
    (passes if condition else failures).append(label)


def main() -> None:
    failures: list[str] = []
    passes: list[str] = []

    contracts = [
        ("TopicCandidate", "02_roteiros/video-003-topic-v1.json"),
        ("ContentBlueprint", "02_roteiros/video-003-blueprint-v1.json"),
        ("ContentBlueprint", "02_roteiros/video-003-vertical-01-blueprint-v1.json"),
        ("ContentBlueprint", "02_roteiros/video-003-vertical-02-blueprint-v1.json"),
        ("MediaRequirement", "06_edicao/video-003/media-requirement-v1.json"),
        ("CostQuote", "06_edicao/video-003/custos/elevenlabs-v1.json"),
        ("CostQuote", "06_edicao/video-003/custos/heygen-v1.json"),
        ("CostQuote", "06_edicao/video-003/custos/kling-v1.json"),
        ("CostQuote", "06_edicao/video-003/custos/elevenlabs-calibracao-v2.json"),
        ("IntegrationIncident", "06_edicao/video-003/incidentes/pexels-search-order-v1.json"),
        ("IntegrationIncident", "06_edicao/video-003/incidentes/elevenlabs-semantics-v1.json"),
        ("GatePolicy", "06_edicao/video-003/gate-audio-semantico-v1.json"),
    ]
    for contract, relative in contracts:
        try:
            validate_contract(contract, load(relative))
            passes.append(f"contract:{relative}")
        except Exception as exc:  # surfaced in report with the exact contract path
            failures.append(f"contract:{relative}:{exc}")

    citation_manifest = load("02_roteiros/video-003-citacoes-acf-v1.json")
    performance = load("02_roteiros/video-003-performance-v1.json")
    scene_plan = load("06_edicao/video-003/scene-plan-v1.json")
    spoken = "\n".join(block["text"] for block in performance["blocks"])
    scripture_scenes = {
        item["scripture"]["reference"]: item["scripture"]
        for item in scene_plan["scenes"]
        if "scripture" in item
    }
    for citation in citation_manifest["direct_acf_citations"]:
        reference = citation["reference"]
        check(citation["spoken_lead_in"] in spoken, f"lead-in completo:{reference}", failures, passes)
        check(citation["text"] in spoken, f"citacao falada exata:{reference}", failures, passes)
        check(reference in scripture_scenes, f"cena de citacao:{reference}", failures, passes)
        if reference in scripture_scenes:
            check(scripture_scenes[reference]["text"] == citation["text"], f"texto visual integral:{reference}", failures, passes)

    source_counts = Counter(
        item["source"] for item in scene_plan["scenes"]
        if item.get("source") and not str(item["source"]).startswith("planned:")
    )
    max_reuse = int(scene_plan["visual_policy"]["maximum_base_asset_reuse"])
    for source, count in source_counts.items():
        check(count <= max_reuse, f"reuso {count}/{max_reuse}:{source}", failures, passes)
        check((CHANNEL_ROOT / source).is_file(), f"asset existe:{source}", failures, passes)

    check(scene_plan["asset_summary"]["generated_stills_available"] >= 18, "18 imagens geradas", failures, passes)
    check(scene_plan["asset_summary"]["stock_clips_reviewed"] >= 6, "6 stocks revisados", failures, passes)
    check(scene_plan["visual_policy"]["end_screen_recommendation_slots"] == 2, "dois destinos na tela final", failures, passes)

    publication = load("08_publicacao/video-003-publicacao-v0.1.json")
    check(publication["end_screen"]["recommendation_slots"] == 2, "publicacao com dois destinos", failures, passes)
    check(publication["acf"]["direct_units_master"] == len(citation_manifest["direct_acf_citations"]), "controle ACF do master", failures, passes)

    thumbnail = CHANNEL_ROOT / "08_publicacao/video-003-thumbnail-v1.png"
    with Image.open(thumbnail) as image:
        check(image.size == (1280, 720), "thumbnail 1280x720", failures, passes)
    check(thumbnail.stat().st_size < 2_000_000, "thumbnail abaixo de 2 MB", failures, passes)

    lineage = load("04_assets/video-003/generated/lineage-v1.json")
    for asset in lineage["assets"]:
        path = CHANNEL_ROOT / asset["file"]
        digest = hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else ""
        check(digest == asset["sha256"], f"linhagem:{asset['asset_id']}", failures, passes)

    report = {
        "schema_version": "1.0.0",
        "video_id": "video-003",
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "state": "passed" if not failures else "failed",
        "passes": passes,
        "failures": failures,
        "paid_calls_started": False,
    }
    output = CHANNEL_ROOT / "06_edicao/video-003/preproduction-qa-v1.json"
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{report['state']}: {len(passes)} passes, {len(failures)} failures")
    if failures:
        for failure in failures:
            print(f"FAIL {failure}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
