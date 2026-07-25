from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = ROOT / "04_assets" / "video-003" / "thumbnail" / "video-003-thumbnail-base-v1.png"
DEFAULT_OUTPUT = ROOT / "08_publicacao" / "video-003-thumbnail-v1.png"
FONT_PATH = Path("C:/Windows/Fonts/impact.ttf")
CANVAS = (1280, 720)
NAVY = "#061D3A"
WHITE = "#F8FAFF"
YELLOW = "#FFD500"


def cover(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    scale = max(size[0] / image.width, size[1] / image.height)
    resized = image.resize((round(image.width * scale), round(image.height * scale)), Image.Resampling.LANCZOS)
    left = (resized.width - size[0]) // 2
    top = (resized.height - size[1]) // 2
    return resized.crop((left, top, left + size[0], top + size[1]))


def fit_font(draw: ImageDraw.ImageDraw, text: str, max_width: int, start_size: int) -> ImageFont.FreeTypeFont:
    for size in range(start_size, 39, -2):
        font = ImageFont.truetype(str(FONT_PATH), size)
        box = draw.textbbox((0, 0), text, font=font, stroke_width=0)
        if box[2] - box[0] <= max_width:
            return font
    raise RuntimeError(f"Nao foi possivel ajustar a linha: {text}")


def build(source: Path, output: Path) -> None:
    if not FONT_PATH.is_file():
        raise FileNotFoundError(f"Fonte ausente: {FONT_PATH}")
    canvas = cover(Image.open(source).convert("RGB"), CANVAS)

    # Mantem a imagem legivel, mas reserva contraste constante para a tipografia.
    shade = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    pixels = shade.load()
    for x in range(760):
        alpha = round(82 * (1 - x / 760) ** 1.8)
        for y in range(CANVAS[1]):
            pixels[x, y] = (1, 15, 33, alpha)
    canvas = Image.alpha_composite(canvas.convert("RGBA"), shade)

    draw = ImageDraw.Draw(canvas)
    lines = [
        ("NEM TODA", WHITE, 150),
        ("DOR É", YELLOW, 205),
        ("CASTIGO", YELLOW, 194),
    ]
    x = 42
    y = 66
    max_width = 690
    for text, color, initial_size in lines:
        font = fit_font(draw, text, max_width, initial_size)
        box = draw.textbbox((x, y), text, font=font, stroke_width=12)
        draw.text((x + 7, y + 9), text, font=font, fill="#000B1E", stroke_width=13, stroke_fill="#000B1E")
        draw.text((x, y), text, font=font, fill=color, stroke_width=10, stroke_fill=NAVY)
        y += (box[3] - box[1]) + 12

    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(output, "PNG", optimize=True)
    if output.stat().st_size > 2_000_000:
        raise RuntimeError(f"Thumbnail excedeu 2 MB: {output.stat().st_size} bytes")


def main() -> None:
    parser = argparse.ArgumentParser(description="Compoe a thumbnail reproducivel do video 003.")
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    build(args.source, args.output)
    print(args.output)


if __name__ == "__main__":
    main()
