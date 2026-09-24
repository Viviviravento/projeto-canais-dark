# QA dos curtos do vídeo 007

Data: 2026-07-29.

## Estado do vídeo longo e fontes

- O master longo do vídeo 007 não existe na pasta de exportação.
- `render-status-v1.json` permaneceu indevidamente como `running`, porém não havia processo ativo, log de render nem MP4 de saída no momento da verificação.
- Os curtos foram montados do master de narração 1,07x aprovado pela usuária, do alinhamento correspondente e das seis imagens canônicas do episódio.

## Recortes editoriais

- Curto 01: `Jesus não despreza a sua fraqueza`. Trabalha Hebreus 4:15 e conclui com uma oração honesta para momentos de vulnerabilidade.
- Curto 02: `Três perguntas antes de uma escolha urgente`. Oferece três perguntas concretas para não decidir apenas no impulso.
- Os dois começam e terminam em frases completas e funcionam como peças autônomas.

## Resultado técnico

- Formato: vertical real em 1080x1920, 30 fps.
- Codec: H.264 com áudio AAC estéreo em 48 kHz.
- Duração do curto 01: 84,567 s, com 80,546 s de fala.
- Duração do curto 02: 92,167 s, com 88,151 s de fala.
- Decodificação integral por FFmpeg: aprovada, sem erro.
- Segmentos pretos com duração igual ou superior a 0,5 s: nenhum.
- Primeiro quadro: imagem útil e não preta nos dois masters.
- Legendas: derivadas do alinhamento canônico e posicionadas na área segura vertical.

## Resultado visual

- Todas as imagens foram recompostas em `cover`; não existe quadro horizontal encaixado dentro da tela vertical.
- O curto 01 abre com Jesus inteiro e centralizado no deserto.
- O curto 02 abre com a personagem enquadrada em retrato coerente.
- Os pontos de foco de Jesus e da personagem na sala foram corrigidos depois do preflight para eliminar cortes laterais ruins.
- Não foi usada imagem de caderno aberto ou páginas em branco.
- O cartão de Hebreus 4:15 aparece somente durante a leitura direta do versículo.
- Telas finais: legíveis e com chamada para o vídeo completo no YouTube.

## Arquivos de verificação

- `assets-contact-sheet.png`
- `final-first-01.png`
- `master-01-contact.png`
- `master-02-contact.png`
- `master-01-end.png`
- `master-02-end.png`

## Integridade e custo

- Os hashes SHA-256 dos masters canônicos coincidem com os arquivos renderizados de origem.
- APIs pagas: US$ 0.
- A produção reutilizou áudio e imagens existentes e fez edição e renderização local.

Status: QA técnico e visual aprovado; aguardando revisão humana dos dois masters.
