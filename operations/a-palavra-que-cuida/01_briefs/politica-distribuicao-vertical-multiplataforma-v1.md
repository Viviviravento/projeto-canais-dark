# Distribuição vertical multiplataforma v1

Data da decisão: 2026-07-23.

## Evidência

- O YouTube classifica vídeos verticais ou quadrados de até três minutos como Shorts. Shorts com mais de um minuto e reivindicação ativa do Content ID são bloqueados globalmente: https://support.google.com/youtube/answer/15424877?hl=pt-BR
- URLs em descrições e comentários de Shorts não são clicáveis. O recurso nativo de vídeo relacionado é clicável: https://support.google.com/youtube/answer/13748639
- O TikTok permite vincular uma conta do YouTube ao perfil: https://support.tiktok.com/en/getting-started/setting-up-your-profile/linking-another-social-media-account
- Para o Programa de Recompensas do Criador, o TikTok exige conteúdo original e de alta qualidade com mais de um minuto: https://support.tiktok.com/pt_BR/business-and-creator/creator-rewards-program/how-is-the-creator-rewards-program-different-from-the-tiktok-creator-fund
- Relatos recentes de criadores mostram que o mesmo vídeo pode ter resultados muito diferentes no TikTok e no Shorts. Isso é evidência prática de variabilidade, não prova de uma regra algorítmica universal: https://www.reddit.com/r/shortsAlgorithm/comments/1tfnro7/youtube_vs_tiktok_views/ e https://www.reddit.com/r/NewTubers/comments/1ksvrd1/

## Decisão operacional

As descrições e legendas de publicação seguem `politica-arquitetura-descricoes-multiplataforma-v1.md`; o mesmo núcleo semântico será adaptado por plataforma, não copiado integralmente.

- Shorts do YouTube e TikTok são destinos obrigatórios da fábrica de vídeos do canal.
- Produzir primeiro um master vertical limpo, 9:16, sem marca d'água de plataforma, com legenda literal incorporada e sem música proprietária de plataforma.
- Reutilizar o mesmo corpo quando gancho, ritmo, duração e sentido funcionarem nas duas plataformas. Isso economiza edição sem pressupor que os públicos sejam iguais.
- Criar acabamentos separados:
  - TikTok: CTA para o YouTube, legenda e hashtags próprias, link do YouTube no perfil e música escolhida dentro do TikTok quando fizer sentido.
  - YouTube Shorts: título e descrição próprios, vídeo longo associado pelo recurso nativo e CTA para tocar no vídeo relacionado. Não depender do URL da descrição.
- Não usar no Short acima de um minuto música que possa gerar reivindicação do Content ID.
- Medir TikTok e Shorts separadamente. Depois de três a cinco recortes comparáveis, decidir por evidência se algum deles precisa de ritmo, duração, gancho ou linguagem próprios.
- Se um mesmo master funcionar nos dois, preservar a economia. Se houver divergência repetida, produzir variantes específicas; não inferir equivalência de público.

## Legendas

- Legenda é transcrição literal da fala, não resumo, comentário ou segunda mensagem.
- Usar timestamps reais do áudio. Dividir apenas para legibilidade, sem alterar palavras, sentido ou ordem.
- Mensagem editorial adicional só pode aparecer quando não competir com a narração, como capa, silêncio inicial dedicado ou cartão final.
- Reprovar qualquer recorte que comece ou termine no meio de uma frase.
