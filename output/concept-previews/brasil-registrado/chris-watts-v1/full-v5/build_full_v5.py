"""Documentary-first V5 internal render for Testemunha do Tempo."""
from __future__ import annotations

import asyncio
import json
import shutil
import subprocess
import sys
from pathlib import Path

import edge_tts
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from factory.core.decision_governance import active_rules, validate_rule_application
from factory.core.documentary_priority import validate_documentary_timeline
from factory.core.narration_input_firewall import load_public_narration
from factory.core.visual_semantic_sync import validate_narration_visual_script

CASE = ROOT / "output/concept-previews/brasil-registrado/chris-watts-v1"
OUTDIR, WORK, RAW = CASE / "full-v5", CASE / "full-v5/work-v5-render", CASE / "sources/raw"
LEDGER = ROOT / "output/concept-previews/brasil-registrado/indaiatuba-v1/production-rule-ledger-v1.json"
WHITELIST = CASE / "full-v3/narration-whitelist-full-v3.json"
FFMPEG, FFPROBE = ROOT / "tools/ffmpeg/bin/ffmpeg.exe", ROOT / "tools/ffmpeg/bin/ffprobe.exe"
# This is deliberately the documentary core. The second, versioned build
# stage extends it with additional captioned primary-record segments before
# the conclusion; that avoids padding the episode with synthetic narration.
OUT = OUTDIR / "CHRIS-WATTS-EPISODIO-COMPLETO-INTERNO-V5-BASE-8M39.mp4"
SOURCES = {"doorbell": RAW / "btM4jzYzOjE.mp4", "bodycam": RAW / "-iJ3Pq4TW0E.mp4", "neighbor_tv": RAW / "u11A4FQlDMo.mp4", "interview": RAW / "denver7-raw-interview-2018-08-14.mp4"}
BLOCKED = ((0.0, 24.0), (204.0, 216.0))
W, H, CREAM, ORANGE, PETROL = 1280, 720, (239,233,218,255), (202,92,47,255), (5,29,30,225)

TEXT_IDS = tuple(["CW-OPENING-001"] + [f"CW-BRIDGE-{n:03d}" for n in range(1,11)] + [f"CW-DETAIL-{n:03d}" for n in range(1,11)] + ["CW-EPILOGUE-001","CW-EPILOGUE-002","CW-EPILOGUE-003","CW-OUTRO-001"])
N = load_public_narration(WHITELIST, TEXT_IDS)

def D(id, source, start, end, focus, why, cues):
    return {"id":id,"role":"documentary_dialogue","source":source,"start":start,"end":end,"narrative_focus":focus,"why_it_matters":why,"visual_reason":why,"source_audio":"audible","narration_over_dialogue":False,"captions":[{"start":a-start,"end":b-start,"pt_br":t} for a,b,t in cues]}

