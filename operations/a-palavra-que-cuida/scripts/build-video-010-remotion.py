from __future__ import annotations

import json
import math
import shutil
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[3]
CHANNEL = ROOT / "operations" / "a-palavra-que-cuida"
PROJECT = ROOT / "tools" / "OpenMontage" / "projects" / "a-palavra-que-cuida-video-010"
PUBLIC = ROOT / "tools" / "OpenMontage" / "remotion-composer" / "public" / "video-010"
ALIGNMENT = CHANNEL / "05_audio" / "video-010" / "v1" / "master-alignment-1.07x.json"
PLAN = CHANNEL / "06_edicao" / "video-010" / "scene-plan-v1.json"
MUSIC = ROOT / "tools" / "OpenMontage" / "projects" / "a-palavra-que-cuida-video-003" / "public" / "music" / "classical-6-jonny-s-mixkit.mp3"


def copy_one(source: Path, destination: Path) -> None:
    if not source.exists():
        raise FileNotFoundError(source)
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def copy_assets(plan: dict) -> None:
    copy_one(CHANNEL / "05_audio" / "video-010" / "v1" / "video-010-narracao-v1-1.07x-master.wav", PUBLIC / "audio" / "narracao-producao.wav")
    copy_one(MUSIC, PUBLIC / "music" / MUSIC.name)
    for block in plan["scenes"]:
        for asset in block["assets"]:
            source = CHANNEL / "04_assets" / asset
            copy_one(source, PUBLIC / "assets" / asset)
    for scripture in plan["scripture_cards"]:
        source = CHANNEL / scripture["source"]
        copy_one(source, PUBLIC / "assets" / "scripture" / source.name)


def captions(blocks: list[dict], card_ranges: list[tuple[float, float]]) -> list[dict]:
    captions_out = []
    for block in blocks:
        text = "".join(block["characters"])
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
            scenes.append({"id": f"scene-{len(scenes) + 1:03d}", "start": begin, "end": finish, "focus": ["center", "left center", "right center"][index % 3], "asset": f"video-010/assets/{block['assets'][index % len(block['assets'])].split('/', 1)[1]}", "media": "image", "shade": 0.045})
    for card in plan["scripture_cards"]:
        source = Path(card["source"])
        scenes.append({"id": card["id"], "start": round(float(card["start_seconds"]), 3), "end": round(float(card["end_seconds"]), 3), "asset": f"video-010/assets/scripture/{source.name}", "media": "image", "focus": "center", "shade": 0})
    return scenes


def build_project_files() -> None:
    PROJECT.mkdir(parents=True, exist_ok=True)
    source_project = ROOT / "tools" / "OpenMontage" / "projects" / "a-palavra-que-cuida-video-009"
    for name in ["CompositionV2.tsx", "RootV2.tsx", "index-v2.tsx"]:
        target = PROJECT / name
        text = (source_project / name).read_text(encoding="utf-8").replace("Video009", "Video010").replace("video-009", "video-010").replace("Video009", "Video010")
        target.write_text(text, encoding="utf-8")


def main() -> None:
    alignment = json.loads(ALIGNMENT.read_text(encoding="utf-8"))
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    copy_assets(plan)
    build_project_files()
    card_ranges = [(card["start_seconds"], card["end_seconds"]) for card in plan["scripture_cards"]]
    total = float(alignment["master_duration_seconds"])
    timeline = {"fps": 30, "width": 1920, "height": 1080, "totalSeconds": round(total, 6), "endScreenStart": round(total - 15, 6), "visualSourceTempo": 1, "scenes": build_scenes(plan), "specialScenes": [], "scriptures": [], "captions": [caption for caption in captions(alignment["blocks"], card_ranges) if caption["end"] <= total - 15], "tags": []}
    (PROJECT / "timeline-v2.json").write_text(json.dumps(timeline, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"project": str(PROJECT), "public": str(PUBLIC), "scenes": len(timeline["scenes"]), "captions": len(timeline["captions"]), "total_seconds": timeline["totalSeconds"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
