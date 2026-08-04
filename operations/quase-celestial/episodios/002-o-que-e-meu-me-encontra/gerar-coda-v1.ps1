$ErrorActionPreference = 'Stop'
$episodio = $PSScriptRoot
$raizCanal = Split-Path -Parent (Split-Path -Parent $episodio)
$envPath = Join-Path (Split-Path -Parent $raizCanal) 'tools\OpenMontage\.env'
$perfilPath = Join-Path $raizCanal 'calibracao-audio-001\pronuncia-marianne-v1.json'
$codaPath = Join-Path $episodio 'audio\coda-v1.txt'
$texto = [string](Get-Content -Raw -Encoding utf8 -LiteralPath $codaPath)
$perfil = Get-Content -Raw -Encoding utf8 $perfilPath | ConvertFrom-Json
$chaveLinha = Get-Content -Encoding utf8 $envPath | Where-Object { $_ -match '^ELEVENLABS_API_KEY=' } | Select-Object -First 1
$chave = ($chaveLinha -replace '^ELEVENLABS_API_KEY=', '').Trim('"').Trim("'")
$destino = Join-Path $episodio 'audio\narracao-seca-coda-v1.mp3'
if (Test-Path -LiteralPath $destino) { Write-Output "Coda existente: $destino"; exit 0 }
$corpo = @{ text=$texto; model_id=$perfil.model_id; language_code=$perfil.language_code; seed=$perfil.seed; voice_settings=@{ stability=0.5; similarity_boost=0.75; style=0; speed=$perfil.speed; use_speaker_boost=$true } } | ConvertTo-Json -Depth 5 -Compress
Invoke-WebRequest -Uri ("https://api.elevenlabs.io/v1/text-to-speech/{0}?output_format=mp3_44100_192" -f $perfil.voice_id) -Method Post -Headers @{ 'xi-api-key'=$chave } -ContentType 'application/json' -Body ([System.Text.Encoding]::UTF8.GetBytes($corpo)) -OutFile $destino | Out-Null
& ffmpeg -hide_banner -y -i (Join-Path $episodio 'audio\narracao-seca-master-v1.mp3') -i $destino -filter_complex '[0:a][1:a]concat=n=2:v=0:a=1[a]' -map '[a]' -c:a libmp3lame -b:a 192k (Join-Path $episodio 'audio\narracao-seca-master-v2.mp3')
if ($LASTEXITCODE -ne 0) { throw 'Falha ao montar master final.' }
