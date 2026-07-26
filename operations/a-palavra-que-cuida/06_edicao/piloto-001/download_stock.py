from __future__ import annotations

import json
from pathlib import Path

import requests


OPERATION_ROOT = Path(__file__).resolve().parents[2]
EDIT_DIR = OPERATION_ROOT / "06_edicao" / "piloto-001"
ASSET_DIR = OPERATION_ROOT / "04_assets" / "piloto-001" / "stock"
CANDIDATES_PATH = EDIT_DIR / "stock-candidates.json"
SELECTION_PATH = EDIT_DIR / "stock-selection.json"
MANIFEST_PATH = EDIT_DIR / "stock-manifest.json"


def main() -> int:
    candidates = json.loads(CANDIDATES_PATH.read_text(encoding="utf-8"))
    selections = json.loads(SELECTION_PATH.read_text(encoding="utf-8"))
    by_slot = {record["slot"]: record for record in candidates}
    ASSET_DIR.mkdir(parents=True, exist_ok=True)

    downloaded_by_id: dict[int, Path] = {}
    manifest: list[dict] = []

    for slot, candidate_index in selections.items():
        record = by_slot[slot]
        candidate = record["candidates"][candidate_index]
        video_id = int(candidate["video_id"])

        if video_id in downloaded_by_id:
            output_path = downloaded_by_id[video_id]
        else:
            files = candidate.get("files") or []
            if not files:
                raise RuntimeError(f"No suitable 720p/1080p file for {slot}")
            selected_file = files[0]
            suffix = ".mp4" if "mp4" in (selected_file.get("file_type") or "") else ".mp4"
            output_path = ASSET_DIR / f"pexels-{video_id}{suffix}"
            if not output_path.exists():
                with requests.get(selected_file["link"], stream=True, timeout=180) as response:
                    response.raise_for_status()
                    with output_path.open("wb") as handle:
                        for chunk in response.iter_content(chunk_size=1024 * 1024):
                            if chunk:
                                handle.write(chunk)
            downloaded_by_id[video_id] = output_path

        manifest.append(
            {
                "slot": slot,
                "query": record["query"],
                "provider": "Pexels",
                "video_id": video_id,
                "duration_seconds": candidate["duration_seconds"],
                "author": candidate["author"],
                "source_url": candidate["pexels_url"],
                "license": "Pexels License",
                "license_url": "https://www.pexels.com/license/",
                "local_path": str(output_path),
            }
        )

    MANIFEST_PATH.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    total_bytes = sum(path.stat().st_size for path in set(downloaded_by_id.values()))
    print(
        json.dumps(
            {
                "slots": len(manifest),
                "unique_files": len(downloaded_by_id),
                "total_bytes": total_bytes,
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
