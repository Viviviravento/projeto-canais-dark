from __future__ import annotations

import json
from io import BytesIO
from pathlib import Path

import requests
from PIL import Image, ImageDraw, ImageFont, ImageOps


PROJECT_ROOT = Path(__file__).resolve().parents[4]
OPERATION_ROOT = Path(__file__).resolve().parents[2]
ENV_PATH = PROJECT_ROOT / "tools" / "OpenMontage" / ".env"
EDIT_DIR = OPERATION_ROOT / "06_edicao" / "piloto-001"
PREVIEW_DIR = EDIT_DIR / "stock-previews"

SLOTS = [
    ("open01", "middle aged woman organizing table home"),
    ("open02", "woman writing planner home close up"),
    ("open03", "smartphone notifications table close up"),
    ("open04", "quiet living room window sunset"),
    ("bible01", "open bible wooden table"),
    ("control01", "woman closing notebook by window"),
    ("burden01", "bills table calculator close up"),
    ("burden02", "empty hospital corridor"),
    ("burden03", "middle aged woman sitting alone living room daylight"),
    ("support01", "two mature women talking at home"),
    ("support02", "woman serving coffee to friend"),
    ("support03", "woman sending message smartphone close up"),
    ("release01", "middle aged woman walking quiet street"),
    ("release02", "opening door sunlight home"),
    ("release03", "woman praying quietly at home"),
    ("steps01", "woman writing journal checklist close up"),
    ("steps02", "hands closing bible on table"),
    ("steps03", "middle aged woman looking out window calm"),
    ("close01", "bible on table sunset light"),
    ("close02", "sunrise through window home"),
]


def load_secret(name: str) -> str:
    for raw_line in ENV_PATH.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        if key.strip() == name:
            return value.strip().strip('"').strip("'")
    raise RuntimeError(f"Missing {name} in {ENV_PATH}")


def search() -> list[dict]:
    key = load_secret("PEXELS_API_KEY")
    headers = {"Authorization": key}
    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    records: list[dict] = []

    for slot, query in SLOTS:
        response = requests.get(
            "https://api.pexels.com/videos/search",
            headers=headers,
            params={"query": query, "orientation": "landscape", "per_page": 4, "page": 1},
            timeout=30,
        )
        response.raise_for_status()
        videos = response.json().get("videos", [])
        slot_candidates: list[dict] = []
        for index, video in enumerate(videos):
            thumb_bytes = requests.get(video["image"], timeout=30).content
            thumb_path = PREVIEW_DIR / f"{slot}-{index}.jpg"
            thumb_path.write_bytes(thumb_bytes)

            files = []
            for item in video.get("video_files", []):
                width = item.get("width") or 0
                height = item.get("height") or 0
                if width >= 1280 and width <= 1920 and height >= 720:
                    files.append(
                        {
                            "id": item.get("id"),
                            "quality": item.get("quality"),
                            "file_type": item.get("file_type"),
                            "width": width,
                            "height": height,
                            "fps": item.get("fps"),
                            "link": item.get("link"),
                        }
                    )
            files.sort(key=lambda item: (abs(item["width"] - 1920), -item["height"]))
            slot_candidates.append(
                {
                    "index": index,
                    "video_id": video["id"],
                    "duration_seconds": video.get("duration"),
                    "width": video.get("width"),
                    "height": video.get("height"),
                    "author": video.get("user", {}).get("name"),
                    "pexels_url": video.get("url"),
                    "thumbnail": str(thumb_path),
                    "files": files,
                }
            )
        records.append({"slot": slot, "query": query, "candidates": slot_candidates})

    (EDIT_DIR / "stock-candidates.json").write_text(
        json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return records


def font(size: int) -> ImageFont.ImageFont:
    for candidate in ["arial.ttf", "C:/Windows/Fonts/arial.ttf"]:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue
    return ImageFont.load_default()


def contact_sheets(records: list[dict]) -> None:
    cell_w, cell_h = 320, 180
    label_h = 44
    margin = 16
    title_font = font(20)
    item_font = font(16)

    for page_index in range(0, len(records), 5):
        group = records[page_index : page_index + 5]
        canvas = Image.new("RGB", (margin * 2 + cell_w * 4, margin * 2 + (cell_h + label_h) * 5), "#121212")
        draw = ImageDraw.Draw(canvas)
        for row, record in enumerate(group):
            y = margin + row * (cell_h + label_h)
            draw.text((margin, y), f"{record['slot']} | {record['query']}", fill="#ffffff", font=title_font)
            for col, candidate in enumerate(record["candidates"]):
                x = margin + col * cell_w
                image = Image.open(candidate["thumbnail"]).convert("RGB")
                image = ImageOps.fit(image, (cell_w, cell_h - 28), method=Image.Resampling.LANCZOS)
                canvas.paste(image, (x, y + 28))
                draw.rectangle((x, y + 28, x + 64, y + 54), fill="#111111")
                draw.text(
                    (x + 6, y + 31),
                    f"#{candidate['index']} {candidate['duration_seconds']}s",
                    fill="#ffd166",
                    font=item_font,
                )
        output = EDIT_DIR / f"stock-contact-{page_index // 5 + 1}.jpg"
        canvas.save(output, quality=90)


def main() -> int:
    records = search()
    contact_sheets(records)
    print(json.dumps({"slots": len(records), "candidates": sum(len(r["candidates"]) for r in records)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
