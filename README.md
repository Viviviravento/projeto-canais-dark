# Projeto Canais Dark

Este repositório registra o desenvolvimento de uma fábrica de canais dark e de
vídeos. O primeiro campo de prova é o canal religioso `A Palavra que Cuida`.

## Estrutura

- `ai/`: memória do projeto e núcleo candidato da fábrica, com contratos,
  políticas e testes em Python.
- `Canal Religioso/`: briefs, roteiros, evidências e materiais textuais de
  produção do primeiro canal.
- `00_incubadora/`: experimentos e evidências de hipóteses de novos canais.

## Tecnologias identificadas

O projeto contém Python, PowerShell, JSON Schema, YAML e Markdown. A composição
audiovisual local utiliza OpenMontage, mantido fora deste repositório por ser uma
ferramenta externa com dependências, ambientes locais e artefatos de trabalho.

## Testes conhecidos

Com o ambiente local do OpenMontage configurado, o núcleo da fábrica pode ser
testado com:

```powershell
tools\OpenMontage\.venv\Scripts\python.exe -m unittest discover ai\fabrica\tests
```

## Configuração local

Credenciais e arquivos `.env` permanecem exclusivamente na máquina local e não
devem ser adicionados ao repositório.
