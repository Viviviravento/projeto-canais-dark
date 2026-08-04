# Auditoria retrospectiva do fluxo agentico

> Auditoria historica. Referencias a `ai/fabrica/` e `Canal Religioso/` preservam os caminhos existentes quando a evidencia foi produzida. Desde 2026-08-04, os destinos ativos sao `factory/` e `operations/a-palavra-que-cuida/`.

Data: 24 de julho de 2026.

Escopo: metamorfose inicial, instalacao das ferramentas, estruturacao da fabrica,
producao dos videos 001 a 003, primeiro derivado vertical e primeira publicacao.

## Veredito executivo

O projeto ja provou que consegue transformar uma ideia de canal em ativos reais:
identidade, publico, pesquisa, roteiro, narracao, imagens, avatar, montagem,
legendas, thumbnail, pacote de publicacao e um video publico. Isso e uma conquista
concreta.

O fluxo, porem, **ainda nao esta pronto para producao autonoma**. A fabrica v1
deve permanecer em `v1-candidate`. O terceiro video nao foi uma execucao limpa:
foi finalizado com divida de prosodia aceita pelo usuario, depois de o QA tecnico
aprovar um master que o crivo humano reprovou. A fabrica de canais tambem passou
somente por um ensaio seco estrutural de mukbang, nao por uma genese real com
piloto e observacao.

O diagnostico principal e:

> Temos um sistema rico em memoria e regras, mas ainda pobre em enforcement.
> Muitas decisoes corretas existem em Markdown, YAML e JSON; poucos desses
> controles governam obrigatoriamente os scripts que gastam dinheiro e geram o
> master.

Por isso o humano ainda atuou como detector de incidentes, revisor de regras ja
conhecidas e reconciliador de estado. O papel desejado e menor: aprovar amostras
compactas, exercer gosto onde ele importa e autorizar atos sensiveis.

## O que esta auditoria considera

Fontes principais:

- `ai/memoria.md`;
- `ai/preparacao-metamorfose.md`;
- `ai/fabrica/` e seus testes;
- `Canal Religioso/politicas/subesteira-v1.yaml`;
- manifests, revisoes humanas, incidentes, resultados e custos dos videos 001 a
  003;
- pacote de publicacao do piloto 001;
- registro de limpeza de midias de 24 de julho.

Limites:

- o tempo humano nao foi cronometrado, portanto esta auditoria nao inventa horas;
- a geracao de imagens integrada ao Codex, eletricidade e processamento local nao
  possuem preco unitario registrado;
- o desembolso inicial do HeyGen nao esta documentado;
- binarios rejeitados foram apagados, mas os registros textuais preservam parte
  suficiente das causas e decisoes;
- bloqueios do Google, OAuth e permissoes de provedores sao separados de erros
  internos quando sua causa foi externa.

## Resultado que realmente obtivemos

| Area | Resultado comprovado | Estado atual |
|---|---|---|
| Canal | `A Palavra Que Cuida`, publico, promessa, avatar e identidade definidos | Utilizavel |
| Ferramentas | OpenMontage, ElevenLabs, HeyGen, fal.ai, Pexels, Pixabay, FFmpeg/Remotion e yutu | Integradas em graus diferentes |
| Video 001 | Master, vertical, Short, thumbnail, metadados e publicacao publica | Publicado com dividas antigas |
| Video 002 | Master de 11:01, thumbnail e pacote de publicacao | Aprovado, ainda com dividas visuais registradas |
| Video 003 | Master de 11:19, thumbnail, pacote e dois derivados planejados | Finalizado com divida de voz aceita |
| Fabrica universal | Contratos, estados, gates, custos, incidentes, QA e seguranca | `v1-candidate`, pouco conectada ao executor real |
| Fabrica de canais | Ensaio seco de mukbang sem herdar regras religiosas | Valida estrutura, nao valida resultado |
| Metricas | Janelas e schemas definidos | Loop ainda nao fechado com observacoes reais |

## Custo e retrabalho observados

### Total corrigido

A auditoria de 23 de julho registrou 9 clipes fal.ai e total de
`US$ 13,395487 / R$ 68,06`. A revisao de 24 de julho encontrou 10 clipes. Com o
clipe omitido de `US$ 0,42`, o consumo economico corrigido dos tres videos e:

