from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


CONTRACTS_ROOT = Path(__file__).resolve().parents[1] / "contracts" / "v1"


def schema_path(contract: str) -> Path:
    path = CONTRACTS_ROOT / f"{contract}.schema.json"
    if not path.is_file():
        raise KeyError(f"Contrato desconhecido: {contract}")
    return path


def load_schema(contract: str) -> dict[str, Any]:
    return json.loads(schema_path(contract).read_text(encoding="utf-8"))


def validate_contract(contract: str, payload: dict[str, Any]) -> None:
    """Valida um payload e levanta ValidationError no primeiro desvio."""
    validator = Draft202012Validator(load_schema(contract))
    errors = sorted(validator.iter_errors(payload), key=lambda error: list(error.path))
    if errors:
        raise errors[0]


def list_contracts() -> list[str]:
    return sorted(path.name.removesuffix(".schema.json") for path in CONTRACTS_ROOT.glob("*.schema.json"))

