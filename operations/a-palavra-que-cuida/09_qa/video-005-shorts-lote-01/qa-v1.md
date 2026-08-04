# QA dos curtos do vídeo 005

Data: 2026-07-29.

## Recortes editoriais

- Curto 01: `Você não começa a ter valor quando produz muito`. Parte da leitura de Gênesis 1:27 e desenvolve a dignidade recebida antes de currículo, produtividade e aprovação.
- Curto 02: `Descansar não é falhar`. Usa o ritmo da criação para distinguir descanso de fracasso e de fuga da responsabilidade.
- Os dois recortes começam e terminam em frases completas e funcionam sem depender do trecho anterior do vídeo longo.

## Resultado técnico

- Formato: vertical real em 1080x1920, 30 fps.
- Codec: H.264 com áudio AAC estéreo em 48 kHz.
- Duração do curto 01: 80,300 s.
- Duração do curto 02: 74,767 s.
- Decodificação integral por FFmpeg: aprovada, sem erro.
- Segmentos pretos com duração igual ou superior a 0,5 s: nenhum.
- Primeiro quadro: imagem útil e não preta nos dois masters.
- Legendas: derivadas do alinhamento canônico da narração e posicionadas na área segura vertical.

## Resultado visual

- As imagens foram recompostas em `cover`; não há vídeo horizontal encaixado dentro de uma tela vertical.
- Personagens foram enquadrados por rosto ou tronco com sentido visual; não há personagem cortado ao meio por reutilização do quadro horizontal.
- O curto 02 abre com um plano de mãos em repouso para que o título não cubra o rosto de uma personagem.
- O curto 01 abre com um rosto centralizado e usa imagens de apoio coerentes com dignidade, acolhimento e autocuidado.
- Não foi usada nenhuma imagem de caderno aberto com páginas em branco.
- Cartão bíblico do curto 01 aparece somente durante a leitura direta de Gênesis 1:27.
- Tela final: legível, com chamada para o vídeo completo no YouTube.

## Arquivos de verificação

- `video-005-curto-01-contact.png`
- `video-005-curto-02-contact.png`
- `video-005-curto-01-first.png`
- `video-005-curto-02-first.png`
- `video-005-curto-01-endcard.png`
- `video-005-curto-02-endcard.png`

## Custo

- APIs pagas: US$ 0.
- A produção reutilizou narração e imagens existentes e fez apenas edição/renderização local.

Status: QA técnico e visual aprovado; aguardando revisão humana dos dois masters.
