"""Derive a conservative, citation-safe visual plan for video 008."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CHANNEL = ROOT / "operations" / "a-palavra-que-cuida"
ALIGNMENT = CHANNEL / "05_audio" / "video-008" / "v1" / "master-alignment-1.07x.json"
CITATIONS = CHANNEL / "02_roteiros" / "video-008-citacoes-acf-v1.json"
OUTPUT = CHANNEL / "06_edicao" / "video-008" / "scene-plan-v1.json"
ASSETS = {
    "01-quando-a-vergonha-chama-seu-nome": ["video-008/images/v01-lembranca-na-cozinha-com-croche-v1.png", "video-008/images/v05-choro-sem-espetaculo-v1.png"],
    "02-jesus-viu-pedro-antes-da-queda": ["video-008/images/v02-pedro-antes-do-patio-v1.png", "video-008/images/v03-verdade-no-corredor-v1.png"],
    "03-o-medo-no-patio": ["video-008/images/v04-pedro-perto-do-fogo-v1.png", "video-008/images/v03-verdade-no-corredor-v1.png"],
    "04-o-olhar-o-choro-e-a-verdade": ["video-008/images/v05-choro-sem-espetaculo-v1.png", "video-008/images/v04-pedro-perto-do-fogo-v1.png"],
    "05-jesus-encontra-pedro-junto-ao-mar": ["video-008/images/v06-encontro-a-beira-do-mar-v1.png", "video-008/images/v05-choro-sem-espetaculo-v1.png"],
    "06-a-pergunta-que-aponta-para-frente": ["video-008/images/v06-encontro-a-beira-do-mar-v1.png", "video-008/images/v07-passo-novo-pela-manha-v1.png"],
    "07-como-comecar-a-recomecar": ["video-008/images/v03-verdade-no-corredor-v1.png", "video-008/images/v07-passo-novo-pela-manha-v1.png"],
    "08-fechamento-e-convite": ["video-008/images/v07-passo-novo-pela-manha-v1.png", "video-008/images/v01-lembranca-na-cozinha-com-croche-v1.png"],
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
            scripture_cards.append({"id": f"scripture-{filename(citation['reference']).removesuffix('.png')}", "reference": citation["reference"], "text": citation["text"], "source": f"04_assets/video-008/scripture_cards/{filename(citation['reference'])}", "block_id": block["block_id"], "start_seconds": block["character_start_times_seconds"][start], "end_seconds": block["character_end_times_seconds"][end - 1], "must_match_spoken_audio": True, "complete_reference_required": True, "trigger_policy": "show only while the verse text itself is being read"})
            break
        else:
            raise RuntimeError(f"Citation missing from master alignment: {citation['reference']}")
    payload = {"schema_version": "1.0.0", "video_id": "video-008", "timing_state": "derived_from_master_alignment_1.07x", "master_duration_seconds": alignment["master_duration_seconds"], "visual_policy": {"maximum_static_seconds": 7, "maximum_base_asset_reuse": 2, "avatar_only_while_speaking": True, "scripture_display_must_match_spoken_quote": True, "scripture_cards_only_during_direct_verse_reading": True, "editorial_text_cards": False, "end_screen_seconds": 15, "end_screen_fixed_boxes": False, "end_screen_native_youtube_recommendations": 2, "end_screen_handle": "@apalavraquecuidabr"}, "publication_cta_requirements": {"audio_contains_comment_question": True, "audio_contains_next_video_direction": True, "must_add_two_native_youtube_video_elements": True, "must_add_pinned_comment_question": True}, "scenes": scenes, "scripture_cards": scripture_cards, "asset_strategy": "Use only approved video-008 stills. Scripture cards are reserved exclusively for direct verse readings."}
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"scenes": len(scenes), "scripture_cards": len(scripture_cards), "output": str(OUTPUT)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
