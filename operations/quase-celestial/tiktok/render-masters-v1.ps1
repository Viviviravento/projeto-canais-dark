$ErrorActionPreference = 'Continue'

function Get-DurationSeconds([string]$Path) {
    return [double](& ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 $Path)
}

$base = $PSScriptRoot
$jobs = @(
    @{ Id = '001-nao-estou-atrasada'; Frequencies = '174.61,220,261.63'; Animated = $true },
    @{ Id = '002-deixar-o-dia-ir'; Frequencies = '146.83,220,293.66'; Animated = $true },
    @{ Id = '003-eu-me-permito-querer-mais'; Frequencies = '196,246.94,293.66'; Animated = $false }
)

foreach ($job in $jobs) {
    $dir = Join-Path $base $job.Id
    $voice = Join-Path $dir 'narracao-seca-v2.mp3'
    $art = Join-Path $dir 'arte-master-v1.png'
    $ambience = Join-Path $dir 'ambiente-original-v1.wav'
    $masterAudio = Join-Path $dir 'master-audio-v1.mp3'
    $loop = Join-Path $dir 'loop-visual-v1.mp4'
    $master = Join-Path $dir ('master-tiktok-{0}-v1.mp4' -f $job.Id)
    if (Test-Path -LiteralPath $master) { throw "Arquivo ja existe: $master" }

    $duration = Get-DurationSeconds $voice
    $fadeStart = [math]::Max(0, $duration - 2)
    $invariant = [System.Globalization.CultureInfo]::InvariantCulture
    $durationText = $duration.ToString('0.###', $invariant)
    $fadeStartText = $fadeStart.ToString('0.###', $invariant)
    $freq = $job.Frequencies -split ','
    $source = "aevalsrc=0.008*sin(2*PI*$($freq[0])*t)+0.006*sin(2*PI*$($freq[1])*t)+0.004*sin(2*PI*$($freq[2])*t):s=44100:d=$durationText"
    & ffmpeg -y -f lavfi -i $source -af "lowpass=f=1500,afade=t=in:st=0:d=1.2,afade=t=out:st=${fadeStartText}:d=2" -c:a pcm_s16le $ambience 1>$null 2>$null
    if ($LASTEXITCODE -ne 0) { throw "Falha ao gerar ambiente: $($job.Id)" }
    & ffmpeg -y -i $voice -i $ambience -filter_complex "[0:a]aresample=44100,volume=1.0[voice];[1:a]volume=0.65,lowpass=f=1600[bed];[voice][bed]amix=inputs=2:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=7[a]" -map "[a]" -c:a libmp3lame -b:a 192k $masterAudio 1>$null 2>$null
    if ($LASTEXITCODE -ne 0) { throw "Falha ao mixar audio: $($job.Id)" }

    if ($job.Animated) {
        $motion = Join-Path $dir 'movimento-cenario-v1-seedance-5s.mp4'
        & ffmpeg -y -i $motion -filter_complex "[0:v]split=2[forward][back];[back]reverse[reverse];[forward][reverse]concat=n=2:v=1:a=0,format=yuv420p[v]" -map "[v]" -an -c:v libx264 -preset medium -crf 18 $loop 1>$null 2>$null
        if ($LASTEXITCODE -ne 0) { throw "Falha ao criar loop de movimento: $($job.Id)" }
    } else {
        & ffmpeg -y -loop 1 -i $art -vf "scale=1200:2134,zoompan=z='min(zoom+0.00008,1.03)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=300:s=1080x1920:fps=30,eq=brightness='0.015*sin(2*PI*t/5)':contrast=1.02,format=yuv420p" -t 10 -an -c:v libx264 -preset medium -crf 18 $loop 1>$null 2>$null
        if ($LASTEXITCODE -ne 0) { throw "Falha ao criar arte viva: $($job.Id)" }
    }

    & ffmpeg -y -stream_loop -1 -i $loop -i $masterAudio -t $duration -map 0:v -map 1:a -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,drawtext=fontfile='C\:/Windows/Fonts/gadugi.ttf':text='Quase Celestial':fontcolor=0xF8F5FF:fontsize=44:x=76:y=116:shadowcolor=0x10071C@0.70:shadowx=0:shadowy=2" -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart -shortest $master 1>$null 2>$null
    if ($LASTEXITCODE -ne 0) { throw "Falha ao renderizar master: $($job.Id)" }
    Write-Output ("Renderizado {0}: {1:N2}s" -f $job.Id, (Get-DurationSeconds $master))
}
