# Politica de Legendas e TikTok v1

## Decisao

Todo video de A Palavra Que Cuida deve sair com legendas revisadas. Isso vale para YouTube e TikTok e passa a fazer parte da definicao de pronto.

O papel principal do TikTok e descobrir novas pessoas e conduzir parte delas a videos especificos de A Palavra Que Cuida no YouTube. A monetizacao direta no TikTok permanece objetivo secundario. A estrategia de ponte, os CTAs e as metricas ficam em `estrategia-aquisicao-tiktok-youtube-v1.md`.

## Fonte canonica

Cada episodio tera uma unica fonte de sincronizacao, criada a partir do audio aprovado:

- transcricao final identica a fala;
- marcacao de tempo por frase ou segmento;
- pontuacao e acentuacao revisadas;
- identificacao da citacao biblica completa;
- indicacao breve de sons relevantes para compreender a cena, como `[musica suave]` ou `[batida na porta]`;
- nenhuma sobreposicao entre legendas.

Essa fonte gera duas saidas sem regenerar voz:

1. `subtitles-master.srt`, para o YouTube;
2. legendas incorporadas na composicao vertical do TikTok.

## YouTube horizontal

- Formato principal: `16:9`.
- Entregar `.srt` em portugues do Brasil (`pt-BR`).
- A legenda fechada nao substitui textos editoriais importantes.
- Quando houver leitura biblica, o texto visual deve mostrar livro, capitulo e versiculo completos e acompanhar integralmente o trecho falado, mesmo que dividido em blocos.
- Frases editoriais sobrepostas devem ser usadas apenas quando agregarem sentido; nao devem duplicar a legenda inteira.

### Regra de sincronizacao de texto

- Mencionar um livro, personagem ou capitulo nao autoriza exibir uma carta biblica completa.
- A carta com livro, capitulo, versiculo e texto ACF entra somente no intervalo exato da leitura direta daquele trecho e sai quando a leitura termina.
- No master horizontal, nao usar placas editoriais, titulo de abertura ou frases de apoio sobre as imagens. Fora da carta biblica, o texto visual e somente a legenda sincronizada; a tela final de recomendacoes e excecao estrutural da plataforma.
- Legendas sao a transcricao sincronizada; elas nao podem competir com a carta biblica, que ocupa a tela apenas durante a leitura direta.
- O QA humano deve conferir inicio, meio e fim do master ouvindo a fala e lendo a tela. Qualquer texto que apareca sem ancora narrativa explicita reprova o render.

### Tela final horizontal

- O master termina limpo, sem quadrados, molduras ou marcacoes que reservem posições para elementos clicáveis do YouTube.
- A marca do canal e o handle ativo `@apalavraquecuidabr` permanecem centralizados horizontalmente no encerramento.
- A quantidade, os tipos e o posicionamento dos elementos clicáveis são definidos no YouTube Studio no momento da publicação, sem depender de coordenadas fixas no master.
- O vídeo 004 v5 é exceção histórica aprovada: conserva os dois espaços visuais já renderizados.

Os videos 001 e 002 ja possuem arquivos `.srt`; portanto, nao precisam ser renderizados novamente para receber legenda no YouTube.

## TikTok vertical

- Formato: `1080x1920`, proporcao `9:16`.
- Duracao operacional minima: 65 segundos finais.
- Legenda incorporada, com alto contraste, no maximo duas linhas e dentro da area segura da interface.
- Posicao e quebra de linha podem mudar em relacao ao YouTube, mas palavras e tempos partem da mesma fonte canonica.
- Conteudo central, rosto, textos e citacoes nao podem ficar cobertos pela descricao, botoes laterais ou controles inferiores.
- O primeiro quadro renderizado deve conter uma imagem forte, clara e representativa do recorte. Abertura preta, quase preta ou em transicao nao passa no QA, porque pode virar a miniatura exibida no perfil.
- Antes de publicar, selecionar manualmente em `Selecionar capa` um quadro legivel e coerente com a promessa do recorte; incluir essa verificacao no preflight de publicacao.
- Na publicacao, verificar a visualizacao final no aplicativo e evitar legenda nativa duplicada sobre a legenda incorporada.
- Aplicar o rotulo de conteudo gerado por IA quando exigido, especialmente em cenas, avatar ou fala realistas.

