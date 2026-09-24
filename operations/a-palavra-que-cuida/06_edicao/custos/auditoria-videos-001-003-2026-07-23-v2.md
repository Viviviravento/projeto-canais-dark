# Auditoria de custos dos videos 001 a 003 - v2

Data: 23 de julho de 2026.

Esta versao incorpora o teste comparativo mais recente da cauda do video 003 e converte os valores para reais pela PTAX de venda do Banco Central do Brasil de 23/07/2026: **R$ 5,0807 por US$ 1**.

## Consumo economico

| Producao | ElevenLabs | HeyGen | fal.ai | Total USD | Total BRL |
|---|---:|---:|---:|---:|---:|
| Piloto 001 | US$ 1,542 | US$ 2,353 | US$ 1,680 | **US$ 5,575** | **R$ 28,33** |
| Video 002 | US$ 1,227 | US$ 1,911 | US$ 1,260 | **US$ 4,398** | **R$ 22,34** |
| Video 003 | US$ 1,696 | US$ 0,886 | US$ 0,840 | **US$ 3,422** | **R$ 17,39** |
| **Total** | **US$ 4,465** | **US$ 5,150** | **US$ 3,780** | **US$ 13,395** | **R$ 68,06** |

O teste mais recente da cauda do video 003 consumiu 1.180 creditos ElevenLabs, equivalentes a aproximadamente **US$ 0,177 / R$ 0,90** dentro do plano Starter.

## Dinheiro colocado

O desembolso documentado e de pelo menos **US$ 16,00 / R$ 81,29**:

- ElevenLabs Starter: US$ 6,00.
- Recarga fal.ai: US$ 10,00.
- HeyGen: o valor originalmente colocado nao aparece no endpoint da conta nem nos registros locais. Por isso, o desembolso total real e maior que o piso acima.

Dinheiro colocado e consumo economico nao sao a mesma coisa. Saldo pre-pago ainda nao consumido continua sendo ativo da producao.

## Saldos atuais

- ElevenLabs: 10.233 de 40.000 creditos, equivalentes a cerca de **US$ 1,535 / R$ 7,80** do plano atual.
- HeyGen: **US$ 0,05 / R$ 0,25** na carteira.
- fal.ai: saldo esperado de **US$ 6,22 / R$ 31,60**. O saldo e calculado, nao observado, porque a chave de producao recebe HTTP 403 no endpoint administrativo de billing.

## Quantos videos ainda cabem

No molde estabilizado do video 003:

- ElevenLabs sustenta **2 narracoes** de aproximadamente 10 a 12 minutos.
- fal.ai sustenta aproximadamente **7 videos** com dois clipes Kling de cinco segundos.
- HeyGen sustenta **0 novos videos com avatar**, porque US$ 0,05 nao cobre os cerca de 17,72 segundos usados no video 003.

Conclusao: sem recarga, cabem **2 novos videos sem gerar avatar novo**. Para repetir integralmente o molde atual com avatar, cabem **0**, e o gargalo e o HeyGen.

## Limites

Nao estao precificados: geracao de imagens pelo Codex, trabalho humano, energia eletrica e computacao local. A conversao em reais e uma referencia; cobranca de cartao pode incluir IOF e spread.
