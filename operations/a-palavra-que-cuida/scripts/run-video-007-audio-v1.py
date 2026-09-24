from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
CHANNEL_ROOT = PROJECT_ROOT / "operations" / "a-palavra-que-cuida"
MANIFEST = CHANNEL_ROOT / "02_roteiros" / "video-007-performance-v1.json"
QUOTE_PATH = CHANNEL_ROOT / "06_edicao" / "video-007" / "custos" / "elevenlabs-v1.json"
EXECUTION_PATH = CHANNEL_ROOT / "06_edicao" / "video-007" / "custos" / "elevenlabs-v1-execution.json"
PREFLIGHT_PATH = CHANNEL_ROOT / "06_edicao" / "video-007" / "preflight-prosodia-v1.json"
OUTPUT_DIR = CHANNEL_ROOT / "05_audio" / "video-007" / "v1"
BUILDER = CHANNEL_ROOT / "06_edicao" / "piloto-001" / "build_audio_v1.py"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def command(generate: bool) -> list[str]:
    command_line = [sys.executable, str(BUILDER), "--manifest", str(MANIFEST), "--output-dir", str(OUTPUT_DIR), "--output-prefix", "video-007-narracao-v1", "--review-title", "Vídeo 007 — Narração v1", "--disable-request-stitching"]
    if generate:
        command_line.append("--generate")
    return command_line


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--commit-paid-call", action="store_true")
    parser.add_argument("--approved-maximum-credits", type=int)
    parser.add_argument("--user-statement", default="continua")
    args = parser.parse_args()
    quote = json.loads(QUOTE_PATH.read_text(encoding="utf-8"))
    preflight = json.loads(PREFLIGHT_PATH.read_text(encoding="utf-8"))
    maximum = int(quote["maximum_subscription_credits"])
    if preflight.get("status") != "passed_pending_paid_audio_approval":
        raise RuntimeError("A narração exige preflight aprovado.")
    if quote.get("status") != "reserved_pending_user_approval":
        raise RuntimeError(f"A cotação não está aberta para aprovação: {quote.get('status')}")
    if not args.commit_paid_call:
        subprocess.run(command(False), check=True)
        print(json.dumps({"state": "dry-run", "maximum_credits": maximum}, ensure_ascii=False))
        return
    if args.approved_maximum_credits is None or args.approved_maximum_credits < maximum:
        raise RuntimeError(f"A narração exige aprovação de pelo menos {maximum} créditos.")
    if quote.get("maximum_incremental_cash_charge") != 0.0:
        raise RuntimeError("A cotação não garante custo incremental zero.")
    remaining = quote.get("subscription_snapshot", {}).get("credits_remaining_observed")
    if not isinstance(remaining, int) or remaining < maximum:
        raise RuntimeError("O saldo observado não cobre o teto aprovado.")
    if EXECUTION_PATH.exists() or (OUTPUT_DIR / "resultado-geracao.json").exists():
        raise RuntimeError("A narração já foi iniciada ou concluída; não repetir automaticamente.")
    approved_at = now()
    quote["status"] = "reserved"
    quote["approval"].update({"approved_at": approved_at, "user_statement": args.user_statement})
    execution = {"schema_version": "1.0.0", "execution_id": f"v007-elevenlabs-v1-{sha256(MANIFEST)[:12]}", "quote_id": quote["quote_id"], "manifest_sha256": sha256(MANIFEST), "state": "reserved", "reserved_at": approved_at, "approved_maximum_credits": args.approved_maximum_credits, "request_stitching": False, "automatic_retry": False}
    write(QUOTE_PATH, quote)
    write(EXECUTION_PATH, execution)
    try:
        subprocess.run(command(True), check=True)
    except Exception as exc:
        execution.update({"state": "failed_needs_incident", "failed_at": now(), "error_type": type(exc).__name__})
        quote["status"] = "failed"
        write(QUOTE_PATH, quote)
        write(EXECUTION_PATH, execution)
        raise
    report = json.loads((OUTPUT_DIR / "resultado-geracao.json").read_text(encoding="utf-8"))
    observed = report.get("character_cost_current_version_sum")
    if report.get("request_stitching") is not False or not isinstance(observed, int) or observed > maximum:
        raise RuntimeError("A geração exige auditoria antes de reconciliação.")
    quote.update({"status": "reconciled", "observed_subscription_credits": observed})
    execution.update({"state": "reconciled_pending_master_qa", "reconciled_at": now(), "observed_subscription_credits": observed, "report": str((OUTPUT_DIR / "resultado-geracao.json").relative_to(PROJECT_ROOT)).replace("\\", "/")})
    write(QUOTE_PATH, quote)
    write(EXECUTION_PATH, execution)
    print(json.dumps(execution, ensure_ascii=False))


if __name__ == "__main__":
    main()
