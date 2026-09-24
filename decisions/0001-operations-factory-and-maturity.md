# Decisão 0001 — operações, fábrica e maturidade

Status: aceita para a candidata estrutural
Data: 2026-08-04

## Problema e contexto

O repositório mistura memória do agente, implementação universal, auditorias e operações concretas. A raiz cresce com pastas especiais por canal, enquanto “casulo” aparece como categoria espacial apesar de representar maturação.

## Decisão

- `factory/` contém a implementação reutilizável.
- `operations/` agrupa unidades concretas de trabalho. Uma operação pode ser canal, perfil, marca ou experimento; o núcleo não precisa saber qual desses rótulos ela usa.
- Plataformas (`surfaces`) e formatos são propriedades declaradas pela operação, não etapas obrigatórias da fábrica.
- `ai/` fica restrito à memória contextual do agente; auditorias e pesquisa histórica recebem áreas semânticas próprias.
- “Casulo” é regime de maturação, não pasta. Ele é representado por lifecycle da operação, maturidade granular de capacidades, baselines, gates de regressão e execuções limpas.
- Uma regressão afeta a capacidade correspondente e restaura seu gate; não reinicia automaticamente toda a operação.
- Baselines são aprovações reproduzíveis sustentadas por evidência. Mudanças em variáveis explicitamente declaradas invalidam a reutilização silenciosa da aprovação.
- A abertura futura ocorre por composição e configuração. A fábrica não modelará antecipadamente todas as plataformas, durações, formatos ou combinações possíveis.

## Alternativas rejeitadas

- Manter operações concretas na raiz: não escala e perpetua exceções.
- Usar `channels/`: estreito demais para perfis, marcas e experimentos.
- Usar `workspaces/`: confunde operação de conteúdo com o workspace local e ferramentas.
- Usar `projects/`: amplo demais dentro de um repositório que já é um projeto.
- Remover completamente `ai/`: descartaria uma função contextual explícita definida pelo projeto.
- Criar módulos por plataforma ou tipo de mídia: antecipa variações ainda não exigidas.

## Consequências e limites

Os caminhos ativos mudam e precisam de validação. Contratos v1 com terminologia de canal permanecem compatíveis enquanto novos pontos de entrada usam `OperationManifest`. Não serão fabricadas baselines para capacidades não estabilizadas. As estruturas internas das operações existentes permanecem como estão nesta etapa.

## Adiado

Generalização de todos os contratos históricos, manifestos das operações sem decisões suficientes, reorganização interna de produção, handoff GitHub automatizado e qualquer correção funcional de integração audiovisual.
