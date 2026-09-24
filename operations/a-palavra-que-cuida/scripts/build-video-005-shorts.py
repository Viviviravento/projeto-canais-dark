from __future__ import annotations

import json
import re
import subprocess
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "tools" / "OpenMontage" / "projects" / "a-palavra-que-cuida-video-005"
SOURCE_AUDIO = (
    ROOT
    / "operations" / "a-palavra-que-cuida"
    / "05_audio"
    / "video-005"
    / "v1"
    / "video-005-narracao-v1-1.05x-master.wav"
)
ALIGNMENT = (
    ROOT
    / "operations" / "a-palavra-que-cuida"
    / "05_audio"
    / "video-005"
    / "v1"
    / "master-alignment-1.05x.json"
)
WORK_ROOT = ROOT / "operations" / "a-palavra-que-cuida" / "06_edicao" / "video-005" / "shorts"
PROPS_ROOT = WORK_ROOT / "props"
PUBLIC_AUDIO = (
    ROOT / "tools" / "OpenMontage" / "remotion-composer" / "public" / "video-005-curtos" / "audio"
)
GAP_SECONDS = 0.18


@dataclass(frozen=True)
class SegmentSpec:
    start_phrase: str
    end_phrase: str


@dataclass(frozen=True)
class VisualSpec:
    end: float
    asset: str
    focus: str
    fit: str = "cover"
    scale: float = 1.08


@dataclass(frozen=True)
class ScriptureSpec:
    start_phrase: str
    end_phrase: str
    text: str
    reference: str


@dataclass(frozen=True)
class ShortSpec:
    short_id: str
    title: str
    hook: str
    segments: tuple[SegmentSpec, ...]
    visuals: tuple[VisualSpec, ...]
    scriptures: tuple[ScriptureSpec, ...]


SPECS = (
    ShortSpec(
        short_id="01",
        title="Você não começa a ter valor quando produz muito",
        hook="Seu valor vem antes da performance",
        segments=(
            SegmentSpec(
                "Gênesis capítulo um versículo vinte e sete diz",
                "idade ou ferida",
            ),
        ),
        visuals=(
            VisualSpec(9.0, "video-005/assets/library/cotidiano_brasileiro/p001-reflexo-v1.png", "70% 50%"),
            VisualSpec(18.0, "video-005/assets/library/cotidiano_brasileiro/p001-chegar-cansada-v1.png", "50% 50%"),
            VisualSpec(27.0, "video-005/assets/library/apoio_relacoes/p001-carga-compartilhada-v1.png", "68% 50%"),
            VisualSpec(36.0, "video-005/assets/library/cotidiano_brasileiro/p001-pausa-v1.png", "52% 50%"),
            VisualSpec(45.0, "video-005/assets/library/cotidiano_brasileiro/v002-amanhecer-presente-v1.png", "72% 50%"),
            VisualSpec(54.0, "video-005/assets/library/cotidiano_brasileiro/p001-reflexo-v1.png", "70% 50%"),
            VisualSpec(63.0, "video-005/assets/library/apoio_relacoes/p001-carga-compartilhada-v1.png", "68% 50%"),
            VisualSpec(72.0, "video-005/assets/library/apoio_relacoes/p001-escuta-v1.png", "76% 50%"),
            VisualSpec(999.0, "video-005/assets/library/cotidiano_brasileiro/v002-amanhecer-presente-v1.png", "72% 50%"),
        ),
        scriptures=(
            ScriptureSpec(
                "E criou Deus o homem à sua imagem",
                "homem e mulher os criou",
                "E criou Deus o homem à sua imagem; à imagem de Deus o criou; homem e mulher os criou.",
                "Gênesis 1:27 — ACF",
            ),
        ),
    ),
    ShortSpec(
        short_id="02",
        title="Descansar não é falhar",
        hook="Descansar não é falhar",
        segments=(
            SegmentSpec(
                "Mesmo lendo apenas alguns versículos",
                "nós não somos o Criador",
            ),
        ),
        visuals=(
            VisualSpec(9.0, "video-005/assets/library/objetos_cenarios/p001-maos-em-pausa-v1.png", "50% 50%"),
            VisualSpec(18.0, "video-005/assets/library/cotidiano_brasileiro/p001-pausa-v1.png", "52% 50%"),
            VisualSpec(27.0, "video-005/assets/library/cotidiano_brasileiro/p001-chegar-cansada-v1.png", "50% 50%"),
            VisualSpec(36.0, "video-005/assets/video004/brazil/b08-tempo-de-ouvir-v1.png", "38% 50%"),
            VisualSpec(45.0, "video-005/assets/library/cotidiano_brasileiro/v002-amanhecer-presente-v1.png", "72% 50%"),
            VisualSpec(54.0, "video-005/assets/library/cotidiano_brasileiro/p001-reflexo-v1.png", "70% 50%"),
            VisualSpec(63.0, "video-005/assets/library/cotidiano_brasileiro/p001-pausa-v1.png", "52% 50%"),
            VisualSpec(999.0, "video-005/assets/video004/brazil/b08-tempo-de-ouvir-v1.png", "38% 50%"),
        ),
        scriptures=(),
    ),
)


