# Video 002 - Resultado de producao v2

Status: aprovado pelo usuario para publicacao, com dividas de qualidade registradas para os proximos videos.

Titulo oficial aprovado: `Nao andeis ansiosos: o que Jesus realmente quis dizer`.

## Arquivo entregue

- Master: `operations/a-palavra-que-cuida/07_exports/video-002/nao-andeis-ansiosos-v2.mp4`
- Duracao: `11:01.248`
- Resolucao: `1920x1080`
- Frame rate: `30 fps`
- Codec: H.264 + AAC estereo, 48 kHz
- Tamanho: `517.360.343 bytes` (`493,39 MiB`)
- SHA-256: `f0a74cf98076c19101ef3b1b9d5fa6315aded65519c8e7adf279cc2ca9f9c3fb`

## O que mudou

- A timeline foi reconstruida, sem reaproveitar a decupagem longa e repetitiva do v1.
- Sao 124 planos: 108 de imagem e 16 de video.
- As imagens estaticas duram em media `5,16 s`; nenhuma passa de `7,02 s`.
- Foram usados 32 ativos de imagem e 12 ativos de video distintos.
- Os unicos planos acima de 12 segundos sao os dois trechos em que o avatar esta falando.
- Entraram reconstrucoes visuais de Jesus ensinando, Sermao do Monte, aves, flores e cotidiano da Galileia.
- Cenas brasileiras aprovadas foram redistribuidas sem concentrar o episodio na mesma mulher e no mesmo ambiente.
- O orcamento antigo e o caderno vazio foram removidos.
- Os envelopes agora usam a imagem com `ALUGUEL`, `LUZ` e `MERCADO` fisicamente integrados.
- Textos-chave aparecem como grafismo editorial sincronizado, nunca achatados sobre papeis, rotulos ou telas.
- O avatar usa a fonte 16:9 com mesa continua.
- Depois da ultima fala do avatar, o quadro muda para um ambiente vazio; nao ha retrato estatico segurado.

## Sincronismo e encerramento

- Os textos-chave usam os tempos por caractere da narracao aprovada.
- `FATO OU PREVISAO?`: `09:00.154` narrativo / `539.852 s` do master.
- `ACAO OU CONTROLE?`: `556.919 s`.
- `HOJE OU AMANHA?`: `577.631 s`.
- A end screen visual entra no frame correspondente a `641,2 s`, exatamente 600 frames antes do fim.
- No container final, os ultimos 20 segundos comecam em aproximadamente `641,248 s`.
- A ultima fala termina em `657,984 s`; restam aproximadamente `3,264 s` de respiro e fade.

## QA local

- Loudness integrado: `-13,2 LUFS`.
- True peak: `-1,4 dBFS`.
- Intervalos pretos de 250 ms ou mais: `0`.
- Hash do render e do arquivo exportado: identicos.
- Contato visual final: `tools/OpenMontage/projects/a-palavra-que-cuida-video-002/snapshots/v2-final-contact.jpg`.
- Nenhuma nova chamada paga foi realizada na revisao v2. Imagens, videos e avatares ja existentes foram reutilizados.

## Observacao de esteira

Videos inseridos no Remotion aumentaram bastante o tempo de renderizacao 1080p, sobretudo stock e avatar. Para os proximos episodios, medir uma estrategia de proxy/intraframe ou montagem hibrida por FFmpeg antes de consolidar esse metodo como padrao.

## Consumo consolidado de ferramentas

- ElevenLabs: duas narracoes completas foram geradas. A v1 consumiu `4.404` creditos e a v2 consumiu `3.774`, segundo a variacao do contador da assinatura. Total debitado: `8.178` creditos. Foram produzidos `1.326,788 s` de audio bruto entre as duas versoes; somente os `658,193 s` da v2 entraram no master.
- HeyGen Avatar IV: dois videos concluidos, de `16,916 s` e `21,304 s`. Total animado: `38,220 s`; custo registrado no projeto: `US$ 1,911`. Uma tentativa preliminar falhou com custo registrado de `US$ 0,00`.
- Cadastro do novo Photo Avatar 16:9: o plano reservou conservadoramente `US$ 1,00`, mas o repositorio nao possui comprovante de transacao do provedor que permita tratar esse valor como debito confirmado.
- fal.ai / Kling O3 Standard: tres clipes sem audio, com `5 s` cada. Total gerado: `15 s`; custo registrado: `3 x US$ 0,42 = US$ 1,26`.
- Geracao de imagens integrada ao Codex: antes da thumbnail, o repositorio preservava `15` saidas atribuiveis ao episodio, sendo `14` imagens `img-v002-*` e uma nova fonte 16:9 do avatar. A thumbnail acrescentou mais uma saida, totalizando `16` arquivos identificaveis. Nao houve uso da chave fal.ai para essas imagens e o ambiente nao fornece custo monetario unitario da geracao integrada.
- Pexels: dois videos de stock, custo `US$ 0,00`. Pixabay nao foi usado neste episodio.
- Remotion e FFmpeg: montagem, remontagem, composicao, sincronizacao, normalizacao, render e compressao locais, sem custo externo por chamada.
- Total externo confirmado, sem atribuir preco aos creditos da assinatura ElevenLabs: `US$ 3,171` (`HeyGen + Kling`). Total conservador com a reserva nao confirmada do cadastro do avatar: `US$ 4,171`.

## Thumbnail

- Arquivo de publicacao: `operations/a-palavra-que-cuida/08_publicacao/video-002-thumbnail-v1.png`.
- Frase: `ANSIEDADE NAO E FALTA DE FE`, exibida na arte com os acentos corretos.
- Especificacao: `1280x720`, PNG, `1.279.389 bytes`.
- A composicao preserva o sistema visual do piloto 001: personagem brasileira a direita, Biblia aberta, ambiente claro e texto branco/amarelo com contorno azul-marinho.
- A imagem foi gerada pela ferramenta de imagem integrada ao Codex e redimensionada localmente para o arquivo de publicacao.

## Dividas aceitas somente neste video

- Alguns textos inseridos em cartas, correspondencias, rotulos ou outros objetos ainda parecem uma camada externa, em vez de impressao pertencente ao material. O usuario aceitou publicar o v2 assim para poupar creditos, mas o resultado nao vira referencia de qualidade.
- A citacao visual de Mateus 6:25 mostrou apenas o inicio do versiculo enquanto a narracao leu mais. Nos proximos videos, todo o texto biblico efetivamente lido precisa aparecer na tela, sem omissoes, junto da referencia completa.
- Algumas imagens retornam varias vezes ao longo do episodio. A repeticao foi tolerada porque o acervo atual ainda e pequeno; os proximos videos precisam ampliar o conjunto de ativos antes da montagem.
- A tela final deste video continua com uma unica opcao. A partir do proximo episodio, reservar dois espacos para videos e adicionar dois elementos nativos no YouTube.
