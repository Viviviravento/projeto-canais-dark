from __future__ import annotations

import argparse
import json
from pathlib import Path

from .contracts import list_contracts, validate_contract
from .pipeline import FactoryRun


def main() -> int:
    parser = argparse.ArgumentParser(prog="canais-factory")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("contracts")

    validate_parser = subparsers.add_parser("validate")
    validate_parser.add_argument("contract")
    validate_parser.add_argument("path", type=Path)

    run_parser = subparsers.add_parser("new-run")
    run_parser.add_argument("kind", choices=("operation", "content", "channel", "video"))
    run_parser.add_argument("run_id")
    run_parser.add_argument("output", type=Path)

    args = parser.parse_args()
    if args.command == "contracts":
        print("\n".join(list_contracts()))
        return 0
    if args.command == "validate":
        payload = json.loads(args.path.read_text(encoding="utf-8"))
        validate_contract(args.contract, payload)
        print(f"ok: {args.contract}")
        return 0
    if args.command == "new-run":
        run = FactoryRun(args.run_id, args.kind)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(run.as_dict(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(args.output)
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

