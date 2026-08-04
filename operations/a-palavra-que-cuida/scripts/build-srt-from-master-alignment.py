from __future__ import annotations

import argparse
import json
import re
import textwrap
from pathlib import Path


MAX_CUE_CHARACTERS = 76
MAX_CUE_SECONDS = 5.2
MAX_WORDS = 12
MAX_LINE_CHARACTERS = 42
MAX_REBALANCED_CHARACTERS = 84
MAX_REBALANCED_SECONDS = 6.2


def timestamp(seconds: float) -> str:
    milliseconds = max(0, round(seconds * 1000))
    hours, milliseconds = divmod(milliseconds, 3_600_000)
    minutes, milliseconds = divmod(milliseconds, 60_000)
    seconds_part, milliseconds = divmod(milliseconds, 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds_part:02d},{milliseconds:03d}"


def timed_words(blocks: list[dict]) -> list[dict]:
    output: list[dict] = []
    for block in blocks:
        text = "".join(block["characters"])
        starts = block["character_start_times_seconds"]
        ends = block["character_end_times_seconds"]
        for match in re.finditer(r"\S+", text):
            output.append(
                {
                    "word": match.group(),
                    "start": float(starts[match.start()]),
                    "end": float(ends[match.end() - 1]),
                }
            )
    return output


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


def rebalance_short_cues(cues: list[list[dict]]) -> list[list[dict]]:
    output: list[list[dict]] = []
    index = 0
    while index < len(cues):
        cue = cues[index]
        text = " ".join(item["word"] for item in cue)
        duration = cue[-1]["end"] - cue[0]["start"]
        orphan = len(cue) <= 2 or duration < 0.9 or len(text) <= 12
        if orphan and output:
            combined = output[-1] + cue
            combined_text = " ".join(item["word"] for item in combined)
            combined_duration = combined[-1]["end"] - combined[0]["start"]
            if len(combined_text) <= MAX_REBALANCED_CHARACTERS and combined_duration <= MAX_REBALANCED_SECONDS:
                output[-1] = combined
                index += 1
                continue
        if orphan and index + 1 < len(cues):
            combined = cue + cues[index + 1]
            combined_text = " ".join(item["word"] for item in combined)
            combined_duration = combined[-1]["end"] - combined[0]["start"]
            if len(combined_text) <= MAX_REBALANCED_CHARACTERS and combined_duration <= MAX_REBALANCED_SECONDS:
                output.append(combined)
                index += 2
                continue
        output.append(cue)
        index += 1
    return output


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
    return "\n".join(
        textwrap.wrap(text, width=MAX_LINE_CHARACTERS, break_long_words=False, break_on_hyphens=False)
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--alignment", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    alignment = json.loads(args.alignment.read_text(encoding="utf-8"))
    words = timed_words(alignment["blocks"])
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
        lines.extend(
            [
                str(index),
                f"{timestamp(cue[0]['start'])} --> {timestamp(cue[-1]['end'])}",
                wrap_cue(" ".join(item["word"] for item in cue)),
                "",
            ]
        )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"output": str(args.output), "words": len(words), "cues": len(cues)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
