"""V4 master: a fail-closed narration and visual script are rendered together.

This corrective build preserves the approved narration whitelist and the
doorbell framing, but replaces V3's generic neighbor-room background with a
source-specific visual sequence for every narrative block.
"""

from __future__ import annotations

import asyncio
import json
import subprocess
import sys
from pathlib import Path

import edge_tts
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from factory.core.narration_input_firewall import load_public_narration
from factory.core.visual_semantic_sync import validate_narration_visual_script

CASE = ROOT / "output/concept-previews/brasil-registrado/chris-watts-v1"
OUTDIR = CASE / "full-v4"
WORK = OUTDIR / "work-v4"
RAW = CASE / "sources/raw"
FFMPEG = ROOT / "tools/ffmpeg/bin/ffmpeg.exe"
FFPROBE = ROOT / "tools/ffmpeg/bin/ffprobe.exe"
OUT = OUTDIR / "CHRIS-WATTS-EPISODIO-COMPLETO-INTERNO-V4.mp4"
PLAN_PATH = OUTDIR / "visual-script-v4.json"
WHITELIST = CASE / "full-v3/narration-whitelist-full-v3.json"
W, H = 1920, 1080
CREAM = (239, 233, 218, 255)
ORANGE = (202, 92, 47, 255)
PETROL = (5, 29, 30, 225)

# Preserved V9 dialogue: source speech is audible here, and every retained turn
# receives a readable, identity-consistent Portuguese caption. No TTS overlaps.
CUES = [
    (1.94, 4.66, "A câmera mostra este carro começando a descer a rua."),
    (4.62, 5.18, "Aquele ali."),
    (7.10, 7.92, "Entende o que eu quero dizer?"),
    (7.92, 9.44, "Ela alcança até lá embaixo."),
    (9.58, 10.12, "Legal."),
    (10.36, 11.46, "Ele mora ali ao lado."),
    (12.52, 13.08, "Podemos ir?"),
    (14.56, 15.90, "Eu estava falando dessa pressão."),
    (17.44, 18.56, "Vai ficar perto de quatro."),
    (18.66, 20.82, "Sim, ela pega carros vindo por aqui."),
    (20.74, 23.12, "Eu registro o que vem por aqui quando faz a curva."),
    (24.20, 27.54, "À noite, geralmente eu percebo o carro fazendo a curva."),
    (28.18, 29.98, "Então, a menos que ela pare bem aqui,"),
    (29.98, 33.20, "eu teria visto se ela tivesse saído a pé."),
    (39.32, 40.20, "Diesel."),
]

# Inspected in the source before this corrective render. They contain baked
# English editorial cards and therefore can never be silently reused.
BLOCKED_BODYCAM_RANGES = ((0.0, 24.0), (204.0, 216.0))

TEXT_IDS = tuple(
    ["CW-OPENING-001"]
    + [f"CW-BRIDGE-{number:03d}" for number in range(1, 11)]
    + [f"CW-DETAIL-{number:03d}" for number in range(1, 11)]
    + ["CW-EPILOGUE-001", "CW-EPILOGUE-002", "CW-EPILOGUE-003", "CW-OUTRO-001"]
)
NARRATION = load_public_narration(WHITELIST, TEXT_IDS)


def run(arguments: list[object]) -> None:
    subprocess.run([str(value) for value in arguments], check=True)


