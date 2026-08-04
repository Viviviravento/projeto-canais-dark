param(
    [Parameter(Mandatory = $true)]
    [ValidateRange(1, 9)]
    [int]$Bloco
)

$ErrorActionPreference = 'Stop'

$raiz = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$roteiro = Join-Path $PSScriptRoot 'roteiro-001-nova-era-v1.md'
$destino = Join-Path $PSScriptRoot ('calibracao-audio-001\\master-marianne-v3-bloco-{0:D2}.mp3' -f $Bloco)
$perfilPronuncia = Join-Path $PSScriptRoot 'calibracao-audio-001\\pronuncia-marianne-v1.json'
$envPath = Join-Path $raiz 'tools\\OpenMontage\\.env'

$linhaChave = Get-Content -Encoding utf8 $envPath |
    Where-Object { $_ -match '^ELEVENLABS_API_KEY=' } |
    Select-Object -First 1
$chave = ($linhaChave -replace '^ELEVENLABS_API_KEY=', '').Trim('"').Trim("'")
if (-not $chave) { throw 'ELEVENLABS_API_KEY nao encontrada.' }

$conteudo = Get-Content -Raw -Encoding utf8 $roteiro
$falado = ($conteudo -split '## Texto falado', 2)[1].Trim()
$perfil = Get-Content -Raw -Encoding utf8 $perfilPronuncia | ConvertFrom-Json
foreach ($entrada in $perfil.entries) {
    $falado = $falado.Replace($entrada.written, $entrada.render)
}
$paragrafos = $falado -split '(?:\r?\n){2,}' |
    ForEach-Object { $_.Trim() } |
    Where-Object { $_ }

$partes = [System.Collections.Generic.List[string]]::new()
$atual = ''
foreach ($paragrafo in $paragrafos) {
    $candidato = if ($atual) { "$atual`n`n$paragrafo" } else { $paragrafo }
    if ($candidato.Length -gt 1450 -and $atual) {
        $partes.Add($atual)
        $atual = $paragrafo
    } else {
        $atual = $candidato
    }
}
if ($atual) { $partes.Add($atual) }

if ($partes.Count -ne 9) { throw "Foram esperados 9 blocos, mas o roteiro gerou $($partes.Count)." }
if (Test-Path -LiteralPath $destino) { throw "O arquivo ja existe: $destino" }

$corpo = @{
    text = $partes[$Bloco - 1]
    model_id = $perfil.model_id
    language_code = $perfil.language_code
    seed = $perfil.seed
    voice_settings = @{
        stability = 0.5
        similarity_boost = 0.75
        style = 0
        speed = $perfil.speed
        use_speaker_boost = $true
    }
} | ConvertTo-Json -Depth 5 -Compress

$headers = @{ 'xi-api-key' = $chave }
$bytes = [System.Text.Encoding]::UTF8.GetBytes($corpo)
Invoke-WebRequest `
    -Uri ("https://api.elevenlabs.io/v1/text-to-speech/{0}?output_format=mp3_44100_192" -f $perfil.voice_id) `
    -Method Post `
    -Headers $headers `
    -ContentType 'application/json' `
    -Body $bytes `
    -OutFile $destino | Out-Null

Write-Output ("Gerado bloco {0}/9 ({1} caracteres): {2}" -f $Bloco, $partes[$Bloco - 1].Length, $destino)
