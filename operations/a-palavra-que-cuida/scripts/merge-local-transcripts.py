"""Merge fixed-size local transcription chunks into one timestamped transcript."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--chunk-seconds", required=True, type=float)
    parser.add_argument("--duration-seconds", required=True, type=float)
    args = parser.parse_args()

    transcripts = sorted(args.input_dir.glob("chunk-*_transcript.json"))
    if not transcripts:
        raise SystemExit("No chunk transcripts were found.")

    all_segments: list[dict] = []
    all_words: list[dict] = []
    for transcript_path in transcripts:
        match = re.search(r"chunk-(\d+)", transcript_path.name)
        if not match:
            raise SystemExit(f"Could not read chunk index: {transcript_path.name}")

        offset = int(match.group(1)) * args.chunk_seconds
        transcript = json.loads(transcript_path.read_text(encoding="utf-8"))
        for segment in transcript["segments"]:
            merged_segment = dict(segment)
            merged_segment["start"] = round(segment["start"] + offset, 3)
            merged_segment["end"] = round(segment["end"] + offset, 3)
            merged_words = []
            for word in segment.get("words", []):
                merged_word = dict(word)
                merged_word["start"] = round(word["start"] + offset, 3)
                merged_word["end"] = round(word["end"] + offset, 3)
                merged_words.append(merged_word)
                all_words.append(merged_word)
            merged_segment["words"] = merged_words
            all_segments.append(merged_segment)

    payload = {
        "schema_version": "1.0.0",
        "generator": "local faster-whisper base segmented transcription",
        "language": "pt",
        "duration_seconds": args.duration_seconds,
        "segments": all_segments,
        "word_timestamps": all_words,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"segments={len(all_segments)}")
    print(f"words={len(all_words)}")
    print(f"output={args.output}")


if __name__ == "__main__":
    main()
