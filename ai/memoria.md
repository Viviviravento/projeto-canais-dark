# Memória da Metamorfose

Este arquivo preserva o que precisa atravessar conversas longas. Ele deve ser curto, vivo e útil. O resto deve continuar no chat até amadurecer.

## Espírito do projeto

Criar uma esteira de canais dark, começando por um canal religioso, em que o Codex funcione como parceiro de idealização, organização, pesquisa, roteiro e coordenação. A esteira não deve nascer rígida; ela deve se transformar conforme o método for sendo descoberto.

O primeiro objetivo não é produzir muitos vídeos. É encontrar um método realista, econômico e replicável.

O projeto não deve ser pensado apenas como um canal nem apenas como automação de vídeos. O organismo correto contém uma fábrica de canais e uma fábrica de vídeos. A primeira transforma possibilidades em canais amadurecidos; cada canal cristalizado recebe uma subesteira própria, operada sobre o núcleo reutilizável da segunda.

Formulação cristalizada: estamos criando uma fábrica de canais dark que também é fábrica de vídeos. O canal religioso é o primeiro campo de prova. O casulo deve proteger tanto o método de gênese de canais quanto o núcleo reutilizável de produção, sem confundir decisões específicas de um canal com regras universais do sistema.

O trabalho atual é meta-context-prompting: construir, por conversa e evidência, o contexto que depois dará origem ao agente, à esteira e ao piloto. Ainda não é hora de transformar tudo em instrução operacional final.

Metamorfose, neste projeto, significa sair de inferência para evidência. A conversa serve para levantar hipóteses, buscar evidências, descartar o que não se sustenta e, quando houver material confiável o bastante, preparar um "casulo": uma estrutura provisória que protege e organiza as decisões até virar o fluxo agêntico correto, com a esteira correta.

Não se cria fluxo agêntico definitivo a partir de inferência. Primeiro evidências; depois casulo; depois esteira.

Só depois de entender ferramentas, evidências e custo-benefício deve-se separar o que cabe ao usuário humano e o que cabe ao agente Codex.

O Codex não deve presumir que tarefas visualmente caras, como QA visual fino, análise frame a frame, transições, estética final ou operação minuciosa de interfaces, são responsabilidade natural do agente. Essas fronteiras dependem das ferramentas escolhidas, do custo, da automação disponível e da qualidade necessária.

## Decisões atuais

- Prioridade de crescimento cristalizada em 2026-07-24: buscar o maior público possível e construir `A Palavra Que Cuida` para escala de milhões de acessos, usando intensamente as alavancas legítimas de distribuição. O projeto não testará tráfego artificial, spam, engagement bait, redes de contas, violação de direitos ou contorno de enforcement. O guia central é `operations/a-palavra-que-cuida/01_briefs/guardrails-crescimento-multiplataforma-v1.md`.
- Política de curtos cristalizada em 2026-07-24: Shorts e TikTok serão tratados como funil mensurável de `parada -> compreensão -> permanência -> satisfação -> ação -> conversão`. Edição admirável significa edição semanticamente intencional, não efeito frenético. Desde a mudança de contagem do Shorts, `Views` é alcance bruto; a análise prioriza `Engaged views`, `Stayed to watch`, retenção e conversão. Manual central: `operations/a-palavra-que-cuida/01_briefs/manual-curtos-retencao-conversao-v1.md`.
- Consolidação de armazenamento decidida pelo usuário em 2026-07-27: todos os MP4s verticais aprovados ficam diretamente em `operations/a-palavra-que-cuida/07_exports/shorts-aprovados/`, sem subpastas por vídeo-fonte. Quando o mesmo curto servir ao TikTok e ao YouTube Shorts, preservar um único MP4 universal identificado como `shorts-e-tiktok`. Não duplicar o arquivo inteiro apenas para trocar nome ou tela final. Caption, som, link e vídeo relacionado ficam na publicação; versão separada só existe quando houver diferença material obrigatória no próprio vídeo. Cópias redundantes devem ir para a Lixeira, preservando fontes, scripts e QA reproduzíveis.
- Regra de dependência dos curtos decidida pelo usuário em 2026-07-29: o master renderizado do vídeo longo não é requisito absoluto para produzir seus curtos. A produção antecipada só é permitida quando existirem narração final aprovada, alinhamento canônico correspondente, imagens aprovadas suficientes e possibilidade de executar o mesmo QA técnico e visual aplicado aos demais curtos. O curto deve ser montado diretamente dessas fontes sem perda de qualidade; se qualquer uma dessas garantias faltar, houver risco de mudança editorial material ou o enquadramento não puder ser validado, aguardar o master longo e não produzir antecipadamente.
- Decisão TikTok de 2026-07-24: um único perfil pode variar forma sem variar público ou promessa. O piloto começa com duas famílias — reflexão falada com ponte ao YouTube e música cristã em contexto — limitado a no máximo três famílias ativas. Cadência inicial: cinco publicações por semana durante quatro semanas, com doze peças faladas e oito musicais. O ápice experimental futuro é três por dia, alcançado pela escada cinco por semana, uma por dia, duas por dia e três por dia, sempre condicionado aos gates. Documento central: `operations/a-palavra-que-cuida/01_briefs/decisao-perfil-tiktok-formatos-cadencia-v1.md`.
- Direção de escala multiplataforma aprovada em 2026-07-24: buscar a maior cadência sustentável pelo ganho marginal total, não por preenchimento de limite técnico. Ápice experimental: 2 longos e até 3 Shorts por dia no YouTube; até 3 TikToks; até 3 Facebook Reels; até 3 blocos de Stories. Espaçamento mínimo: 8 horas entre longos e 4 horas entre verticais do mesmo formato. Correção de balanço: `quatro curtos por longo` passa a significar pelo menos quatro candidatos mapeados, não quatro renders completos obrigatórios. Separar candidato de corte, master editorial vertical e adaptação por plataforma. Com dois longos por dia, a base segura é 1 vertical ligado a cada longo e distribuído em Shorts e TikTok quando couber; terceiro slot é opcional por métrica. Quatro ou mais por plataforma/dia só entram como experimento futuro depois de 3/dia provar ganho marginal e ausência de fadiga. A frequência atual não muda automaticamente; cada plataforma sobe separadamente por coortes e recua quando total, mediana, conversão, QA, originalidade ou segurança cruzarem os gates. Política: `operations/a-palavra-que-cuida/01_briefs/politica-cadencia-maxima-multiplataforma-v0.1.md`.
- Modelo operacional desejado pelo usuário: depois de construída e aprovada a base, o Codex deve funcionar como braço direito de publicação e tomar autonomamente decisões de slots, adaptações, reagendamentos e promoção de cadência dentro das políticas. Isso é direção de governança futura, não prova de capacidade técnica nem autorização de publicação imediata. Automação pública ainda depende de manifestos, estados, logs, credenciais, OAuth/2FA, auditorias de API, consentimentos e kill switches.
- Política de contas seguidas no TikTok, decidida em 2026-07-24: seguir serve como radar editorial e de relacionamento, não como hack de distribuição. Começar com 30 contas manualmente selecionadas e manter faixa operacional de 30 a 60 contas úteis, com revisão mensal. Não praticar follow for follow, seguimento automático, ciclos em massa nem promoção invasiva nos comentários alheios. A quantidade seguida não é KPI; medir achados editoriais, testes originados e relações legítimas. Detalhes no documento central da decisão TikTok.
- Radar inicial do TikTok verificado publicamente em 2026-07-24: 30 handles distribuídos entre reflexão, música, necessidades do público, criação e ecossistema estão em `operations/a-palavra-que-cuida/01_briefs/radar-contas-tiktok-inicial-v1.md`. Antes de seguir, conferir handle e duas publicações no aplicativo. Interação inicial é manual e autêntica, sem promoção do canal, comentário copiado ou resposta em massa; três a cinco comentários substantivos por dia é limite operacional inicial, não regra da plataforma.
- Decisão de metadados e comunidade YouTube de 2026-07-24: descrições horizontais terão parte editorial única, palavras estratégicas naturais e rodapé fixo com redes verificadas. Cada vídeo terá conjunto semântico próprio de tags e hashtags, orientado pela pergunta que responde; tags são secundárias e hashtags serão poucas e precisas, normalmente duas a quatro como disciplina interna. Foram substituídas as antigas metas de 8 a 15 hashtags e de aproximadamente 450 caracteres de tags. Medir termos reais de pesquisa, tráfego de Busca, CTR por origem, retenção, inscrições e próxima visualização, sem atribuir alcance aos metadados isoladamente. Cada vídeo começa com pergunta específica fixada pelo canal. Até média aproximada de 200 comentários por vídeo, curtir todos os comentários elegíveis; coração é endosso seletivo de contribuições especialmente valiosas e seguras. Notificação é efeito possível, não justificativa para engajamento indiscriminado. Política: `operations/a-palavra-que-cuida/01_briefs/politica-descricoes-comunidade-youtube-v1.md`.
- Correção operacional de 2026-07-26: a publicação de cada longo só é concluída depois de verificar na interface que a pergunta específica do canal foi publicada nos comentários e, quando prevista, fixada no topo. Essa verificação é parte do gate final, não uma intenção registrada apenas no manifesto.
- Regra transversal de comunidade, decidida em 2026-07-29: todo vídeo longo publicado por qualquer canal deve receber, pela própria conta do canal, um comentário original e específico daquele episódio. O comentário precisa ampliar ou aprofundar a ideia do vídeo e convidar uma resposta humana concreta; não usar pergunta genérica, CTA mecânico ou texto repetido entre vídeos. A publicação só fica concluída após verificar que o comentário foi efetivamente enviado e, quando a plataforma permitir, fixado no topo.
- Regra universal de interação em comentários, decidida em 2026-07-29: em todos os canais atuais e futuros, até cada canal alcançar 1.000 inscritos, curtir todos os comentários elegíveis recebidos nos seus vídeos. Dar coração apenas de forma seletiva a comentários pertinentes, seguros e especialmente alinhados ao assunto do vídeo ou ao propósito do canal; o coração é endosso editorial, não ação automática. A notificação ao autor é um possível efeito da plataforma, não garantia de retorno.
- Arquitetura de descrições aprovada em 2026-07-24: padronizar a ordem `essencial -> próximo passo -> apoio -> identidade -> classificação`, sem copiar o mesmo texto. A primeira linha sempre começa pelo conteúdo; redes e hashtags não abrem a descrição. YouTube longo usa primeiras linhas únicas, continuidade, resumo, capítulos, fontes, rodapé social e hashtags; Shorts usa texto curto e vídeo relacionado, sem URL crua; TikTok e Facebook recebem captions próprias; Stories organizam contexto e CTA dentro dos frames. Cada publicação terá campos estruturados, preview móvel e validação de links. Política: `operations/a-palavra-que-cuida/01_briefs/politica-arquitetura-descricoes-multiplataforma-v1.md`.
- O primeiro canal será o `Canal Religioso`.
- O projeto raiz é plural: `Canais Dark`. O canal religioso é o primeiro caso de teste, não o limite da arquitetura.
- A esteira-base deve sustentar a gênese de vários canais e uma fábrica de vídeos reutilizável; cada canal nasce com sua própria subesteira sobre esse núcleo comum.
- O fluxo agêntico metamorfado deve conter duas fábricas aninhadas: a fábrica de canais, que imagina, pesquisa, desenvolve, amadurece, testa e cristaliza novos canais; e a fábrica de vídeos, que opera dentro de cada canal cristalizado. Cada canal herda um núcleo universal e possui sua própria subesteira editorial, econômica, visual e operacional.
- A próxima frente de foco é a parte que custa dinheiro: integrações pagas, chaves de API, créditos, gateways e decisões de custo-benefício. Nenhuma ferramenta paga deve virar stack definida sem evidência atual de preço, utilidade e teste pequeno aprovado.
- As redes iniciais são YouTube e TikTok.
- Regra de organização atualizada em 2026-08-04: cada unidade concreta recebe uma pasta própria sob `operations/`, com todo o seu material de produção. Nunca misturar ativos entre operações; `operations/a-palavra-que-cuida/` e `operations/quase-celestial/` são estruturas independentes. Quando uma nova operação começar, criar sua pasta sob `operations/` antes de gerar ou salvar o primeiro ativo. Esta regra substitui a decisão de 2026-07-29 que colocava cada canal diretamente na raiz.
- Decisão arquitetural de 2026-08-04: `factory/` contém a implementação universal; `operations/` agrupa unidades concretas; `audits/`, `decisions/` e `research/` separam vereditos, decisões arquiteturais e pesquisa transversal; `ai/` fica restrito à memória contextual do agente. “Casulo” é regime de maturação por lifecycle, capacidades, baselines, gates e execuções limpas, não uma pasta.
- Estado de maturidade de 2026-08-04 para `A Palavra que Cuida`: lifecycle `stabilizing`. `longform_voice` está em `regression_detected`, sem baseline reproduzível; QA técnico não equivale a aprovação semântica. A regressão dessa capacidade não reinicia automaticamente toda a operação.
- `ai/` guarda apenas memória, ideias importantes, decisões e limites do agente.
- O público-alvo é fixo no nível do canal, não dinâmico por vídeo.
- Público-alvo inicial definido: majoritariamente mulheres de 25 a 49 anos, com preferência estratégica por 35 a 49 anos.
- O conteúdo deve mesclar interesses das faixas 25-34 e 35-49 no começo, observar rendimento/métricas e centralizar mais na faixa com maior aderência.
- O tom desejado é uma mistura neutra entre professor, conselheiro e pregador, sem caricaturar nenhum desses papéis.
- O avatar deve parecer um narrador comum com autoridade pelo conhecimento, não uma autoridade pedante, professoral ou que fale de cima para baixo.
- Preferência atual para o canal religioso: voz separada do avatar. O avatar deve funcionar como corpo/presença visual; a voz pode ser escolhida como identidade própria e reutilizada também fora do avatar.
- Música deve começar por stock/biblioteca com licença limpa, não por geração musical paga.
- Decisão do usuário em 2026-07-29 para o futuro canal de legendas/traduções musicais: operar sem contato manual por e-mail. Só selecionar faixas de catálogos cuja licença ou regra nativa autorize claramente uso comercial no YouTube, tradução/legenda da letra e publicação com visual próprio; não usar clipes ou músicas de terceiros quando essa permissão não estiver explícita. Cada faixa deverá passar por um gate documental simples antes da produção, preservando a fonte da licença e seus limites.
- Organização do novo canal em 2026-07-29, atualizada apenas quanto ao caminho em 2026-08-04: seus briefs, pesquisas, licenças, letras/traduções, artes, projetos, renders, publicações e métricas deverão ficar em pasta própria sob `operations/`, separada de `operations/a-palavra-que-cuida/` e `operations/quase-celestial/`. A pasta só deve ser criada com o nome definitivo; até lá, não salvar ativos dentro de outra operação.
- Direção editorial inicial do canal de legendas/traduções, aprovada pelo usuário em 2026-07-29: não ficar preso a um único gênero, mas manter a promessa `ajudar brasileiros a entender e sentir músicas internacionais através de traduções naturais`. Piloto exploratório: 60% pop romântico/emocional, 25% R&B/soul/hip-hop melódico e 15% indie/alternative/nostalgia. A divisão pode mudar conforme a disponibilidade de licenças compatíveis, busca, retenção, inscritos ganhos por vídeo e retorno da audiência; não é uma regra permanente.
- Ajuste editorial do canal de legendas/traduções em 2026-07-29: reservar 20% dos vídeos do piloto para rock, com prioridade para clássicos antigos e cobertura controlada de outros subgêneros (pop rock, alternative, emo, hard rock e similares). O balanceamento será acompanhado em uma janela móvel de 20 vídeos, e a seleção de cada música deverá considerar a proporção acumulada do canal, a disponibilidade de licença compatível e o desempenho por subgênero. Os 20% são hipótese inicial, não promessa de resultado.
- Prioridade atual de contas/APIs pagas: HeyGen entra primeiro por causa do papel central do avatar no canal religioso. Depois disso, investigar um caminho para usar a versão mais atual do Kling, sem assumir que o gateway do OpenMontage já expõe a versão mais nova.
- Chaves iniciais já foram coletadas por janela segura e gravadas no `.env` do OpenMontage. Daqui em diante, novas chaves só devem ser coletadas quando o usuário pedir explicitamente.
- A ideia de vídeos longos ficou suspensa por custo. Minutagens com avatar/geração paga tornam longos caros demais para o início. Precisamos decidir depois novos tamanhos realistas e como adaptar as ideias anteriores para formatos menores, testáveis e financeiramente viáveis.
- Pesquisa atual sobre YouTube: vídeos menores que 8 minutos podem monetizar quando o canal estiver no YPP, mas vídeos monetizados com 8 minutos ou mais permitem mid-roll ads. Portanto, se o objetivo é pensar em formato-carro-chefe monetizável para YouTube, o alvo inicial não deve ser 3-6 minutos; deve mirar pelo menos 8 minutos, com custo controlado por reduzir uso de avatar/geração paga.
- Correção de formato bíblico: em vídeos médios de 8-12 minutos, não tentar replicar a ideia antiga de ler capítulos inteiros ou trechos enormes. O formato viável é trabalhar versículos ou microtrechos curtos, com leitura breve e comentário/aplicação como corpo principal do vídeo.
- Correção editorial de 2026-07-22: os cinco subtipos anteriores eram uma taxonomia exploratória e não devem estruturar ou limitar o canal. Podem continuar como lentes para classificar ideias, mas cada vídeo de 10 a 12 minutos deve adotar a forma exigida pelo tema e sustentar reflexão bíblica mais profunda, com contexto, argumento, conexões e aplicação sem redundância.
- Regra editorial de público: a segmentação deve orientar escolhas de tema, tom, ritmo e exemplos nos bastidores, mas não deve aparecer no roteiro como laudo demográfico. É permitido nomear a pessoa quando o tema justificar naturalmente, como "você que é mãe" em um vídeo sobre maternidade, mas evitar enumerações artificiais ou invasivas como "você, mulher de 35-49 anos, mãe/esposa/trabalhadora...". A linguagem deve acertar pela generalidade íntima, sem assustar o espectador e sem esconder tanto o alvo a ponto de ficar abstrata demais.
- Versão bíblica escolhida para citações/leitura curta do canal religioso: Bíblia Sagrada - Almeida Corrigida Fiel, da Sociedade Bíblica Trinitariana do Brasil. Não baixar nem armazenar a Bíblia inteira no repositório sem permissão expressa; a regra é guardar apenas os versículos/microtrechos usados por vídeo, com atribuição correta e controle de limite.
- Identidade do canal: nome, promessa central, estética, tipo de autoridade e limites denominacionais podem ser propostos/decididos pelo Codex, com base na lógica do canal e sem inferência disfarçada de fato. Avatar é exceção parcial: o Codex pode gerar/propor opções, mas a escolha final precisa passar por crivo humano porque aparência, naturalidade e confiança são altamente sensíveis.
- Correção de sequência: antes de montar o piloto, o próximo bloco correto é concluir uma identidade v0 suficiente do canal: promessa central, estética, tipo de autoridade, limites denominacionais, direção de avatar e naming em versão testável. Isso dá chão ao piloto sem tentar fechar a estrutura inteira do canal.
- Naming do canal reaberto. `A Palavra e o Dia` não está aprovado; fica apenas como hipótese inicial. O nome do canal não deve ser escolhido por intuição ou gosto solto. Antes de propor lista curta, pesquisar critérios de naming para YouTube, saturação do nicho religioso brasileiro, handles, risco de confusão e relação entre nome, marca, descoberta e monetização.
- Identidade do canal religioso promovida para v1. Nome público: `A Palavra que Cuida`. Handle escolhido: `@apalavraquecuida`, com fallback operacional `@apalavraquecuidabr` se a plataforma bloquear o handle na criação. A identidade atual está em `operations/a-palavra-que-cuida/01_briefs/identidade-canal-v1.md`; versões anteriores foram movidas para `operations/a-palavra-que-cuida/01_briefs/legacy/`.
- Avatar-base do canal religioso aprovado pelo usuário e salvo em `operations/a-palavra-que-cuida/04_assets/avatar/avatar-base-v1.png`. Direção: homem brasileiro/lusófono maduro, comum, sereno, camisa azul-marinho, barba curta grisalha, fenótipo pardo/moreno moderado. Não alterar raça/fenótipo de forma brusca; ajustes futuros devem ser finos e práticos, como enquadramento, nitidez, iluminação, fundo, roupa ou compatibilidade com HeyGen.
- A pesquisa de naming e concorrência não deve prender o projeto em preparação infinita. Ela serve para entender o espaço disponível, evitar erros óbvios e formular uma posição plausível. Depois do piloto publicado, o feedback decisivo passa a ser das métricas pós-publicação: CTR, retenção, comentários, inscritos por vídeo, desempenho de cortes, custo por minuto produzido e sinais de aderência do público.
- Pilares editoriais amplos não precisam ser fechados agora. Eles devem amadurecer depois de 1-3 pilotos, quando já houver direção real de edição, visual, formato e resposta humana.
- Não existe uma estrutura editorial única nem cinco moldes obrigatórios. A esteira deve montar a arquitetura de cada episódio a partir da promessa, da evidência, do argumento e da duração de 10 a 12 minutos, preservando apenas contratos transversais já aprovados, como clareza de abertura, referências bíblicas completas, conclusão, CTA, legendas e tela final.
- Métricas de decisão não devem ser chutadas como "padrão ouro" universal. Quando chegarmos nesse bloco, pesquisar benchmarks e boas práticas de YouTube/religião, separar o que é evidência geral do que é específico do nosso canal, e depois criar um método próprio de avaliação.
- O Codex não deve inferir público-alvo, persona, promessa, linguagem, denominação, stack de ferramentas ou estratégia como se fossem fatos.
- Ferramentas externas de avatar, vídeo, voz e edição ainda são hipóteses, não stack decidida.
- Vídeos longos devem ser evitados no início até existir um piloto menor que valide custo, qualidade e processo.
- A divisão entre humano e Codex ainda não está definida; ela deve nascer depois da análise realista de ferramentas e custo-benefício.
- Veredito humano após o vídeo 003, em 2026-07-23: o Codex ainda não está pronto para conduzir sozinho a produção audiovisual integral, embora a evolução do método seja reconhecida. A subesteira permanece em modo assistido. QA técnico, validação por keyframes e conclusão do render não autorizam promoção automática do gate editorial-visual. Enquanto não houver evidência posterior suficiente, o humano deve assistir ao master completo e aprovar contexto, pertinência das imagens, ritmo, montagem, avatar e qualidade geral antes da publicação. O próprio Codex continua responsável por perceber quando há base para propor mudança de gate, mas o vídeo 003 não forneceu essa base.
- Correção humana complementar do vídeo 003: a voz melhorou, porém ainda fala devagar demais e conserva pausas artificiais. A direção para o próximo ajuste é acelerar levemente, com comparação curta antes de qualquer nova geração paga. Não fixar uma porcentagem por intuição; distinguir pausa causada pela escrita/geração de simples lentidão global.
- Decisão do usuário atualizada em 2026-07-28: a voz Bruno Cardoso passa a receber pós-processamento local em `1.07x`, com pitch preservado. Aplicar a aceleração após o TTS e antes de gerar alinhamentos, legendas, avatar ou composição. O padrão resolve apenas a lentidão global; pausas artificiais internas devem voltar para escrita e geração, sem aceleração excessiva para escondê-las. O vídeo 006 permanece em `1.05x` como exceção histórica, pois o render já havia começado antes da mudança.

