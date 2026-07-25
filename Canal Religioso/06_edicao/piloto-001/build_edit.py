from __future__ import annotations

import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
EDIT_DIR = ROOT / "Canal Religioso" / "06_edicao" / "piloto-001"
MANIFEST_PATH = EDIT_DIR / "stock-manifest.json"
CAPTIONS_PATH = EDIT_DIR / "captions-word.json"
AUDIO_PATH = ROOT / "Canal Religioso" / "05_audio" / "piloto-001" / "narracao-final-master.wav"
PROPS_PATH = EDIT_DIR / "remotion-props.json"
PUBLIC_DIR = ROOT / "tools" / "OpenMontage" / "remotion-composer" / "public" / "piloto-001"


def main() -> int:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    PUBLIC_DIR.mkdir(parents=True, exist_ok=True)
    assets: dict[str, str] = {}
    staged_by_source: dict[Path, str] = {}
    for item in manifest:
        source = Path(item["local_path"]).resolve()
        if source not in staged_by_source:
            target = PUBLIC_DIR / source.name
            if not target.exists() or target.stat().st_size != source.stat().st_size:
                shutil.copy2(source, target)
            staged_by_source[source] = f"piloto-001/{target.name}"
        assets[item["slot"]] = staged_by_source[source]

    staged_audio = PUBLIC_DIR / "narracao-final-master.wav"
    if not staged_audio.exists() or staged_audio.stat().st_size != AUDIO_PATH.stat().st_size:
        shutil.copy2(AUDIO_PATH, staged_audio)
    captions = json.loads(CAPTIONS_PATH.read_text(encoding="utf-8"))

    # Full-frame cards already carry the essential text. Suppress lower
    # captions during those intervals to preserve a clean reading hierarchy.
    card_ranges = [
        (0.0, 4.52),
        (68.58, 93.17),
        (122.81, 132.13),
        (202.19, 211.22),
        (260.74, 270.47),
        (337.91, 349.88),
        (438.54, 442.33),
        (510.86, 513.58),
        (537.63, 541.0),
    ]
    captions = [
        word
        for word in captions
        if not any(start * 1000 <= word["startMs"] < end * 1000 for start, end in card_ranges)
    ]

    cuts: list[dict] = []

    def video(slot: str, start: float, end: float, source_start: float = 0.0) -> None:
        cuts.append(
            {
                "id": f"cut-{len(cuts) + 1:02d}-{slot}",
                "source": assets[slot],
                "source_in_seconds": source_start,
                "in_seconds": start,
                "out_seconds": end,
            }
        )

    def card(
        text: str,
        start: float,
        end: float,
        background_slot: str,
        background_start: float = 0.0,
        font_size: int = 54,
    ) -> None:
        cuts.append(
            {
                "id": f"cut-{len(cuts) + 1:02d}-card",
                "type": "text_card",
                "text": text,
                "fontSize": font_size,
                "color": "#FFFDF7",
                "accentColor": "#D7B56D",
                "backgroundVideo": assets[background_slot],
                "backgroundVideoStart": background_start,
                "backgroundOverlay": 0.64,
                "in_seconds": start,
                "out_seconds": end,
            }
        )

    card("Voc\u00ea n\u00e3o precisa\ncarregar tudo sozinha", 0.0, 4.52, "open01", 0.0, 64)
    video("open02", 4.52, 19.92)
    video("open03", 19.92, 32.0)
    video("open04", 32.0, 45.0)
    video("open01", 45.0, 53.16, 6.5)
    video("bible01", 53.16, 68.58, 0.0)

    card(
        "Vinde a mim, todos os que estais cansados e oprimidos,\ne eu vos aliviarei.\n\nMateus 11:28, ACF",
        68.58,
        75.07,
        "bible01",
        0.0,
        44,
    )
    card(
        "Tomai sobre v\u00f3s o meu jugo, e aprendei de mim,\nque sou manso e humilde de cora\u00e7\u00e3o;\ne encontrareis descanso para as vossas almas.\n\nMateus 11:29, ACF",
        75.07,
        84.927,
        "bible01",
        8.0,
        43,
    )
    card(
        "Porque o meu jugo \u00e9 suave\ne o meu fardo \u00e9 leve.\n\nMateus 11:30, ACF",
        84.927,
        93.17,
        "bible01",
        20.0,
        54,
    )

    video("control01", 93.17, 100.17)
    video("burden03", 100.17, 110.10)
    video("bible01", 110.10, 122.81, 18.0)
    card(
        "Viver com responsabilidade\nn\u00e3o \u00e9 viver como se tudo\ndependesse de voc\u00ea.",
        122.81,
        132.13,
        "open04",
        0.0,
        46,
    )
    video("steps01", 132.13, 152.17)
    video("release01", 152.17, 165.98)
    video("burden01", 165.98, 180.98)
    video("burden02", 180.98, 183.15)
    video("burden03", 183.15, 202.19)
    card("Cuidado n\u00e3o pode\nvirar pris\u00e3o.", 202.19, 211.22, "burden03", 10.0, 62)
    video("open01", 211.22, 226.22)
    video("open02", 226.22, 230.31, 10.0)
    video("steps03", 230.31, 238.31)
    video("release02", 238.31, 249.74)
    video("bible01", 249.74, 260.74, 24.0)

    card(
        "Levai as cargas uns dos outros,\ne assim cumprireis a lei de Cristo.\n\nG\u00e1latas 6:2, ACF",
        260.74,
        270.47,
        "bible01",
        32.0,
        44,
    )
    video("support01", 270.47, 287.17)
    video("support02", 287.17, 295.17)
    video("support03", 295.17, 307.77)
    video("support01", 307.77, 322.43, 8.0)
    video("support03", 322.43, 336.44)
    video("bible01", 336.44, 337.91, 43.0)
    card(
        "Lan\u00e7ando sobre ele toda a vossa ansiedade,\nporque ele tem cuidado de v\u00f3s.\n\n1 Pedro 5:7, ACF",
        337.91,
        349.88,
        "bible01",
        45.0,
        52,
    )

    video("release01", 349.88, 364.88)
    video("release03", 364.88, 380.88)
    video("open04", 380.88, 386.31, 7.0)
    video("release02", 386.31, 400.31)
    video("steps03", 400.31, 405.04)
    video("support01", 405.04, 420.04)
    video("burden02", 420.04, 426.55)
    video("steps01", 426.55, 438.54)
    card("Tr\u00eas perguntas\npara hoje", 438.54, 442.33, "steps01", 0.0, 66)
    video("steps01", 442.33, 461.44, 8.0)
    video("release01", 461.44, 481.44)
    video("release02", 481.44, 483.87, 10.0)
    video("support01", 483.87, 500.60)
    video("open04", 500.60, 510.86)
    card("Voc\u00ea n\u00e3o precisa\ncarregar tudo sozinha.", 510.86, 513.58, "close01", 0.0, 64)
    video("bible01", 513.58, 527.50, 40.0)
    video("close01", 527.50, 533.50)
    video("open04", 533.50, 537.63, 4.0)
    card(
        "A Palavra que Cuida\n@apalavraquecuida",
        537.63,
        541.0,
        "bible01",
        50.0,
        62,
    )

    overlays = [
        {
            "type": "section_title",
            "text": "O convite de Jesus",
            "subtitle": "Mateus 11:28-30",
            "position": "top-left",
            "accentColor": "#D7B56D",
            "in_seconds": 53.16,
            "out_seconds": 67.44,
        },
        {
            "type": "section_title",
            "text": "Cargas compartilhadas",
            "subtitle": "G\u00e1latas 6:2",
            "position": "top-left",
            "accentColor": "#D7B56D",
            "in_seconds": 249.74,
            "out_seconds": 260.74,
        },
        {
            "type": "section_title",
            "text": "Entregar n\u00e3o \u00e9 negar",
            "subtitle": "1 Pedro 5:7",
            "position": "top-left",
            "accentColor": "#D7B56D",
            "in_seconds": 349.88,
            "out_seconds": 364.88,
        },
        {
            "type": "section_title",
            "text": "Um passo de cada vez",
            "position": "top-left",
            "accentColor": "#D7B56D",
            "in_seconds": 426.55,
            "out_seconds": 438.54,
        },
    ]

    props = {
        "renderer_family": "explainer-data",
        "render_runtime": "remotion",
        "total_duration_seconds": 541.0,
        "cuts": cuts,
        "overlays": overlays,
        "captions": captions,
        "audio": {"narration": {"src": "piloto-001/narracao-final-master.wav", "volume": 1.0}},
        "themeConfig": {
            "primaryColor": "#31483C",
            "accentColor": "#D7B56D",
            "backgroundColor": "#F4EFE5",
            "surfaceColor": "#E9E1D3",
            "textColor": "#233129",
            "mutedTextColor": "#66736B",
            "headingFont": "Space Grotesk",
            "bodyFont": "Space Grotesk",
            "monoFont": "Consolas",
            "chartColors": ["#31483C", "#D7B56D", "#7A9185", "#B86B4B"],
            "springConfig": {"damping": 22, "stiffness": 105, "mass": 1},
            "transitionDuration": 0.55,
            "captionHighlightColor": "#F2C96D",
            "captionBackgroundColor": "rgba(28, 39, 33, 0.78)",
        },
    }

    PROPS_PATH.write_text(
        json.dumps(props, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"cuts": len(cuts), "overlays": len(overlays), "captions": len(captions)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
