from __future__ import annotations

import json
import math
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CHANNEL = ROOT / "operations" / "a-palavra-que-cuida"
PROJECT = ROOT / "tools" / "OpenMontage" / "projects" / "a-palavra-que-cuida-video-004"
PUBLIC = ROOT / "tools" / "OpenMontage" / "remotion-composer" / "public" / "video-004"
ALIGNMENT = CHANNEL / "05_audio" / "video-004" / "v1" / "master-alignment-1.05x.json"
SCENE_PLAN = CHANNEL / "06_edicao" / "video-004" / "scene-plan-v1.json"

BLOCK_ASSETS = {
    "01-a-pergunta-que-existe-entre-duas-cenas": ["historical/h05-casa-de-nazare-v1.png", "historical/h02-caminho-a-jerusalem-v1.png", "historical/h07-passos-de-peregrinos-v1.png"],
    "02-o-que-o-evangelho-mostra": ["historical/h01-jesus-no-templo-v1.png", "historical/h06-reflexao-domestica-v1.png"],
    "03-uma-familia-que-volta-todos-os-anos": ["historical/h02-caminho-a-jerusalem-v1.png", "historical/h07-passos-de-peregrinos-v1.png", "historical/h08-patio-do-templo-v1.png"],
    "04-o-menino-no-templo": ["historical/h03-procura-em-jerusalem-v1.png", "historical/h08-patio-do-templo-v1.png", "historical/h01-jesus-no-templo-v1.png", "historical/h09-escuta-e-perguntas-v1.png"],
    "05-uma-resposta-que-abre-o-centro": ["historical/h09-escuta-e-perguntas-v1.png", "historical/h06-reflexao-domestica-v1.png", "historical/h01-jesus-no-templo-v1.png"],
    "06-o-versiculo-que-impede-dois-erros": ["historical/h04-retorno-a-nazare-v1.png", "historical/h10-retorno-pelo-caminho-v1.png", "historical/h05-casa-de-nazare-v1.png"],
    "07-crescer-tambem-e-parte-da-historia": ["brazil/b01-escuta-em-familia-v1.png", "brazil/b02-aprender-com-constancia-v1.png", "brazil/b03-pedido-de-perdao-v1.png", "brazil/b04-crescimento-em-dias-comuns-v1.png", "brazil/b05-mesa-com-croche-v1.png", "brazil/b06-aprender-ouvindo-v1.png", "brazil/b07-responsabilidade-comum-v1.png", "brazil/b08-tempo-de-ouvir-v1.png"],
    "08-o-silencio-dos-anos": ["historical/h05-casa-de-nazare-v1.png", "historical/h06-reflexao-domestica-v1.png"],
    "09-fechamento-e-convite": ["brazil/b05-mesa-com-croche-v1.png", "brazil/b06-aprender-ouvindo-v1.png", "brazil/b08-tempo-de-ouvir-v1.png"],
}


def validate_b_roll_assets() -> None:
    if any(asset.startswith("editorial/") for assets in BLOCK_ASSETS.values() for asset in assets):
        raise RuntimeError("Editorial text assets require explicit narrative timestamps and cannot rotate as B-roll")


def copy_assets() -> None:
    for source, target in [
        (CHANNEL / "05_audio/video-004/v1/video-004-narracao-v1-1.05x-master.wav", PUBLIC / "audio/narracao-producao.wav"),
        (ROOT / "tools/OpenMontage/projects/a-palavra-que-cuida-video-003/public/music/classical-6-jonny-s-mixkit.mp3", PUBLIC / "music/classical-6-jonny-s-mixkit.mp3"),
    ]:
        target.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(source, target)
    for folder, source in [("historical", CHANNEL / "04_assets/video-004/generated/historical"), ("brazil", CHANNEL / "04_assets/video-004/generated/brazil")]:
        target = PUBLIC / "images" / folder; target.mkdir(parents=True, exist_ok=True)
        for image in source.glob("*.png"): shutil.copy2(image, target / image.name)