## Regra de César

Dar a César o que é de César:

- input do usuário é input do usuário;
- hipótese é hipótese;
- pesquisa é pesquisa;
- decisão é decisão.

Se uma informação importante não estiver fechada, o Codex deve perguntar ao usuário ou pesquisar quando fizer sentido. Se for apenas uma hipótese útil para pensar, deve ser marcada como hipótese e não usada como fundamento fixo.

Correção operacional adicionada em 2026-07-10: em decisões sobre ferramentas, APIs, custos, qualidade técnica, licenças, plataformas, versões bíblicas, público ou estratégia, o Codex não deve orientar decisão com "suspeito", "aposto", "provavelmente" ou equivalentes. Deve buscar evidência atual, usar fonte primária quando possível, testar localmente quando couber, ou declarar que ainda é hipótese não decidida.

Quando a pergunta envolver comparação de ferramentas pagas, como "HeyGen com voz nativa vs ElevenLabs + lip-sync", a primeira resposta correta é pesquisar documentação, preço e limitações em fontes atuais/primárias. Teste prático só entra depois, se a pesquisa não resolver a decisão ou se o usuário pedir validação prática. Não se decide por intuição.

## Ideia inicial do canal religioso

O canal deve trabalhar conteúdo bíblico em português brasileiro, com ligação ao cotidiano vivido brasileiro.

Formatos imaginados até agora:

- vídeos longos de leitura da Bíblia e monólogo;
- vídeos médios de autoajuda com prisma bíblico;
- vídeos médios de ensaios temáticos com prisma bíblico;
- vídeos médios sobre figuras bíblicas em momentos específicos;
- cortes curtos extraídos dos melhores momentos.

Visual imaginado para o formato longo:

- Bíblia vista de cima como imagem principal;
- avatar religioso no canto inferior direito durante a leitura;
- avatar em tela cheia durante comentários, sentado à mesa com a Bíblia à frente.

Essas ideias ainda são matéria-prima. A forma final deve surgir da conversa, do público definido e dos testes.

## Público-alvo inicial

Decisão: o canal começa mirando majoritariamente mulheres de 25 a 49 anos.

Preferência estratégica: dar mais peso ao subgrupo de 35 a 49 anos, sem excluir 25 a 34 no início.

Racional:

- Pesquisa inicial indicou que o público cristão/evangélico brasileiro tende a ser mais feminino.
- O recorte 25-49 concentra temas fortes para cotidiano, família, casamento, trabalho, sofrimento, fé, culpa, responsabilidade e recomeço.
- O subgrupo 35-49 parece especialmente compatível com conteúdo mais calmo, reflexivo, de orientação e companhia.

Estratégia:

- Mesclar temas que conversem com 25-34 e 35-49.
- Medir aderência por vídeo, retenção, comentários, CTR e cortes.
- Com o tempo, centralizar o conteúdo no subgrupo que responder melhor.

Evidências registradas:

- IBGE/Censo 2022, via Religião e Poder/ISER: evangélicos no Brasil são majoritariamente mulheres, cerca de 55,4%; católicos são mais equilibrados; pessoas sem religião têm maioria masculina. Fonte: https://religiaoepoder.org.br/artigo/o-que-mudou-no-quadro-das-religioes-do-brasil-comparacoes-entre-os-censos-2010-e-2022
- Datafolha 2019, reproduzido pelo Informe Blumenau: evangélicos apareciam com cerca de 58% mulheres; distribuição etária evangélica relevante entre 25-59, com presença também em 16-24. Fonte: https://www.informeblumenau.com/datafolha-50-dos-brasileiros-sao-catolicos-31-evangelicos-e-10-nao-tem-religiao/
- Globo/Gente, Diversidade Cristã: evangélicos são mais jovens que católicos; 40% dos evangélicos têm 16-34 anos; 54% dos evangélicos são classe C; fé e conteúdos religiosos aparecem como apoio emocional. Fonte: https://gente.globo.com/pesquisa-infografico-diversidade-crista/
- Estudo "As religiões e as mídias sociais": evangélicos usam redes sociais mais que católicos em alguns recortes, com presença relevante em YouTube e WhatsApp. Fonte: https://revistaplura.emnuvens.com.br/anais/article/view/2115/1649
- DataReportal 2026 Brasil: YouTube tem alcance amplo e levemente feminino no Brasil; Instagram é mais feminino; TikTok, nos dados publicitários adultos, aparece mais masculino. Fonte: https://datareportal.com/reports/digital-2026-brazil

Limite da pesquisa: não foi encontrada uma fonte pública única que responda diretamente, com precisão nacional, "quem consome conteúdo religioso online no Brasil por sexo e idade". A decisão foi tomada por triangulação entre composição religiosa, uso de redes e dados de plataformas.

## Inputs recentes do usuário

- O usuário escolheu público inicial majoritariamente feminino, 25-49, com preferência por 35-49.
- A escolha entre cristãs praticantes, afastadas, curiosas ou outro segmento ainda pode ser refinada dentro desse público.
- A versão bíblica deve ser decidida depois de entender público-alvo e segurança de uso.
- O piloto mínimo deve ser decidido depois de discutir as ferramentas e a esteira viável.

## Perguntas que importam agora

- As perguntas de refinamento do público estão congeladas por enquanto, mas continuam válidas para o casulo. Elas só não são o foco imediato desta rodada.
- O foco volta para a essência do primeiro prompt: desenhar a esteira agêntica, entender papéis, custos, artefatos e ferramentas necessárias.
- Ainda não há stack de ferramentas definida.
- Antes de dividir tarefas entre usuário e Codex, é preciso discutir ferramentas, limitações práticas e custo-benefício.
- O casulo precisa incluir também público-alvo, dores prioritárias, linguagem e relação com a fé, porque isso afeta roteiro, avatar, temas e formato.

## Pesquisa inicial: edição de vídeo por agente

Data: 2026-07-08.

Estado local:

- Node/npm funcionam no ambiente.
- O Python padrão do sistema não está instalado, mas o runtime interno do Codex possui Python próprio.
- O ambiente atual não tem FFmpeg no PATH.
- O runtime interno do Codex tem PIL e NumPy, mas não tem MoviePy nem OpenCV.

Achados:

- Remotion permite criar vídeos programaticamente com React e possui Agent Skills oficiais para agentes como Codex. Bom candidato para vídeos templateados, motion graphics, composições previsíveis e renderização por código. Fontes: https://www.remotion.dev/ e https://www.remotion.dev/docs/ai/skills
- MCPs de edição baseados em FFmpeg existem, como KyaniteLabs `mcp-video`, `video-audio-mcp` e `ffmpeg-mcp`. Eles são bons para cortes, concatenação, crop, resize, overlay, legenda, transcode, extração de áudio/frames e operações determinísticas. Fontes: https://github.com/KyaniteLabs/mcp-video, https://github.com/misbahsy/video-audio-mcp, https://github.com/yubraaj11/ffmpeg-mcp
- Reap possui MCP hospedado para clipping, captions, reframing, dubbing, transcrição e publicação, mas requer plano pago com API. Pode ser candidato para cortes/repurpose quando já houver vídeos longos ou médios. Fonte: https://docs.reap.video/api-reference/mcp
- FFmpeg Micro possui MCP hospedado para transcode, upload, geração de SRT e downloads, com OAuth. Parece mais processamento/transcrição do que edição criativa completa. Fonte: https://www.ffmpeg-micro.com/mcp
- Shotstack e Creatomate são APIs de automação/template de vídeo. Podem servir para montar vídeos por JSON/template, especialmente em volume, mas entram depois se o custo-benefício fizer sentido. Fontes: https://shotstack.io/ e https://creatomate.com/

Interpretação:

- O Codex pode editar vídeos bem quando a edição é especificável: cortar de X a Y, juntar clips, inserir legenda, gerar thumbnail, reformatar para vertical, renderizar template, adicionar texto, trocar imagem/áudio.
- O Codex não deve ser tratado como responsável natural por decisões visuais caras, como QA frame a frame, ritmo fino, estética subjetiva, transições complexas e julgamento visual final. Isso depende das ferramentas e do custo.
- Geração de imagem fica com o Codex por padrão; não complexificar com ferramenta externa para imagem enquanto a capacidade interna for suficiente.

## Pesquisa inicial: OpenMontage

Data: 2026-07-08.

Achado importante:

- OpenMontage parece mais alinhado ao projeto do que MCPs simples de FFmpeg, porque não é apenas uma ferramenta de edição; é um sistema agentic de produção de vídeo com pipelines, skills, ferramentas, checkpoints, custo, preflight e aprovação humana.
- Repositório oficial pesquisado: https://github.com/calesthio/OpenMontage
- Cuidado de segurança: existe issue alertando sobre um repositório lookalike `Open-Montage/OpenMontage` com comportamento malicioso. Usar apenas `calesthio/OpenMontage`. Fonte: https://github.com/calesthio/OpenMontage/issues/200

Pontos relevantes:

- OpenMontage se declara compatível com Codex e inclui `CODEX.md`, apontando para `AGENT_GUIDE.md`.
- Arquitetura é agent-first/instruction-driven: o agente lê manifestos YAML, skills de cada estágio, usa tools Python, gera checkpoints e pede aprovação humana.
- Pipelines relevantes para este projeto: `avatar-spokesperson`, `animated-explainer`, `clip-factory`, `talking-head`, `podcast-repurpose`, `hybrid`.
- Pré-requisitos: Python 3.10+, FFmpeg, Node.js 18+ e um agente de código.
- Licença: AGPL-3.0.

Interpretação para o casulo:

- OpenMontage deve virar candidato central para estudo do fluxo agêntico de vídeo.
- Não adotar cegamente. Primeiro auditar setup, dependências, licença, custo real, estabilidade, issues abertas e compatibilidade com Windows/Codex.
- Pode servir como referência para o nosso casulo mesmo que não seja adotado integralmente.

Auditoria local inicial:

- O repositório oficial foi clonado apenas em pasta temporária para auditoria, não incorporado ao projeto.
- O repo tinha 536 arquivos rastreados no momento da auditoria.
- Pipelines encontrados: `animated-explainer`, `animation`, `avatar-spokesperson`, `character-animation`, `cinematic`, `clip-factory`, `documentary-montage`, `framework-smoke`, `hybrid`, `localization-dub`, `podcast-repurpose`, `screen-demo` e `talking-head`.
- Foram instalados `requirements.txt` e dependências do `remotion-composer` em ambiente temporário.
- Sem FFmpeg no PATH, o runtime de composição por FFmpeg não ficou disponível.
- Após `npm install` no `remotion-composer`, o provider menu passou a reconhecer Remotion como disponível.
- Provider menu validado localmente: Remotion disponível; FFmpeg indisponível; HyperFrames indisponível; TTS, avatar, geração de vídeo e geração de imagem por APIs indisponíveis por falta de chaves/configuração.
- Demos zero-key listados pelo `render_demo.py`: `code-to-screen`, `focusflow-pitch`, `world-in-numbers`.

Leitura técnica:

- O AGENT_GUIDE do OpenMontage combina com a nossa regra de evidência: selecionar pipeline, rodar preflight, descobrir ferramentas reais pelo registry, apresentar plano/custos e executar por estágios com checkpoints.
- A documentação de providers apresenta Remotion como fallback local importante quando não há geração de vídeo configurada: imagens estáticas, cards, textos, gráficos e transições podem virar vídeo programático.
- O setup mínimo útil indicado pela própria documentação gira em torno de FFmpeg + Node; para uma esteira mais completa entram Piper TTS e fontes gratuitas como Pexels/Pixabay, depois APIs pagas se fizer sentido.

Interpretação atual:

- O usuário estava certo em puxar OpenMontage: ele é o candidato mais forte até agora para estudar a esteira agêntica de vídeo.
- OpenMontage não deve substituir o raciocínio da metamorfose; deve virar evidência e possível fundação do casulo.
- Para o canal religioso, o pipeline `avatar-spokesperson` parece o encaixe mais próximo para o formato com narrador/avatar; `clip-factory` parece o encaixe natural para cortes curtos a partir de longos/médios; `talking-head` é mais útil para footage bruto de uma pessoa real e não parece ser o eixo principal do canal dark com avatar.
- A próxima validação prática, se seguirmos por esse caminho, é instalar/configurar FFmpeg e renderizar um demo local para provar que Windows + Node + Remotion + FFmpeg funcionam antes de falar em piloto religioso.
- Geração de imagem continua preferencialmente com Codex; não há motivo atual para complexificar essa parte com providers de imagem do OpenMontage.

Instalação local realizada:

- OpenMontage instalado em `tools/OpenMontage`, a partir do repositório oficial `https://github.com/calesthio/OpenMontage`, branch `main`, commit local auditado `de348f1`.
- FFmpeg instalado localmente em `tools/ffmpeg`; `tools/ffmpeg/bin` foi adicionado ao PATH do usuário.
- Helper criado em `tools/openmontage-env.ps1` para carregar, em sessões futuras, `OPENMONTAGE_HOME`, PATH da venv e PATH do FFmpeg.
- Ambiente Python criado em `tools/OpenMontage/.venv` usando Python 3.12 do runtime do Codex.
- Dependências instaladas: `requirements.txt`, Piper TTS, dependências Node do `remotion-composer`, e extras locais úteis para análise/ingestão (`yt-dlp`, `youtube-transcript-api`, `faster-whisper`, `scenedetect`, `opencv-python`, `pygments`).
- `.env` local criado a partir de `.env.example`, ainda sem chaves pagas.
- Vozes Piper brasileiras baixadas localmente: `pt_BR-cadu-medium`, `pt_BR-faber-medium` e `pt_BR-jeff-medium`, todas com dataset CC0 conforme model cards. Samples gerados em `tools/OpenMontage/assets/voices/piper/_samples/`.

Validação pós-instalação:

- Provider menu reconheceu `ffmpeg`, `remotion` e `hyperframes` como runtimes disponíveis.
- Provider menu reconheceu `piper` como TTS local disponível.
- Provider menu reconheceu ingestão via `yt-dlp`, legenda via OpenMontage/Remotion e pós-produção de vídeo `9/9` via FFmpeg/HyperFrames.
- A ferramenta interna `piper_tts` do OpenMontage gerou áudio com modelo `pt_BR-faber-medium`.
- Remotion renderizou demo zero-key `focusflow-pitch.mp4`; `ffprobe` validou duração aproximada de 22,55s e arquivo de cerca de 4 MB.

Limites atuais da instalação:

- Nenhuma API paga foi configurada.
- Geração de vídeo por Runway/Kling/Veo/Sora/HeyGen e similares continua indisponível até decisão e chave.
- Avatar/lip-sync local com SadTalker/Wav2Lip não foi instalado; depende de decisão, GPU e custo-benefício.
- `requirements-gpu.txt` não foi instalado.
- A instalação habilita a fundação local barata da esteira, mas ainda não define o workflow final do canal religioso.

## Pesquisa inicial: parte paga da fábrica de vídeos

Data: 2026-07-10.

Princípio:

- OpenMontage ajuda a operar e estimar, mas preço final deve vir da página atual do provider antes de qualquer gasto.
- Ferramenta paga só entra no casulo se tiver função clara, preço atual, teste mínimo aprovado e alternativa de fallback. O gate humano não pedirá aprovação de um orçamento abstrato ou permanente: antes de cada lote pago, mostrará provedor, modelo, quantidade, preço vigente e custo calculado em moeda real para aquela execução. Depois, registrará o custo efetivamente debitado. Retentativa paga nunca é automática.
- Não confundir ferramenta paga com stack definida. Chave de API é hipótese operacional até passar por teste pequeno.
- Chaves, senhas, tokens e outros segredos não devem ser pedidos no chat. Foi criada uma skill global do Codex, `sensitive-input-collector`, em `C:\Users\Vivia\.codex\skills\sensitive-input-collector`, para abrir janela local de coleta e gravar o valor direto no destino correto sem imprimir o segredo.

Integrações pagas ou com chave externa vistas no OpenMontage:

