from __future__ import annotations

import json
import math
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CHANNEL = ROOT / "operations" / "a-palavra-que-cuida"
SOURCE_PROJECT = ROOT / "tools" / "OpenMontage" / "projects" / "a-palavra-que-cuida-video-006"
PROJECT = ROOT / "tools" / "OpenMontage" / "projects" / "a-palavra-que-cuida-video-007"
PUBLIC = ROOT / "tools" / "OpenMontage" / "remotion-composer" / "public" / "video-007"
ALIGNMENT = CHANNEL / "05_audio" / "video-007" / "v1" / "master-alignment-1.07x.json"
SCENE_PLAN = CHANNEL / "06_edicao" / "video-007" / "scene-plan-v1.json"
MUSIC = ROOT / "tools" / "OpenMontage" / "projects" / "a-palavra-que-cuida-video-003" / "public" / "music" / "classical-6-jonny-s-mixkit.mp3"

ASSET_ROOTS = {
    "video-007": CHANNEL / "04_assets" / "video-007",
}


def copy_one(source: Path, target: Path) -> None:
    if not source.exists():
        raise FileNotFoundError(source)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def copy_assets(plan: dict) -> None:
    copy_one(CHANNEL / "05_audio" / "video-007" / "v1" / "video-007-narracao-v1-1.07x-master.wav", PUBLIC / "audio" / "narracao-producao.wav")
    copy_one(MUSIC, PUBLIC / "music" / MUSIC.name)
    for block in plan["scenes"]:
        for asset in block["assets"]:
            family, relative = asset.split("/", 1)
            copy_one(ASSET_ROOTS[family] / relative, PUBLIC / "assets" / family / relative)
    for scripture in plan["scripture_cards"]:
        source = CHANNEL / scripture["source"]
        copy_one(source, PUBLIC / "assets" / "scripture" / source.name)


def captions(blocks: list[dict], card_ranges: list[tuple[float, float]]) -> list[dict]:
    output = []
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
                output.append({"id": f"caption-{len(output) + 1:04d}", "start": round(start, 3), "end": round(end, 3), "text": phrase})
            group = []
        if group:
            start, end = group[0][1], group[-1][2]
            if not any(start < card_end and end > card_start for card_start, card_end in card_ranges):
                output.append({"id": f"caption-{len(output) + 1:04d}", "start": round(start, 3), "end": round(end, 3), "text": " ".join(item[0] for item in group)})
    for current, following in zip(output, output[1:]):
        current["end"] = round(min(current["end"], following["start"] - 0.01), 3)
    return output


def asset_scene(asset: str) -> dict:
    family, relative = asset.split("/", 1)
    return {"asset": f"video-007/assets/{family}/{relative}", "media": "image", "focus": "center", "shade": 0.045}


def build_scenes(plan: dict) -> list[dict]:
    scenes = []
    for block in plan["scenes"]:
        choices = block["assets"]
        start, end = float(block["start_seconds"]), float(block["end_seconds"])
        count = math.ceil((end - start) / 5.8)
        for index in range(count):
            begin = round(start + (end - start) * index / count, 3)
            finish = round(start + (end - start) * (index + 1) / count, 3)
            scenes.append({
                "id": f"scene-{len(scenes) + 1:03d}",
                "start": begin,
                "end": finish,
                "focus": ["center", "left center", "right center"][index % 3],
                **asset_scene(choices[index % len(choices)]),
            })
    for item in plan["scripture_cards"]:
        source = Path(item["source"])
        scenes.append({
            "id": item["id"],
            "start": round(float(item["start_seconds"]), 3),
            "end": round(float(item["end_seconds"]), 3),
            "asset": f"video-007/assets/scripture/{source.name}",
            "media": "image",
            "focus": "center",
            "shade": 0,
        })
    return scenes


def build_project_files() -> None:
    PROJECT.mkdir(parents=True, exist_ok=True)
    for name in ["CompositionV2.tsx", "RootV2.tsx", "index-v2.tsx"]:
        shutil.copy2(SOURCE_PROJECT / name, PROJECT / name)
    composition = PROJECT / "CompositionV2.tsx"
    text = composition.read_text(encoding="utf-8")
    text = text.replace("Video006", "Video007").replace("video-006", "video-007")
    composition.write_text(text, encoding="utf-8")
    root = PROJECT / "RootV2.tsx"
    root.write_text(root.read_text(encoding="utf-8").replace("Video006", "Video007").replace("Video006V1", "Video007V1"), encoding="utf-8")


def main() -> None:
    alignment = json.loads(ALIGNMENT.read_text(encoding="utf-8"))
    plan = json.loads(SCENE_PLAN.read_text(encoding="utf-8"))
    copy_assets(plan)
    build_project_files()
    card_ranges = [(item["start_seconds"], item["end_seconds"]) for item in plan["scripture_cards"]]
    master_duration = float(alignment["master_duration_seconds"])
    timeline = {
        "fps": 30,
        "width": 1920,
        "height": 1080,
        "totalSeconds": round(master_duration, 6),
        "endScreenStart": round(master_duration - 15, 6),
        "visualSourceTempo": 1,
        "scenes": build_scenes(plan),
        "specialScenes": [],
        "scriptures": [],
        "captions": [caption for caption in captions(alignment["blocks"], card_ranges) if caption["end"] <= master_duration - 15],
        "tags": [],
    }
    (PROJECT / "timeline-v2.json").write_text(json.dumps(timeline, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"project": str(PROJECT), "public": str(PUBLIC), "scenes": len(timeline["scenes"]), "captions": len(timeline["captions"]), "total_seconds": timeline["totalSeconds"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
