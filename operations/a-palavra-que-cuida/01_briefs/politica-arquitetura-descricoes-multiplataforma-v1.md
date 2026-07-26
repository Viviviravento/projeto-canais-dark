# Política de arquitetura de descrições multiplataforma v1

Data da pesquisa e decisão operacional: 2026-07-24.

Escopo: vídeos longos e Shorts no YouTube, TikTok, Facebook Reels e Facebook Stories de `A Palavra Que Cuida`.

## Decisão

Adotar uma arquitetura universal de informação, mas nunca uma descrição universal copiada.

O que será padronizado:

- função e ordem dos blocos;
- localização do assunto, CTA, navegação, fontes, identidade e hashtags;
- campos obrigatórios e condicionais;
- validações antes da publicação;
- métricas usadas para revisar a política.

O que permanecerá único:

- primeira formulação;
- pergunta ou necessidade respondida;
- promessa e resumo;
- CTA e destino;
- referências, fontes e avisos;
- conjunto semântico de hashtags.

`Padronizar arquitetura não significa repetir texto.`

## Relevância comprovada e limite da evidência

O YouTube recomenda explicitamente:

- usar as primeiras linhas para descrever o vídeo, porque são vistas antes de `Mostrar mais`;
- criar uma descrição única para cada vídeo;
- destacar naturalmente uma ou duas expressões principais no título e na descrição;
- usar a parte inferior para informações gerais do canal;
- verificar como a descrição aparece na busca, na página do vídeo e no celular.

Fonte oficial: https://support.google.com/youtube/answer/12948449

Na Busca do YouTube, a relevância considera correspondência entre consulta, título, tags, descrição e o conteúdo do próprio vídeo, ao lado de engajamento e qualidade. Isso torna a descrição importante para compreensão e busca, mas não capaz de compensar um vídeo fraco.

Fonte oficial: https://support.google.com/youtube/answer/16090438

No TikTok, a plataforma informa que resultados de busca consideram a correspondência do conteúdo com a consulta, hashtags e som, enquanto interações e tempo assistido têm grande peso nos feeds. O Creator Search Insights permite observar tópicos procurados e desempenho em busca. O TikTok não publica uma ordem orgânica universal para a legenda.

Fontes oficiais:

- https://support.tiktok.com/en/using-tiktok/exploring-videos/how-tiktok-recommends-content
- https://support.tiktok.com/en/using-tiktok/growing-your-audience/creator-search-insights

No Facebook, hashtags podem ajudar pessoas a encontrar Reels por busca, mas a Meta alerta que legendas longas e distrativas, hashtags excessivas ou texto sem relação com o conteúdo podem limitar distribuição e monetização. A plataforma não publica uma ordem universal para a descrição.

Fontes oficiais:

- https://www.facebook.com/help/fblite/2862139500770200
- https://about.fb.com/br/news/2025/04/reduzindo-conteudo-com-spam-no-facebook/

Consequência: a ordem é mais diretamente sustentada por evidência oficial no YouTube. Para TikTok e Facebook, a arquitetura abaixo é decisão interna de clareza, busca, conversão e segurança.

## Arquitetura universal

Ordem semântica padrão:

1. `Essencial`: assunto, necessidade e valor do conteúdo.
2. `Próximo passo`: uma ação principal e um destino claro.
3. `Apoio`: resumo, navegação, referências, fontes, créditos e avisos aplicáveis.
4. `Identidade`: canal e redes verificadas, somente onde houver espaço e função.
5. `Classificação`: hashtags relevantes no final.

### Exceção de precedência

Disclosure obrigatório, risco de segurança ou informação que precise ser vista antes da ação pode subir de posição. Recursos nativos de conteúdo alterado, parceria paga, audiência e restrição etária devem ser preenchidos mesmo que a informação também apareça no texto.

## Regras universais

- A primeira linha começa pelo conteúdo; nunca por saudação, pedido de inscrição, redes sociais, lista de hashtags ou apresentação genérica do canal.
- A primeira formulação precisa funcionar para uma pessoa que não conhece o canal.
- Usar a expressão principal somente quando ela corresponde à fala e à entrega.
- Não repetir título, thumbnail e primeira frase mecanicamente; eles devem sustentar a mesma promessa com informação complementar.
- Cada publicação possui um CTA principal. CTAs secundários ficam no rodapé ou são omitidos.
- O destino citado precisa existir, estar público ou elegível e ser semanticamente relacionado.
- Links sociais nunca ocupam as primeiras linhas.
- Hashtags ficam no final para preservar leitura; essa posição é disciplina editorial, não vantagem algorítmica comprovada.
- Não transformar limite de caracteres em meta de preenchimento.
- Não incluir URL não clicável apenas para simular um caminho.
- Não usar blocos de palavras-chave, hashtags genéricas de alcance ou texto copiado de outro vídeo.
- Links, menções, capítulos e formatação precisam ser verificados fora da conta administradora antes de virarem padrão.

