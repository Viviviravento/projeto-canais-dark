# Camada `ai/`

Este diretório é a memória mínima da metamorfose do projeto.

Ele não é uma estrutura final de agente, nem uma coleção de workflows prontos. O agente deve nascer no chat, a partir de conversa, decisões, testes e correções. Só depois algo vira instrução persistente.

## Arquivo principal

- `memoria.md`: ideias, decisões, limites e perguntas que precisam sobreviver entre contextos.
- `memoria.md` preserva os caminhos e decisões conhecidos no momento em que foram registrados; eles são evidência histórica, não um mapa de diretórios ativo.

## Regra

Adicionar arquivo novo em `ai/` só quando houver necessidade real e recorrente. Por padrão, atualizar `memoria.md`.

## O que fica fora

Implementação reutilizável fica em `../factory/`; maturidade e experimentos ficam
em `../research/`; auditorias ficam em `../audits/`; decisões versionáveis ficam
em `../decisions/`; materiais de produção vivem em uma operação concreta sob
`../operations/`.