- Voz/TTS: ElevenLabs, Google TTS, OpenAI TTS, Doubao, DashScope. Piper fica como fallback local gratuito.
- Imagem: fal.ai/FLUX/Recraft, Google Imagen, OpenAI image, xAI/Grok, DashScope, Pexels/Pixabay como stock gratuito com chave.
- Vídeo: fal.ai/Kling/Veo/MiniMax, Runway, OpenAI/Sora, xAI/Grok video, HeyGen, Higgsfield, Replicate/Seedance, local GPU como alternativa sem API mas com custo de hardware.
- Avatar/gateway: HeyGen parece especialmente relevante para avatar/vídeo, mas precisa teste e custo por minuto/segundo.
- Música/SFX: ElevenLabs e Suno via `sunoapi.org`; tratar Suno como zona de cautela porque o tool do OpenMontage chama um provedor terceiro, não necessariamente uma API pública oficial da Suno.
- Stock gratuito com chave: Pexels, Pixabay, Unsplash. Ainda assim exigem leitura de licença, limites e regras de uso/cache/atribuição.

Fontes de referência pesquisadas:

- ElevenLabs API pricing: https://elevenlabs.io/pricing/api
- Google Cloud TTS pricing: https://cloud.google.com/text-to-speech/pricing
- Google Gemini/Imagen pricing: https://ai.google.dev/gemini-api/docs/pricing
- OpenAI API pricing: https://developers.openai.com/api/docs/pricing
- fal.ai pricing e páginas de modelos: https://fal.ai/pricing
- Runway API pricing: https://docs.dev.runwayml.com/guides/pricing/
- HeyGen API pricing: https://help.heygen.com/en/articles/10060327-heygen-api-pricing-explained
- xAI/Grok API pricing: https://docs.x.ai/developers/pricing
- Pexels API: https://www.pexels.com/api/
- Pixabay API: https://pixabay.com/api/docs/

Pesquisa específica: HeyGen voz nativa vs áudio externo para lip-sync

- Fonte oficial HeyGen `POST /v3/videos`: o endpoint cria vídeo a partir de avatar ou imagem e suporta tanto `script` quanto áudio pré-gravado para lip-sync.
- No modo com texto, usa-se `script` + `voice_id`; se `avatar_id` tiver voz padrão, `voice_id` pode ser omitido.
- `script` é mutuamente exclusivo com `audio_url`/`audio_asset_id`. Ou seja: ou HeyGen gera a fala a partir do texto, ou o usuário fornece áudio externo para lip-sync.
- HeyGen também possui Text-to-Speech próprio (`POST /v3/voices/speech`) com `voice_id`, duração e word timestamps. Aceita `locale`, incluindo formato como `pt-BR`.
- HeyGen possui endpoint de Lipsync separado (`POST /v3/lipsyncs`) para trazer vídeo e áudio próprios; a própria documentação descreve esse modo como "engine only": o usuário traz o áudio e o motor redesenha a boca para corresponder.
- A documentação oficial não afirma que áudio externo de ElevenLabs fica pior que voz nativa HeyGen. A evidência documentada é: os dois modos são suportados, têm fluxos diferentes e custos diferentes.
- Preço oficial HeyGen self-serve pesquisado: Avatar IV Photo Avatar `US$0.05/s`; Avatar IV Digital Twin/Studio `US$0.0667/s`; Avatar III Digital Twin/Studio `US$0.0167/s`; Lipsync Speed `US$0.0333/s`; Lipsync Precision `US$0.0667/s`; TTS Starfish `US$0.000667/s`.
- ElevenLabs API pricing pesquisado: TTS `US$0.05` a `US$0.10` por 1.000 caracteres, dependendo do modelo.
- Conclusão de evidência: não dá para dizer, sem teste ou documentação comparativa explícita, que HeyGen nativo terá melhor lip-sync que ElevenLabs+HeyGen. Dá para dizer que HeyGen nativo é um fluxo operacional mais simples porque usa um endpoint e não exige áudio externo/hospedagem/upload; ElevenLabs+HeyGen é um fluxo mais composto que pode valer se a voz ElevenLabs for escolhida como identidade de canal.
- Decisão ainda não tomada: escolher voz nativa HeyGen ou voz externa depende de prioridade entre simplicidade operacional, qualidade/identidade da voz em português BR, custo por minuto e reutilização da mesma voz fora do avatar.

Pesquisa específica: HeyGen e Kling mais atual no OpenMontage

- HeyGen deve ser pensado primeiro como ferramenta de avatar/lip-sync/composição de presença humana, não como motor para preencher todo o tempo do vídeo. Como o custo é por segundo/minuto de saída, usar avatar por muitos minutos encarece rapidamente; o desenho econômico deve privilegiar trechos curtos, comentários-chave, abertura/fechamento e reaproveitamento quando possível.
- O `heygen_video` local do OpenMontage é um gateway genérico de vídeo via HeyGen, não o núcleo do avatar religioso. O avatar religioso se aproxima mais dos fluxos HeyGen de avatar/lip-sync (`/v3/videos`, `/v3/lipsyncs` ou o legado `/v2/video/generate`) combinados com Remotion/OpenMontage para composição final.
- Para Kling atualizado, a rota mais direta no OpenMontage é `FAL_KEY` via `kling_video`. O tool local já possui `model_variant="v3/standard"`, além de variantes 2.1, mas ainda não expõe todos os endpoints atuais do fal, como Kling v3 Turbo e Kling O3.
- Evidência atual: fal.ai expõe Kling v3 Turbo, Kling V3 e Kling O3, com preços por segundo. Kling v3 Turbo Standard aparece como `US$0.112/s`; O3 Pro aparece como `US$0.112/s` com áudio off e `US$0.14/s` com áudio on; V3 Pro aparece como `US$0.112/s` áudio off, `US$0.168/s` áudio on e `US$0.196/s` com voice control.
- A documentação oficial Kling 3.0 informa suporte a até 15s, multi-shot, referência de elementos e áudio nativo, mas o áudio nativo lista chinês, inglês, japonês, coreano e espanhol; portanto, para conteúdo PT-BR, a hipótese operacional econômica é usar Kling sem áudio nativo e adicionar voz/narração em separado.
- Higgsfield também aparece no OpenMontage como `higgsfield_video` e declara `kling_3.0`, mas depende de `HIGGSFIELD_API_KEY` + `HIGGSFIELD_API_SECRET`, parece mais próximo de assinatura/orquestrador multi-modelo e tem menos transparência local de endpoint/preço do que fal para nosso primeiro teste técnico.
- Conclusão provisória: para "Kling mais atual" dentro do OpenMontage, priorizar fal.ai como base técnica. Quando chegar a hora de testar, pode ser necessário adaptar o `kling_video.py` para expor `v3/turbo/*`, `v3/pro/*`, `o3/*`, `reference-to-video`, `generate_audio=false` por padrão e o mapeamento correto de campos (`start_image_url` vs `image_url`).

Configuração de chaves em 2026-07-10:

- Chaves coletadas por janela segura da skill global `sensitive-input-collector`, sem colar segredo no chat.
- Gravadas no `.env` do OpenMontage: `PEXELS_API_KEY`, `PIXABAY_API_KEY`, `ELEVENLABS_API_KEY`, `HEYGEN_API_KEY`, `FAL_KEY`.
- O OpenMontage passou a marcar como disponíveis: Pexels/Pixabay para stock, ElevenLabs para TTS, HeyGen para vídeo/gateway, fal.ai para Kling/Veo/MiniMax/Seedance/FLUX/Recraft.
- Nenhuma geração paga foi executada nessa validação. Foi feita apenas validação local de configuração/status para evitar gasto/cota.
- Observação: `music_gen` também aparece disponível por causa da ElevenLabs, mas a decisão atual continua sendo começar música por stock/biblioteca com licença limpa.

## Estado atual: YouTube/yutu

Data: 2026-07-10.

- `yutu` foi instalado via `winget`, pacote `eat-pray-ai.yutu`, versão `0.10.9`.
- Validação local feita por caminho absoluto: `yutu 0.10.9 windows/amd64`, build `OpenWaygate-2026-06-21T10:38:47Z`.
- O shell atual pode não reconhecer `yutu` até reiniciar/abrir um novo terminal, porque o `winget` alterou PATH/alias durante a instalação.
- Caminho validado do binário: `C:\Users\Vivia\AppData\Local\Microsoft\WinGet\Packages\eat-pray-ai.yutu_Microsoft.Winget.Source_8wekyb3d8bbwe\yutu.exe`.
- Conexão com YouTube fica pendente. Não rodar `yutu auth`, não configurar OAuth e não coletar `client_secret.json`/`youtube.token.json` até o usuário pedir explicitamente.
- Agent mode do yutu não está em uso. Não configurar `YUTU_LLM_API_KEY`, `YUTU_ADVANCED_MODEL` ou `YUTU_LITE_MODEL` para este bloco.
- Próximo uso possível, quando chegar a hora: autenticar via OAuth com janela segura para segredos, testar comandos read-only, e só depois pensar em upload/thumbnail/metadata.

## Como o Codex deve agir

Voltar ao chat antes de estruturar demais.

Organizar sem engessar. Questionar sem travar. Registrar só o que precisa virar memória. Pesquisar quando depender de fato externo. Perguntar quando depender de decisão do usuário.

Quando algo cristalizar, atualizar este arquivo.

## Restricao operacional: Unicode em narracao PT-BR

Data: 2026-07-11.

- Foi confirmado que scripts Python enviados pelo pipe textual do PowerShell converteram caracteres nao ASCII em `?` antes da chamada de TTS.
- O texto correto continha `nao`, `ja`, `esta` e `fe` com acentos, mas o Python recebeu `n?o`, `j?`, `est?` e `f?`; por isso a ElevenLabs pronunciou trechos de forma estranha.
- As primeiras tomadas de Brian e Fernando Borges feitas por esse caminho sao invalidas para avaliacao de voz.
- Para texto PT-BR, nao usar PowerShell pipe -> Python com caracteres literais. Usar arquivo UTF-8, payload JSON estruturado ou escapes Unicode ASCII (`\uXXXX`).
- Antes de qualquer chamada paga de voz, validar que o texto nao contem `?` substituto e conferir os pontos de codigo dos caracteres acentuados.

## Voz PT-BR aprovada: Bruno Cardoso

Data: 2026-07-11.

- Voz adicionada a colecao ElevenLabs: `Bruno Cardoso`, voice id `iF2QszmZhlyFLleUoFxy`.
- Metadados verificados: homem brasileiro, pt-BR, middle-aged, sotaque brazilian, perfil confident.
- A voz foi aprovada pelo usuario como identidade de narracao depois de comparacao cega entre tres vozes e tres movimentos narrativos. Na calibracao, `Voz A` correspondia a Bruno Cardoso.
- O problema do primeiro piloto nao era apenas a identidade vocal. A mesma voz melhorou de forma clara quando recebeu roteiro de performance, grandes unidades semanticas, contexto anterior/posterior, `language_code=pt`, stability `0.50`, similarity `0.75`, style `0`, speed `1.0` e pausas intencionais.
- Metodo aprovado para producao: gerar grandes blocos contiguos com Request Stitching, montar automaticamente e pedir ao humano apenas aprovacao/reprovacao do audio completo ou de um bloco inteiro. Nao criar processo normal de remendos frase a frase.
- Regra fixa de encerramento do canal: depois de concluir a mensagem, apontar para outro video que aparece na tela, pedir inscricao, curtida e compartilhamento e terminar com uma pergunta/reflexao especifica do episodio para incentivar comentarios. A estrutura e fixa; a pergunta final e contextual e nao deve ser repetida mecanicamente.
- Reforco operacional de 2026-07-27: se a narração aprovada não direcionar claramente para próximos vídeos, não regenerar voz só por isso sem necessidade; completar obrigatoriamente na tela final, descrição, elementos nativos do YouTube e comentário fixado. Em todo pacote de publicação de longo, verificar quatro itens de CTA: inscrição/curtida/compartilhamento, pergunta de comentário, dois próximos vídeos recomendados e comentário fixado do canal.
- Direção de thumbnails reforçada em 2026-07-27: capas conceituais podem existir, mas normalmente devem ter algum ponto humano/personagem quando isso aumentar conexão emocional. Em temas bíblicos, não inserir anjos, figuras divinas ou cenas sobrenaturais se o roteiro/texto bíblico não sustentar isso; preferir pessoa humana discreta, silhueta, mãos com Bíblia ou olhar para luz/horizonte.
- Modelos listados para a voz: `eleven_multilingual_v2`, `eleven_turbo_v2_5`, `eleven_v2_5_flash`, `eleven_flash_v2_5`, `eleven_multilingual_sts_v2`.
- Correcao apos o audio 002: 42 tags `<break>` em oito blocos, somando 34,9 segundos de pausas cronometradas, produziram ritmo artificial e foram reprovadas pelo usuario. A documentacao da ElevenLabs alerta que excesso de break tags pode causar instabilidade. Regra atual: em narracao longa com Multilingual v2, controlar o ritmo primeiro por estrutura semantica, pontuacao natural e Request Stitching. Pausa cronometrada vira excecao justificada, deve ser contada no preflight e nao pode ser espalhada mecanicamente entre todos os paragrafos.
- Regra de referencia biblica falada: toda vez que a narracao identificar um versiculo, deve dizer livro, capitulo e versiculo de forma completa. Nao mencionar apenas `versiculo vinte e cinco` confiando que o ouvinte lembrara o livro e o capitulo. Para evitar redundancia, apresentar a referencia completa uma vez imediatamente antes da leitura, em vez de dar referencia incompleta antes e repeti-la depois.

## Correcao de custo: avatar como assinatura, nao como base visual

Data: 2026-07-11.

- O avatar animado nao sera o preenchimento padrao dos videos medios do canal religioso. O custo por segundos de HeyGen e a qualidade observada tornam esse uso incompativel com o piloto economico.
- A base visual passa a ser narracao separada, texto biblico e frases-chave legiveis, stock selecionado e imagens geradas apenas para lacunas que o stock nao resolver.
- O avatar aprovado continua como ativo de marca para thumbnails e materiais visuais, mas nao deve aparecer de forma estatica dentro do video. Quando entrar no episodio, deve ser animado, falado e ter funcao editorial clara. Qualquer nova renderizacao animada exige decisao e aprovacao explicita por episodio.

## Evidencia tecnica: HeyGen Photo Avatar de mesa

Data: 2026-07-11.

- O retrato limpo de mesa aprovado foi aceito pelo HeyGen como Photo Avatar, com dimensoes registradas de 1122x1402.
- A primeira chamada de video com `aspect_ratio: 9:16` e `fit: contain` falhou com a mensagem incorreta de "missing image dimensions". A imagem tinha dimensoes validas; nao tratar essa resposta como defeito do arquivo sem antes verificar o avatar registrado.
- Reutilizar o mesmo avatar com `aspect_ratio: auto`, sem `fit`, concluiu o microteste de 9,36 segundos. A saida foi 720x900 (4:5), coerente com a proporcao do retrato.
- Para Photo Avatars futuros, comecar pelo `aspect_ratio: auto` recomendado pela documentacao. Solicitar 16:9 ou 9:16 apenas quando houver uma necessidade concreta de composicao e depois de teste pequeno.

## Piloto editorial escolhido

Data: 2026-07-11.

- Tema/titulo de trabalho do primeiro piloto: `Voce nao precisa carregar tudo sozinha`.
- Pautas reservadas para videos futuros: `O que Jo ensina quando a vida parece injusta` e `Nao andeis ansiosos: o que Jesus realmente quis dizer`.
- Pautas sugeridas por Layane em 2026-07-21, preservadas como sementes editoriais: infância de Jesus; tentações; narrativas dos Evangelhos; criação em Gênesis; personagens bíblicos contados por história e conflito; Apocalipse, selos, falso profeta e anticristo. O vídeo 004 foi escolhido como `O que a Bíblia revela sobre a infância de Jesus — e o que ela não conta`, uma mudança deliberada para narrativa bíblica e curiosidade textual. A linha de Apocalipse fica reservada para pesquisa e delimitação denominacional antes de qualquer roteiro; ela não deve ensinar a identificar pessoas, governos ou eventos atuais como se o texto bíblico oferecesse esse diagnóstico.
- Grade editorial decidida em 2026-07-27 para os 7 longos novos ate 15/08: `video-005` sera Genesis/criacao; depois Marta e Maria; tentacoes de Jesus; Pedro negou Jesus; mulher samaritana; Jesus acalma a tempestade; filho prodigo. Como acabou de sair um video sobre Jesus, temas em que Jesus e o foco principal foram espaçados. Fonte operacional: `operations/a-palavra-que-cuida/01_briefs/grade-editorial-2026-07-27-a-2026-08-15-v1.md`.
- Ainda nao definir versiculo central, estrutura, duracao, roteiro ou custo do piloto sem pesquisa e decisao especificas.

## Regra editorial e controle ACF

Data: 2026-07-11.

- Um roteiro pode ter um texto biblico principal e citar outros trechos de apoio quando isso for necessario para contexto, argumento ou nao redundancia. Referencias de apoio nao devem virar uma lista decorativa de versiculos.
- A SBTB permite citar ate 1.100 versiculos ACF sem autorizacao previa, desde que nao formem livro completo nem 50% da obra que os menciona, e exige atribuicao. O termo publico nao esclarece o escopo desse teto entre obras diferentes.
- Como politica interna conservadora, a fabrica nao ultrapassara 1.000 unidades de versiculo ACF em todas as saidas publicadas sob seu controle sem autorizacao escrita da SBTB. A regra abrange canais diferentes; abrir outro canal nao reinicia nem multiplica o teto. Cada versiculo citado direta e parcialmente conta uma vez por saida publica; um short ou republicacao separada conta de novo. O registro e o preflight ficam em `operations/a-palavra-que-cuida/08_publicacao/`.

## Biblia Livre para leitura integral

Data: 2026-07-11.

- O usuario escolheu a Biblia Livre (BLIVRE) como candidata aprovada para a futura linha de leitura integral. O PDF sera enviado pelo usuario e deve ser guardado como material-fonte do canal.
- A versao e uma atualizacao brasileira da Almeida de 1819, edicao Textus Receptus, licenciada em CC BY 4.0. A atribuicao indicada pelo licenciante deve acompanhar cada video que use o texto, na descricao ou em local equivalente.
- Credito de referencia: `Todas as Escrituras em portugues citadas sao da Biblia Livre (BLIVRE), Copyright © Diego Santos, Mario Sergio e Marco Teles. Licenca Creative Commons Atribuicao 4.0.`
- Esta decisao resolve a licenca da leitura integral, mas nao substitui automaticamente a ACF nos episodios comentados. O piloto 001 continua com ACF ate nova decisao explicita do usuario.

## Lancamento do piloto 001 e divida de qualidade

Data: 2026-07-19.

- O usuario autorizou publicar o piloto 001 na versao mais proxima do concluido, mesmo sem tratar a edicao como padrao definitivo do canal. O primeiro envio deve passar como nao listado para checagem da plataforma antes da visibilidade publica.
- Melhorias obrigatorias para os proximos episodios: sincronizacao mais precisa entre fala e textos, mascara/recorte natural do avatar e da mesa, melhor integracao do avatar ao cenario, selecao de cenas com maior identificacao e distribuicao mais criteriosa dos segundos de video gerado.
- Nao usar a imperfeicao do piloto como permissao para repetir defeitos conhecidos. O piloto serve como linha de base para medir e melhorar.
- Regra visual de embalagem: toda thumbnail do canal deve conter uma frase curta e chamativa, legivel em tamanho pequeno, com boa iluminacao, cores vivas mas sobrias e contraste adequado ao publico do canal. A frase deve complementar o titulo e o tema, nao virar clickbait sem entrega.

## Aprendizados aprovados apos o piloto 001

Data: 2026-07-21.

