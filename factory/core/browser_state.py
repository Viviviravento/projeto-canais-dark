from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


SessionHealth = Literal["healthy", "expired", "challenged", "wrong_account", "unknown"]


class SelectorBreak(LookupError):
    pass


def classify_session(
    *,
    expected_account: str | None,
    observed_account: str | None,
    studio_navigation_visible: bool,
    login_visible: bool = False,
    challenge_visible: bool = False,
) -> SessionHealth:
    if challenge_visible:
        return "challenged"
    if login_visible:
        return "expired"
    if expected_account and observed_account and expected_account != observed_account:
        return "wrong_account"
    if studio_navigation_visible and observed_account:
        return "healthy"
    return "unknown"


@dataclass(frozen=True)
class SelectorCandidate:
    strategy: Literal["role_name", "label", "landmark_text", "test_id", "scoped_css"]
    value: str


SELECTOR_PRIORITY = {name: index for index, name in enumerate(("role_name", "label", "landmark_text", "test_id", "scoped_css"))}


def resolve_selector(candidates: list[SelectorCandidate], observed: dict[str, set[str]]) -> SelectorCandidate:
    for candidate in sorted(candidates, key=lambda item: SELECTOR_PRIORITY[item.strategy]):
        if candidate.value in observed.get(candidate.strategy, set()):
            return candidate
    raise SelectorBreak("Nenhum seletor semantico ou fallback observado corresponde ao controle")

