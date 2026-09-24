from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
AUDIO_DIR = ROOT / "operations" / "a-palavra-que-cuida" / "05_audio" / "video-011" / "v1"
FFMPEG = ROOT / "tools" / "ffmpeg" / "bin" / "ffmpeg.exe"
FFPROBE = ROOT / "tools" / "ffmpeg" / "bin" / "ffprobe.exe"
PREFIX = "video-011-narracao-v1"
TEMPO = 1.07


def duration(path: Path) -> float:
    result = subprocess.run([str(FFPROBE), "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(path)], check=True, capture_output=True, text=True)
    return float(result.stdout.strip())


def loudness(path: Path) -> dict[str, float]:
    result = subprocess.run([str(FFMPEG), "-hide_banner", "-nostats", "-i", str(path), "-af", "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json", "-f", "null", "NUL"], check=True, capture_output=True, text=True)
    match = re.search(r"\{\s*\"input_i\".*?\}", result.stderr, flags=re.DOTALL)
    if not match:
        raise RuntimeError("Could not parse loudness analysis")
    payload = json.loads(match.group(0))
    return {key: float(payload[key]) for key in ("input_i", "input_tp", "input_lra", "input_thresh", "target_offset")}


def main() -> None:
    report = json.loads((AUDIO_DIR / "resultado-geracao.json").read_text(encoding="utf-8"))
    source = AUDIO_DIR / report["assembled"]["raw_wav"]
    tempo_wav = AUDIO_DIR / f"{PREFIX}-1.07x-raw.wav"
    master_wav = AUDIO_DIR / f"{PREFIX}-1.07x-master.wav"
    review_mp3 = AUDIO_DIR / f"{PREFIX}-1.07x-review.mp3"
    alignment_path = AUDIO_DIR / "master-alignment-1.07x.json"
    audit_path = AUDIO_DIR / "postprocess-1.07x.json"

    subprocess.run([str(FFMPEG), "-y", "-i", str(source), "-af", f"atempo={TEMPO}", "-ac", "1", "-ar", "48000", "-c:a", "pcm_s16le", str(tempo_wav)], check=True, capture_output=True)
    measured = loudness(tempo_wav)
    filter_value = "loudnorm=I=-16:TP=-1.5:LRA=11:" + f"measured_I={measured['input_i']}:measured_LRA={measured['input_lra']}:measured_TP={measured['input_tp']}:measured_thresh={measured['input_thresh']}:offset={measured['target_offset']}:linear=true:print_format=summary"
    subprocess.run([str(FFMPEG), "-y", "-i", str(tempo_wav), "-af", filter_value, "-ac", "1", "-ar", "48000", "-c:a", "pcm_s16le", str(master_wav)], check=True, capture_output=True)
    subprocess.run([str(FFMPEG), "-y", "-i", str(master_wav), "-vn", "-c:a", "libmp3lame", "-b:a", "192k", str(review_mp3)], check=True, capture_output=True)
    normalized = loudness(master_wav)

    offset, blocks = 0.0, []
    for result in report["results"]:
        alignment = json.loads((AUDIO_DIR / f"{result['block_id']}.alignment.json").read_text(encoding="utf-8"))["alignment"]
        starts = alignment.get("character_start_times_seconds") or []
        ends = alignment.get("character_end_times_seconds") or []
        blocks.append({
            "block_id": result["block_id"],
            "start_seconds": round(offset, 6),
            "end_seconds": round(offset + result["duration_seconds"] / TEMPO, 6),
            "characters": alignment.get("characters") or [],
            "character_start_times_seconds": [round(offset + value / TEMPO, 6) for value in starts],
            "character_end_times_seconds": [round(offset + value / TEMPO, 6) for value in ends],
        })
        offset += result["duration_seconds"] / TEMPO

    master_duration = duration(master_wav)
    alignment_path.write_text(json.dumps({
        "version": "video-011-master-alignment-1.07x-v1",
        "tempo": TEMPO,
        "pitch": "preserved",
        "source_generation_report": "resultado-geracao.json",
        "blocks": blocks,
        "expected_duration_seconds": round(offset, 6),
        "master_duration_seconds": round(master_duration, 6),
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    audit_path.write_text(json.dumps({
        "version": "video-011-audio-postprocess-1.07x-v1",
        "source": source.name,
        "tempo": TEMPO,
        "pitch": "preserved",
        "raw_duration_seconds": round(duration(source), 6),
        "master_duration_seconds": round(master_duration, 6),
        "files": {"tempo_wav": tempo_wav.name, "master_wav": master_wav.name, "review_mp3": review_mp3.name, "alignment": alignment_path.name},
        "loudness": {"pre_normalization": measured, "master": normalized, "target_integrated_lufs": -16.0, "target_true_peak_dbfs": -1.5},
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"master": str(review_mp3), "duration_seconds": round(master_duration, 3), "alignment": str(alignment_path)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