- **US$ 13,815487**;
- **R$ 70,19**, pela PTAX de `R$ 5,0807` usada nos registros;
- sem imagem integrada ao Codex, trabalho humano, computacao local e valor
  desconhecido colocado inicialmente no HeyGen.

Isso nao e igual ao dinheiro depositado. O desembolso minimo documentado e
`US$ 16`, composto por ElevenLabs Starter e recarga fal.ai, alem do aporte HeyGen
nao registrado. Saldo pre-pago e consumo economico precisam continuar separados.

### Onde o retrabalho apareceu

- ElevenLabs consumiu 29.767 creditos nos tres videos.
- Somente 11.347 foram atribuidos as narracoes finais.
- 18.420 creditos, ou **61,9%**, ficaram em testes e versoes descartadas.
- Pelo rateio do plano, isso equivale a `US$ 2,763 / R$ 14,04` de aprendizado e
  retrabalho. Nem tudo foi desperdicio: parte descobriu voz, configuracao e falhas
  reais. O erro foi repetir aprendizado caro que poderia ter sido isolado em
  amostras menores e mais representativas.
- O video 003 consumiu `US$ 3,422 / R$ 17,39` incluindo testes. O molde final
  reproduzivel foi estimado em `US$ 2,388 / R$ 12,13`. A diferenca de
  `US$ 1,034 / cerca de R$ 5,26`, ou **30,2% do custo do episodio**, foi
  principalmente experimentacao de voz.
- O HeyGen produziu 8 saidas concluidas e 103,01 segundos no conjunto dos tres
  videos. Como o registro nao separa de forma uniforme segundos finais de testes,
  a auditoria nao classifica uma parcela como desperdicio sem evidencia.
- A limpeza final apagou **1.209 arquivos** e liberou **6,262 GB**. Muitos eram
  caches legitimos, mas o volume mostra que candidato, rejeitado, derivado,
  canonico e recriavel nao estavam separados desde o nascimento do artefato.

## Retrospectiva por fase

### 1. Metamorfose e definicoes

**Erro:** o publico foi inicialmente inferido e tratado como variavel de video.

**Trabalho causado:** o usuario precisou interromper a materializacao, exigir
pesquisa brasileira e esclarecer que o publico e uma propriedade fixa do canal.

**Causa sistemica:** pressa para transformar uma ideia incompleta em estrutura.

**Correcao aprendida:** Regra de Cesar; separar input, hipotese, pesquisa,
observacao e decisao. Essa regra hoje esta bem registrada, mas precisa ser
validada por contrato em toda decisao relevante.

**Erro:** a primeira interpretacao de metamorfose virou estrutura prematura em
`ai/`, com workflows para perguntas que seriam respondidas uma unica vez.

**Trabalho causado:** varias rodadas para esclarecer que o casulo deveria
preservar decisoes e evidencias, e que a metamorfose era a passagem do abstrato
ao concreto.

**Causa sistemica:** confundir persistencia com automacao e completude visual da
arvore com maturidade do metodo.

**Correcao aprendida:** fabrica universal e subesteiras por canal. A arquitetura
atual representa isso, mas ainda precisa provar operacao real.

### 2. Pesquisa e escolha de ferramentas

**Erro:** a primeira busca por edicao de video foi rasa. O usuario encontrou o
OpenMontage com uma pesquisa simples, e as integracoes pagas dele foram
subestimadas na primeira leitura.

**Trabalho causado:** reinicio do bloco de ferramentas e revisao da matriz.

**Causa sistemica:** procurar uma ferramenta que correspondesse a uma categoria
preconcebida, em vez de pesquisar o problema de ponta a ponta e ler custos,
providers e limites reais.

**Correcao aprendida:** OpenMontage e executor, nao cerebro; imagem integrada ao
Codex nao precisa ser duplicada por outro provedor; avatar e voz merecem escolhas
deliberadas; stock e video podem ter multiplos fornecedores.

**Erro:** a coleta de chaves foi proposta antes de as contas e ferramentas serem
decididas.

**Trabalho causado:** o usuario precisou frear a coleta e recolocar a sequencia
correta.

**Correcao aprendida:** decidir capacidade e necessidade, criar conta, escolher
permissoes minimas e somente entao coletar o segredo pela janela segura.

