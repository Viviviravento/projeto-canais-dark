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
SCRIPT = CHANNEL / "02_roteiros" / "video-011-roteiro-v1.md"
CITATIONS = CHANNEL / "02_roteiros" / "video-011-citacoes-acf-v1.json"
PREFLIGHT = CHANNEL / "06_edicao" / "video-011" / "preflight-prosodia-v1.json"
QUOTE = CHANNEL / "06_edicao" / "video-011" / "custos" / "elevenlabs-v1.json"
ENV = ROOT / "tools" / "OpenMontage" / ".env"

FUNCTIONS = {
    "01": "Abrir pela identificação dupla de quem partiu e de quem ficou.",
    "02": "Mostrar a decisão do filho sem romantizar independência ou condenar todo afastamento.",
    "03": "Ler Lucas 15:17-20 e diferenciar responsabilidade de vergonha destrutiva.",
    "04": "Ler Lucas 15:22-24 e estabelecer limites contra reconciliação apressada ou insegura.",
    "05": "Dar voz à dor do irmão mais velho sem chamá-lo de vilão.",
    "06": "Ler Lucas 15:31-32 e mostrar que a compaixão alcança os dois filhos.",
    "07": "Aplicar retorno, perdão, ajuda e limites à vida real.",
    "08": "Concluir com acolhimento, CTA genérica de tela final e pergunta concreta.",
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
    citations = json.loads(CITATIONS.read_text(encoding="utf-8"))["direct_acf_citations"]
    narration = "\n\n".join(block["text"] for block in narration_blocks)
    characters = sum(len(block["text"]) for block in narration_blocks)
    maximum = ((characters + 999) // 1000) * 1000
    missing = [item["reference"] for item in citations if item["spoken_lead_in"] not in narration or item["text"] not in narration]
    specific_cta_words = ["assista ao vídeo sobre", "continue no vídeo sobre", "vídeo sobre Pedro", "vídeo sobre Marta", "vídeo sobre Maria"]
    specific_cta_found = [phrase for phrase in specific_cta_words if phrase.casefold() in narration.casefold()]
    preflight = {"schema_version": "1.0.0", "video_id": "video-011", "status": "passed_pending_paid_audio_approval" if not missing and not specific_cta_found and "<break" not in narration else "failed", "checks": {"blocks": len(narration_blocks), "total_characters": characters, "break_tags_found": "<break" in narration, "missing_direct_citations": missing, "specific_end_screen_cta_phrases": specific_cta_found, "cta_is_generic": not specific_cta_found, "cta_contains_next_video_direction": "vídeos exibidos na tela" in narration_blocks[-1]["text"], "cta_contains_comment_prompt": "comentários" in narration_blocks[-1]["text"]}}
    snapshot = subscription()
    quote = {"schema_version": "1.0.0", "quote_id": "v011-elevenlabs-v1-20260729", "provider": "ElevenLabs", "model": "eleven_multilingual_v2", "operation": "full eight-block narration for video-011 using one controlled sequential execution and 1.07x local postprocess", "unit": "provider credit", "quantity": characters, "expected_subscription_credits": characters, "maximum_subscription_credits": maximum, "currency": "USD", "expected_incremental_cash_charge": 0.0, "maximum_incremental_cash_charge": 0.0, "price_checked_at": snapshot["checked_at"], "price_source": "Authenticated ElevenLabs subscription API read-only check in this Codex session; no paid generation started.", "subscription_snapshot": snapshot, "status": "reserved_pending_user_approval", "approval": {"approved_at": None, "user_statement": None, "scope": f"Generate only video-011 narration up to {maximum} subscription credits, with no automatic retry and no incremental cash charge."}, "metadata": {"manifest": "operations/a-palavra-que-cuida/02_roteiros/video-011-performance-v1.json", "citation_manifest": "operations/a-palavra-que-cuida/02_roteiros/video-011-citacoes-acf-v1.json", "request_stitching": False, "context_mode": "independent_blocks", "automatic_retry": False, "postprocess_after_generation": "1.07x preserving pitch before master alignment"}}
    write(PREFLIGHT, preflight)
    write(QUOTE, quote)
    print(json.dumps({"characters": characters, "maximum_credits": maximum, "remaining": snapshot["credits_remaining_observed"], "preflight": preflight["status"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
