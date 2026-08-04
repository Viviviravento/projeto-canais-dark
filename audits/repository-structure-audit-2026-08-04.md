# Auditoria estrutural do repositório

Data: 2026-08-04
Escopo: arquitetura, separação semântica, maturidade operacional e referências de caminho.
Fora do escopo: comportamento de ElevenLabs, produção audiovisual, chamadas pagas, credenciais e reescrita funcional da esteira.

## Diagnóstico

A raiz mistura operações concretas, uma incubadora temática e o núcleo candidato da fábrica. `ai/` também acumula memória, pesquisa histórica, auditorias, implementação, contratos, políticas, testes e instruções de integração. O núcleo é em grande parte reutilizável, mas ainda nomeia sua unidade principal como `ChannelManifest`, exige `channel_id` e modela lifecycle apenas no nível do canal. Não há contrato de baseline nem detecção determinística de invalidação.

O workspace contém 252 arquivos rastreados, 14 arquivos rastreados já modificados antes desta auditoria e 389 arquivos não rastreados. As operações têm grande volume de mídia local ignorada. A migração deve ser por renomeação no mesmo volume, sem copiar mídia, e deve preservar as mudanças preexistentes.

## Classificação predominante

| Elemento atual | Classificação | Observação |
| --- | --- | --- |
| `ai/fabrica/contracts`, `core`, `policies`, `tests` | `universal_implementation` | Núcleo candidato reutilizável; nome e manifesto ainda estreitos. |
| `ai/fabrica/skills` | `agent_instruction` | Capacidades opcionais reutilizáveis; TikTok é integração concreta, não pressuposto do núcleo. |
| `Canal Religioso/`, `Quase Celestial/`, `Ruptura Oculta/`, `Canal Instrumental Brain Rot/` | `operation_specific` | Operações concretas hoje especiais na raiz. |
| `Canal Religioso/politicas` e políticas vigentes em `01_briefs` | `active_policy` | Regras locais; não devem migrar para a fábrica. |
| Roteiros, publicação, métricas, QA e edição | `generated_artifact` | Artefatos da operação; a organização interna será preservada. |
| Pesquisas em `Canal Religioso/01_briefs` | `research` | Pesquisa local da operação, mantida junto dela. |
| `00_incubadora/mukbang-ensaio-seco` | `incubation_state` | Operação candidata com ensaio seco; lifecycle `incubating`. |
| `ai/preparacao-metamorfose.md` | `historical_memory` | Fotografia histórica de prontidão; não é runtime. |
| `ai/auditorias` | `audit` | Evidência histórica e veredito da candidata. |
| `ai/memoria.md` | `historical_memory` | Memória contextual viva do agente. |
| `agents.md` | `agent_instruction` | Porta de entrada e limites do agente. |
| `tools/` e OpenMontage local | `external_tooling` | Checkout/toolchain externo e ignorado; permanece fora da fábrica. |
| `.obsidian/` | `external_tooling` | Estado local de editor; ignorado. |
| PDF bíblico local | `research` | Fonte local ignorada; não será movida nem versionada. |

## Escolha da coleção de operações

Nome escolhido: `operations/`.

`operations` descreve uma unidade concreta de trabalho sem exigir canal, marca, plataforma, duração ou combinação de formatos. É compreensível em português técnico e inglês, distingue-se de `factory/`, funciona bem em caminhos e comandos e tem baixa chance de colisão com toolchains. `workspaces` colide semanticamente com o workspace local; `projects` é amplo demais e duplicaria o próprio repositório; `properties` é menos claro em português.

## Estrutura atual relevante

```text
ai/
├── auditorias/
├── fabrica/
├── memoria.md
└── preparacao-metamorfose.md
00_incubadora/
└── mukbang-ensaio-seco/
Canal Religioso/
Quase Celestial/
Ruptura Oculta/
Canal Instrumental Brain Rot/
```

## Estrutura proposta

```text
factory/                  # implementação universal e testes
operations/               # unidades concretas, sem pressuposto de canal
├── a-palavra-que-cuida/
├── mukbang-ensaio-seco/
├── quase-celestial/
├── ruptura-oculta/
└── instrumental-brain-rot/
audits/                   # auditorias, inclusive históricas
decisions/                # decisões arquiteturais curtas
research/                 # pesquisa transversal e fotografias históricas
ai/                       # somente memória contextual do agente
```

## Mapa origem → destino

| Origem | Destino | Justificativa | Risco / compatibilidade |
| --- | --- | --- | --- |
| `ai/fabrica/` | `factory/` | Dar nome semântico à implementação universal. | Atualizar imports, testes e comandos; referências históricas ficam documentadas. |
| `Canal Religioso/` | `operations/a-palavra-que-cuida/` | Agrupar a operação atual sob abstração neutra. | Atualizar scripts, manifests, documentação e ignores; renomear sem copiar mídia. |
| `Canal Religioso/canal.yaml` | `operations/a-palavra-que-cuida/manifest.yaml` | Instanciar contrato genérico de operação. | Atualizar referência local e preservar `channel_id` apenas nos contratos históricos compatíveis. |
| `00_incubadora/mukbang-ensaio-seco/` | `operations/mukbang-ensaio-seco/` | Casulo é lifecycle; o ensaio é uma operação candidata. | Converter manifesto candidato ao contrato de operação sem promover capacidades. |
| `Quase Celestial/` | `operations/quase-celestial/` | Remover operação especial da raiz. | Sem manifesto canônico atual; não inventar decisões. |
| `Ruptura Oculta/` | `operations/ruptura-oculta/` | Remover operação especial da raiz. | Sem manifesto canônico atual; não inventar decisões. |
| `Canal Instrumental Brain Rot/` | `operations/instrumental-brain-rot/` | Remover operação especial da raiz. | Estado ainda exploratório; não inventar superfícies. |
| `ai/auditorias/` | `audits/` | Separar vereditos da memória do agente. | Preservar menções históricas ao caminho antigo e registrar a migração. |
| `ai/preparacao-metamorfose.md` | `research/preparacao-metamorfose-2026-07-22.md` | Fotografia histórica, não implementação. | Atualizar apenas referências ativas. |

