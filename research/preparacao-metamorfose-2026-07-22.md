# Preparacao da Metamorfose

> Documento historico de 2026-07-22. Os caminhos `ai/fabrica/` e `ai/auditorias/` abaixo registram a estrutura existente na data. Desde 2026-08-04, os destinos ativos sao `factory/` e `audits/`.

Data da revisao: 2026-07-22.

## Estado

Estado historico do casulo anterior a implementacao da candidata v1.

A candidata foi materializada em `ai/fabrica/`, mas nao foi promovida. A
auditoria dos videos 001 a 003 encontrou falhas de enforcement,
reprodutibilidade, estado e QA semantico. O veredito atual esta em
`audits/retrospectiva-fluxo-agentico-videos-001-003-v1.md`.

Opcao escolhida naquele momento: **B**.

O projeto ainda nao sera convertido em uma arquitetura versionada e fechada. Primeiro serao preservadas as evidencias, decisoes, capacidades aprovadas e lacunas que precisam ser resolvidas. Este documento nao e um roadmap de implementacao; e o inventario de prontidao do casulo.

## Objetivo completo

O sistema final nao e apenas uma automacao de videos. Ele deve operar duas fabricas aninhadas.

### Fabrica de canais

E a camada metafisica ou de genese. Sua funcao e transformar uma possibilidade abstrata em um canal testavel e, depois, em uma subesteira propria:

1. Imaginar teses e espacos possiveis.
2. Captar sinais em publico, cultura, busca, concorrencia e economia.
3. Separar dados, hipoteses, preferencias e decisoes.
4. Desenvolver publico, problema, promessa, posicionamento e limites.
5. Amadurecer identidade, formatos possiveis, linguagem e modelo economico.
6. Selecionar ferramentas conforme qualidade, custo e automatizacao reais.
7. Conceber pilotos que reduzam incertezas relevantes.
8. Publicar, observar e aprender.
9. Cristalizar a subesteira do canal somente depois de evidencia suficiente.

Um novo canal nao deve nascer como copia tematica de A Palavra Que Cuida. Ele herda principios universais da fabrica, mas precisa conquistar suas proprias definicoes.

### Fabrica de videos

Opera dentro de cada canal e transforma uma pauta em ativos publicados e aprendizado:

- captacao e selecao de tema;
- pesquisa e verificacao;
- promessa, argumento e roteiro;
- voz e sincronizacao;
- plano visual e alocacao de midia com custo otimizado;
- geracao, stock, avatar e composicao;
- edicao, legendas e QA;
- titulo, thumbnail e metadados;
- publicacao horizontal e vertical;
- distribuicao entre plataformas;
- metricas, diagnostico e memoria.

### Nucleo universal

As duas fabricas compartilham infraestrutura que nao pertence a um nicho especifico:

- Regra de Cesar e proveniencia da evidencia;
- coleta segura de segredos;
- registro de licencas e direitos;
- catalogo de ferramentas e capacidades;
- preflight de custo em moeda real;
- armazenamento e catalogacao de ativos;
- execucao local deterministica;
- logs, manifestos, checkpoints e rastreabilidade;
- interfaces de aprovacao humana;
- leitura de metricas e retroalimentacao.

## O que ja tem evidencia pratica

- Um canal passou da abstracao para identidade, publico, avatar, limites editoriais e dois videos completos.
- ElevenLabs, HeyGen, fal.ai, stock, Remotion, FFmpeg/OpenMontage e empacotamento local foram usados na pratica, com capacidades e problemas observados.
- Existe uma direcao de voz aprovada e um metodo melhor de geracao por blocos semanticos.
- Existem regras concretas para citacoes biblicas, legendas, tela final, CTA, texto diegetico, variedade visual, thumbnails e reaproveitamento vertical.
- A producao ja registra ativos, arquivos canonicos, custos observados, dividas aceitas e pacotes de publicacao.
- YouTube e TikTok possuem papeis comerciais definidos, com o TikTok servindo principalmente a aquisicao para o YouTube.

Essas conquistas devem ser preservadas. Elas nao eliminam as lacunas abaixo.

## Lacunas prioritarias

### 1. Genese de canais

