from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CHANNEL = ROOT / "operations" / "a-palavra-que-cuida"
ALIGNMENT = CHANNEL / "05_audio" / "video-010" / "v1" / "master-alignment-1.07x.json"
CITATIONS = CHANNEL / "02_roteiros" / "video-010-citacoes-acf-v1.json"
OUTPUT = CHANNEL / "06_edicao" / "video-010" / "scene-plan-v1.json"
ASSETS = {
    "01-quando-o-barco-comeca-a-encher": ["video-010/images/v01-ansiedade-na-cozinha.png", "video-010/images/v02-barco-na-tempestade.png"],
    "02-a-travessia-nao-foi-um-erro": ["video-010/images/v02-barco-na-tempestade.png", "video-010/images/v01-ansiedade-na-cozinha.png"],
    "03-jesus-dormia": ["video-010/images/v03-jesus-dorme-no-barco.png", "video-010/images/v02-barco-na-tempestade.png"],
    "04-o-silencio-do-mar-nao-e-a-unica-resposta": ["video-010/images/v04-tempestade-se-acalma.png", "video-010/images/v03-jesus-dorme-no-barco.png"],
    "05-por-que-o-medo-aparece": ["video-010/images/v05-medo-na-vida-real.png", "video-010/images/v01-ansiedade-na-cozinha.png"],
    "06-entre-confianca-e-controle": ["video-010/images/v06-apoio-que-escuta.png", "video-010/images/v05-medo-na-vida-real.png"],
    "07-o-que-fica-depois-da-bonanca": ["video-010/images/v07-depois-da-chuva.png", "video-010/images/v06-apoio-que-escuta.png"],
    "08-fechamento-e-convite": ["video-010/images/v07-depois-da-chuva.png", "video-010/images/v01-ansiedade-na-cozinha.png"],
}


def filename(reference: str) -> str:
    return "acf-" + re.sub(r"[^a-z0-9]+", "-", reference.casefold()).strip("-") + ".png"


def main() -> None:
    alignment = json.loads(ALIGNMENT.read_text(encoding="utf-8"))
    citations = json.loads(CITATIONS.read_text(encoding="utf-8"))["direct_acf_citations"]
    scenes = [{"id": f"block-{block['block_id']}", "block_id": block["block_id"], "start_seconds": block["start_seconds"], "end_seconds": block["end_seconds"], "assets": ASSETS[block["block_id"]], "maximum_static_seconds": 7, "vertical_recomposition": "planned"} for block in alignment["blocks"]]
    scripture_cards = []
    for citation in citations:
        for block in alignment["blocks"]:
            text = "".join(block["characters"])
            start = text.find(citation["text"])
            if start < 0:
                continue
            end = start + len(citation["text"])
            scripture_cards.append({"id": f"scripture-{filename(citation['reference']).removesuffix('.png')}", "reference": citation["reference"], "text": citation["text"], "source": f"04_assets/video-010/scripture_cards/{filename(citation['reference'])}", "block_id": block["block_id"], "start_seconds": block["character_start_times_seconds"][start], "end_seconds": block["character_end_times_seconds"][end - 1], "must_match_spoken_audio": True, "complete_reference_required": True, "trigger_policy": "show only while the verse text itself is being read"})
            break
        else:
            raise RuntimeError(f"Citation missing from master alignment: {citation['reference']}")
    payload = {"schema_version": "1.0.0", "video_id": "video-010", "timing_state": "derived_from_master_alignment_1.07x", "master_duration_seconds": alignment["master_duration_seconds"], "visual_policy": {"maximum_static_seconds": 7, "maximum_base_asset_reuse": 2, "avatar_only_while_speaking": True, "scripture_display_must_match_spoken_quote": True, "scripture_cards_only_during_direct_verse_reading": True, "editorial_text_cards": False, "end_screen_seconds": 15, "end_screen_fixed_boxes": False, "end_screen_native_youtube_recommendations": 2, "end_screen_handle": "@apalavraquecuidabr"}, "publication_cta_requirements": {"audio_contains_comment_question": True, "audio_contains_next_video_direction": True, "must_add_two_native_youtube_video_elements": True, "must_add_pinned_comment_question": True}, "scenes": scenes, "scripture_cards": scripture_cards, "asset_strategy": "Use only approved video-010 stills. Scripture cards are reserved exclusively for direct verse readings."}
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"scenes": len(scenes), "scripture_cards": len(scripture_cards), "output": str(OUTPUT)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
