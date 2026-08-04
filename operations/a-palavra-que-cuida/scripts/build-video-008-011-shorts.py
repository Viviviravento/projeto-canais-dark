from __future__ import annotations

"""Build the eight approved-format vertical derivatives for videos 008--011.

The render is deliberately made from the canonical narration and approved stills,
not from a horizontal long-form export.  Each image is recomposed in 9:16 cover
with a manually chosen focal point, so the person remains present in the frame.
"""

import importlib.util
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
HELPER_PATH = ROOT / "operations/a-palavra-que-cuida/scripts/build-video-006-shorts.py"
helper_spec = importlib.util.spec_from_file_location("short_builder_helper", HELPER_PATH)
if helper_spec is None or helper_spec.loader is None:
    raise RuntimeError(f"Unable to load helper: {HELPER_PATH}")
helper = importlib.util.module_from_spec(helper_spec)
sys.modules[helper_spec.name] = helper
helper_spec.loader.exec_module(helper)

EXPORT_ROOT = ROOT / "operations/a-palavra-que-cuida/07_exports/shorts-aprovados"
FONT = "C:/Windows/Fonts/arialbd.ttf"
END_CARD_SECONDS = 3.0


@dataclass(frozen=True)
class Segment:
    start_phrase: str
    end_phrase: str


@dataclass(frozen=True)
class Image:
    filename: str
    focus_x: float


@dataclass(frozen=True)
class Short:
    number: str
    title: str
    hook: str
    segments: tuple[Segment, ...]
    images: tuple[Image, ...]


@dataclass(frozen=True)
class Video:
    number: str
    audio: str
    alignment: str
    shorts: tuple[Short, ...]


