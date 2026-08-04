$ErrorActionPreference = 'Stop'

$workspace = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $PSScriptRoot))
$envPath = Join-Path $workspace 'tools\OpenMontage\.env'
$keyLine = Get-Content -LiteralPath $envPath -Encoding utf8 |
    Where-Object { $_ -match '^ELEVENLABS_API_KEY=' } |
    Select-Object -First 1
$apiKey = ($keyLine -replace '^ELEVENLABS_API_KEY=', '').Trim('"').Trim("'")
if (-not $apiKey) { throw 'ELEVENLABS_API_KEY nao encontrada.' }

$jobs = @(
    @{ id = '001-nao-estou-atrasada'; output = 'narracao-seca-v2.mp3' },
    @{ id = '002-deixar-o-dia-ir'; output = 'narracao-seca-v2.mp3' },
    @{ id = '003-eu-me-permito-querer-mais'; output = 'narracao-seca-v2.mp3' }
)

foreach ($job in $jobs) {
    $dir = Join-Path $PSScriptRoot $job.id
    $scriptPath = Join-Path $dir 'roteiro.md'
    $outputPath = Join-Path $dir $job.output
    if (Test-Path -LiteralPath $outputPath) { throw "Arquivo ja existe: $outputPath" }

    $raw = Get-Content -LiteralPath $scriptPath -Raw -Encoding utf8
    $spoken = ($raw -split '## Texto falado', 2)[1] -split '## Caption inicial', 2 | Select-Object -First 1
    $spoken = $spoken.Trim()
    if (-not $spoken) { throw "Texto falado ausente: $scriptPath" }

    $body = @{
        text = $spoken
        model_id = 'eleven_v3'
        language_code = 'pt'
        seed = 170324
        voice_settings = @{
            stability = 0.5
            similarity_boost = 0.75
            style = 0
            use_speaker_boost = $true
        }
    } | ConvertTo-Json -Depth 5 -Compress

    $bytes = [System.Text.Encoding]::UTF8.GetBytes($body)
    Invoke-WebRequest `
        -Uri 'https://api.elevenlabs.io/v1/text-to-speech/iScHbNW8K33gNo3lGgbo?output_format=mp3_44100_192' `
        -Method Post `
        -Headers @{ 'xi-api-key' = $apiKey } `
        -ContentType 'application/json' `
        -Body $bytes `
        -OutFile $outputPath | Out-Null

    Write-Output ("Gerado {0}: {1} caracteres" -f $job.id, $spoken.Length)
}