- O usuario aprovou a direcao geral do piloto 001 e destacou positivamente os cenarios reconhecivelmente brasileiros. Essa direcao de cotidiano brasileiro deve ser preservada nos proximos episodios.
- Nova regra visual: objetos que naturalmente carregam texto, como rotulos de medicamentos, cadernos, cartazes, embalagens e telas, nao devem aparecer vazios ou com escrita sem sentido. O conteudo deve ser legivel e coerente com a cena. Se a geracao nao produzir texto confiavel, reenquadrar, substituir o objeto ou aplicar o texto durante a composicao.
- O video 002 foi escolhido: `Nao andeis ansiosos: o que Jesus realmente quis dizer`, no subtipo versiculo comentado.
- A publicacao do piloto 001 esta temporariamente bloqueada porque a conta Google `apalavraquecuida@gmail.com` foi desativada. A contestacao foi enviada ao Google em 2026-07-21. O master, a thumbnail e os metadados permanecem prontos; retomar o OAuth do yutu somente depois da restauracao da conta.
- Regra de duracao do canal: todo video medio deve ter master final de no minimo 10 minutos. A pauta e o roteiro devem sustentar essa duracao sem repeticao, enrolacao ou alongamento artificial. O alvo de narracao precisa deixar margem para o master permanecer acima de 10 minutos depois da edicao.
- Regra de economia visual: stock pode ser usado quando tiver correspondencia forte com o contexto narrado. Economia nao autoriza imagem generica, imprecisa ou desconectada. Quando stock nao representar a ideia com precisao, priorizar imagem/video gerado ou outra composicao adequada.
- A permissao de inserir mid-rolls comeca atualmente em videos monetizados de 8 minutos ou mais. A duracao de 10 minutos e uma decisao editorial de margem e espaco narrativo; nao garante que o YouTube servira mais anuncios, pois os slots sao apenas oportunidades de veiculacao.
- Regra de apresentacao de midia local: sempre que o Codex quiser mostrar ao usuario onde esta uma imagem, audio ou video produzido, deve abrir o Explorador de Arquivos nativo do Windows na pasta correspondente, de preferencia com o arquivo selecionado. Link local no chat nao substitui essa acao e nao deve ser a forma principal de entrega.

## Audio aprovado do video 002

Data: 2026-07-21.

- A narracao v2 de `Nao andeis ansiosos: o que Jesus realmente quis dizer` foi aprovada pelo usuario. O metodo sem tags `<break>`, apoiado em pontuacao natural, blocos semanticos e Request Stitching, produziu uma leitura claramente melhor e passa a ser a referencia atual para narracoes longas com a voz Bruno Cardoso.
- Correcao do video 003: voz, modelo e Request Stitching nao bastam para generalizar o resultado entre roteiros. O contrato de performance armazenado no manifesto nao controla a API se nao fizer parte dos parametros realmente enviados. A primeira narracao de Jo passou em integridade textual e loudness, mas foi reprovada por leitura sem compreensao, entonacao e hierarquia. A tentativa de correcao v2 nao isolou a capacidade da voz: ela supersegmentou a fala em microfrases e, por isso, nao prova incapacidade de Bruno Cardoso + Multilingual v2. No payload da calibracao nao havia prompt de atuacao, contexto longo, caracteres ocultos nem Request Stitching; overprompting e rotten context foram descartados para esse teste. A causa da narracao integral v1 continua aberta; ancoragem de uma cadencia ruim pelo Request Stitching e apenas hipotese. Antes de trocar de motor, fazer um A/B pequeno com escrita oral continua, mantendo o restante fixo. QA tecnico aprovado nunca pode ser chamado de audio aprovado sem o crivo semantico humano. Pesquisa pratica: `operations/a-palavra-que-cuida/01_briefs/pesquisa-pratica-prosodia-tts-2026-v1.md`.
- Escrita oral v0.1: pontuacao deve continuar gramatical e o ritmo deve nascer de sintaxe, conectivos, ordem das informacoes e paragrafos semanticamente completos. Ponto encerra ideia completa; listas nao viram cascatas de microfrases para forcar enfase. Reticencias, travessoes repetidos, caixa alta e tags de pausa ficam proibidos por padrao. O preflight local alerta acima de 15% de frases com ate quatro palavras ou tres frases consecutivas com ate sete; esses limites vieram do contraste com o video 002 aprovado e nao sao regra universal. O primeiro bloco precisa ser aprovado antes de alimentar Request Stitching. A amostra v3 foi preparada sem chamada paga em `operations/a-palavra-que-cuida/02_roteiros/video-003-calibracao-performance-v3.json`.
- Em 2026-07-23, a amostra v3 foi aprovada pelo crivo humano com a mesma voz, modelo, seed e configuracoes. A mudanca isolada da escrita confirmou a supersegmentacao como causa principal da falha da calibracao v2. O metodo deve ser aplicado ao roteiro integral, mas a narracao completa continua bloqueada ate o preflight textual e a aprovacao humana do primeiro bloco reescrito.
- A fala termina em 658,194 segundos. O master de producao recebeu localmente 3 segundos de silencio ao final e ficou com 661,193 segundos. Nao houve regeneracao nem novo custo de ElevenLabs.
- Regra de fechamento: preservar alguns segundos depois da ultima fala para a end screen continuar utilizavel e para o audio terminar sem corte seco.
- Para o video 002, textos e trocas visuais devem ser sincronizados pelos alinhamentos por caractere da ElevenLabs, nao por estimativa livre.
- Correcao do avatar: a fonte vertical usada no piloto carregou um retangulo estreito de mesa para o quadro 16:9. Antes de novo HeyGen, preparar e aprovar uma fonte 16:9 com a mesa atravessando toda a largura; nao repetir o recorte quadrado.
## Video 002 - master produzido

- Em 2026-07-21, o video `Nao andeis ansiosos: o que Jesus realmente quis dizer` foi montado em 1080p com duracao final de 11:01.248.
- O metodo visual aprovado para este video combina imagens geradas precisas, stock apenas quando literal, movimento pago reservado a acoes humanas e avatar somente quando ele fala.
- A fonte 16:9 do avatar com mesa de ponta a ponta resolveu o recorte retangular observado no piloto.
- Objetos que naturalmente carregariam texto, como envelopes e cadernos, devem receber escrita legivel na composicao ou sair de quadro.
- A tela visual recomendada pode surgir durante a fala; o elemento nativo do YouTube deve ocupar exatamente os 20 segundos finais permitidos pela plataforma.
- Custo conservador da producao visual externa: US$ 4.171, abaixo do teto aprovado de US$ 4.28, sem retentativa paga automatica.

## Correcao editorial apos a reprovacao da primeira montagem do video 002

- Nao interpretar "o objeto precisa ter texto" como autorizacao para achatar tipografia por cima de papel, caderno, embalagem, remedio, envelope ou tela. Se o objeto exige escrita, ela precisa parecer fisicamente pertencente ao objeto, com perspectiva, material, oclusao e iluminacao coerentes. Se isso nao puder ser feito com qualidade, trocar a imagem ou retirar o objeto.
- Economia de recursos so e valida enquanto nao compromete variedade, precisao contextual ou qualidade percebida.
- Evitar planos estaticos longos e repeticao excessiva do mesmo asset. Como referencia inicial para montagens desse formato, trabalhar principalmente com planos de 4 a 8 segundos; planos acima de 12 segundos precisam de motivo claro, movimento real ou mudanca interna de enquadramento.
- Usar stock gratuito quando houver correspondencia literal e boa qualidade. Nao limitar stock a natureza.
- Figuras e cenas biblicas podem e devem aparecer quando pertencem ao argumento, por exemplo Jesus ensinando, o Sermao do Monte e ouvintes do contexto. Tratar essas imagens como reconstrucao visual, sem inventar que uma interacao especifica consta do texto biblico quando isso nao estiver evidenciado.
- A identidade brasileira continua importante nas aplicacoes contemporaneas, mas nao deve transformar todo o video numa sequencia da mesma mulher, da mesma cozinha e da mesma sala.

## Biblioteca central de imagens geradas

- As imagens geradas reutilizaveis do canal ficam centralizadas em `operations/a-palavra-que-cuida/04_assets/biblioteca_imagens/`, sem remover os originais dos projetos em que nasceram.
- O acervo e deduplicado por SHA-256 e separado entre imagens atuais e legado util. Origem, dimensoes, categoria, estado e motivo de exclusao ficam em `catalogo.json`.
- Folhas de QA, contact sheets, screenshots e frames derivados nao contam como ativos-fonte.
- Imagens explicitamente reprovadas nao entram na biblioteca curada. A exclusao permanece registrada para impedir reutilizacao acidental, especialmente cadernos/papeis vazios, medicamentos sem rotulo e composicoes com texto achatado sobre objetos.

## Video 002 - remontagem v2

- O v1 reprovado foi preservado apenas como referencia. A v2 foi reconstruida em composicao separada, com 124 planos, media estatica de 5,16 segundos e nenhum plano de imagem acima de 7,02 segundos.
- A v2 removeu o caderno vazio, o orcamento sem rotulos e todas as sobreposicoes que fingiam pertencer fisicamente a objetos. Os envelopes aprovados usam texto integrado na propria imagem.
- Cenas de Jesus, Sermao do Monte e Galileia passaram a ocupar os trechos biblicos; cotidiano brasileiro e apoio humano ocupam as aplicacoes contemporaneas.
- End screen: os 600 frames finais, equivalentes a 20 segundos, ficam reservados ao video recomendado. Depois da ultima fala ha cerca de 3,264 segundos de respiro e fade, sem avatar estatico.
- A revisao reutilizou ativos existentes e nao fez nova chamada paga. O master local esta em `operations/a-palavra-que-cuida/07_exports/video-002/nao-andeis-ansiosos-v2.mp4` e foi aprovado pelo usuario para publicacao com dividas de qualidade registradas abaixo.
- Limite tecnico observado: videos stock e avatar tornam o render 1080p no Remotion muito mais lento que planos de imagem. Investigar proxy/intraframe ou montagem hibrida com FFmpeg antes de fixar a estrategia da esteira.

## Feedback humano cristalizado depois do video 002

- O video 002 v2 foi aprovado para publicacao sem nova revisao, para poupar creditos. Essa aprovacao aceita defeitos especificos do episodio e nao transforma esses defeitos em padrao para os proximos.
- Texto diegetico precisa parecer realmente impresso, escrito, gravado ou exibido no objeto. Legibilidade e perspectiva sozinhas nao bastam. A composicao deve reproduzir curvatura da superficie, textura e porosidade do material, mistura de tinta, desgaste, foco, granulado, iluminacao, sombra, reflexo e oclusao. Uma camada 2D limpa por cima de carta, correspondencia, embalagem, caderno, rotulo ou tela esta reprovada.
- Se texto diegetico nao puder passar por uma verificacao aproximada em tamanho grande, o objeto deve sair de quadro, ser reenquadrado ou ser substituido. Nao gastar creditos repetindo uma solucao que continua parecendo colagem.
- Proibicao visual absoluta do canal: nao usar papel, folha, pagina, carta ou caderno em branco como cena de apoio. Mesmo quando um papel vazio seria plausivel na realidade, essa imagem foi considerada feia e com aparencia de producao inacabada. Usar outro objeto ou enquadramento; se a cena realmente exigir escrita, ela deve nascer integrada ao material com qualidade suficiente, nunca como tipografia achatada por cima.
- Regra biblica absoluta para os proximos videos: toda vez que um versiculo for citado, falado ou lido, a referencia apresentada precisa conter livro, capitulo e versiculo. Nao confiar em contexto anterior e nao mostrar somente `versiculo X`.
- Quando a narracao ou o avatar ler um versiculo, todo o texto efetivamente lido deve aparecer na tela, sem abreviacao nem corte. Se nao couber com legibilidade, dividir em blocos consecutivos sincronizados, preservando todas as palavras e mantendo a referencia completa visivel em cada bloco.
- Antes do render, comparar a transcricao do trecho biblico com o grafismo palavra por palavra. A fala, o texto exibido e a versao biblica registrada precisam coincidir.
- Repeticao visual deve diminuir conforme o acervo cresce. Antes da montagem, contar reutilizacoes por ativo e ampliar o conjunto com stock preciso ou novas geracoes. Repetir somente quando houver funcao editorial clara; falta de material nao pode virar repeticao silenciosa por padrao.
- Decisao cristalizada de tela final para todos os proximos videos: reservar dois espacos visuais para recomendacoes e configurar exatamente dois elementos nativos de video no YouTube. Um deve ser a continuacao tematica prioritaria escolhida pelo canal; o outro, uma alternativa relevante para o espectador. O CTA deve falar no plural ou permitir naturalmente que o espectador escolha entre as duas opcoes.
- Regra universal reforcada pelo usuario em 2026-07-29: todo video longo publicado no YouTube, de qualquer canal atual ou futuro, deve ter exatamente dois videos recomendados por elementos nativos na tela final. Prever dois espacos no master nao basta: a publicacao so pode ser considerada concluida depois de configurar e verificar os dois destinos no YouTube Studio/player publico. Se a verificacao nao ocorrer, manter o video bloqueado, nao concluido ou explicitamente pendente; nao tratar pendencia manual como sucesso.
- Aplicacao retroativa e prospectiva definida pelo usuario em 2026-07-29: auditar todos os videos longos ja publicados em todos os canais e corrigir, quando houver acesso operacional, os que estiverem sem os dois elementos nativos. A ausencia nao e excecao editorial nem deve ser repetida em canais futuros.
- Regra universal de tela final, decidida em 2026-07-29: em todos os canais do YouTube, os dois elementos nativos devem apontar para o video imediatamente anterior ao episodio e para o video mais recentemente publicado no canal no momento da publicacao. A narração nunca deve citar titulos, personagens ou temas especificos dos cards; deve apenas orientar o espectador a escolher um dos videos exibidos. A selecao deve ser atualizada por episodio, sem presumir que o video assistido seja o mais recente, e sem prometer uma recomendacao que possa ficar arquivada, indisponivel ou desatualizada.
- Aplicacao operacional da regra de 2026-07-29: o video 010 ja teve a narracao gerada com a CTA especifica anterior e nao sera regravado sem nova aprovacao de custo; a regra generica passa a ser obrigatoria a partir do video 011 e em todos os canais futuros.
- Nao usar tres ou quatro recomendacoes por padrao. Uma quantidade maior so podera entrar como teste futuro, sustentado por catalogo realmente pertinente e pelas metricas de clique dos elementos da tela final.
- Evidencia de plataforma verificada em 2026-07-21: o YouTube permite tela final nos ultimos 5 a 20 segundos e ate quatro elementos em video 16:9; portanto, duas recomendacoes de video sao suportadas. Fonte oficial: https://support.google.com/youtube/answer/6388789?hl=pt-br
- Excecao explicita: nao remontar o video 002 para aplicar a tela dupla ou corrigir as dividas acima. As regras comecam no proximo video.

## Distribuicao no YouTube: clique qualificado

- O objetivo comercial continua sendo maximizar receita, mas o projeto nao otimizara clique isolado. A unidade operacional e o clique qualificado: impressao, clique, cumprimento da promessa, permanencia, satisfacao e proxima visualizacao.
- Tema, titulo, thumbnail, abertura, roteiro, narracao, imagens e fechamento precisam sustentar a mesma promessa. CTR alto com baixa duracao media e poucas impressoes pode indicar clickbait ou desalinhamento, nao sucesso.
- Para busca, pesquisar termos antes de publicar com a aba Pesquisa do YouTube Analytics, autocomplete em `pt-BR`, Google Trends/Keyword Planner e, depois da publicacao, os termos reais de busca do canal. Autocomplete evidencia formulacoes, nao volume exato.
- Descricoes serao unicas, com uma ou duas expressoes principais nas primeiras linhas, variacoes naturais no corpo, capitulos, fontes, creditos, CTA e duas ou tres hashtags pertinentes. Keyword stuffing esta proibido.
- Tags de video sao baixa prioridade e servem principalmente para grafias alternativas e erros comuns.
- Titulo e thumbnail devem ser avaliados juntos. Quando houver impressoes suficientes e recursos avancados, usar o teste A/B nativo do YouTube, cujo vencedor e escolhido por tempo de exibicao, nao CTR isolado.
- Metricas devem ser lidas por origem de trafego e em conjunto. Nao adotar meta universal de CTR, retencao ou horario sem dados do proprio canal e de videos comparaveis.
- Pesquisa e aplicacao do video 002 registradas em `operations/a-palavra-que-cuida/01_briefs/estrategia-distribuicao-youtube-v0.1.md`.
- Familia futura de testes temporais aprovada pelo usuario: `Se esta mensagem apareceu para voce hoje, [data], ouca ate o fim`; `Uma palavra para voce hoje, [data]: voce nao esta sozinha`; `Antes de dormir nesta [dia da semana], voce precisa ouvir isto`; `Talvez voce tenha encontrado esta mensagem no momento certo`. Testar primeiro uma unica variacao em conteudo que cumpra a promessa. Se houver melhora sustentada de clique qualificado, retencao inicial, tempo de exibicao por impressao e satisfacao contra videos comparaveis, testar as demais com espacamento. Nao promover toda a familia por CTR isolado nem afirmar selecao divina ou pessoal pelo algoritmo.

## Pacotes de publicacao dos videos 001 e 002

- Em 2026-07-21, tudo que podia ser concluido localmente para os dois primeiros videos foi fechado em `operations/a-palavra-que-cuida/08_publicacao/`.
- Os manifestos canonicos sao `piloto-001-publicacao-v1.json` e `video-002-publicacao-v1.json`. Eles preservam titulo, descricao, capitulos exatos, tags, hashtags, comentario fixado, arquivos, hashes, tela final, controle ACF e dividas aceitas de cada episodio.
- O video 002 recebeu legenda `pt-BR` baseada nos alinhamentos por caractere da narracao aprovada: 168 cues ate `657,984 s`, preservando o respiro final.
- O preflight local dos dois pacotes passou. Os rascunhos somam 8 unidades ACF, mas o registro publicado continua em 0 ate que cada video realmente se torne publico.
- Pendencias externas: restauracao da conta Google, OAuth do yutu, upload nao listado, IDs/URLs do YouTube, links cruzados, elementos nativos de tela final, processamento 1080p, checagem humana e confirmacao de visibilidade publica.

## Preparacao offline do canal no YouTube

- Antes da restauracao da conta Google, foram preparados o banner `2560x1440`, a foto de perfil ja aprovada, uma marca-dagua `300x300` abaixo de 1 MB, a descricao do canal, palavras-chave enxutas, a playlist inicial e a hipotese de pagina inicial.
- O manifesto canonico e `operations/a-palavra-que-cuida/08_publicacao/configuracao-canal-v1.json`; os comandos reais do yutu estao em `yutu-pos-restauracao-v1.md`.
- O yutu pode atualizar canal e banner, criar playlist, enviar videos, thumbnails e legendas, atualizar metadados, publicar comentarios e administrar marca-dagua depois do OAuth.
- A sintaxe preparada para canal, banner, playlist, video, thumbnail, legenda, comentario e marca-dagua passou no `--dry-run` local do yutu em 2026-07-21, sem chamada a API.
- Continuam humanos no YouTube Studio: handle, foto de perfil, telas finais, fixacao dos comentarios, pagina inicial e confirmacao da visibilidade publica.
- A marca-dagua esta pronta, mas nao deve ser ativada cegamente. Primeiro revisar em video nao listado se ela compete com textos ou telas finais.

## Guardrail de monetizacao do YouTube

