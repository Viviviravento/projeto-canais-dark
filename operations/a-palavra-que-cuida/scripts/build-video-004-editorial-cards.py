from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


PROJECT_ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = PROJECT_ROOT / "operations" / "a-palavra-que-cuida" / "04_assets" / "video-004" / "editorial_cards"
WIDTH = 1920
HEIGHT = 1080
BACKGROUND = "#F5F0E7"
INK = "#26382F"
ACCENT = "#A9853D"
MUTED = "#6E786F"
CARDS = [
    ("g01-o-que-lucas-conta", "O QUE LUCAS CONTA", "crescimento • caminho anual • templo • retorno"),
    ("g02-o-que-o-texto-nao-conta", "O QUE O TEXTO NÃO CONTA", "Não é uma lacuna para preencher com invenções."),
    ("g03-missao-e-vida-concreta", "MISSÃO E VIDA CONCRETA", "Jesus fala do Pai e volta para Nazaré."),
    ("g04-o-silencio-ensina-limites", "O SILÊNCIO TAMBÉM ENSINA LIMITES", "O que foi revelado já nos orienta."),
    ("g05-entre-o-nascimento-e-o-templo", "ENTRE O NASCIMENTO E O TEMPLO", "Os Evangelhos não escrevem um diário de cada dia."),
    ("g06-uma-familia-caminha", "UMA FAMÍLIA CAMINHA TODOS OS ANOS", "A fé também ganha forma em práticas repetidas."),
    ("g07-ouvir-perguntar-crescer", "OUVIR • PERGUNTAR • CRESCER", "A cena no templo é de atenção e diálogo."),
    ("g08-identidade-e-missao", "IDENTIDADE E MISSÃO", "Uma resposta profunda, sem transformar a família em confronto."),
    ("g09-de-volta-a-nazare", "DE VOLTA A NAZARÉ", "A missão não apaga a vida concreta."),
    ("g10-continue-por-aqui", "CONTINUE POR AQUI", "Escolha um próximo vídeo e acompanhe o canal."),
]


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    filename = "georgiab.ttf" if bold else "georgia.ttf"
    return ImageFont.truetype(Path("C:/Windows/Fonts") / filename, size=size)


def wrap(draw: ImageDraw.ImageDraw, text: str, active_font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    lines: list[str] = []
    words: list[str] = []
    for word in text.split():
        candidate = " ".join([*words, word])
        if draw.textbbox((0, 0), candidate, font=active_font)[2] <= max_width:
            words.append(word)
        else:
            lines.append(" ".join(words))
            words = [word]
    if words:
        lines.append(" ".join(words))
    return lines


def title_font(draw: ImageDraw.ImageDraw, text: str) -> tuple[ImageFont.FreeTypeFont, list[str]]:
    for size in range(92, 44, -2):
        active_font = font(size, bold=True)
        lines = wrap(draw, text, active_font, 1280)
        if len(lines) <= 2:
            return active_font, lines
    raise RuntimeError(f"Title does not fit: {text}")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest = []
    for slug, title, body in CARDS:
        canvas = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
        draw = ImageDraw.Draw(canvas)
        draw.rectangle((168, 174, 178, 906), fill=ACCENT)
        draw.text((230, 210), "A PALAVRA QUE CUIDA", fill=ACCENT, font=font(28, bold=True))
        active_font, title_lines = title_font(draw, title)
        y = 350
        for line in title_lines:
            draw.text((230, y), line, fill=INK, font=active_font)
            y += int(active_font.size * 1.15)
        body_font = font(44)
        for line in wrap(draw, body, body_font, 1260):
            draw.text((230, y + 62), line, fill=MUTED, font=body_font)
            y += int(body_font.size * 1.3)
        draw.text((230, 920), "A Palavra Que Cuida", fill=MUTED, font=font(24))
        filename = f"{slug}.png"
        canvas.save(OUTPUT_DIR / filename, optimize=True)
        manifest.append({"asset_id": slug, "file": filename, "width": WIDTH, "height": HEIGHT, "title": title, "body": body})
    (OUTPUT_DIR / "manifest.json").write_text(json.dumps({"cards": manifest}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"cards": len(manifest), "output_dir": str(OUTPUT_DIR)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
