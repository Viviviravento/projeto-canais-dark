from __future__ import annotations

import json
import re
import subprocess
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "tools" / "OpenMontage" / "projects" / "a-palavra-que-cuida-video-002"
AUDIO_ROOT = ROOT / "operations" / "a-palavra-que-cuida" / "05_audio" / "video-002" / "v2"
SOURCE_AUDIO = AUDIO_ROOT / "video-002-narracao-v2-producao.wav"
WORK_ROOT = ROOT / "operations" / "a-palavra-que-cuida" / "06_edicao" / "video-002" / "shorts"
PROPS_ROOT = WORK_ROOT / "props"
PUBLIC_AUDIO = PROJECT / "public" / "audio"
GAP_SECONDS = 0.18


@dataclass(frozen=True)
class SegmentSpec:
    block_id: str
    start_phrase: str
    end_phrase: str


@dataclass(frozen=True)
class ShortSpec:
    short_id: str
    title: str
    segments: tuple[SegmentSpec, ...]
    visuals: tuple[tuple[str, str, float], ...]


SPECS = (
    ShortSpec(
        short_id="01",
        title="Ansiedade não é falta de fé",
        segments=(
            SegmentSpec(
                block_id="05-nao-e-uma-condenacao-medica",
                start_phrase="Aqui precisamos fazer uma distinção importante",
                end_phrase="está simplesmente desobedecendo a Jesus",
            ),
            SegmentSpec(
                block_id="05-nao-e-uma-condenacao-medica",
                start_phrase="Fé e tratamento não são rivais",
                end_phrase="onde colocamos nossa esperança",
            ),
        ),
        visuals=(
            ("images/img-v002-cansaco-amanhecer-v1.png", "70% 48%", 1.00),
            ("images/img-v002-espera-saude-v1.png", "41% 48%", 1.00),
            ("images/img-s27-ajuda-profissional-v1.png", "34% 48%", 1.00),
            ("images/img-s24-entrega-v1.png", "32% 48%", 1.00),
            ("images/img-s32-contato-seguro-v1.png", "50% 48%", 1.00),
            ("images/img-v002-jesus-ouvinte-mulher-v2.png", "75% 48%", 1.00),
            ("images/img-s22-conversa-confiavel-v1.png", "50% 49%", 1.00),
            ("images/img-v002-amanhecer-presente-v1.png", "55% 48%", 1.00),
            ("images/img-v002-cansaco-amanhecer-v1.png", "70% 48%", 1.03),
        ),
    ),
    ShortSpec(
        short_id="02",
        title="Três perguntas para quando a preocupação crescer",
        segments=(
            SegmentSpec(
                block_id="07-o-tamanho-de-um-dia",
                start_phrase="O convite é parar de somar",
                end_phrase="todo o espaço do presente",
            ),
        ),
        visuals=(
            ("images/img-v002-cansaco-amanhecer-v1.png", "70% 48%", 1.00),
            ("images/img-v002-noite-pensamentos-v1.png", "85% 48%", 1.00),
            ("images/img-v002-orcamento-rotulos-integrados-v2.png", "55% 50%", 1.00),
            ("images/img-v002-ligacao-documentos-v1.png", "60% 48%", 1.00),
            ("images/img-s33-fechar-trabalho-v1.png", "55% 48%", 1.00),
            ("images/img-s32-contato-seguro-v1.png", "50% 48%", 1.00),
            ("images/img-s28-escolhas-do-outro-v1.png", "47% 48%", 1.00),
            ("images/img-v002-amanhecer-presente-v1.png", "55% 48%", 1.00),
            ("images/img-v002-cansaco-amanhecer-v1.png", "70% 48%", 1.03),
        ),
    ),
)


