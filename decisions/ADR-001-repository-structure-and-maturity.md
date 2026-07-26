# ADR-001 — Estrutura de repositório e maturidade por capacidade

**Status:** aceito em 2026-07-26.

## Contexto

O primeiro caso real é `A Palavra que Cuida`, mas a fábrica deve atender
operações concretas de conteúdo sem pressupor nicho, marca, plataforma ou
formato. A estrutura anterior colocava a implementação em `ai/`, tratava
`00_incubadora` como estágio físico e usava o nome do primeiro canal como raiz
operacional.

## Decisão

- `factory/` contém a implementação reutilizável: contratos, núcleo,
  políticas, skills e testes.
- `operations/` é a coleção neutra de operações concretas. O nome é curto,
  não presume que toda operação seja um canal e separa claramente o núcleo do
  caso concreto. Esta é uma decisão arquitetural, não uma alegação de padrão
  universal.
- `operations/a-palavra-que-cuida/` é a instância concreta atual.
- `ai/` fica limitado a memória e orientação do agente. Referências antigas
  dentro da memória continuam sendo evidência histórica.
- `research/` guarda experimentos e o estado de maturidade. “Casulo” é um
  regime de decisão baseado em evidência, não o nome de uma pasta.
- `audits/` guarda retrospectivas e auditorias; `decisions/` guarda decisões
  versionáveis que sobreviveram à conversa.

## Ciclo de vida de uma operação

`exploring -> incubating -> piloting -> stabilizing -> operational`

`paused` e `retired` são saídas administrativas. Promover uma operação não
promove automaticamente suas capacidades: cada uma possui estado próprio.

## Estados de capacidade

`unexercised`, `investigating`, `validating`, `stable`,
`regression_detected`, `blocked` e `not_applicable` descrevem a maturidade
individual. Estados `blocked` e `not_applicable` exigem motivo. `stable` exige
uma baseline ativa e evidência verificável.

## Contrato de baseline

Uma baseline é um artefato versionado, não uma impressão subjetiva. Ela
registra: capability, versão, escopo, condições, parâmetros rastreados,
evidências, testes, gate humano, execuções limpas e regras de invalidação.

Uma mudança em parâmetro rastreado torna a comparação incompatível e exige
revalidação explícita. A baseline anterior pode continuar como evidência, mas
não pode sustentar o estado `stable` da configuração nova.

## Compatibilidade e migração

`ChannelManifest`, `channel` e `video` permanecem compatíveis como vocabulário
legado. Novas superfícies usam `OperationManifest`, `operation` e `content`.
O repositório não cria espelhos vazios ou caminhos de compatibilidade; a tabela
da auditoria registra a origem histórica.

## Consequências

- A primeira operação continua sendo o campo de prova, sem virar dependência
  do núcleo.
- A promoção para `operational` depende de evidência por capacidade, não de
  quantidade de pastas ou de vídeos.
- Integrações específicas permanecem fora do núcleo e só entram em uma operação
  quando houver uso real e evidência correspondente.