### 3. Modelo economico

**Erro:** durante parte do trabalho, `economizar` foi operacionalizado como
reduzir gasto direto, mesmo quando isso empobrecia a cena.

**Sintomas:** imagens genericas, movimento aplicado a objetos sem funcao,
repeticao e tentativa de fazer materiais baratos sustentarem uma mensagem para a
qual nao eram adequados.

**Trabalho causado:** remontagem integral do video 002 e varias correcoes humanas.

**Correcao aprendida:** otimizar custo total, incluindo chance de refacao,
operacao humana, confiabilidade, reutilizacao e retorno. Essa correcao ja entrou
no nucleo e na politica de midia.

**Erro:** o controle financeiro teve mais de uma verdade simultanea.

**Evidencia:** o `run-v1.json` do video 003 registra `US$ 2,1314` no pacote
original e `US$ 3,24535` com retries; a auditoria posterior registra
`US$ 3,42235`; depois, a contagem fal.ai global mudou de 9 para 10 clipes.

**Causa sistemica:** cotacoes e reconciliacoes ficaram espalhadas em arquivos
por provedor, resumos manuais e convencoes diferentes de custo.

**Correcao necessaria:** ledger append-only unico por run, com `cash_outlay`,
`allocated_usage`, `observed_debit`, `provider_job_id` e `retry_parent` como
campos distintos. Resumos devem ser derivados, nunca digitados separadamente.

### 4. Voz e artefato performatico

**Erro:** o primeiro metodo tratou o texto como prosa a ser lida, nao como fala a
ser interpretada. O resultado foi descrito pelo usuario como um aluno lendo sem
compreender o contexto.

**Erro:** a tentativa de controlar a prosodia do video 002 inseriu 42 tags
`<break>` em oito blocos, somando 34,9 segundos de pausas artificiais.

**Erro:** a calibracao v2 do video 003 supersegmentou a fala. A calibracao v3
aprovou escrita oral continua, mas essa aprovacao local foi extrapolada para o
episodio inteiro. Do meio para o fim, a prosodia voltou a falhar.

**Erro:** instrucoes presentes no `performance_contract` foram tratadas como se
controlassem o provedor, embora o payload real enviasse somente texto,
configuracao, idioma, seed e contexto textual.

**Trabalho causado:** duas narracoes completas no video 002; no video 003, pelo
menos uma narracao inicial, calibracoes, nova narracao integral, teste isolado da
cauda e retime local. O usuario precisou ouvir repetidamente masters longos para
descobrir falhas que amostras corretas deveriam ter exposto.

**Causa sistemica:** o gate media conformidade textual e tecnica, mas ainda nao
media estabilidade semantica em pontos representativos do episodio.

**O que funcionou:** voz Bruno Cardoso, portugues explicito, blocos semanticos,
pontuacao natural, ausencia de pausas mecanicas e retime local em `1.05x`. O
retime corrige velocidade global, nao prosodia interna.

**Estado:** gate de voz `restored`, zero execucoes limpas. Divida aceita no video
003 nao conta como aprovacao do metodo.

### 5. Planejamento e aquisicao visual

**Erros observados:**

- imagens repetidas e genericas;
- cenas sem relacao suficiente com a fala;
- dinheiro gasto animando o elemento errado, como um objeto sem funcao em vez da
  interacao humana relevante;
- texto achatado por cima de cadernos, cartas ou rotulos, em vez de pertencer
  fisicamente ao objeto;
- papeis em branco usados como apoio visual;
- versiculo exibido apenas em parte enquanto a narracao lia o trecho completo;
- referencia biblica falada sem o nome do livro;
- cenas longas demais sobre o mesmo ativo.

**Trabalho causado:** o video 002 teve a timeline reconstruida em 124 planos. A
revisao foi feita sem nova chamada paga, o que foi uma boa recuperacao, mas
consumiu edicao, renderizacao e crivo humano.

**Causa sistemica:** a selecao visual acontecia perto demais da composicao e sem
um pacote pequeno de aprovacao semantica. A regra existia depois do incidente,
nao antes dele.

**O que funcionou:** cenarios brasileiros, natureza, animais, artesanato,
personagens proprios, imagens biblicas contextualizadas e acervo curado. A
biblioteca ja e um patrimonio real do canal.