def captions(blocks: list[dict], card_ranges: list[tuple[float, float]]) -> list[dict]:
    result = []
    for block in blocks:
        text = "".join(block["characters"]); starts = block["character_start_times_seconds"]; ends = block["character_end_times_seconds"]
        words = [(m.group(), starts[m.start()], ends[m.end()-1]) for m in re.finditer(r"\S+", text)]
        group = []
        for word in words:
            group.append(word)
            phrase = " ".join(item[0] for item in group)
            ends_phrase = bool(re.search(r"[,.!?;:]$", word[0]))
            if len(group) < 2 or not (ends_phrase or len(group) >= 4 or len(phrase) >= 34):
                continue
            a, b = group[0][1], group[-1][2]
            if not any(a < card_end and b > card_start for card_start, card_end in card_ranges):
                result.append({"id": f"caption-{len(result)+1:04d}", "start": round(a,3), "end": round(b,3), "text": phrase})
            group = []
        if group:
            a, b = group[0][1], group[-1][2]
            if not any(a < card_end and b > card_start for card_start, card_end in card_ranges):
                result.append({"id": f"caption-{len(result)+1:04d}", "start": round(a,3), "end": round(b,3), "text": " ".join(item[0] for item in group)})
    for current, following in zip(result, result[1:]):
        current["end"] = round(min(current["end"], following["start"] - 0.01), 3)
    return result


def main() -> None:
    validate_b_roll_assets()
    PROJECT.mkdir(parents=True, exist_ok=True); copy_assets()
    for name in ["CompositionV2.tsx", "RootV2.tsx", "index-v2.tsx"]: shutil.copy2(ROOT / "tools/OpenMontage/projects/a-palavra-que-cuida-video-003" / name, PROJECT / name)
    composition = PROJECT / "CompositionV2.tsx"
    composition.write_text(
        composition.read_text(encoding="utf-8")
        .replace('staticFile("audio/narracao-producao.wav")', 'staticFile("video-004/audio/narracao-producao.wav")')
        .replace('staticFile("music/classical-6-jonny-s-mixkit.mp3")', 'staticFile("video-004/music/classical-6-jonny-s-mixkit.mp3")'),
        encoding="utf-8",
    )
    alignment = json.loads(ALIGNMENT.read_text(encoding="utf-8")); plan = json.loads(SCENE_PLAN.read_text(encoding="utf-8")); card_ranges = [(item["start_seconds"], item["end_seconds"]) for item in plan["scripture_cards"]]
    scenes=[]
    for block in alignment["blocks"]:
        choices=BLOCK_ASSETS[block["block_id"]]; start=float(block["start_seconds"]); end=float(block["end_seconds"]); count=math.ceil((end-start)/5.8)
        for index in range(count):
            a=round(start+(end-start)*index/count,3); b=round(start+(end-start)*(index+1)/count,3)
            scenes.append({"id":f"scene-{len(scenes)+1:03d}","start":a,"end":b,"asset":"video-004/images/"+choices[index%len(choices)],"media":"image","focus":["center","left center","right center"][index%3],"shade":0.04})
    for item in plan["scripture_cards"]:
        scenes.append({"id":item["id"],"start":item["start_seconds"],"end":item["end_seconds"],"asset":"video-004/images/scripture/"+Path(item["source"]).name,"media":"image","focus":"center","shade":0})
        target=PUBLIC/"images/scripture"; target.mkdir(parents=True,exist_ok=True); shutil.copy2(CHANNEL/item["source"],target/Path(item["source"]).name)
    scenes = [scene for scene in scenes if not scene["id"].startswith("scripture-")] + [scene for scene in scenes if scene["id"].startswith("scripture-")]
    timeline={"fps":30,"width":1920,"height":1080,"totalSeconds":707.391429,"endScreenStart":692.391429,"visualSourceTempo":1,"scenes":scenes,"specialScenes":[],"scriptures":[],"captions":captions(alignment["blocks"],card_ranges),"tags":[{"id":"title","variant":"title","start":.5,"end":8.2,"title":"A INFÂNCIA DE JESUS","subtitle":"o que a Bíblia realmente conta"},{"id":"limite","variant":"tag","start":60,"end":67,"title":"O TEXTO TEM LIMITES","subtitle":None},{"id":"templo","variant":"tag","start":240,"end":247,"title":"OUVIR E PERGUNTAR","subtitle":None},{"id":"crescer","variant":"tag","start":505,"end":512,"title":"CRESCER TAMBÉM IMPORTA","subtitle":None}]}
    timeline["tags"] = []
    (PROJECT/"timeline-v2.json").write_text(json.dumps(timeline,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"project":str(PROJECT),"scenes":len(scenes),"captions":len(timeline["captions"])},ensure_ascii=False))


if __name__ == "__main__": main()
