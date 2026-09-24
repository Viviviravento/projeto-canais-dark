# QA dos curtos do vídeo 006

Data: 2026-07-29.

## Fonte e recortes editoriais

- O master final do vídeo longo 006 ainda não estava exportado. Os curtos foram montados diretamente da narração canônica, do alinhamento aprovado e das imagens já selecionadas para o vídeo.
- Curto 01: `Jesus chama você pelo nome na ansiedade`. Usa a resposta de Jesus a Marta para mostrar ternura, ansiedade, dispersão e o retorno à presença.
- Curto 02: `Sobrecarga também precisa de ajuda real`. Distingue cuidado espiritual de exploração e aponta divisão de tarefas, descanso e conversa honesta.
- Os dois recortes começam e terminam em frases completas e funcionam sem depender do trecho anterior do vídeo longo.

## Resultado técnico

- Formato: vertical real em 1080x1920, 30 fps.
- Codec: H.264 com áudio AAC estéreo em 48 kHz.
- Duração do curto 01: 88,533 s, com 84,530 s de fala.
- Duração do curto 02: 88,300 s, com 84,276 s de fala.
- Decodificação integral por FFmpeg: aprovada, sem erro.
- Segmentos pretos com duração igual ou superior a 0,5 s: nenhum.
- Primeiro quadro: imagem útil e não preta nos dois masters.
- Legendas: derivadas do alinhamento canônico e posicionadas na área segura vertical.
- Primeira e última legendas: frases completas nos dois vídeos.

## Resultado visual

- As imagens foram recompostas em `cover`; não há vídeo horizontal encaixado dentro de uma tela vertical.
- Rostos e personagens foram centralizados com intenção editorial, usando retratos, troncos ou mãos em descanso quando o quadro completo não cabia.
- No plano com duas mulheres, cada enquadramento escolhe uma personagem de forma deliberada; não há meio corpo arbitrário na borda.
- Não foi usada nenhuma imagem de caderno aberto com páginas em branco.
- O cartão de Lucas 10:41 aparece somente durante a leitura direta do versículo no curto 01.
- Telas finais: legíveis e com chamada para o vídeo completo no YouTube.

## Arquivos de verificação

- `assets-contact-sheet.png`
- `vertical-contact-sheet-v3.png`
- `master-01-contact.png`
- `master-02-contact.png`
- `master-01-end.png`
- `master-02-end.png`

## Integridade e custo

- Os hashes SHA-256 dos masters canônicos coincidem com os arquivos renderizados de origem.
- APIs pagas: US$ 0.
- A produção reutilizou narração e imagens existentes e fez apenas edição e renderização local.

Status: QA técnico e visual aprovado; aguardando revisão humana dos dois masters.
