from __future__ import annotations

import json
import math
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CHANNEL = ROOT / "operations" / "a-palavra-que-cuida"
PROJECT = ROOT / "tools" / "OpenMontage" / "projects" / "a-palavra-que-cuida-video-011"
PUBLIC = ROOT / "tools" / "OpenMontage" / "remotion-composer" / "public" / "video-011"
ALIGNMENT = CHANNEL / "05_audio" / "video-011" / "v1" / "master-alignment-1.07x.json"
IMAGE_MANIFEST = CHANNEL / "04_assets" / "video-011" / "images" / "manifest-v1.json"
CARD_MANIFEST = CHANNEL / "04_assets" / "video-011" / "scripture_cards" / "manifest.json"
PLAN = CHANNEL / "06_edicao" / "video-011" / "scene-plan-v1.json"
MUSIC = ROOT / "tools" / "OpenMontage" / "projects" / "a-palavra-que-cuida-video-003" / "public" / "music" / "classical-6-jonny-s-mixkit.mp3"


BLOCK_ASSETS = {
    "01": ["video-011/images/v01-porta-e-mala.png", "video-011/images/v07-proximo-passo.png"],
    "02": ["video-011/images/v02-a-partida.png", "video-011/images/v01-porta-e-mala.png"],
    "03": ["video-011/images/v03-tornando-em-si.png", "video-011/images/v07-proximo-passo.png"],
    "04": ["video-011/images/v04-o-pai-corre.png", "video-011/images/v06-conversa-com-limites.png"],
    "05": ["video-011/images/v05-quem-ficou.png", "video-011/images/v06-conversa-com-limites.png"],
    "06": ["video-011/images/v06-conversa-com-limites.png", "video-011/images/v05-quem-ficou.png"],
    "07": ["video-011/images/v07-proximo-passo.png", "video-011/images/v06-conversa-com-limites.png"],
    "08": ["video-011/images/v01-porta-e-mala.png", "video-011/images/v07-proximo-passo.png"],
}


def copy_one(source: Path, destination: Path) -> None:
    if not source.exists():
        raise FileNotFoundError(source)
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def block_text(block: dict) -> str:
    return "".join(block["characters"])


def locate_quote(block: dict, quote: str) -> tuple[float, float]:
    text = block_text(block)
    start_index = text.find(quote)
    if start_index < 0:
        normalized_text = re.sub(r"\s+", " ", text).strip()
        normalized_quote = re.sub(r"\s+", " ", quote).strip()
        start_index = normalized_text.find(normalized_quote)
        if start_index < 0:
            raise ValueError(f"Citação não encontrada no bloco {block['block_id']}")
        raise ValueError(f"Citação encontrada apenas com normalização no bloco {block['block_id']}")
    end_index = start_index + len(quote) - 1
    starts = block["character_start_times_seconds"]
    ends = block["character_end_times_seconds"]
    return round(starts[start_index], 6), round(ends[end_index], 6)


def build_scripture_cards(alignment: dict, card_manifest: dict) -> list[dict]:
    cards = []
    for card in card_manifest["cards"]:
        matching_blocks = [block for block in alignment["blocks"] if card["text"] in block_text(block)]
        if len(matching_blocks) != 1:
            raise ValueError(f"Esperado um único bloco para {card['reference']}, encontrado {len(matching_blocks)}")
        block = matching_blocks[0]
        start, end = locate_quote(block, card["text"])
        cards.append(
            {
                "id": f"scripture-acf-{card['file'].removesuffix('.png')}",
                "reference": card["reference"],
                "text": card["text"],
                "source": f"04_assets/video-011/scripture_cards/{card['file']}",
                "block_id": block["block_id"],
                "start_seconds": start,
                "end_seconds": end,
                "must_match_spoken_audio": True,
                "complete_reference_required": True,
                "trigger_policy": "show only while the verse text itself is being read",
            }
        )
    return cards


def captions(blocks: list[dict], card_ranges: list[tuple[float, float]]) -> list[dict]:
    captions_out = []
    for block in blocks:
        text = block_text(block)
        starts = block["character_start_times_seconds"]
        ends = block["character_end_times_seconds"]
        words = [(match.group(), starts[match.start()], ends[match.end() - 1]) for match in re.finditer(r"\S+", text)]
        group = []
        for word in words:
            group.append(word)
            phrase = " ".join(item[0] for item in group)
            terminal = bool(re.search(r"[,.!?;:]$", word[0]))
            if len(group) < 2 or not (terminal or len(group) >= 4 or len(phrase) >= 34):
                continue
            start, end = group[0][1], group[-1][2]
            if not any(start < card_end and end > card_start for card_start, card_end in card_ranges):
                captions_out.append({"id": f"caption-{len(captions_out) + 1:04d}", "start": round(start, 3), "end": round(end, 3), "text": phrase})
            group = []
        if group:
            start, end = group[0][1], group[-1][2]
            if not any(start < card_end and end > card_start for card_start, card_end in card_ranges):
                captions_out.append({"id": f"caption-{len(captions_out) + 1:04d}", "start": round(start, 3), "end": round(end, 3), "text": " ".join(item[0] for item in group)})
    for current, following in zip(captions_out, captions_out[1:]):
        current["end"] = round(min(current["end"], following["start"] - 0.01), 3)
    return captions_out