### 6. Avatar e composicao

**Erro:** a primeira edicao visual do avatar confundiu tom de pele com iluminacao
e chegou a alterar sua leitura racial.

**Erro:** mesa e fundo verde foram recortados de forma que a mesa parecia um
retangulo solto.

**Erro critico no video 003:** o avatar parecia sentado, enquanto a unica cadeira
visivel estava ao lado. O personagem parecia sentado no ar.

**Trabalho causado:** novas imagens-base, composicoes e revisao final. A correcao
da cadeira foi local e sem nova chamada paga, o que foi eficiente.

**Causa sistemica:** o QA guardava keyframes, mas nao exigia um veredito sobre
apoio corporal, contato, oclusao, perspectiva, escala e iluminacao. Ter um
keyframe nao significa ter entendido a cena.

### 7. Sincronizacao, legendas e derivados verticais

**Erro:** textos do horizontal apareceram antes da fala em alguns momentos.

**Erro:** o primeiro vertical misturou legenda literal com outra mensagem no
rodape, criando competicao cognitiva.

**Erro de implementacao comprovado:** `Audio` de `@remotion/media` aceitava
`trimBefore`, mas o projeto usou `startFrom`. O parametro foi ignorado: o audio
comecou no zero do master e as legendas em outro ponto.

**Erro editorial:** um corte comecou em `Mas voce pode...`, como se o espectador
tivesse ouvido a frase anterior.

**Trabalho causado:** varias revisoes do vertical ate chegar ao arquivo
autocontido de 62,2 segundos. O usuario precisou identificar que legenda e fala
nao correspondiam e que a abertura nao era autonoma.

**Correcao aprendida:** extrair primeiro o audio exato, gerar legenda literal a
partir dele, validar 10 a 15 segundos renderizados e transcritos, e so depois
renderizar o vertical completo. Cabecalho editorial pode existir; rodape e fala
devem corresponder.

### 8. QA e aprovacao

**Erro central:** QA tecnico foi confundido repetidamente com qualidade
semantica. Loudness, ausencia de preto, duracao, hashes e keyframes passaram em
masters que o usuario reprovou por prosodia ou fisica visual.

**Causa sistemica:** os testes conseguem verificar o que foi declarado no
manifesto, mas nao provam que a declaracao e verdadeira. Por exemplo,
`physical_coherence_review: passed` ainda depende de um observador competente.

**Trabalho causado:** defeitos foram descobertos no master integral, quando a
correcao ja exigia remontagem, nova audicao longa ou nova chamada paga.

**Correcao necessaria:** separar quatro resultados:

1. integridade tecnica automatica;
2. correspondencia objetiva, como fala versus legenda e citacao versus tela;
3. auditoria semantica por cenas e keyframes;
4. aprovacao humana do master enquanto o gate estiver `full` ou `restored`.

Nenhum desses resultados pode promover implicitamente o outro.

### 9. Estado, entrega e publicacao

**Erro:** `pronto`, `gerado`, `refeito`, `exportado`, `enviado ao provedor` e
`publicado` foram usados de forma ambigua em alguns momentos. O usuario precisou
perguntar mais de uma vez se o video realmente havia sido refeito ou publicado.

**Erro recorrente de interface:** o usuario precisou repetir que midia local deve
ser mostrada no Explorador de Arquivos do Windows.

**Bloqueios externos:** conta Google desativada, OAuth com cliente desabilitado e
aplicativo em teste sem testador autorizado. Esses bloqueios nao foram criados
pela edicao, mas o preflight de publicacao nao os detectou cedo.

**Inconsistencia atual:** o pacote do piloto 001 registra corretamente o video
publico `ZkmCkF6XR_g`, mas `09_metricas/README.md` ainda afirma que OAuth e
publicacao real estao pendentes. O `run-v1.json` do video 003 tambem preserva um
estado historico de bloqueio do Google. Nao existe uma fonte operacional unica de
verdade.

**Correcao necessaria:** todo run precisa de um estado canonico e vocabulario
fechado, por exemplo `planned`, `quoted`, `paid_in_progress`, `asset_ready`,
`proxy_ready`, `human_rejected`, `master_approved`, `uploaded_unlisted`,
`published_public` e `metrics_due`.

