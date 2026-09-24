"""Extend the failed 8m39 V5 only with captioned documentary interview clips.

The source render is preserved.  This inserts records before the closing
context and final doorbell, never narration used merely to reach duration.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[5]
OUTDIR = ROOT / "output/concept-previews/brasil-registrado/chris-watts-v1/full-v5"
SOURCE = ROOT / "output/concept-previews/brasil-registrado/chris-watts-v1/sources/raw/denver7-raw-interview-2018-08-14.mp4"
FFMPEG = ROOT / "tools/ffmpeg/bin/ffmpeg.exe"
FFPROBE = ROOT / "tools/ffmpeg/bin/ffprobe.exe"
BASE = OUTDIR / "CHRIS-WATTS-EPISODIO-COMPLETO-INTERNO-V5.mp4"
BACKUP = OUTDIR / "CHRIS-WATTS-EPISODIO-COMPLETO-INTERNO-V5-BASE-8M39.mp4"
WORK = OUTDIR / "duration-extension-work"
W, H = 1280, 720
CREAM, ORANGE, PETROL = (239,233,218,255), (202,92,47,255), (5,29,30,225)

EXTRAS = [
    (170.66, 220.92, [
        (170.66,172.04,"Repórter: Vou fazer uma pergunta difícil."),
        (172.40,173.46,"Repórter: Como é sua relação com as crianças?"),
        (173.90,178.56,"Chris Watts: As crianças são minha vida. Os sorrisos delas iluminam a minha vida."),
        (179.86,191.70,"Chris Watts: Na noite anterior, no horário do jantar, senti falta delas. Senti falta de dizer que precisavam comer."),
        (191.96,200.10,"Chris Watts: Senti falta de vê-las abraçadas nos sofás, vendo desenho."),
        (200.10,207.90,"Chris Watts: Isso estava me destruindo. Eu precisava daquilo naquela noite."),
        (208.20,220.92,"Chris Watts: Entrar nos quartos e saber que eu não ligaria as máquinas de ruído, nem o monitor, nem daria beijo de boa-noite..."),
    ]),
    (225.14,235.98, [
        (225.14,227.80,"Chris Watts: A noite anterior foi horrível. Eu não consegui suportar."),
        (228.98,235.98,"Chris Watts: Eu só quero que todos voltem para casa. Onde estiverem, voltem para casa."),
    ]),
    (249.97,264.73, [
        (249.97,252.05,"Repórter: Ela voltou no domingo à noite?"),
        (252.35,264.73,"Chris Watts: Sim. O voo atrasou. Era para ela chegar às 23h; chegou às 1h48 e foi dormir por volta das duas."),
    ]),
    (409.21,436.93, [
        (409.21,417.69,"Repórter: Se sua esposa puder ver isto, o que você gostaria de dizer a ela?"),
        (418.01,426.57,"Chris Watts: Shanann, Bella, Celeste, se vocês estiverem por aí, voltem. Se alguém estiver com elas, por favor, tragam-nas de volta."),
        (427.23,434.93,"Chris Watts: Eu preciso ver todos de novo. Esta casa não está completa sem ninguém aqui. Por favor, tragam-nas de volta."),
    ]),
]

def run(args: list[object]) -> None:
    subprocess.run([str(x) for x in args], check=True)

def seconds(path: Path) -> float:
    result = subprocess.run([str(FFPROBE),"-v","error","-show_entries","format=duration","-of","default=nw=1:nk=1",str(path)],capture_output=True,text=True,check=True)
    return float(result.stdout.strip())

def wrap(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, width: int) -> list[str]:
    lines, current = [], ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=font) <= width:
            current = trial
        else:
            lines.append(current); current = word
    return lines + ([current] if current else [])

def card(index: int, text: str) -> Path:
    target = WORK / f"caption-{index:03d}.png"
    image = Image.new("RGBA", (W,H), (0,0,0,0)); draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 28)
    lines = wrap(draw,text,font,860); top = 620 - (28 + 38 * len(lines))
    draw.rounded_rectangle((150,top,1130,620),14,fill=PETROL,outline=(44,103,99,225),width=2)
    draw.rounded_rectangle((150,top,158,620),4,fill=ORANGE)
    for row,line in enumerate(lines):
        box = draw.textbbox((0,0),line,font=font)
        draw.text(((W-(box[2]-box[0]))/2,top+12+row*38),line,font=font,fill=CREAM)
    image.save(target); return target

def make_record(index: int, start: float, end: float, cues: list[tuple[float,float,str]], number: int) -> tuple[Path,int]:
    duration = end-start; raw = WORK / f"raw-{index:02d}.mp4"
    run([FFMPEG,"-y","-ss",f"{start:.3f}","-i",SOURCE,"-t",f"{duration:.3f}","-vf","scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2:black,eq=contrast=1.05:brightness=-0.025:saturation=0.80,vignette=PI/5:eval=frame,fps=30","-af","highpass=f=70,acompressor=threshold=-25dB:ratio=1.8:attack=12:release=120:makeup=3,alimiter=limit=0.94,loudnorm=I=-16:TP=-1.2:LRA=10","-c:v","libx264","-preset","ultrafast","-crf","18","-pix_fmt","yuv420p","-c:a","aac","-ar","48000","-ac","2",raw])
    command: list[object] = [FFMPEG,"-y","-i",raw]; filters=["[0:v]setpts=PTS-STARTPTS[v0]"]; current="v0"
    for order,(cue_start,cue_end,text) in enumerate(cues,1):
        image=card(number,text); number += 1
        command += ["-loop","1","-framerate","30","-t",f"{cue_end-cue_start:.3f}","-i",image]
        panel,nxt=f"p{order}",f"v{order}"
        filters += [f"[{order}:v]format=rgba,setpts=PTS-STARTPTS+{cue_start-start:.3f}/TB[{panel}]",f"[{current}][{panel}]overlay=0:0:eof_action=pass:repeatlast=0[{nxt}]"]
        current=nxt
    result=WORK/f"record-{index:02d}.mp4"
    run(command+["-filter_complex",";".join(filters),"-map",f"[{current}]","-map","0:a","-c:v","libx264","-preset","ultrafast","-crf","18","-pix_fmt","yuv420p","-c:a","aac","-ar","48000","-ac","2",result])
    return result,number

def main() -> None:
    if WORK.exists():
        import shutil; shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    if not BACKUP.exists(): BASE.replace(BACKUP)
    # Before the V5 conclusion, so the doorbell remains the last scene.
    core_end = seconds(BACKUP) - 123.55
    head, tail = WORK / "head.mp4", WORK / "tail.mp4"
    run([FFMPEG,"-y","-i",BACKUP,"-t",f"{core_end:.3f}","-c","copy",head])
    run([FFMPEG,"-y","-ss",f"{core_end:.3f}","-i",BACKUP,"-c","copy",tail])
    parts=[head]; number=37
    for idx,(start,end,cues) in enumerate(EXTRAS):
        part,number=make_record(idx,start,end,cues,number); parts.append(part)
    parts.append(tail)
    listing=WORK/"concat.txt"; listing.write_text("".join(f"file '{p.as_posix()}'\n" for p in parts),encoding="utf-8")
    # Every source segment is normalized to 48 kHz before this stage.  Keep
    # the H.264 frames, but encode a single continuous AAC stream so concat
    # boundaries cannot carry incompatible audio headers into the master.
    run([FFMPEG,"-y","-f","concat","-safe","0","-i",listing,"-c:v","copy","-c:a","aac","-b:a","192k","-ar","48000","-ac","2","-movflags","+faststart",BASE])
    if seconds(BASE) < 600:
        raise RuntimeError(f"V5 estendida ainda abaixo do gate: {seconds(BASE):.3f}")
    print(BASE)

if __name__ == "__main__": main()
