from __future__ import annotations

import json
import re
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
CHANNEL_ROOT = PROJECT_ROOT / "operations" / "a-palavra-que-cuida"
ALIGNMENT_PATH = CHANNEL_ROOT / "05_audio" / "video-006" / "v1" / "master-alignment-1.05x.json"
CITATIONS_PATH = CHANNEL_ROOT / "02_roteiros" / "video-006-citacoes-acf-v1.json"
OUTPUT_PATH = CHANNEL_ROOT / "06_edicao" / "video-006" / "scene-plan-v1.json"


BLOCK_ASSETS = {
    "01-uma-casa-que-parece-conhecida": [
        "video-006/images/b01-pausa-na-cozinha-com-croche-v1.png",
        "video-006/images/h02-marta-servindo-v1.png",
        "library/biblia_fe/p001-biblia-mesa-v1.png",
    ],
    "02-maria-nao-esta-fugindo": [
        "video-006/images/h01-maria-em-escuta-v1.png",
        "library/biblico_historico/v002-jesus-ouvinte-mulher-v2.png",
        "library/cotidiano_brasileiro/p001-pausa-v1.png",
    ],
    "03-quando-o-servico-perde-o-centro": [
        "video-006/images/h02-marta-servindo-v1.png",
        "video-006/images/b02-responsabilidades-a-noite-v1.png",
        "library/cotidiano_brasileiro/p001-peso-mental-v1.png",
    ],
    "04-jesus-chama-pelo-nome": [
        "video-006/images/h01-maria-em-escuta-v1.png",
        "library/apoio_relacoes/p001-escuta-v1.png",
        "library/cotidiano_brasileiro/p001-reflexo-v1.png",
    ],
    "05-a-boa-parte-nao-sera-tirada": [
        "library/biblia_fe/p001-oracao-e-acao-v1.png",
        "library/cotidiano_brasileiro/p001-fechar-trabalho-v1.png",
        "library/objetos_cenarios/p001-maos-em-pausa-v1.png",
    ],
    "06-jesus-amava-marta": [
        "library/biblico_historico/v002-galileia-necessidades-v2.png",
        "library/apoio_relacoes/p001-escuta-v1.png",
        "library/biblia_fe/p001-entrega-v1.png",
    ],
    "07-a-casa-a-fe-e-a-sobrecarga": [
        "video-006/images/b01-pausa-na-cozinha-com-croche-v1.png",
        "video-006/images/b02-responsabilidades-a-noite-v1.png",
        "library/apoio_relacoes/p001-pedir-ajuda-v1.png",
    ],
    "08-como-escolher-a-boa-parte-hoje": [
        "video-006/images/b03-responsabilidade-compartilhada-v1.png",
        "library/cotidiano_brasileiro/p001-pausa-v1.png",
        "library/objetos_cenarios/p001-maos-em-pausa-v1.png",
    ],
    "09-fechamento-e-convite": [
        "video-006/images/b03-responsabilidade-compartilhada-v1.png",
        "library/biblia_fe/p001-biblia-mesa-v1.png",
        "library/cotidiano_brasileiro/v002-amanhecer-presente-v1.png",
    ],
}


def card_filename(reference: str) -> str:
    return "acf-" + re.sub(r"[^a-z0-9]+", "-", reference.casefold()).strip("-") + ".png"


def main() -> None:
    alignment = json.loads(ALIGNMENT_PATH.read_text(encoding="utf-8"))
    citations = json.loads(CITATIONS_PATH.read_text(encoding="utf-8"))["direct_acf_citations"]
    scenes = [
        {
            "id": f"block-{block['block_id']}",
            "block_id": block["block_id"],
            "start_seconds": block["start_seconds"],
            "end_seconds": block["end_seconds"],
            "assets": BLOCK_ASSETS[block["block_id"]],
            "maximum_static_seconds": 7,
            "vertical_recomposition": "planned",
        }
        for block in alignment["blocks"]
    ]
    scripture_cards = []
    for citation in citations:
        for block in alignment["blocks"]:
            text = "".join(block["characters"])
            quote_start = text.find(citation["text"])
            if quote_start >= 0:
                quote_end = quote_start + len(citation["text"])
                scripture_cards.append(
                    {
                        "id": f"scripture-{card_filename(citation['reference']).removesuffix('.png')}",
                        "reference": citation["reference"],
                        "text": citation["text"],
                        "source": f"04_assets/video-006/scripture_cards/{card_filename(citation['reference'])}",
                        "block_id": block["block_id"],
                        "start_seconds": block["character_start_times_seconds"][quote_start],
                        "end_seconds": block["character_end_times_seconds"][quote_end - 1],
                        "must_match_spoken_audio": True,
                        "complete_reference_required": True,
                        "trigger_policy": "show only while the verse text itself is being read",
                    }
                )
                break
        else:
            raise RuntimeError(f"Citation not found in master alignment: {citation['reference']}")
    payload = {
        "schema_version": "1.0.0",
        "video_id": "video-006",
        "timing_state": "derived_from_master_alignment_1.05x",
        "master_duration_seconds": alignment["master_duration_seconds"],
        "visual_policy": {
            "maximum_static_seconds": 7,
            "maximum_base_asset_reuse": 2,
            "avatar_only_while_speaking": True,
            "scripture_display_must_match_spoken_quote": True,
            "scripture_cards_only_during_direct_verse_reading": True,
            "editorial_text_cards": False,
            "end_screen_seconds": 15,
            "end_screen_fixed_boxes": False,
            "end_screen_native_youtube_recommendations": 2,
            "end_screen_handle": "@apalavraquecuidabr",
            "held_assets": ["video-006/images/b04-pausa-com-a-palavra-v1.png"],
        },
        "publication_cta_requirements": {
            "audio_contains_comment_question": True,
            "audio_contains_next_video_direction": True,
            "must_add_two_native_youtube_video_elements": True,
            "must_add_pinned_comment_question": True,
        },
        "scenes": scenes,
        "scripture_cards": scripture_cards,
        "asset_strategy": "Use approved video-006 stills and the curated library. Do not use the held b04 asset without human approval.",
    }
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"scenes": len(scenes), "scripture_cards": len(scripture_cards), "output": str(OUTPUT_PATH)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
