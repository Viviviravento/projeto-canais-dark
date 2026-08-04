from __future__ import annotations

import argparse
import base64
import html
import json
import re
from pathlib import Path
from typing import Any

import requests


ROOT = Path(__file__).resolve().parents[4]
MANIFEST_PATH = (
    ROOT
    / "operations" / "a-palavra-que-cuida"
    / "02_roteiros"
    / "piloto-001-calibracao-audio-v1.json"
)
ENV_PATH = ROOT / "tools" / "OpenMontage" / ".env"
OUTPUT_DIR = (
    ROOT / "operations" / "a-palavra-que-cuida" / "05_audio" / "piloto-001" / "calibracao-v1"
)
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
        return
    if "\ufffd" in value:
        raise RuntimeError(f"{field} contains a Unicode replacement character")
    if re.search(r"\w\?\w", value, flags=re.UNICODE):
        raise RuntimeError(f"{field} contains a question mark replacing a letter")
    if any(not char.isprintable() and char not in "\r\n\t" for char in value):
        raise RuntimeError(f"{field} contains a non-printable character")


def slug(value: str) -> str:
    value = value.lower().replace("voz ", "voz-")
    return re.sub(r"[^a-z0-9-]+", "-", value).strip("-")


def get_subscription(api_key: str) -> dict[str, Any]:
    response = requests.get(
        f"{ELEVENLABS_BASE_URL}/v1/user/subscription",
        headers={"xi-api-key": api_key},
        timeout=60,
    )
    response.raise_for_status()
    payload = response.json()
    return {
        "tier": payload.get("tier"),
        "character_count": payload.get("character_count"),
        "character_limit": payload.get("character_limit"),
    }


def ensure_shared_voice(api_key: str, voice: dict[str, Any]) -> None:
    if voice["source"] != "shared":
        return
    response = requests.post(
        (
            f"{ELEVENLABS_BASE_URL}/v1/voices/add/"
            f"{voice['public_owner_id']}/{voice['voice_id']}"
        ),
        headers={"xi-api-key": api_key, "Content-Type": "application/json"},
        json={"new_name": voice["name"], "bookmarked": True},
        timeout=60,
    )
    if response.status_code in {400, 409, 422}:
        # An already-saved voice can return a validation-style response.
        check = requests.get(
            f"{ELEVENLABS_BASE_URL}/v1/voices/{voice['voice_id']}",
            headers={"xi-api-key": api_key},
            timeout=60,
        )
        check.raise_for_status()
        return
    response.raise_for_status()