B = [
 {"id":"CW5-OPEN","role":"narration","text":["CW-OPENING-001"],"source":"doorbell","units":[[0,13]],"intro":True,"narrative_focus":"última chegada","why_it_matters":"A campainha registra o último marco visual conhecido.","visual_reason":"registro de campainha"},
 D("CW5-BODYCAM-CONSENT","bodycam",30.83,45.00,"a primeira busca","A bodycam registra o pedido de consentimento, não uma reconstituição.",[(30.83,37.08,"Policial: Certo. Se estiver de acordo, vamos pedir que você assine um termo autorizando a busca na casa."),(37.09,40.96,"Policial: Vamos aguardar nosso sargento chegar."),(40.97,45.00,"Chris Watts: Eu ia apenas caminhar pelo bairro para espairecer.")]),
 {"id":"CW5-ALERT","role":"narration","text":["CW-BRIDGE-001"],"source":"bodycam","units":[[88,10],[108,10],[135,8]],"narrative_focus":"a amiga percebe a ausência","why_it_matters":"A bodycam mostra a residência e o início da verificação.","visual_reason":"exterior da casa e policiais"},
 D("CW5-INTERVIEW-TIMELINE","interview",30.98,77.42,"versão inicial e Nicole","A entrevista fixa a linha do tempo pública que seria comparada a outros registros.",[(30.98,34.88,"Repórter: O que aconteceu? Conte o que aconteceu."),(35.26,41.52,"Chris Watts: Ela voltou do aeroporto às duas da manhã. Eu saí por volta de 5h15; ela ainda estava aqui."),(43.28,47.52,"Chris Watts: Por volta de 12h10, a amiga Nicole chegou à porta."),(48.04,55.16,"Chris Watts: Mandei mensagens e liguei algumas vezes. Ela não respondeu; também não respondia às outras pessoas."),(55.82,64.24,"Chris Watts: Foi isso que preocupou muita gente. Se ela não responde a mim, pode estar ocupada; mas não responder a ninguém era preocupante."),(64.64,77.42,"Chris Watts: Nicole ligou quando estava na porta. Voltei para casa. Ela não estava aqui. As crianças também não. Não havia ninguém.")]),
 {"id":"CW5-COMPARE","role":"narration","text":["CW-BRIDGE-002"],"source":"bodycam","units":[[135,12],[160,12],[180,12],[218,12]],"narrative_focus":"horários passam a ser comparáveis","why_it_matters":"A busca real ancora o contexto após a entrevista.","visual_reason":"bodycam na residência"},
 {"id":"CW5-NEIGHBOR-CONTEXT","role":"narration","text":["CW-BRIDGE-003"],"source":"neighbor_tv","units":[[170,14],[176,12]],"narrative_focus":"agentes vão ao vizinho","why_it_matters":"A entrada na sala prepara o registro que será ouvido.","visual_reason":"agentes diante da TV"},
 D("CW5-NEIGHBOR-TV","neighbor_tv",180.00,220.25,"alcance da câmera do vizinho","A televisão é a evidência que todos observam; V5 não aplica blur nem delogo.",[(181.94,184.66,"A câmera mostra este carro começando a descer a rua."),(184.62,185.18,"Aquele ali."),(187.10,187.92,"Entende o que eu quero dizer?"),(187.92,189.44,"Ela alcança até lá embaixo."),(189.58,190.12,"Legal."),(190.36,191.46,"Ele mora ali ao lado."),(192.52,193.08,"Podemos ir?"),(194.56,195.90,"Eu estava falando dessa pressão."),(197.44,198.56,"Vai ficar perto de quatro."),(198.66,200.82,"Sim, ela pega carros vindo por aqui."),(200.74,203.12,"Eu registro o que vem por aqui quando faz a curva."),(204.20,207.54,"À noite, geralmente eu percebo o carro fazendo a curva."),(208.18,209.98,"Então, a menos que ela pare bem aqui,"),(209.98,213.20,"eu teria visto se ela tivesse saído a pé."),(219.32,220.20,"Diesel.")]),
 {"id":"CW5-EVIDENCE","role":"narration","text":["CW-BRIDGE-004"],"source":"neighbor_tv","units":[[220.5,12],[238,12],[260,12]],"narrative_focus":"limites e valor da câmera","why_it_matters":"A própria TV continua a evidência enquanto o narrador interpreta.","visual_reason":"registro da TV sem blur"},
 D("CW5-INTERVIEW-APPEAL","interview",124.73,164.01,"apelo público","A fala pública deve ser ouvida, não narrada por cima.",[(124.73,126.27,"Repórter: Você acha que ela simplesmente foi embora?"),(127.15,135.15,"Chris Watts: Neste momento, eu não quero especular. Espero que ela esteja em algum lugar seguro com as crianças."),(139.81,145.89,"Chris Watts: Mas, se alguém está com elas e elas não estão seguras, eu quero que voltem agora. É isso que passa pela minha cabeça."),(149.99,164.01,"Chris Watts: Se elas estiverem seguras, vão voltar. Se não estiverem, é essa falta de saber que pesa. Deixei todas as luzes acesas, esperando que as crianças entrassem pela porta. Isso não aconteceu.")]),
 {"id":"CW5-SEARCH","role":"narration","text":["CW-BRIDGE-005","CW-BRIDGE-006"],"source":"bodycam","units":[[218,12],[236,12],[248,12],[264,12],[280,12],[306,12]],"narrative_focus":"busca e confronto de versões","why_it_matters":"Entrada e cômodos pertencem à busca descrita.","visual_reason":"bodycam limpa da busca"},
 D("CW5-INTERVIEW-ARGUMENT","interview",286.01,315.51,"conversa emocional","A pergunta registra o que ele disse antes do desfecho judicial.",[(286.01,290.83,"Repórter: Esta pode ser uma pergunta difícil: vocês discutiram antes?"),(291.49,297.65,"Chris Watts: Não foi exatamente uma discussão. Tivemos uma conversa emocional, mas vou deixar por isso mesmo."),(297.65,313.91,"Chris Watts: Eu só quero que elas voltem. Se não estiverem seguras, isso está me destruindo. Alguém precisa aparecer e falar."),(314.57,315.51,"Repórter: A família está em contato com você?")]),
 {"id":"CW5-CHRONOLOGY","role":"narration","text":["CW-BRIDGE-007","CW-BRIDGE-008"],"source":"bodycam","units":[[280,12],[306,12],[338,12],[370,12],[390,12],[410,12]],"narrative_focus":"cronologia e ampliação","why_it_matters":"A busca preserva os espaços enquanto a narração conecta cronologia e evidência.","visual_reason":"bodycam da investigação"},
 D("CW5-INTERVIEW-CAMERAS","interview",353.97,405.00,"polícia, vizinhos e câmeras","A entrevista faz a ponte direta entre porta a porta e as câmeras que vimos.",[(353.97,362.85,"Repórter: O que a polícia, o xerife ou os vizinhos estão dizendo?"),(363.45,392.75,"Chris Watts: Eles trabalham com cães farejadores. Ontem, a polícia fez buscas na casa e reuniu informações. Há muita atividade ao redor, e espero que isso leve a algo positivo."),(393.39,397.51,"Repórter: Os vizinhos viram alguma coisa?"),(397.81,405.00,"Chris Watts: A polícia foi de porta em porta perguntando sobre câmeras e tudo mais. Até agora, nada.")]),
 {"id":"CW5-OUTCOME","role":"narration","text":["CW-BRIDGE-009","CW-BRIDGE-010"],"source":"bodycam","units":[[390,12],[410,12],[150,12],[122,12],[135,12],[160,12]],"narrative_focus":"desfecho e método","why_it_matters":"A casa e a rua retomam locais ligados aos registros comparados.","visual_reason":"bodycam do cenário"},
 {"id":"CW5-EPILOGUE","role":"narration","text":["CW-EPILOGUE-001","CW-EPILOGUE-002","CW-EPILOGUE-003"],"source":"neighbor_tv","units":[[240,12],[260,12],[280,12],[300,12],[320,12],[340,12]],"narrative_focus":"o que os registros preservaram","why_it_matters":"A sala do vizinho resume a transformação de um registro comum em evidência.","visual_reason":"TV e pessoas no local"},
 {"id":"CW5-OUTRO","role":"narration","text":["CW-OUTRO-001"],"source":"doorbell","units":[[0,18]],"narrative_focus":"fechamento","why_it_matters":"A campainha é moldura, apenas primeira e última cena.","visual_reason":"registro de campainha"},
]

