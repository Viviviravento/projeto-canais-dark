from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from decimal import Decimal, ROUND_UP
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CHANNEL_ROOT = PROJECT_ROOT / "Canal Religioso"
MANIFEST = CHANNEL_ROOT / "02_roteiros" / "video-003-calibracao-performance-v2.json"
QUOTE_PATH = CHANNEL_ROOT / "06_edicao" / "video-003" / "custos" / "elevenlabs-calibracao-v2.json"
EXECUTION_PATH = CHANNEL_ROOT / "06_edicao" / "video-003" / "custos" / "elevenlabs-calibracao-v2-execution.json"
OUTPUT_DIR = CHANNEL_ROOT / "05_audio" / "video-003" / "calibracao-v2"
GENERATOR = CHANNEL_ROOT / "06_edicao" / "piloto-001" / "calibrate_audio.py"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def command(generate: bool) -> list[str]:
    result = [sys.executable, str(GENERATOR), "--manifest", str(MANIFEST), "--output-dir", str(OUTPUT_DIR)]
    if generate:
        result.append("--generate")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Executa a calibracao semantica v2 com teto real e sem retentativa.")
    parser.add_argument("--commit-paid-call", action="store_true")
    parser.add_argument("--approved-maximum-usd", type=Decimal)
    args = parser.parse_args()

    quote = json.loads(QUOTE_PATH.read_text(encoding="utf-8"))
    maximum = Decimal(str(quote["maximum_cost"]))
    if not args.commit_paid_call:
        subprocess.run(command(False), check=True)
        print(json.dumps({"state": "dry-run", "characters": quote["quantity"], "maximum_usd": quote["maximum_cost"]}, ensure_ascii=False))
        return
    if args.approved_maximum_usd is None or args.approved_maximum_usd < maximum:
        raise RuntimeError(f"A calibracao exige aprovacao explicita de pelo menos US$ {maximum}.")
    if EXECUTION_PATH.exists() or (OUTPUT_DIR / "resultado-geracao.json").exists():
        raise RuntimeError("Calibracao ja iniciada ou concluida; nao repetir chamadas automaticamente.")

    execution = {
        "schema_version": "1.0.0",
        "execution_id": "v003-calibration-v2",
        "quote_id": quote["quote_id"],
        "state": "reserved",
        "reserved_at": now(),
        "approved_maximum_usd": float(args.approved_maximum_usd),
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
        raise RuntimeError("Amostras geradas, mas o consumo nao pode ser reconciliado automaticamente.")
    observed = (Decimal(credits) * Decimal(str(quote["unit_price"]))).quantize(Decimal("0.000001"), rounding=ROUND_UP)
    quote["status"] = "reconciled"
    quote["observed_cost"] = float(observed)
    quote["metadata"]["observed_subscription_credits"] = credits
    execution.update({
        "state": "reconciled_pending_human_review",
        "reconciled_at": now(),
        "observed_subscription_credits": credits,
        "observed_economic_cost_usd": float(observed),
        "review_page": str((OUTPUT_DIR / "avaliacao.html").relative_to(PROJECT_ROOT)).replace("\\", "/"),
    })
    write(QUOTE_PATH, quote)
    write(EXECUTION_PATH, execution)
    print(json.dumps(execution, ensure_ascii=False))


if __name__ == "__main__":
    main()
