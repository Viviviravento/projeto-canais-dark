from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "06_edicao" / "video-003" / "scene-plan-v1.json"
CITATIONS = ROOT / "02_roteiros" / "video-003-citacoes-acf-v1.json"


def scene(block: str, cue: str, asset_id: str, source: str | None, mode: str, role: str, **extra: object) -> dict:
    return {
        "id": f"{block}-{asset_id}",
        "block": block,
        "narration_cue": cue,
        "asset_id": asset_id,
        "source": source,
        "mode": mode,
        "semantic_role": role,
        "maximum_continuous_seconds": 7 if mode not in {"avatar", "end_screen"} else (16 if mode == "avatar" else 15),
        "vertical_recomposition": "planned",
        **extra,
    }


def scripture_scene(block: str, citation: dict) -> dict:
    reference = citation["reference"]
    slug = reference.lower().replace("ó", "o").replace(" ", "-").replace(":", "-")
    return scene(
        block,
        citation["spoken_lead_in"],
        f"scripture-{slug}",
        None,
        "scripture_card",
        "Exibir integralmente a citação enquanto ela é lida.",
        scripture={
            "reference": reference,
            "text": citation["text"],
            "must_match_spoken_audio": True,
            "complete_reference_required": True,
        },
    )


def main() -> None:
    citations = json.loads(CITATIONS.read_text(encoding="utf-8"))["direct_acf_citations"]
    by_reference = {item["reference"]: item for item in citations}

    scenes = [
        scene("01", "Há momentos em que a vida parece quebrar", "b01-difficult-clinic-news-v1", "04_assets/video-003/generated/brazil/b01-difficult-clinic-news-v1.png", "local_motion", "Notícia difícil sem melodrama."),
        scene("01", "Uma perda. Uma injustiça.", "b02-job-loss-bakery-v1", "04_assets/video-003/generated/brazil/b02-job-loss-bakery-v1.png", "local_motion", "Perda de trabalho reconhecível no Brasil."),
        scene("01", "Uma porta fechada depois de anos", "b07-accompanied-bus-stop-v1", "04_assets/video-003/generated/brazil/b07-accompanied-bus-stop-v1.png", "local_motion", "Solidão urbana acompanhada."),
        scene("01", "Talvez você não tenha confiado o bastante", "avatar-v003-open", "planned:HeyGen Avatar IV from approved green-screen avatar", "avatar", "Apresentador confronta explicações precipitadas enquanto fala.", paid=True),
        scene("01", "O livro de Jó entra nesse lugar", "j02-job-after-loss-v1", "04_assets/video-003/generated/historical/j02-job-after-loss-v1.png", "local_motion", "Apresentar Jó depois da perda."),
        scene("01", "concluir o que essa pessoa fez", "b08-honest-lament-v1", "04_assets/video-003/generated/brazil/b08-honest-lament-v1.png", "local_motion", "Dor atual sem diagnóstico religioso."),

        scene("02", "O livro começa com um fato", "j01-job-before-loss-v1", "04_assets/video-003/generated/historical/j01-job-before-loss-v1.png", "local_motion", "Integridade antes da calamidade."),
        scripture_scene("02", by_reference["Jó 1:1"]),
        scene("02", "antes de perder bens", "j03-messengers-v1", "04_assets/video-003/generated/historical/j03-messengers-v1.png", "local_motion", "Notícias sucessivas sem espetáculo."),
        scene("02", "Eles enxergam apenas os escombros", "s01-barren-rock", "04_assets/video-003/stock/selected/s01-barren-rock.mp4", "stock_clip", "Paisagem concreta de perda e limite."),
        scene("02", "A dor não funciona como um exame", "b02-job-loss-bakery-v1-reframe", "04_assets/video-003/generated/brazil/b02-job-loss-bakery-v1.png", "local_motion", "Retorno intencional à perda de trabalho por outro enquadramento."),
        scene("02", "Nem todo luto é cobrança", "j02-job-after-loss-v1-reframe", "04_assets/video-003/generated/historical/j02-job-after-loss-v1.png", "local_motion", "Reforçar sem atribuir culpa."),

        scene("03", "Quando três amigos chegam", "j04-friends-arrive-kling", "planned:Kling O3 from j04-friends-arrive-v1.png", "generated_video", "Animar a chegada humana que carrega o argumento.", paid=True, generation_seconds=5),
        scripture_scene("03", by_reference["Jó 2:13"]),
        scene("03", "Sentam-se no chão", "j05-seven-days-silence-v1", "04_assets/video-003/generated/historical/j05-seven-days-silence-v1.png", "local_motion", "Presença silenciosa dos amigos."),
        scene("03", "É ficar, escutar", "b03-silent-presence-v1", "04_assets/video-003/generated/brazil/b03-silent-presence-v1.png", "local_motion", "Escuta atual e reconhecível."),
        scene("03", "preparar uma refeição", "b04-practical-meal-help-kling", "planned:Kling O3 from b04-practical-meal-help-v1.png", "generated_video", "Animar a entrega de comida, ação concreta e central.", paid=True, generation_seconds=5),
        scene("03", "Depois do silêncio, Jó fala", "j08-job-lament-night-v1", "04_assets/video-003/generated/historical/j08-job-lament-night-v1.png", "local_motion", "Transição da presença ao lamento."),
        scripture_scene("03", by_reference["Jó 3:1"]),

        scene("04", "abandonam a presença", "j06-friend-speaks-v1", "04_assets/video-003/generated/historical/j06-friend-speaks-v1.png", "local_motion", "Amigo passa a explicar e acusar."),
        scene("04", "usam a fórmula para questionar Jó", "j07-job-responds-v1", "04_assets/video-003/generated/historical/j07-job-responds-v1.png", "local_motion", "Jó responde à fórmula."),
        scripture_scene("04", by_reference["Jó 16:2"]),
        scene("04", "tudo acontece por uma razão", "j03-messengers-v1-reframe", "04_assets/video-003/generated/historical/j03-messengers-v1.png", "local_motion", "Retomar as notícias recebidas sem inventar uma causa para elas."),
        scene("04", "quem sofreu uma injustiça", "b05-legal-guidance-v1", "04_assets/video-003/generated/brazil/b05-legal-guidance-v1.png", "local_motion", "Escuta e orientação jurídica concreta."),
        scene("04", "pressa nasce do medo", "s02-strata-rock", "04_assets/video-003/stock/selected/s02-strata-rock.mp4", "stock_clip", "Figura humana pequena diante de terreno instável."),

        scene("05", "Deus responde a Jó de um redemoinho", "j09-whirlwind-v1", "04_assets/video-003/generated/historical/j09-whirlwind-v1.png", "local_motion", "Escala da resposta divina sem personificar Deus."),
        scene("05", "de um redemoinho", "s05-storm-sky", "04_assets/video-003/stock/selected/s05-storm-sky.mp4", "stock_clip", "Movimento real de nuvens para a transição."),
        scripture_scene("05", by_reference["Jó 38:2"]),
        scripture_scene("05", by_reference["Jó 38:4"]),
        scene("05", "a terra, o mar, a luz", "s03-sea-aerial", "04_assets/video-003/stock/selected/s03-sea-aerial.mp4", "stock_clip", "Escala do mar e da criação."),
        scene("05", "forças que nenhum ser humano governa", "s04-waves-rock", "04_assets/video-003/stock/selected/s04-waves-rock.mp4", "stock_clip", "Força natural concreta."),
        scene("05", "os animais", "s06-wild-goats", "04_assets/video-003/stock/selected/s06-wild-goats.mp4", "stock_clip", "Animalidade não controlada pelo ser humano."),

        scene("06", "Jó também é confrontado", "j07-job-responds-v1-reframe", "04_assets/video-003/generated/historical/j07-job-responds-v1.png", "local_motion", "Jó não é retratado como intocável."),
        scripture_scene("06", by_reference["Jó 42:7"]),
        scene("06", "Os amigos falaram muito sobre Deus", "j06-friend-speaks-v1-reframe", "04_assets/video-003/generated/historical/j06-friend-speaks-v1.png", "local_motion", "Fala religiosa não garante acerto."),
        scene("06", "sua vida foi restaurada", "j10-reconciliation-v1", "04_assets/video-003/generated/historical/j10-reconciliation-v1.png", "local_motion", "Restauração relacional sem tabela de prosperidade."),
        scene("06", "novas alegrias", "s03-sea-aerial-reframe", "04_assets/video-003/stock/selected/s03-sea-aerial.mp4", "stock_clip", "Respiro visual sem prometer compensação material."),

        scene("07", "Primeiro: não transforme dor", "b01-difficult-clinic-news-v1-third", "04_assets/video-003/generated/brazil/b01-difficult-clinic-news-v1.png", "local_motion", "Retomar a situação clínica para o primeiro critério."),
        scene("07", "Segundo: não apresse a lição", "b03-silent-presence-v1-third", "04_assets/video-003/generated/brazil/b03-silent-presence-v1.png", "local_motion", "Segundo critério em gesto de escuta."),
        scene("07", "escuta, comida", "b04-practical-meal-help-v1", "04_assets/video-003/generated/brazil/b04-practical-meal-help-v1.png", "local_motion", "Ajuda material."),
        scene("07", "transporte, companhia", "b07-accompanied-bus-stop-v1-reframe", "04_assets/video-003/generated/brazil/b07-accompanied-bus-stop-v1.png", "local_motion", "Acompanhamento prático."),
        scene("07", "ajuda profissional", "b06-psychological-support-v1", "04_assets/video-003/generated/brazil/b06-psychological-support-v1.png", "local_motion", "Apoio psicológico sem oposição à fé."),
        scene("07", "jurídico", "b05-legal-guidance-v1-reframe", "04_assets/video-003/generated/brazil/b05-legal-guidance-v1.png", "local_motion", "Apoio jurídico sem texto falso em primeiro plano."),
        scene("07", "Terceiro: permita que o lamento", "b08-honest-lament-v1-reframe", "04_assets/video-003/generated/brazil/b08-honest-lament-v1.png", "local_motion", "Oração honesta no cotidiano."),
        scene("07", "pode ser uma maneira de a fé ganhar mãos", "j10-reconciliation-v1-reframe", "04_assets/video-003/generated/historical/j10-reconciliation-v1.png", "local_motion", "Fechar a aplicação com cuidado e reconciliação, sem triunfalismo."),

        scene("08", "Jó não ensina que pessoas de fé", "j08-job-lament-night-v1-reframe", "04_assets/video-003/generated/historical/j08-job-lament-night-v1.png", "local_motion", "Lamento não equivale a abandono."),
        scene("08", "não deixá-la sozinha no chão", "j05-seven-days-silence-v1-reframe", "04_assets/video-003/generated/historical/j05-seven-days-silence-v1.png", "local_motion", "Retorno ao motivo central da presença."),
        scene("08", "Este é o canal A Palavra que Cuida", "avatar-v003-close", "planned:HeyGen Avatar IV from approved green-screen avatar", "avatar", "Apresentador fala o CTA e sustenta a identidade do canal.", paid=True),
        scene("08", "clique em um dos dois vídeos", "end-screen-v003", None, "end_screen", "Reservar dois destinos e inscrição sem elementos narrativos concorrentes.", recommendation_slots=2),
    ]

    counts: dict[str, int] = {}
    for item in scenes:
        base = str(item["asset_id"]).removesuffix("-reframe").removesuffix("-third")
        counts[base] = counts.get(base, 0) + 1

    payload = {
        "schema_version": "1.0.0",
        "video_id": "video-003",
        "timing_state": "relative_cues_pending_approved_audio_alignment",
        "visual_policy": {
            "maximum_static_seconds": 7,
            "maximum_base_asset_reuse": 2,
            "reuse_requires_new_crop_or_context": True,
            "paid_motion_must_center_human_action": True,
            "avatar_only_while_speaking": True,
            "scripture_display_must_match_spoken_quote": True,
            "end_screen_seconds": 15,
            "end_screen_recommendation_slots": 2,
        },
        "asset_summary": {
            "scene_slots": len(scenes),
            "generated_stills_available": 18,
            "stock_clips_reviewed": 6,
            "planned_paid_motion_clips": 2,
            "planned_avatar_clips": 2,
            "scripture_cards": len(citations),
        },
        "scenes": scenes,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{OUTPUT}: {len(scenes)} scene slots")


if __name__ == "__main__":
    main()
