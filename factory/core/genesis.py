from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class OperationThesis:
    thesis_id: str
    statement: str
    origin: str
    demand_evidence_refs: tuple[str, ...] = ()
    differentiation: str | None = None
    depth: str = "scan"


def exploratory_theses(supplied: OperationThesis, alternatives: list[OperationThesis]) -> list[OperationThesis]:
    """Retorna exatamente tres teses e aprofunda primeiro a ideia humana."""
    if supplied.origin != "user_input":
        raise ValueError("A primeira tese deve preservar a ideia fornecida pelo usuario")
    unique = [supplied]
    seen = {supplied.thesis_id}
    for thesis in alternatives:
        if thesis.thesis_id not in seen:
            unique.append(thesis)
            seen.add(thesis.thesis_id)
        if len(unique) == 3:
            break
    if len(unique) != 3:
        raise ValueError("Modo exploratorio exige tres teses distintas")
    return [
        OperationThesis(**{**thesis.__dict__, "depth": "deep" if index == 0 else "scan"})
        for index, thesis in enumerate(unique)
    ]


def thesis_ready_for_pilot(thesis: OperationThesis) -> bool:
    """Demanda observavel abre a disputa; diferenciacao define como disputar."""
    return bool(thesis.demand_evidence_refs and (thesis.differentiation or "").strip())


ChannelThesis = OperationThesis