### 10. Incidentes de integracao

**Erro:** um HTTP 403 no endpoint administrativo de billing da fal.ai foi
interpretado inicialmente como problema de credito da producao, embora a geracao
continuasse funcionando e a chave apenas nao pudesse ler aquele endpoint.

**Trabalho causado:** confusao sobre saldo, tentativa de suporte e investigacao
fora do ponto correto.

**Erro comprovado no Pexels:** o downloader usava a posicao mutavel do resultado
de busca, nao o ID imutavel aprovado na folha de contato.

**O que funcionou:** ambos viraram incidentes documentados. O protocolo de
congelar, investigar sem repetir efeito pago e retomar por ID e a direcao certa.

### 11. Limpeza e reprodutibilidade

**Acerto:** a limpeza preservou masters, audios canonicos, legendas, imagens e
registros relevantes, liberando 6,262 GB.

**Erro critico:** ela tambem removeu evidencias ainda referenciadas por arquivos
ativos. Exemplos ausentes:

- `Canal Religioso/05_audio/video-003/v2/audio-qa-v2.json`;
- `Canal Religioso/05_audio/video-003/v1/audio-qa-v1.json`;
- avaliacoes das calibracoes v2 e v3.

O `run-v1.json`, o gate de audio e o validador de pre-producao ainda apontam para
esses caminhos. Assim, o video final existe, mas a cadeia completa de evidencia
nao e reproduzivel nem revalidavel como esta.

**Causa sistemica:** a limpeza usou classes amplas de arquivo sem um grafo de
referencias e sem tombstone para artefatos removidos.

**Correcao necessaria:** nenhum arquivo citado por run, gate, incidente, custo ou
QA pode ser apagado. Artefato grande recriavel pode sair, mas seu manifesto,
hash, gerador, fonte e motivo de descarte precisam permanecer.

## Falhas da propria Metamorfose v1

### A arquitetura nao e ainda a orquestracao

O nucleo possui `FactoryRun`, `CostLedger`, `GatePolicy`, seletor de midia e
`audit_package`, mas a busca de uso mostra que quase todos aparecem apenas nos
testes. Nos scripts reais do canal, o principal uso universal e validar schemas.
O `run-v1.json` foi mantido como documento; ele nao comandou obrigatoriamente
cada transicao.

Consequencia: um script especifico do episodio pode gerar, gastar ou sobrescrever
estado sem passar por todos os controles universais.

### A subesteira e normativa, nao executavel

`subesteira-v1.yaml` contem boas exigencias, mas hoje elas sao listas de texto.
Nao ha um compilador que transforme cada requisito em check automatico, gate
humano ou `not_applicable` justificado.

Consequencia: regras passam a existir depois que o usuario detecta o defeito, mas
nao impedem necessariamente a repeticao no proximo script.

### Os testes de aceitacao sao majoritariamente estruturais

O teste de mukbang confirma que um `run.json` contem todas as macroetapas e
termina corretamente em `not_applicable`. Ele nao executa pesquisa, compara
teses, testa captura nem mede resposta de publico.

Consequencia: o ensaio prova isolamento de estrutura, nao uma fabrica de canais
operacional.

### O terceiro video nao aprovou a fabrica de videos

O master foi finalizado por autorizacao humana com divida conhecida. O gate de
voz esta `restored`, o editorial-visual permanece `full`, publicacao e aprendizado
do run estao pendentes.

Consequencia: promover a arquitetura a v1 agora transformaria uma excecao
consciente em falsa evidencia de autonomia.

## Trabalho humano que o fluxo provocou

Sem inventar duracao, o trabalho observavel incluiu:

- corrigir o conceito de publico e metamorfose;
- encontrar uma ferramenta melhor que a pesquisa inicial do agente;
- explicar prioridades de avatar, custo e qualidade;
- ouvir varias narracoes e masters longos;
- identificar pontuacao, ritmo e referencias biblicas incompletas;
- detectar repeticao, imagem sem sentido, papel em branco e texto falso;
- detectar mesa recortada e avatar sentado no ar;
- descobrir que legenda e fala do vertical nao correspondiam;
- perguntar repetidamente qual arquivo era o atual e se a operacao havia sido
  realmente executada;
