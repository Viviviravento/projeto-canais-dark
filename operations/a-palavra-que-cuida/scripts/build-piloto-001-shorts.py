from __future__ import annotations

import json
import re
import subprocess
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "tools" / "OpenMontage" / "projects" / "a-palavra-que-cuida-piloto-001"
AUDIO_ROOT = ROOT / "operations" / "a-palavra-que-cuida" / "05_audio" / "piloto-001" / "v1"
SOURCE_AUDIO = AUDIO_ROOT / "piloto-001-narracao-v1-master.wav"
WORK_ROOT = ROOT / "operations" / "a-palavra-que-cuida" / "06_edicao" / "piloto-001" / "shorts"
PROPS_ROOT = WORK_ROOT / "props"
PUBLIC_AUDIO = PROJECT / "public" / "audio"


@dataclass(frozen=True)
class ShortSpec:
    short_id: str
    title: str
    block_id: str
    start_phrase: str
    end_phrase: str
    visuals: tuple[tuple[str, str, float], ...]


SPECS = (
    ShortSpec(
        short_id="02",
        title="Quando você continua funcionando, mas já está sobrecarregada",
        block_id="01-abertura",
        start_phrase="Talvez o seu dia ainda nem tenha terminado",
        end_phrase="sustentar o mundo inteiro sozinha",
        visuals=(
            ("images/img-s02-dia-em-andamento-v1.png", "56% 50%", 1.14),
            ("images/img-s03-tarefas-v1.png", "50% 48%", 1.15),
            ("images/img-s04-reflexo-v1.png", "48% 49%", 1.13),
            ("images/img-s16-peso-mental-v1.png", "52% 49%", 1.14),
            ("images/img-s05-maos-em-pausa-v1.png", "50% 52%", 1.13),
            ("images/img-s18-chegar-cansada-v1.png", "52% 48%", 1.14),
            ("images/img-s17-pausa-v1.png", "50% 48%", 1.13),
            ("images/img-s04-reflexo-v1.png", "48% 49%", 1.17),
        ),
    ),
    ShortSpec(
        short_id="03",
        title="Responsabilidade não é tentar controlar tudo",
        block_id="02-o-convite-de-jesus",
        start_phrase="Repare em uma coisa importante",
        end_phrase="transformar cada erro numa condenação sem fim",
        visuals=(
            ("images/img-s06-biblia-mesa-v1.png", "52% 54%", 1.14),
            ("images/img-s10-responsabilidades-v1.png", "50% 48%", 1.13),
            ("images/img-s11-controle-v1.png", "48% 50%", 1.15),
            ("images/img-s13-caminhada-v1.png", "54% 51%", 1.14),
            ("images/img-s28-escolhas-do-outro-v1.png", "47% 50%", 1.13),
            ("images/img-s24-entrega-v1.png", "32% 48%", 1.13),
            ("images/img-s17-pausa-v1.png", "50% 48%", 1.15),
            ("images/img-s06-biblia-mesa-v1.png", "52% 54%", 1.18),
        ),
    ),
    ShortSpec(
        short_id="04",
        title="Quando o cuidado se transforma em prisão",
        block_id="03-o-peso-que-nao-aparece",
        start_phrase="Outros pesos quase nunca recebem nome",
        end_phrase="Pode chegar sem saber como vai resolver tudo",
        visuals=(
            ("images/img-s16-peso-mental-v1.png", "52% 49%", 1.14),
            ("images/img-s14-pesos-visiveis-v1.png", "50% 50%", 1.13),
            ("images/img-s03-tarefas-v1.png", "50% 48%", 1.14),
            ("images/img-s17-pausa-v1.png", "50% 48%", 1.13),
            ("images/img-s18-chegar-cansada-v1.png", "52% 48%", 1.15),
            ("images/img-s04-reflexo-v1.png", "48% 49%", 1.14),
            ("images/img-s05-maos-em-pausa-v1.png", "50% 52%", 1.13),
            ("images/img-s18-chegar-cansada-v1.png", "52% 48%", 1.17),
        ),
    ),
    ShortSpec(
        short_id="05",
        title="Pedir ajuda não diminui a sua fé",
        block_id="04-cargas-compartilhadas",
        start_phrase="Maturidade não é se tornar uma pessoa",
        end_phrase="conversas sinceras e de apoio concreto",
        visuals=(
            ("images/img-s19-carga-compartilhada-v1.png", "50% 49%", 1.14),
            ("images/img-s21-pedir-ajuda-v1.png", "52% 49%", 1.13),
            ("images/img-s22-conversa-confiavel-v1.png", "50% 50%", 1.14),
            ("images/img-s23-apoio-concreto-v1.png", "48% 49%", 1.13),
            ("images/img-s32-contato-seguro-v1.png", "52% 50%", 1.15),
            ("images/img-s12-escuta-v1.png", "50% 49%", 1.14),
            ("images/img-s19-carga-compartilhada-v1.png", "50% 49%", 1.16),
            ("images/img-s23-apoio-concreto-v1.png", "48% 49%", 1.17),
        ),
    ),
    ShortSpec(
        short_id="06",
        title="Entregar a ansiedade não é negar a realidade",
        block_id="05-entregar-nao-e-negar",
        start_phrase="Lançando sobre ele toda a vossa ansiedade",
        end_phrase="também precisa fazer as próprias escolhas",
        visuals=(
            ("images/img-s06-biblia-mesa-v1.png", "52% 54%", 1.14),
            ("images/img-s24-entrega-v1.png", "32% 48%", 1.13),
            ("images/img-s23-apoio-concreto-v1.png", "48% 49%", 1.14),
            ("images/img-s17-pausa-v1.png", "50% 48%", 1.13),
            ("images/img-s28-escolhas-do-outro-v1.png", "47% 50%", 1.14),
            ("images/img-s04-reflexo-v1.png", "48% 49%", 1.15),
            ("images/img-s05-maos-em-pausa-v1.png", "50% 52%", 1.14),
            ("images/img-s24-entrega-v1.png", "32% 48%", 1.17),
        ),
    ),
)


