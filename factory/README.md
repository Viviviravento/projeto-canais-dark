# Fábrica de operações e conteúdo

Estado: `v1-candidate`. A promocao para `v1` esta bloqueada pela auditoria dos
videos 001 a 003. O video 004 sera o primeiro teste operacional depois das
correcoes P0; uma execucao limpa valida a correcao imediata, mas nao elimina os
limiares de promocao dos gates.

Auditoria: `../audits/retrospectives/retrospectiva-fluxo-agentico-videos-001-003-v1.md`.

Este diretorio contem o nucleo universal das duas fabricas. Ele nao conhece o
publico, a duracao, a linguagem, os formatos ou as regras editoriais de nenhum
canal especifico.

## Duas fabricas

Fábrica de operações:

`entrada -> evidencias -> tese -> desenho_do_piloto -> instanciacao -> piloto -> publicacao_observacao -> cristalizacao`

Fábrica de conteúdo:

`tema -> pesquisa -> blueprint -> artefato_performatico -> plano_producao_custo -> aquisicao -> composicao -> qa_pacote -> publicacao_distribuicao -> aprendizado`

Uma etapa que nao se aplica continua presente com estado `not_applicable` e
justificativa. O desaparecimento silencioso de uma etapa invalida a execucao.

## Organizacao

- `contracts/v1/`: schemas JSON dos contratos publicos.
- `core/`: runtime pequeno e deterministico da fabrica.
- `policies/`: defaults universais ainda versionados como `v0.x`.
- `skills/`: procedimentos carregados somente quando uma integracao exige.
- `tests/`: testes do núcleo, maturidade e isolamento entre operações.

Cada operação vive fora daqui, em seu próprio diretório. O arquivo
`operation.yaml` instancia o núcleo, declara ciclo de vida e capacidades locais
e aponta para políticas da operação. `ChannelManifest` continua como contrato
legado; novos manifestos usam `OperationManifest`. O OpenMontage recebe planos
aprovados e executa a composição audiovisual; ele não decide tese nem estratégia
editorial.

O nucleo otimiza custo total para o resultado exigido; nao minimiza gasto bruto.
Preco direto, retrabalho provavel, operacao humana, processamento posterior,
confiabilidade, reutilizacao, aprendizado e retorno esperado entram na decisao.
Gasto maior exige ganho material ou reducao de risco; gasto menor nunca justifica
perder sentido, fidelidade, autenticidade, qualidade ou licenca.

## Uso local

Use o ambiente local do OpenMontage, que contém `jsonschema`:

```powershell
tools\OpenMontage\.venv\Scripts\python.exe -m unittest discover factory\tests
```
