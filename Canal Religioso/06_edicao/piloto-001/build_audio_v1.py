from __future__ import annotations

import argparse
import base64
import difflib
import html
import json
import re
import shutil
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Any

import requests


ROOT = Path(__file__).resolve().parents[3]
MANIFEST_PATH = (
    ROOT / "Canal Religioso" / "02_roteiros" / "piloto-001-performance-v1.json"
)
ENV_PATH = ROOT / "tools" / "OpenMontage" / ".env"
OUTPUT_DIR = ROOT / "Canal Religioso" / "05_audio" / "piloto-001" / "v1"
OUTPUT_PREFIX = "piloto-001-narracao-v1"
REVIEW_TITLE = "Piloto 001 - Narracao v1"
FFMPEG = ROOT / "tools" / "ffmpeg" / "bin" / "ffmpeg.exe"
FFPROBE = ROOT / "tools" / "ffmpeg" / "bin" / "ffprobe.exe"
ELEVENLABS_BASE_URL = "https://api.elevenlabs.io"


def load_secret(name: str) -> str:
    for raw_line in ENV_PATH.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        if key.strip() == name:
            return value.strip().strip('"').strip("'")
    raise RuntimeError(f"Missing {name} in {ENV_PATH}")


def validate_text(value: str, field: str) -> None:
    if not value.strip():
        raise RuntimeError(f"{field} is empty")
    if "\ufffd" in value or re.search(r"\w\?\w", value, flags=re.UNICODE):
        raise RuntimeError(f"{field} contains damaged Unicode")
    if any(not char.isprintable() and char not in "\r\n\t" for char in value):
        raise RuntimeError(f"{field} contains a non-printable character")