# Phrase lookups intentionally use ASCII.  The helper normalizes accents before
# matching, which keeps this source file and the timestamp match deterministic.
VIDEOS = (
    Video(
        "008",
        "operations/a-palavra-que-cuida/05_audio/video-008/v1/video-008-narracao-v1-1.07x-master.wav",
        "operations/a-palavra-que-cuida/05_audio/video-008/v1/master-alignment-1.07x.json",
        (
            Short(
                "01", "Uma queda não precisa ser o fim da história",
                "Jesus não confundiu a queda de Pedro com o fim da história.",
                (
                    Segment("A historia de Pedro passa por esse lugar.", "o futuro de Pedro tambem nao."),
                ),
                (
                    Image("v02-pedro-antes-do-patio-v1.png", 0.50),
                    Image("v04-pedro-perto-do-fogo-v1.png", 0.62),
                    Image("v05-choro-sem-espetaculo-v1.png", 0.26),
                    Image("v06-encontro-a-beira-do-mar-v1.png", 0.56),
                    Image("v03-verdade-no-corredor-v1.png", 0.53),
                    Image("v07-passo-novo-pela-manha-v1.png", 0.50),
                    Image("v01-lembranca-na-cozinha-com-croche-v1.png", 0.43),
                ),
            ),
            Short(
                "02", "Pedir perdão não compra reconciliação",
                "Pedir perdão não compra reconciliação. É um passo de verdade.",
                (
                    Segment("Ha tres movimentos simples que podem ajudar a comecar.", "mudando de caminho."),
                ),
                (
                    Image("v05-choro-sem-espetaculo-v1.png", 0.26),
                    Image("v03-verdade-no-corredor-v1.png", 0.52),
                    Image("v01-lembranca-na-cozinha-com-croche-v1.png", 0.43),
                    Image("v06-encontro-a-beira-do-mar-v1.png", 0.58),
                    Image("v07-passo-novo-pela-manha-v1.png", 0.50),
                    Image("v02-pedro-antes-do-patio-v1.png", 0.50),
                ),
            ),
        ),
    ),
    Video(
        "009",
        "operations/a-palavra-que-cuida/05_audio/video-009/v1/video-009-narracao-v1-1.07x-master.wav",
        "operations/a-palavra-que-cuida/05_audio/video-009/v1/master-alignment-1.07x.json",
        (
            Short(
                "01", "Jesus começa a conversa antes do julgamento",
                "Jesus não começou perguntando pelo passado dela. Pediu água.",
                (
                    Segment("Joao, capitulo quatro, versiculo sete, diz:", "possibilidade de futuro."),
                ),
                (
                    Image("v05-conversa-no-poco.png", 0.70),
                    Image("v03-jesus-junto-ao-poco.png", 0.72),
                    Image("v02-samaritana-caminho-poco.png", 0.49),
                    Image("v01-manha-em-casa.png", 0.25),
                    Image("v06-caminho-ate-a-cidade.png", 0.50),
                    Image("v07-historia-vira-ponte.png", 0.50),
                ),
            ),
            Short(
                "02", "Verdade não é humilhação",
                "Deus conhece a verdade da sua história e isso não precisa virar humilhação.",
                (
                    Segment("Em certo momento, Jesus pede que a mulher", "ela nao precisa mentir diante dele."),
                    Segment("Isso nao autoriza ninguem a invadir sua vida.", "a um profissional."),
                ),
                (
                    Image("v04-verdade-sem-humilhacao.png", 0.80),
                    Image("v05-conversa-no-poco.png", 0.70),
                    Image("v03-jesus-junto-ao-poco.png", 0.72),
                    Image("v01-manha-em-casa.png", 0.25),
                    Image("v07-historia-vira-ponte.png", 0.50),
                    Image("v06-caminho-ate-a-cidade.png", 0.50),
                ),
            ),
        ),
    ),
    Video(
        "010",
        "operations/a-palavra-que-cuida/05_audio/video-010/v1/video-010-narracao-v1-1.07x-master.wav",
        "operations/a-palavra-que-cuida/05_audio/video-010/v1/master-alignment-1.07x.json",
        (
            Short(
                "01", "O medo pode estar no barco sem ser o capitão",
                "Sentir medo não prova que você perdeu a fé.",
                (
                    Segment("Essa frase pode ser usada como acusacao,", "dar o proximo passo possivel."),
                    Segment("O medo pode estar no barco sem ser o capitao.", "como uma mao que ainda consegue chamar por Jesus."),
                ),
                (
                    Image("v01-ansiedade-na-cozinha.png", 0.25),
                    Image("v02-barco-na-tempestade.png", 0.46),
                    Image("v05-medo-na-vida-real.png", 0.22),
                    Image("v06-apoio-que-escuta.png", 0.50),
                    Image("v07-depois-da-chuva.png", 0.54),
                    Image("v04-tempestade-se-acalma.png", 0.69),
                ),
            ),
            Short(
                "02", "Uma oração desesperada ainda é uma oração",
                "Quando parece que Deus está dormindo enquanto o barco enche.",
                (
                    Segment("No meio do temporal, Jesus esta dormindo", "a conclusao deles ainda precisava ser examinada."),
                ),
                (
                    Image("v03-jesus-dorme-no-barco.png", 0.68),
                    Image("v02-barco-na-tempestade.png", 0.46),
                    Image("v04-tempestade-se-acalma.png", 0.69),
                    Image("v06-apoio-que-escuta.png", 0.50),
                    Image("v07-depois-da-chuva.png", 0.54),
                    Image("v05-medo-na-vida-real.png", 0.22),
                ),
            ),
        ),
    ),
    Video(
        "011",
        "operations/a-palavra-que-cuida/05_audio/video-011/v1/video-011-narracao-v1-1.07x-master.wav",
        "operations/a-palavra-que-cuida/05_audio/video-011/v1/master-alignment-1.07x.json",
        (
            Short(
                "01", "Voltar não é fingir que nada aconteceu",
                "Perdão não é devolver todas as chaves no mesmo dia.",
                (
                    Segment("O pai se move de intima compaixao.", "a historia nao terminou na queda."),
                ),
                (
                    Image("v04-o-pai-corre.png", 0.61),
                    Image("v03-tornando-em-si.png", 0.48),
                    Image("v05-quem-ficou.png", 0.68),
                    Image("v06-conversa-com-limites.png", 0.25),
                    Image("v07-proximo-passo.png", 0.50),
                    Image("v01-porta-e-mala.png", 0.16),
                ),
            ),
            Short(
                "02", "Quem ficou também tem uma dor",
                "E se você não foi quem foi embora?",
                (
                    Segment("A historia poderia terminar na festa.", "O cuidado precisa alcancar os dois lados."),
                ),
                (
                    Image("v07-proximo-passo.png", 0.50),
                    Image("v06-conversa-com-limites.png", 0.25),
                    Image("v05-quem-ficou.png", 0.52),
                    Image("v02-a-partida.png", 0.49),
                    Image("v01-porta-e-mala.png", 0.16),
                    Image("v04-o-pai-corre.png", 0.61),
                ),
            ),
        ),
    ),
)