def build_scenes(plan: dict) -> list[dict]:
    scenes = []
    for block in plan["scenes"]:
        start, end = float(block["start_seconds"]), float(block["end_seconds"])
        count = math.ceil((end - start) / 5.8)
        for index in range(count):
            begin = round(start + (end - start) * index / count, 3)
            finish = round(start + (end - start) * (index + 1) / count, 3)
            scenes.append(
                {
                    "id": f"scene-{len(scenes) + 1:03d}",
                    "start": begin,
                    "end": finish,
                    "focus": ["center", "left center", "right center"][index % 3],
                    "asset": f"video-011/assets/{block['assets'][index % len(block['assets'])].split('/', 1)[1]}",
                    "media": "image",
                    "shade": 0.045,
                }
            )
    for card in plan["scripture_cards"]:
        source = Path(card["source"])
        scenes.append(
            {
                "id": card["id"],
                "start": round(float(card["start_seconds"]), 3),
                "end": round(float(card["end_seconds"]), 3),
                "asset": f"video-011/assets/scripture/{source.name}",
                "media": "image",
                "focus": "center",
                "shade": 0,
            }
        )
    return scenes


def copy_assets(plan: dict) -> None:
    copy_one(CHANNEL / "05_audio" / "video-011" / "v1" / "video-011-narracao-v1-1.07x-master.wav", PUBLIC / "audio" / "narracao-producao.wav")
    copy_one(MUSIC, PUBLIC / "music" / MUSIC.name)
    for block in plan["scenes"]:
        for asset in block["assets"]:
            source = CHANNEL / "04_assets" / asset
            destination = PUBLIC / "assets" / Path(*asset.split("/", 1)[1].split("/"))
            copy_one(source, destination)
    for scripture in plan["scripture_cards"]:
        source = CHANNEL / scripture["source"]
        copy_one(source, PUBLIC / "assets" / "scripture" / source.name)


def build_project_files() -> None:
    PROJECT.mkdir(parents=True, exist_ok=True)
    source_project = ROOT / "tools" / "OpenMontage" / "projects" / "a-palavra-que-cuida-video-009"
    for name in ["CompositionV2.tsx", "RootV2.tsx", "index-v2.tsx"]:
        target = PROJECT / name
        text = (source_project / name).read_text(encoding="utf-8").replace("Video009", "Video011").replace("video-009", "video-011")
        target.write_text(text, encoding="utf-8")


def main() -> None:
    alignment = json.loads(ALIGNMENT.read_text(encoding="utf-8"))
    image_manifest = json.loads(IMAGE_MANIFEST.read_text(encoding="utf-8"))
    card_manifest = json.loads(CARD_MANIFEST.read_text(encoding="utf-8"))
    cards = build_scripture_cards(alignment, card_manifest)
    blocks_by_id = {block["block_id"]: block for block in alignment["blocks"]}
    scene_blocks = []
    for section, assets in BLOCK_ASSETS.items():
        matching = [block for block in alignment["blocks"] if block["block_id"].startswith(f"{section}-")]
        if len(matching) != 1:
            raise ValueError(f"Bloco de áudio ausente ou duplicado para a seção {section}")
        block = matching[0]
        scene_blocks.append(
            {
                "id": f"block-{block['block_id']}",
                "block_id": block["block_id"],
                "start_seconds": block["start_seconds"],
                "end_seconds": block["end_seconds"],
                "assets": assets,
                "maximum_static_seconds": 7,
                "vertical_recomposition": "planned",
            }
        )
    plan = {
        "schema_version": "1.0.0",
        "video_id": "video-011",
        "timing_state": "derived_from_master_alignment_1.07x",
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
            "audio_contains_next_video_direction": True,
            "must_add_two_native_youtube_video_elements": True,
            "must_add_pinned_comment_question": True,
        },
        "scenes": scene_blocks,
        "scripture_cards": cards,
        "asset_strategy": "Use only approved video-011 stills. Scripture cards are reserved exclusively for direct verse readings.",
        "approved_image_assets": [asset for item in image_manifest["assets"] for asset in [f"04_assets/video-011/images/{item['file']}"]],
    }
    copy_assets(plan)
    build_project_files()
    card_ranges = [(card["start_seconds"], card["end_seconds"]) for card in cards]
    total = float(alignment["master_duration_seconds"])
    timeline_cards = [{**card, "start": card["start_seconds"], "end": card["end_seconds"]} for card in cards]
    timeline = {
        "fps": 30,
        "width": 1920,
        "height": 1080,
        "totalSeconds": round(total, 6),
        "endScreenStart": round(total - 15, 6),
        "visualSourceTempo": 1,
        "scenes": build_scenes(plan),
        "specialScenes": [],
        "scriptures": timeline_cards,
        "captions": [caption for caption in captions(alignment["blocks"], card_ranges) if caption["end"] <= total - 15],
        "tags": [],
    }
    PLAN.parent.mkdir(parents=True, exist_ok=True)
    PLAN.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (PROJECT / "timeline-v2.json").write_text(json.dumps(timeline, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"project": str(PROJECT), "public": str(PUBLIC), "scenes": len(timeline["scenes"]), "scriptures": len(cards), "captions": len(timeline["captions"]), "total_seconds": timeline["totalSeconds"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
