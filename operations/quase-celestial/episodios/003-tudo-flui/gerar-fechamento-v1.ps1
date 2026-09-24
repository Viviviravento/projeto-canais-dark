$ErrorActionPreference = 'Stop'

$episodio = $PSScriptRoot
$raizCanal = Split-Path -Parent (Split-Path -Parent $episodio)
$audioDir = Join-Path $episodio 'audio'
$perfilPronuncia = Join-Path $raizCanal 'calibracao-audio-001\pronuncia-marianne-v1.json'
$envPath = Join-Path (Split-Path -Parent $raizCanal) 'tools\OpenMontage\.env'
$linhaChave = Get-Content -Encoding utf8 $envPath | Where-Object { $_ -match '^ELEVENLABS_API_KEY=' } | Select-Object -First 1
$chave = ($linhaChave -replace '^ELEVENLABS_API_KEY=', '').Trim('"').Trim("'")
if (-not $chave) { throw 'ELEVENLABS_API_KEY nao encontrada.' }

$texto = @'
Você não perdeu a chance de viver bem.

Não perdeu o momento de começar uma coisa nova.

Ainda existem manhãs que você não viveu, pessoas que você não conheceu e lugares onde o seu jeito vai fazer sentido.

Você não precisa arrancar tudo da vida de uma vez.

Pode receber aos poucos.

Pode aprender a reconhecer o que é bom quando ele aparece sem barulho.

Pode permitir que uma fase mais leve não seja interrompida pela culpa.

Por agora, não precisa apertar tanto o coração.

Não precisa decidir o resto da sua vida antes de descansar.

Pode deixar as respostas amadurecerem e continuar fazendo a sua parte com presença, honestidade e carinho por quem você é agora.

Que a sua vida encontre mais espaço.

Que seus planos encontrem caminhos possíveis.

Que o que for leve tenha permissão para ficar.

Você está se tornando alguém capaz de receber coisas boas sem pedir desculpa.

Agora, deixa os ombros baixarem.

Solta a testa.

Não existe uma versão perfeita que você precise alcançar antes de merecer paz.

Existe esta versão, aqui, aprendendo a caminhar com mais verdade.

Hoje, você não precisa correr.

Só precisa continuar voltando para a vida que quer construir.

Com calma.

Com coragem.

Com espaço para que tudo comece a fluir.
'@

$perfil = Get-Content -Raw -Encoding utf8 $perfilPronuncia | ConvertFrom-Json
foreach ($entrada in $perfil.entries) { $texto = $texto.Replace($entrada.written, $entrada.render) }
$corpo = @{ text = $texto.Trim(); model_id = $perfil.model_id; language_code = $perfil.language_code; seed = $perfil.seed; voice_settings = @{ stability = 0.5; similarity_boost = 0.75; style = 0; speed = $perfil.speed; use_speaker_boost = $true } } | ConvertTo-Json -Depth 5 -Compress
$destino = Join-Path $audioDir 'narracao-fechamento-v1.mp3'
Invoke-WebRequest -Uri ("https://api.elevenlabs.io/v1/text-to-speech/{0}?output_format=mp3_44100_192" -f $perfil.voice_id) -Method Post -Headers @{ 'xi-api-key' = $chave } -ContentType 'application/json' -Body ([System.Text.Encoding]::UTF8.GetBytes($corpo)) -OutFile $destino | Out-Null

$entradas = [System.Collections.Generic.List[string]]::new()
$rotulos = ''
$fontes = @((1..7 | ForEach-Object { Join-Path $audioDir ('narracao-seca-bloco-{0:D2}.mp3' -f $_) })) + $destino
for ($i = 0; $i -lt $fontes.Count; $i++) { $entradas.Add('-i'); $entradas.Add($fontes[$i]); $rotulos += "[${i}:a]" }
$master = Join-Path $audioDir 'narracao-seca-master-v2.mp3'
& ffmpeg -hide_banner -y @entradas -filter_complex ("${rotulos}concat=n=$($fontes.Count):v=0:a=1[a]") -map '[a]' -c:a libmp3lame -b:a 192k $master
if ($LASTEXITCODE -ne 0) { throw 'Falha ao criar master v2.' }
& ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 $master
