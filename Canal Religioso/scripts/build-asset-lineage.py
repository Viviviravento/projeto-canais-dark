from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
ASSET_ROOT = ROOT / "04_assets" / "video-003"
OUTPUT = ASSET_ROOT / "generated" / "lineage-v1.json"

SUMMARIES = {
    "j01-job-before-loss-v1.png": "Jo antes das perdas, integro e sereno em ambiente do antigo Oriente Proximo.",
    "j02-job-after-loss-v1.png": "Jo depois das perdas, digno e abatido entre ruinas, sem sofrimento grafico.",
    "j03-messengers-v1.png": "Mensageiros trazendo noticias sucessivas a Jo em ambiente historico plausivel.",
    "j04-friends-arrive-v1.png": "Tres amigos de Jo chegando para acompanha-lo em sua dor.",
    "j05-seven-days-silence-v1.png": "Jo e seus tres amigos sentados em silencio, preservando distancia e gravidade.",
    "j06-friend-speaks-v1.png": "Um amigo fala de modo assertivo enquanto Jo escuta entre os demais.",
    "j07-job-responds-v1.png": "Jo responde aos amigos com lamento e firmeza contida.",
    "j08-job-lament-night-v1.png": "Jo sozinho durante a noite em lamento honesto, sem teatralidade.",
    "j09-whirlwind-v1.png": "Jo diante de um redemoinho vasto, destacando limite humano e escala da criacao.",
    "j10-reconciliation-v1.png": "Jo e os amigos em gesto final de reconciliacao, sem triunfalismo material.",
    "b01-difficult-clinic-news-v1.png": "Mulher brasileira recebendo noticia dificil em clinica, com emocao contida.",
    "b02-job-loss-bakery-v1.png": "Trabalhadora brasileira diante do fechamento ou perda do trabalho em padaria.",
    "b03-silent-presence-v1.png": "Duas mulheres brasileiras em presenca silenciosa e acolhedora.",
    "b04-practical-meal-help-v1.png": "Ajuda concreta entre mulheres brasileiras por meio de uma refeicao simples.",
    "b05-legal-guidance-v1.png": "Mulher brasileira recebendo orientacao juridica pratica, sem texto legivel artificial.",
    "b06-psychological-support-v1.png": "Atendimento psicologico respeitoso entre duas mulheres brasileiras.",
    "b07-accompanied-bus-stop-v1.png": "Mulher brasileira acompanhada em ponto de onibus urbano depois de um dia dificil.",
    "b08-honest-lament-v1.png": "Mulher brasileira orando com cansaco e honestidade em casa.",
    "video-003-thumbnail-base-v1.png": "Retrato de Jo a direita, rosto grande e iluminado, com espaco negativo a esquerda para tipografia.",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    files = sorted((ASSET_ROOT / "generated").rglob("*.png"))
    files += [ASSET_ROOT / "thumbnail" / "video-003-thumbnail-base-v1.png"]
    unknown = [path.name for path in files if path.name not in SUMMARIES]
    if unknown:
        raise RuntimeError(f"Assets sem resumo de linhagem: {unknown}")

    assets = []
    for path in files:
        with Image.open(path) as image:
            width, height = image.size
        assets.append({
            "asset_id": path.stem,
            "file": path.relative_to(ROOT).as_posix(),
            "sha256": sha256(path),
            "width": width,
            "height": height,
            "media_type": "image/png",
            "origin": "Codex integrated image generation",
            "license": "generated-for-project",
            "prompt_record": {
                "kind": "reconstructed_summary" if path.parent.name != "thumbnail" else "exact_prompt_in_sibling_file",
                "summary": SUMMARIES[path.name],
                "exact_prompt_ref": "04_assets/video-003/thumbnail/video-003-thumbnail-base-v1.prompt.md" if path.parent.name == "thumbnail" else None,
            },
            "human_review": "accepted_for_video_003_asset_pool",
        })

    payload = {
        "schema_version": "1.0.0",
        "collection_id": "palavra-que-cuida-video-003-generated",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "recording_note": "Os prompts historicos exatos da primeira rodada nao foram persistidos localmente; para nao inventa-los, este manifesto os registra como resumos reconstruidos. Novas geracoes devem persistir o prompt exato antes da chamada.",
        "global_constraints": [
            "personagem de Jo consistente entre cenas",
            "antigo Oriente Proximo sem anacronismo cristao",
            "cotidiano brasileiro plausivel e sem pobreza performatica",
            "dor contida, sem ferimentos graficos",
            "sem texto gerado; textos e referencias entram na composicao",
        ],
        "assets": assets,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{OUTPUT}: {len(assets)} assets")


if __name__ == "__main__":
    main()
