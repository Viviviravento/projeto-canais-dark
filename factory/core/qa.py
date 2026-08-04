from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class Finding:
    check: str
    severity: str
    message: str
    scene_id: str | None = None


@dataclass
class QAReport:
    findings: list[Finding] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return not any(finding.severity in {"critical", "error"} for finding in self.findings)

    def add(self, check: str, severity: str, message: str, scene_id: str | None = None) -> None:
        self.findings.append(Finding(check, severity, message, scene_id))


def audit_package(manifest: dict[str, Any], *, sync_tolerance_seconds: float = 0.35) -> QAReport:
    """Audita manifestos, cenas e keyframes; nunca percorre o video frame a frame."""
    report = QAReport()
    output = manifest.get("output") or {}
    output_path = output.get("path")
    if output_path:
        path = Path(output_path)
        if not path.is_file() or path.stat().st_size == 0:
            report.add("technical_output", "critical", f"Arquivo de saida ausente ou vazio: {path}")
    else:
        report.add("technical_output", "error", "Manifesto sem caminho de saida")

    captions = manifest.get("captions") or {}
    if captions.get("required") and not captions.get("artifact"):
        report.add("captions", "error", "Legenda obrigatoria sem artefato")
    if captions.get("artifact") and captions.get("verify_exists") and not Path(captions["artifact"]).is_file():
        report.add("captions", "error", f"Artefato de legenda ausente: {captions['artifact']}")

    audio = manifest.get("audio") or {}
    if audio.get("required") and not audio.get("artifact"):
        report.add("voice", "error", "Audio obrigatorio sem artefato")
    if audio.get("required") and audio.get("semantic_review") != "passed":
        report.add("voice", "error", "Revisao semantica da voz ainda nao foi aprovada")

    scenes = manifest.get("scenes") or []
    if not scenes:
        report.add("scene_audit", "error", "Nenhuma cena para auditoria semantica")
        return report

    assets = Counter()
    for scene in scenes:
        scene_id = str(scene.get("id", "unknown"))
        asset = scene.get("asset_id")
        if asset:
            assets[str(asset)] += 1
        keyframes = scene.get("keyframes") or []
        if not keyframes:
            report.add("keyframes", "error", "Cena sem keyframe representativo", scene_id)
        if scene.get("contains_diegetic_text") and not scene.get("diegetic_text_integrated_verified"):
            report.add("diegetic_text", "error", "Texto no objeto nao foi validado como integrado", scene_id)
        if scene.get("requires_clean_cutout") and not scene.get("clean_cutout_verified"):
            report.add("cutout", "error", "Recorte visual ainda nao foi aprovado", scene_id)
        if scene.get("mode") == "avatar" and not scene.get("avatar_is_speaking"):
            report.add("avatar", "error", "Avatar aparece sem fala sincronizada", scene_id)
        if (
            scene.get("mode") == "avatar"
            and scene.get("composited")
            and scene.get("physical_coherence_review") != "passed"
        ):
            report.add(
                "physical_coherence",
                "error",
                "Composicao do avatar sem aprovacao de apoio, contato, oclusao, perspectiva e iluminacao",
                scene_id,
            )
        duration = float(scene.get("continuous_seconds", 0))
        max_static = float(manifest.get("visual_policy", {}).get("maximum_static_seconds", 0))
        if max_static and scene.get("mode") in {"still", "local_motion"} and duration > max_static:
            report.add("visual_pacing", "error", f"Cena permanece {duration:.3f}s; limite {max_static:.3f}s", scene_id)
        expected_text = scene.get("exact_text_expected")
        if expected_text is not None and scene.get("exact_text_observed") != expected_text:
            report.add("exact_text", "error", "Texto exibido nao corresponde ao texto exigido", scene_id)
        for sync in scene.get("sync_events") or []:
            delta = abs(float(sync["visual_start"]) - float(sync["audio_start"]))
            if delta > sync_tolerance_seconds:
                report.add("sync", "error", f"Dessincronia de {delta:.3f}s", scene_id)

    max_reuse = int(manifest.get("visual_policy", {}).get("max_asset_reuse", 2))
    for asset_id, count in assets.items():
        if count > max_reuse:
            report.add("asset_repetition", "warning", f"Ativo {asset_id} usado {count} vezes; limite {max_reuse}")

    end_screen = manifest.get("end_screen") or {}
    if end_screen.get("required"):
        duration = float(end_screen.get("duration_seconds", 0))
        minimum = float(end_screen.get("minimum_seconds", 0))
        maximum = float(end_screen.get("maximum_seconds", 20))
        if duration < minimum or duration > maximum:
            report.add("end_screen", "error", f"Tela final com {duration}s fora do intervalo {minimum}-{maximum}s")
        slots = int(end_screen.get("slots", 0))
        if slots != 2:
            report.add(
                "end_screen",
                "error",
                f"Tela final precisa de exatamente dois espacos de recomendacao; encontrou {slots}",
            )

        native_video_elements = end_screen.get("native_video_elements")
        if native_video_elements is not None:
            native_video_count = sum(
                1 for element in native_video_elements if element.get("type") == "video"
            )
            if native_video_count != 2:
                report.add(
                    "end_screen",
                    "error",
                    "Tela final precisa de exatamente dois elementos nativos de video",
                )

    return report