## Referências e imports afetados

- Imports `ai.fabrica.*` em testes passam a `factory.*`.
- Comandos `unittest discover ai\fabrica\tests` passam a `factory\tests`.
- `extends: ../../ai/fabrica` passa a apontar para `../../factory` a partir da operação.
- O teste do ensaio seco passa de `00_incubadora/...` para `operations/mukbang-ensaio-seco/...`.
- Scripts e manifests ativos com `Canal Religioso` passam a usar `operations/a-palavra-que-cuida`.
- Registros históricos podem manter caminhos antigos quando descrevem o que ocorreu; a tabela final distinguirá referência ativa de histórica.

## Implementação mínima planejada

1. Mover as áreas sem reestruturar internamente a produção.
2. Introduzir `OperationManifest` sem remover os contratos antigos; `ChannelManifest` permanece para compatibilidade v1.
3. Adicionar `Baseline` e um runtime pequeno de maturidade.
4. Modelar lifecycle geral e estados granulares de capacidades.
5. Marcar `longform_voice` como `regression_detected`, sem baseline e sem alterar TTS.
6. Comparar somente variáveis declaradas por uma baseline e restaurar o gate de revalidação quando houver mudança.
7. Definir execução limpa sem impor contagem arbitrária.
8. Testar operações com uma ou várias superfícies, sem YouTube, sem TikTok e sem vídeo horizontal.

## Itens deliberadamente adiados

- Reorganização interna das pastas numeradas da operação religiosa.
- Manifestos canônicos das outras operações sem decisões suficientes.
- Generalização completa de contratos históricos como `ContentBlueprint` e `MetricObservation`.
- Integrações novas, microserviços, banco de dados e módulos por plataforma.
- Implementação da skill de handoff GitHub.
- Correção ou investigação de voz, modelo, segmentação, prosódia ou Request Stitching.

## Resultado implementado

A estrutura proposta foi aplicada por renomeação no mesmo volume. Foram preservados 1.874 arquivos das cinco operações, totalizando 15.501.887.507 bytes, sem copiar mídia. A fábrica preservou 61 arquivos existentes e recebeu os contratos `OperationManifest`, `Baseline` e `CleanRun`, além do runtime de maturidade.

`A Palavra que Cuida` está em `stabilizing`. Nenhuma capacidade foi promovida artificialmente a `stable`; todas as referências de baseline são nulas. `longform_voice` está em `regression_detected`, com dívida de prosódia, causa ainda não provada e separação explícita entre QA técnico e aprovação semântica.

A detecção de invalidação compara apenas variáveis declaradas em `invalidation_triggers`. Mudança relevante produz `revalidation_required` e restaura o gate correspondente. A função não tenta julgar naturalidade humana.

## Referências antigas encontradas após a migração

| Referência | Tipo | Histórica ou ativa | Ação tomada |
| --- | --- | --- | --- |
| `ai/fabrica/` | caminho de implementação | histórica | Preservada na retrospectiva e na fotografia de 2026-07-22; ambas receberam nota de migração para `factory/`. Referências ativas e imports foram corrigidos. |
| `Canal Religioso/` | caminho de operação | histórica | Preservada apenas na retrospectiva e no plano de migração; a retrospectiva registra o destino `operations/a-palavra-que-cuida/`. Referências operacionais foram corrigidas. |
| `00_incubadora/` | caminho de incubação | histórica | Preservada somente neste mapa de origem; o ensaio passou a `operations/mukbang-ensaio-seco/`. |
| `canal.yaml` | manifesto local antigo | histórica | Registrada somente no mapa origem → destino; referências canônicas passaram a `manifest.yaml`. |
| `manifesto-candidato.yaml` | manifesto candidato antigo | ativa quebrada antes da correção | Referências em `run.json` e claims foram atualizadas para `manifest.yaml`. |
| `ai.fabrica.*` | import Python | ativa | Todos os imports passaram a `factory.*`; busca final não encontrou imports antigos. |

## Validação executada

- 47 testes da fábrica: aprovados.
- 14 schemas públicos: válidos.
- Dois manifests de operação: carregados e validados pelo CLI.
- Parse estático: 103 arquivos Python, 423 JSON, 6 JSONL e 14 YAML sem erro.
- Referências ativas aos caminhos antigos: nenhuma encontrada.
- Imports antigos: nenhum encontrado.
- Scan de segredos em arquivos versionáveis: nenhuma correspondência.
- Arquivos novos versionáveis acima de 1 MiB: nenhum.
- Mídia, PDF local, `tools/`, `.env` e arquivo local de chaves: confirmados como ignorados.
- Chamadas externas ou pagas: nenhuma.

## Falhas preexistentes preservadas

Dois dry-runs locais continuam falhando por divergências funcionais anteriores à migração:

1. `validate-video-003-preproduction.py` encontra artefatos de incidente e gate de voz com campos e estados que evoluíram além dos schemas v1 (`latest_evidence`, `latest_failure` e estados locais adicionais).
2. `validar-pacote-publicacao.py` inclui pelo glob arquivos `*-publicacao-v1.json` de formatos diferentes e encontra um pacote sem `video_id`.

Essas falhas não são quebras de caminho. Corrigi-las exigiria alterar contratos ou comportamento de produção/publicação e foi deliberadamente adiado para não misturar correção estrutural com correção funcional.