def normalize_token(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]", "", value.lower())


def alignment_words() -> list[dict[str, Any]]:
    payload = json.loads(ALIGNMENT.read_text(encoding="utf-8-sig"))
    words: list[dict[str, Any]] = []
    for block in payload["blocks"]:
        chars = block["characters"]
        starts = block["character_start_times_seconds"]
        ends = block["character_end_times_seconds"]
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
                            "start": float(starts[start_index]),
                            "end": float(ends[index - 1]),
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


def caption_cues(words: list[dict[str, Any]], clip_start: float, timeline_offset: float) -> list[dict[str, Any]]:
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
    return [
        {
            "start": round(timeline_offset + group[0]["start"] - clip_start, 3),
            "end": round(timeline_offset + group[-1]["end"] - clip_start, 3),
            "text": " ".join(item["word"] for item in group),
        }
        for group in groups
    ]


def make_visuals(spec: ShortSpec, duration: float) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    start = 0.0
    for visual in spec.visuals:
        end = min(duration, visual.end)
        if end <= start:
            break
        result.append(
            {
                "start": round(start, 3),
                "end": round(end, 3),
                "asset": visual.asset,
                "focus": visual.focus,
                "scale": visual.scale,
                "fit": visual.fit,
            }
        )
        start = end
        if start >= duration:
            break
    if result:
        result[-1]["end"] = round(duration, 3)
    return result