Ainda nao existe um metodo comprovado para imaginar, comparar, amadurecer e validar um segundo canal. O canal religioso ensina muito sobre producao, mas uma unica instancia nao prova que a fabrica de canais e reutilizavel.

### 2. Captacao e selecao de temas

Ha fontes e criterios iniciais, mas ainda nao existe um metodo executado de ponta a ponta que una demanda, adequacao ao publico, profundidade possivel, concorrencia, custo de producao e destino entre plataformas.

### 3. Arquitetura de conteudo profundo

Os cinco subtipos foram rebaixados a lentes. Falta consolidar como o agente transforma uma boa pergunta em um argumento de 10 a 12 minutos que seja profundo, nao redundante, biblicamente responsavel e visualmente produzivel.

### 4. Pesquisa e revisao especializada

O canal religioso ainda precisa de um contrato confiavel para pesquisa biblica, contexto historico, divergencias interpretativas, versao citada e nivel de certeza. A qualidade de dois roteiros nao prova generalizacao.

### 5. Planejamento visual com custo otimizado

O objetivo nao e minimizar gasto, mas obter o resultado exigido sem pagar por processos desnecessarios. Ainda variam demais a pertinencia dos assets, a repeticao, a decisao entre stock e geracao, o movimento que merece custo e a qualidade de texto pertencente a objetos. O humano aprovou resultados, mas o agente ainda nao reproduz essa qualidade cegamente.

### 6. QA audiovisual

Sincronizacao, naturalidade da narracao, ritmo, recortes, texto diegetico e coerencia visual ainda exigem julgamento humano relevante. Precisamos decidir quais verificacoes podem ser automaticas e quais permanecem como calibracao ou aprovacao humana.

### 7. Gate financeiro

Nao sera usado um limite abstrato de `gasto aprovado`. Cada execucao paga precisa apresentar custo calculado em moeda real a partir do preco vigente, modelo e quantidade. Falta padronizar a cotacao antes e a conciliacao do debito depois entre APIs com unidades diferentes.

### 8. Publicacao e distribuicao reais

Os pacotes estao preparados, mas OAuth, publicacao efetiva, telas finais, links, TikToks recompostos e verificacao nas plataformas ainda nao completaram um ciclo operacional.

### 9. Metricas e aprendizagem

Ainda nao existem dados publicados do canal para validar tema, embalagem, retencao, conversao TikTok-YouTube, custo por resultado ou aderencia do publico. Sem isso, varias estrategias continuam hipoteses bem pesquisadas.

### 10. Fronteira humano-agente

A experiencia revelou gates humanos necessarios, mas eles ainda nao foram reduzidos ao minimo correto. O sistema final deve pedir decisao humana apenas onde houver gosto, risco, custo pago, credencial, publicacao irreversivel ou julgamento que as ferramentas nao resolvem com confianca.

## Gate financeiro desejado

Antes de uma chamada paga, o agente deve apresentar algo equivalente a:

> fal.ai, modelo X, quatro clips de cinco segundos. Preco vigente consultado: US$ X por segundo. Custo calculado deste lote: US$ Y. Posso executar?

Regras:

- usar moeda real, nao apenas creditos internos;
- informar a data do preco;
- discriminar quantidade e unidade cobrada;
- quando o custo depender do resultado, apresentar o maximo calculado em moeda real;
- agrupar chamadas homogeneas num unico pedido;
- registrar o debito observado depois da execucao;
- pedir nova aprovacao para retentativa paga;
- nao interromper por custo operacoes locais ou gratuitas ja autorizadas pela tarefa.

## Sinais de que o casulo esta pronto

A metamorfose podera ser iniciada quando for possivel descrever, sem inventar:

- como nasce e amadurece um canal novo;
- o que e universal e o que pertence a cada canal;
- quais artefatos atravessam cada etapa e por que existem;
- quais decisoes o agente toma sozinho;
- quais gates humanos permanecem e qual informacao apresentam;
- como custos pagos sao cotados e conciliados;
- como um video vai de tema a publicacao e reaproveitamento;
- como metricas alteram canal, pauta e producao;
- quais falhas exigem fallback, nova pesquisa ou parada.

Enquanto essas respostas ainda mudarem de natureza, continuamos no casulo. Quando mudarem apenas de parametro, estaremos prontos para materializar skills, agentes, schemas e workflows.
