from __future__ import annotations

import json
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


PROJECT_ROOT = Path(__file__).resolve().parents[3]
MANIFEST_PATH = PROJECT_ROOT / "operations" / "a-palavra-que-cuida" / "02_roteiros" / "video-006-citacoes-acf-v1.json"
OUTPUT_DIR = PROJECT_ROOT / "operations" / "a-palavra-que-cuida" / "04_assets" / "video-006" / "scripture_cards"
WIDTH = 1920
HEIGHT = 1080
BACKGROUND = "#F5F0E7"
INK = "#26382F"
ACCENT = "#A9853D"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    filename = "georgiab.ttf" if bold else "georgia.ttf"
    return ImageFont.truetype(Path("C:/Windows/Fonts") / filename, size=size)


def wrap(draw: ImageDraw.ImageDraw, text: str, active_font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current: list[str] = []
    for word in words:
        candidate = " ".join([*current, word])
        if draw.textbbox((0, 0), candidate, font=active_font)[2] <= max_width:
            current.append(word)
        else:
            lines.append(" ".join(current))
            current = [word]
    if current:
        lines.append(" ".join(current))
    return lines


def quote_font(draw: ImageDraw.ImageDraw, text: str, max_width: int, max_height: int) -> tuple[ImageFont.FreeTypeFont, list[str]]:
    for size in range(62, 32, -2):
        active_font = font(size)
        lines = wrap(draw, text, active_font, max_width)
        if len(lines) * int(size * 1.42) <= max_height:
            return active_font, lines
    raise RuntimeError("Scripture text does not fit the card")


def slug(reference: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", reference.casefold()).strip("-")


def main() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    results = []
    for item in manifest["direct_acf_citations"]:
        canvas = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
        draw = ImageDraw.Draw(canvas)
        draw.rectangle((168, 174, 178, 906), fill=ACCENT)
        body_font, lines = quote_font(draw, item["text"], 1370, 500)
        draw.text((230, 205), "ALMEIDA CORRIGIDA FIEL", fill=ACCENT, font=font(28, bold=True))
        draw.text((230, 258), item["reference"], fill=INK, font=font(52, bold=True))
        line_height = int(body_font.size * 1.42)
        y = 570 - (len(lines) * line_height) // 2
        draw.text((230, y - 68), "“", fill=ACCENT, font=font(82))
        for line in lines:
            draw.text((288, y), line, fill=INK, font=body_font)
            y += line_height
        draw.text((230, 920), "A Palavra Que Cuida", fill="#6E786F", font=font(24))
        filename = f"acf-{slug(item['reference'])}.png"
        canvas.save(OUTPUT_DIR / filename, optimize=True)
        results.append({"reference": item["reference"], "text": item["text"], "file": filename, "width": WIDTH, "height": HEIGHT})
    (OUTPUT_DIR / "manifest.json").write_text(json.dumps({
        "source": str(MANIFEST_PATH.relative_to(PROJECT_ROOT)).replace("\\", "/"),
        "display_policy": manifest["display_policy"],
        "cards": results,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"cards": len(results), "output_dir": str(OUTPUT_DIR)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
