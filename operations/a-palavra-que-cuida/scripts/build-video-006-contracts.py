from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests


PROJECT_ROOT = Path(__file__).resolve().parents[3]
CHANNEL_ROOT = PROJECT_ROOT / "operations" / "a-palavra-que-cuida"
OPENMONTAGE_ENV = PROJECT_ROOT / "tools" / "OpenMontage" / ".env"
SCRIPT_PATH = CHANNEL_ROOT / "02_roteiros" / "video-006-roteiro-v1.md"
CITATIONS_PATH = CHANNEL_ROOT / "02_roteiros" / "video-006-citacoes-acf-v1.json"
PERFORMANCE_PATH = CHANNEL_ROOT / "02_roteiros" / "video-006-performance-v1.json"
BLUEPRINT_PATH = CHANNEL_ROOT / "02_roteiros" / "video-006-blueprint-v1.json"
PREFLIGHT_PATH = CHANNEL_ROOT / "06_edicao" / "video-006" / "preflight-prosodia-v1.json"
QUOTE_PATH = CHANNEL_ROOT / "06_edicao" / "video-006" / "custos" / "elevenlabs-v1.json"


def load_env() -> None:
    for raw_line in OPENMONTAGE_ENV.read_text(encoding="utf-8-sig").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def write(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def slug(value: str) -> str:
    normalized = (
        value.casefold()
        .replace("ã", "a")
        .replace("á", "a")
        .replace("à", "a")
        .replace("â", "a")
        .replace("é", "e")
        .replace("ê", "e")
        .replace("í", "i")
        .replace("ó", "o")
        .replace("ô", "o")
        .replace("õ", "o")
        .replace("ú", "u")
        .replace("ç", "c")
    )
    return re.sub(r"[^a-z0-9]+", "-", normalized).strip("-")


def parse_blocks() -> list[dict[str, str]]:
    source = SCRIPT_PATH.read_text(encoding="utf-8")
    matches = list(re.finditer(r"^##\s+(\d+)\s+-\s+(.+)$", source, flags=re.MULTILINE))
    blocks: list[dict[str, str]] = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(source)
        number = match.group(1)
        title = match.group(2).strip()
        text = source[start:end].strip()
        blocks.append(
            {
                "id": f"{number}-{slug(title)}",
                "source_section": number,
                "title": title,
                "text": text,
            }
        )
    if len(blocks) != 9:
        raise RuntimeError(f"Expected 9 roteiro blocks, got {len(blocks)}")
    return blocks


def get_subscription_snapshot() -> dict[str, Any]:
    load_env()
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        return {"ok": False, "error": "ELEVENLABS_API_KEY not found"}
    response = requests.get(
        "https://api.elevenlabs.io/v1/user/subscription",
        headers={"xi-api-key": api_key},
        timeout=60,
    )
    payload = response.json() if response.content else {}
    response.raise_for_status()
    character_count = payload.get("character_count")
    character_limit = payload.get("character_limit")
    return {
        "ok": True,
        "tier": payload.get("tier"),
        "character_count": character_count,
        "character_limit": character_limit,
        "credits_remaining_observed": (
            character_limit - character_count
            if isinstance(character_limit, int) and isinstance(character_count, int)
            else None
        ),
        "next_character_count_reset_unix": payload.get("next_character_count_reset_unix"),
        "checked_at": datetime.now(timezone.utc).isoformat(),
    }


def main() -> None:
    blocks = parse_blocks()
    citations = json.loads(CITATIONS_PATH.read_text(encoding="utf-8"))
    performance_blocks = []
    functions = {
        "01": "Abrir a cena domestica e proteger Marta de uma leitura caricata.",
        "02": "Ler Lucas 10:39 e explicar Maria como discípula em escuta.",
        "03": "Ler Lucas 10:40 e mostrar quando serviço vira ansiedade e ressentimento.",
        "04": "Ler Lucas 10:41 e destacar a ternura da repetição do nome de Marta.",
        "05": "Ler Lucas 10:42 e explicar a boa parte sem negar responsabilidades concretas.",
        "06": "Ler João 11:5 para mostrar que Jesus amava Marta e não a descartou.",
        "07": "Aplicar a passagem à sobrecarga doméstica com responsabilidade prática.",
        "08": "Propor caminhos concretos para escolher a boa parte hoje.",
        "09": "Concluir, pedir inscrição, direcionar próximos vídeos e provocar comentário.",
    }
    for block in blocks:
        performance_blocks.append(
            {
                "id": block["id"],
                "source_section": block["source_section"],
                "title": block["title"],
                "function": functions[block["source_section"]],
                "text": block["text"],
            }
        )

    total_characters = sum(len(block["text"]) for block in performance_blocks)
    spoken_characters = sum(len(re.sub(r"\s+", " ", block["text"]).strip()) for block in performance_blocks)
    subscription = get_subscription_snapshot()
    maximum_credits = ((total_characters + 999) // 1000) * 1000
    if maximum_credits < total_characters:
        maximum_credits = total_characters

    performance = {
        "version": "video-006-performance-v1",
        "source_script": str(SCRIPT_PATH),
        "performance_contract": {
            "relationship": "Falar com uma pessoa cansada de servir, mas que não quer abandonar o cuidado.",
            "authority": "Autoridade pelo cuidado com Lucas 10, sem transformar Marta em vilã nem Maria em álibi para irresponsabilidade.",
            "interpretation": "Distinguir serviço, ansiedade, escuta, sobrecarga real, presença de Jesus e limites saudáveis.",
            "intensity": "Íntimo, doméstico, acolhedor e firme. Evitar tom acusatório com quem está sobrecarregado.",
            "scripture": "Anunciar livro, capítulo e versículo; ler somente quando a citação direta começar; cards bíblicos apenas durante a leitura real.",
            "pause_policy": "Sem break tags e sem pontuação artificial para induzir pausas. Frases mais curtas para reduzir vírgulas faladas de modo estranho.",
            "cta": "Concluir a mensagem, pedir inscrição/curtida/compartilhamento, apontar para dois próximos vídeos e terminar com pergunta de comentário.",
        },
        "api": {
            "provider": "ElevenLabs",
            "voice_name": "Bruno Cardoso",
            "voice_id": "iF2QszmZhlyFLleUoFxy",
            "model_id": "eleven_multilingual_v2",
            "language_code": "pt",
            "output_format": "mp3_44100_128",
            "seed": 314159,
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75,
                "style": 0.0,
                "speed": 1.0,
                "use_speaker_boost": True,
            },
            "postprocess": {
                "speed_factor": 1.05,
                "preserve_pitch": True,
            },
        },
        "blocks": performance_blocks,
    }
    write(PERFORMANCE_PATH, performance)

    blueprint = {
        "schema_version": "1.0.0",
        "video_id": "video-006",
        "title": "Marta e Maria: quando servir vira ansiedade",
        "primary_text": "Lucas 10:38-42",
        "supporting_text": "João 11:5",
        "promise": "Mostrar que Jesus não despreza o serviço de Marta, mas confronta a ansiedade que sequestra a presença.",
        "audience_moment": "Pessoas que cuidam de tudo, carregam a casa, trabalham demais e sentem culpa quando param.",
        "visual_direction": {
            "core": "Casa brasileira, mesa, Bíblia, cozinha, cansaço, escuta e presença.",
            "human_preference": "Mais mulheres brasileiras/latinas, com presença real e natural.",
            "crochet_detail": "Incluir uma peça de crochê sutil uma vez, como trilho de mesa ou apoio de xícara.",
            "avoid": [
                "Marta caricata como vilã",
                "Maria como pessoa preguiçosa",
                "texto editorial fora de citações bíblicas",
                "anjos ou sobrenatural não narrado"
            ]
        },
        "short_candidates": [
            {
                "id": "v006-short-01",
                "hook": "Servir pode virar ansiedade?",
                "source_blocks": ["03-quando-o-servico-perde-o-centro", "04-jesus-chama-pelo-nome"],
                "angle": "Quando fazer algo bom começa a adoecer o coração."
            },
            {
                "id": "v006-short-02",
                "hook": "Jesus não descartou Marta",
                "source_blocks": ["06-jesus-amava-marta"],
                "angle": "Correção de Jesus sem vergonha destrutiva."
            }
        ],
        "publication_bridge": {
            "end_screen_targets": ["video-002", "video-004"],
            "comment_prompt": "Hoje você se identifica mais com Marta, com Maria, ou com a tentativa difícil de servir sem perder a presença de Jesus?"
        }
    }
    write(BLUEPRINT_PATH, blueprint)

    missing_citations = []
    all_text = "\n\n".join(block["text"] for block in performance_blocks)
    for citation in citations["direct_acf_citations"]:
        if citation["spoken_lead_in"] not in all_text or citation["text"] not in all_text:
            missing_citations.append(citation["reference"])
    preflight = {
        "schema_version": "1.0.0",
        "video_id": "video-006",
        "status": "passed_pending_paid_audio_approval" if not missing_citations else "failed",
        "checks": {
            "blocks": len(performance_blocks),
            "total_characters": total_characters,
            "spoken_characters": spoken_characters,
            "break_tags_found": "<break" in all_text,
            "missing_direct_citations": missing_citations,
            "scripture_cards_policy": citations["display_policy"],
            "cta_contains_next_video_direction": "vídeos sugeridos na tela" in all_text,
            "cta_contains_comment_prompt": "comentários" in performance_blocks[-1]["text"],
        },
        "known_risk": "Ainda pode haver pausas naturais interpretadas como vírgula pela voz; roteiro usa frases mais curtas e sem break tags para reduzir o risco.",
    }
    write(PREFLIGHT_PATH, preflight)

    quote = {
        "schema_version": "1.0.0",
        "quote_id": "v006-elevenlabs-v1-20260728",
        "provider": "ElevenLabs",
        "model": "eleven_multilingual_v2",
        "operation": "full nine-block narration for video-006 using independent requests and 1.05x local postprocess",
        "unit": "provider credit",
        "quantity": total_characters,
        "expected_subscription_credits": total_characters,
        "maximum_subscription_credits": maximum_credits,
        "currency": "USD",
        "expected_incremental_cash_charge": 0.0,
        "maximum_incremental_cash_charge": 0.0,
        "price_checked_at": subscription.get("checked_at"),
        "price_source": "Authenticated ElevenLabs subscription API read-only check in this Codex session; no paid generation started.",
        "subscription_snapshot": subscription,
        "status": "reserved_pending_user_approval",
        "approval": {
            "approved_at": None,
            "user_statement": None,
            "scope": f"Generate only the full narration for video-006 up to {maximum_credits} subscription credits. No automatic retry and no incremental cash charge.",
        },
        "metadata": {
            "manifest": "operations/a-palavra-que-cuida/02_roteiros/video-006-performance-v1.json",
            "citation_manifest": "operations/a-palavra-que-cuida/02_roteiros/video-006-citacoes-acf-v1.json",
            "request_stitching": False,
            "context_mode": "independent_blocks",
            "automatic_retry": False,
            "postprocess_after_generation": "1.05x preserving pitch before master alignment",
        },
    }
    write(QUOTE_PATH, quote)
    print(
        json.dumps(
            {
                "performance": str(PERFORMANCE_PATH),
                "blueprint": str(BLUEPRINT_PATH),
                "preflight": str(PREFLIGHT_PATH),
                "quote": str(QUOTE_PATH),
                "blocks": len(performance_blocks),
                "characters": total_characters,
                "maximum_credits": maximum_credits,
                "subscription_ok": subscription.get("ok"),
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