def spoken_text(value: str) -> str:
    value = re.sub(r"<break\s+time=\"[0-9.]+s\"\s*/>", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def comparison_text(value: str) -> str:
    value = spoken_text(value).casefold()
    return "".join(char for char in value if char.isalnum())


def subscription(api_key: str) -> dict[str, Any]:
    response = requests.get(
        f"{ELEVENLABS_BASE_URL}/v1/user/subscription",
        headers={"xi-api-key": api_key},
        timeout=60,
    )
    response.raise_for_status()
    body = response.json()
    return {
        "tier": body.get("tier"),
        "character_count": body.get("character_count"),
        "character_limit": body.get("character_limit"),
    }


def wait_for_subscription_update(
    api_key: str, before: dict[str, Any], generation_performed: bool
) -> dict[str, Any]:
    after = subscription(api_key)
    if not generation_performed:
        return after
    before_count = before.get("character_count")
    if not isinstance(before_count, int):
        return after
    deadline = time.monotonic() + 30
    while after.get("character_count") == before_count and time.monotonic() < deadline:
        time.sleep(2)
        after = subscription(api_key)
    return after


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


def loudness_analysis(path: Path) -> dict[str, float]:
    result = subprocess.run(
        [
            str(FFMPEG),
            "-hide_banner",
            "-nostats",
            "-i",
            str(path),
            "-af",
            "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json",
            "-f",
            "null",
            "NUL",
        ],
        capture_output=True,
        text=True,
    )
    match = re.search(r"\{\s*\"input_i\".*?\}", result.stderr, flags=re.DOTALL)
    if not match:
        raise RuntimeError("Could not parse loudnorm analysis")
    payload = json.loads(match.group(0))
    numeric_keys = {
        "input_i",
        "input_tp",
        "input_lra",
        "input_thresh",
        "output_i",
        "output_tp",
        "output_lra",
        "output_thresh",
        "target_offset",
    }
    return {key: float(value) for key, value in payload.items() if key in numeric_keys}


def generate_block(
    api_key: str,
    manifest: dict[str, Any],
    block: dict[str, Any],
    next_block: dict[str, Any] | None,
    previous_request_ids: list[str],
    previous_text: str | None = None,
) -> dict[str, Any]:
    api = manifest["api"]
    payload: dict[str, Any] = {
        "text": block["text"],
        "model_id": api["model_id"],
        "language_code": api["language_code"],
        "voice_settings": api["voice_settings"],
        "seed": api["seed"],
    }
    if previous_request_ids:
        payload["previous_request_ids"] = previous_request_ids[-3:]
        context_mode = "request_stitching"
    elif previous_text:
        payload["previous_text"] = previous_text
        context_mode = "previous_text_fallback"
    else:
        context_mode = "next_text_only"
    if next_block:
        payload["next_text"] = spoken_text(next_block["text"])

    response = requests.post(
        (
            f"{ELEVENLABS_BASE_URL}/v1/text-to-speech/"
            f"{api['voice_id']}/with-timestamps"
        ),
        headers={
            "xi-api-key": api_key,
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        params={"output_format": api["output_format"]},
        json=payload,
        timeout=300,
    )
    response.raise_for_status()
    body = response.json()
    alignment = body.get("normalized_alignment") or body.get("alignment") or {}
    aligned_text = "".join(alignment.get("characters") or [])
    integrity = difflib.SequenceMatcher(
        None, comparison_text(block["text"]), comparison_text(aligned_text)
    ).ratio()
    if integrity < 0.995:
        raise RuntimeError(
            f"Text integrity below threshold for {block['id']}: {integrity:.5f}"
        )

    audio_path = OUTPUT_DIR / f"{block['id']}.mp3"
    audio_path.write_bytes(base64.b64decode(body["audio_base64"]))
    request_id = response.headers.get("request-id")
    if not request_id:
        raise RuntimeError(f"Missing request-id for {block['id']}")

    result = {
        "block_id": block["id"],
        "function": block["function"],
        "file": audio_path.name,
        "characters_sent": len(block["text"]),
        "spoken_characters": len(spoken_text(block["text"])),
        "character_cost": int(response.headers.get("character-cost", "0")),
        "request_id": request_id,
        "integrity_ratio": round(integrity, 6),
        "duration_seconds": round(duration(audio_path), 3),
        "context_mode": context_mode,
    }
    (OUTPUT_DIR / f"{block['id']}.alignment.json").write_text(
        json.dumps(
            {"generation": result, "alignment": alignment},
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return result


def assemble(blocks: list[dict[str, Any]]) -> dict[str, Any]:
    concat_path = OUTPUT_DIR / "concat.txt"
    concat_path.write_text(
        "".join(
            f"file '{(OUTPUT_DIR / block['file']).as_posix()}'\n" for block in blocks
        ),
        encoding="utf-8",
    )
    raw_wav = OUTPUT_DIR / f"{OUTPUT_PREFIX}-raw.wav"
    master_wav = OUTPUT_DIR / f"{OUTPUT_PREFIX}-master.wav"
    review_mp3 = OUTPUT_DIR / f"{OUTPUT_PREFIX}-review.mp3"
    common = ["-f", "concat", "-safe", "0", "-i", str(concat_path)]
    subprocess.run(
        [
            str(FFMPEG),
            "-y",
            *common,
            "-vn",
            "-ac",
            "1",
            "-ar",
            "48000",
            "-c:a",
            "pcm_s16le",
            str(raw_wav),
        ],
        check=True,
        capture_output=True,
    )
    measured = loudness_analysis(raw_wav)
    normalization_filter = (
        "loudnorm=I=-16:TP=-1.5:LRA=11:"
        f"measured_I={measured['input_i']}:"
        f"measured_LRA={measured['input_lra']}:"
        f"measured_TP={measured['input_tp']}:"
        f"measured_thresh={measured['input_thresh']}:"
        f"offset={measured['target_offset']}:linear=true:print_format=summary"
    )
    subprocess.run(
        [
            str(FFMPEG),
            "-y",
            "-i",
            str(raw_wav),
            "-af",
            normalization_filter,
            "-ac",
            "1",
            "-ar",
            "48000",
            "-c:a",
            "pcm_s16le",
            str(master_wav),
        ],
        check=True,
        capture_output=True,
    )
    subprocess.run(
        [
            str(FFMPEG),
            "-y",
            "-i",
            str(master_wav),
            "-vn",
            "-c:a",
            "libmp3lame",
            "-b:a",
            "192k",
            str(review_mp3),
        ],
        check=True,
        capture_output=True,
    )
    normalized = loudness_analysis(master_wav)
    return {
        "raw_wav": raw_wav.name,
        "master_wav": master_wav.name,
        "review_mp3": review_mp3.name,
        "duration_seconds": round(duration(review_mp3), 3),
        "loudness": {
            "raw_integrated_lufs": measured["input_i"],
            "raw_true_peak_dbfs": measured["input_tp"],
            "master_integrated_lufs": normalized["input_i"],
            "master_true_peak_dbfs": normalized["input_tp"],
            "target_integrated_lufs": -16.0,
            "target_true_peak_dbfs": -1.5,
        },
    }


def build_review_page(manifest: dict[str, Any], results: list[dict[str, Any]]) -> None:
    rows = []
    for result in results:
        rows.append(
            "<section>"
            f"<h2>{html.escape(result['block_id'])}</h2>"
            f"<p>{html.escape(result['function'])}</p>"
            f"<audio controls preload='metadata' src='{html.escape(result['file'])}'></audio>"
            f"<small>{result['duration_seconds']:.1f}s</small>"
            "</section>"
        )
    page = f"""<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(REVIEW_TITLE)}</title>
  <style>
    body {{ margin: 0; background: #f4f0e7; color: #243129; font-family: Arial, sans-serif; }}
    main {{ max-width: 900px; margin: auto; padding: 32px 24px; }}
    .full, section {{ background: white; border: 1px solid #d9d5cc; padding: 18px; margin: 14px 0; }}
    h1 {{ margin: 0 0 8px; }} h2 {{ font-size: 17px; margin: 0 0 6px; }}
    p, small {{ color: #66736b; }} audio {{ display: block; width: 100%; margin: 10px 0; }}
    .rule {{ border-left: 4px solid #b08a3e; padding: 14px; background: white; margin-top: 20px; }}
  </style>
</head>
<body><main>
  <h1>{html.escape(REVIEW_TITLE)}</h1>
  <p>Voz A aprovada, grandes blocos semanticos e continuidade por Request Stitching.</p>
  <div class="full"><strong>Audio completo</strong><audio controls preload="metadata" src="{html.escape(OUTPUT_PREFIX)}-review.mp3"></audio></div>
  {''.join(rows)}
  <div class="rule">Crivo esperado: <strong>audio aprovado</strong>, <strong>bloco reprovado</strong> ou <strong>metodo reprovado</strong>. Nao e necessario marcar frases ou timestamps.</div>
</main></body></html>"""
    (OUTPUT_DIR / "avaliacao.html").write_text(page, encoding="utf-8")


def main() -> int:
    global MANIFEST_PATH, OUTPUT_DIR, OUTPUT_PREFIX, REVIEW_TITLE

    parser = argparse.ArgumentParser()
    parser.add_argument("--generate", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--regenerate-block")
    parser.add_argument("--manifest", type=Path, default=MANIFEST_PATH)
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DIR)
    parser.add_argument("--output-prefix", default=OUTPUT_PREFIX)
    parser.add_argument("--review-title", default=REVIEW_TITLE)
    args = parser.parse_args()

    MANIFEST_PATH = (
        args.manifest if args.manifest.is_absolute() else ROOT / args.manifest
    )
    OUTPUT_DIR = (
        args.output_dir if args.output_dir.is_absolute() else ROOT / args.output_dir
    )
    OUTPUT_PREFIX = args.output_prefix
    REVIEW_TITLE = args.review_title

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    blocks = manifest["blocks"]
    block_ids = [block["id"] for block in blocks]
    if args.regenerate_block and args.regenerate_block not in block_ids:
        raise RuntimeError(
            f"Unknown block {args.regenerate_block}; choose one of {block_ids}"
        )
    for block in blocks:
        validate_text(block["text"], block["id"])
    projection = {
        "blocks": len(blocks),
        "characters_sent": sum(len(block["text"]) for block in blocks),
        "spoken_characters": sum(len(spoken_text(block["text"])) for block in blocks),
        "voice": manifest["api"]["voice_name"],
        "model": manifest["api"]["model_id"],
    }
    print(json.dumps(projection, ensure_ascii=False))
    if not args.generate:
        print("dry-run")
        return 0

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    existing = [OUTPUT_DIR / f"{block['id']}.mp3" for block in blocks]
    previous_report_path = OUTPUT_DIR / "resultado-geracao.json"
    previous_report = (
        json.loads(previous_report_path.read_text(encoding="utf-8"))
        if previous_report_path.exists()
        else {}
    )
    if args.regenerate_block and not all(path.exists() for path in existing):
        raise RuntimeError(
            "Block regeneration requires an existing complete generation."
        )
    if any(path.exists() for path in existing) and not all(path.exists() for path in existing):
        if not args.force:
            raise RuntimeError(
                "Partial generation found. Use --force to regenerate the full stitched sequence."
            )

    api_key = load_secret("ELEVENLABS_API_KEY")
    before = subscription(api_key)
    results: list[dict[str, Any]] = []
    reused_generation = (
        all(path.exists() for path in existing)
        and not args.force
        and not args.regenerate_block
    )
    revision_record: dict[str, Any] | None = None
    if args.regenerate_block:
        saved_results = {
            item["block_id"]: item for item in previous_report.get("results", [])
        }
        if set(saved_results) != set(block_ids):
            raise RuntimeError("Previous report does not contain every generated block")
        revision_number = len(previous_report.get("revisions", [])) + 1
        revision_id = f"revision-{revision_number:03d}"
        legacy_dir = OUTPUT_DIR / "legacy" / revision_id
        legacy_dir.mkdir(parents=True, exist_ok=False)
        old_audio = OUTPUT_DIR / f"{args.regenerate_block}.mp3"
        old_alignment = OUTPUT_DIR / f"{args.regenerate_block}.alignment.json"
        shutil.copy2(old_audio, legacy_dir / old_audio.name)
        shutil.copy2(old_alignment, legacy_dir / old_alignment.name)

        target_index = block_ids.index(args.regenerate_block)
        target_block = blocks[target_index]
        previous_text = (
            spoken_text(blocks[target_index - 1]["text"])
            if target_index > 0
            else None
        )
        next_block = blocks[target_index + 1] if target_index + 1 < len(blocks) else None
        replacement = generate_block(
            api_key,
            manifest,
            target_block,
            next_block,
            [],
            previous_text=previous_text,
        )
        for block in blocks:
            results.append(
                replacement
                if block["id"] == args.regenerate_block
                else saved_results[block["id"]]
            )
        revision_record = {
            "revision_id": revision_id,
            "created_at": datetime.now().astimezone().isoformat(),
            "block_id": args.regenerate_block,
            "context_mode": replacement["context_mode"],
            "legacy_dir": str(legacy_dir.relative_to(ROOT)),
            "reason": "User-approved CTA template applied to the full closing block.",
        }
    elif reused_generation:
        for block in blocks:
            saved = json.loads(
                (OUTPUT_DIR / f"{block['id']}.alignment.json").read_text(encoding="utf-8")
            )
            results.append(saved["generation"])
    else:
        request_ids: list[str] = []
        for index, block in enumerate(blocks):
            next_block = blocks[index + 1] if index + 1 < len(blocks) else None
            result = generate_block(
                api_key, manifest, block, next_block, request_ids
            )
            request_ids.append(result["request_id"])
            results.append(result)

    assembled = assemble(results)
    generation_performed = bool(args.force or args.regenerate_block or not reused_generation)
    after = wait_for_subscription_update(api_key, before, generation_performed)
    credits_consumed = (
        after["character_count"] - before["character_count"]
        if isinstance(before.get("character_count"), int)
        and isinstance(after.get("character_count"), int)
        else None
    )
    generation_credits = credits_consumed
    if (reused_generation or args.regenerate_block) and previous_report:
        generation_credits = previous_report.get(
            "credits_consumed_generation",
            previous_report.get("credits_consumed_this_run"),
        )
    previous_total_credits = previous_report.get(
        "credits_consumed_total_audio_v1", generation_credits or 0
    )
    total_audio_credits = previous_total_credits
    if args.regenerate_block and isinstance(credits_consumed, int):
        total_audio_credits += credits_consumed
    revisions = list(previous_report.get("revisions", []))
    if revision_record:
        revision_record["credits_consumed"] = credits_consumed
        revision_record["character_cost_header"] = next(
            item["character_cost"]
            for item in results
            if item["block_id"] == args.regenerate_block
        )
        revisions.append(revision_record)
    current_character_cost = sum(item["character_cost"] for item in results)
    previous_character_cost_history = previous_report.get(
        "character_cost_total_history", previous_report.get("character_cost_sum", 0)
    )
    character_cost_total_history = previous_character_cost_history
    if args.regenerate_block:
        character_cost_total_history += revision_record["character_cost_header"]
    elif args.force or not previous_report:
        character_cost_total_history += current_character_cost
    report = {
        "version": manifest["version"],
        "projection": projection,
        "subscription_before": before,
        "subscription_after": after,
        "credits_consumed_this_run": credits_consumed,
        "credits_consumed_generation": generation_credits,
        "credits_consumed_total_audio_v1": total_audio_credits,
        "character_cost_sum": current_character_cost,
        "character_cost_current_version_sum": current_character_cost,
        "character_cost_total_history": character_cost_total_history,
        "request_stitching": True,
        "revisions": revisions,
        "results": results,
        "assembled": assembled,
    }
    (OUTPUT_DIR / "resultado-geracao.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    build_review_page(manifest, results)
    print(
        json.dumps(
            {
                "credits_consumed": credits_consumed,
                "credits_consumed_generation": generation_credits,
                "credits_consumed_total_audio_v1": total_audio_credits,
                "character_cost_sum": report["character_cost_sum"],
                "duration_seconds": assembled["duration_seconds"],
                "review_page": str(OUTPUT_DIR / "avaliacao.html"),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
