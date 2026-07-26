# Auditoria de estrutura — 2026-07-26

## Escopo e evidência

Esta auditoria trata apenas da organização do repositório. Não executa
integrações, não gera mídia, não consulta serviços pagos e não altera decisões
de produção. A base auditada é o commit `06d590e`; alterações de produção que
existiam na worktree principal ficaram fora desta branch em uma worktree
isolada.

## Diagnóstico

| Origem | Classificação | Situação | Destino ou tratamento |
| --- | --- | --- | --- |
| `ai/memoria.md` | memória de agente | ativo | permanece em `ai/` |
| `ai/README.md` | instrução de agente | ativo | permanece em `ai/` e passa a apontar para os locais neutros |
| `ai/preparacao-metamorfose.md` | estado de maturidade | ativo, mas fora do papel de `ai/` | `research/maturation-state.md` |
| `ai/auditorias/` | auditoria/retrospectiva | evidência histórica | `audits/retrospectives/` sem reescrever seus fatos |
| `ai/fabrica/` | implementação universal | ativo, mas no domínio errado | `factory/` |
| `00_incubadora/mukbang-ensaio-seco/` | experimento de pesquisa | ativo | `research/experiments/mukbang-ensaio-seco/` |
| `00_incubadora/README.md` | instrução de pesquisa | ativo | `research/experiments/README.md` |
| `Canal Religioso/` | operação concreta | ativo | `operations/a-palavra-que-cuida/` |
| `Canal Religioso/canal.yaml` | configuração de operação | ativo e específica | `operations/a-palavra-que-cuida/operation.yaml` |
| `Canal Religioso/scripts/*.py` | implementação operacional | ativo | mantém-se na operação, com raiz calculada pelo caminho novo |
| artefatos em `01_briefs` a `09_metricas` | produção e evidência de produção | histórico/ativo | movidos intactos com a operação |
| caminhos dentro de artefatos gerados e retrospectivas | registro histórico | histórico | não são reescritos em massa; a migração é documentada aqui |
| `tools/` | ferramenta externa local | externo/ignorado | permanece fora da arquitetura de domínio |

## Referências encontradas

As referências foram separadas entre:

- **ativas:** README raiz, `agents.md`, `ai/README.md`, README da fábrica,
  testes da fábrica, manifesto e scripts de produção;
- **históricas:** memória, auditorias, relatórios, manifests de assets e
  caminhos serializados de produções anteriores;
- **geradas:** mídia, áudio, exports e prévias ignorados pelo Git;
- **instruções de agente:** `agents.md`, `ai/README.md` e `ai/memoria.md`.

As referências históricas não serão alteradas para simular que o passado usou a
estrutura nova. O guia de migração no README raiz é a compatibilidade humana
para esses caminhos.

## Acoplamentos que exigem migração mínima

1. A fábrica usa o namespace `ai.fabrica` em testes e scripts.
2. O fluxo nomeia os dois tipos de execução como `channel` e `video`, embora a
   implementação tenha valor para operações e conteúdos além de canais.
3. Seis scripts de áudio/validação calculam `PROJECT_ROOT / "Canal Religioso"`.
4. O `.gitignore` usa o caminho antigo para mídia gerada.
5. O manifesto da operação é um `ChannelManifest` específico e não expressa
   capacidades, baseline ou regressão.

## Critério de aceitação da migração

- A fábrica não precisa de uma plataforma, formato, tema religioso ou perfil
  concreto para importar, validar contratos ou abrir uma execução.
- A operação mantém seus arquivos internos e seus scripts resolvem o novo
  caminho sem mudar a lógica de ElevenLabs ou chamar serviços externos.
- O manifesto de operação declara ciclo de vida e capacidades separadas.
- Nenhuma capacidade é declarada estável sem baseline verificável.
- Testes locais cobrem manifesto genérico, incompatibilidade de baseline e
  inexistência de exigência de plataforma/formato no núcleo.