- navegar bloqueios de conta, OAuth, verificacao e publicacao;
- pedir reconciliacao de saldo e corrigir a contagem de uso.

Esse e o principal custo oculto. O gasto de API foi pequeno em reais; a carga de
atencao do usuario foi grande. Otimizacao de custo precisa incluir essa carga.

## O que funcionou e deve ser preservado

- Regra de Cesar e pesquisa antes de decisao relevante.
- Usuario como fonte de gosto e contexto, nao como operador manual da esteira.
- Coleta segura de credenciais.
- Separacao entre fabrica universal e politica local do canal.
- Roteiro editorial separado de artefato performatico.
- Voz externa no ElevenLabs alimentando o HeyGen.
- Imagens proprias, cenarios brasileiros, natureza, animais e artesanato.
- Stock somente quando semanticamente adequado.
- Movimento pago reservado a acao que carrega argumento.
- Composicao local para corrigir problemas sem repetir chamada paga.
- Legendas obrigatorias e derivados recompostos para vertical.
- Citacoes ACF registradas e comparacao integral fala/tela.
- Cotacao antes de lote pago e ausencia de retentativa automatica.
- Registro de incidentes com causa, correcao e ponto de retomada.
- Divida aceita explicitamente sem virar padrao de qualidade.

## Correcoes obrigatorias antes do video 004

### P0 - impedir repeticao do retrabalho

1. **Criar um runner real da fabrica.** Toda operacao do video 004 deve nascer de
   um `FactoryRun` canonico e passar por transicoes validadas. Scripts especificos
   nao podem pular o runner.
2. **Unificar estado.** Um arquivo canonico informa o que existe, o que foi
   aprovado, o que foi rejeitado, o que foi publicado e qual e a proxima acao.
   Outros documentos apenas referenciam esse estado.
3. **Unificar custos.** Um ledger append-only recebe cotacao, reserva, job do
   provedor, debito, falha e retentativa. Todo resumo financeiro e derivado dele.
4. **Registrar ciclo de vida de artefatos.** Estados minimos: `candidate`,
   `approved`, `canonical`, `rejected`, `derived` e `recreatable`. Limpeza consulta
   referencias antes de excluir.
5. **Calibrar voz em tres regioes reais.** Abertura, miolo denso e CTA devem usar
   o texto e os parametros exatos da narracao integral. Nenhuma narracao completa
   antes das tres aprovacoes enquanto o gate estiver restaurado.
6. **Revisar o storyboard antes da aquisicao paga.** Entregar folha de contato com
   funcao da cena, fala correspondente, fonte, repeticao prevista e motivo de
   movimento. Aprovar lacunas, nao cada frame.
7. **Testar composicao do avatar em still/proxy.** Apoio, contato, oclusao,
   perspectiva, escala, luz, mesa e cadeira precisam ser aprovados antes de
   render longo ou novo HeyGen.
8. **Renderizar proxy antes do master.** Video leve com audio final, legendas,
   cenas e telas biblicas. O master 1080p so nasce depois do QA semantico do proxy.
9. **Validar um trecho vertical renderizado.** Extrair audio, transcrever a saida
   e comparar legenda literal antes do render completo.
10. **Atualizar a verdade operacional.** Registrar publicacao do 001 na camada de
    metricas e remover afirmacoes ativas de que nenhum video foi publicado.

### P1 - reduzir trabalho humano sem reduzir qualidade

1. Transformar cada requisito da subesteira em um dos tipos:
   `automatic_check`, `human_sample_gate`, `human_final_gate` ou
   `not_applicable_with_reason`.
2. Substituir scripts nomeados por episodio por configuracao de run e componentes
   reutilizaveis.
3. Criar preflight de caminhos: nenhum run pode ser declarado reproduzivel se
   referenciar artefato ausente.
4. Criar comparacao automatica entre texto canonico, audio transcrito, SRT e texto
   exibido nas citacoes.
5. Gerar relatorio de repeticao e cobertura do acervo antes da composicao.
6. Fazer preflight read-only de sessao Google/yutu antes de iniciar upload.
7. Entregar toda midia local abrindo o Explorador com o arquivo selecionado e
   registrar o caminho canonico na atualizacao ao usuario.

