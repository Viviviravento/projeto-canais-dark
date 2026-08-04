from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
CHANNEL_ROOT = PROJECT_ROOT / "operations" / "a-palavra-que-cuida"
MANIFEST = CHANNEL_ROOT / "02_roteiros" / "video-004-calibracao-performance-v1.json"
QUOTE_PATH = CHANNEL_ROOT / "06_edicao" / "video-004" / "custos" / "elevenlabs-calibracao-v1.json"
EXECUTION_PATH = CHANNEL_ROOT / "06_edicao" / "video-004" / "custos" / "elevenlabs-calibracao-v1-execution.json"
OUTPUT_DIR = CHANNEL_ROOT / "05_audio" / "video-004" / "calibracao-v1"
GENERATOR = CHANNEL_ROOT / "06_edicao" / "piloto-001" / "calibrate_audio.py"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def command(generate: bool) -> list[str]:
    result = [
        sys.executable,
        str(GENERATOR),
        "--manifest",
        str(MANIFEST),
        "--output-dir",
        str(OUTPUT_DIR),
    ]
    if generate:
        result.append("--generate")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Gera as amostras de voz do vídeo 004 com teto de crédito e sem retentativa.")
    parser.add_argument("--commit-paid-call", action="store_true")
    parser.add_argument("--approved-maximum-credits", type=int)
    args = parser.parse_args()

    quote = json.loads(QUOTE_PATH.read_text(encoding="utf-8"))
    maximum = int(quote["maximum_subscription_credits"])
    if not args.commit_paid_call:
        subprocess.run(command(False), check=True)
        print(json.dumps({"state": "dry-run", "maximum_credits": maximum}, ensure_ascii=False))
        return
    if args.approved_maximum_credits is None or args.approved_maximum_credits < maximum:
        raise RuntimeError(f"A calibração exige aprovação explícita de pelo menos {maximum} créditos.")
    if quote.get("maximum_incremental_cash_charge") != 0.0:
        raise RuntimeError("A cotação deixou de garantir custo incremental zero.")
    if maximum > int(quote["subscription_snapshot"]["credits_remaining"]):
        raise RuntimeError("O teto da calibração excede o saldo conferido.")
    if EXECUTION_PATH.exists() or (OUTPUT_DIR / "resultado-geracao.json").exists():
        raise RuntimeError("A calibração já foi iniciada ou concluída; não repetir automaticamente.")

    execution = {
        "schema_version": "1.0.0",
        "execution_id": "v004-elevenlabs-calibration-v1",
        "quote_id": quote["quote_id"],
        "state": "reserved",
        "reserved_at": now(),
        "approved_maximum_credits": args.approved_maximum_credits,
        "automatic_retry": False,
    }
    quote["status"] = "reserved"
    write(EXECUTION_PATH, execution)
    write(QUOTE_PATH, quote)
    try:
        subprocess.run(command(True), check=True)
    except Exception as exc:
        execution.update({"state": "failed_needs_incident", "failed_at": now(), "error_type": type(exc).__name__})
        quote["status"] = "failed"
        write(EXECUTION_PATH, execution)
        write(QUOTE_PATH, quote)
        raise

    report = json.loads((OUTPUT_DIR / "resultado-geracao.json").read_text(encoding="utf-8"))
    credits = report.get("credits_consumed")
    if not isinstance(credits, int) or credits < 0:
        raise RuntimeError("As amostras foram geradas, mas o consumo não pode ser reconciliado automaticamente.")
    if credits > maximum:
        raise RuntimeError("O consumo observado ultrapassou o teto aprovado; auditoria obrigatória.")

    quote["status"] = "reconciled"
    quote["observed_subscription_credits"] = credits
    execution.update({
        "state": "reconciled_pending_human_review",
        "reconciled_at": now(),
        "observed_subscription_credits": credits,
        "review_page": str((OUTPUT_DIR / "avaliacao.html").relative_to(PROJECT_ROOT)).replace("\\", "/"),
    })
    write(QUOTE_PATH, quote)
    write(EXECUTION_PATH, execution)
    print(json.dumps(execution, ensure_ascii=False))


if __name__ == "__main__":
    main()
