from __future__ import annotations

import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter


PROJECT_ROOT = Path(__file__).resolve().parents[3]
SOURCE_VIDEO = (
    PROJECT_ROOT
    / "operations" / "a-palavra-que-cuida"
    / "04_assets"
    / "video-003"
    / "stock"
    / "selected"
    / "s05-storm-sky.mp4"
)
HUMAN_SOURCE = (
    PROJECT_ROOT
    / "operations" / "a-palavra-que-cuida"
    / "04_assets"
    / "biblioteca_imagens"
    / "curadas"
    / "biblia_fe"
    / "p001-biblia-mesa-v1.png"
)
WORK_FRAME = (
    PROJECT_ROOT
    / "operations" / "a-palavra-que-cuida"
    / "04_assets"
    / "video-005"
    / "thumbnail"
    / "video-005-thumbnail-source-frame-v3.png"
)
ASSET_OUTPUT = (
    PROJECT_ROOT
    / "operations" / "a-palavra-que-cuida"
    / "04_assets"
    / "video-005"
    / "thumbnail"
    / "video-005-thumbnail-v3.png"
)
PUBLICATION_OUTPUT = (
    PROJECT_ROOT
    / "operations" / "a-palavra-que-cuida"
    / "08_publicacao"
    / "video-005-thumbnail-v3.png"
)
FFMPEG = PROJECT_ROOT / "tools" / "ffmpeg" / "bin" / "ffmpeg.exe"
WIDTH = 1280
HEIGHT = 720


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    filename = "arialbd.ttf" if bold else "arial.ttf"
    return ImageFont.truetype(Path("C:/Windows/Fonts") / filename, size=size)


def outlined(
    draw: ImageDraw.ImageDraw,
    position: tuple[int, int],
    text: str,
    active_font: ImageFont.FreeTypeFont,
    fill: str,
    stroke: str = "#061815",
) -> None:
    draw.text(position, text, font=active_font, fill=fill, stroke_width=7, stroke_fill=stroke)


def extract_frame() -> None:
    WORK_FRAME.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            str(FFMPEG),
            "-y",
            "-ss",
            "00:00:01.4",
            "-i",
            str(SOURCE_VIDEO),
            "-frames:v",
            "1",
            str(WORK_FRAME),
        ],
        check=True,
        capture_output=True,
    )


def fit_cover(source: Image.Image, width: int, height: int, offset_x: int = 0) -> Image.Image:
    scale = max(width / source.width, height / source.height)
    resized = source.resize(
        (round(source.width * scale), round(source.height * scale)),
        Image.Resampling.LANCZOS,
    )
    left = min(max((resized.width - width) // 2 + offset_x, 0), max(resized.width - width, 0))
    top = max((resized.height - height) // 2, 0)
    return resized.crop((left, top, left + width, top + height))


def add_real_human_panel(canvas: Image.Image) -> Image.Image:
    human = Image.open(HUMAN_SOURCE).convert("RGB")
    panel = fit_cover(human, 430, 720, offset_x=-80).convert("RGBA")
    panel = ImageEnhance.Color(panel).enhance(0.78)
    panel = ImageEnhance.Contrast(panel).enhance(1.08)
    dark = Image.new("RGBA", panel.size, (3, 18, 16, 105))
    panel = Image.alpha_composite(panel, dark)

    mask = Image.new("L", (430, 720), 0)
    pixels = mask.load()
    for x in range(430):
        alpha = int(max(0, min(210, (x / 140) * 210)))
        for y in range(720):
            pixels[x, y] = alpha
    mask = mask.filter(ImageFilter.GaussianBlur(10))
    panel.putalpha(mask)
    canvas.alpha_composite(panel, (850, 0))

    light = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    light_draw = ImageDraw.Draw(light)
    light_draw.rectangle((835, 0, 845, HEIGHT), fill=(243, 211, 122, 70))
    light = light.filter(ImageFilter.GaussianBlur(6))
    return Image.alpha_composite(canvas, light)


def main() -> None:
    extract_frame()
    source = Image.open(WORK_FRAME).convert("RGB")
    canvas = fit_cover(source, WIDTH, HEIGHT).convert("RGBA")

    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    pixels = overlay.load()
    for x in range(WIDTH):
        opacity = int(max(35, min(225, 220 * (1 - x / 880))))
        for y in range(HEIGHT):
            pixels[x, y] = (4, 22, 20, opacity)
    canvas = Image.alpha_composite(canvas, overlay)
    canvas = add_real_human_panel(canvas)

    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((58, 80, 340, 138), radius=12, fill="#F3D37A")
    draw.text((82, 94), "GÊNESIS 1", font=font(29, bold=True), fill="#09201B")
    outlined(draw, (56, 180), "O COMEÇO", font(82, bold=True), "#FFFFFF")
    outlined(draw, (56, 276), "NÃO É", font(94, bold=True), "#F3D37A")
    outlined(draw, (56, 388), "CAOS", font(126, bold=True), "#FFFFFF")
    draw.rounded_rectangle((62, 560, 545, 623), radius=12, fill=(246, 246, 235, 235))
    draw.text((84, 576), "uma reflexão sobre criação", font=font(28, bold=True), fill="#09201B")

    ASSET_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(ASSET_OUTPUT, optimize=True, quality=95)
    PUBLICATION_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(PUBLICATION_OUTPUT, optimize=True, quality=95)
    print(ASSET_OUTPUT)
    print(PUBLICATION_OUTPUT)


if __name__ == "__main__":
    main()
