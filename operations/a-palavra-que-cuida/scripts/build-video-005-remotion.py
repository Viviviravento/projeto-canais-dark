from __future__ import annotations

import json
import math
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CHANNEL = ROOT / "operations" / "a-palavra-que-cuida"
SOURCE_PROJECT = ROOT / "tools" / "OpenMontage" / "projects" / "a-palavra-que-cuida-video-004"
PROJECT = ROOT / "tools" / "OpenMontage" / "projects" / "a-palavra-que-cuida-video-005"
PUBLIC = ROOT / "tools" / "OpenMontage" / "remotion-composer" / "public" / "video-005"
ALIGNMENT = CHANNEL / "05_audio" / "video-005" / "v1" / "master-alignment-1.05x.json"
SCENE_PLAN = CHANNEL / "06_edicao" / "video-005" / "scene-plan-v1.json"


ASSET_ROOTS = {
    "stock": CHANNEL / "04_assets" / "video-003" / "stock" / "selected",
    "library": CHANNEL / "04_assets" / "biblioteca_imagens" / "curadas",
    "video004": CHANNEL / "04_assets" / "video-004" / "generated",
}


def copy_one(source: Path, target: Path) -> None:
    if not source.exists():
        raise FileNotFoundError(source)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def copy_assets(plan: dict) -> None:
    copy_one(
        CHANNEL / "05_audio" / "video-005" / "v1" / "video-005-narracao-v1-1.05x-master.wav",
        PUBLIC / "audio" / "narracao-producao.wav",
    )
    copy_one(
        ROOT
        / "tools"
        / "OpenMontage"
        / "projects"
        / "a-palavra-que-cuida-video-003"
        / "public"
        / "music"
        / "classical-6-jonny-s-mixkit.mp3",
        PUBLIC / "music" / "classical-6-jonny-s-mixkit.mp3",
    )
    for scene in plan["scenes"]:
        for asset in scene["assets"]:
            family, relative = asset.split("/", 1)
            copy_one(ASSET_ROOTS[family] / relative, PUBLIC / "assets" / family / relative)
    for scripture in plan["scripture_cards"]:
        source = CHANNEL / scripture["source"]
        copy_one(source, PUBLIC / "assets" / "scripture" / source.name)


def captions(blocks: list[dict], card_ranges: list[tuple[float, float]]) -> list[dict]:
    result = []
    for block in blocks:
        text = "".join(block["characters"])
        starts = block["character_start_times_seconds"]
        ends = block["character_end_times_seconds"]
        words = [(match.group(), starts[match.start()], ends[match.end() - 1]) for match in re.finditer(r"\S+", text)]
        group = []
        for word in words:
            group.append(word)
            phrase = " ".join(item[0] for item in group)
            ends_phrase = bool(re.search(r"[,.!?;:]$", word[0]))
            if len(group) < 2 or not (ends_phrase or len(group) >= 4 or len(phrase) >= 34):
                continue
            start, end = group[0][1], group[-1][2]
            if not any(start < card_end and end > card_start for card_start, card_end in card_ranges):
                result.append(
                    {
                        "id": f"caption-{len(result) + 1:04d}",
                        "start": round(start, 3),
                        "end": round(end, 3),
                        "text": phrase,
                    }
                )
            group = []
        if group:
            start, end = group[0][1], group[-1][2]
            if not any(start < card_end and end > card_start for card_start, card_end in card_ranges):
                result.append(
                    {
                        "id": f"caption-{len(result) + 1:04d}",
                        "start": round(start, 3),
                        "end": round(end, 3),
                        "text": " ".join(item[0] for item in group),
                    }
                )
    for current, following in zip(result, result[1:]):
        current["end"] = round(min(current["end"], following["start"] - 0.01), 3)
    return result


def asset_scene(asset: str) -> dict:
    family, relative = asset.split("/", 1)
    media = "video" if relative.lower().endswith(".mp4") else "image"
    return {
        "asset": f"video-005/assets/{family}/{relative}",
        "media": media,
        "focus": "center",
        "shade": 0.035 if media == "video" else 0.045,
    }


def build_scenes(plan: dict) -> list[dict]:
    scenes = []
    for block in plan["scenes"]:
        choices = block["assets"]
        start = float(block["start_seconds"])
        end = float(block["end_seconds"])
        count = math.ceil((end - start) / 5.8)
        for index in range(count):
            begin = round(start + (end - start) * index / count, 3)
            finish = round(start + (end - start) * (index + 1) / count, 3)
            chosen = choices[index % len(choices)]
            scene = {
                "id": f"scene-{len(scenes) + 1:03d}",
                "start": begin,
                "end": finish,
                "focus": ["center", "left center", "right center"][index % 3],
                **asset_scene(chosen),
            }
            if scene["media"] == "video":
                scene["startFromSeconds"] = round((index * 2.7) % 12, 3)
            scenes.append(scene)
    for item in plan["scripture_cards"]:
        source = Path(item["source"])
        scenes.append(
            {
                "id": item["id"],
                "start": round(float(item["start_seconds"]), 3),
                "end": round(float(item["end_seconds"]), 3),
                "asset": f"video-005/assets/scripture/{source.name}",
                "media": "image",
                "focus": "center",
                "shade": 0,
            }
        )
    return scenes


