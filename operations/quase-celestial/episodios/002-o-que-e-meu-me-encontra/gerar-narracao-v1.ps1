$ErrorActionPreference = 'Stop'

$episodio = $PSScriptRoot
$raizCanal = Split-Path -Parent (Split-Path -Parent $episodio)
$roteiro = Join-Path $episodio 'roteiro-v1.md'
$audioDir = Join-Path $episodio 'audio'
$perfilPronuncia = Join-Path $raizCanal 'calibracao-audio-001\pronuncia-marianne-v1.json'
$envPath = Join-Path (Split-Path -Parent $raizCanal) 'tools\OpenMontage\.env'

$linhaChave = Get-Content -Encoding utf8 $envPath | Where-Object { $_ -match '^ELEVENLABS_API_KEY=' } | Select-Object -First 1
$chave = ($linhaChave -replace '^ELEVENLABS_API_KEY=', '').Trim('"').Trim("'")
if (-not $chave) { throw 'ELEVENLABS_API_KEY nao encontrada.' }

$bruto = Get-Content -Raw -Encoding utf8 $roteiro
$falado = ($bruto -split '## Texto falado', 2)[1].Trim()
$perfil = Get-Content -Raw -Encoding utf8 $perfilPronuncia | ConvertFrom-Json
foreach ($entrada in $perfil.entries) { $falado = $falado.Replace($entrada.written, $entrada.render) }

$paragrafos = $falado -split '(?:\r?\n){2,}' | ForEach-Object { $_.Trim() } | Where-Object { $_ }
$partes = [System.Collections.Generic.List[string]]::new()
$atual = ''
foreach ($paragrafo in $paragrafos) {
    $candidato = if ($atual) { "$atual`n`n$paragrafo" } else { $paragrafo }
    if ($candidato.Length -gt 1400 -and $atual) { $partes.Add($atual); $atual = $paragrafo } else { $atual = $candidato }
}
if ($atual) { $partes.Add($atual) }

$headers = @{ 'xi-api-key' = $chave }
for ($i = 0; $i -lt $partes.Count; $i++) {
    $destino = Join-Path $audioDir ('narracao-seca-bloco-{0:D2}.mp3' -f ($i + 1))
    if (Test-Path -LiteralPath $destino) { continue }
    $corpo = @{
        text = $partes[$i]
        model_id = $perfil.model_id
        language_code = $perfil.language_code
        seed = $perfil.seed
        voice_settings = @{ stability = 0.5; similarity_boost = 0.75; style = 0; speed = $perfil.speed; use_speaker_boost = $true }
    } | ConvertTo-Json -Depth 5 -Compress
    Invoke-WebRequest -Uri ("https://api.elevenlabs.io/v1/text-to-speech/{0}?output_format=mp3_44100_192" -f $perfil.voice_id) -Method Post -Headers $headers -ContentType 'application/json' -Body ([System.Text.Encoding]::UTF8.GetBytes($corpo)) -OutFile $destino | Out-Null
    Write-Output ("Gerado bloco {0}/{1}: {2}" -f ($i + 1), $partes.Count, $destino)
}

$partesGeradas = Get-ChildItem -LiteralPath $audioDir -Filter 'narracao-seca-bloco-*.mp3' | Sort-Object Name
if ($partesGeradas.Count -ne $partes.Count) { throw 'Quantidade de blocos gerados nao confere.' }
$listaConcat = ($partesGeradas | ForEach-Object { $_.FullName -replace '\\','/' }) -join '|'
$master = Join-Path $audioDir 'narracao-seca-master-v1.mp3'
& ffmpeg -hide_banner -y -i ("concat:{0}" -f $listaConcat) -c copy $master
if ($LASTEXITCODE -ne 0) { throw 'Falha ao concatenar narracao.' }
Write-Output "Master criado: $master"