def duration(path: Path) -> float:
    result = subprocess.run(
        [str(FFPROBE), "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(path)],
        capture_output=True,
        text=True,
        check=True,
    )
    return float(result.stdout.strip())


def wrap(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, width: int) -> list[str]:
    lines: list[str] = []
    current = ""
    for word in text.split():
        candidate = (current + " " + word).strip()
        if draw.textlength(candidate, font=font) <= width:
            current = candidate
        else:
            lines.append(current)
            current = word
    return lines + ([current] if current else [])


def make_caption(index: int, text: str) -> Path:
    path = WORK / f"caption-{index:02d}.png"
    image = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 42)
    lines = wrap(draw, text, font, 1320)
    top = 930 - (38 + 56 * len(lines))
    draw.rounded_rectangle((225, top, 1695, 930), 18, fill=PETROL, outline=(44, 103, 99, 225), width=2)
    draw.rounded_rectangle((225, top, 236, 930), 4, fill=ORANGE)
    for line_number, line in enumerate(lines):
        bounds = draw.textbbox((0, 0), line, font=font)
        draw.text(((W - (bounds[2] - bounds[0])) / 2, top + 20 + line_number * 56), line, font=font, fill=CREAM)
    image.save(path)
    return path


def make_intro() -> Path:
    path = WORK / "intro.png"
    image = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((110, 108, 1310, 402), 22, fill=PETROL, outline=(44, 103, 99, 225), width=2)
    draw.rounded_rectangle((110, 108, 126, 402), 5, fill=ORANGE)
    draw.text((154, 142), "REGISTRO REAL", font=ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 30), fill=CREAM)
    draw.text((154, 183), "A ÚLTIMA\nCHEGADA", font=ImageFont.truetype(r"C:\Windows\Fonts\georgiab.ttf", 67), fill=CREAM, spacing=0)
    draw.text((154, 348), "FREDERICK, COLORADO · 13 DE AGOSTO DE 2018", font=ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 25), fill=CREAM)
    image.save(path)
    return path


async def tts(index: int, text: str) -> Path:
    raw = WORK / f"voice-{index:02d}.mp3"
    processed = WORK / f"voice-{index:02d}.wav"
    await edge_tts.Communicate(text, "pt-BR-AntonioNeural", rate="+0%", pitch="-8Hz").save(str(raw))
    run([
        FFMPEG, "-y", "-i", raw,
        "-af", "atempo=1.11,highpass=f=70,equalizer=f=180:t=q:w=1:g=1.5,equalizer=f=3000:t=q:w=1:g=0.8,acompressor=threshold=-18dB:ratio=2.4:attack=12:release=130:makeup=2,loudnorm=I=-16:TP=-1.5:LRA=7",
        "-ar", "48000", "-ac", "2", processed,
    ])
    return processed


def visual_filter(source_name: str) -> str:
    if source_name == "neighbor":
        base = "crop=534:300:53:60,scale=1920:1080,delogo=x=585:y=805:w=740:h=260"
    else:
        base = "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black"
    return base + ",eq=contrast=1.05:brightness=-0.025:saturation=0.80,vignette=PI/5:eval=frame,fps=30"


def make_visual_clip(source: Path, source_name: str, start: float, seconds: float, name: str, include_audio: bool = False) -> Path:
    path = WORK / f"{name}.mp4"
    command: list[object] = [
        FFMPEG, "-y", "-ss", f"{start:.3f}", "-i", source, "-t", f"{seconds:.3f}",
        "-vf", visual_filter(source_name), "-c:v", "libx264", "-preset", "ultrafast", "-crf", "20", "-pix_fmt", "yuv420p",
    ]
    if include_audio:
        command += ["-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2"]
    else:
        command += ["-an"]
    run(command + [path])
    return path