def normalize_token(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]", "", value.lower())


def alignment_words(path: Path, offset: float) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    alignment = payload["alignment"]
    chars = alignment["characters"]
    starts = alignment["character_start_times_seconds"]
    ends = alignment["character_end_times_seconds"]
    words: list[dict[str, Any]] = []
    start_index: int | None = None
    for index in range(len(chars) + 1):
        char = chars[index] if index < len(chars) else " "
        if index < len(chars) and not char.isspace() and start_index is None:
            start_index = index
        if (index == len(chars) or char.isspace()) and start_index is not None:
            token = "".join(chars[start_index:index]).strip()
            if token and normalize_token(token):
                words.append(
                    {
                        "word": token,
                        "normalized": normalize_token(token),
                        "start": float(starts[start_index]) + offset,
                        "end": float(ends[index - 1]) + offset,
                    }
                )
            start_index = None
    return words


def phrase_tokens(value: str) -> list[str]:
    return [token for token in (normalize_token(part) for part in value.split()) if token]


def find_phrase(words: list[dict[str, Any]], phrase: str) -> tuple[int, int]:
    needle = phrase_tokens(phrase)
    haystack = [word["normalized"] for word in words]
    for start in range(0, len(haystack) - len(needle) + 1):
        if haystack[start : start + len(needle)] == needle:
            return start, start + len(needle) - 1
    raise ValueError(f"Phrase not found: {phrase}")


def caption_cues(words: list[dict[str, Any]], clip_start: float) -> list[dict[str, Any]]:
    groups: list[list[dict[str, Any]]] = []
    current: list[dict[str, Any]] = []
    for word in words:
        candidate = current + [word]
        text = " ".join(item["word"] for item in candidate)
        long_pause = bool(current and word["start"] - current[-1]["end"] > 0.62)
        too_long = len(candidate) > 9 or len(text) > 67 or word["end"] - candidate[0]["start"] > 4.8
        if current and (long_pause or too_long):
            groups.append(current)
            current = [word]
        else:
            current = candidate
        strong_boundary = current and current[-1]["word"].endswith((".", "?", "!", ":")) and len(current) >= 4
        readable_comma = current and current[-1]["word"].endswith(",") and len(current) >= 7
        if strong_boundary or readable_comma:
            groups.append(current)
            current = []
    if current:
        groups.append(current)

    rebalanced: list[list[dict[str, Any]]] = []
    for group in groups:
        if len(group) <= 2 and rebalanced:
            combined = rebalanced[-1] + group
            combined_text = " ".join(item["word"] for item in combined)
            if len(combined) <= 10 and len(combined_text) <= 75:
                rebalanced[-1] = combined
                continue
        rebalanced.append(group)
    groups = rebalanced

    return [
        {
            "start": round(group[0]["start"] - clip_start, 3),
            "end": round(group[-1]["end"] - clip_start, 3),
            "text": " ".join(item["word"] for item in group),
        }
        for group in groups
    ]


