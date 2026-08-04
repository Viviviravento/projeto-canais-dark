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
MANIFEST = CHANNEL_ROOT / "02_roteiros" / "video-006-performance-v1.json"
QUOTE_PATH = CHANNEL_ROOT / "06_edicao" / "video-006" / "custos" / "elevenlabs-v1.json"
EXECUTION_PATH = CHANNEL_ROOT / "06_edicao" / "video-006" / "custos" / "elevenlabs-v1-execution.json"
PREFLIGHT_PATH = CHANNEL_ROOT / "06_edicao" / "video-006" / "preflight-prosodia-v1.json"
OUTPUT_DIR = CHANNEL_ROOT / "05_audio" / "video-006" / "v1"
BUILDER = CHANNEL_ROOT / "06_edicao" / "piloto-001" / "build_audio_v1.py"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def command(generate: bool, resume_missing_blocks: bool = False) -> list[str]:
    result = [
        sys.executable,
        str(BUILDER),
        "--manifest", str(MANIFEST),
        "--output-dir", str(OUTPUT_DIR),
        "--output-prefix", "video-006-narracao-v1",
        "--review-title", "Vídeo 006 — Narração v1",
        "--disable-request-stitching",
    ]
    if generate:
        result.append("--generate")
    if resume_missing_blocks:
        result.append("--resume-missing-blocks")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Gera a narração integral do vídeo 006 sem encadeamento de requests.")
    parser.add_argument("--commit-paid-call", action="store_true")
    parser.add_argument("--resume-interrupted-call", action="store_true")
    parser.add_argument("--approved-maximum-credits", type=int)
    parser.add_argument("--user-statement", default="nice, continua, no roteiro voce nao comete erros, confio 100%")
    args = parser.parse_args()

    quote = json.loads(QUOTE_PATH.read_text(encoding="utf-8"))
    preflight = json.loads(PREFLIGHT_PATH.read_text(encoding="utf-8"))
    maximum = int(quote["maximum_subscription_credits"])
    if preflight.get("status") != "passed_pending_paid_audio_approval":
        raise RuntimeError("A narração integral exige preflight de prosódia aprovado.")
    permitted_quote_statuses = {"reserved_pending_user_approval"}
    if args.resume_interrupted_call:
        permitted_quote_statuses.add("reserved")
    if quote.get("status") not in permitted_quote_statuses:
        raise RuntimeError(f"A cotação não está aberta para aprovação: {quote.get('status')}")
    if not args.commit_paid_call:
        subprocess.run(command(False), check=True)
        print(json.dumps({"state": "dry-run", "maximum_credits": maximum}, ensure_ascii=False))
        return
    if args.approved_maximum_credits is None or args.approved_maximum_credits < maximum:
        raise RuntimeError(f"A narração integral exige aprovação explícita de pelo menos {maximum} créditos.")
    if quote.get("maximum_incremental_cash_charge") != 0.0:
        raise RuntimeError("A cotação deixou de garantir custo incremental zero.")
    remaining = quote.get("subscription_snapshot", {}).get("credits_remaining_observed")
    if not isinstance(remaining, int) or maximum > remaining:
        raise RuntimeError("O teto da narração excede o saldo observado disponível.")
    if EXECUTION_PATH.exists() or (OUTPUT_DIR / "resultado-geracao.json").exists():
        if not args.resume_interrupted_call or (OUTPUT_DIR / "resultado-geracao.json").exists():
            raise RuntimeError("A narração já foi iniciada ou concluída; não repetir automaticamente.")

    if args.resume_interrupted_call:
        execution = json.loads(EXECUTION_PATH.read_text(encoding="utf-8"))
        execution["state"] = "resuming_missing_blocks"
        execution["resumed_at"] = now()
        write(EXECUTION_PATH, execution)
    else:
        approved_at = now()
        quote["status"] = "reserved"
        quote["approval"]["approved_at"] = approved_at
        quote["approval"]["user_statement"] = args.user_statement
        execution = {
            "schema_version": "1.0.0",
            "execution_id": f"v006-elevenlabs-v1-{sha256(MANIFEST)[:12]}",
            "quote_id": quote["quote_id"],
            "manifest_sha256": sha256(MANIFEST),
            "state": "reserved",
            "reserved_at": approved_at,
            "approved_maximum_credits": args.approved_maximum_credits,
            "request_stitching": False,
            "automatic_retry": False,
        }
        write(EXECUTION_PATH, execution)
        write(QUOTE_PATH, quote)
    try:
        subprocess.run(command(True, args.resume_interrupted_call), check=True)
    except Exception as exc:
        execution.update({"state": "failed_needs_incident", "failed_at": now(), "error_type": type(exc).__name__})
        quote["status"] = "failed"
        write(EXECUTION_PATH, execution)
        write(QUOTE_PATH, quote)
        raise

    report = json.loads((OUTPUT_DIR / "resultado-geracao.json").read_text(encoding="utf-8"))
    observed = report.get("character_cost_current_version_sum")
    if report.get("request_stitching") is not False:
        raise RuntimeError("A geração integral usou encadeamento de requests; auditoria obrigatória.")
    if not isinstance(observed, int) or observed < 0:
        raise RuntimeError("O consumo da narração não pode ser reconciliado automaticamente.")
    if observed > maximum:
        raise RuntimeError("O consumo observado ultrapassou o teto aprovado; auditoria obrigatória.")

    quote["status"] = "reconciled"
    quote["observed_subscription_credits"] = observed
    execution.update({
        "state": "reconciled_pending_master_qa",
        "reconciled_at": now(),
        "observed_subscription_credits": observed,
        "report": str((OUTPUT_DIR / "resultado-geracao.json").relative_to(PROJECT_ROOT)).replace("\\", "/"),
    })
    write(QUOTE_PATH, quote)
    write(EXECUTION_PATH, execution)
    print(json.dumps(execution, ensure_ascii=False))


if __name__ == "__main__":
    main()
