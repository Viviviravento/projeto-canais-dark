from __future__ import annotations

import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter


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
WORK_FRAME = (
    PROJECT_ROOT
    / "operations" / "a-palavra-que-cuida"
    / "04_assets"
    / "video-005"
    / "thumbnail"
    / "video-005-thumbnail-source-frame-v2.png"
)
ASSET_OUTPUT = (
    PROJECT_ROOT
    / "operations" / "a-palavra-que-cuida"
    / "04_assets"
    / "video-005"
    / "thumbnail"
    / "video-005-thumbnail-v2.png"
)
PUBLICATION_OUTPUT = (
    PROJECT_ROOT
    / "operations" / "a-palavra-que-cuida"
    / "08_publicacao"
    / "video-005-thumbnail-v2.png"
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


def add_human_silhouette(canvas: Image.Image) -> Image.Image:
    layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    shadow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.ellipse((965, 633, 1134, 666), fill=(0, 0, 0, 105))
    shadow = shadow.filter(ImageFilter.GaussianBlur(10))
    layer = Image.alpha_composite(layer, shadow)

    draw = ImageDraw.Draw(layer)
    ink = (3, 13, 13, 238)
    soft_ink = (4, 17, 16, 220)

    draw.ellipse((1030, 492, 1062, 527), fill=ink)
    draw.ellipse((1024, 488, 1048, 514), fill=ink)
    draw.polygon([(1022, 526), (1067, 526), (1090, 624), (1000, 624)], fill=soft_ink)
    draw.polygon([(1014, 543), (988, 602), (1003, 611), (1030, 548)], fill=ink)
    draw.polygon([(1063, 542), (1104, 592), (1092, 606), (1054, 556)], fill=ink)
    draw.polygon([(1016, 619), (1038, 619), (1034, 653), (1006, 653)], fill=ink)
    draw.polygon([(1056, 619), (1078, 619), (1098, 653), (1068, 653)], fill=ink)
    draw.ellipse((998, 648, 1038, 660), fill=ink)
    draw.ellipse((1064, 648, 1104, 660), fill=ink)

    layer = layer.filter(ImageFilter.GaussianBlur(0.45))
    return Image.alpha_composite(canvas, layer)


def main() -> None:
    extract_frame()
    source = Image.open(WORK_FRAME).convert("RGB")
    scale = max(WIDTH / source.width, HEIGHT / source.height)
    resized = source.resize(
        (round(source.width * scale), round(source.height * scale)),
        Image.Resampling.LANCZOS,
    )
    left = max((resized.width - WIDTH) // 2, 0)
    top = max((resized.height - HEIGHT) // 2, 0)
    canvas = resized.crop((left, top, left + WIDTH, top + HEIGHT)).convert("RGBA")

    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    pixels = overlay.load()
    for x in range(WIDTH):
        opacity = int(max(20, min(225, 220 * (1 - x / 850))))
        for y in range(HEIGHT):
            pixels[x, y] = (4, 22, 20, opacity)
    canvas = Image.alpha_composite(canvas, overlay)
    canvas = add_human_silhouette(canvas)

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