def visual_plan(spec: ShortSpec, spoken_duration: float) -> list[dict[str, Any]]:
    segment = spoken_duration / len(spec.visuals)
    result = []
    for index, (asset, focus, scale) in enumerate(spec.visuals):
        start = round(index * segment, 3)
        end = round(spoken_duration if index == len(spec.visuals) - 1 else (index + 1) * segment, 3)
        result.append({"start": start, "end": end, "asset": asset, "focus": focus, "scale": scale})
    return result


def run_ffmpeg(start: float, duration: float, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    command = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "error",
        "-y",
        "-ss",
        f"{start:.6f}",
        "-i",
        str(SOURCE_AUDIO),
        "-t",
        f"{duration:.6f}",
        "-ar",
        "48000",
        "-ac",
        "1",
        "-c:a",
        "pcm_s16le",
        str(output),
    ]
    subprocess.run(command, check=True)


def main() -> None:
    generation = json.loads((AUDIO_ROOT / "resultado-geracao.json").read_text(encoding="utf-8-sig"))
    block_offsets: dict[str, float] = {}
    offset = 0.0
    for result in generation["results"]:
        block_offsets[result["block_id"]] = offset
        offset += float(result["duration_seconds"])

    PROPS_ROOT.mkdir(parents=True, exist_ok=True)
    PUBLIC_AUDIO.mkdir(parents=True, exist_ok=True)
    outputs: list[dict[str, Any]] = []

    for spec in SPECS:
        offset = block_offsets[spec.block_id]
        words = alignment_words(AUDIO_ROOT / f"{spec.block_id}.alignment.json", offset)
        start_index, _ = find_phrase(words, spec.start_phrase)
        _, end_index = find_phrase(words, spec.end_phrase)
        selected = words[start_index : end_index + 1]
        clip_start = max(0.0, selected[0]["start"] - 0.12)
        clip_end = selected[-1]["end"] + 0.24
        spoken_duration = round(clip_end - clip_start, 3)
        audio_name = f"piloto-001-short-{spec.short_id}-narracao.wav"
        audio_output = PUBLIC_AUDIO / audio_name
        run_ffmpeg(clip_start, spoken_duration, audio_output)

        base_props = {
            "derivativeId": f"piloto-001-short-{spec.short_id}",
            "title": spec.title,
            "audioFile": f"audio/{audio_name}",
            "spokenDurationSeconds": spoken_duration,
            "endCardSeconds": 4.0,
            "visuals": visual_plan(spec, spoken_duration),
            "cues": caption_cues(selected, clip_start),
        }
        platform_files = {}
        for platform in ("tiktok", "youtube_shorts"):
            props = dict(base_props)
            props["platform"] = platform
            props_path = PROPS_ROOT / f"piloto-001-short-{spec.short_id}-{platform}.json"
            props_path.write_text(json.dumps(props, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            platform_files[platform] = str(props_path.relative_to(ROOT)).replace("\\", "/")

        outputs.append(
            {
                "derivative_id": base_props["derivativeId"],
                "title": spec.title,
                "source_block": spec.block_id,
                "source_window_seconds": {"start": round(clip_start, 3), "end": round(clip_end, 3)},
                "spoken_duration_seconds": spoken_duration,
                "total_duration_seconds": round(spoken_duration + 4.0, 3),
                "audio": str(audio_output.relative_to(ROOT)).replace("\\", "/"),
                "props": platform_files,
                "paid_api_cost_usd": 0,
            }
        )

    manifest = {
        "schema_version": 1,
        "source_video": "piloto-001",
        "new_derivatives": outputs,
        "existing_approved_derivative": "piloto-001-vertical-01",
        "total_content_derivatives_after_build": 6,
        "paid_api_cost_usd": 0,
        "method": "Dedicated WAV excerpts, canonical ElevenLabs alignments, local Remotion composition and local FFmpeg rendering.",
    }
    (WORK_ROOT / "manifest-v1.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
