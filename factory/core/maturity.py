from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


CAPABILITY_STATES = frozenset(
    {"unexercised", "investigating", "validating", "stable", "regression_detected", "blocked", "not_applicable"}
)
LIFECYCLE_STATES = frozenset({"exploring", "incubating", "piloting", "stabilizing", "operational", "paused", "retired"})
_MISSING = object()


@dataclass(frozen=True)
class BaselineComparison:
    compatible: bool
    changed_paths: tuple[str, ...]


def _value_at(payload: Mapping[str, Any], dotted_path: str) -> Any:
    current: Any = payload
    for part in dotted_path.split("."):
        if not isinstance(current, Mapping) or part not in current:
            return _MISSING
        current = current[part]
    return current


def compare_baseline(baseline: Mapping[str, Any], current_parameters: Mapping[str, Any]) -> BaselineComparison:
    """Compara somente parâmetros explicitamente rastreados pela baseline."""
    paths = baseline["invalidation"]["tracked_parameter_paths"]
    reference_parameters = baseline["parameters"]
    changed = tuple(
        path
        for path in paths
        if _value_at(reference_parameters, path) != _value_at(current_parameters, path)
    )
    return BaselineComparison(compatible=not changed, changed_paths=changed)


def revalidation_status(capability: Mapping[str, Any], comparison: BaselineComparison) -> dict[str, Any]:
    """Retorna a transição determinística sem promover ou alterar evidência."""
    if not comparison.compatible:
        return {
            "state": "validating",
            "baseline_invalidated": True,
            "changed_paths": list(comparison.changed_paths),
            "revalidation_required": True,
        }
    return {
        "state": capability["state"],
        "baseline_invalidated": False,
        "changed_paths": [],
        "revalidation_required": False,
    }