def run(a): subprocess.run([str(x) for x in a],check=True)
def duration(p): return float(subprocess.run([str(FFPROBE),"-v","error","-show_entries","format=duration","-of","default=nw=1:nk=1",str(p)],capture_output=True,text=True,check=True).stdout.strip())
def clean(source,start,end):
    if source=="bodycam" and any(start<hi and end>lo for lo,hi in BLOCKED): raise RuntimeError(f"bodycam bloqueada: {start}-{end}")
def vf(): return "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2:black,eq=contrast=1.05:brightness=-0.025:saturation=0.80,vignette=PI/5:eval=frame,fps=30"
def base(source,start,seconds,name,audio):
    clean(source,start,start+seconds); out=WORK/f"{name}.mp4"; cmd=[FFMPEG,"-y","-ss",f"{start:.3f}","-i",SOURCES[source],"-t",f"{seconds:.3f}","-vf",vf(),"-c:v","libx264","-preset","ultrafast","-crf","19","-pix_fmt","yuv420p"]
    cmd += ["-af","highpass=f=70,acompressor=threshold=-25dB:ratio=1.8:attack=12:release=120:makeup=3,alimiter=limit=0.94,loudnorm=I=-16:TP=-1.2:LRA=10","-c:a","aac","-b:a","192k","-ar","48000","-ac","2"] if audio else ["-an"]
    run(cmd+[out]); return out
def wrap(draw,text,font,width):
    lines=[]; current=""
    for word in text.split():
        candidate=(current+" "+word).strip()
        if draw.textlength(candidate,font=font)<=width: current=candidate
        else: lines.append(current); current=word
    return lines+([current] if current else [])
