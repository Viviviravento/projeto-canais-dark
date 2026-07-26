"""Validate local YouTube publication packages before upload."""

from __future__ import annotations

import hashlib
import json
import re
import struct
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
OPERATION_ROOT = Path(__file__).resolve().parents[1]
PACKAGE_DIR = Path(__file__).resolve().parent
CHANNEL_CONFIG_PATH = PACKAGE_DIR / "configuracao-canal-v1.json"
SRT_TIME = re.compile(
    r"(?P<h>\d{2}):(?P<m>\d{2}):(?P<s>\d{2}),(?P<ms>\d{3})"
    r" --> "
    r"(?P<eh>\d{2}):(?P<em>\d{2}):(?P<es>\d{2}),(?P<ems>\d{3})"
)


def fail(message: str) -> None:
    raise ValueError(message)


def resolve_recorded_path(recorded_path: str) -> Path:
    """Resolve registros históricos sem reescrever manifests de produção."""
    path = Path(recorded_path)
    if path.parts and path.parts[0] == "Canal Religioso":
        return OPERATION_ROOT.joinpath(*path.parts[1:])
    return PROJECT_ROOT / path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def png_dimensions(path: Path) -> tuple[int, int]:
    with path.open("rb") as handle:
        header = handle.read(24)
    if header[:8] != b"\x89PNG\r\n\x1a\n":
        fail(f"Thumbnail is not a PNG: {path}")
    return struct.unpack(">II", header[16:24])


def seconds(groups: tuple[str, str, str, str]) -> float:
    hours, minutes, secs, millis = map(int, groups)
    return hours * 3600 + minutes * 60 + secs + millis / 1000


def validate_srt(path: Path, duration: float) -> dict:
    blocks = re.split(r"\r?\n\r?\n", path.read_text(encoding="utf-8").strip())
    previous_end = -1.0
    longest_line = 0
    last_end = 0.0

    for expected_index, block in enumerate(blocks, start=1):
        lines = block.splitlines()
        if len(lines) < 3:
            fail(f"Malformed SRT cue in {path}: {block!r}")
        if int(lines[0]) != expected_index:
            fail(f"Non-sequential SRT cue in {path}: {lines[0]}")
        match = SRT_TIME.fullmatch(lines[1])
        if not match:
            fail(f"Malformed SRT timestamp in {path}: {lines[1]}")
        values = match.groups()
        start = seconds(values[:4])
        end = seconds(values[4:])
        if start < previous_end:
            fail(f"Overlapping SRT cues in {path} at cue {expected_index}")
        if end <= start:
            fail(f"Non-positive SRT cue in {path} at cue {expected_index}")
        previous_end = end
        last_end = end
        longest_line = max(longest_line, *(len(line) for line in lines[2:]))

    if last_end > duration + 0.1:
        fail(f"SRT exceeds master duration in {path}: {last_end:.3f} > {duration:.3f}")
    return {"cues": len(blocks), "last_end_seconds": last_end, "longest_line": longest_line}