def run(command: list[str]) -> None:
    subprocess.run(command, check=True)


def escape_ass(text: str) -> str:
    return text.replace("\\", r"\\").replace("{", r"\{").replace("}", r"\}").replace("\n", r"\N")


def seconds(value: float) -> str:
    hours, remaining = divmod(max(0.0, value), 3600)
    minutes, remaining = divmod(remaining, 60)
    return f"{int(hours)}:{int(minutes):02d}:{remaining:05.2f}"


def write_ass(cues: list[dict[str, Any]], path: Path) -> None:
    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Caption,Arial,54,&H00FFFFFF,&H0000D7FF,&HDD000000,&H99000000,-1,0,0,0,100,100,0,0,3,2.5,1,2,85,85,215,1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""
    body = "".join(
        f"Dialogue: 0,{seconds(cue['start'])},{seconds(cue['end'] + 0.10)},Caption,,0,0,0,,{escape_ass(cue['text'])}\n"
        for cue in cues
    )
    path.write_text(header + body, encoding="utf-8")


def audio_and_cues(video: Video, short: Short, work_root: Path) -> tuple[Path, list[dict[str, Any]], list[dict[str, float]], float]:
    helper.ALIGNMENT = ROOT / video.alignment
    helper.SOURCE_AUDIO = ROOT / video.audio
    words = helper.alignment_words()
    selected: list[dict[str, Any]] = []
    for segment in short.segments:
        start_index, _ = helper.find_phrase(words, segment.start_phrase)
        _, end_index = helper.find_phrase(words, segment.end_phrase)
        if end_index < start_index:
            raise ValueError(f"Invalid range in video {video.number} short {short.number}")
        clip_words = words[start_index:end_index + 1]
        selected.append({
            "start": max(0.0, clip_words[0]["start"] - 0.08),
            "end": clip_words[-1]["end"] + 0.15,
            "words": clip_words,
        })
    audio_path = work_root / "audio" / f"video-{video.number}-curto-{short.number}-narracao.wav"
    helper.render_audio([(item["start"], item["end"]) for item in selected], audio_path)
    cues: list[dict[str, Any]] = []
    windows: list[dict[str, float]] = []
    offset = 0.0
    for index, item in enumerate(selected):
        cues.extend(helper.caption_cues(item["words"], item["start"], offset))
        windows.append({"start": round(item["start"], 3), "end": round(item["end"], 3)})
        offset += item["end"] - item["start"]
        if index < len(selected) - 1:
            offset += helper.GAP_SECONDS
    return audio_path, cues, windows, round(offset, 3)


def image_path(video_number: str, image: Image) -> Path:
    matches = list((ROOT / f"operations/a-palavra-que-cuida/04_assets/video-{video_number}/images").glob(image.filename))
    if len(matches) != 1:
        raise FileNotFoundError(f"Expected exactly one image matching {image.filename}; got {matches}")
    return matches[0]


def render_video(video: Video, short: Short, audio: Path, ass: Path, spoken_duration: float, output: Path) -> None:
    count = len(short.images)
    durations = [round(spoken_duration / count, 4) for _ in range(count)]
    durations[-1] = round(spoken_duration - sum(durations[:-1]), 4)
    command = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(audio)]
    for image, duration in zip(short.images, durations):
        command.extend(["-loop", "1", "-t", f"{duration:.4f}", "-i", str(image_path(video.number, image))])
    visual_filters: list[str] = []
    labels: list[str] = []
    # Assets are 16:9. Crop around an explicit focal point *before* scaling.
    # This is visually equivalent to scaling then cropping but avoids processing
    # millions of off-frame pixels on every rendered frame.
    for index, (image, duration) in enumerate(zip(short.images, durations), start=1):
        crop_x = round((1672 - 529) * image.focus_x)
        label = f"v{index}"
        visual_filters.append(
            f"[{index}:v]fps=30,crop=529:941:{crop_x}:0,scale=1080:1920,"
            f"eq=brightness=-0.02:saturation=0.96,setsar=1,trim=duration={duration:.4f},setpts=PTS-STARTPTS[{label}]"
        )
        labels.append(f"[{label}]")
    visual_filters.append("".join(labels) + f"concat=n={count}:v=1:a=0[story]")
    font_filter = FONT.replace(":", r"\:")
    visual_filters.append(
        "color=c=0x111827:s=1080x1920:r=30:d=3,"
        f"drawtext=fontfile='{font_filter}':text='A PALAVRA QUE CUIDA':fontcolor=white:fontsize=52:x=(w-text_w)/2:y=810,"
        f"drawtext=fontfile='{font_filter}':text='Reflexao completa no YouTube':fontcolor=0xD7E7FF:fontsize=34:x=(w-text_w)/2:y=895[end]"
    )
    visual_filters.append("[story][end]concat=n=2:v=1:a=0[base]")
    ass_filter = str(ass).replace("\\", "/").replace(":", r"\:").replace("'", r"\'")
    visual_filters.append(f"[base]subtitles=filename='{ass_filter}':charenc=UTF-8[vout]")
    command.extend([
        "-filter_complex", ";".join(visual_filters),
        "-map", "[vout]", "-map", "0:a?",
        "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(output),
    ])
    run(command)


