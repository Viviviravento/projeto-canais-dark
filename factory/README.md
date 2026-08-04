# Fábrica universal de operações de conteúdo

Estado: `v1-candidate`. Esta pasta contém somente implementação reutilizável: contratos, runtime determinístico, políticas universais, gates, capacidades opcionais e testes.

Uma operação concreta vive em `../operations/` e declara em `manifest.yaml`:

- lifecycle operacional;
- superfícies e formatos como dados configuráveis;
- maturidade granular de capacidades;
- referências a baselines e políticas locais.

A fábrica não exige YouTube, TikTok, vídeo horizontal, vídeo longo ou múltiplas superfícies. Os tipos legados `channel` e `video` e o contrato `ChannelManifest` permanecem disponíveis para compatibilidade v1, mas novos pontos de entrada usam `operation`, `content` e `OperationManifest`.

## Maturidade

Lifecycle: `exploring`, `incubating`, `piloting`, `stabilizing`, `operational`, `paused` ou `retired`.

Capacidades: `not_exercised`, `investigating`, `exercised`, `validating`, `stable`, `regression_detected`, `blocked` ou `not_applicable`. Somente `stable` exige baseline aprovada; estados ainda não estabilizados não podem apontar para uma baseline como se ela existisse.

Uma baseline registra configuração aprovada, evidências, testes, gate, execuções limpas e variáveis que exigem revalidação. `factory.core.maturity.compare_baseline_configuration` compara apenas essas variáveis declaradas, e `enforce_baseline_assessment` restaura o gate quando necessário. Julgamento humano de naturalidade não é automatizado.

Uma execução só é limpa quando não contorna gates, não aceita regressão conhecida, não repete chamada paga por erro evitável, não diverge de baseline sem revalidação, preserva evidência e mantém o estado canônico fiel ao ocorrido. A fábrica não impõe uma contagem universal arbitrária de execuções limpas.

Pilotos existem para estabilizar capacidades e estabelecer evidências reproduzíveis. A saída da incubação depende dessa maturidade, não de um número fixo de vídeos.

## Organização

- `contracts/v1/`: contratos públicos e contratos legados compatíveis.
- `core/`: runtime pequeno e determinístico.
- `policies/`: defaults universais versionados.
- `skills/`: capacidades opcionais carregadas quando uma integração real exige.
- `tests/`: contratos, isolamento e governança de maturidade.

## Testes

```powershell
tools\OpenMontage\.venv\Scripts\python.exe -m unittest discover factory\tests
tools\OpenMontage\.venv\Scripts\python.exe -m factory.core.cli validate OperationManifest operations\a-palavra-que-cuida\manifest.yaml
```
