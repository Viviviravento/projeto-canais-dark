# Projeto Canais Dark

Este repositório desenvolve uma fábrica universal de operações de conteúdo. Uma operação concreta pode representar um canal, perfil, marca ou experimento e declara suas próprias superfícies, formatos, políticas e maturidade.

## Estrutura

- `factory/`: contratos, runtime, políticas universais, capacidades opcionais e testes.
- `operations/`: operações concretas; a atual é `operations/a-palavra-que-cuida/`.
- `audits/`: auditorias e evidências de vereditos.
- `decisions/`: decisões arquiteturais curtas.
- `research/`: pesquisa transversal e fotografias históricas de preparação.
- `ai/`: memória contextual mínima do agente.

O “casulo” não é uma pasta. É o regime de maturação descrito pelo lifecycle da operação, pelo estado granular de capacidades, por baselines reproduzíveis, gates de regressão e execuções limpas.

## Testes

Com o ambiente Python local já configurado:

```powershell
tools\OpenMontage\.venv\Scripts\python.exe -m unittest discover factory\tests
```

O OpenMontage permanece ferramenta externa em `tools/`. Credenciais, `.env`, mídia e estado local do editor não fazem parte da fábrica nem devem ser versionados.
