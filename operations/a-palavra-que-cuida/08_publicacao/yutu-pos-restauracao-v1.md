# Yutu depois da restauracao da conta

Este arquivo registra os comandos reais ja confirmados no `yutu --help`. Nao executar antes da restauracao da conta Google e do OAuth.

Validacao: os comandos de canal, banner, playlist, video, thumbnail, legenda, comentario e marca-dagua passaram em `--dry-run` em 2026-07-21, sem autenticacao e sem envio.

## Carregar os pacotes

```powershell
$Root = "C:\Users\Vivia\OneDrive\Desktop\Projeto Canais Dark"
$Canal = Get-Content -LiteralPath "$Root\Canal Religioso\08_publicacao\configuracao-canal-v1.json" -Raw -Encoding UTF8 | ConvertFrom-Json
$Video001 = Get-Content -LiteralPath "$Root\Canal Religioso\08_publicacao\piloto-001-publicacao-v1.json" -Raw -Encoding UTF8 | ConvertFrom-Json
$Video002 = Get-Content -LiteralPath "$Root\Canal Religioso\08_publicacao\video-002-publicacao-v1.json" -Raw -Encoding UTF8 | ConvertFrom-Json
$ChannelId = "<ID_DO_CANAL>"
```

## Canal e banner

```powershell
yutu channel update --id $ChannelId --title $Canal.channel.public_name --description $Canal.channel.description --country BR --defaultLanguage pt-BR --output json --yes
yutu channelBanner insert --channelId $ChannelId --file "$Root\Canal Religioso\04_assets\branding\banner-youtube-v1.png" --output json --yes
```

O handle e a foto `Canal Religioso/Imagem Perfil Avatar.png` continuam no YouTube Studio. A API usada pelo yutu nao oferece essas duas alteracoes.

## Playlist

Criar primeiro como nao listada e guardar o ID devolvido:

```powershell
yutu playlist insert --channelId $ChannelId --title $Canal.initial_playlist.title --description $Canal.initial_playlist.description --language pt-BR --privacy unlisted --output json --yes
$PlaylistId = "<ID_DA_PLAYLIST>"
```

## Upload nao listado

Os valores booleanos abaixo evitam os defaults indesejados do yutu para estabilizacao, nivelamento e notificacao.

```powershell
yutu video insert --channelId $ChannelId --file "$Root\$($Video001.files.publication_master)" --title $Video001.title --description $Video001.description --categoryId 27 --privacy unlisted --tags ($Video001.tags -join ',') --thumbnail "$Root\$($Video001.files.thumbnail)" --language pt-BR --license youtube --containsSyntheticMedia=true --forKids=false --notifySubscribers=false --autoLevels=false --stabilize=false --embeddable=true --publicStatsViewable=true --playlistId $PlaylistId --output json --yes

yutu video insert --channelId $ChannelId --file "$Root\$($Video002.files.publication_master)" --title $Video002.title --description $Video002.description --categoryId 27 --privacy unlisted --tags ($Video002.tags -join ',') --thumbnail "$Root\$($Video002.files.thumbnail)" --language pt-BR --license youtube --containsSyntheticMedia=true --forKids=false --notifySubscribers=false --autoLevels=false --stabilize=false --embeddable=true --publicStatsViewable=true --playlistId $PlaylistId --output json --yes
```

Guardar os IDs devolvidos como `$Video001Id` e `$Video002Id`. Depois, enviar as legendas ja cronometradas:

```powershell
yutu caption insert --videoId $Video001Id --file "$Root\$($Video001.files.captions)" --language pt-BR --name "Português (Brasil)" --trackKind standard --isAutoSynced=false --isDraft=false --output json --yes
yutu caption insert --videoId $Video002Id --file "$Root\$($Video002.files.captions)" --language pt-BR --name "Português (Brasil)" --trackKind standard --isAutoSynced=false --isDraft=false --output json --yes
```

## Depois que os IDs existirem

1. Registrar IDs e URLs nos manifestos.
2. Gerar novamente as folhas `copiar-e-colar` com `exportar-textos-publicacao.py` para inserir os links cruzados.
3. Atualizar as descricoes com `yutu video update`.
4. Configurar manualmente tela final, foto, handle, pagina inicial e fixacao dos comentarios.
5. Revisar os dois videos nao listados antes de mudar a visibilidade.

O yutu publica comentarios, mas a API nao oferece o ato de fixa-los. O yutu tambem nao configura elementos de tela final.

## Marca-dagua

A imagem esta pronta, mas so deve ser ativada depois da revisao nao listada confirmar que ela nao compete com textos ou telas finais:

```powershell
yutu watermark set --channelId $ChannelId --file "$Root\Canal Religioso\04_assets\branding\marca-dagua-youtube-v1.png" --inVideoPosition bottomRight --offsetType offsetFromStart --offsetMs 30000 --yes
```
