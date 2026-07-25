# Fabrica de Canais e Videos

Estado: `v1-candidate`. A promocao para `v1` esta bloqueada pela auditoria dos
videos 001 a 003. O video 004 sera o primeiro teste operacional depois das
correcoes P0; uma execucao limpa valida a correcao imediata, mas nao elimina os
limiares de promocao dos gates.

Auditoria: `../auditorias/retrospectiva-fluxo-agentico-videos-001-003-v1.md`.

Este diretorio contem o nucleo universal das duas fabricas. Ele nao conhece o
publico, a duracao, a linguagem, os formatos ou as regras editoriais de nenhum
canal especifico.

## Duas fabricas

Fabrica de canais:

`entrada -> evidencias -> tese -> desenho_do_piloto -> instanciacao -> piloto -> publicacao_observacao -> cristalizacao`

Fabrica de videos:

`tema -> pesquisa -> blueprint -> artefato_performatico -> plano_producao_custo -> aquisicao -> composicao -> qa_pacote -> publicacao_distribuicao -> aprendizado`

Uma etapa que nao se aplica continua presente com estado `not_applicable` e
justificativa. O desaparecimento silencioso de uma etapa invalida a execucao.

## Organizacao

- `contracts/v1/`: schemas JSON dos contratos publicos.
- `core/`: runtime pequeno e deterministico da fabrica.
- `policies/`: defaults universais ainda versionados como `v0.x`.
- `skills/`: procedimentos carregados somente quando uma integracao exige.
- `tests/`: testes do nucleo e de isolamento entre canais.

Cada canal vive fora daqui, em seu proprio diretorio. O arquivo `canal.yaml`
instancia o nucleo e aponta para suas politicas locais. O OpenMontage recebe
planos aprovados e executa a composicao audiovisual; ele nao decide a tese do
canal nem a estrategia editorial.

O nucleo otimiza custo total para o resultado exigido; nao minimiza gasto bruto.
Preco direto, retrabalho provavel, operacao humana, processamento posterior,
confiabilidade, reutilizacao, aprendizado e retorno esperado entram na decisao.
Gasto maior exige ganho material ou reducao de risco; gasto menor nunca justifica
perder sentido, fidelidade, autenticidade, qualidade ou licenca.

## Uso local

O ambiente Python ja configurado no projeto e o do OpenMontage:

```powershell
tools\OpenMontage\.venv\Scripts\python.exe -m unittest discover ai\fabrica\tests
```
