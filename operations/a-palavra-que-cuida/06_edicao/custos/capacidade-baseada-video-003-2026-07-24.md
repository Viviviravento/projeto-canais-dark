# Capacidade restante baseada no video 003

Data da verificacao: 24 de julho de 2026.

Este levantamento nao usa media entre os videos. A referencia e exclusivamente o video 003, apresentada de duas formas para nao misturar retrabalho com o custo reproduzivel da versao aprovada.

Conversao de referencia: PTAX de venda do Banco Central do Brasil de 23 de julho de 2026, ultima disponivel na consulta: **US$ 1 = R$ 5,0807**. A cobranca efetiva do cartao pode incluir IOF e spread.

## Saldos

| Provedor | Saldo atual | Equivalente em reais | Evidencia |
|---|---:|---:|---|
| ElevenLabs | 10.233 de 40.000 creditos, equivalentes a US$ 1,535 do plano | R$ 7,80 | Consultado pela API da assinatura |
| HeyGen | US$ 0,05 na carteira de API | R$ 0,25 | Consultado por `GET /v3/users/me` |
| fal.ai | US$ 5,80 esperados | R$ 29,47 | US$ 10,00 recarregados menos 10 clipes Kling registrados a US$ 0,42; a chave de producao nao pode consultar o endpoint administrativo de billing |

Valor economico restante somado: **US$ 7,385 / R$ 37,52**. Esses saldos nao sao intercambiaveis: dinheiro restante na fal.ai nao paga HeyGen ou ElevenLabs.

A ElevenLabs renova o periodo para 40.000 creditos em 10 de agosto de 2026, as 18:11:41 no horario de Brasilia, desde que a assinatura continue ativa.

## Quanto o video 003 consumiu

### Producao inteira, incluindo testes e versoes descartadas

| Provedor | Consumo do video 003 | Equivalente em reais |
|---|---:|---:|
| ElevenLabs | 11.309 creditos, equivalentes a US$ 1,696 do plano | R$ 8,62 |
| HeyGen | US$ 0,886 por 17,72 segundos de avatar | R$ 4,50 |
| fal.ai | US$ 0,84 por dois clipes Kling de cinco segundos | R$ 4,27 |
| **Total** | **US$ 3,422** | **R$ 17,39** |

Usando literalmente esse consumo completo outra vez, o saldo atual comporta:

- ElevenLabs: 0 videos completos; faltariam 1.076 creditos para repetir todo o retrabalho do video 003.
- HeyGen: 0 videos com um novo clipe de avatar equivalente.
- fal.ai: 6 videos com dois clipes Kling equivalentes.
- Esteira completa: 0 videos, limitada pelo HeyGen e pela ElevenLabs.

### Versao final estabilizada, sem repetir os testes

Esta conta usa somente os debitos observados dos artefatos finais do video 003. Nao e uma media:

| Componente final | Consumo observado por video | Equivalente em reais |
|---|---:|---:|
| Narracao completa aprovada | 4.414 creditos ElevenLabs, equivalentes a US$ 0,662 do plano | R$ 3,36 |
| Avatar de encerramento | US$ 0,886 HeyGen | R$ 4,50 |
| Movimento gerado | US$ 0,84 fal.ai | R$ 4,27 |
| **Total reproduzivel** | **US$ 2,388** | **R$ 12,13** |

Capacidade restante nesse molde:

- ElevenLabs: 2 narracoes completas, com 1.405 creditos restantes.
- fal.ai: 6 videos com dois clipes Kling, com saldo calculado de US$ 0,76 depois deles.
- HeyGen: 0 novos clipes equivalentes; faltariam US$ 0,836, cerca de R$ 4,25, para apenas um.
- Esteira completa com avatar novo: 0 videos.
- Sem nova geracao de avatar: 2 videos, limitados pela ElevenLabs. Cada um consome aproximadamente US$ 1,502 / R$ 7,63 dos saldos ja pagos, considerando narracao e dois clipes Kling.

## Correcao da auditoria anterior

A auditoria de 23 de julho contabilizou nove clipes fal.ai. A leitura integral dos arquivos `events.jsonl` encontrou dez geracoes Kling bem-sucedidas, todas a US$ 0,42. O consumo acumulado registrado e US$ 4,20, deixando saldo esperado de US$ 5,80 sobre a recarga documentada de US$ 10,00.

O saldo da fal.ai continua classificado como calculado, nao observado. Para transforma-lo em dado observado, e necessario consultar o painel autenticado ou criar deliberadamente uma chave administrativa com permissao de faturamento; nenhuma dessas acoes foi inferida ou executada.
