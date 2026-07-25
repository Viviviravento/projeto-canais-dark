from __future__ import annotations

import json
import re
import textwrap
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
PERFORMANCE_PATH = ROOT / "Canal Religioso" / "02_roteiros" / "piloto-001-performance-v1.json"
TRANSCRIPT_PATH = (
    ROOT
    / "tools"
    / "OpenMontage"
    / "projects"
    / "a-palavra-que-cuida-piloto-001"
    / "artifacts"
    / "piloto-001-narracao-v1-master_transcript.json"
)
OUTPUT_PATH = Path(__file__).with_name("subtitles-master-v1.srt")


def timestamp(seconds: float) -> str:
    millis = max(0, round(seconds * 1000))
    hours, millis = divmod(millis, 3_600_000)
    minutes, millis = divmod(millis, 60_000)
    secs, millis = divmod(millis, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def main() -> None:
    performance = json.loads(PERFORMANCE_PATH.read_text(encoding="utf-8"))
    source = " ".join(block["text"] for block in performance["blocks"])
    source = re.sub(r"<break\b[^>]*?/>", " ", source)
    source_tokens = re.findall(r"\S+", source)

    transcript = json.loads(TRANSCRIPT_PATH.read_text(encoding="utf-8"))
    timed_words = [word for segment in transcript["segments"] for word in segment["words"]]
    if len(source_tokens) != len(timed_words):
        raise RuntimeError(
            f"Token alignment changed: source={len(source_tokens)}, timed={len(timed_words)}"
        )

    words = [
        {
            "word": source_word,
            "start": float(timed_word["start"]),
            "end": float(timed_word["end"]),
        }
        for source_word, timed_word in zip(source_tokens, timed_words, strict=True)
    ]

    cues: list[list[dict[str, str | float]]] = []
    buffer: list[dict[str, str | float]] = []
    for word in words:
        candidate = " ".join([str(item["word"]) for item in buffer] + [str(word["word"])])
        long_pause = bool(buffer and float(word["start"]) - float(buffer[-1]["end"]) > 0.65)
        if buffer and (len(buffer) >= 7 or len(candidate) > 46 or long_pause):
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
                f"{timestamp(float(cue[0]['start']))} --> {timestamp(float(cue[-1]['end']))}",
                "\n".join(
                    textwrap.wrap(
                        " ".join(str(item["word"]) for item in cue),
                        width=42,
                        break_long_words=False,
                        break_on_hyphens=False,
                    )
                ),
                "",
            ]
        )
    OUTPUT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(
        json.dumps(
            {
                "output": str(OUTPUT_PATH),
                "tokens": len(words),
                "cues": len(cues),
                "first_start": words[0]["start"],
                "last_end": words[-1]["end"],
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