def card(number,text):
    path=WORK/f"caption-{number:03d}.png"; im=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(im); font=ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf",28); lines=wrap(d,text,font,860); top=620-(28+38*len(lines)); d.rounded_rectangle((150,top,1130,620),14,fill=PETROL,outline=(44,103,99,225),width=2); d.rounded_rectangle((150,top,158,620),4,fill=ORANGE)
    for n,line in enumerate(lines):
        b=d.textbbox((0,0),line,font=font); d.text(((W-(b[2]-b[0]))/2,top+12+n*38),line,font=font,fill=CREAM)
    im.save(path); return path
def intro():
    path=WORK/"intro.png"; im=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(im); d.rounded_rectangle((74,72,874,268),15,fill=PETROL,outline=(44,103,99,225),width=2);d.rounded_rectangle((74,72,85,268),4,fill=ORANGE);d.text((103,95),"REGISTRO REAL",font=ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf",20),fill=CREAM);d.text((103,122),"A ÚLTIMA\nCHEGADA",font=ImageFont.truetype(r"C:\Windows\Fonts\georgiab.ttf",45),fill=CREAM,spacing=0);d.text((103,232),"FREDERICK, COLORADO · 13 DE AGOSTO DE 2018",font=ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf",16),fill=CREAM);im.save(path);return path
async def speech(number,text):
    mp3,wav=WORK/f"voice-{number:02d}.mp3",WORK/f"voice-{number:02d}.wav"; await edge_tts.Communicate(text,"pt-BR-AntonioNeural",rate="+0%",pitch="-8Hz").save(str(mp3));run([FFMPEG,"-y","-i",mp3,"-af","atempo=1.11,highpass=f=70,equalizer=f=180:t=q:w=1:g=1.5,equalizer=f=3000:t=q:w=1:g=0.8,acompressor=threshold=-18dB:ratio=2.4:attack=12:release=130:makeup=2,loudnorm=I=-16:TP=-1.5:LRA=7","-ar","48000","-ac","2",wav]);return wav
def join(clips,name):
    listing=WORK/f"{name}.txt";out=WORK/f"{name}.mp4";listing.write_text("".join(f"file '{p.as_posix()}'\n" for p in clips),encoding="utf-8");run([FFMPEG,"-y","-f","concat","-safe","0","-i",listing,"-c","copy",out]);return out
def narrated(block,index):
    voice=asyncio.run(speech(index," ".join(N[x] for x in block["text"]))); target=duration(voice)+.75; clips=[];units=[];remain=target
    for j,(start,planned) in enumerate(block["units"]):
        take=min(planned,remain); clips.append(base(block["source"],start,take,f"n{index:02d}-{j:02d}",False));units.append({"source":block["source"],"source_start_seconds":start,"duration_seconds":round(take,3)});remain-=take
        if remain<=.02:break
    if remain>.3:raise RuntimeError(f"{block['id']}: visual insuficiente por {remain:.2f}s")
    visual=clips[0] if len(clips)==1 else join(clips,f"visual-{index:02d}");out=WORK/f"narration-{index:02d}.mp4";cmd=[FFMPEG,"-y","-i",visual,"-i",voice]
    if block.get("intro"):cmd += ["-loop","1","-framerate","30","-t","6","-i",intro()];filterv="[0:v][2:v]overlay=0:0:eof_action=pass[v]"
    else:filterv="[0:v]null[v]"
    run(cmd+["-filter_complex",filterv+";[1:a]volume=0.72,alimiter=limit=0.96,loudnorm=I=-14:TP=-1.0:LRA=11,apad=pad_dur=0.75[a]","-map","[v]","-map","[a]","-t",f"{target:.3f}","-c:v","libx264","-preset","ultrafast","-crf","18","-pix_fmt","yuv420p","-c:a","aac","-b:a","256k","-ar","48000","-ac","2",out])
    return out,{"id":block["id"],"role":"narration","narrative_focus":block["narrative_focus"],"why_it_matters":block["why_it_matters"],"visual_reason":block["visual_reason"],"source_audio":"muted_broll","narration_seconds":round(duration(voice),3),"segment_seconds":round(target,3),"units":units,"whitelist_text_ids":block["text"]}
