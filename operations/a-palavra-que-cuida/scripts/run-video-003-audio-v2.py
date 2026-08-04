from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from decimal import Decimal, ROUND_UP
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
CHANNEL_ROOT = PROJECT_ROOT / "operations" / "a-palavra-que-cuida"
MANIFEST = CHANNEL_ROOT / "02_roteiros" / "video-003-performance-v2.json"
QUOTE_PATH = CHANNEL_ROOT / "06_edicao" / "video-003" / "custos" / "elevenlabs-v2.json"
EXECUTION_PATH = (
    CHANNEL_ROOT
    / "06_edicao"
    / "video-003"
    / "custos"
    / "elevenlabs-execution-v2.json"
)
LEDGER_PATH = CHANNEL_ROOT / "06_edicao" / "video-003" / "custos" / "events.jsonl"
OUTPUT_DIR = CHANNEL_ROOT / "05_audio" / "video-003" / "v2"
BUILDER = CHANNEL_ROOT / "06_edicao" / "piloto-001" / "build_audio_v1.py"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def append_event(event: str, payload: dict) -> None:
    LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LEDGER_PATH.open("a", encoding="utf-8") as handle:
        record = {"event": event, "recorded_at": now(), **payload}
        handle.write(
            json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n"
        )


def builder_command(generate: bool) -> list[str]:
    command = [
        sys.executable,
        str(BUILDER),
        "--manifest",
        str(MANIFEST),
        "--output-dir",
        str(OUTPUT_DIR),
        "--output-prefix",
        "video-003-narracao-v2",
        "--review-title",
        "Video 003 - Narracao v2",
    ]
    if generate:
        command.append("--generate")
    return command


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Executa a narracao v2 do video 003 com custo e idempotencia."
    )
    parser.add_argument("--commit-paid-call", action="store_true")
    parser.add_argument("--approved-maximum-usd", type=Decimal)
    args = parser.parse_args()

    quote = json.loads(QUOTE_PATH.read_text(encoding="utf-8"))
    if quote["quote_id"] != "v003-elevenlabs-v2-20260723":
        raise RuntimeError("A cotacao esperada foi substituida.")
    maximum = Decimal(str(quote["maximum_cost"]))

    if not args.commit_paid_call:
        subprocess.run(builder_command(False), check=True)
        print(
            json.dumps(
                {
                    "state": "dry-run",
                    "expected_usd": quote["expected_cost"],
                    "maximum_usd": quote["maximum_cost"],
                    "incremental_cash_usd": quote[
                        "maximum_incremental_cash_charge"
                    ],
                    "paid_call_started": False,
                },
                ensure_ascii=False,
            )
        )
        return

    if args.approved_maximum_usd is None or args.approved_maximum_usd < maximum:
        raise RuntimeError(
            f"A execucao exige aprovacao explicita de pelo menos US$ {maximum}."
        )

    report_path = OUTPUT_DIR / "resultado-geracao.json"
    if EXECUTION_PATH.exists():
        previous = json.loads(EXECUTION_PATH.read_text(encoding="utf-8"))
        if previous.get("state") == "reconciled" and report_path.is_file():
            print(
                json.dumps(
                    {"state": "already-reconciled", "report": str(report_path)},
                    ensure_ascii=False,
                )
            )
            return
        raise RuntimeError(
            "Existe uma execucao incompleta. Diagnosticar antes de repetir."
        )
    if report_path.exists():
        raise RuntimeError(
            "Resultado preexistente sem registro de execucao. Auditoria obrigatoria."
        )

    execution = {
        "schema_version": "1.0.0",
        "execution_id": f"v003-elevenlabs-v2-{sha256(MANIFEST)[:12]}",
        "idempotency_key": f"video-003-audio-v2-{sha256(MANIFEST)}",
        "quote_id": quote["quote_id"],
        "manifest_sha256": sha256(MANIFEST),
        "state": "reserved",
        "reserved_at": now(),
        "approved_maximum_usd": float(args.approved_maximum_usd),
        "automatic_retry": False,
    }
    write_json(EXECUTION_PATH, execution)
    quote["status"] = "reserved"
    write_json(QUOTE_PATH, quote)
    append_event("reserved", {"execution": execution, "quote": quote})

    try:
        subprocess.run(builder_command(True), check=True)
    except Exception as exc:
        execution["state"] = "failed_needs_incident"
        execution["failed_at"] = now()
        execution["error_type"] = type(exc).__name__
        execution["resume_point"] = (
            "Inspect provider history and partial files before any retry."
        )
        quote["status"] = "failed"
        write_json(EXECUTION_PATH, execution)
        write_json(QUOTE_PATH, quote)
        append_event("failed", {"execution": execution, "quote": quote})
        raise

    report = json.loads(report_path.read_text(encoding="utf-8"))
    credits = report.get("credits_consumed_this_run")
    if not isinstance(credits, int) or credits < 0:
        raise RuntimeError("O debito nao pode ser reconciliado automaticamente.")

    observed = (
        Decimal(credits) * Decimal(str(quote["unit_price"]))
    ).quantize(Decimal("0.000001"), rounding=ROUND_UP)
    quote["status"] = "reconciled"
    quote["observed_cost"] = float(observed)
    quote["metadata"]["observed_subscription_credits"] = credits
    quote["metadata"]["incremental_cash_charge"] = 0.0
    execution["state"] = "reconciled"
    execution["reconciled_at"] = now()
    execution["observed_subscription_credits"] = credits
    execution["observed_economic_cost_usd"] = float(observed)
    execution["report"] = str(report_path.relative_to(PROJECT_ROOT)).replace(
        "\\", "/"
    )
    write_json(QUOTE_PATH, quote)
    write_json(EXECUTION_PATH, execution)
    append_event("reconciled", {"execution": execution, "quote": quote})
    print(json.dumps(execution, ensure_ascii=False))


if __name__ == "__main__":
    main()