- A politica atual do YouTube permite formatos recorrentes quando a substancia de cada episodio varia materialmente, mas barra conteudo generico, intercambiavel, repetitivo ou produzido em massa com pouco valor original.
- Os dois primeiros videos seguem a direcao permitida: roteiros, comentario, estrutura e edicao originais. Isso reduz risco conhecido, mas nao garante aprovacao futura no YPP.
- O video 002 tem um ponto de atencao por tratar de ansiedade. O narrador sintetico deve permanecer como narrador de reflexao biblica, nunca profissional de saude; nao diagnosticar, prescrever ou substituir atendimento.
- A futura ideia de leitura integral composta apenas por texto subindo e narracao tem alto risco de nao monetizacao: a politica cita leitura exclusiva de material nao criado e texto rolando/slideshow com pouco comentario. Nao produzir presumindo elegibilidade para anuncios.
- Marcar sempre a divulgacao de conteudo alterado ou sintetico. Segundo o YouTube, a divulgacao correta nao reduz por si mesma o alcance nem a elegibilidade para monetizacao.
- Politica e preflight registrados em `operations/a-palavra-que-cuida/01_briefs/politica-monetizacao-youtube-v1.md`.

## Legendas e TikTok

- Legendas em portugues revisadas sao obrigatorias em todos os videos, no YouTube e no TikTok. Acessibilidade nao e acabamento opcional.
- Cada video tera uma fonte canonica de sincronizacao, derivada da narracao aprovada. Dela saem o arquivo `.srt` do YouTube e as legendas incorporadas na versao vertical.
- Sons sem fala que forem importantes para compreender a cena tambem devem ser legendados de forma breve; efeitos meramente decorativos nao precisam poluir a leitura.
- No YouTube, entregar legenda fechada em `.srt` com idioma `pt-BR`; os textos editoriais na imagem e a exibicao integral dos versiculos continuam sendo elementos separados.
- No TikTok, entregar uma composicao propria em `9:16`, com legenda incorporada, legivel, sincronizada e dentro da area segura da interface.
- Nao recortar cegamente o master horizontal. Reaproveitar roteiro, audio, sincronizacao, imagens e videos, mas recompor os enquadramentos para o formato vertical.
- A recomposicao vertical e a adaptacao das legendas devem ser locais, com OpenMontage, Remotion ou FFmpeg, sem nova cobranca de ElevenLabs, HeyGen ou geracao visual, salvo quando um novo asset for realmente necessario.
- Os videos de TikTok terao pelo menos 65 segundos finais. Esse e um limite operacional conservador para nunca ficar abaixo do requisito de um minuto por arredondamento ou corte.
- TikTok serve tanto para descoberta e encaminhamento ao canal quanto para futura monetizacao; duracao, sozinha, nao garante elegibilidade no Creator Rewards.
- Conteudo realista gerado ou alterado por IA deve receber a identificacao exigida pelo TikTok.
- Cada video medio do YouTube deve ser planejado tambem como fonte de varios videos curtos. Roteiro e montagem precisam identificar antecipadamente trechos fortes, autocontidos e compreensiveis fora do episodio completo.
- O recorte de TikTok deve usar a parte mais chamativa, surpreendente, emocional ou provocadora do argumento: um "sensacionalismo" responsavel, que desperta curiosidade sem inventar, exagerar alem do que o episodio entrega ou romper o contexto biblico.
- Como o avatar aparece em momentos importantes, dar preferencia a recortes que incluam uma aparicao falada dele quando isso fortalecer reconhecimento, autoridade e continuidade visual do canal. Isso nao obriga todo curto a usar avatar.
- Um unico video medio pode e deve originar varios videos de TikTok quando houver mais de um trecho forte. Nao repetir a mesma ideia apenas para aumentar quantidade.
- Politica de selecao: primeiro marcar candidatos durante o roteiro; depois confirmar os melhores no audio aprovado e na montagem final. Cada recorte precisa ter gancho proprio, desenvolvimento minimo, conclusao ou ponte e CTA adequado.
- Politica operacional completa registrada em `operations/a-palavra-que-cuida/01_briefs/politica-legendas-e-tiktok-v1.md`.

## Musica e descoberta no TikTok

- No YouTube horizontal, trilha de fundo permanece opcional. Quando usada, deve acompanhar o arco emocional com sobriedade, nunca competir com a narracao e possuir licenca valida para o YouTube.
- No TikTok, musica passa a ser considerada por padrao em cada recorte. Pode cumprir funcao editorial de sentido, ritmo e retencao ou entrar como experimento controlado de associacao a uma tendencia. Nao usar faixa viral cujo titulo, letra, contexto ou publico associado prejudiquem a mensagem e a identidade do canal.
- A versao vertical deve sair da esteira com voz e efeitos preservados, mas sem incorporar uma musica exclusiva da biblioteca do TikTok. Perto da publicacao, o humano seleciona e adiciona a faixa dentro do proprio aplicativo, mantendo a associacao oficial ao som.
- A musica do TikTok nao deve ser exportada para YouTube ou outra plataforma. As licencas da biblioteca sao restritas ao uso permitido no TikTok.
- A conta do canal no TikTok deve permanecer Pessoal enquanto monetizacao pelo Creator Rewards for objetivo. Contas pessoais podem acessar programas de monetizacao e tanto a biblioteca geral quanto a Biblioteca de Musicas Comerciais; contas corporativas nao sao elegiveis ao Creator Rewards.
- Sons participam das informacoes usadas na recomendacao e na busca, mas o TikTok afirma que interacoes e tempo assistido normalmente pesam mais no feed Para Voce. Musica e alavanca secundaria, nao substituto para gancho, clareza, retencao e satisfacao.
- Antes de cada publicacao, pesquisar sons atuais no Brasil no aplicativo e no Creative Center. Avaliar adequacao semantica e religiosa, tendencia atual, publico dos videos associados, direitos disponiveis, risco de letra concorrente e compatibilidade com a voz.
- Correção sobre som de tendência: é permitido adicionar pelo próprio TikTok uma faixa em volume muito baixo, inclusive praticamente inaudível, apenas para testar a associação à página do som, desde que a licença e o sentido da faixa sejam adequados. Não há evidência oficial de impulso garantido nem de penalidade por esse uso. Relatos de 2026 indicam que o aplicativo pode remover sons detectados como baixos demais; por isso, verificar depois da publicação se a faixa permaneceu associada e comparar resultados com e sem essa técnica.
- Conteudo patrocinado ou que promova produto, servico ou marca de terceiro deve usar a Biblioteca de Musicas Comerciais ou musica com direitos comprovados. Nao presumir que uma faixa da biblioteca geral cobre uso comercial.
- Ativar a verificacao de direitos autorais de som no TikTok Studio antes de publicar. Se houver duvida sobre licenca, nao publicar com a faixa.
- Pesquisa e procedimento registrados em `operations/a-palavra-que-cuida/01_briefs/pesquisa-musica-distribuicao-tiktok-v1.md`.

## TikTok como aquisicao para o YouTube

- Prioridade comercial cristalizada: o YouTube e o destino principal de audiencia, relacionamento e receita. O TikTok funciona primeiro como canal de descoberta e aquisicao; a receita do TikTok e desejavel, mas secundaria.
- Visualizacoes no TikTok nao serao tratadas como sucesso isolado. O resultado procurado e uma sequencia mensuravel: consumo do recorte, visita ao perfil, passagem ao YouTube, consumo do video prometido, proxima visualizacao e inscricao.
- Todo recorte precisa entregar valor por si mesmo e, quando houver continuacao real, apontar para um video especifico no YouTube. Evitar CTA generico como `va ao meu YouTube`; nomear a pergunta que continua, o titulo pesquisavel e o canal `A Palavra Que Cuida`.
- O TikTok nao deve parecer um anuncio incompleto. A ponte usa curiosidade honesta: resolve uma parte da questao e deixa clara a profundidade adicional disponivel no video completo, sem esconder artificialmente a resposta prometida pelo proprio recorte.
- Manter nome, avatar, handle `@apalavraquecuida`, promessa e linguagem visual reconheciveis nas duas plataformas. Quando a conta permitir, ligar o YouTube no perfil do TikTok e verificar a visibilidade do link por outra conta ou sessao deslogada.
- Cada video medio deve nascer com candidatos de recorte associados ao proprio episodio. Os melhores tambem podem ser publicados como YouTube Shorts, usando o recurso nativo de video relacionado para levar ao video longo quando os recursos avancados estiverem habilitados.
- A pagina inicial do YouTube deve reduzir atrito para quem chega do TikTok: promessa clara, video ou secao de entrada e playlists tematicas. O conteudo citado no CTA precisa ser encontrado imediatamente.
- Metricas do funil serao lidas em conjunto: retencao e conclusao no TikTok, visitas ao perfil, cliques quando disponiveis, trafego externo no YouTube, desempenho do video de destino, espectadores recorrentes e origem das inscricoes. Nao adotar taxa universal antes dos dados do canal.
- Relatos atuais de criadores mostram resultados contraditorios: alguns obtiveram inscritos ao pedir a migracao, outros tiveram grande alcance no TikTok sem impacto perceptivel no YouTube. Isso confirma que conversao nao e automatica e que relato individual e hipotese operacional, nao regra do algoritmo.
- Metodo obrigatorio de pesquisa para distribuicao: consultar primeiro fontes oficiais atuais para capacidades, elegibilidade e politicas; depois investigar videos, minicursos publicos, Reddit e foruns recentes para praticas, incidentes e mudancas percebidas. Registrar data, pais, tipo de conta e natureza da evidencia. Confirmar alegacoes secundarias em fonte primaria quando possivel e deixar como hipotese quando nao for.
- Estrategia, evidencias e procedimento registrados em `operations/a-palavra-que-cuida/01_briefs/estrategia-aquisicao-tiktok-youtube-v1.md`.

## Decisão sobre a metamorfose

- Em 2026-07-22 foi escolhida a opção B: ainda não materializar o fluxo agêntico definitivo nem criar uma sucessão artificial de v1, v2 e v3.
- O casulo continuará registrando decisões, evidências, erros, capacidades aprovadas e lacunas. A metamorfose será iniciada quando a arquitetura conseguir representar tanto a gênese de novos canais quanto a produção dentro de cada canal, sem carregar hipóteses imaturas como regras universais.
- A camada metafísica, ou gênese de canal, é parte central do objetivo: imaginar uma tese de canal, captar sinais e oportunidades, pesquisar público e ecossistema, desenvolver posicionamento, amadurecer identidade e economia, desenhar pilotos, aprender com publicação e só então cristalizar a subesteira daquele canal.
- O foco imediato deve recair sobre as partes ainda negativas ou não validadas, em vez de reempacotar como skill aquilo que já funciona. O inventário atual está em `ai/preparacao-metamorfose.md`.

## Video 003 - reprovacao humana do master v2

Data: 2026-07-23.

- O master v2 de `O que Jo ensina quando a vida parece injusta` foi reprovado pelo usuario. O QA tecnico passou, mas isso nao equivale a aprovacao editorial, semantica ou visual.
- A narracao comeca melhor e volta a errar pausas, pontuacao e continuidade do meio para o final. Nao houve reducao de qualidade para economizar: os oito blocos usaram a mesma voz, modelo, idioma, seed, formato e configuracoes. A hipotese de deriva preservada ou acumulada pelo encadeamento de `previous_request_ids` permanece plausivel, mas ainda nao comprovada.
- Aprovacao da abertura nao prova estabilidade de um episodio longo. Enquanto o gate de voz estiver `full` ou `restored`, devem existir tres calibracoes independentes: abertura, miolo denso representativo e fechamento com CTA.
- Request Stitching nao deve encadear o episodio inteiro a partir de uma unica ancora enquanto nao houver evidencia pratica de estabilidade. Testar ancoras limitadas por trecho e comparar com geracao sem cadeia progressiva antes de nova narracao integral.
- O usuario nao deve precisar marcar erros frase a frase. O gate humano aprova ou reprova amostras representativas e depois o master completo.
- A cena final do avatar foi reprovada porque uma cadeira deslocada ao lado contradizia a postura central e fazia o personagem parecer sentado no ar. A cadeira estava no fundo escolhido na composicao, nao no video bruto do HeyGen.
- Toda composicao de avatar deve receber veredito explicito sobre apoio corporal, contato, oclusao, perspectiva, escala e iluminacao. A mera existencia de keyframes nao aprova a cena.
- Um fundo de sala sem cadeira, sofa ou mesa de centro e um composite corrigido foram preparados localmente, sem chamada paga. Eles so entram no proximo master depois da correcao da narracao.

## Video 003 - finalizacao v3 com divida aceita

Data: 2026-07-23.

- O teste dos blocos 07 e 08 sem `previous_request_ids`, usando `previous_text` longo, foi percebido pelo usuario como pior que o audio anterior. Essa substituicao esta reprovada e nao deve ser repetida.
- O resultado nao prova que Request Stitching seja inofensivo; prova somente que remover a cadeia e inserir contexto textual longo nao foi uma correcao eficaz.
- O usuario autorizou finalizar o video 003 com o melhor audio existente e transferir o aperfeicoamento de prosodia para os proximos videos.
- A divida de audio e excecao explicita deste episodio. Ela nao conta como execucao limpa, nao promove o gate de voz e nao vira padrao do canal.
- O master v3 preserva bit a bit a faixa de audio escolhida do v2 e substitui o encerramento por uma composicao fisicamente coerente, sem cadeira deslocada.
- O master v3 passou no QA tecnico local, conserva legendas, dois espacos de recomendacao e fade final. A publicacao aguarda somente a restauracao do acesso Google e OAuth do yutu.

## Metadados do YouTube - margem de seguranca

Data: 2026-07-23.

- Limites tecnicos de descricao, tags e hashtags sao tetos, nao metas de preenchimento.
- O Codex deve aproveitar os recursos disponiveis sem contrariar alertas da plataforma: somente termos sustentados pelo video, sem repeticao mecanica ou metadado enganoso.
- Politica substituida em 2026-07-24: cada video tera conjunto semantico proprio de tags e hashtags, orientado pela pergunta especifica que responde.
- Tags internas sao secundarias e ficam principalmente para grafias alternativas, erros comuns, nomes e referencias biblicas pertinentes; nao existe meta de preencher os 500 caracteres.
- Hashtags serao poucas e precisas, normalmente duas a quatro como disciplina interna, sem declarar essa faixa como quantidade otima comprovada. Acima de 60, o YouTube ignora todas.
- O piloto 001 historicamente usa 18 tags internas, aproximadamente 430 caracteres, e 15 hashtags. Esse pacote nao vira modelo para os proximos episodios.
- Medir termos reais de pesquisa, trafego de Busca, CTR por origem, retencao, duracao media, inscricoes e proxima visualizacao. Nao atribuir alcance a tags ou hashtags isoladamente.

## Primeiro derivado vertical do piloto 001

Data: 2026-07-23.

- O primeiro recorte vertical reutiliza o trecho de 450,6 a 538,98 segundos do piloto, com 88,7 segundos de fala e 3 segundos de cartão final. A duração total é 91,7 segundos.
- A composição é própria em 1080x1920, com legendas incorporadas dentro da área segura. Não é um recorte cego do master horizontal.
- Nenhuma API paga foi chamada: áudio e imagens já adquiridos foram reutilizados, e a montagem foi renderizada localmente.
- O primeiro QA rejeitou a abertura com caderno em branco. A v2 a substituiu por uma cena de cansaço noturno, coerente com o gancho, sem nova geração.
- A v2 foi reprovada pelo usuário porque as legendas resumiam a mensagem em vez de transcrever a fala e o áudio começava uma frase cortada no final. A v3 usa transcrição literal sincronizada por palavra e termina depois de `porque ele cuida de você`.
- TikTok e YouTube Shorts são destinos obrigatórios. O corpo pode ser comum para economizar, mas cada plataforma recebe acabamento próprio e métricas separadas; não inferir que os públicos ou resultados serão iguais.
- Local canônico atual do corte 01: TikTok em `operations/a-palavra-que-cuida/07_exports/shorts-aprovados/piloto-001/piloto-001-short-01-tiktok-v5-autocontido.mp4`; YouTube Shorts em `operations/a-palavra-que-cuida/07_exports/shorts-aprovados/piloto-001/piloto-001-short-01-youtube-short-v3-autocontido.mp4`.
- No YouTube Short, associar o vídeo longo `ZkmCkF6XR_g` pelo recurso de vídeo relacionado. No TikTok, vincular o YouTube ao perfil e selecionar música com verificação de direitos dentro do aplicativo perto da publicação.
- Política completa: `operations/a-palavra-que-cuida/01_briefs/politica-distribuicao-vertical-multiplataforma-v1.md`.

## Incidente de áudio e legenda no primeiro vertical

Data: 2026-07-23.

- As versões verticais inicialmente entregues foram corretamente reprovadas: o áudio falava um trecho e a legenda mostrava outro.
- Causa comprovada no código instalado: `Audio` importado de `@remotion/media` 4.0.484 aceita `trimBefore`, não `startFrom`. O parâmetro incorreto foi ignorado e o áudio começou no zero do master, enquanto as legendas começavam em 450,6 segundos.
- Correção robusta: extrair previamente um WAV dedicado ao recorte e reproduzi-lo desde o zero da composição. Não depender de deslocamento implícito no componente.
- Gate novo: antes do render vertical completo, renderizar uma prévia de 10 a 15 segundos e transcrever o áudio que saiu do próprio vídeo. A prévia só passa se transcrição, legenda e roteiro coincidirem.
- A prévia corrigida foi transcrita como `Mas você pode começar distinguindo três coisas. Primeiro, o que realmente é sua responsabilidade hoje?...`, coincidindo com a legenda.
- As saídas anteriores ficam marcadas como `do_not_publish` e não podem ser promovidas por engano.

## Regra de abertura para derivados verticais

Data: 2026-07-24.

- Todo TikTok ou YouTube Short deve ser semanticamente autossuficiente desde a primeira palavra.
- Um trecho que funciona no vídeo longo pode falhar isoladamente. Conjunções como `mas`, `então`, `por isso` e `ainda assim` não podem abrir o derivado quando retomarem uma frase ausente.
- Entrar direto no assunto continua desejável, mas isso não autoriza eliminar o contexto mínimo necessário para a primeira frase parecer um começo real.
- Para o derivado 001, a abertura `Mas você pode começar distinguindo três coisas` foi reprovada e substituída por `Hoje, talvez você não consiga resolver todos os pesos que carrega. E tudo bem.`
- A duração v0.1 para derivados voltados também ao Creator Rewards é pouco acima de um minuto quando o conteúdo sustentar esse tempo. Não esticar até 90 segundos sem ganho editorial; o TikTok considera simultaneamente tempo assistido e taxa de conclusão.

## Aprovação do primeiro derivado vertical

Data: 2026-07-24.

- A versão autocontida de 62,2 segundos do derivado vertical 001 foi aprovada pelo usuário como aceitável para publicação.
- Dívida aceita: o vídeo ainda pode ficar um pouco mais dinâmico. Não regenerar este derivado apenas por isso; aplicar o aprendizado desde o planejamento dos próximos.
- Dinamismo futuro deve vir de ritmo e variedade visual coerentes com a mensagem. Não acelerar por acelerar, não competir com a legenda e não aumentar custos sem função comunicativa.
- Incidente observado na primeira publicação do TikTok em 2026-07-26: o quadro inicial preto virou a miniatura do vídeo no perfil. Para todos os próximos verticais, o primeiro frame deve ser uma imagem forte do próprio vídeo, nunca preto ou em transição, e a capa deve ser selecionada e conferida manualmente antes de publicar.

## Pasta canônica de Shorts aprovados

Data: 2026-07-24.

- Os derivados verticais aprovados ficam concentrados em `operations/a-palavra-que-cuida/07_exports/shorts-aprovados/`, com uma subpasta por vídeo-fonte.
- A pasta canônica guarda somente finalizações aprovadas. Prévia de QA, render intermediário e versão reprovada ficam fora dela.
- Finalizações de TikTok e YouTube Shorts não são tratadas como duplicatas quando possuem acabamento ou tela final específicos para a plataforma.
- O piloto 001 possui seis cortes aprovados e doze arquivos finais, duas finalizações por corte. O índice verificável está em `operations/a-palavra-que-cuida/07_exports/shorts-aprovados/piloto-001/catalogo-v1.json`.