def make_visual_sequence(block: dict, target: float, plan_sources: dict[str, Path], index: int) -> tuple[Path, list[dict]]:
    """Render only preplanned source cuts; a plan shortfall fails rather than looping a background."""
    clips: list[Path] = []
    actual_units: list[dict] = []
    remaining = target
    planned = block["units"]
    for unit_index, (source_name, start, planned_seconds) in enumerate(planned):
        if remaining <= 0.02:
            break
        take = min(float(planned_seconds), remaining)
        if source_name == "bodycam" and any(
            float(start) < blocked_end and float(start) + take > blocked_start
            for blocked_start, blocked_end in BLOCKED_BODYCAM_RANGES
        ):
            raise RuntimeError(f"{block['id']}: bodycam atravessa card editorial bloqueado")
        clip = make_visual_clip(plan_sources[source_name], source_name, float(start), take, f"v{index:02d}-{unit_index:02d}")
        clips.append(clip)
        actual_units.append({"source": source_name, "source_start_seconds": start, "duration_seconds": round(take, 3)})
        remaining -= take
    if remaining > 1.25:
        raise RuntimeError(f"{block['id']}: roteiro visual curto por {remaining:.2f}s; acrescente uma evidência planejada")
    if remaining > 0.02:
        source_name, start, planned_seconds = planned[-1]
        start = float(start) + float(planned_seconds)
        clip = make_visual_clip(plan_sources[source_name], source_name, start, remaining, f"v{index:02d}-tail")
        clips.append(clip)
        actual_units.append({"source": source_name, "source_start_seconds": round(start, 3), "duration_seconds": round(remaining, 3), "purpose": "respiro máximo de 1,25s após a fala"})
    if len(clips) == 1:
        return clips[0], actual_units
    list_path = WORK / f"visual-{index:02d}.txt"
    list_path.write_text("".join(f"file '{clip.as_posix()}'\n" for clip in clips), encoding="utf-8")
    output = WORK / f"visual-{index:02d}.mp4"
    run([FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", list_path, "-c", "copy", output])
    return output, actual_units


def make_narrated(index: int, block: dict, text: str, plan_sources: dict[str, Path], show_intro: bool) -> tuple[Path, dict]:
    voice = asyncio.run(tts(index, text))
    voice_seconds = duration(voice)
    target = voice_seconds + 1.20
    visual, actual_units = make_visual_sequence(block, target, plan_sources, index)
    output = WORK / f"narrated-{index:02d}.mp4"
    command: list[object] = [FFMPEG, "-y", "-i", visual, "-i", voice]
    if show_intro:
        command += ["-loop", "1", "-framerate", "30", "-t", "6", "-i", make_intro()]
        filter_video = "[0:v][2:v]overlay=0:0:eof_action=pass[v]"
    else:
        filter_video = "[0:v]null[v]"
    # Narrator remains present but not disproportionately louder; no source
    # speech is left under narration because the non-Portuguese material would
    # require turn-by-turn captions.
    filter_audio = "[1:a]volume=0.72,alimiter=limit=0.96,loudnorm=I=-14:TP=-1.0:LRA=11,apad=pad_dur=1.20[a]"
    run(command + [
        "-filter_complex", filter_video + ";" + filter_audio,
        "-map", "[v]", "-map", "[a]", "-t", f"{target:.3f}",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "256k", output,
    ])
    record = {
        "block_id": block["id"], "narrative_focus": block["narrative_focus"], "visual_reason": block["visual_reason"],
        "narration_seconds": round(voice_seconds, 3), "segment_seconds": round(target, 3), "units": actual_units,
        "narration_source": "firewall_whitelist_only", "source_audio": "muted_under_narration",
    }
    return output, record


def make_neighbor_dialogue(block: dict, plan_sources: dict[str, Path]) -> tuple[Path, dict]:
    source_name, start, seconds = block["units"][0]
    base = make_visual_clip(plan_sources[source_name], source_name, float(start), float(seconds), "neighbor-dialogue-base", include_audio=True)
    output = WORK / "neighbor-dialogue.mp4"
    command: list[object] = [FFMPEG, "-y", "-i", base]
    filters = ["[0:v]setpts=PTS-STARTPTS[v0]", "[0:a]volume=1.10,highpass=f=70,acompressor=threshold=-25dB:ratio=1.8:attack=12:release=120:makeup=3,alimiter=limit=0.94,loudnorm=I=-16:TP=-1.2:LRA=10[a]"]
    current = "v0"
    for cue_index, (cue_start, cue_end, cue_text) in enumerate(CUES, 1):
        image = make_caption(cue_index, cue_text)
        command += ["-loop", "1", "-framerate", "30", "-t", f"{cue_end - cue_start:.3f}", "-i", image]
        panel_label, next_label = f"p{cue_index}", f"v{cue_index}"
        filters += [
            f"[{cue_index}:v]format=rgba,setpts=PTS-STARTPTS+{cue_start:.3f}/TB[{panel_label}]",
            f"[{current}][{panel_label}]overlay=0:0:eof_action=pass:repeatlast=0[{next_label}]",
        ]
        current = next_label
    run(command + [
        "-filter_complex", ";".join(filters), "-map", f"[{current}]", "-map", "[a]",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "256k", output,
    ])
    record = {
        "block_id": block["id"], "narrative_focus": block["narrative_focus"], "visual_reason": block["visual_reason"],
        "segment_seconds": float(seconds), "units": [{"source": source_name, "source_start_seconds": start, "duration_seconds": seconds}],
        "narration_source": "none; original dialogue has priority", "source_audio": "audible_with_ptbr_turn_captions", "captioned_turns": len(CUES),
    }
    return output, record


def narration_for(block_id: str) -> str:
    if block_id == "CW-OPENING-001" or block_id == "CW-OUTRO-001" or block_id.startswith("CW-EPILOGUE"):
        return NARRATION[block_id]
    number = block_id.removeprefix("CW-BRIDGE-")
    return NARRATION[block_id] + " " + NARRATION[f"CW-DETAIL-{number}"]


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    validate_narration_visual_script(plan)
    plan_sources = {key: (OUTDIR / value).resolve() for key, value in plan["sources"].items()}
    for key, source in plan_sources.items():
        if not source.is_file():
            raise FileNotFoundError(f"Fonte visual ausente ({key}): {source}")

    parts: list[Path] = []
    timeline: list[dict] = []
    cursor = 0.0
    for index, block in enumerate(plan["blocks"]):
        if block.get("source_dialogue"):
            part, record = make_neighbor_dialogue(block, plan_sources)
        else:
            part, record = make_narrated(index, block, narration_for(block["id"]), plan_sources, block["id"] == "CW-OPENING-001")
        part_duration = duration(part)
        record["episode_start_seconds"] = round(cursor, 3)
        record["episode_end_seconds"] = round(cursor + part_duration, 3)
        cursor += part_duration
        parts.append(part)
        timeline.append(record)

    concat = WORK / "concat.txt"
    concat.write_text("".join(f"file '{part.as_posix()}'\n" for part in parts), encoding="utf-8")
    run([FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", concat, "-c", "copy", "-movflags", "+faststart", OUT])
    final_duration = duration(OUT)
    if final_duration < 600:
        raise RuntimeError(f"Gate de duração falhou: {final_duration:.3f}s")

    visual_timeline = {"schema": "NarrationVisualTimeline.v1", "artifact": OUT.name, "blocks": timeline}
    (OUTDIR / "visual-timeline-v4.json").write_text(json.dumps(visual_timeline, ensure_ascii=False, indent=2), encoding="utf-8")
    report = {
        "artifact": str(OUT.relative_to(ROOT)).replace("\\", "/"), "duration_seconds": round(final_duration, 3),
        "status": "pending_human_review_and_rights_clearance", "checks": {
            "visual_semantic_script_validated": True, "doorbell_positions": ["first", "last"], "intermediate_doorbell_uses": 0,
            "foreign_dialogue_turns_captioned": len(CUES), "narration_over_source_dialogue": False,
            "narration_speed": "1.11x_pitch_preserved", "narration_source": "firewall_whitelist_only",
            "narrator_gain": "0.72 after loudness processing", "source_audio_under_narration": "muted where foreign speech is uncaptioned",
            "narrated_tail_max_seconds": 1.20, "minimum_duration_seconds": 600,
            "publication_clearance": "blocked_pending_human_review_and_rights_clearance"
        },
    }
    (OUTDIR / "qa-full-v4.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()
