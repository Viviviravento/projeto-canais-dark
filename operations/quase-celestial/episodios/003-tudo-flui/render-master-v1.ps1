$ErrorActionPreference = 'Stop'
$episodio = $PSScriptRoot
$arte = Join-Path $episodio 'arte'
$audio = Join-Path $episodio 'audio'
$export = Join-Path $episodio 'export'

$voz = Join-Path $audio 'narracao-seca-master-v2.mp3'
$duracao = [double](& ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 $voz)
$metadeComDissolve = ($duracao + 1) / 2
$invariant = [System.Globalization.CultureInfo]::InvariantCulture
$duracaoText = $duracao.ToString('0.###', $invariant)
$metadeText = $metadeComDissolve.ToString('0.###', $invariant)
$offsetText = ($metadeComDissolve - 1).ToString('0.###', $invariant)

$cena1 = Join-Path $arte 'movimento-cena-v1-manha-verde-local.mp4'
$cena2 = Join-Path $arte 'movimento-cena-v2-litoral-turquesa-local.mp4'
$visual = Join-Path $arte 'master-visual-duas-cenas-v1.mp4'
$ambiente = Join-Path $audio 'ambiente-original-v1.wav'
$mix = Join-Path $audio 'master-audio-v1.mp3'
$master = Join-Path $export 'master-003-tudo-flui-v1.mp4'

# Movimento de câmera amplo e cíclico: revela os elementos de primeiro plano (galhos e capim)
# sem perder a quietude exigida pelo formato.
if (-not (Test-Path -LiteralPath $cena1)) {
    & ffmpeg -hide_banner -y -loop 1 -framerate 30 -i (Join-Path $arte 'arte-master-v1-manha-verde.png') -t $metadeText -vf "scale=w='1500+42*sin(2*PI*t/18)':h=-2:eval=frame,crop=1280:720:x='110+90*sin(2*PI*t/14)':y='62+25*sin(2*PI*t/9)',eq=brightness='0.018*sin(2*PI*t/7)':saturation=1.06:contrast=1.025,noise=alls=2:allf=t+u,format=yuv420p" -an -c:v libx264 -preset medium -crf 18 -r 30 $cena1
    if ($LASTEXITCODE -ne 0) { throw 'Falha ao renderizar a primeira cena.' }
}

if (-not (Test-Path -LiteralPath $cena2)) {
    & ffmpeg -hide_banner -y -loop 1 -framerate 30 -i (Join-Path $arte 'arte-master-v2-litoral-turquesa.png') -t $metadeText -vf "scale=w='1525+46*sin(2*PI*t/16+1)':h=-2:eval=frame,crop=1280:720:x='122-96*sin(2*PI*t/13)':y='64+30*sin(2*PI*t/8+1)',eq=brightness='0.020*sin(2*PI*t/6+1)':saturation=1.08:contrast=1.03,noise=alls=2:allf=t+u,format=yuv420p" -an -c:v libx264 -preset medium -crf 18 -r 30 $cena2
    if ($LASTEXITCODE -ne 0) { throw 'Falha ao renderizar a segunda cena.' }
}

if (-not (Test-Path -LiteralPath $visual)) {
    & ffmpeg -hide_banner -y -i $cena1 -i $cena2 -filter_complex "[0:v][1:v]xfade=transition=fade:duration=1:offset=$offsetText,format=yuv420p[v]" -map '[v]' -t $duracaoText -an -c:v libx264 -preset medium -crf 18 -movflags +faststart $visual
    if ($LASTEXITCODE -ne 0) { throw 'Falha ao unir as duas cenas.' }
}

# Cama harmônica original e discreta, sem eco ou segunda voz na abertura.
$fonte = "aevalsrc=0.007*sin(2*PI*174.61*t)+0.004*sin(2*PI*220*t)+0.003*sin(2*PI*261.63*t):s=44100:d=$duracaoText"
$fadeOut = ([math]::Max(0, ($duracao - 2))).ToString('0.###', $invariant)
& ffmpeg -hide_banner -y -f lavfi -i $fonte -af "lowpass=f=1450,afade=t=in:st=0:d=1.5,afade=t=out:st=${fadeOut}:d=2" -c:a pcm_s16le $ambiente
if ($LASTEXITCODE -ne 0) { throw 'Falha ao criar ambiente original.' }

& ffmpeg -hide_banner -y -i $voz -i $ambiente -filter_complex "[0:a]aresample=44100,volume=1.0[voz];[1:a]volume=0.52,lowpass=f=1500[cama];[voz][cama]amix=inputs=2:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=7[a]" -map '[a]' -c:a libmp3lame -b:a 192k $mix
if ($LASTEXITCODE -ne 0) { throw 'Falha ao mixar o audio.' }

& ffmpeg -hide_banner -y -i $visual -i $mix -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -movflags +faststart -shortest $master
if ($LASTEXITCODE -ne 0) { throw 'Falha ao renderizar o master final.' }

& ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 $master