def validate_package(path: Path) -> dict:
    package = json.loads(path.read_text(encoding="utf-8"))
    video_id = package["video_id"]
    title = package["title"]
    description = package["description"]
    tags = package["tags"]
    duration = float(package["technical_identity"]["duration_seconds"])

    if len(title) > 100:
        fail(f"{video_id}: title exceeds 100 characters")
    if len(description) > 5000:
        fail(f"{video_id}: description exceeds 5000 characters")
    if sum(len(tag) for tag in tags) + max(0, len(tags) - 1) > 500:
        fail(f"{video_id}: tags exceed the 500-character field")

    chapters = package["chapters"]
    starts = [int(chapter["start_seconds"]) for chapter in chapters]
    if not starts or starts[0] != 0:
        fail(f"{video_id}: chapters must begin at 00:00")
    if any(current <= previous for previous, current in zip(starts, starts[1:])):
        fail(f"{video_id}: chapter times must be strictly increasing")
    if any(current - previous < 10 for previous, current in zip(starts, starts[1:])):
        fail(f"{video_id}: every chapter must last at least 10 seconds")
    if starts[-1] >= duration:
        fail(f"{video_id}: last chapter starts after the master ends")

    master_path = resolve_recorded_path(package["files"]["publication_master"])
    caption_path = resolve_recorded_path(package["files"]["captions"])
    thumbnail_path = resolve_recorded_path(package["files"]["thumbnail"])
    for asset_path in (master_path, caption_path, thumbnail_path):
        if not asset_path.is_file():
            fail(f"{video_id}: missing file {asset_path}")

    dimensions = png_dimensions(thumbnail_path)
    aspect_ratio = dimensions[0] / dimensions[1]
    if dimensions[0] < 640 or dimensions[1] < 360 or abs(aspect_ratio - (16 / 9)) > 0.01:
        fail(f"{video_id}: thumbnail must be at least 640x360 and approximately 16:9, got {dimensions}")
    if thumbnail_path.stat().st_size > 2_000_000:
        fail(f"{video_id}: thumbnail exceeds 2,000,000 bytes")

    master_hash = sha256(master_path)
    thumbnail_hash = sha256(thumbnail_path)
    if master_hash != package["technical_identity"]["master_sha256"]:
        fail(f"{video_id}: master SHA-256 mismatch")
    if thumbnail_hash != package["technical_identity"]["thumbnail_sha256"]:
        fail(f"{video_id}: thumbnail SHA-256 mismatch")

    captions = validate_srt(caption_path, duration)
    return {
        "video_id": video_id,
        "title_characters": len(title),
        "description_characters": len(description),
        "tag_field_characters": sum(len(tag) for tag in tags) + max(0, len(tags) - 1),
        "chapters": len(chapters),
        "thumbnail": {
            "dimensions": f"{dimensions[0]}x{dimensions[1]}",
            "aspect_ratio": round(aspect_ratio, 4),
            "bytes": thumbnail_path.stat().st_size,
        },
        "captions": captions,
        "result": "PASS",
    }


def validate_channel_configuration(path: Path) -> dict:
    config = json.loads(path.read_text(encoding="utf-8"))
    channel = config["channel"]
    handle = channel["primary_handle"].removeprefix("@")
    if not 3 <= len(handle) <= 30:
        fail("Channel handle must contain between 3 and 30 characters")

    playlist = config["initial_playlist"]
    if len(playlist["title"]) > 150:
        fail("Initial playlist title exceeds 150 characters")
    if len(playlist["description"]) > 5000:
        fail("Initial playlist description exceeds 5000 characters")

    limits = {
        "profile_picture": {"max_bytes": 15_000_000, "minimum": 98, "square": True},
        "banner": {"max_bytes": 6_000_000, "dimensions": (2560, 1440)},
        "watermark": {"max_bytes": 1_000_000, "minimum": 150, "square": True},
    }
    assets: dict[str, dict] = {}
    for name, rules in limits.items():
        asset = config["branding"][name]
        asset_path = resolve_recorded_path(asset["path"])
        if not asset_path.is_file():
            fail(f"Missing channel branding asset: {asset_path}")
        dimensions = png_dimensions(asset_path)
        if asset_path.stat().st_size > rules["max_bytes"]:
            fail(f"Channel branding asset exceeds size limit: {asset_path}")
        if rules.get("square") and dimensions[0] != dimensions[1]:
            fail(f"Channel branding asset must be square: {asset_path}")
        if rules.get("minimum") and min(dimensions) < rules["minimum"]:
            fail(f"Channel branding asset is too small: {asset_path}")
        if rules.get("dimensions") and dimensions != rules["dimensions"]:
            fail(f"Unexpected channel branding dimensions for {asset_path}: {dimensions}")
        if sha256(asset_path) != asset["sha256"]:
            fail(f"Channel branding SHA-256 mismatch: {asset_path}")
        assets[name] = {
            "dimensions": f"{dimensions[0]}x{dimensions[1]}",
            "bytes": asset_path.stat().st_size,
        }

    if not config["monetization_preflight"]["synthetic_disclosure_required"]:
        fail("Synthetic content disclosure guardrail must remain enabled")

    return {
        "name": channel["public_name"],
        "handle": channel["primary_handle"],
        "description_characters": len(channel["description"]),
        "playlist_title_characters": len(playlist["title"]),
        "branding": assets,
        "result": "PASS",
    }


def main() -> int:
    package_paths = sorted(PACKAGE_DIR.glob("*-publicacao-v1.json"))
    if not package_paths:
        print("No v1 publication packages found.", file=sys.stderr)
        return 2
    results = [validate_package(path) for path in package_paths]
    channel = validate_channel_configuration(CHANNEL_CONFIG_PATH)
    print(json.dumps({"videos": results, "channel": channel}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
