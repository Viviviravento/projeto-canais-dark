from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

import requests


PROJECT_ROOT = Path(__file__).resolve().parents[3]
CHANNEL_ROOT = PROJECT_ROOT / "operations" / "a-palavra-que-cuida"
ENV_PATH = PROJECT_ROOT / "tools" / "OpenMontage" / ".env"
SCRIPT_PATH = CHANNEL_ROOT / "02_roteiros" / "video-007-roteiro-v1.md"
CITATIONS_PATH = CHANNEL_ROOT / "02_roteiros" / "video-007-citacoes-acf-v1.json"
PERFORMANCE_PATH = CHANNEL_ROOT / "02_roteiros" / "video-007-performance-v1.json"
BLUEPRINT_PATH = CHANNEL_ROOT / "02_roteiros" / "video-007-blueprint-v1.json"
PREFLIGHT_PATH = CHANNEL_ROOT / "06_edicao" / "video-007" / "preflight-prosodia-v1.json"
QUOTE_PATH = CHANNEL_ROOT / "06_edicao" / "video-007" / "custos" / "elevenlabs-v1.json"

FUNCTIONS = {
    "01": "Abrir pela vida cotidiana e redefinir tentação como atalho que parece alívio.",
    "02": "Mostrar a fome real de Jesus e separar necessidade de submissão ao impulso.",
    "03": "Aplicar a pressão de provar valor sem transformar coragem em espetáculo.",
    "04": "Expor o custo escondido de trocar convicção por controle rápido.",
    "05": "Acolher a fraqueza com Hebreus 4 sem normalizar uma escolha destrutiva.",
    "06": "Oferecer perguntas práticas para discernir antes de decidir.",
    "07": "Reafirmar que Jesus não pede pressa nem passividade diante da dor.",
    "08": "Concluir com CTA, continuidade e uma pergunta concreta para comentários.",
}