def render_audio(segments: list[tuple[float, float]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    filters: list[str] = []
    inputs: list[str] = []
    for index, (start, end) in enumerate(segments):
        filters.append(
            f"[0:a]atrim=start={start:.6f}:end={end:.6f},asetpts=PTS-STARTPTS,aresample=48000[a{index}]"
        )
        inputs.append(f"[a{index}]")
        if index < len(segments) - 1:
            filters.append(f"anullsrc=r=48000:cl=mono,atrim=duration={GAP_SECONDS:.3f}[gap{index}]")
            inputs.append(f"[gap{index}]")
    filters.append("".join(inputs) + f"concat=n={len(inputs)}:v=0:a=1[out]")
    subprocess.run(
        [
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(SOURCE_AUDIO),
            "-filter_complex", ";".join(filters), "-map", "[out]", "-ar", "48000", "-ac", "1",
            "-c:a", "pcm_s16le", str(output),
        ],
        check=True,
    )


def main() -> None:
    words = alignment_words()
    PROPS_ROOT.mkdir(parents=True, exist_ok=True)
    PUBLIC_AUDIO.mkdir(parents=True, exist_ok=True)
    outputs: list[dict[str, Any]] = []

    for spec in SPECS:
        selected_segments: list[dict[str, Any]] = []
        for segment in spec.segments:
            start_index, _ = find_phrase(words, segment.start_phrase)
            _, end_index = find_phrase(words, segment.end_phrase)
            selected = words[start_index : end_index + 1]
            selected_segments.append(
                {
                    "start": max(0.0, selected[0]["start"] - 0.08),
                    "end": selected[-1]["end"] + 0.15,
                    "words": selected,
                }
            )

        audio_name = f"video-005-curto-{spec.short_id}-narracao.wav"
        audio_output = PUBLIC_AUDIO / audio_name
        render_audio([(item["start"], item["end"]) for item in selected_segments], audio_output)

        cues: list[dict[str, Any]] = []
        source_windows: list[dict[str, float]] = []
        segment_offsets: list[float] = []
        timeline_offset = 0.0
        for index, segment in enumerate(selected_segments):
            segment_offsets.append(timeline_offset)
            cues.extend(caption_cues(segment["words"], segment["start"], timeline_offset))
            source_windows.append({"start": round(segment["start"], 3), "end": round(segment["end"], 3)})
            timeline_offset += segment["end"] - segment["start"]
            if index < len(selected_segments) - 1:
                timeline_offset += GAP_SECONDS
        spoken_duration = round(timeline_offset, 3)
        if spoken_duration < 60:
            raise ValueError(f"Short {spec.short_id} is only {spoken_duration}s")

        scriptures: list[dict[str, Any]] = []
        for scripture in spec.scriptures:
            start_index, _ = find_phrase(words, scripture.start_phrase)
            _, end_index = find_phrase(words, scripture.end_phrase)
            source_start = words[start_index]["start"]
            source_end = words[end_index]["end"]
            containing_index = next(
                i for i, segment in enumerate(selected_segments)
                if segment["start"] <= source_start <= segment["end"]
            )
            segment = selected_segments[containing_index]
            scriptures.append(
                {
                    "start": round(segment_offsets[containing_index] + source_start - segment["start"], 3),
                    "end": round(segment_offsets[containing_index] + source_end - segment["start"], 3),
                    "text": scripture.text,
                    "reference": scripture.reference,
                }
            )

        props = {
            "derivativeId": f"video-005-curto-{spec.short_id}",
            "title": spec.title,
            "platform": "universal",
            "audioFile": f"video-005-curtos/audio/{audio_name}",
            "spokenDurationSeconds": spoken_duration,
            "endCardSeconds": 4.0,
            "hook": spec.hook,
            "hookEndSeconds": 4.2,
            "visuals": make_visuals(spec, spoken_duration),
            "cues": cues,
            "scriptures": scriptures,
        }
        props_path = PROPS_ROOT / f"video-005-curto-{spec.short_id}-shorts-e-tiktok.json"
        props_path.write_text(json.dumps(props, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        outputs.append(
            {
                "derivative_id": props["derivativeId"],
                "title": spec.title,
                "source_windows": source_windows,
                "spoken_duration_seconds": spoken_duration,
                "total_duration_seconds": round(spoken_duration + 4.0, 3),
                "audio": str(audio_output.relative_to(ROOT)).replace("\\", "/"),
                "props": str(props_path.relative_to(ROOT)).replace("\\", "/"),
                "platforms": ["youtube_shorts", "tiktok"],
                "paid_api_cost_usd": 0,
            }
        )

    manifest = {
        "schema_version": 1,
        "source_video": "video-005",
        "rendered_editorial_derivatives": outputs,
        "editorial_derivative_count": 2,
        "physical_mp4_target_count": 2,
        "paid_api_cost_usd": 0,
        "method": "Narração e imagens já aprovadas, alinhamento canônico, recomposição vertical manual em cover e render local.",
    }
    (WORK_ROOT / "manifest-v1.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