## YouTube — vídeo longo

### Ordem

1. `Duas ou três primeiras linhas únicas`: problema ou pergunta e valor entregue, com uma ou duas expressões principais naturais.
2. `Continuação recomendada`: um vídeo ou playlist diretamente relacionado, com link.
3. `Resumo navegável`: dois ou três parágrafos curtos ou até três pontos do que o vídeo desenvolve.
4. `Capítulos`: quando aplicáveis e baseados na timeline final.
5. `Referências bíblicas e fontes`.
6. `Avisos, créditos e disclosures` aplicáveis.
7. `Rodapé do canal`: identidade, inscrição sóbria, TikTok e Página do Facebook verificados.
8. `Hashtags`: normalmente duas a quatro, específicas ao episódio.

### Molde

```text
[PERGUNTA OU NECESSIDADE + VALOR ENTREGUE]
[SEGUNDA LINHA HUMANA COM A EXPRESSÃO PRINCIPAL, SE COUBER]

Continue por aqui: [VÍDEO OU PLAYLIST RELACIONADA]
[LINK VERIFICADO]

Neste vídeo:
- [PONTO 1]
- [PONTO 2]
- [PONTO 3, SE NECESSÁRIO]

Capítulos
00:00 [TÍTULO REAL]
[DEMAIS CAPÍTULOS]

Referências bíblicas
[REFERÊNCIAS COMPLETAS]

Fontes, avisos e créditos
[SOMENTE O QUE SE APLICA]

A Palavra Que Cuida — fé cristã para a vida real.
TikTok: [URL OFICIAL VERIFICADA]
Facebook: [URL OFICIAL VERIFICADA]

#[TEMA1] #[TEMA2] #[TEMA3 OPCIONAL]
```

Não deixar cabeçalhos vazios. Se um bloco não se aplica, removê-lo.

## YouTube Shorts

URLs em descrições e comentários de Shorts não são clicáveis. A ponte principal será o recurso nativo `vídeo relacionado`.

Fonte oficial: https://support.google.com/youtube/answer/13748639

### Ordem

1. Uma ou duas frases únicas que situem o tema e completem o sentido do Short.
2. CTA curto para tocar no vídeo relacionado, quando houver destino compatível.
3. Referência bíblica ou crédito indispensável.
4. Duas a quatro hashtags específicas.

### Molde

```text
[IDEIA COMPLETA E PESQUISÁVEL DO SHORT]

Toque no vídeo relacionado para aprofundar esta mensagem.
[REFERÊNCIA OU CRÉDITO, SE NECESSÁRIO]

#[TEMA1] #[TEMA2] #[TEMA3 OPCIONAL]
```

Não repetir o rodapé completo de redes sociais nem inserir URL crua esperando clique.

## TikTok

O campo de legenda do Direct Post aceita hashtags e menções e possui limite técnico de 2.200 unidades UTF-16. Esse limite não será meta de preenchimento.

Fonte oficial: https://developers.tiktok.com/doc/content-posting-api-reference-direct-post

### Ordem

1. Uma frase curta e humana que nomeie a necessidade ou a ideia central com linguagem encontrada em busca quando pertinente.
2. Uma frase complementar, pergunta reflexiva ou aplicação concreta.
3. CTA específico para o YouTube apenas quando o vídeo longo realmente aprofunda aquela mensagem e o perfil já possui caminho funcional.
4. Hashtags temáticas no final; normalmente três a cinco como disciplina interna, não quantidade ótima comprovada.

### Molde

```text
[IDEIA CENTRAL OU PERGUNTA DE BUSCA EM LINGUAGEM NATURAL]
[APLICAÇÃO OU PERGUNTA REFLEXIVA OPCIONAL]

Conteúdo completo no YouTube: A Palavra Que Cuida. [SOMENTE SE O CAMINHO DO PERFIL ESTIVER ATIVO]

#[TEMA1] #[TEMA2] #[TEMA3] #[TEMA4 OPCIONAL]
```

Não começar por `#fyp`, `viral`, `paravocê` ou lista de hashtags. Não usar uma consulta apenas porque possui volume; ela precisa corresponder ao conteúdo falado e entregue.