MAPPED_CANDIDATES = (
    {
        "candidate_id": "video-002-short-01",
        "promise": "Ansiedade não é falta de fé; procurar tratamento pode ser cuidado responsável.",
        "source_block": "05-nao-e-uma-condenacao-medica",
        "priority": "render",
    },
    {
        "candidate_id": "video-002-short-02",
        "promise": "Três perguntas práticas para separar fato, ação possível e o peso de amanhã.",
        "source_block": "07-o-tamanho-de-um-dia",
        "priority": "render",
    },
    {
        "candidate_id": "video-002-candidate-03",
        "promise": "Cuidado responsável não é o mesmo que tentar controlar o futuro.",
        "source_block": "03-necessidades-reais",
        "priority": "mapped_not_rendered",
    },
    {
        "candidate_id": "video-002-candidate-04",
        "promise": "Confiar não é cruzar os braços, mas agir sem se tornar soberana.",
        "source_block": "04-aves-flores-e-limite-do-controle",
        "priority": "mapped_not_rendered",
    },
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


def caption_cues(
    words: list[dict[str, Any]],
    clip_start: float,
    timeline_offset: float,
) -> list[dict[str, Any]]:
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
        strong_boundary = current[-1]["word"].endswith((".", "?", "!", ":")) and len(current) >= 4
        readable_comma = current[-1]["word"].endswith(",") and len(current) >= 7
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

    return [
        {
            "start": round(timeline_offset + group[0]["start"] - clip_start, 3),
            "end": round(timeline_offset + group[-1]["end"] - clip_start, 3),
            "text": " ".join(item["word"] for item in group),
        }
        for group in rebalanced
    ]


def visual_plan(spec: ShortSpec, spoken_duration: float) -> list[dict[str, Any]]:
    segment = spoken_duration / len(spec.visuals)
    result = []
    for index, (asset, focus, scale) in enumerate(spec.visuals):
        start = round(index * segment, 3)
        end = round(spoken_duration if index == len(spec.visuals) - 1 else (index + 1) * segment, 3)
        result.append({"start": start, "end": end, "asset": asset, "focus": focus, "scale": scale})
    return result


def run_ffmpeg_segments(segments: list[tuple[float, float]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    if len(segments) == 1:
        start, end = segments[0]
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
            f"{end - start:.6f}",
            "-ar",
            "48000",
            "-ac",
            "1",
            "-c:a",
            "pcm_s16le",
            str(output),
        ]
        subprocess.run(command, check=True)
        return

    filters: list[str] = []
    concat_inputs: list[str] = []
    for index, (start, end) in enumerate(segments):
        filters.append(
            f"[0:a]atrim=start={start:.6f}:end={end:.6f},"
            f"asetpts=PTS-STARTPTS,aresample=48000[a{index}]"
        )
        concat_inputs.append(f"[a{index}]")
        if index < len(segments) - 1:
            filters.append(
                f"anullsrc=r=48000:cl=mono,atrim=duration={GAP_SECONDS:.3f}[gap{index}]"
            )
            concat_inputs.append(f"[gap{index}]")
    filters.append(
        "".join(concat_inputs)
        + f"concat=n={len(concat_inputs)}:v=0:a=1[out]"
    )
    command = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "error",
        "-y",
        "-i",
        str(SOURCE_AUDIO),
        "-filter_complex",
        ";".join(filters),
        "-map",
        "[out]",
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
        selected_segments: list[dict[str, Any]] = []
        for segment_spec in spec.segments:
            block_offset = block_offsets[segment_spec.block_id]
            words = alignment_words(
                AUDIO_ROOT / f"{segment_spec.block_id}.alignment.json",
                block_offset,
            )
            start_index, _ = find_phrase(words, segment_spec.start_phrase)
            _, end_index = find_phrase(words, segment_spec.end_phrase)
            selected = words[start_index : end_index + 1]
            clip_start = max(0.0, selected[0]["start"] - 0.12)
            clip_end = selected[-1]["end"] + 0.24
            selected_segments.append(
                {
                    "block_id": segment_spec.block_id,
                    "start": clip_start,
                    "end": clip_end,
                    "words": selected,
                }
            )

        audio_name = f"video-002-short-{spec.short_id}-narracao.wav"
        audio_output = PUBLIC_AUDIO / audio_name
        run_ffmpeg_segments(
            [(segment["start"], segment["end"]) for segment in selected_segments],
            audio_output,
        )

        cues: list[dict[str, Any]] = []
        timeline_offset = 0.0
        source_windows = []
        for index, segment in enumerate(selected_segments):
            cues.extend(
                caption_cues(
                    segment["words"],
                    segment["start"],
                    timeline_offset,
                )
            )
            duration = segment["end"] - segment["start"]
            source_windows.append(
                {
                    "block_id": segment["block_id"],
                    "start": round(segment["start"], 3),
                    "end": round(segment["end"], 3),
                }
            )
            timeline_offset += duration
            if index < len(selected_segments) - 1:
                timeline_offset += GAP_SECONDS

        spoken_duration = round(timeline_offset, 3)
        if spoken_duration < 65:
            raise ValueError(
                f"{spec.short_id} has only {spoken_duration:.3f}s; video 002 requires at least 65s"
            )

        base_props = {
            "derivativeId": f"video-002-short-{spec.short_id}",
            "title": spec.title,
            "audioFile": f"audio/{audio_name}",
            "spokenDurationSeconds": spoken_duration,
            "endCardSeconds": 4.0,
            "visuals": visual_plan(spec, spoken_duration),
            "cues": cues,
        }
        platform_files = {}
        for platform in ("tiktok", "youtube_shorts"):
            props = dict(base_props)
            props["platform"] = platform
            props_path = PROPS_ROOT / f"video-002-short-{spec.short_id}-{platform}.json"
            props_path.write_text(
                json.dumps(props, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            platform_files[platform] = str(props_path.relative_to(ROOT)).replace("\\", "/")

        outputs.append(
            {
                "derivative_id": base_props["derivativeId"],
                "title": spec.title,
                "source_windows": source_windows,
                "spoken_duration_seconds": spoken_duration,
                "total_duration_seconds": round(spoken_duration + 4.0, 3),
                "audio": str(audio_output.relative_to(ROOT)).replace("\\", "/"),
                "props": platform_files,
                "paid_api_cost_usd": 0,
            }
        )

    manifest = {
        "schema_version": 1,
        "source_video": "video-002",
        "mapped_candidates": MAPPED_CANDIDATES,
        "rendered_editorial_derivatives": outputs,
        "editorial_derivative_count": len(outputs),
        "platform_output_count": len(outputs) * 2,
        "paid_api_cost_usd": 0,
        "method": (
            "Trechos dedicados da narração aprovada, alinhamentos canônicos da ElevenLabs, "
            "recomposição vertical com assets originais e render local."
        ),
    }
    (WORK_ROOT / "manifest-v1.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