## Evidência para títulos de encontro providencial

Data: 2026-07-24.

- Após assistir ao primeiro vídeo de `A Palavra Que Cuida` numa conta sem consumo anterior declarado, o usuário recebeu como próxima recomendação `Deus te Mostrará ESTE VÍDEO pouco antes do seu MILAGRE`, do canal `Feitas para Reinar`.
- O título e o canal foram verificados publicamente. A condição da conta é input do usuário. O YouTube informa que o vídeo atual é o principal sinal da recomendação `A seguir`.
- Inferência permitida: nosso vídeo foi associado a esse bairro temático. Inferência proibida: afirmar que o título concorrente causou sozinho sua recomendação ou desempenho.
- Decisão: testar futuramente a moldura de `encontro providencial` em um episódio compatível, sem promessa sobrenatural específica não entregue e sem transformar todo o canal nesse padrão.
- A forma evergreen é especialmente interessante porque cria sensação de oportunidade sem exigir mudança diária de título.
- Experimento documentado em `operations/a-palavra-que-cuida/01_briefs/experimento-titulo-encontro-providencial-v0.1.md`.

## Frase editorial candidata - preservar a paz

Data: 2026-07-23.

- Frase espontânea aprovada pelo usuário: `Não se estressa tanto, preserve a sua paz.`
- Variante revisada para roteiro e narração, sem alterar o sentido: `Não se estresse tanto. Preserve a sua paz.`
- Origem: conselho dito pelo usuário à própria mãe; a naturalidade cotidiana é parte do valor da frase.
- Considerar a frase já no próximo roteiro se houver encaixe orgânico, especialmente em temas de ansiedade, sobrecarga, limites, descanso, controle ou cuidado.
- Não inserir por obrigação, não forçar a ligação bíblica e não transformar em bordão antes de observar se ela funciona bem no conteúdo.

## Direção visual aprovada - natureza, animais e artesanato

Data: 2026-07-24.

- O usuário aprovou especialmente o uso de imagens de natureza e animais. Para `A Palavra que Cuida`, elas passam a integrar o vocabulário visual recorrente e podem substituir parte do stock humano genérico quando houver relação semântica com a mensagem.
- Natureza não é preenchimento automático: cada imagem precisa exercer função comunicativa e combinar com a fala, o ritmo e o sentimento daquele trecho.
- Pessoas de stock continuam permitidas, mas os personagens próprios do canal devem concentrar identidade, continuidade e características recorrentes sempre que a cena pedir uma pessoa reconhecível.
- O usuário aprovou a presença natural de uma peça de crochê no sofá de uma personagem. Crochê e outros detalhes artesanais brasileiros podem reforçar familiaridade, cuidado e autenticidade doméstica.
- Esses detalhes não devem aparecer em toda cena nem virar assinatura forçada. Variar ambientes e objetos, mantendo coerência cultural e evitando repetição artificial.

## Acervo visual como patrimônio de produção

Data: 2026-07-24.

- Decisão do usuário: durante a fase inicial do canal, cada episódio deve acrescentar uma parcela de imagens exclusivas e reutilizáveis. O objetivo é formar um acervo amplo que reduza significativamente a necessidade de geração nos meses seguintes.
- Não foi fechado um corte rígido entre 10 ou 30 vídeos. A transição ocorrerá pela cobertura real da biblioteca: primeiro expansão acelerada, depois geração seletiva e, por fim, reutilização como padrão com geração apenas de lacunas.
- Mesmo com acervo maduro, temas novos e passagens sem representação adequada podem exigir imagens novas. Economia nunca autoriza imagem semanticamente errada.
- Thumbnail, abertura e embalagem precisam continuar distinguindo cada episódio. Reciclar o corpo visual não significa apresentar vídeos indistinguíveis.
- Política operacional registrada em `operations/a-palavra-que-cuida/01_briefs/politica-acervo-visual-v0.1.md`.

## Cadência futura e alternância editorial

Data: 2026-07-24.

- Preferência estratégica do usuário: chegar a dois vídeos longos por dia. Isso é alvo de escala, não evidência de que a frequência por si só aumentará a distribuição ou a receita. A hipótese será testada com dados do canal, capacidade de produção, custo e manutenção de qualidade.
- Regra operacional adicionada em 2026-07-27: manter estoque de seguranca de aproximadamente 7 videos longos prontos, com seus derivados e pacote de publicacao quando aplicavel. A producao diaria pode ser de 1 ou 2 longos, mas a publicacao nao deve depender do video recem-produzido ficar pronto em cima do horario.
- Ao finalizar um episodio, a esteira deve deixar o video no esquema completo: master preparado, derivados planejados ou renderizados conforme a politica de curtos, thumbnail/metadados/pacote de publicacao e estado claro de aprovacao. Depois que o comando de render final for iniciado com log e caminho de saida previstos, o Codex pode encerrar a resposta sem esperar o render terminar, desde que informe o processo iniciado, o arquivo esperado e o ponto de retomada.
- Render local longo deve ser tratado como trabalho assincrono quando for demorado. A regra desejada e criar uma notificacao persistente do sistema ao concluir, com clique abrindo o video renderizado. Ate isso estar implementado tecnicamente nos scripts, registrar a pendencia e nao prometer notificacao real sem executar um watcher ou automacao equivalente.
- Quando o canal passar a publicar três vídeos por semana, o Codex deve relembrar proativamente esta decisão e propor uma grade que alterne dinâmicas editoriais sem abandonar a identidade reconhecível de `A Palavra que Cuida`.
- Elementos constantes: voz, avatar, identidade visual, fidelidade bíblica, cotidiano brasileiro, legendas e padrão de qualidade. O que deve variar é o motor narrativo, por exemplo: acolhimento e aplicação; história de uma figura bíblica; investigação de uma pergunta difícil; correção de uma leitura popular; ou mensagem direta de encontro providencial.
- Se a cadência chegar a dois vídeos por dia, a hipótese inicial é usar o primeiro slot para o formato reflexivo-aplicado já conhecido e o segundo para uma dinâmica claramente diferente. Não variar apenas o tema: promessa, abertura, progressão, ritmo e função das imagens também precisam mudar.
- A grade não vira taxonomia rígida. Desempenho por formato, custo, retenção, retorno ao canal e fadiga visual determinarão quais dinâmicas permanecem.

## Tela final a partir do vídeo 004

- A partir do vídeo 004, o espaço superior deve conduzir ao vídeo mais recente elegível do canal e o inferior ao episódio publicado imediatamente antes do vídeo que está sendo assistido.
- Os dois destinos precisam ser vídeos distintos e nenhum elemento pode apontar para o próprio vídeo em exibição. Antes de configurar o vídeo 004, verificar na interface atual do YouTube como o elemento dinâmico `upload mais recente` trata o próprio vídeo. Se houver autorreferência ou duplicação, usar o vídeo mais recente elegível como destino fixo.

- Observação de descoberta de marca em 2026-07-25: na consulta manual `a palavra que cuida`, vídeos longos de terceiros puderam aparecer acima do vídeo do canal mesmo sem conter a frase inteira no título. O caso `CUIDADO COM O QUE FALAS` não tem descrição; a página de resultados expôs um trecho do próprio conteúdo em `29:39` com `palavras`, enquanto o título contém `cuidado`. Isso confirma, para esse caso, que a busca combina título e conteúdo falado/indexado, não apenas nome, descrição, comentários ou hashtags. A ordem variou entre a observação do usuário e a sessão de verificação, coerente com personalização. Não tratar posição de uma conta como ranking universal; repetir a medição em sessão sem histórico e acompanhar no Analytics os termos reais de busca. Fontes: documentação oficial de busca do YouTube e observação registrada no chat.
- A cada nova publicação, revisar as telas finais dos vídeos anteriores quando necessário para que o destino superior continue levando ao conteúdo mais recente e o inferior preserve o antecessor direto.

## Aberturas e primeiros segundos

Data: 2026-07-24.

- Decisão do usuário: nos vídeos horizontais, os primeiros 30 segundos devem ser chamativos sem esfregar promessa, listar benefícios ou transformar a abertura em anúncio. A mensagem começa imediatamente e já entrega conteúdo antes do fim dessa janela.
- No YouTube, 30 segundos é uma janela oficial do relatório de retenção, não uma fórmula secreta de viralização. A abertura deve cumprir a expectativa criada por título e thumbnail sem necessariamente repeti-los.
- Para TikTok e Shorts, não existe segundo mágico universal. A política v0.1 é cumulativa: primeiro frame ativo; motivo para parar até dois segundos; assunto compreensível até três; primeira recompensa concreta até cinco ou seis segundos.
- No TikTok Creator Rewards, visualizações inferiores a cinco segundos não são qualificadas quando a conta participa do programa. Isso torna cinco segundos uma fronteira financeira relevante, não garantia de distribuição.
- Curiosidade é permitida quando nasce do conteúdo. Urgência falsa, promessa mirabolante, revelação pessoal inventada e `assista até o fim` vazio são proibidos.
- Política e fontes registradas em `operations/a-palavra-que-cuida/01_briefs/politica-aberturas-retencao-v0.1.md`.

## Catalogo futuro e playlists

Data: 2026-07-24.

- Decisao do usuario: toda ideacao de video deve considerar que outros episodios parecidos poderao ser produzidos. A pauta precisa contribuir para a estrutura futura do canal, suas familias de conteudo e suas playlists.
- Uma mesma figura biblica pode originar linhas distintas, como historia de vida, um periodo especifico, escolhas, erros, acertos, sofrimento ou ensinamentos. Compartilhar personagem nao obriga os videos a pertencerem a uma unica playlist.
- A arquitetura usa camadas cruzadas: necessidade vivida, mapa biblico e abordagem editorial. Playlists comuns permitem ate uma classificacao primaria e duas secundarias por video.
- Crescimento v0.1: um video registra a semente no repositorio; dois tornam a playlist elegivel para publicacao; tres tornam a lista elegivel para secao da pagina inicial. Esses limiares evitam listas vazias e nao sao apresentados como regra do algoritmo.
- Series oficiais do YouTube ficam reservadas a sequencias realmente ordenadas, pois um video nao pode integrar mais de uma playlist de serie.
- O catalogo inicial e as familias incubadas estao em `operations/a-palavra-que-cuida/08_publicacao/catalogo-playlists-v0.1.yaml`; politica completa em `operations/a-palavra-que-cuida/01_briefs/politica-catalogo-playlists-v0.1.md`.

## Correcao economica - otimizar, nao reduzir

Data: 2026-07-24.

- O usuario corrigiu uma formulacao anterior: pedidos para `reduzir custos`, `gastar pouco` ou `economizar` devem ser entendidos como `otimizar custos`.
- O objetivo nao e produzir o resultado mais barato. E evitar chamadas, segundos, resolucoes, repeticoes e operacoes pagas que nao acrescentem resultado, sem sacrificar qualidade, precisao, naturalidade, acessibilidade, coerencia, identificacao ou retorno esperado.
- Custo relevante e custo total: cobranca direta, risco de refacao, operacao humana, processamento posterior e oportunidade perdida. Confiabilidade, reutilizacao, aprendizado e retorno esperado tambem entram no valor.
- Entre opcoes que entregam resultado equivalente, escolher a de menor custo total. Uma opcao mais cara pode ser correta quando houver evidencia de ganho material ou reducao de risco.
- Registros historicos de versoes economicas permanecem como historia. Politicas ativas e o nucleo universal passam a usar custo otimizado.

## Auditoria retrospectiva dos videos 001 a 003

Data: 2026-07-24.

- A fabrica permanece `v1-candidate`; nao esta pronta para producao autonoma nem para promocao a v1.
- O diagnostico central e excesso de memoria normativa com pouco enforcement no executor real. `FactoryRun`, gates, custos e QA ainda governam pouco os scripts concretos de producao.
- O consumo economico corrigido dos tres videos e `US$ 13,815487 / R$ 70,19`, sem precificar imagem integrada, trabalho humano, computacao local e o aporte desconhecido do HeyGen.
- Dos 29.767 creditos ElevenLabs, 18.420, ou 61,9%, ficaram em testes e versoes descartadas. Parte foi aprendizado legitimo, mas o proximo fluxo deve descobrir defeitos em amostras representativas menores.
- O video 003 foi concluido com divida de prosodia aceita; seu gate de voz continua `restored` e a execucao nao conta como limpa.
- O QA tecnico aprovou masters depois reprovados por prosodia e coerencia fisica. Integridade tecnica, correspondencia objetiva, QA semantico e crivo humano sao resultados separados.
- A limpeza de 1.209 arquivos liberou 6,262 GB, mas removeu evidencias ainda citadas pelo run, gate e validador do video 003. Limpeza futura precisa consultar referencias e preservar tombstones reproduziveis.
- O pacote do piloto 001 registra publicacao publica, enquanto a camada de metricas ainda diz que nenhuma publicacao ocorreu. Estado operacional precisa ter uma unica fonte canonica.
- Antes do video 004, sao P0: runner real da fabrica, estado e custo unificados, ciclo de vida de artefatos, calibracao de voz em abertura/miolo/CTA, storyboard revisado antes de gasto, proxy antes do master e atualizacao da verdade de publicacao/metricas.
- A auditoria completa e suas evidencias estao em `ai/auditorias/retrospectiva-fluxo-agentico-videos-001-003-v1.md`.

## Correcao de edicao - texto na tela

Data: 2026-07-27.

- Decisao do usuario: fora de legendas sincronizadas, o master horizontal nao usa textos editoriais, titulos de abertura ou frases de apoio sobre imagens. A excecao e a carta biblica completa durante a leitura direta e a tela final estrutural.
- Mencionar livro, personagem ou capitulo nao aciona carta biblica. A carta ACF completa aparece exclusivamente durante a leitura direta do versiculo correspondente.
- Legendas sao transcricao sincronizada e continuam separadas de placas editoriais. O QA humano confere inicio, meio e fim ouvindo a fala e lendo a tela; texto sem frase correspondente reprova o master.
- A politica central e `operations/a-palavra-que-cuida/01_briefs/politica-legendas-e-tiktok-v1.md`. O gerador do video 004 passou a bloquear por erro qualquer ativo `editorial/` na lista ciclica de B-roll.

## Correcao de tela final - sem slots fixos

Data: 2026-07-27.

- Decisao do usuario: os proximos masters horizontais terminam sem quadrados, molduras ou lugares pré-determinados para videos clicáveis. A plataforma define quantidade e posicionamento dos elementos na etapa de publicacao.
- A tela final preserva o nome do canal e o handle ativo `@apalavraquecuidabr`, centralizado horizontalmente. O video 004 v5 permanece como excecao aprovada, com seus dois espacos visuais.

## Cadencia dos curtos apos cada video longo

Data: 2026-07-28.

- Nova grade semanal decidida pelo usuario: videos longos do canal religioso sao publicados as segundas, quartas e sextas-feiras. Os curtos do canal e de suas redes sao publicados as tercas, quintas e sabados, sempre derivados do longo do dia anterior.
- Cadencia operacional fixa: em cada terca, quinta e sabado, publicar o primeiro par as 11h e o segundo par as 17h. Cada par contem 1 YouTube Short e 1 TikTok do mesmo corte; no total do dia, sao 2 YouTube Shorts e 2 TikToks.
- Domingo foi definido como dia de proximidade com a comunidade, sem video regular. Publicar as 11h um post na Comunidade do YouTube com imagem bonita e original acompanhada de um versiculo ou de uma boa mensagem de acolhimento; perguntas e pedidos de oracao podem ser usados quando fizerem sentido.
- Decisao do usuario: os dois curtos derivados de cada video longo devem ser publicados no dia seguinte ao longo, tanto no YouTube Shorts quanto no TikTok.
- Horarios fixos decididos: curto 1 as 11h e curto 2 as 17h, no horario de Brasilia.
- Quando houver um video longo novo no mesmo dia, ele entra a noite; no YouTube, a operacao fica em dois Shorts e um longo naquele dia.
- Esta regra substitui a grade anterior que espalhava os dois curtos por varios dias. Curto atrasado de um longo ja publicado tem prioridade sobre o estoque antigo que nao esta ligado ao episodio mais recente.
- Nao publicar curto antes do respectivo video longo. Estoque antigo pode ocupar dias sem estreia ou slots de recuperacao, desde que nao atrase os dois curtos do episodio mais recente.
- Procedimento padrao decidido pelo usuario: todo YouTube Short deve receber, antes da publicacao, o respectivo video longo pelo recurso nativo `Video relacionado`. A URL na descricao nao substitui esse vinculo. Se os recursos avancados da conta impedirem o vinculo, manter o Short privado e pausar a publicacao ate a verificacao ser concluida.
- Divisao operacional de `A Palavra Que Cuida`, atualizada pela usuaria em 2026-08-01: o Codex assume a publicacao do YouTube Shorts e do TikTok no mesmo slot. Sempre que publicar um Short, deve publicar tambem o TikTok correspondente, verificando antes canal autenticado, arquivo aprovado, capa, legenda, localizacao, direitos autorais, elegibilidade e duplicacao. Se qualquer plataforma ou conta impedir a publicacao, registrar o bloqueio e avisar imediatamente a usuaria para que ela possa intervir. O envio ao tablet deixa de ser a rota padrao deste canal e passa a ser contingencia quando a publicacao direta do TikTok nao estiver disponivel.
- Roteamento operacional atualizado pela central em 2026-07-29: este chat executor responde apenas pelos pares de YouTube Shorts e TikTok das tercas, quintas e sabados, as 11h e 17h. O post da Comunidade do YouTube aos domingos as 11h passa a ser executado pelo chat de videos longos.
- Decisao do usuario sobre duracao: os curtos destinados tambem ao TikTok nao precisam terminar em 1:00 cravado. Quando a mensagem permitir, devem ultrapassar 60 segundos por alguns segundos para atender a estrategia de monetizacao, sem inserir enrolacao ou prejudicar o ritmo. A faixa exata ainda nao foi fixada; o corte aprovado atual, com 1:14, e uma referencia valida.
- Regra visual explícita do usuário: não usar imagens de caderno aberto com páginas em branco. A proibição vale para vídeos longos, curtos, novos renders e seleção de biblioteca; não basta evitar um arquivo específico. Cadernos só podem aparecer quando houver ação concreta e informação visual necessária, nunca como preenchimento genérico ou grande área vazia.

## Duracao dos videos longos

Data: 2026-07-28.

- Decisao do usuario: os videos longos do canal religioso devem durar no minimo 10 minutos e no maximo 13 minutos.
- A duracao real deve ser conferida pelo master WAV e pela linha do tempo, nunca apenas pelo MP3 de revisao. Se a narracao exceder o teto, pausar antes da edicao e propor enxugamento do roteiro e nova geracao com cotacao e aprovacao separadas.

## Emocao da narracao

Data: 2026-07-28.

- Sinal humano a investigar: a narracao atual em `eleven_multilingual_v2`, com a voz Bruno Cardoso e configuracao-base de estabilidade `0.5` e estilo `0`, foi percebida como pouco emocional. Isso e uma observacao de QA, nao um diagnostico definitivo da voz ou do modelo.
- Antes de uma proxima narracao longa paga, executar uma calibracao curta e representativa de abertura, leitura biblica e trecho de acolhimento, com cotacao e aprovacao explicitas. Comparar configuracoes de expressividade e avaliar por escuta humana antes de gerar o roteiro inteiro.
- Nao usar tags pseudoemocionais, comandos entre colchetes, direcoes teatrais que seriam narradas, excesso de reticencias, nem `<break>` como atalho. Esses recursos nao pertencem ao contrato atual da voz e ja causaram pausas artificiais ou prosodia ruim. A emocao deve vir primeiro do texto, da segmentacao semantica e de parametros validados por amostra.