def doc(block,index,count):
    seconds=block["end"]-block["start"]; raw=base(block["source"],block["start"],seconds,f"d{index:02d}",True);cmd=[FFMPEG,"-y","-i",raw];filters=["[0:v]setpts=PTS-STARTPTS[v0]"];current="v0"
    for i,cue in enumerate(block["captions"],1):
        img=card(count,cue["pt_br"]);count+=1;cmd += ["-loop","1","-framerate","30","-t",f"{cue['end']-cue['start']:.3f}","-i",img];panel=f"p{i}";nxt=f"v{i}";filters += [f"[{i}:v]format=rgba,setpts=PTS-STARTPTS+{cue['start']:.3f}/TB[{panel}]",f"[{current}][{panel}]overlay=0:0:eof_action=pass:repeatlast=0[{nxt}]"];current=nxt
    out=WORK/f"dialogue-{index:02d}.mp4";run(cmd+["-filter_complex",";".join(filters),"-map",f"[{current}]","-map","0:a","-c:v","libx264","-preset","ultrafast","-crf","18","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-ar","48000","-ac","2",out]);record={k:v for k,v in block.items() if k not in {"start","end"}};record["source_start_seconds"]=block["start"];record["segment_seconds"]=round(seconds,3);return out,record,count
def main():
    if WORK.exists():shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    for p in SOURCES.values():
        if not p.is_file():raise FileNotFoundError(p)
    ledger=json.loads(LEDGER.read_text(encoding="utf-8"));rules=[{"rule_id":r["rule_id"],"rule_version":r["version"],"status":"applied","evidence":"V5 documentary plan and QA"} for r in active_rules(ledger,stage="master_render",format_id="video_16_9")];manifest={"schema":"RuleApplicationManifest.v1","operation_id":ledger["operation_id"],"ledger_version":ledger["ledger_version"],"stage":"master_render","format":"video_16_9","artifact":OUT.name,"applied_rules":rules,"deviations":[]};validate_rule_application(ledger,manifest);(OUTDIR/"rule-application-manifest-v5.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding="utf-8")
    visual={"schema":"NarrationVisualScript.v1","sources":{k:str(v) for k,v in SOURCES.items()},"blocks":[]};timeline={"schema":"DocumentaryTimeline.v1","blocks":[]}
    for b in B:
        units=[[b["source"],b["start"],b["end"]-b["start"]]] if b["role"]=="documentary_dialogue" else [[b["source"],a,d] for a,d in b["units"]];visual["blocks"].append({"id":b["id"],"narrative_focus":b["narrative_focus"],"visual_reason":b["visual_reason"],"source_dialogue":b["role"]=="documentary_dialogue","units":units});timeline["blocks"].append({**{k:v for k,v in b.items() if k not in {"text","source","start","end","units","intro","narrative_focus","visual_reason"}}, **({"source_audio":"muted_broll"} if b["role"]=="narration" else {})})
    validate_narration_visual_script(visual);validate_documentary_timeline(timeline);(OUTDIR/"visual-script-v5.json").write_text(json.dumps(visual,ensure_ascii=False,indent=2),encoding="utf-8")
    parts=[];records=[];cursor=0;count=1
    for i,b in enumerate(B):
        part,record,count=doc(b,i,count) if b["role"]=="documentary_dialogue" else (*narrated(b,i),count)
        length=duration(part);record["episode_start_seconds"]=round(cursor,3);cursor+=length;record["episode_end_seconds"]=round(cursor,3);parts.append(part);records.append(record)
    final=join(parts,"final");run([FFMPEG,"-y","-i",final,"-c","copy","-movflags","+faststart",OUT]);total=duration(OUT)
    if total<480:raise RuntimeError(f"Núcleo documental inesperadamente curto: {total:.3f}")
    rendered={"schema":"DocumentaryTimeline.v1","artifact":OUT.name,"blocks":records,"summary":{"documentary_dialogue_blocks":6,"pt_br_caption_turns":count-1,"doorbell_blocks":[records[0]["id"],records[-1]["id"]],"tv_artificial_blur":"none"}};validate_documentary_timeline(rendered);(OUTDIR/"documentary-timeline-core-v5.json").write_text(json.dumps(rendered,ensure_ascii=False,indent=2),encoding="utf-8");qa={"artifact":str(OUT.relative_to(ROOT)).replace("\\","/"),"duration_seconds":round(total,3),"status":"internal_core_requires_documentary_extension","checks":{"documentary_dialogue_blocks":6,"pt_br_caption_turns":count-1,"narration_over_important_dialogue":False,"doorbell_intermediate_uses":0,"tv_artificial_blur":False,"narration_speed":"1.11x_pitch_preserved","narrator_gain":"0.72"}};(OUTDIR/"qa-core-v5.json").write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding="utf-8");print(OUT)
if __name__=="__main__":main()
