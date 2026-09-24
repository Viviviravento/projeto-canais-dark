from __future__ import annotations

from collections.abc import Iterable
from typing import Any


QUALITY_GATES = ("meaning", "fidelity", "authenticity", "quality", "license")


def _cost_benefit(option: dict[str, Any]) -> tuple[float, float, str]:
    direct_cost = float(option["estimated_cost"])
    calculated_total = (
        direct_cost
        + float(option.get("expected_rework_cost", 0))
        + float(option.get("expected_human_operation_cost", 0))
        + float(option.get("expected_downstream_cost", 0))
        - float(option.get("expected_reuse_savings", 0))
    )
    total_cost = float(option.get("expected_total_cost", calculated_total))
    expected_value = float(option.get("expected_value", 1.0))
    if direct_cost < 0 or total_cost < 0 or expected_value <= 0:
        raise ValueError("Custos nao podem ser negativos e valor esperado deve ser positivo")
    if "expected_value" in option and not option.get("value_evidence"):
        raise ValueError("Valor esperado diferente do padrao exige evidencia registrada")
    return (total_cost / expected_value, total_cost, str(option.get("id", "")))


def select_cost_optimized_eligible(options: Iterable[dict[str, Any]]) -> dict[str, Any]:
    """Otimiza custo total por valor somente entre opcoes que cumprem o resultado exigido."""
    eligible = []
    for option in options:
        checks = option.get("checks", {})
        if option.get("eligible") and all(checks.get(gate) is True for gate in QUALITY_GATES):
            eligible.append(option)
    if not eligible:
        raise ValueError("Nenhuma opcao atende sentido, fidelidade, autenticidade, qualidade e licenca")
    return min(eligible, key=_cost_benefit)


def select_lowest_cost_eligible(options: Iterable[dict[str, Any]]) -> dict[str, Any]:
    """Alias de compatibilidade; a selecao agora considera custo-beneficio total."""
    return select_cost_optimized_eligible(options)