## Identificacao em videos por personagens biblicos

Data: 2026-07-28.

- Decisao do usuario: historias de personagens biblicos continuam sendo uma frente importante, mas nao podem afastar a espectadora da propria vida. Cada roteiro desse tipo deve conduzir, nas entrelinhas, a experiencia de quem escuta para dentro da cena: cansaco, escolhas, culpa, espera, fe, relacoes e cotidiano reconhecivel.
- A identificacao nao deve virar rotulo demografico, interrogatorio ou formula repetitiva. A personagem biblica abre o episodio; a aplicacao faz a espectadora se perceber sem ser colocada de forma artificial no papel de Marta, Maria ou outro personagem.
- A grade futura tambem deve preservar episodios dedicados diretamente a necessidade vivida pela espectadora, como nos primeiros videos, alternando motores narrativos sem perder a identidade do canal.
- Alternancia editorial confirmada: intercalar videos que contam e interpretam uma historia ou figura biblica com videos que partem diretamente de uma situacao da vida cotidiana. Em ambos, a mensagem biblica e o acolhimento ao publico permanecem centrais; muda o ponto de entrada, nao a promessa do canal.

## Direcao exploratoria - canal de afirmacoes

Data: 2026-07-26.

- Para o proximo canal em exploracao, o usuario escolheu manter o foco em duas linhas: `afirmacoes positivas para dormir` e `manifestacao por afirmacoes`.
- Publico-alvo fixado pelo usuario: meninas e mulheres brasileiras de 16 a 24 anos. O centro imaginado para linguagem, estetica, titulos e referencias culturais esta entre o fim da adolescencia e o inicio dos vinte; o conteudo nao e direcionado a criancas.
- Nome criativo escolhido pelo usuario para o canal de afirmacoes: `Quase Celestial`. A checagem inicial de busca publica em 2026-07-26 nao mostrou concorrente direto evidente, mas as consultas diretas a YouTube e Instagram foram limitadas pela plataforma e isso nao comprova disponibilidade de `@`, marca ou dominio. Antes da abertura/publicacao, verificar handle no proprio YouTube e Instagram e fazer busca formal aplicavel no INPI.
- Esta e uma direcao editorial de pesquisa e piloto, nao uma decisao de publico-alvo, promessa garantida, stack ou formato final.
- Meditacao guiada e sons ambientes puros nao serao o foco deste canal. Podem ser referencias ou alternativas para outro canal no futuro, sem entrar automaticamente no escopo atual.
- A hipotese visual candidata e uma estetica imaginativa, delicada e "salvavel no Pinterest", com voz feminina de afirmacoes como centro e loops/cenas sutis como atmosfera; ela ainda precisa de analise concorrencial e teste original antes de ser cristalizada.
- A palavra `subliminal` pode ser testada somente como sublinha ou playlist, nao como identidade obrigatoria do canal; a comunicacao deve evitar alegacoes medicas, promessas de resultado ou apresentacao de crenca como fato comprovado.
- A composicao editorial candidata passa a ter somente duas linhas: aproximadamente 60% de `afirmacoes positivas para dormir` e 40% de `manifestacao por afirmacoes`. Nao ha espaco reservado para meditacao guiada.
- Regra de audio: a voz pode ser suave pela interpretacao e pela mixagem, mas deve permanecer clara em volume normal de celular. Nao baixar o master a ponto de exigir que a pessoa aumente muito o aparelho para dormir; cada faixa devera passar por escuta em alto-falante mono de celular e em fones, em volume habitual.
- Voz-base escolhida pelo usuario para o canal de afirmacoes: `Marianne - Sweet, Calm and Clear` (voice id `iScHbNW8K33gNo3lGgbo`), gerada com o modelo `eleven_v3`. A escolha substitui a tentativa anterior com Laura, que fica somente como amostra descartada de calibracao. A Marianne foi selecionada por audicao de amostra curta em portugues e e classificada como jovem adulta no catalogo; parametros de performance, ritmo, tags e mixagem permanecem para calibracao no piloto. O nome descritivo do catalogo nao substitui o crivo humano de adequacao ao canal.
- Assinatura sonora aprovada para os dois pilares: em momentos pontuais, a voz principal da Marianne, clara e central, ganha uma segunda copia da mesma voz, curta, baixa e difusa como textura eterea — nao um eco nitido. Em `manifestacao por afirmacoes`, ela pode aparecer nos pontos de expansao e frases-chave; em `afirmacoes para dormir`, mais discreta, sobretudo em finais de frase. Ponto de partida de calibracao: copia cerca de 14–18 dB abaixo da principal e atraso inicial de 45–70 ms; validar inteligibilidade em fones e alto-falante mono antes de promover.
- A amostra de manifestacao com Marianne em `eleven_v3`, cama sonora eterea original e voz-sombra pontual foi aprovada pelo usuario como direcao do primeiro episodio. O roteiro completo ainda precisa ser recalibrado para atingir a duracao-alvo de 11:11 no ritmo real dessa voz.
- A experiencia de anuncios e variavel e esta fora do controle do canal. A documentacao do YouTube informa que o recurso de volume estavel pode equilibrar o audio do video, mas nao afeta anuncios. Logo, essa incerteza nao justifica publicar uma faixa artificialmente baixa; a mitigacao controlavel e evitar picos, fala agressiva e diferencas grandes dentro do nosso proprio audio.
- Identidade criativa candidata aprovada pelo usuario: nucleo em afirmacoes audiveis e manifestacao; experiencia bonita, intima, feminina e imaginativa; visual composto por loops ou cenas sutis com estetica propria. O canal nao usara avatar, persona de "professora guiando meditacao", chuva/cachoeira ou musica de relaxamento generica como pilares.
- Direcao visual candidata do canal de afirmacoes: eterea, onirica, pictorica e sublime, com presencas/femininas luminosas, feixes de luz, flores, agua/cosmos e uma sensacao angelical nao necessariamente religiosa. A referencia deve privilegiar atmosfera, luz, paleta e movimento; nunca reproduzir composicao, personagem ou obra de terceiros.
- Pinterest e outros moodboards sao instrumentos de descoberta, nao banco de assets. Para cada arte publicada, usar somente geracao original, stock com licenca comercial compativel com monetizacao, ou obra comprovadamente em dominio publico com a origem documentada. Uma obra original conhecida, sua fotografia ou seu scan nao se presume livre apenas por aparecer no Pinterest.
- Movimento visual inicial de custo otimizado: uma arte-master original com animacao sutil e coerente (pulso de luz, particulas, agua/ceu, parallax leve ou zoom lento). Decidir por video se um loop sem costura ou uma animacao curta agrega valor; nao animar por obrigacao nem repetir o mesmo master de modo indistinguivel entre episodios.
- Exclusividade visual decidida para o canal de afirmacoes: cada episodio publicado recebe uma arte-master propria e nao reutiliza a arte de outro episodio. Paleta, motivos e linguagem podem se repetir como identidade, mas nunca a mesma imagem, personagem ou composicao final.
- A arte publicada sai da rotacao editorial apos o episodio, mas permanece arquivada com sua origem, prompt/licenca, versao e destino publicado. "Descartar" significa nao reutilizar no canal; nao apagar evidencia nem abrir margem para reutilizacao acidental.
- Formato visual-base decidido: todo episodio longo usa uma "arte viva" exclusiva — imagem original com movimento local sutil e continuo, como pulso de luz, particulas, nevoa, agua, parallax ou zoom lento. Isso evita tanto a tela completamente parada quanto a obrigacao de gerar video caro para cada faixa.
- Geracao de animacao por IA fica reservada a episodios em que uma cena realmente animada acrescentar sentido e justificar seu custo, depois de storyboard, amostra e QA. Nao e requisito para publicar nem substitui a arte viva.
- Tratamento visual confirmado: os dois pilares usam arte viva original, editada para a assinatura do canal. Em `afirmacoes para dormir`, o movimento e quase imperceptivel e sem cortes (por exemplo, luz respirando, nevoa, particulas, agua ou zoom lentissimo). Em `manifestacao por afirmacoes`, a mesma linguagem recebe movimento um pouco mais expressivo, mas ainda suave e em loop (aura, feixes, flores/tecido, profundidade ou parallax). Video integralmente gerado por IA fica reservado a episodios especiais, nao como padrao.
- Prototipos visuais aprovados como referencia de direcao, nao como assets reutilizaveis: para `afirmacoes para dormir`, o usuario preferiu a primeira arte gerada em noite azul-profunda, figura repousando, halo lilas e agua, por manter riqueza visual e misterio sem ficar escura demais; para `manifestacao`, aprovou a versao de aurora rosada com garota de aparencia cotidiana, roupa simples, cabelo natural e rosto oculto, rejeitando o aspecto de "princesa perfeita". Cada episodio continua exigindo arte exclusiva.
- Correcao visual do piloto de manifestacao: personagens humanas devem ler claramente como jovens adultas; evitar rostos, proporcoes ou figurinos que as facam parecer criancas ou "princesas". A imagem do episodio 001 foi aprovada apesar desse desvio; a regra vale para os proximos.
- Diversidade visual de `Quase Celestial`, decidida em 2026-08-01: a identidade nao deve se reduzir a uma mesma garota contemplando uma janela em tons violetas. Cada novo episodio deve explorar deliberadamente outra combinacao de paleta, personagem/presenca, cenario e motivo visual, preservando apenas a atmosfera intima, imaginativa e salvavel. As referencias anteriores continuam servindo como direcao de sensacao e nao como composicao a repetir. O episodio 002, com mulher jovem-adulta em cena noturna, foi aprovado como uso pontual; nao vira modelo composicional padrao.
- Foto de perfil aprovada para `Quase Celestial`: gato preto luminoso integrado a um talisma de quatro pontas com orbita interrompida, em azul-noite, lilas, fucsia e damasco. O gato e mascote/identidade visual, nao assunto recorrente dos videos; pode aparecer apenas de forma pontual nas artes.
- Correcao de audio do piloto: na abertura dos proximos episodios, manter a voz totalmente seca e inequivoca; qualquer voz-sombra/textura que possa soar como segunda fala so pode entrar depois de uma amostra de abertura aprovada. O piloto 001 permanece aceito pelo usuario apesar de uma poluicao leve percebida nos primeiros minutos.
- Direcao TikTok para `Quase Celestial` escolhida pelo usuario: publicar videos verticais originais com duracao-alvo de 1:05 a 1:20, e nao cortes de menos de um minuto, para manter elegibilidade potencial ao Programa de Recompensas do Criador. Cada video deve ter arco proprio e ser pensado para TikTok; a entrada e a remuneracao efetiva continuam sujeitas aos requisitos, revisao e metricas vigentes da plataforma.
- Programacao TikTok para `Quase Celestial`, delegada pelo usuario em 2026-07-29: o Codex escolhe, por tema e funcao editorial, a mistura entre verticais originais e cortes reeditados dos videos longos. Nao ha alternancia fixa. Todo corte precisa ganhar gancho, inicio e fim proprios, continuar acima de um minuto quando destinado ao TikTok e nunca parecer um trecho solto. A decisao de volume e sequencia deve priorizar variedade, descoberta e ponte honesta ao YouTube, com revisao posterior pelas metricas.
- Cadencia inicial do TikTok de `Quase Celestial`, atualizada em 2026-07-29: publicar 6 videos por semana, um por dia de segunda a sabado, sem publicacao aos domingos. A fonte regular passa a ser somente cortes reeditados dos longos: dois candidatos fortes por episodio, com tres longos semanais gerando seis verticais. Nao produzir novos TikToks exclusivos enquanto essa grade for suficiente. Cada corte precisa ser autonomo, com gancho, inicio e fim proprios; se um episodio nao oferecer dois trechos realmente bons, priorizar qualidade em vez de publicar um corte fraco. Ao fim do ciclo inicial, revisar retencao, conclusao, salvamentos, compartilhamentos, visitas ao perfil e ponte ao YouTube antes de mudar a frequencia.
- Entrega para TikTok de `Quase Celestial`, decidida em 2026-07-29: a usuaria publica manualmente. De segunda a sabado, as 9h, o Codex deve enviar ao tablet o proximo MP4 aprovado e entregar no chat a legenda final pronta para copiar, com aviso explicito de que o video foi enviado. Nunca publicar o TikTok por conta propria; no domingo nao ha entrega. Se nao houver master aprovado, declarar o bloqueio em vez de enviar substituto improvisado.
- Estoque inicial de `Quase Celestial`, decidido em 2026-07-29: preparar 13 TikToks prontos para publicar, cobrindo os slots de uma cadencia de 5 por semana de 29 de julho a 15 de agosto de 2026. Cada master precisa obedecer ao padrao de legendas sincronizadas. O primeiro longo disponivel, `Minha nova era`, dura 11:38,9 e pode originar cortes depois de uma selecao editorial e reediçao propria; sua publicacao so pode ocorrer no canal `Quase Celestial`, nunca em outro canal autenticado por engano.
- Cadencia de longos de `Quase Celestial`, atualizada em 2026-08-01: publicar tres videos longos por semana, sempre as segundas, quartas e sextas-feiras, as 19h (America/Sao_Paulo). Cada longo deve nascer com dois candidatos reais de cortes verticais; assim, os tres longos geram seis candidatos para sustentar a publicacao de um TikTok por dia, de segunda a sabado. A automacao `Publicar longos — Quase Celestial` executa esse slot somente quando houver pacote plenamente aprovado; identidade do canal, master, thumbnail, metadados e comentario especifico do criador continuam gates obrigatorios.
- Grade de YouTube Shorts de `Quase Celestial`, atualizada em 2026-08-01: publicar dois Shorts por dia, as tercas, quintas e sabados, nos horarios de 11h e 17h (America/Sao_Paulo); nao publicar Shorts nos demais dias. Cada Short deve ser reeditado a partir do video longo mais recentemente publicado no canal e manter gancho, contexto, encerramento e legendas proprios. A automacao `Publicar Shorts — Quase Celestial` executa a publicacao somente com master aprovado, canal correto e metadados/classificacao verificados. Os horarios sao uma hipotese operacional e devem ser revistos depois de 28 dias com dados do YouTube Analytics.
- Comunidade de `Quase Celestial`, decidida em 2026-07-29: todo domingo, inicialmente as 11h (America/Sao_Paulo), publicar um post interessante e interativo conectado a algum material da semana anterior, preferencialmente ao longo mais recente. Pode ser pergunta curta, enquete ou texto acompanhado de composicao grafica original simples; nao reutilizar arte final de episodio como se fosse material novo. A automacao `Publicar comunidade — Quase Celestial` realiza essa publicacao no canal correto, ou registra bloqueio se faltar material ou acesso. O horario de 11h e hipotese operacional ate haver dados de audiencia suficientes para revisao.
- Legendas TikTok para `Quase Celestial`, decididas pelo usuario em 2026-07-29: todos os videos verticais publicados devem trazer legendas queimadas, sincronizadas com a narracao e posicionadas de forma discreta no terco inferior seguro. Elas precisam reproduzir o que e falado e passar por checagem contra o audio. Titulos grandes centralizados de abertura nao sao o padrao; so entram quando houver uma escolha editorial especifica aprovada.
- Padrao visual de legendas TikTok para `Quase Celestial`, atualizado em 2026-08-01: fonte Gadugi, 52 px no canvas 1080x1920, peso regular, texto branco-rosado, contorno escuro de 2,2 px, sombra de 0,8 px, centralizada no rodape seguro com margens laterais de 110 px e margem vertical de 320 px. A legenda deve ficar mais alta que o rodape/interface nativa do TikTok e reproduzir a fala com checagem contra o audio.
- Assinatura de cabecalho TikTok para `Quase Celestial`, atualizada em 2026-08-01: absolutamente todos os TikToks futuros devem trazer `Quase Celestial` no canto superior esquerdo desde o primeiro frame, mantendo-se visivel durante todo o video e na miniatura automatica. A posicao segue a referencia dos curtos de `A Palavra que Cuida`, com ajuste para baixo: Gadugi, 44 px, branco-rosado com sombra discreta, x=64/y=150 em canvas 1080x1920. Esta assinatura e exclusiva dos verticais; videos longos do YouTube permanecem limpos.
- Estrutura visual dos longos de `Quase Celestial`, decidida em 2026-08-01: cada episodio usara duas artes-master originais, exclusivas e visualmente distintas. A primeira ocupa a primeira metade e a segunda, a metade final; ambas recebem animacao propria, perceptivel e ainda serena, priorizando elementos naturais da cena como folhas, galhos, capim e agua. Os dois cortes verticais derivados devem vir de metades diferentes, para comunicar variedade visual tambem no TikTok. Nao reutilizar a mesma arte em episodios distintos.
- Correção de identidade visual de `Quase Celestial`, decidida em 2026-08-03: variedade não autoriza uma estética naturalista, simples ou dessaturada. Todo novo vídeo deve conservar energia etérea e cósmica inequívoca: luz radiante, brilho, contraste, saturação intencional e cores de fantasia (por exemplo, azul-noturno, lilás, fúcsia, rosa-aurora, dourado, turquesa luminoso), com espaço sideral, estrelas, halos, partículas, feixes ou aura quando fizer sentido. Elementos naturais só entram como cenário transformado por essa linguagem — nunca como uma paisagem comum de aparência tranquila/genérica. Antes de renderizar, avaliar a arte em miniatura e em tela cheia contra esse gate; se ela puder passar por vídeo de natureza/relaxamento genérico, está reprovada. O episódio 003 é exceção já publicada, não nova referência de direção.

## Grade semanal do canal religioso

Data: 2026-07-28.

- Decisao do usuario: publicar video longo no YouTube as segundas, quartas e sextas-feiras. Nas tercas, quintas e sabados, publicar 2 YouTube Shorts e 2 TikToks por dia: primeiro par as 11h e segundo par as 17h.
- Domingo fica sem publicacao de video. As 11h, publicar um post na Comunidade do YouTube com imagem original e mensagem ou versiculo; quando fizer sentido, pode haver pergunta, pedido de oracao ou convite de conversa.

## Direcao de interpretacao da narracao

Data: 2026-07-28.

- Decisao do usuario: a narracao deve ter emocao seletiva e certeira, nao uma dramatizacao constante. Reservar maior carga interpretativa para o apice do argumento, perguntas realmente importantes, leituras biblicas e temas sensiveis; o restante preserva a serenidade acolhedora do canal.
- O roteiro deve marcar esses pontos como batidas internas de interpretacao e escrever a fala de modo natural para sustenta-los: perguntas curtas, imagens concretas, contraste e pausas semanticas reais. A marcacao nao deve ser enviada como direcao teatral que a voz possa ler em voz alta.
- Quando a configuracao de voz precisar mudar para uma batida especial, gerar apenas esse bloco separado depois de calibracao curta, cotacao e aprovacao humanas. Nao aumentar a expressividade do episodio inteiro nem recorrer a tags nao suportadas, excesso de pontuacao ou `<break>`.

## Interpretacao de comportamento em true crime

Data: 2026-07-29.

- Direcao do usuario para o novo canal: o roteiro pode descrever comportamentos observaveis durante interrogatorios, como desviar o olhar, pausar ou mudar a postura, para criar tensao e acompanhar a cena.
- A observacao nao deve ser apresentada como prova cientifica de mentira, culpa ou estado mental. A ressalva deve ser curta, natural e variar de formulacao; nao repetir um aviso mecanico em toda ocorrencia.
- Evitar leitura de mente na narracao. Preferir "desviou o olhar quando o investigador apresentou a suspeita" a afirmar que a pessoa percebeu, mentiu ou se sentiu encurralada, salvo quando isso estiver documentado.
- Se evidencias posteriores apontarem fortemente para a culpa, o comportamento pode ganhar valor retrospectivo dentro da narrativa, mas continua sendo elemento de tensao e interpretacao, nao prova isolada. Fatos documentados, analise profissional e hipotese narrativa devem permanecer separados.