def probe(path: Path) -> dict[str, Any]:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type,codec_name,width,height", "-of", "json", str(path)],
        check=True, capture_output=True, text=True,
    )
    return json.loads(result.stdout)


def main() -> None:
    EXPORT_ROOT.mkdir(parents=True, exist_ok=True)
    all_outputs: list[dict[str, Any]] = []
    for video in VIDEOS:
        work_root = ROOT / f"operations/a-palavra-que-cuida/06_edicao/video-{video.number}/shorts"
        props_root = work_root / "props"
        props_root.mkdir(parents=True, exist_ok=True)
        video_outputs: list[dict[str, Any]] = []
        for short in video.shorts:
            audio, cues, windows, spoken_duration = audio_and_cues(video, short, work_root)
            if spoken_duration < 60:
                raise ValueError(f"video-{video.number} short {short.number} is only {spoken_duration}s")
            if spoken_duration > 95:
                raise ValueError(f"video-{video.number} short {short.number} is too long: {spoken_duration}s")
            ass_path = props_root / f"video-{video.number}-curto-{short.number}-shorts-e-tiktok.ass"
            write_ass(cues, ass_path)
            output = EXPORT_ROOT / f"video-{video.number}-short-{short.number}-shorts-e-tiktok-v1.mp4"
            render_video(video, short, audio, ass_path, spoken_duration, output)
            validation = probe(output)
            video_stream = next(stream for stream in validation["streams"] if stream["codec_type"] == "video")
            if (video_stream["width"], video_stream["height"]) != (1080, 1920):
                raise ValueError(f"Wrong dimensions in {output}: {video_stream}")
            props = {
                "derivativeId": f"video-{video.number}-curto-{short.number}",
                "title": short.title,
                "platform": "universal",
                "hook": short.hook,
                "spokenDurationSeconds": spoken_duration,
                "endCardSeconds": END_CARD_SECONDS,
                "visualTreatment": "9:16 cover crops with manually selected focal points; no landscape letterboxing.",
                "cues": cues,
                "sourceWindows": windows,
            }
            props_path = props_root / f"video-{video.number}-curto-{short.number}-shorts-e-tiktok.json"
            props_path.write_text(json.dumps(props, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            record = {
                "derivative_id": props["derivativeId"], "title": short.title,
                "hook": short.hook, "source_windows": windows,
                "spoken_duration_seconds": spoken_duration,
                "total_duration_seconds": round(spoken_duration + END_CARD_SECONDS, 3),
                "file": str(output.relative_to(ROOT)).replace("\\", "/"),
                "props": str(props_path.relative_to(ROOT)).replace("\\", "/"),
                "qa": {"dimensions": "1080x1920", "video_codec": video_stream["codec_name"], "duration": round(float(validation["format"]["duration"]), 3)},
                "platforms": ["youtube_shorts", "tiktok"],
                "paid_api_cost_usd": 0,
            }
            video_outputs.append(record)
            all_outputs.append(record)
            print(f"DONE video-{video.number} short-{short.number}: {record['qa']}")
        manifest = {
            "schema_version": 1,
            "source_video": f"video-{video.number}",
            "method": "Narracao canonica e imagens aprovadas; recomposicao vertical manual em cover, legendas sincronizadas e render local.",
            "rendered_editorial_derivatives": video_outputs,
            "editorial_derivative_count": 2,
            "physical_mp4_target_count": 2,
            "paid_api_cost_usd": 0,
        }
        (work_root / "manifest-v1.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    summary = {"generated": all_outputs, "count": len(all_outputs), "paid_api_cost_usd": 0}
    (EXPORT_ROOT / "catalogo-video-008-011-v1.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
