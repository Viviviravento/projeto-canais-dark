from __future__ import annotations

import argparse
import base64
import json
import re
import unicodedata
from pathlib import Path

import requests


PROJECT_ROOT = Path(__file__).resolve().parents[4]
OPERATION_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = OPERATION_ROOT / "02_roteiros" / "piloto-001-roteiro-v0.md"
ENV_PATH = PROJECT_ROOT / "tools" / "OpenMontage" / ".env"
AUDIO_DIR = OPERATION_ROOT / "05_audio" / "piloto-001"
EDIT_DIR = OPERATION_ROOT / "06_edicao" / "piloto-001"

VOICE_ID = "iF2QszmZhlyFLleUoFxy"
MODEL_ID = "eleven_multilingual_v2"
VOICE_SETTINGS = {
    "stability": 0.65,
    "similarity_boost": 0.75,
    "style": 0.0,
    "speed": 1.0,
    "use_speaker_boost": True,
}


def ascii_fold(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    return "".join(ch for ch in normalized if not unicodedata.combining(ch))


def extract_narration(markdown: str) -> str:
    lines = markdown.splitlines()
    paragraphs: list[str] = []
    collecting = False
    current: list[str] = []

    def flush() -> None:
        nonlocal current
        text = " ".join(part.strip() for part in current if part.strip()).strip()
        if text:
            paragraphs.append(text)
        current = []

    for line in lines:
        folded = ascii_fold(line.strip()).lower()
        if folded == "**narracao:**":
            collecting = True
            flush()
            continue
        if collecting and line.startswith("### "):
            flush()
            collecting = False
            continue
        if collecting and line.startswith("## "):
            flush()
            collecting = False
            continue
        if not collecting:
            continue
        cleaned = line.strip()
        if cleaned.startswith(">"):
            cleaned = cleaned[1:].strip()
        cleaned = cleaned.rstrip()
        if not cleaned:
            flush()
        else:
            current.append(cleaned)

    flush()
    text = "\n\n".join(paragraphs)
    return make_tts_safe(text)


def make_tts_safe(text: str) -> str:
    replacements = {
        "Mateus 11:28-30, ACF": "Mateus, cap\u00edtulo onze, vers\u00edculos vinte e oito a trinta.",
        "Mateus 11": "Mateus, cap\u00edtulo onze",
        "G\u00e1latas 6:2, lemos": "G\u00e1latas, cap\u00edtulo seis, vers\u00edculo dois, lemos",
        "G\u00e1latas 6:2, ACF": "G\u00e1latas, cap\u00edtulo seis, vers\u00edculo dois.",
        "1 Pedro 5:7, ACF": "Primeira Carta de Pedro, cap\u00edtulo cinco, vers\u00edculo sete.",
    }
    for source, target in replacements.items():
        text = text.replace(source, target)
    text = text.replace('"', "")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return text


def load_secret(name: str) -> str:
    for raw_line in ENV_PATH.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        if key.strip() == name:
            return value.strip().strip('"').strip("'")
    raise RuntimeError(f"Missing {name} in {ENV_PATH}")


def build_words(alignment: dict) -> list[dict]:
    chars = alignment["characters"]
    starts = alignment["character_start_times_seconds"]
    ends = alignment["character_end_times_seconds"]
    words: list[dict] = []
    start_index: int | None = None

    for index, char in enumerate(chars + [" "]):
        if index < len(chars) and not char.isspace() and start_index is None:
            start_index = index
        if (index == len(chars) or char.isspace()) and start_index is not None:
            end_index = index - 1
            word = "".join(chars[start_index:index]).strip()
            if word:
                words.append(
                    {
                        "word": word,
                        "start": float(starts[start_index]),
                        "end": float(ends[end_index]),
                        "startMs": round(float(starts[start_index]) * 1000),
                        "endMs": round(float(ends[end_index]) * 1000),
                    }
                )
            start_index = None
    return words


def srt_timestamp(seconds: float) -> str:
    millis = max(0, round(seconds * 1000))
    hours, millis = divmod(millis, 3_600_000)
    minutes, millis = divmod(millis, 60_000)
    secs, millis = divmod(millis, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def build_srt(words: list[dict], max_words: int = 7, max_chars: int = 46) -> str:
    cues: list[list[dict]] = []
    buffer: list[dict] = []
    for word in words:
        candidate = " ".join([item["word"] for item in buffer] + [word["word"]])
        long_pause = bool(buffer and word["start"] - buffer[-1]["end"] > 0.65)
        if buffer and (len(buffer) >= max_words or len(candidate) > max_chars or long_pause):
            cues.append(buffer)
            buffer = []
        buffer.append(word)
    if buffer:
        cues.append(buffer)

    lines: list[str] = []
    for index, cue in enumerate(cues, start=1):
        lines.extend(
            [
                str(index),
                f"{srt_timestamp(cue[0]['start'])} --> {srt_timestamp(cue[-1]['end'])}",
                " ".join(item["word"] for item in cue),
                "",
            ]
        )
    return "\n".join(lines)


def validate_text(text: str) -> None:
    if not text:
        raise RuntimeError("Narration extraction returned no text")
    if re.search(r"\w\?\w", text, flags=re.UNICODE):
        raise RuntimeError("Narration contains a replacement question mark between letters")
    required = [
        "Vinde a mim, todos os que estais cansados",
        "Levai as cargas uns dos outros",
        "Lan\u00e7ando sobre ele toda a vossa ansiedade",
    ]
    missing = [phrase for phrase in required if phrase not in text]
    if missing:
        raise RuntimeError(f"Required narration phrases missing: {missing}")


def write_dry_run(text: str) -> None:
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    EDIT_DIR.mkdir(parents=True, exist_ok=True)
    (AUDIO_DIR / "narracao-final.txt").write_text(text + "\n", encoding="utf-8")
    metadata = {
        "voice_id": VOICE_ID,
        "voice_name": "Bruno Cardoso",
        "model_id": MODEL_ID,
        "voice_settings": VOICE_SETTINGS,
        "characters": len(text),
        "words": len(text.split()),
        "source_script": str(SCRIPT_PATH),
    }
    (EDIT_DIR / "audio-request.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def generate(text: str) -> None:
    api_key = load_secret("ELEVENLABS_API_KEY")
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/with-timestamps"
    response = requests.post(
        url,
        headers={
            "xi-api-key": api_key,
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        params={"output_format": "mp3_44100_128"},
        json={
            "text": text,
            "model_id": MODEL_ID,
            "voice_settings": VOICE_SETTINGS,
        },
        timeout=240,
    )
    response.raise_for_status()
    payload = response.json()
    alignment = payload.get("normalized_alignment") or payload.get("alignment")
    if not alignment:
        raise RuntimeError("ElevenLabs response did not include alignment")

    audio_bytes = base64.b64decode(payload["audio_base64"])
    (AUDIO_DIR / "narracao-final-bruno.mp3").write_bytes(audio_bytes)

    words = build_words(alignment)
    captions = [
        {"word": item["word"], "startMs": item["startMs"], "endMs": item["endMs"]}
        for item in words
    ]
    (EDIT_DIR / "captions-word.json").write_text(
        json.dumps(captions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (EDIT_DIR / "subtitles.srt").write_text(build_srt(words), encoding="utf-8")

    safe_payload = {
        "voice_id": VOICE_ID,
        "model_id": MODEL_ID,
        "voice_settings": VOICE_SETTINGS,
        "text_length": len(text),
        "word_count": len(words),
        "aligned_duration_seconds": words[-1]["end"] if words else 0,
        "alignment": alignment,
    }
    (EDIT_DIR / "elevenlabs-alignment.json").write_text(
        json.dumps(safe_payload, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--generate", action="store_true")
    args = parser.parse_args()

    markdown = SCRIPT_PATH.read_text(encoding="utf-8")
    text = extract_narration(markdown)
    validate_text(text)
    write_dry_run(text)
    print(json.dumps({"characters": len(text), "words": len(text.split())}))
    if args.generate:
        generate(text)
        print("generated")
    else:
        print("dry-run")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