### P2 - promover automacao somente com evidencia

1. Tres execucoes comparaveis limpas permitem reduzir o gate para amostragem.
2. Seis aprovacoes amostradas permitem automacao daquele gate especifico.
3. Defeito critico, mudanca de modelo/preco ou perda de confianca restaura o gate.
4. Uma execucao com divida aceita nao conta como limpa.
5. A fabrica de canais so passa no teste quando um segundo canal atravessar
   pesquisa, piloto real e observacao sem herdar politica religiosa.
6. A arquitetura pode virar v1 antes das metricas editoriais, mas as politicas de
   desempenho permanecem v0.x ate haver coortes reais.

## Fluxo corrigido para o proximo episodio

`tema e evidencia`

`-> roteiro canonico e controle biblico`

`-> artefato performatico`

`-> amostras de voz: abertura + miolo + CTA`

`-> storyboard e folha de contato`

`-> cotacao consolidada em USD e BRL`

`-> narracao integral`

`-> alinhamento, SRT e verificacao de referencias`

`-> aquisicao apenas das lacunas aprovadas`

`-> proxy horizontal e amostra vertical`

`-> QA tecnico + objetivo + semantico`

`-> crivo humano do proxy`

`-> master final e pacote de publicacao`

`-> crivo humano final enquanto gates estiverem restaurados`

`-> publicacao, estado canonico e snapshots de metricas`

O principio e simples: **descobrir defeito no menor artefato capaz de revelá-lo**.
Nao pedir ao usuario para revisar vinte detalhes soltos, mas tambem nao esperar o
master de onze minutos para descobrir um problema que cabia numa amostra de
quarenta segundos ou numa folha de contato.

## Definicao de execucao limpa

Um video so conta para promocao de gate quando:

- nenhuma regra ja conhecida precisa ser lembrada pelo usuario;
- nenhuma chamada paga e repetida por erro evitavel de input, estado ou codigo;
- custos cotados e observados reconciliam no ledger;
- todos os artefatos referenciados existem ou possuem tombstone reproduzivel;
- voz passa nas amostras e no crivo integral correspondente ao gate;
- fala, legenda, referencia e texto biblico exibido correspondem;
- storyboard aprovado e master nao introduzem imagem semanticamente falsa;
- avatar composto respeita fisica e recorte;
- vertical comeca autocontido e legenda literalmente a fala;
- status de entrega e publicacao nao e ambiguo;
- nao ha divida critica aceita apenas para encerrar o episodio.

## Decisao de promocao

**Nao promover `ai/fabrica` para v1 agora.**

Continuar com pilotos supervisionados. O video 004 deve ser tratado como teste de
aceitacao operacional da fabrica corrigida, nao apenas como mais um episodio. A
promocao pode ser reavaliada quando:

- o runner governar a execucao real;
- custo e estado tiverem uma unica verdade;
- a limpeza nao quebrar referencias;
- audio e visual completarem uma execucao limpa;
- publicacao e primeira observacao de metricas fecharem o ciclo.

## Evidencias locais principais

- `Canal Religioso/06_edicao/custos/auditoria-videos-001-003-2026-07-23-v2.json`
- `Canal Religioso/06_edicao/custos/capacidade-baseada-video-003-2026-07-24.md`
- `Canal Religioso/06_edicao/limpeza-midias-2026-07-24.json`
- `Canal Religioso/06_edicao/video-002/resultado-producao-v2.md`
- `Canal Religioso/06_edicao/video-003/human-review-v1.json`
- `Canal Religioso/06_edicao/video-003/human-review-v2.json`
- `Canal Religioso/06_edicao/video-003/human-review-v3-authorization.json`
- `Canal Religioso/06_edicao/video-003/incidentes/elevenlabs-semantics-v1.json`
- `Canal Religioso/06_edicao/video-003/incidentes/avatar-composite-physics-v1.json`
- `Canal Religioso/06_edicao/video-003/incidentes/pexels-search-order-v1.json`
- `Canal Religioso/06_edicao/video-003/run-v1.json`
- `Canal Religioso/08_publicacao/piloto-001-publicacao-v1.json`
- `Canal Religioso/09_metricas/README.md`
- `ai/fabrica/core/cli.py`
- `ai/fabrica/tests/test_core.py`