def build_project_files() -> None:
    PROJECT.mkdir(parents=True, exist_ok=True)
    for name in ["CompositionV2.tsx", "RootV2.tsx", "index-v2.tsx"]:
        shutil.copy2(SOURCE_PROJECT / name, PROJECT / name)
    composition = PROJECT / "CompositionV2.tsx"
    text = composition.read_text(encoding="utf-8")
    text = re.sub(
        r"const EndScreen: React\.FC = \(\) => \{.*?\n\};\n\nconst FinalFade",
        """const EndScreen: React.FC = () => {
  const frame = useCurrentFrame();
  const enter = interpolate(frame, [0, 10], [0, 1], {extrapolateRight: "clamp"});

  return (
    <AbsoluteFill style={{pointerEvents: "none"}}>
      <AbsoluteFill
        style={{
          background:
            "radial-gradient(circle at center, rgba(16,31,24,.68), rgba(5,9,7,.72))",
          opacity: enter,
        }}
      />
      <div
        style={{
          position: "absolute",
          left: "50%",
          top: 250,
          transform: "translateX(-50%)",
          color: palette.cream,
          fontFamily: "Georgia, serif",
          fontSize: 58,
          fontWeight: 800,
          letterSpacing: 1,
          textAlign: "center",
          opacity: enter,
          textShadow: "0 8px 24px rgba(0,0,0,.38)",
        }}
      >
        A Palavra Que Cuida
      </div>
      <div
        style={{
          position: "absolute",
          left: "50%",
          top: 344,
          transform: "translateX(-50%)",
          color: palette.softGold,
          fontFamily: "Arial, sans-serif",
          fontSize: 34,
          fontWeight: 900,
          textAlign: "center",
          opacity: enter,
        }}
      >
        @apalavraquecuidabr
      </div>
      <div
        style={{
          position: "absolute",
          left: "50%",
          top: 432,
          transform: "translateX(-50%)",
          width: 1180,
          color: palette.cream,
          fontFamily: "Arial, sans-serif",
          fontSize: 33,
          fontWeight: 800,
          lineHeight: 1.28,
          textAlign: "center",
          opacity: enter,
        }}
      >
        Continue por um dos vídeos sugeridos na tela e conte nos comentários o que Gênesis mais falou com você hoje.
      </div>
    </AbsoluteFill>
  );
};

const FinalFade""",
        text,
        flags=re.DOTALL,
    )
    text = text.replace("export const Video003: React.FC", "export const Video005: React.FC")
    text = text.replace('staticFile("video-004/audio/narracao-producao.wav")', 'staticFile("video-005/audio/narracao-producao.wav")')
    text = text.replace('staticFile("video-004/music/classical-6-jonny-s-mixkit.mp3")', 'staticFile("video-005/music/classical-6-jonny-s-mixkit.mp3")')
    composition.write_text(text, encoding="utf-8")

    root = (PROJECT / "RootV2.tsx").read_text(encoding="utf-8")
    root = root.replace('import {Video003} from "./CompositionV2";', 'import {Video005} from "./CompositionV2";')
    root = root.replace("id=\"APalavraQueCuidaVideo003V2\"", "id=\"APalavraQueCuidaVideo005V1\"")
    root = root.replace("component={Video003}", "component={Video005}")
    (PROJECT / "RootV2.tsx").write_text(root, encoding="utf-8")


def main() -> None:
    alignment = json.loads(ALIGNMENT.read_text(encoding="utf-8"))
    plan = json.loads(SCENE_PLAN.read_text(encoding="utf-8"))
    copy_assets(plan)
    build_project_files()
    card_ranges = [(item["start_seconds"], item["end_seconds"]) for item in plan["scripture_cards"]]
    master_duration = float(alignment["master_duration_seconds"])
    total_seconds = round(master_duration + 5, 6)
    clean_captions = [
        caption
        for caption in captions(alignment["blocks"], card_ranges)
        if caption["end"] <= max(0, master_duration - 15)
    ]
    timeline = {
        "fps": 30,
        "width": 1920,
        "height": 1080,
        "totalSeconds": total_seconds,
        "endScreenStart": round(max(0, master_duration - 15), 6),
        "visualSourceTempo": 1,
        "scenes": build_scenes(plan),
        "specialScenes": [],
        "scriptures": [],
        "captions": clean_captions,
        "tags": [],
    }
    (PROJECT / "timeline-v2.json").write_text(
        json.dumps(timeline, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "project": str(PROJECT),
                "public": str(PUBLIC),
                "scenes": len(timeline["scenes"]),
                "captions": len(timeline["captions"]),
                "total_seconds": total_seconds,
                "end_screen_start": timeline["endScreenStart"],
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
