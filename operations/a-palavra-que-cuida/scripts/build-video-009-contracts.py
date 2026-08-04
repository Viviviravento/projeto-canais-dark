"""Prepare the narration manifest and approved-cost record for video 009."""

from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

import requests
from dotenv import load_dotenv


ROOT = Path(__file__).resolve().parents[3]
CHANNEL = ROOT / "operations" / "a-palavra-que-cuida"
SCRIPT = CHANNEL / "02_roteiros" / "video-009-roteiro-v1.md"
CITATIONS = CHANNEL / "02_roteiros" / "video-009-citacoes-acf-v1.json"
PERFORMANCE = CHANNEL / "02_roteiros" / "video-009-performance-v1.json"
PREFLIGHT = CHANNEL / "06_edicao" / "video-009" / "preflight-prosodia-v1.json"
QUOTE = CHANNEL / "06_edicao" / "video-009" / "custos" / "elevenlabs-v1.json"
ENV = ROOT / "tools" / "OpenMontage" / ".env"

FUNCTIONS = {
    "01": "Abrir pela sensação de ser resumida pelo pior capítulo da própria história.",
    "02": "Mostrar o pedido simples de Jesus e as barreiras reais atravessadas pela conversa.",
    "03": "Explicar a água viva sem prometer uma vida sem necessidades humanas.",
    "04": "Trabalhar verdade sem humilhação, especulação ou invasão de privacidade.",
    "05": "Conectar adoração em espírito e verdade à vida prática e ao cuidado responsável.",
    "06": "Contar a volta da samaritana à cidade como testemunho honesto, não discurso perfeito.",
    "07": "Mostrar a história transformada em ponte sem apagar o passado nem exigir perfeição.",
    "08": "Concluir com acolhimento, continuidade para outros vídeos e pergunta de comentário.",
}


def write(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def slug(value: str) -> str:
    normalized = value.casefold().translate(str.maketrans("áàâãéêíóôõúç", "aaaaeeiooouc"))
    return re.sub(r"[^a-z0-9]+", "-", normalized).strip("-")


def blocks() -> list[dict]:
    source = SCRIPT.read_text(encoding="utf-8")
    headings = list(re.finditer(r"^##\s+(\d+)\s+-\s+(.+)$", source, flags=re.MULTILINE))
    if len(headings) != 8:
        raise RuntimeError(f"Expected 8 script blocks, found {len(headings)}")
    output = []
    for index, heading in enumerate(headings):
        end = headings[index + 1].start() if index + 1 < len(headings) else len(source)
        number, title = heading.group(1), heading.group(2).strip()
        output.append({"id": f"{number}-{slug(title)}", "source_section": number, "title": title, "function": FUNCTIONS[number], "text": source[heading.end():end].strip()})
    return output


def subscription() -> dict:
    load_dotenv(ENV)
    response = requests.get("https://api.elevenlabs.io/v1/user/subscription", headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"]}, timeout=30)
    response.raise_for_status()
    payload = response.json()
    used, limit = payload.get("character_count"), payload.get("character_limit")
    return {"tier": payload.get("tier"), "character_count": used, "character_limit": limit, "credits_remaining_observed": limit - used, "checked_at": datetime.now(timezone.utc).isoformat()}


def main() -> None:
    narration_blocks = blocks()
    citations = json.loads(CITATIONS.read_text(encoding="utf-8"))
    narration = "\n\n".join(block["text"] for block in narration_blocks)
    characters = sum(len(block["text"]) for block in narration_blocks)
    maximum = ((characters + 999) // 1000) * 1000
    missing = [item["reference"] for item in citations["direct_acf_citations"] if item["spoken_lead_in"] not in narration or item["text"] not in narration]
    preflight = {"schema_version": "1.0.0", "video_id": "video-009", "status": "passed_pending_paid_audio_approval" if not missing and "<break" not in narration else "failed", "checks": {"blocks": len(narration_blocks), "total_characters": characters, "break_tags_found": "<break" in narration, "missing_direct_citations": missing, "cta_contains_next_video_direction": "vídeos sugeridos na tela" in narration_blocks[-1]["text"], "cta_contains_comment_prompt": "comentários" in narration_blocks[-1]["text"]}}
    performance = {"version": "video-009-performance-v1", "source_script": str(SCRIPT), "performance_contract": {"relationship": "Falar com quem teme ser reduzida ao passado ou a uma fase confusa.", "intensity": "Serena e acolhedora; elevar emoção apenas nas perguntas centrais, leituras bíblicas e pontos de vulnerabilidade.", "scripture": "Anunciar referência e mostrar o card ACF somente durante a leitura direta.", "pause_policy": "Sem tags, pausas artificiais ou pontuação para forçar interpretação.", "cta": "Pedir inscrição, curta e compartilhamento; conduzir a Pedro e Marta e Maria; concluir com pergunta de comentário."}, "api": {"provider": "ElevenLabs", "voice_name": "Bruno Cardoso", "voice_id": "iF2QszmZhlyFLleUoFxy", "model_id": "eleven_multilingual_v2", "language_code": "pt", "output_format": "mp3_44100_128", "seed": 314159, "voice_settings": {"stability": 0.5, "similarity_boost": 0.75, "style": 0.0, "speed": 1.0, "use_speaker_boost": True}, "postprocess": {"speed_factor": 1.07, "preserve_pitch": True}}, "blocks": narration_blocks}
    snapshot = subscription()
    quote = {"schema_version": "1.0.0", "quote_id": "v009-elevenlabs-v1-20260729", "provider": "ElevenLabs", "model": "eleven_multilingual_v2", "operation": "full eight-block narration for video-009 using one controlled sequential execution and 1.07x local postprocess", "unit": "provider credit", "quantity": characters, "expected_subscription_credits": characters, "maximum_subscription_credits": maximum, "currency": "USD", "expected_incremental_cash_charge": 0.0, "maximum_incremental_cash_charge": 0.0, "price_checked_at": snapshot["checked_at"], "price_source": "Authenticated ElevenLabs subscription API read-only check in this Codex session; no paid generation started.", "subscription_snapshot": snapshot, "status": "reserved_pending_user_approval", "approval": {"approved_at": None, "user_statement": None, "scope": f"Generate only video-009 narration up to {maximum} subscription credits, with no automatic retry and no incremental cash charge."}, "metadata": {"manifest": "operations/a-palavra-que-cuida/02_roteiros/video-009-performance-v1.json", "citation_manifest": "operations/a-palavra-que-cuida/02_roteiros/video-009-citacoes-acf-v1.json", "request_stitching": False, "context_mode": "independent_blocks", "automatic_retry": False, "postprocess_after_generation": "1.07x preserving pitch before master alignment"}}
    write(PERFORMANCE, performance)
    write(PREFLIGHT, preflight)
    write(QUOTE, quote)
    print(json.dumps({"characters": characters, "maximum_credits": maximum, "remaining": snapshot["credits_remaining_observed"], "preflight": preflight["status"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
