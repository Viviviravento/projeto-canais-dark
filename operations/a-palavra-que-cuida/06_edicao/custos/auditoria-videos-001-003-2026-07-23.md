# Auditoria de custos: vídeos 001 a 003

Data da auditoria: 23 de julho de 2026.

## Resposta curta

- Valor econômico consumido nas três produções: **US$ 13,22**.
- Média histórica, incluindo testes e versões descartadas: **US$ 4,41 por vídeo concluído**.
- Custo esperado do método já estabilizado no vídeo 003, sem refação: **US$ 2,39 por vídeo**.
- Capacidade atual sem comprar ou renovar créditos: **zero vídeos completos no formato atual**, porque o HeyGen tem apenas **US$ 0,05**.
- Sem gerar avatar novo, ainda há capacidade para aproximadamente **dois vídeos**, limitada pelo ElevenLabs.

O valor econômico consumido não é igual ao dinheiro carregado nas contas. Uma recarga continua sendo saldo até ser usada.

## Dinheiro colocado nas contas

- ElevenLabs Starter: **US$ 6,00** no período mensal atual.
- fal.ai: **US$ 10,00** de recarga pré-paga.
- HeyGen: o extrato acessível informa o saldo, mas não informa quanto foi carregado originalmente.

Portanto, o desembolso documentado é de **pelo menos US$ 16,00**, mais qualquer valor colocado no HeyGen. Não é correto somar os US$ 10,00 inteiros do fal.ai como gasto de produção, porque aproximadamente US$ 6,22 ainda permanecem como saldo.

## Uso por vídeo

| Produção | ElevenLabs | HeyGen | fal.ai | Total econômico |
|---|---:|---:|---:|---:|
| Piloto 001 | 10.280 créditos = US$ 1,54 | 47,069 s = US$ 2,35 | 4 clips = US$ 1,68 | **US$ 5,58** |
| Vídeo 002 | 8.178 créditos = US$ 1,23 | 38,220 s = US$ 1,91 | 3 clips = US$ 1,26 | **US$ 4,40** |
| Vídeo 003 | 10.129 créditos = US$ 1,52 | 17,720 s = US$ 0,89 | 2 clips = US$ 0,84 | **US$ 3,25** |
| **Total** | **28.587 = US$ 4,29** | **103,009 s = US$ 5,15** | **9 clips = US$ 3,78** | **US$ 13,22** |

O piloto 001 absorve os dois microtestes iniciais do avatar e os testes de escolha/calibração de voz. O vídeo 003 inclui o áudio v1 descartado, calibrações e o áudio v2 aprovado.

## Refação do áudio

Dos 28.587 créditos usados no ElevenLabs:

- 11.347 créditos viraram as três narrações finais;
- 17.240 créditos foram consumidos por testes, calibrações e versões descartadas;
- portanto, aproximadamente 60,3% do consumo de voz até agora foi aprendizado/refação.

Esse número não deve ser projetado como custo normal futuro. O áudio final do vídeo 003 consumiu 4.414 créditos, que é a base conservadora para o próximo episódio.

## Saldos atuais

### ElevenLabs

- Plano: Starter.
- Limite: 40.000 créditos.
- Usado: 28.587.
- Restante: **11.413 créditos**.
- Próxima renovação observada: **10 de agosto de 2026, 18:11 BRT**.
- Próxima fatura informada pela conta: **US$ 6,00**.

Capacidade conservadora: `11.413 / 4.414 = 2` narrações completas sem refação.

### HeyGen

- Carteira observada pela API: **US$ 0,05**.
- Oito vídeos concluídos na conta: 103,009 segundos no total.
- Valor de tabela do material concluído: aproximadamente **US$ 5,15**.

O endpoint antigo também mostra cotas promocionais separadas. Elas não foram contadas como saldo utilizável porque a última geração Avatar IV, feita pela API v3, reduziu a carteira e não reduziu essas cotas.

Capacidade no formato atual: **zero**, pois o último avatar de 17,72 segundos custa aproximadamente US$ 0,89.

### fal.ai

- Recarga informada pelo usuário: US$ 10,00.
- Nove saídas Kling bem-sucedidas registradas: `9 x US$ 0,42 = US$ 3,78`.
- Saldo esperado: **US$ 6,22**.

Esse saldo é uma reconstrução, não uma leitura direta. A chave atual é de produção e recebeu HTTP 403 no endpoint financeiro, que exige chave administrativa. Se o painel mostrar outro valor, a diferença representa débito duplicado ou uso não registrado e deve ser investigada.

Capacidade esperada: `US$ 6,22 / US$ 0,84 = 7` vídeos usando dois clips Kling de cinco segundos cada.

## Próximo vídeo

Baseando-se somente na versão aprovada do vídeo 003, sem repetir geração:

| Componente | Uso por vídeo | Valor econômico |
|---|---:|---:|
| ElevenLabs | 4.414 créditos | US$ 0,66 do plano |
| HeyGen | 17,72 segundos | US$ 0,89 |
| fal.ai | 2 clips de 5 segundos | US$ 0,84 |
| **Total esperado** |  | **US$ 2,39** |

Hoje, os serviços comportam:

- ElevenLabs: 2 vídeos;
- fal.ai: aproximadamente 7 vídeos;
- HeyGen: 0 vídeos;
- cadeia completa: **0 vídeos**, pois vale o menor número da cadeia.

Sem gerar avatar novo, é possível produzir cerca de **dois vídeos** com narração, imagens geradas/stock e até dois clips Kling por episódio. Isso seria uma variante econômica, não o formato-padrão aprovado.

## Itens sem preço atribuído

- geração de imagens pelo Codex;
- trabalho humano;
- eletricidade e processamento local;
- FFmpeg, Remotion e OpenMontage;
- Pexels, Pixabay e materiais stock gratuitos usados sob suas licenças.

Não atribuir zero às imagens do Codex como se fossem comprovadamente gratuitas: o ambiente não fornece um extrato financeiro por imagem.

## Fontes externas verificadas

- ElevenLabs: `GET /v1/user/subscription` para plano, cota, uso, renovação e próxima fatura.
- HeyGen: `GET /v3/users/me` para carteira e `GET /v3/videos` para a lista completa de saídas.
- fal.ai: página oficial do Kling O3 Standard, com US$ 0,084 por segundo sem áudio, e regra oficial de cobrança por saída bem-sucedida.

Os dados brutos da consulta estão em `provider-balances-2026-07-23.json`. A versão estruturada desta auditoria está em `auditoria-videos-001-003-2026-07-23.json`.
