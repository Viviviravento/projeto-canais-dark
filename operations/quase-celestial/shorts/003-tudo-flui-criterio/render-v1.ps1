$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$master = Join-Path $root 'episodios\003-tudo-flui\export\master-003-tudo-flui-v1.mp4'
$ass = Join-Path $PSScriptRoot 'legendas.ass'
$saida = Join-Path $PSScriptRoot 'master-shorts-e-tiktok-003-paz-tambem-e-criterio-v1.mp4'
& ffmpeg -hide_banner -y -ss 356 -i $master -t 83.52 -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,ass='$($ass.Replace('\','/').Replace(':','\:'))'" -c:v libx264 -preset medium -crf 18 -c:a aac -b:a 192k -movflags +faststart $saida
if ($LASTEXITCODE -ne 0) { throw 'Falha ao renderizar o curto 2.' }
