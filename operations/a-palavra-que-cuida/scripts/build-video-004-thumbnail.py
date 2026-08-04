from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


PROJECT_ROOT = Path(__file__).resolve().parents[3]
SOURCE = PROJECT_ROOT / "operations" / "a-palavra-que-cuida" / "04_assets" / "video-004" / "generated" / "historical" / "h01-jesus-no-templo-v1.png"
OUTPUT = PROJECT_ROOT / "operations" / "a-palavra-que-cuida" / "04_assets" / "video-004" / "thumbnail" / "video-004-thumbnail-v1.png"
WIDTH = 1280
HEIGHT = 720


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    filename = "arialbd.ttf" if bold else "arial.ttf"
    return ImageFont.truetype(Path("C:/Windows/Fonts") / filename, size=size)


def outlined_text(draw: ImageDraw.ImageDraw, position: tuple[int, int], text: str, active_font: ImageFont.FreeTypeFont, fill: str) -> None:
    draw.text(position, text, font=active_font, fill=fill, stroke_width=7, stroke_fill="#092640")


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    source = Image.open(SOURCE).convert("RGB")
    scale = max(WIDTH / source.width, HEIGHT / source.height)
    resized = source.resize((round(source.width * scale), round(source.height * scale)), Image.Resampling.LANCZOS)
    left = max((resized.width - WIDTH) // 2 - 100, 0)
    top = max((resized.height - HEIGHT) // 2, 0)
    canvas = resized.crop((left, top, left + WIDTH, top + HEIGHT))
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    pixels = overlay.load()
    for x in range(WIDTH):
        opacity = int(max(0, min(220, 205 * (1 - x / 760))))
        for y in range(HEIGHT):
            pixels[x, y] = (5, 28, 43, opacity)
    canvas = Image.alpha_composite(canvas.convert("RGBA"), overlay)
    draw = ImageDraw.Draw(canvas)
    outlined_text(draw, (58, 142), "A INFÂNCIA", font(86, bold=True), "#FFFFFF")
    outlined_text(draw, (58, 236), "DE JESUS", font(104, bold=True), "#FFD71F")
    draw.rounded_rectangle((62, 382, 537, 450), radius=13, fill="#FFFFFF")
    draw.text((84, 397), "O QUE A BÍBLIA DIZ?", font=font(31, bold=True), fill="#092640")
    canvas.convert("RGB").save(OUTPUT, optimize=True, quality=95)
    print(OUTPUT)


if __name__ == "__main__":
    main()
