from __future__ import annotations

import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
CHANNEL_ROOT = PROJECT_ROOT / "operations" / "a-palavra-que-cuida"
ALIGNMENT_PATH = CHANNEL_ROOT / "05_audio" / "video-004" / "v1" / "master-alignment-1.05x.json"
CITATIONS_PATH = CHANNEL_ROOT / "02_roteiros" / "video-004-citacoes-acf-v1.json"
OUTPUT_PATH = CHANNEL_ROOT / "06_edicao" / "video-004" / "scene-plan-v1.json"


BLOCK_ASSETS = {
    "01-a-pergunta-que-existe-entre-duas-cenas": ["planned:avatar-opening", "planned:editorial-time-gap", "h02-caminho-a-jerusalem-v1"],
    "02-o-que-o-evangelho-mostra": ["planned:graphic-what-is-written", "h01-jesus-no-templo-v1"],
    "03-uma-familia-que-volta-todos-os-anos": ["h02-caminho-a-jerusalem-v1", "planned:jerusalem-road-detail"],
    "04-o-menino-no-templo": ["h03-procura-em-jerusalem-v1", "h01-jesus-no-templo-v1"],
    "05-uma-resposta-que-abre-o-centro": ["h01-jesus-no-templo-v1", "planned:family-listening-detail"],
    "06-o-versiculo-que-impede-dois-erros": ["h04-retorno-a-nazare-v1", "planned:nazareth-home-exterior"],
    "07-crescer-tambem-e-parte-da-historia": ["b01-escuta-em-familia-v1", "b02-aprender-com-constancia-v1", "b03-pedido-de-perdao-v1", "b04-crescimento-em-dias-comuns-v1"],
    "08-o-silencio-dos-anos": ["planned:graphic-silence-is-not-invention", "planned:nazareth-still-life"],
    "09-fechamento-e-convite": ["planned:avatar-closing", "planned:end-screen-two-slots"],
}


def card_filename(reference: str) -> str:
    return "acf-" + reference.casefold().replace(" ", "-").replace(":", "-") + ".png"


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
                matched_block = (block, lead_start, quote_start + len(citation["text"]))
                break
        if matched_block is None:
            raise RuntimeError(f"Citation not found in master alignment: {citation['reference']}")
        block, start_index, end_index = matched_block
        scripture_cards.append(
            {
                "id": f"scripture-{citation['reference'].casefold().replace(' ', '-').replace(':', '-')}",
                "reference": citation["reference"],
                "text": citation["text"],
                "source": f"04_assets/video-004/scripture_cards/{card_filename(citation['reference'])}",
                "block_id": block["block_id"],
                "start_seconds": block["character_start_times_seconds"][start_index],
                "end_seconds": block["character_end_times_seconds"][end_index - 1],
                "must_match_spoken_audio": True,
                "complete_reference_required": True,
            }
        )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(
            {
                "schema_version": "1.0.0",
                "video_id": "video-004",
                "timing_state": "derived_from_master_alignment_1.05x",
                "master_duration_seconds": alignment["master_duration_seconds"],
                "visual_policy": {
                    "maximum_static_seconds": 7,
                    "maximum_base_asset_reuse": 2,
                    "avatar_only_while_speaking": True,
                    "scripture_display_must_match_spoken_quote": True,
                    "end_screen_seconds": 15,
                    "end_screen_recommendation_slots": 2,
                },
                "scenes": scenes,
                "scripture_cards": scripture_cards,
                "remaining_asset_families": ["historical details", "Brazilian applications", "stock literal", "editorial graphics", "avatar", "thumbnail"],
            },
            ensure_ascii=False,
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"scenes": len(scenes), "scripture_cards": len(scripture_cards), "output": str(OUTPUT_PATH)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