## Recortes de alta atracao

O TikTok nao deve receber um minuto aleatorio do video medio. Cada recorte deve partir de um dos momentos mais fortes do episodio: uma pergunta provocadora, uma quebra de expectativa, uma frase emocional, uma explicacao biblica surpreendente ou uma aplicacao na qual o publico se reconheca rapidamente.

Esse "sensacionalismo" e editorialmente responsavel:

- chama atencao sem prometer algo ausente do conteudo;
- preserva o contexto biblico e o sentido da fala;
- e compreensivel mesmo para quem nao assistiu ao video completo;
- entrega valor dentro do proprio TikTok, alem de despertar vontade de ver o episodio;
- evita comecar no meio de uma frase ou depender de informacao que ficou fora do recorte.

Como o avatar tende a aparecer nos pontos importantes, os candidatos que incluam uma aparicao falada dele devem receber preferencia quando isso fortalecer o reconhecimento e a autoridade do canal. Nem todo TikTok precisa do avatar: o trecho e sua qualidade continuam sendo o primeiro criterio.

Um video medio pode originar varios TikToks de pelo menos 65 segundos, desde que cada um tenha ideia e promessa proprias. Nao criar variacoes quase identicas apenas para multiplicar publicacoes.

Quando o recorte tiver continuacao pertinente no YouTube, seu CTA deve indicar um destino concreto: a questao aprofundada, o titulo pesquisavel do video e o nome do canal. O recorte ainda precisa entregar uma ideia completa; nao cortar antes da resposta apenas para fabricar curiosidade.

## Planejamento conjunto

O video medio deve ser concebido desde o roteiro pensando tambem nos curtos:

1. Durante o roteiro, marcar tres a cinco candidatos a recorte, sem deformar a naturalidade do episodio longo.
2. Depois do audio aprovado, calcular os tempos reais de cada candidato e verificar se sustentam pelo menos 65 segundos.
3. Depois da montagem, selecionar os recortes com melhor combinacao de gancho, clareza, emocao, imagem e aparicao do avatar.
4. Recompor cada selecionado em `9:16`, usando a fonte canonica de legenda e os mesmos materiais do episodio.
5. Criar abertura, fechamento e CTA adequados ao recorte quando forem necessarios para ele funcionar sozinho.

O roteiro pode construir momentos recortaveis, mas o episodio do YouTube nao deve parecer uma colagem de chamadas artificiais. A narrativa longa continua sendo prioritaria, e os curtos nascem organicamente de suas melhores partes.

## Musica por plataforma

### YouTube

A musica de fundo e opcional. Quando for usada, deve ser licenciada para o YouTube, acompanhar o arco emocional com sobriedade e permanecer abaixo da narracao. Uma musica obtida na biblioteca do TikTok nao deve ser incorporada ao master horizontal.

### TikTok

A musica deve ser considerada em todo recorte, porque o som faz parte das informacoes usadas na recomendacao e na busca. Ela continua subordinada ao conteudo: tempo assistido, conclusao e interacoes tendem a pesar mais que a simples presenca de uma faixa.

Fluxo operacional:

1. Exportar a composicao vertical com narracao e efeitos, sem musica exclusiva do TikTok incorporada.
2. Perto da publicacao, pesquisar no aplicativo e no Creative Center sons que estejam atuais no Brasil.
3. Verificar se a faixa combina com o sentido, o publico e o tom religioso do recorte.
4. Adicionar o som dentro do TikTok para preservar sua identificacao e associacao na plataforma.
5. Ajustar o volume ouvindo em alto-falante de celular; a voz deve permanecer completamente inteligivel.
6. Executar a verificacao de direitos autorais de som no TikTok Studio antes de publicar.
7. Registrar faixa, link ou identificador, data da escolha, trecho utilizado, volume e categoria de direitos.

