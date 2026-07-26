"""Download one reviewed Pexels candidate and preserve provenance."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


MAX_VIDEO_BYTES = 500 * 1024 * 1024


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("clip_id")
    parser.add_argument("output", type=Path)
    parser.add_argument("--openmontage-root", type=Path, required=True)
    parser.add_argument("--provenance", type=Path, required=True)
    args = parser.parse_args()

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    known = {row["source"] + "_" + row["source_id"] for row in manifest["candidates"]}
    if args.clip_id not in known:
        raise ValueError("Selection is not present in the reviewed candidate manifest")

    root = args.openmontage_root.resolve()
    sys.path.insert(0, str(root))
    from dotenv import load_dotenv

    load_dotenv(root / ".env")
    from tools.video.stock_sources.base import Candidate, SearchFilters
    from tools.video.stock_sources.pexels import PexelsSource

    source = PexelsSource()
    filters = SearchFilters(
        kind="video",
        min_duration=5,
        max_duration=40,
        orientation="landscape",
        min_width=1280,
        per_page=max(1, min(len(manifest["candidates"]), 20)),
    )
    candidates = source.search(manifest["query"], filters)
    candidate = next((item for item in candidates if item.clip_id == args.clip_id), None)
    if candidate is None:
        candidate = fetch_pexels_video_by_id(args.clip_id, Candidate)

    output = args.output.resolve()
    if output.exists():
        raise FileExistsError(f"Refusing to overwrite existing stock asset: {output}")
    source.download(candidate, output)
    if output.stat().st_size > MAX_VIDEO_BYTES:
        output.unlink(missing_ok=True)
        raise ValueError("Downloaded video exceeds the configured size limit")
    header = output.read_bytes()[:16]
    if b"ftyp" not in header:
        output.unlink(missing_ok=True)
        raise ValueError("Downloaded file is not an MP4 container")

    technical = probe_video(output)
    record = {
        "asset_id": candidate.clip_id,
        "query": manifest["query"],
        "file": str(output),
        "sha256": sha256(output),
        "source_url": candidate.source_url,
        "creator": candidate.creator,
        "license": candidate.license,
        "duration_seconds": candidate.duration,
        "width": candidate.width,
        "height": candidate.height,
        "technical": technical,
        "review_status": "selected_after_contact_sheet_review",
    }
    args.provenance.parent.mkdir(parents=True, exist_ok=True)
    existing = []
    if args.provenance.exists():
        existing = [
            json.loads(line)
            for line in args.provenance.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
    if any(row["asset_id"] == record["asset_id"] for row in existing):
        output.unlink(missing_ok=True)
        raise ValueError("Candidate already exists in the provenance registry")
    existing.append(record)
    args.provenance.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in existing),
        encoding="utf-8",
    )
    print(json.dumps(record, ensure_ascii=True))
    return 0


def probe_video(path: Path) -> dict:
    ffprobe = shutil.which("ffprobe")
    if ffprobe is None:
        return {"status": "not_available"}
    completed = subprocess.run(
        [
            ffprobe,
            "-v",
            "error",
            "-select_streams",
            "v:0",
            "-show_entries",
            "stream=codec_name,width,height,r_frame_rate,duration",
            "-of",
            "json",
            str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
        timeout=30,
    )
    return json.loads(completed.stdout)


def fetch_pexels_video_by_id(clip_id: str, candidate_type):
    """Resolve a reviewed immutable Pexels ID when search order changes."""
    import requests

    prefix = "pexels_"
    if not clip_id.startswith(prefix):
        raise ValueError("Only Pexels IDs are supported by this fallback")
    source_id = clip_id[len(prefix) :]
    api_key = os.environ.get("PEXELS_API_KEY")
    if not api_key:
        raise RuntimeError("Pexels is not configured")
    response = requests.get(
        f"https://api.pexels.com/videos/videos/{source_id}",
        headers={"Authorization": api_key},
        timeout=30,
    )
    response.raise_for_status()
    video = response.json()
    renditions = [
        row
        for row in (video.get("video_files") or [])
        if int(row.get("width") or 0) >= 1280 and int(row.get("width") or 0) <= 1920
    ]
    if not renditions:
        raise RuntimeError("Reviewed Pexels video has no suitable rendition")
    rendition = max(renditions, key=lambda row: int(row.get("width") or 0))
    user = video.get("user") or {}
    return candidate_type(
        source="pexels",
        source_id=str(video.get("id")),
        source_url=video.get("url", "") or "",
        download_url=rendition.get("link", "") or "",
        kind="video",
        width=int(rendition.get("width") or 0),
        height=int(rendition.get("height") or 0),
        duration=float(video.get("duration") or 0),
        creator=user.get("name", "") or "",
        license="Pexels License (free, no attribution required)",
        source_tags="",
        thumbnail_url=video.get("image", "") or "",
        extra={"fps": rendition.get("fps"), "resolved_by_immutable_id": True},
    )


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


if __name__ == "__main__":
    raise SystemExit(main())
