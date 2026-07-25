"""Create a scene-level keyframe contact sheet without frame-by-frame review."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import tempfile
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    ffmpeg = shutil.which("ffmpeg")
    ffprobe = shutil.which("ffprobe")
    if not ffmpeg or not ffprobe:
        raise RuntimeError("ffmpeg and ffprobe are required")

    videos = sorted(args.input_dir.glob("*.mp4"))
    if not videos:
        raise ValueError("No MP4 files found")

    from PIL import Image, ImageDraw, ImageFont

    tile_width, tile_height = 420, 270
    canvas = Image.new("RGB", (tile_width * 3, tile_height * len(videos)), "#111111")
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.load_default()
    audit = []

    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        for row, video in enumerate(videos):
            duration = probe_duration(ffprobe, video)
            timestamps = [duration * ratio for ratio in (0.15, 0.5, 0.85)]
            for column, timestamp in enumerate(timestamps):
                frame = tmp_dir / f"{row}-{column}.jpg"
                subprocess.run(
                    [
                        ffmpeg,
                        "-v",
                        "error",
                        "-ss",
                        f"{timestamp:.3f}",
                        "-i",
                        str(video),
                        "-frames:v",
                        "1",
                        "-vf",
                        "scale=420:-2",
                        "-y",
                        str(frame),
                    ],
                    check=True,
                    timeout=60,
                )
                image = Image.open(frame).convert("RGB")
                image.thumbnail((tile_width, tile_height - 32))
                x = column * tile_width + (tile_width - image.width) // 2
                y = row * tile_height
                canvas.paste(image, (x, y))
                label = f"{video.name} | {timestamp:.1f}s"
                draw.rectangle(
                    (column * tile_width, y + tile_height - 32, (column + 1) * tile_width, y + tile_height),
                    fill="#111111",
                )
                draw.text((column * tile_width + 7, y + tile_height - 22), label, fill="white", font=font)
            audit.append({"file": str(video.resolve()), "duration_seconds": duration, "sample_ratios": [0.15, 0.5, 0.85]})

    args.output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(args.output, quality=88)
    args.output.with_suffix(".json").write_text(
        json.dumps({"schema_version": 1, "audit": audit}, indent=2) + "\n",
        encoding="utf-8",
    )
    return 0


def probe_duration(ffprobe: str, path: Path) -> float:
    completed = subprocess.run(
        [ffprobe, "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(path)],
        check=True,
        capture_output=True,
        text=True,
        timeout=30,
    )
    return float(completed.stdout.strip())


if __name__ == "__main__":
    raise SystemExit(main())
