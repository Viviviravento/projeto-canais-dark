from __future__ import annotations

import json
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[3]
MANIFEST = ROOT / "operations" / "a-palavra-que-cuida" / "02_roteiros" / "video-011-citacoes-acf-v1.json"
OUTPUT = ROOT / "operations" / "a-palavra-que-cuida" / "04_assets" / "video-011" / "scripture_cards"
WIDTH, HEIGHT = 1920, 1080
BACKGROUND, INK, ACCENT = "#F5F0E7", "#26382F", "#A9853D"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(Path("C:/Windows/Fonts") / ("georgiab.ttf" if bold else "georgia.ttf"), size=size)


def wrap(draw: ImageDraw.ImageDraw, text: str, active_font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    lines, current = [], []
    for word in text.split():
        candidate = " ".join([*current, word])
        if draw.textbbox((0, 0), candidate, font=active_font)[2] <= max_width:
            current.append(word)
        else:
            lines.append(" ".join(current))
            current = [word]
    if current:
        lines.append(" ".join(current))
    return lines


def text_layout(draw: ImageDraw.ImageDraw, text: str) -> tuple[ImageFont.FreeTypeFont, list[str]]:
    for size in range(62, 32, -2):
        active_font = font(size)
        lines = wrap(draw, text, active_font, 1370)
        if len(lines) * int(size * 1.42) <= 500:
            return active_font, lines
    raise RuntimeError("Verse does not fit its card")


def slug(reference: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", reference.casefold()).strip("-")


def main() -> None:
    source = json.loads(MANIFEST.read_text(encoding="utf-8"))
    OUTPUT.mkdir(parents=True, exist_ok=True)
    cards = []
    for citation in source["direct_acf_citations"]:
        image = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
        draw = ImageDraw.Draw(image)
        draw.rectangle((168, 174, 178, 906), fill=ACCENT)
        body_font, lines = text_layout(draw, citation["text"])
        draw.text((230, 205), "ALMEIDA CORRIGIDA FIEL", fill=ACCENT, font=font(28, bold=True))
        draw.text((230, 258), citation["reference"], fill=INK, font=font(52, bold=True))
        line_height = int(body_font.size * 1.42)
        y = 570 - (len(lines) * line_height) // 2
        draw.text((230, y - 68), "“", fill=ACCENT, font=font(82))
        for line in lines:
            draw.text((288, y), line, fill=INK, font=body_font)
            y += line_height
        draw.text((230, 920), "A Palavra Que Cuida", fill="#6E786F", font=font(24))
        filename = f"acf-{slug(citation['reference'])}.png"
        image.save(OUTPUT / filename, optimize=True)
        cards.append({"reference": citation["reference"], "text": citation["text"], "file": filename, "width": WIDTH, "height": HEIGHT})
    (OUTPUT / "manifest.json").write_text(json.dumps({"source": str(MANIFEST.relative_to(ROOT)).replace("\\", "/"), "display_policy": source["display_policy"], "cards": cards}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"cards": len(cards), "output": str(OUTPUT)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