Nao usar som viral desconectado do tema, letra que contradiga a mensagem ou musica que destrua pausas e enfases da narracao. Uma faixa de tendencia pode ser adicionada pelo proprio TikTok em volume praticamente inaudivel como hipotese de distribuicao, desde que seja licenciada e semanticamente segura. Registrar o teste e confirmar depois da publicacao que o aplicativo manteve a associacao ao som.

O video ter 65 segundos ou mais nao obriga a musica a tocar durante todo ele. Usar somente o trecho que o aplicativo disponibilizar. Ate que os termos apresentados a conta elegivel confirmem o limite aplicavel, nao manter musica protegida por mais de 60 segundos continuos; preferir trecho menor, CML ou som com direitos proprios.

Pesquisa e criterios completos: `pesquisa-musica-distribuicao-tiktok-v1.md`.

## Reaproveitamento sem nova cobranca

O video horizontal nao sera simplesmente cortado no centro. Isso eliminaria informacao e poderia danificar legenda, avatar e composicao.

A versao vertical deve reaproveitar:

- roteiro e voz;
- arquivo de sincronizacao;
- cenas geradas e imagens de stock;
- avatar ja produzido;
- musica e efeitos;
- ordem narrativa e identidade visual.

O OpenMontage, Remotion ou FFmpeg recompora esses materiais localmente em `9:16`. Assim, adaptar a legenda e o enquadramento nao consome creditos de ElevenLabs, HeyGen ou fal.ai. So ha novo custo quando for indispensavel gerar uma cena que nao possa ser reenquadrada com qualidade.

A partir do video 003, a selecao de assets e a composicao horizontal devem considerar tambem o futuro recorte vertical: assuntos principais mais centralizados quando isso nao prejudicar o YouTube, fundos com margem e textos sempre tratados separadamente da imagem.

Para os videos 001 e 002, futuros cortes de TikTok devem usar trechos autocontidos com pelo menos 65 segundos e ser recompostos a partir dos assets originais, nao recortados diretamente do master final.

## Qualidade minima das legendas

- texto fiel ao que foi falado;
- sons narrativamente relevantes identificados sem excesso;
- portugues e nomes biblicos revisados;
- entradas e saidas sincronizadas com a voz;
- leitura confortavel, sem blocos excessivos;
- no maximo duas linhas por exibicao;
- contraste suficiente em qualquer cena;
- nenhuma informacao importante fora da area segura;
- pausa final mantida para CTA e tela final.

## Monetizacao e distribuicao

Videos com um minuto ou mais atendem ao requisito de duracao do TikTok Creator Rewards, mas isso nao basta para monetizar. O programa tambem exige conta e regiao elegiveis, audiencia minima, visualizacoes validas e conteudo original e de qualidade.

Por isso, o corte vertical nao deve parecer um recorte automatico, uma sequencia estatica de fotos, texto solto ou loop. Ele deve ser uma adaptacao editorial completa do nosso proprio material, com narrativa, composicao vertical e ritmo visual.

## Evidencias atuais

- TikTok Creator Rewards: https://support.tiktok.com/pt_BR/business-and-creator/tiktok-creator-fund-us
- Diferencas e exigencia de videos com mais de um minuto: https://support.tiktok.com/pt_BR/business-and-creator/creator-rewards-program/how-is-the-creator-rewards-program-different-from-the-tiktok-creator-fund
- Boas praticas de formato vertical, resolucao e area segura: https://ads.tiktok.com/help/article/creative-best-practices
- Especificacoes e variacao da area segura: https://ads.tiktok.com/help/article?aid=10002742
- Identificacao de conteudo gerado por IA: https://support.tiktok.com/en/using-tiktok/creating-videos/ai-generated-content
- Como o TikTok recomenda conteudo, incluindo sons: https://support.tiktok.com/en/using-tiktok/exploring-videos/how-tiktok-recommends-content
- Tipos de conta e acesso a musica: https://support.tiktok.com/pt_BR/using-tiktok/growing-your-audience/switching-to-a-creator-or-business-account
- Uso comercial de musica: https://support.tiktok.com/pt_BR/business-and-creator/creator-and-business-accounts/commercial-use-of-music-on-tiktok