def generate_sample(
    api_key: str,
    manifest: dict[str, Any],
    voice: dict[str, Any],
    sample: dict[str, Any],
    force: bool,
) -> dict[str, Any]:
    label_slug = slug(voice["blind_label"])
    output_path = OUTPUT_DIR / f"{sample['id']}__{label_slug}.mp3"
    alignment_path = output_path.with_suffix(".alignment.json")
    if output_path.exists() and alignment_path.exists() and not force:
        saved = json.loads(alignment_path.read_text(encoding="utf-8"))
        return {**saved["generation"], "status": "reused"}

    api = manifest["api"]
    payload: dict[str, Any] = {
        "text": sample["text"],
        "model_id": api["model_id"],
        "language_code": api["language_code"],
        "voice_settings": api["voice_settings"],
        "seed": api["seed"],
    }
    if sample.get("previous_text"):
        payload["previous_text"] = sample["previous_text"]
    if sample.get("next_text"):
        payload["next_text"] = sample["next_text"]

    response = requests.post(
        (
            f"{ELEVENLABS_BASE_URL}/v1/text-to-speech/"
            f"{voice['voice_id']}/with-timestamps"
        ),
        headers={
            "xi-api-key": api_key,
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        params={"output_format": api["output_format"]},
        json=payload,
        timeout=240,
    )
    response.raise_for_status()
    body = response.json()
    output_path.write_bytes(base64.b64decode(body["audio_base64"]))

    alignment = body.get("normalized_alignment") or body.get("alignment") or {}
    duration = 0.0
    ends = alignment.get("character_end_times_seconds") or []
    if ends:
        duration = float(ends[-1])

    generation = {
        "sample_id": sample["id"],
        "blind_label": voice["blind_label"],
        "voice_id": voice["voice_id"],
        "file": output_path.name,
        "characters_sent": len(sample["text"]),
        "character_cost_header": response.headers.get("character-cost"),
        "request_id": response.headers.get("request-id"),
        "duration_seconds": round(duration, 3),
        "status": "generated",
    }
    alignment_path.write_text(
        json.dumps(
            {"generation": generation, "alignment": alignment},
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return generation


def build_audition_page(manifest: dict[str, Any], results: list[dict[str, Any]]) -> None:
    by_key = {(item["sample_id"], item["blind_label"]): item for item in results}
    headers = "".join(
        f"<th>{html.escape(voice['blind_label'])}</th>" for voice in manifest["voices"]
    )
    rows: list[str] = []
    for sample in manifest["samples"]:
        cells: list[str] = []
        for voice in manifest["voices"]:
            result = by_key[(sample["id"], voice["blind_label"])]
            cells.append(
                "<td>"
                f"<audio controls preload='metadata' src='{html.escape(result['file'])}'></audio>"
                f"<small>{result['duration_seconds']:.1f}s</small>"
                "</td>"
            )
        rows.append(
            "<tr>"
            f"<th><strong>{html.escape(sample['id'])}</strong>"
            f"<span>{html.escape(sample['function'])}</span></th>"
            + "".join(cells)
            + "</tr>"
        )

    page = f"""<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(manifest.get('review_title', 'Calibracao de narracao'))}</title>
  <style>
    :root {{ color-scheme: light; font-family: Arial, sans-serif; color: #243129; }}
    body {{ margin: 0; background: #f4f0e7; }}
    main {{ max-width: 1180px; margin: 0 auto; padding: 32px 24px; }}
    h1 {{ font-size: 26px; margin: 0 0 8px; }}
    p {{ color: #5d6a62; margin: 0 0 24px; }}
    table {{ width: 100%; border-collapse: collapse; background: white; }}
    th, td {{ border: 1px solid #d9d5cc; padding: 16px; text-align: left; vertical-align: top; }}
    thead th {{ background: #31483c; color: white; }}
    tbody th {{ width: 280px; }}
    tbody th span, small {{ display: block; margin-top: 8px; color: #6b756f; font-weight: normal; }}
    audio {{ width: min(260px, 100%); }}
    .rule {{ margin-top: 20px; padding: 14px 16px; border-left: 4px solid #b08a3e; background: #fff; }}
  </style>
</head>
<body>
<main>
  <h1>{html.escape(manifest.get('review_title', 'Calibracao de narracao'))}</h1>
  <p>{html.escape(manifest.get('review_instruction', 'Ouça cada bloco por inteiro e avalie se a voz compreende e conduz a mensagem.'))}</p>
  <table>
    <thead><tr><th>Movimento narrativo</th>{headers}</tr></thead>
    <tbody>{''.join(rows)}</tbody>
  </table>
  <div class="rule">{html.escape(manifest.get('review_rule', 'Aprove ou reprove a direcao geral. Nao e necessario marcar frases ou timestamps.'))}</div>
</main>
</body>
</html>
"""
    (OUTPUT_DIR / "avaliacao.html").write_text(page, encoding="utf-8")


def main() -> int:
    global MANIFEST_PATH, OUTPUT_DIR

    parser = argparse.ArgumentParser()
    parser.add_argument("--generate", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--manifest", type=Path, default=MANIFEST_PATH)
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DIR)
    args = parser.parse_args()

    MANIFEST_PATH = args.manifest if args.manifest.is_absolute() else ROOT / args.manifest
    OUTPUT_DIR = args.output_dir if args.output_dir.is_absolute() else ROOT / args.output_dir

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    for sample in manifest["samples"]:
        for field in ("previous_text", "text", "next_text"):
            validate_text(sample.get(field, ""), f"{sample['id']}.{field}")

    unique_chars = sum(len(sample["text"]) for sample in manifest["samples"])
    projection = {
        "samples": len(manifest["samples"]),
        "voices": len(manifest["voices"]),
        "characters_per_voice": unique_chars,
        "characters_total_sent": unique_chars * len(manifest["voices"]),
        "voice_rate_multipliers": {
            voice["blind_label"]: voice["rate"] for voice in manifest["voices"]
        },
    }
    print(json.dumps(projection, ensure_ascii=False))
    if not args.generate:
        print("dry-run")
        return 0

    api_key = load_secret("ELEVENLABS_API_KEY")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    before = get_subscription(api_key)
    for voice in manifest["voices"]:
        ensure_shared_voice(api_key, voice)

    results: list[dict[str, Any]] = []
    for sample in manifest["samples"]:
        for voice in manifest["voices"]:
            results.append(
                generate_sample(api_key, manifest, voice, sample, force=args.force)
            )

    after = get_subscription(api_key)
    report = {
        "experiment": manifest["experiment"],
        "projection": projection,
        "subscription_before": before,
        "subscription_after": after,
        "credits_consumed": (
            after["character_count"] - before["character_count"]
            if isinstance(before.get("character_count"), int)
            and isinstance(after.get("character_count"), int)
            else None
        ),
        "results": results,
        "blind_voice_map": {
            voice["blind_label"]: {
                "name": voice["name"],
                "voice_id": voice["voice_id"],
                "selection_reason": voice["selection_reason"],
            }
            for voice in manifest["voices"]
        },
    }
    (OUTPUT_DIR / "resultado-geracao.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    build_audition_page(manifest, results)
    print(
        json.dumps(
            {
                "generated": len(results),
                "credits_consumed": report["credits_consumed"],
                "audition_page": str(OUTPUT_DIR / "avaliacao.html"),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
