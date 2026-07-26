from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
OPERATION_ROOT = Path(__file__).resolve().parents[1]
AUDIO_DIR = OPERATION_ROOT / "05_audio" / "video-003" / "v2"
FFMPEG = PROJECT_ROOT / "tools" / "ffmpeg" / "bin" / "ffmpeg.exe"
FFPROBE = PROJECT_ROOT / "tools" / "ffmpeg" / "bin" / "ffprobe.exe"
TAIL_SECONDS = 3.0


def duration(path: Path) -> float:
    result = subprocess.run(
        [
            str(FFPROBE),
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return float(result.stdout.strip())


def main() -> None:
    report_path = AUDIO_DIR / "resultado-geracao.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))
    source = AUDIO_DIR / report["assembled"]["master_wav"]
    production = AUDIO_DIR / "video-003-narracao-v2-production.wav"
    review = AUDIO_DIR / "video-003-narracao-v2-production-review.mp3"

    subprocess.run(
        [
            str(FFMPEG),
            "-y",
            "-i",
            str(source),
            "-af",
            f"apad=pad_dur={TAIL_SECONDS}",
            "-ac",
            "1",
            "-ar",
            "48000",
            "-c:a",
            "pcm_s16le",
            str(production),
        ],
        check=True,
        capture_output=True,
    )
    subprocess.run(
        [
            str(FFMPEG),
            "-y",
            "-i",
            str(production),
            "-vn",
            "-c:a",
            "libmp3lame",
            "-b:a",
            "192k",
            str(review),
        ],
        check=True,
        capture_output=True,
    )

    merged = {
        "characters": [],
        "character_start_times_seconds": [],
        "character_end_times_seconds": [],
    }
    blocks = []
    offset = 0.0
    for result in report["results"]:
        alignment_path = AUDIO_DIR / f"{result['block_id']}.alignment.json"
        alignment = json.loads(
            alignment_path.read_text(encoding="utf-8")
        )["alignment"]
        starts = [
            round(offset + float(value), 6)
            for value in alignment["character_start_times_seconds"]
        ]
        ends = [
            round(offset + float(value), 6)
            for value in alignment["character_end_times_seconds"]
        ]
        merged["characters"].extend(alignment["characters"])
        merged["character_start_times_seconds"].extend(starts)
        merged["character_end_times_seconds"].extend(ends)
        blocks.append(
            {
                "block_id": result["block_id"],
                "start_seconds": round(offset, 3),
                "speech_end_seconds": round(ends[-1], 3),
                "file_end_seconds": round(
                    offset + float(result["duration_seconds"]), 3
                ),
            }
        )
        offset += float(result["duration_seconds"])

    merged_payload = {
        "schema_version": "1.0.0",
        "source": "ElevenLabs normalized per-block alignment merged by generated block durations",
        "audio": production.name,
        "tail_silence_seconds": TAIL_SECONDS,
        "blocks": blocks,
        "alignment": merged,
    }
    merged_path = AUDIO_DIR / "merged-alignment-v2.json"
    merged_path.write_text(
        json.dumps(merged_payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    production_duration = duration(production)
    report["production"] = {
        "master_wav": production.name,
        "review_mp3": review.name,
        "duration_seconds": round(production_duration, 3),
        "tail_silence_seconds": TAIL_SECONDS,
        "merged_alignment": merged_path.name,
    }
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    integrity = [float(item["integrity_ratio"]) for item in report["results"]]
    qa = {
        "schema_version": "1.0.0",
        "video_id": "video-003",
        "audio_version": "v2",
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "automated_state": "passed",
        "semantic_review": "pending_human_on_completed_master",
        "checks": {
            "duration_10_to_12_minutes": 600 <= production_duration <= 720,
            "text_integrity_all_at_least_0_995": min(integrity) >= 0.995,
            "all_eight_blocks_present": len(report["results"]) == 8,
            "request_stitching_after_first_block": all(
                item["context_mode"] == "request_stitching"
                for item in report["results"][1:]
            ),
            "master_loudness_near_minus_16_lufs": (
                -16.5
                <= float(report["assembled"]["loudness"][
                    "master_integrated_lufs"
                ])
                <= -15.5
            ),
            "true_peak_at_or_below_minus_1_dbfs": float(
                report["assembled"]["loudness"]["master_true_peak_dbfs"]
            )
            <= -1.0,
            "tail_silence_at_least_2_seconds": TAIL_SECONDS >= 2.0,
            "no_paid_retry": not report.get("revisions"),
        },
        "human_review_questions": [
            "As pausas acompanham conclusão, continuidade e mudança de ideia?",
            "As sete referências bíblicas estão compreensíveis e completas?",
            "A leitura das citações soa reverente sem ficar teatral?",
            "O CTA final conclui naturalmente e deixa espaço antes do fim?",
        ],
    }
    if not all(qa["checks"].values()):
        qa["automated_state"] = "failed"
    (AUDIO_DIR / "audio-qa-v2.json").write_text(
        json.dumps(qa, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    review_page = AUDIO_DIR / "avaliacao.html"
    page = review_page.read_text(encoding="utf-8")
    page = page.replace(
        "video-003-narracao-v2-review.mp3", review.name
    )
    review_page.write_text(page, encoding="utf-8")
    print(
        json.dumps(
            {
                "production": str(production),
                "review": str(review),
                "duration_seconds": round(production_duration, 3),
                "qa": qa["automated_state"],
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
