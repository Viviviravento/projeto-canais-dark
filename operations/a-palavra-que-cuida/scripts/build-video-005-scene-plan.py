from __future__ import annotations

import json
import re
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
CHANNEL_ROOT = PROJECT_ROOT / "operations" / "a-palavra-que-cuida"
ALIGNMENT_PATH = CHANNEL_ROOT / "05_audio" / "video-005" / "v1" / "master-alignment-1.05x.json"
CITATIONS_PATH = CHANNEL_ROOT / "02_roteiros" / "video-005-citacoes-acf-v1.json"
OUTPUT_PATH = CHANNEL_ROOT / "06_edicao" / "video-005" / "scene-plan-v1.json"


BLOCK_ASSETS = {
    "01-antes-da-discussao-o-comeco": [
        "stock/s05-storm-sky.mp4",
        "stock/s03-sea-aerial.mp4",
        "library/biblia_fe/p001-biblia-mesa-v1.png",
    ],
    "02-deus-comeca-onde-ha-vazio": [
        "stock/s01-barren-rock.mp4",
        "stock/s05-storm-sky.mp4",
        "library/cotidiano_brasileiro/p001-peso-mental-v1.png",
    ],
    "03-a-palavra-que-ilumina": [
        "stock/s03-sea-aerial.mp4",
        "library/cotidiano_brasileiro/v002-amanhecer-presente-v1.png",
        "library/cotidiano_brasileiro/p001-caminhada-v1.png",
    ],
    "04-o-mundo-nao-e-descartavel": [
        "stock/s04-waves-rock.mp4",
        "stock/s06-wild-goats.mp4",
        "library/biblico_historico/v002-jesus-aves-flores-v2.png",
    ],
    "05-valor-antes-da-performance": [
        "library/apoio_relacoes/p001-escuta-v1.png",
        "library/apoio_relacoes/p001-carga-compartilhada-v1.png",
        "library/cotidiano_brasileiro/p001-reflexo-v1.png",
    ],
    "06-muito-bom-e-responsavel": [
        "stock/s03-sea-aerial.mp4",
        "library/objetos_cenarios/p001-maos-em-pausa-v1.png",
        "library/cotidiano_brasileiro/p001-dia-em-andamento-v1.png",
    ],
    "07-trabalhar-e-guardar": [
        "library/objetos_cenarios/p001-tarefas-v1.png",
        "library/cotidiano_brasileiro/p001-fechar-trabalho-v1.png",
        "video004/brazil/b05-mesa-com-croche-v1.png",
    ],
    "08-o-comeco-ensina-descanso": [
        "library/cotidiano_brasileiro/p001-pausa-v1.png",
        "library/cotidiano_brasileiro/p001-chegar-cansada-v1.png",
        "video004/brazil/b08-tempo-de-ouvir-v1.png",
    ],
    "09-fechamento-e-convite": [
        "library/biblia_fe/p001-biblia-mesa-v1.png",
        "library/apoio_relacoes/p001-carga-compartilhada-v1.png",
        "library/cotidiano_brasileiro/v002-amanhecer-presente-v1.png",
    ],
}


def card_filename(reference: str) -> str:
    return "acf-" + re.sub(r"[^a-z0-9]+", "-", reference.casefold()).strip("-") + ".png"


def main() -> None:
    alignment = json.loads(ALIGNMENT_PATH.read_text(encoding="utf-8"))
    citations = json.loads(CITATIONS_PATH.read_text(encoding="utf-8"))["direct_acf_citations"]
    scenes = []
    for block in alignment["blocks"]:
        scenes.append(
            {
                "id": f"block-{block['block_id']}",
                "block_id": block["block_id"],
                "start_seconds": block["start_seconds"],
                "end_seconds": block["end_seconds"],
                "assets": BLOCK_ASSETS[block["block_id"]],
                "maximum_static_seconds": 7,
                "vertical_recomposition": "planned",
            }
        )

    scripture_cards = []
    for citation in citations:
        matched_block = None
        for block in alignment["blocks"]:
            text = "".join(block["characters"])
            lead_start = text.find(citation["spoken_lead_in"])
            quote_start = text.find(citation["text"])
            if lead_start >= 0 and quote_start >= 0:
                matched_block = (block, quote_start, quote_start + len(citation["text"]))
                break
        if matched_block is None:
            raise RuntimeError(f"Citation not found in master alignment: {citation['reference']}")
        block, start_index, end_index = matched_block
        scripture_cards.append(
            {
                "id": f"scripture-{card_filename(citation['reference']).removesuffix('.png')}",
                "reference": citation["reference"],
                "text": citation["text"],
                "source": f"04_assets/video-005/scripture_cards/{card_filename(citation['reference'])}",
                "block_id": block["block_id"],
                "start_seconds": block["character_start_times_seconds"][start_index],
                "end_seconds": block["character_end_times_seconds"][end_index - 1],
                "must_match_spoken_audio": True,
                "complete_reference_required": True,
                "trigger_policy": "show only while the verse text itself is being read",
            }
        )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(
            {
                "schema_version": "1.0.0",
                "video_id": "video-005",
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
                },
                "publication_cta_requirements": {
                    "audio_contains_comment_question": True,
                    "audio_contains_next_video_direction": False,
                    "must_add_next_video_direction_in_end_screen": True,
                    "must_add_two_native_youtube_video_elements": True,
                    "must_add_pinned_comment_question": True,
                },
                "scenes": scenes,
                "scripture_cards": scripture_cards,
                "asset_strategy": "Use existing stock nature clips and approved Brazilian daily-life assets before requesting paid generation.",
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "scenes": len(scenes),
                "scripture_cards": len(scripture_cards),
                "output": str(OUTPUT_PATH),
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