def write(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def slug(value: str) -> str:
    normalized = value.casefold().translate(str.maketrans("áàâãéêíóôõúç", "aaaaeeiooouc"))
    return re.sub(r"[^a-z0-9]+", "-", normalized).strip("-")


def parse_blocks() -> list[dict]:
    source = SCRIPT_PATH.read_text(encoding="utf-8")
    matches = list(re.finditer(r"^##\s+(\d+)\s+-\s+(.+)$", source, flags=re.MULTILINE))
    if len(matches) != 8:
        raise RuntimeError(f"Expected 8 roteiro blocks, found {len(matches)}")
    blocks = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(source)
        number, title = match.group(1), match.group(2).strip()
        blocks.append({"id": f"{number}-{slug(title)}", "source_section": number, "title": title, "function": FUNCTIONS[number], "text": source[match.end():end].strip()})
    return blocks


def subscription() -> dict:
    api_key = None
    for raw in ENV_PATH.read_text(encoding="utf-8-sig").splitlines():
        if raw.strip().startswith("ELEVENLABS_API_KEY="):
            api_key = raw.split("=", 1)[1].strip().strip('"').strip("'")
            break
    if not api_key:
        return {"ok": False, "error": "ELEVENLABS_API_KEY not found"}
    response = requests.get("https://api.elevenlabs.io/v1/user/subscription", headers={"xi-api-key": api_key}, timeout=60)
    response.raise_for_status()
    payload = response.json()
    used, limit = payload.get("character_count"), payload.get("character_limit")
    return {"ok": True, "tier": payload.get("tier"), "character_count": used, "character_limit": limit, "credits_remaining_observed": limit - used if isinstance(used, int) and isinstance(limit, int) else None, "checked_at": datetime.now(timezone.utc).isoformat()}


def main() -> None:
    blocks = parse_blocks()
    citations = json.loads(CITATIONS_PATH.read_text(encoding="utf-8"))
    text = "\n\n".join(block["text"] for block in blocks)
    characters = sum(len(block["text"]) for block in blocks)
    missing = [citation["reference"] for citation in citations["direct_acf_citations"] if citation["spoken_lead_in"] not in text or citation["text"] not in text]
    estimated_seconds = round(characters * 0.07667, 1)
    performance = {
        "version": "video-007-performance-v1",
        "source_script": str(SCRIPT_PATH),
        "performance_contract": {
            "relationship": "Falar com quem está vulnerável a escolher um alívio que pode cobrar caro depois.",
            "authority": "Jesus no deserto como luz para a vida cotidiana, sem moralismo ou simplificação da dor.",
            "intensity": "Íntimo, claro e sereno. Começar pela experiência humana e usar a Bíblia para dar direção.",
            "scripture": "Anunciar referência e mostrar carta ACF somente enquanto a citação direta estiver sendo lida.",
            "pause_policy": "Sem break tags e sem pontuação artificial. Frases naturais e curtas quando a ideia pedir pausa.",
            "cta": "Pedir inscrição, curta e compartilhamento; apontar para Marta e Maria e Não andeis ansiosos; concluir com pergunta de comentário.",
        },
        "api": {
            "provider": "ElevenLabs",
            "voice_name": "Bruno Cardoso",
            "voice_id": "iF2QszmZhlyFLleUoFxy",
            "model_id": "eleven_multilingual_v2",
            "language_code": "pt",
            "output_format": "mp3_44100_128",
            "seed": 314159,
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.75, "style": 0.0, "speed": 1.0, "use_speaker_boost": True},
            "postprocess": {"speed_factor": 1.07, "preserve_pitch": True},
        },
        "blocks": blocks,
    }
    blueprint = {
        "schema_version": "1.0.0",
        "video_id": "video-007",
        "title": "Quando o atalho parece alívio",
        "primary_text": "Mateus 4:1-10",
        "supporting_text": "Hebreus 4:15",
        "promise": "Ajudar a espectadora a reconhecer quando uma necessidade real está sendo usada para empurrá-la a um caminho que cobra caro.",
        "audience_moment": "Cansaço, carência, pressa e pressão para resolver algo sem clareza.",
        "visual_direction": {"core": "Noite e manhã em casa, escolhas cotidianas, caminho, pausa, deserto discreto e presença humana.", "human_preference": "Mulheres brasileiras/latinas, naturais e reconhecíveis; uma peça de crochê sutil em apenas uma cena quando fizer sentido.", "avoid": ["texto editorial fora de citações", "anjos ou sobrenatural não narrado", "tentação caricata ou sensacionalista"]},
        "short_candidates": [{"id": "v007-short-01", "hook": "O atalho quase nunca diz que vai ferir você", "source_sections": ["01", "02"]}, {"id": "v007-short-02", "hook": "Nem tudo que parece coragem é fé", "source_sections": ["03", "04"]}],
        "publication_bridge": {"end_screen_targets": ["video-006", "video-002"], "comment_prompt": "Que tipo de atalho costuma parecer alívio quando você está cansada?"},
    }
    status = "passed_pending_paid_audio_approval" if not missing and 8000 <= characters <= 9900 and "<break" not in text else "failed"
    preflight = {"schema_version": "1.0.0", "video_id": "video-007", "status": status, "checks": {"blocks": len(blocks), "total_characters": characters, "estimated_postprocess_duration_seconds": estimated_seconds, "allowed_postprocess_duration_seconds": [600, 780], "break_tags_found": "<break" in text, "missing_direct_citations": missing, "cta_contains_next_video_direction": "vídeos sugeridos na tela" in text, "cta_contains_comment_prompt": "comentários" in blocks[-1]["text"]}, "known_risk": "A estimativa parte do ritmo real do vídeo 006; a duração final será conferida pelo WAV e pela linha do tempo antes da edição."}
    snap = subscription()
    maximum = ((characters + 999) // 1000) * 1000
    quote = {"schema_version": "1.0.0", "quote_id": "v007-elevenlabs-v1-20260728", "provider": "ElevenLabs", "model": "eleven_multilingual_v2", "operation": "full eight-block narration for video-007 using independent requests and 1.07x local postprocess", "unit": "provider credit", "quantity": characters, "expected_subscription_credits": characters, "maximum_subscription_credits": maximum, "currency": "USD", "expected_incremental_cash_charge": 0.0, "maximum_incremental_cash_charge": 0.0, "price_checked_at": snap.get("checked_at"), "price_source": "Authenticated ElevenLabs subscription API read-only check in this Codex session; no paid generation started.", "subscription_snapshot": snap, "status": "reserved_pending_user_approval", "approval": {"approved_at": None, "user_statement": None, "scope": f"Generate only the full narration for video-007 up to {maximum} subscription credits. No automatic retry and no incremental cash charge."}, "metadata": {"manifest": "operations/a-palavra-que-cuida/02_roteiros/video-007-performance-v1.json", "citation_manifest": "operations/a-palavra-que-cuida/02_roteiros/video-007-citacoes-acf-v1.json", "request_stitching": False, "context_mode": "independent_blocks", "automatic_retry": False, "postprocess_after_generation": "1.07x preserving pitch before master alignment"}}
    write(PERFORMANCE_PATH, performance)
    write(BLUEPRINT_PATH, blueprint)
    write(PREFLIGHT_PATH, preflight)
    write(QUOTE_PATH, quote)
    print(json.dumps({"characters": characters, "estimated_seconds": estimated_seconds, "maximum_credits": maximum, "preflight": status, "subscription": snap.get("credits_remaining_observed")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