## Facebook Reels

### Ordem

1. Uma ou duas frases que expliquem o valor ou a reflexão do Reel.
2. Uma pergunta específica ou um próximo passo, sem engagement bait.
3. Link verificado para o vídeo completo ou indicação do caminho no perfil/Story, quando aplicável.
4. Uma a três hashtags pertinentes no final como disciplina interna, não ótimo comprovado.

### Molde

```text
[REFLEXÃO OU VALOR CENTRAL DO REEL]
[PERGUNTA ESPECÍFICA OU APLICAÇÃO]

Assista ao conteúdo completo: [LINK, SOMENTE DEPOIS DE VALIDAR CLIQUE E DESTINO]

#[TEMA1] #[TEMA2 OPCIONAL] #[TEMA3 OPCIONAL]
```

Não presumir que link externo reduza ou aumente alcance. Testar em coortes comparáveis. Texto longo sem função, hashtags excessivas e conteúdo alheio ao vídeo ficam proibidos pela margem de segurança do canal.

## Facebook Stories

Stories não usam a mesma lógica de descrição. A arquitetura ocorre dentro do bloco visual:

1. `Frame 1`: contexto ou promessa específica, legível sem áudio.
2. `Frame 2`: continuação e CTA por recurso nativo ou caminho verificado.

Se houver somente um frame, ele precisa combinar contexto e CTA sem poluição. Link, sticker ou outro recurso interativo só entra depois de verificação na Página e fora da conta administradora. Hashtags não são bloco obrigatório.

## Reutilização entre plataformas

O núcleo semântico pode ser reaproveitado, mas a publicação final precisa ser adaptada:

- YouTube longo prioriza busca, continuidade, capítulos e fontes;
- Shorts prioriza sentido completo e vídeo relacionado;
- TikTok prioriza linguagem da busca, conversa e caminho do perfil;
- Facebook Reels prioriza leitura rápida, conversa e link testado;
- Stories priorizam texto visual e recurso interativo.

Não copiar automaticamente a descrição longa do YouTube para TikTok ou Facebook. A automação deve montar cada versão a partir dos mesmos campos estruturados.

## Manifesto de publicação

Cada publicação deve possuir campos separados:

- `primary_need`;
- `primary_phrase`;
- `unique_opening`;
- `supporting_sentence`;
- `primary_cta`;
- `destination_type` e `destination_url_or_id`;
- `chapters`;
- `biblical_references`;
- `sources`;
- `credits`;
- `disclosures`;
- `social_footer`;
- `hashtags`;
- `platform_rendered_description`;
- `link_check_status`;
- `mobile_preview_status`.

O gerador pode montar a descrição; não pode publicar enquanto campos obrigatórios, links e preview estiverem sem validação.

## Medição

### YouTube longo

- termos reais de pesquisa;
- tráfego e tempo assistido de Busca;
- CTR por origem;
- cliques observáveis para próxima visualização;
- inscrições e retorno ao canal;
- desempenho do link ou playlist quando houver medição disponível.

### Shorts

- visualizações do vídeo relacionado e visitas ao canal;
- inscrições por mil Engaged views;
- termos de pesquisa quando disponíveis;
- retenção e satisfação do Short.

### TikTok

- Search Analytics e consultas associadas;
- visitas ao perfil, seguidores e cliques do perfil quando disponíveis;
- comentários relevantes gerados pela pergunta;
- migração observável ao YouTube.

### Facebook

- alcance, tempo assistido e compartilhamentos;
- respostas à pergunta sem contar spam;
- cliques com parâmetros de campanha quando tecnicamente disponíveis;
- ocultações, denúncias e feedback negativo.

Não atribuir desempenho à ordem da descrição isoladamente. Testes de ordem serão feitos por coortes comparáveis, mantendo tema, formato, duração e CTA tão estáveis quanto possível.

## Checklist antes da publicação

- a primeira linha explica o conteúdo sem depender do título;
- a parte única corresponde ao vídeo real;
- a expressão principal aparece naturalmente;
- existe somente um CTA principal;
- o destino está correto, disponível e relacionado;
- links e recursos nativos foram testados;
- capítulos correspondem ao master final;
- referências, créditos, licenças e disclosures estão completos;
- rodapé social usa URLs oficiais verificadas;
- hashtags são específicas e ficam no final;
- não há cabeçalho vazio, palavra-chave empilhada ou texto de outra plataforma;
- o preview móvel foi aprovado.

