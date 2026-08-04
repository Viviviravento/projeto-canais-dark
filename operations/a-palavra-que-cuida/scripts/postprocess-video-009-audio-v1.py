"""Create the 1.07x pitch-preserved master and aligned timeline for video 009."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
AUDIO = ROOT / "operations" / "a-palavra-que-cuida" / "05_audio" / "video-009" / "v1"
FFMPEG = ROOT / "tools" / "ffmpeg" / "bin" / "ffmpeg.exe"
FFPROBE = ROOT / "tools" / "ffmpeg" / "bin" / "ffprobe.exe"
PREFIX = "video-009-narracao-v1"
TEMPO = 1.07


def duration(path: Path) -> float:
    result = subprocess.run([str(FFPROBE), "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(path)], check=True, capture_output=True, text=True)
    return float(result.stdout.strip())


def loudness(path: Path) -> dict[str, float]:
    result = subprocess.run([str(FFMPEG), "-hide_banner", "-nostats", "-i", str(path), "-af", "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json", "-f", "null", "NUL"], check=True, capture_output=True, text=True)
    match = re.search(r"\{\s*\"input_i\".*?\}", result.stderr, flags=re.DOTALL)
    if not match:
        raise RuntimeError("Could not read loudness analysis")
    payload = json.loads(match.group(0))
    return {key: float(payload[key]) for key in ("input_i", "input_tp", "input_lra", "input_thresh", "target_offset")}


def main() -> None:
    report = json.loads((AUDIO / "resultado-geracao.json").read_text(encoding="utf-8"))
    raw = AUDIO / report["assembled"]["raw_wav"]
    tempo = AUDIO / f"{PREFIX}-1.07x-raw.wav"
    master = AUDIO / f"{PREFIX}-1.07x-master.wav"
    review = AUDIO / f"{PREFIX}-1.07x-review.mp3"
    subprocess.run([str(FFMPEG), "-y", "-i", str(raw), "-af", f"atempo={TEMPO}", "-ac", "1", "-ar", "48000", "-c:a", "pcm_s16le", str(tempo)], check=True, capture_output=True)
    measured = loudness(tempo)
    filter_value = "loudnorm=I=-16:TP=-1.5:LRA=11:" + f"measured_I={measured['input_i']}:measured_LRA={measured['input_lra']}:measured_TP={measured['input_tp']}:measured_thresh={measured['input_thresh']}:offset={measured['target_offset']}:linear=true:print_format=summary"
    subprocess.run([str(FFMPEG), "-y", "-i", str(tempo), "-af", filter_value, "-ac", "1", "-ar", "48000", "-c:a", "pcm_s16le", str(master)], check=True, capture_output=True)
    subprocess.run([str(FFMPEG), "-y", "-i", str(master), "-vn", "-c:a", "libmp3lame", "-b:a", "192k", str(review)], check=True, capture_output=True)
    offset, blocks = 0.0, []
    for result in report["results"]:
        alignment = json.loads((AUDIO / f"{result['block_id']}.alignment.json").read_text(encoding="utf-8"))["alignment"]
        starts = alignment.get("character_start_times_seconds") or []
        ends = alignment.get("character_end_times_seconds") or []
        duration_seconds = float(result["duration_seconds"]) / TEMPO
        blocks.append({"block_id": result["block_id"], "start_seconds": round(offset, 6), "end_seconds": round(offset + duration_seconds, 6), "characters": alignment.get("characters") or [], "character_start_times_seconds": [round(offset + value / TEMPO, 6) for value in starts], "character_end_times_seconds": [round(offset + value / TEMPO, 6) for value in ends]})
        offset += duration_seconds
    payload = {"version": "video-009-master-alignment-1.07x-v1", "tempo": TEMPO, "pitch": "preserved", "source_generation_report": "resultado-geracao.json", "blocks": blocks, "expected_duration_seconds": round(offset, 6), "master_duration_seconds": round(duration(master), 6)}
    alignment_path = AUDIO / "master-alignment-1.07x.json"
    alignment_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    audit = {"version": "video-009-audio-postprocess-1.07x-v1", "source": raw.name, "tempo": TEMPO, "pitch": "preserved", "raw_duration_seconds": round(duration(raw), 6), "master_duration_seconds": round(duration(master), 6), "files": {"tempo_wav": tempo.name, "master_wav": master.name, "review_mp3": review.name, "alignment": alignment_path.name}, "loudness": {"pre_normalization": measured, "master": loudness(master), "target_integrated_lufs": -16.0, "target_true_peak_dbfs": -1.5}}
    (AUDIO / "postprocess-1.07x.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"review": str(review), "duration_seconds": payload["master_duration_seconds"], "alignment": str(alignment_path)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