## Direcao editorial inicial do canal de crimes

Data: 2026-07-29.

- O canal deve abordar casos brasileiros e internacionais; crimes acontecem em contextos diversos e a pauta nao fica limitada ao Brasil.
- A selecao deve alternar casos pouco comentados ou pouco explorados no YouTube com casos famosos, desde que exista justificativa editorial para voltar ao assunto: novo hype, interesse publico ainda ativo, informacao relevante, novo angulo ou momento de alta procura.
- Dar preferencia a casos recentes ou ainda culturalmente vivos, sem transformar recencia em criterio absoluto. Casos antigos podem entrar quando a historia, as provas ou o comportamento continuam fortes para o formato.
- Priorizar casos de alta complexidade, estranheza, sofrimento e impacto narrativo. O canal pode explorar o sofrimento como parte do espetaculo emocional do true crime — medo, choque, indignacao, suspense e desconforto sao motores legitimos de audiencia — desde que isso seja construido por narrativa, contexto, testemunhos, evidencias e consequencias, e nao dependa automaticamente de gore gratuito ou de afirmacoes falsas.
- A intensidade nao deve ser higienizada a ponto de retirar o motivo pelo qual o publico procura o genero. Ao mesmo tempo, cenas graficas, thumbnails e descricoes precisam ser avaliadas separadamente por risco de restricao de plataforma, monetizacao limitada, dano a vitimas e perda de credibilidade.
- Tom editorial: usar um grau controlado de sensacionalismo como ferramenta de atracao — titulos fortes, aberturas perturbadoras, detalhes selecionados, urgencia e suspense — sem fabricar fatos, inflar provas, afirmar hipoteses como certezas ou humilhar vitimas e familiares. O sensacionalismo deve amplificar uma historia real, nao substituir a pesquisa.
- Direcao visual provisoria: identidade baseada em preto e vermelho, por associarem imediatamente perigo, urgencia, crime e tensao. Para evitar uma estetica generica ou exageradamente gore, o preto/carvao deve dominar, o vermelho deve funcionar como acento de alerta — preferencialmente vermelho profundo/vinho — e textos podem usar branco quebrado ou cinza claro. Tons exatos, tipografia e sistema de thumbnails ainda precisam de teste pratico.
- Direcao de thumbnails: usar preto e vinho como elementos de identidade, sem obrigar toda thumbnail a ser escura ou visualmente carregada. A composicao deve priorizar alto contraste, um unico foco de atencao, imagem ou rosto/objeto relevante do caso, atmosfera sensacionalista controlada e texto curto, forte e chamativo. A tipografia deve manter letras levemente ponteagudas, coerentes com a capa do canal, com leitura imediata em tela pequena. O impacto pode ser agressivo, mas titulo e imagem nao devem prometer algo que o video nao entrega.

## Nome criativo em exploracao para o canal de crimes

Data: 2026-07-29.

- Nome escolhido pelo usuario para a exploracao: `Ruptura Oculta`.
- A escolha combina a ideia de uma ruptura na versao oficial de um caso com a descoberta de uma camada escondida. O nome ainda nao esta aprovado como marca final: antes da abertura, verificar disponibilidade de handle nas plataformas, risco de confusao e busca formal aplicavel no INPI.
- Publico inicial de trabalho definido pelo usuario: mulheres de 25 a 44 anos como prioridade, sem exclusividade; homens continuam incluidos por se tratar de um canal documental aberto. A linguagem, a escolha de casos e a abordagem podem considerar interesses predominantes desse publico sem mencionar segmentacao no roteiro. A faixa e a composicao de genero devem ser confirmadas pelas metricas do proprio canal.
- Regra estrutural do projeto: cada canal deve ter uma pasta propria diretamente dentro de `Canais Dark`, com seus assets, roteiros, audios, edicoes, exports, publicacao e metricas isolados. Nenhum material de um canal novo deve ser guardado em `Canal Religioso` ou em outra pasta de canal existente.
- Regra transversal de comunidade: todo video longo publicado por qualquer canal atual ou futuro deve receber um comentario escrito pelo proprio criador do canal. O comentario precisa fazer sentido com o episodio, acrescentar uma observacao ou pergunta relevante e instigar respostas reais, sem CTA generico ou engajamento artificial. A publicacao so e considerada concluida depois de verificar esse comentario na interface; quando fizer sentido editorial, ele tambem pode ser fixado.
- Estrategia inicial de TikTok: o video longo do YouTube sera o ativo editorial principal e tambem abastecera o TikTok com cortes bem escolhidos das melhores partes — perguntas decisivas, contradicoes, viradas e momentos de tensao. A prioridade e equilibrar custo e retorno; nao produzir um video completamente separado para cada postagem por padrao.
- Plataformas iniciais do Ruptura Oculta: YouTube como casa dos documentarios completos e TikTok como canal de descoberta por meio dos cortes; Instagram nao faz parte do escopo inicial.
- Cada corte ainda deve funcionar como peca vertical: entrada compreensivel, contexto minimo, ritmo proprio, legendas e encerramento que preserve curiosidade. Nao produzir videos exclusivos para TikTok por padrao; Shorts e TikToks serao derivados estrategicamente dos videos longos.
- Regra transversal para canais longos com TikTok: o video longo deve ser planejado desde a pauta e o storyboard com possiveis blocos verticais de pouco mais de 1 minuto. Cada candidato deve conter um gancho claro, contexto suficiente, uma escalada de tensao ou revelacao e um fechamento que deixe curiosidade sem mutilar o argumento do longo. A selecao do corte acontece antes da edicao final para orientar enquadramento, legendas e pontos de transicao. A regra vale para qualquer canal da fabrica somente quando o usuario optar por manter uma conta correspondente no TikTok.
- Direcao de edicao aprovada para o Ruptura Oculta: documentario criminal tensionado, inspirado na intensidade do Insanity, na leitura de interrogatorios do JCS e na costura documental de referencias semelhantes, sem copia direta. A narracao original e a espinha dorsal; trechos reais, documentos, fotos, mapas, timelines e telas de evidencia entram com comentario, pausas, zooms discretos, congelamentos, sound design e movimento leve. A producao deve economizar creditos evitando avatar, video gerado por IA em cada cena, animacoes complexas e troca freneticamente generica de imagens. O efeito de alto valor deve vir de ritmo, silencio, selecao de evidencia, voz e montagem.
- Duracao aprovada para videos longos: minimo de 20 minutos e maximo de 24 minutos. A faixa deve ser cumprida pelo master final, sem alongar o episodio com repeticao ou preenchimento; casos que nao sustentem a duracao devem ser recusados ou reestruturados antes da producao.
- Restricoes explicitas de edicao: nao usar video gerado por IA para cada cena, avatar falando, animacoes complexas, excesso de transicoes, trilhas caras, imagens genericas trocadas freneticamente ou blocos longos de bodycam sem analise. Essas praticas ficam fora do padrao do canal; qualquer excecao futura precisa de justificativa editorial e aprovacao especifica.

## Identidade visual aprovada do Ruptura Oculta

Data: 2026-07-29.

- Foto de perfil aprovada pelo usuario.
- Paleta aprovada: preto e vinho como base, com carvao, branco envelhecido e contraste suficiente para leitura em telas pequenas.
- Thumbnails podem fugir pontualmente da paleta quando isso for necessario para contraste, legibilidade ou impacto editorial, mas o padrao deve permanecer preto e vinho.
- O efeito de nevoeiro usado na identidade deve continuar aparecendo como recurso de atmosfera, sem encobrir a leitura.
- Toda capa de video deve conter texto.
- Todos os textos de capa e thumbnail devem usar a mesma fonte agressiva e levemente pontiaguda da capa do canal.
- A hierarquia de cor dos textos pode alternar palavras em branco e em vinho dessaturado. Palavras em vinho podem receber reducao de opacidade, desde que continuem legiveis; esse tratamento funciona como assinatura visual do sentido de "oculta".

- Nova referencia visual aprovada para thumbnails: usar objetos como pistas materiais do caso, em composicoes de alto contraste e textura forte. Exemplos de linguagem observada no Dr Insanity/Viroscopo: correntes, cadeados, digitais, papeis, alfinetes, simbolos quebrados e retratos estilizados. No Ruptura Oculta, selecionar poucos objetos diretamente ligados ao episodio e evitar colagem generica; cada objeto precisa representar uma pergunta, evidencia ou conflito real.

## Comunidade aos domingos

Data: 2026-07-28.

- Decisao do usuario: todo domingo as 11h tera um post na Comunidade do YouTube, com imagem original e uma proposta de conversa bonita e interativa. O post deve acolher, fazer uma pergunta simples e relevante, e pode aproveitar de forma natural o tema do longo mais recente ou abrir escuta para uma pauta futura.
- O post de domingo nao e video, nem substitui os videos curtos da grade. Ele deve ser preparado junto com o pacote editorial da semana, sem uso de imagem generica ou CTA mecanico.
- A execucao do post dominical pertence ao chat de videos longos; o presente chat de curtos nao deve publicar esse slot quando a central despachar a agenda.
- Atualizacao do usuario em 2026-08-02: a publicacao na Comunidade do YouTube fica suspensa por enquanto. Nao preparar nem publicar o post dominical automaticamente ate nova autorizacao explicita.

## Longos pensados para cortes verticais

Data: 2026-07-29.

- Decisao do usuario para todos os canais atuais e futuros: quando um canal tiver TikTok, seus videos longos devem nascer com possiveis trechos verticais autonomos previstos no roteiro e no plano de edicao. Nao deixar a busca de cortes para depois do master pronto.
- Cada longo deve mapear pelo menos dois candidatos reais de aproximadamente 65 a 80 segundos, com gancho proprio, ideia compreensivel, desenvolvimento curto e fechamento ou ponte honesta. O objetivo e permitir curtos um pouco acima de um minuto sem enrolacao.
- O longo continua sendo uma obra completa: nao pode virar uma sequencia artificial de clipes nem sacrificar contexto, profundidade ou ritmo apenas para produzir cortes.
- O mapa de candidatos deve registrar inicio editorial, promessa, texto de gancho, funcao de retencao, final e riscos de contexto. Depois do master, a selecao final continua dependente da narracao, da sincronizacao e da qualidade real do trecho.
- Quando um canal nao tiver TikTok, esta regra nao cria obrigacao de produzir verticais; ela apenas preserva a possibilidade editorial caso essa distribuicao seja adotada depois.

## Operacao diaria do Facebook

Data: 2026-07-29.

- O Facebook de `A Palavra que Cuida` tera, como cadencia inicial, uma publicacao diaria pela manha.
- Cada post deve ser preparado no chat antes da publicacao manual pela usuaria, sempre considerando as publicacoes mais recentes do YouTube, com prioridade para o video mais recente.
- Todo post do Facebook deve direcionar para o canal do YouTube. A URL do canal deve ser incluida quando estiver confirmada; o handle ativo de referencia e `@apalavraquecuidabr`.
- A usuaria nao quer usar o perfil pessoal nem aparecer para atrair publico. As orientacoes de crescimento devem priorizar a propria pagina, conteudo original, colaboracoes, grupos quando permitidos e testes pagos controlados.

## Voz do Ruptura Oculta

Data: 2026-07-29.

- Direcao aprovada para o narrador: homem adulto, voz grave, segura e clara, com autoridade documental e sem teatralidade excessiva.
- A escolha masculina substitui a preferencia feminina anterior porque se alinha melhor ao padrao sonoro dos canais de referencia e ao tom documental criminal definido para o canal. A voz final ainda sera escolhida por teste real no Eleven v3, comparando perfis documental grave, intimo investigativo e frio cinematografico; o nome exibido pela biblioteca nao substitui a audicao em portugues brasileiro.
- O Eleven v3 sera usado com audio tags entre colchetes para orientar emocao, ritmo, entrega e reacoes humanas. As tags devem ser aplicadas com criterio, apenas em batidas narrativas que ganham com interpretacao; nao devem aparecer em toda frase nem substituir um bom texto.
- Tags candidatas para o canal: `[curious]`, `[concerned]`, `[thoughtful]`, `[quietly]`, `[whispers]`, `[sighs]`, `[hesitates]`, `[surprised]`, `[serious]` e `[slowly]`, sempre validadas na voz escolhida. Evitar tags que criem uma performance melodramatica ou contradigam os fatos.
- O roteiro deve marcar internamente as batidas de interpretacao e separar o texto enviado ao modelo das observacoes de producao. Gerar a narracao em blocos curtos e coerentes, porque o v3 e mais expressivo, mas pode variar mais; revisar abertura, miolo denso e fechamento antes de renderizar o episodio inteiro.
- Hierarquia de validacao: as recomendacoes tecnicas oficiais da ElevenLabs devem orientar o uso do v3, das tags, dos parametros e da segmentacao, desde que nao contrariem uma pratica ja testada, compreendida e aprovada como utilizacao legitima pelo usuario. Quando houver conflito, a identidade editorial do canal e a aprovacao humana prevalecem; a excecao deve ser documentada e validada por amostra.
- Correção de decisão em 2026-08-04: a voz-base aprovada pelo usuário para o Ruptura Oculta é `Marcelo Costa - Articulate and Balanced` (voice id `bJrNspxJVFovUxNBQ0wh`), na interpretação tensa/cinematográfica calibrada para o canal. `Bruno Cardoso` pertence ao canal A Palavra que Cuida e não deve ser reutilizado no Ruptura Oculta. A promoção anterior do Bruno para o episódio 01 foi um erro de registro e produção; os áudios correspondentes foram reclassificados como rejeitados por voz incorreta.
- Ponto de partida de performance do Marcelo: modelo `eleven_v3`, stability `0.42`, similarity boost `0.75`, style `0.28`, speed de geração `1.0`, speaker boost ativo e pós-processamento local em `1.08x` com pitch preservado. A direção deve preservar tensão controlada/cinematográfica, sem teatralidade, grave excessivo ou ritmo arrastado.

## Regra de clareza e emocao do audio do Ruptura Oculta

Data: 2026-08-01.

- O usuario aprovou o uso frequente e intencional das audio tags do Eleven v3, no formato `<emocao>`/tags entre colchetes conforme o formato aceito pelo modelo, para evitar uma narracao generica e dar tensao real a cada bloco.
- As tags devem ser distribuidas por funcao narrativa: curiosidade no gancho, preocupacao na escalada, seriedade em fatos graves, pausa ou entrega mais baixa em revelacoes e firmeza nas conclusoes. Nao usar a mesma emocao mecanicamente em todas as frases.
- A prioridade absoluta continua sendo a audibilidade: texto revisado, palavras simples quando possivel, frases com respiracao natural, pontuacao clara e velocidade que nao engula consoantes ou finais de palavra.
- Todo episodio deve passar por uma revisao textual antes da geracao e por uma escuta de controle depois da geracao. Trechos com erro de pronuncia, palavra pouco audivel, emocao exagerada ou ritmo arrastado devem ser regenerados isoladamente, sem desperdiçar creditos refazendo o episodio inteiro.
- A narracao sera produzida em blocos curtos e semanticamente fechados. As tags entram no texto de producao, mas nunca devem ser lidas pelo narrador; a versao final precisa ser conferida contra o roteiro aprovado.

- Antes de cada geracao, preservar acentos e grafia completa do portugues brasileiro. Pontuacao deve ser revisada para controlar pausas, evitar frases longas e impedir que o v3 desloque a enfase. Palavras com risco de erro de pronuncia devem ser testadas isoladamente ou em frase curta antes de entrar no episodio.

- Falhas observadas em testes anteriores de `A Palavra Que Cuida` e confirmadas na calibracao do Ruptura Oculta viram gate universal: nunca remover acentos, nunca gerar episodio inteiro sem amostra aprovada, conferir audio palavra por palavra contra o texto e regenerar blocos com erro antes da montagem. Um arquivo com emocao bonita, mas pronuncia ou pontuacao errada, e reprovado.

## Referencia editorial adicional do Ruptura Oculta

Data: 2026-08-02.

- O usuario aprovou observar o canal Viroscopo, especialmente o video `Como a internet resolveu um misterio 36 anos depois`, como referencia de admirador para estrutura de documentarios criminais, perguntas investigativas, aprofundamento e promessa clara de titulo. A inspiracao deve ser adaptada ao Ruptura Oculta, sem copiar roteiro, identidade, frases, thumbnails ou montagem.

## Regra de profundidade sem preenchimento do Ruptura Oculta

Data: 2026-08-02.

- O usuario definiu que os documentarios devem ser completos, detalhados e bem contextualizados, mas nunca esticados artificialmente para atingir uma minutagem.
- Cada bloco precisa acrescentar algo: fato novo, contexto, evidencia, contradicao, consequencia, analise ou virada narrativa. Repetir a mesma informacao com palavras diferentes e considerado falha de roteiro.
- Imagens, trechos documentais e telas de apoio precisam cumprir funcao editorial clara. Nao usar imagem generica, plano vazio ou montagem decorativa apenas para ocupar tempo.
- A faixa de duracao de referencia passa a ser aproximadamente 28 a 38 minutos, com casos excepcionais podendo chegar a 45 quando a pesquisa sustentar. A duracao final continua subordinada a completude e a qualidade do caso, nao o contrario.

## Regra de montagem documental e economia de narracao

Data: 2026-08-02.

- Quando uma gravacao real ja comunica a acao, a emocao ou a reacao de forma compreensivel, deixar a cena se desenvolver sem cobrir cada segundo com narracao.
- A voz do Bruno deve entrar em comentarios certeiros e pontuais: situar o momento, chamar atencao para uma evidencia, explicar uma contradicao ou fazer a ponte para a proxima parte. Nao descrever literalmente tudo o que o espectador esta vendo.
- A narracao deve ser economizada em blocos de imagens e gravacoes que funcionam sozinhos. Isso reduz custo de ElevenLabs sem reduzir densidade editorial.
- Materiais escritos entram como evidencias visuais: manchetes, documentos, datas, locais, nomes de operacoes, trechos curtos e citacoes essenciais. Exibir o titulo ou uma frase-chave pode ser melhor do que narrar o texto inteiro; leituras completas so entram quando o documento for central para a compreensao.
- Toda informacao escrita precisa ter funcao e fonte identificavel. Evitar telas cheias de texto, leitura acelerada e materiais usados apenas como decoracao.
- O uso de videos de terceiros deve passar por verificacao de origem, permissao/licenca aplicavel e transformacao editorial suficiente. Priorizar materiais oficiais, jornalisticos e licenciados, sempre com comentario, contexto ou analise proprios.

## Direcao de sound design e textos em tela do Ruptura Oculta

Data: 2026-08-02.

- O usuario aprovou estudar a linguagem de edicao do canal Dr Insanity como referencia de admirador, especialmente textos que entram como digitacao, sons de teclado e cliques, impactos discretos, transicoes sonoras, ambiencias, silencias e efeitos sincronizados com evidencias ou mudancas de cena.
- O sound design deve aumentar a tensao sem virar uma camada barulhenta. Cada efeito precisa marcar uma acao, revelacao, documento, mudanca de tempo ou ponto de virada; nao usar efeitos aleatorios em toda troca de imagem.
- Textos em tela podem simular digitacao quando apresentarem mensagens, documentos, datas, titulos, nomes de operacoes ou frases-chave. A leitura deve ser curta, grande e legivel, com tempo suficiente para o espectador compreender.
- A referencia Dr Insanity serve para linguagem e ritmo, nunca para copiar identidade, roteiro, frases, thumbnails, sequencias ou assets.
