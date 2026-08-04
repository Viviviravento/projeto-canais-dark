from __future__ import annotations

import json
import re
import textwrap
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
AUDIO_DIR = ROOT / "operations" / "a-palavra-que-cuida" / "05_audio" / "video-002" / "v2"
RESULT_PATH = AUDIO_DIR / "resultado-geracao.json"
OUTPUT_PATH = Path(__file__).with_name("subtitles-master-v1.srt")

MAX_CUE_CHARACTERS = 76
MAX_CUE_SECONDS = 5.2
MAX_WORDS = 12
MAX_LINE_CHARACTERS = 42
MAX_REBALANCED_CHARACTERS = 84
MAX_REBALANCED_SECONDS = 6.2


def timestamp(seconds: float) -> str:
    millis = max(0, round(seconds * 1000))
    hours, millis = divmod(millis, 3_600_000)
    minutes, millis = divmod(millis, 60_000)
    secs, millis = divmod(millis, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def timed_words(characters: list[str], starts: list[float], ends: list[float], offset: float) -> list[dict]:
    text = "".join(characters)
    words: list[dict] = []
    for match in re.finditer(r"\S+", text):
        first = match.start()
        last = match.end() - 1
        words.append(
            {
                "word": match.group(0),
                "start": offset + float(starts[first]),
                "end": offset + float(ends[last]),
            }
        )
    return words


def should_close(buffer: list[dict], next_word: dict | None) -> bool:
    if not buffer:
        return False
    text = " ".join(item["word"] for item in buffer)
    duration = buffer[-1]["end"] - buffer[0]["start"]
    sentence_end = bool(re.search(r"[.!?][\"')\]]?$", buffer[-1]["word"]))
    long_pause = bool(next_word and next_word["start"] - buffer[-1]["end"] > 0.55)
    return (
        len(text) >= MAX_CUE_CHARACTERS
        or len(buffer) >= MAX_WORDS
        or duration >= MAX_CUE_SECONDS
        or long_pause
        or (sentence_end and duration >= 1.1)
    )


def wrap_cue(text: str) -> str:
    if len(text) <= MAX_LINE_CHARACTERS:
        return text

    words = text.split()
    candidates: list[tuple[int, str, str]] = []
    for split_index in range(1, len(words)):
        first = " ".join(words[:split_index])
        second = " ".join(words[split_index:])
        if len(first) <= MAX_LINE_CHARACTERS and len(second) <= MAX_LINE_CHARACTERS:
            candidates.append((abs(len(first) - len(second)), first, second))
    if candidates:
        _, first, second = min(candidates, key=lambda item: item[0])
        return first + "\n" + second

    lines = textwrap.wrap(
        text,
        width=MAX_LINE_CHARACTERS,
        break_long_words=False,
        break_on_hyphens=False,
    )
    return "\n".join(lines)


def rebalance_short_cues(cues: list[list[dict]]) -> list[list[dict]]:
    balanced: list[list[dict]] = []
    index = 0
    while index < len(cues):
        cue = cues[index]
        text = " ".join(item["word"] for item in cue)
        duration = cue[-1]["end"] - cue[0]["start"]
        is_orphan = len(cue) <= 2 or duration < 0.9 or len(text) <= 12

        if is_orphan and balanced:
            previous = balanced[-1]
            combined = previous + cue
            combined_text = " ".join(item["word"] for item in combined)
            combined_duration = combined[-1]["end"] - combined[0]["start"]
            if (
                len(combined_text) <= MAX_REBALANCED_CHARACTERS
                and combined_duration <= MAX_REBALANCED_SECONDS
            ):
                balanced[-1] = combined
                index += 1
                continue

        if is_orphan and index + 1 < len(cues):
            combined = cue + cues[index + 1]
            combined_text = " ".join(item["word"] for item in combined)
            combined_duration = combined[-1]["end"] - combined[0]["start"]
            if (
                len(combined_text) <= MAX_REBALANCED_CHARACTERS
                and combined_duration <= MAX_REBALANCED_SECONDS
            ):
                balanced.append(combined)
                index += 2
                continue

        balanced.append(cue)
        index += 1
    return balanced


def main() -> None:
    result = json.loads(RESULT_PATH.read_text(encoding="utf-8"))
    words: list[dict] = []
    offset = 0.0

    for block in result["results"]:
        alignment_path = AUDIO_DIR / f"{block['block_id']}.alignment.json"
        payload = json.loads(alignment_path.read_text(encoding="utf-8"))
        alignment = payload["alignment"]
        words.extend(
            timed_words(
                alignment["characters"],
                alignment["character_start_times_seconds"],
                alignment["character_end_times_seconds"],
                offset,
            )
        )
        offset += float(block["duration_seconds"])

    cues: list[list[dict]] = []
    buffer: list[dict] = []
    for index, word in enumerate(words):
        buffer.append(word)
        next_word = words[index + 1] if index + 1 < len(words) else None
        if should_close(buffer, next_word):
            cues.append(buffer)
            buffer = []
    if buffer:
        cues.append(buffer)
    cues = rebalance_short_cues(cues)

    lines: list[str] = []
    for index, cue in enumerate(cues, start=1):
        text = " ".join(item["word"] for item in cue)
        lines.extend(
            [
                str(index),
                f"{timestamp(cue[0]['start'])} --> {timestamp(cue[-1]['end'])}",
                wrap_cue(text),
                "",
            ]
        )

    OUTPUT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(
        json.dumps(
            {
                "output": str(OUTPUT_PATH),
                "words": len(words),
                "cues": len(cues),
                "first_start": words[0]["start"],
                "last_end": words[-1]["end"],
                "assembled_audio_seconds": result["assembled"]["duration_seconds"],
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
