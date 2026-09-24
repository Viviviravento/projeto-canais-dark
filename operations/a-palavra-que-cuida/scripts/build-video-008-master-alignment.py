"""Build the video 008 master alignment, recovering only its missing block locally."""

from __future__ import annotations

import json
import re
import subprocess
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
AUDIO_DIR = ROOT / "operations" / "a-palavra-que-cuida" / "05_audio" / "video-008" / "v1"
SCRIPT_PATH = ROOT / "operations" / "a-palavra-que-cuida" / "02_roteiros" / "video-008-roteiro-v1.md"
LOCAL_TRANSCRIPT = AUDIO_DIR / "local-whisper-small-word-timestamps-v1.json"
FFPROBE = ROOT / "tools" / "ffmpeg" / "bin" / "ffprobe.exe"
TEMPO = 1.07
BLOCK_IDS = [
    "01-quando-a-vergonha-chama-seu-nome",
    "02-jesus-viu-pedro-antes-da-queda",
    "03-o-medo-no-patio",
    "04-o-olhar-o-choro-e-a-verdade",
    "05-jesus-encontra-pedro-junto-ao-mar",
    "06-a-pergunta-que-aponta-para-frente",
    "07-como-comecar-a-recomecar",
    "08-fechamento-e-convite",
]


def duration(path: Path) -> float:
    result = subprocess.run(
        [str(FFPROBE), "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        check=True,
        capture_output=True,
        text=True,
    )
    return float(result.stdout.strip())


def script_blocks() -> dict[str, str]:
    sections = re.split(r"^## \d{2} - .*?$", SCRIPT_PATH.read_text(encoding="utf-8"), flags=re.MULTILINE)
    content = [re.sub(r"\s+", " ", section).strip() for section in sections[1:]]
    if len(content) != len(BLOCK_IDS):
        raise RuntimeError("Expected eight script sections for video 008.")
    return dict(zip(BLOCK_IDS, content, strict=True))


def normalized(token: str) -> str:
    token = unicodedata.normalize("NFD", token.lower())
    token = "".join(character for character in token if unicodedata.category(character) != "Mn")
    return re.sub(r"[^a-z0-9]", "", token)


def fill_missing_word_times(times: list[tuple[float, float] | None], start: float, end: float) -> list[tuple[float, float]]:
    resolved = list(times)
    index = 0
    while index < len(resolved):
        if resolved[index] is not None:
            index += 1
            continue
        gap_start = index
        while index < len(resolved) and resolved[index] is None:
            index += 1
        gap_end = index
        left = resolved[gap_start - 1][1] if gap_start else start
        right = resolved[gap_end][0] if gap_end < len(resolved) else end
        width = (right - left) / (gap_end - gap_start)
        for position in range(gap_start, gap_end):
            relative = position - gap_start
            resolved[position] = (left + width * relative, left + width * (relative + 1))
    return [(round(item[0], 6), round(item[1], 6)) for item in resolved if item is not None]


def alignment_from_local_text(text: str, block_start: float, block_end: float) -> tuple[dict, dict]:
    transcript = json.loads(LOCAL_TRANSCRIPT.read_text(encoding="utf-8"))
    spoken_words = [
        word
        for segment in transcript["segments"]
        for word in segment.get("words", [])
        if float(word["end"]) >= block_start and float(word["start"]) <= block_end
    ]
    script_words = list(re.finditer(r"\S+", text))
    expected = [normalized(match.group()) for match in script_words]
    actual = [normalized(word["word"]) for word in spoken_words]
    timings: list[tuple[float, float] | None] = [None] * len(script_words)
    matcher = SequenceMatcher(a=expected, b=actual, autojunk=False)
    direct_matches = 0
    for match in matcher.get_matching_blocks():
        for relative in range(match.size):
            script_index = match.a + relative
            spoken = spoken_words[match.b + relative]
            timings[script_index] = (float(spoken["start"]), float(spoken["end"]))
            direct_matches += 1
    word_times = fill_missing_word_times(timings, block_start, block_end)

    starts = [block_start] * len(text)
    ends = [block_start] * len(text)
    for word_match, (word_start, word_end) in zip(script_words, word_times, strict=True):
        first, last = word_match.span()
        length = max(last - first, 1)
        for position in range(first, last):
            starts[position] = round(word_start + (word_end - word_start) * (position - first) / length, 6)
            ends[position] = round(word_start + (word_end - word_start) * (position - first + 1) / length, 6)
        if first:
            starts[first - 1] = word_start
            ends[first - 1] = word_start
    previous_end = block_start
    for position in range(len(text)):
        if starts[position] == block_start and ends[position] == block_start and text[position].isspace():
            starts[position] = previous_end
            ends[position] = previous_end
        previous_end = max(previous_end, ends[position])
    alignment = {
        "characters": list(text),
        "character_start_times_seconds": starts,
        "character_end_times_seconds": ends,
    }
    audit = {
        "source": LOCAL_TRANSCRIPT.name,
        "script_words": len(script_words),
        "local_words": len(spoken_words),
        "direct_word_matches": direct_matches,
        "direct_match_ratio": round(direct_matches / len(script_words), 4),
    }
    return alignment, audit


def main() -> None:
    texts = script_blocks()
    offset = 0.0
    blocks = []
    recovery_audit = None
    for block_id in BLOCK_IDS:
        source = AUDIO_DIR / f"{block_id}.mp3"
        block_duration = duration(source) / TEMPO
        block_start = offset
        block_end = offset + block_duration
        alignment_path = AUDIO_DIR / f"{block_id}.alignment.json"
        if alignment_path.exists():
            original = json.loads(alignment_path.read_text(encoding="utf-8"))["alignment"]
            alignment = {
                "characters": original["characters"],
                "character_start_times_seconds": [round(block_start + float(value) / TEMPO, 6) for value in original["character_start_times_seconds"]],
                "character_end_times_seconds": [round(block_start + float(value) / TEMPO, 6) for value in original["character_end_times_seconds"]],
            }
        else:
            alignment, recovery_audit = alignment_from_local_text(texts[block_id], block_start, block_end)
        blocks.append({"block_id": block_id, "start_seconds": round(block_start, 6), "end_seconds": round(block_end, 6), **alignment})
        offset = block_end

    master = AUDIO_DIR / "video-008-narracao-v1-1.07x-master.wav"
    payload = {
        "version": "video-008-master-alignment-1.07x-v1",
        "tempo": TEMPO,
        "pitch": "preserved",
        "alignment_sources": "ElevenLabs native alignment, with local recovery only for block 07",
        "blocks": blocks,
        "expected_duration_seconds": round(offset, 6),
        "master_duration_seconds": round(duration(master), 6),
        "local_recovery_audit": recovery_audit,
    }
    output = AUDIO_DIR / "master-alignment-1.07x.json"
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "duration": payload["master_duration_seconds"], "recovery": recovery_audit}, ensure_ascii=False))


if __name__ == "__main__":
    main()
