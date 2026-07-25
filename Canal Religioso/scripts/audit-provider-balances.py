from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests


ROOT = Path(__file__).resolve().parents[2]
OPENMONTAGE = ROOT / "tools" / "OpenMontage"
OUTPUT = (
    ROOT
    / "Canal Religioso"
    / "06_edicao"
    / "custos"
    / "provider-balances-2026-07-23.json"
)

SAFE_ACCOUNT_TERMS = (
    "amount",
    "balance",
    "billing",
    "character",
    "credit",
    "currency",
    "discount",
    "duration",
    "engine",
    "invoice",
    "limit",
    "overage",
    "payment",
    "period",
    "plan",
    "quota",
    "remaining",
    "reset",
    "status",
    "subtotal",
    "tax",
    "tier",
    "title",
    "type",
    "usage",
    "video_id",
)


def load_env(path: Path) -> None:
    for raw_line in path.read_text(encoding="utf-8-sig").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip("\"").strip("'"))


def safe_fields(value: Any) -> Any:
    if isinstance(value, dict):
        result = {}
        for key, item in value.items():
            lowered = key.lower()
            if any(term in lowered for term in SAFE_ACCOUNT_TERMS):
                result[key] = safe_fields(item)
            elif isinstance(item, (dict, list)):
                nested = safe_fields(item)
                if nested not in ({}, []):
                    result[key] = nested
        return result
    if isinstance(value, list):
        return [safe_fields(item) for item in value]
    return value


def get_json(
    provider: str,
    url: str,
    headers: dict[str, str],
    params: dict[str, str] | None = None,
) -> dict[str, Any]:
    try:
        response = requests.get(url, headers=headers, params=params, timeout=60)
        payload = response.json() if response.content else {}
        if response.ok:
            return {
                "provider": provider,
                "endpoint": url,
                "http_status": response.status_code,
                "ok": True,
                "data": safe_fields(payload),
            }
        return {
            "provider": provider,
            "endpoint": url,
            "http_status": response.status_code,
            "ok": False,
            "error": safe_fields(payload),
        }
    except Exception as exc:
        return {
            "provider": provider,
            "endpoint": url,
            "http_status": None,
            "ok": False,
            "error": f"{type(exc).__name__}: {exc}",
        }


def main() -> None:
    load_env(OPENMONTAGE / ".env")
    eleven_key = os.environ["ELEVENLABS_API_KEY"]
    heygen_key = os.environ["HEYGEN_API_KEY"]
    fal_key = os.environ["FAL_KEY"]

    checks = [
        get_json(
            "ElevenLabs",
            "https://api.elevenlabs.io/v1/user/subscription",
            {"xi-api-key": eleven_key},
        ),
        get_json(
            "HeyGen",
            "https://api.heygen.com/v2/user/remaining_quota",
            {"x-api-key": heygen_key},
        ),
        get_json(
            "HeyGen",
            "https://api.heygen.com/v3/users/me",
            {"x-api-key": heygen_key},
        ),
        get_json(
            "HeyGen",
            "https://api.heygen.com/v3/videos",
            {"x-api-key": heygen_key},
            {"limit": "100"},
        ),
        get_json(
            "fal.ai",
            "https://api.fal.ai/v1/account/billing",
            {"Authorization": f"Key {fal_key}"},
            {"expand": "credits"},
        ),
    ]
    result = {
        "schema_version": "1.0.0",
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "read_only": True,
        "paid_generation_started": False,
        "checks": checks,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
