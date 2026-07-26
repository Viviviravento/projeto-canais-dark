# Projeto Canais Dark

Este repositório registra o desenvolvimento de uma fábrica de canais dark e de
vídeos. O primeiro campo de prova é o canal religioso `A Palavra que Cuida`.

## Estrutura

- `ai/`: memória e orientação mínima do agente; não contém implementação.
- `factory/`: implementação reutilizável, contratos, políticas, skills e testes.
- `operations/a-palavra-que-cuida/`: primeira operação concreta, com seus
  briefs, roteiros, evidências e materiais de produção.
- `research/`: estado de maturidade e experimentos que ainda não são operações.
- `audits/`: auditorias e retrospectivas preservadas como evidência.
- `decisions/`: decisões arquiteturais que sobreviveram à conversa.

O regime de “casulo” é de maturidade, não uma pasta. A estrutura e o critério de
promoção por capacidade estão em `decisions/ADR-001-repository-structure-and-maturity.md`.

## Tecnologias identificadas

O projeto contém Python, PowerShell, JSON Schema, YAML e Markdown. A composição
audiovisual local utiliza OpenMontage, mantido fora deste repositório por ser uma
ferramenta externa com dependências, ambientes locais e artefatos de trabalho.

## Testes conhecidos

Com o ambiente local do OpenMontage configurado, o núcleo da fábrica pode ser
testado com:

```powershell
tools\OpenMontage\.venv\Scripts\python.exe -m unittest discover factory\tests
```

## Configuração local

Credenciais e arquivos `.env` permanecem exclusivamente na máquina local e não
devem ser adicionados ao repositório.
