# Pesquisa v0 - Direcao de narracao com ElevenLabs

Data da pesquisa: 2026-07-12.

## Pergunta

Como controlar pausas, continuidade, contexto, pronuncia e interpretacao no ElevenLabs sem enviar um roteiro inteiro e torcer para a leitura funcionar?

## Conclusao

A documentacao sustenta abandonar a geracao monolitica sem direcao: para textos longos, recomenda segmentacao e contexto entre requisicoes. Ela tambem oferece recursos para regeneracao localizada, mas nao determina como deve funcionar nosso crivo humano.

Combinando essa evidencia com o requisito de escala definido pelo usuario, a proposta operacional e gerar grandes blocos semanticos com contexto entre eles, montar o episodio e submeter ao humano apenas para aprovacao ou rejeicao. Evitar remendos frase a frase e uma decisao de processo do projeto, nao uma regra da ElevenLabs.

O texto deve ser convertido num roteiro de performance dividido por movimentos completos do argumento. Cada bloco pode receber pausas explicitas e ser gerado com contexto anterior e posterior. Quando houver falha, o padrao deve ser regenerar o bloco completo ou revisar o metodo para o conjunto, nao pedir ao humano que localize e remende frases.

Migrar tudo para `Eleven v3` nao e a resposta automatica. V3 oferece mais expressividade e tags de atuacao, mas nao aceita SSML `<break>` nem Request Stitching. A propria ElevenLabs ainda descreve v3 como mais variavel e informa que Professional Voice Clones nao estao totalmente otimizados para ele.

Tambem nao ha base para tratar a voz Bruno Cardoso como definida apenas porque funcionou em um microteste. A ElevenLabs declara que a escolha da voz e o fator de maior impacto, seguida pelo modelo e so depois pelas configuracoes. A ficha verificada do Bruno o descreve para `social media`, compartilhamento de fatos e entrega `confident`; o piloto revelou uma atuacao pouco interpretativa em texto pastoral longo. Isso torna o desalinhamento entre voz-fonte e uso desejado uma hipotese forte que precisa de comparacao, nao uma conclusao definitiva.

## O que a documentacao confirma

### Multilingual v2

- E apresentado pela ElevenLabs como o modelo mais estavel para narracao longa.
- Aceita texto de ate 10.000 caracteres por chamada de API.
- Pausas podem ser marcadas com `<break time="x.xs" />`, ate 3 segundos.
- Excesso de tags `<break>` pode causar instabilidade, aceleracao ou artefatos.
- O endpoint normal e o endpoint com timestamps aceitam `previous_text`, `next_text`, `previous_request_ids` e `next_request_ids`.
- Request Stitching existe para preservar prosodia entre chamadas e permite corrigir um bloco usando os IDs dos blocos vizinhos como contexto.
- `seed` oferece uma tentativa de repetibilidade, mas nao garante determinismo.
- `style` diferente de zero pode tornar a geracao menos estavel; a recomendacao oficial e mante-lo em zero quando aparecem inconsistencias.
- Dicionarios de pronuncia podem aplicar aliases ao Multilingual v2. Eles corrigem palavras, nomes e siglas; nao resolvem prosodia de frases.
- A documentacao recomenda dividir textos longos em segmentos e usar texto anterior/posterior ou IDs de requisicoes para manter o fluxo prosodico.
- A ElevenLabs alerta que trocas de idioma ou sotaque podem surgir em geracoes longas e que o problema depende da combinacao entre voz e texto.

### Eleven v3

- Aceita tags de atuacao e emocao, como `[whispers]`, `[sighs]` e direcoes semelhantes.
- Pontuacao, elipses, capitalizacao e estrutura textual influenciam fortemente a entrega.
- Nao aceita SSML `<break>`.
- Nao oferece Request Stitching.
- Stability em modo Creative amplia expressividade e risco de alucinacoes; Natural busca equilibrio; Robust aumenta consistencia e reduz resposta a direcao.
- A voz escolhida precisa ter material de origem compativel com a interpretacao desejada; tags nao transformam completamente o comportamento de uma voz.

### Studio

- Permite ajustar voz e configuracoes por paragrafo ou selecao.
- Permite inserir pausas e trabalhar por unidades pequenas.
- Permite regenerar paragrafo, frase ou selecao; a ElevenLabs recomenda regenerar pelo menos uma frase completa em vez de uma palavra isolada.
- Quando texto e voz nao mudam, existem ate duas regeneracoes gratuitas da selecao no Studio.
- Studio 3.0 possui Actor Mode: uma gravacao humana pode dirigir a interpretacao da voz.
- E mais controlavel para crivo humano, mas envolve interface e operacao manual; a API segmentada e mais automatizavel.
- A regeneracao automatica em exportacoes completas verifica problemas como volume, similaridade da voz, artefatos e pronuncia. A documentacao nao afirma que ela avalie compreensao do argumento ou coerencia interpretativa; portanto, nao substitui o crivo humano de atuacao.
- Actor Mode exige uma atuacao-guia humana. Pode servir para diagnostico ou excecao, mas contraria o objetivo de baixa operacao humana se virar etapa padrao de cada episodio.

## Metodo escalavel proposto para testar depois

Este metodo ainda e proposta, nao decisao cristalizada.

1. Manter dois textos: roteiro editorial e roteiro de performance.
2. Criar um contrato de atuacao unico para o episodio: relacao com o ouvinte, intensidade, ritmo, hierarquia das ideias, tratamento das citacoes e forma de concluir argumentos.
3. Fazer uma calibracao barata com tres blocos representativos: abertura, desenvolvimento explicativo denso e fechamento com CTA.
4. Comparar nesses blocos pelo menos a voz atual e uma voz nativa pt-BR cuja ficha e amostra sejam voltadas a narracao longa, audiobook, storytelling ou entrega meditativa. Comparar voz antes de multiplicar ajustes finos de estabilidade.
5. O humano escolhe a combinacao voz + modelo + contrato de atuacao. Ele nao marca frases defeituosas.
6. Dividir o episodio em grandes movimentos semanticos, nao em cada frase ou paragrafo. A quantidade e o tamanho precisam ser calibrados pelo piloto; a ElevenLabs nao publica um tamanho semantico ideal universal.
7. Marcar somente pausas necessarias no Multilingual v2. As faixas abaixo sao hipoteses de calibracao nossas, nao recomendacoes numericas oficiais:
   - pausa curta entre oracoes: cerca de 0,3 a 0,5 segundo;
   - conclusao de ideia: cerca de 0,7 a 1 segundo;
   - mudanca de bloco: cerca de 1,1 a 1,5 segundo.
8. Enviar contexto anterior e posterior e usar Request Stitching no Multilingual v2.
9. Usar `seed` fixo durante comparacoes, sem tratar a saida como deterministica, e manter `style=0` enquanto houver instabilidade.
10. Gerar todos os grandes blocos, montar o audio automaticamente e aplicar verificacoes automaticas de integridade textual, duracao, volume, silencios e palavras ausentes/adicionais.
11. O humano ouve a montagem e responde somente `aprovado` ou `reprovado`, podendo rejeitar um grande bloco sem anotar cada defeito.
12. Se a falha for localizada na atuacao de um movimento completo, regenerar esse bloco. Se o mesmo padrao aparecer em varios blocos, revisar voz/modelo/contrato e regenerar o conjunto.
13. Frase isolada e Actor Mode ficam como excecoes de resgate, nao como fluxo normal da fabrica.

## Limite da automacao

Transcricao, alinhamento, volume, duracao e pausas podem ser verificados automaticamente. Nao foi encontrada evidencia de que ElevenLabs ou nossas ferramentas consigam julgar de forma confiavel se a voz "entendeu" a progressao do argumento pastoral. Esse criterio exige crivo humano na calibracao e na aprovacao final, mas nao exige anotacao manual de defeitos.

## Estrutura futura do encerramento

O encerramento deve ser uma unidade de performance propria, separada do ultimo paragrafo da reflexao:

1. Concluir a mensagem sem CTA.
2. Pausa perceptivel.
3. Mencionar `A Palavra que Cuida`.
4. Convidar a pessoa a se inscrever e curtir.
5. Pedir compartilhamento para que a mensagem alcance outra pessoa que possa precisar dela.
6. Encerrar com assinatura breve, sem adicionar uma nova reflexao.

O texto exato do CTA ainda precisa ser escrito e aprovado. Nao inserir automaticamente uma formula generica em todos os formatos.

## Fontes oficiais

- Best practices de TTS: https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices
- Guia de TTS e prioridade entre voz, modelo e configuracoes: https://elevenlabs.io/docs/eleven-creative/playground/text-to-speech
- Prompting Eleven v3: https://elevenlabs.io/docs/best-practices/prompting
- Modelos e envelopes: https://elevenlabs.io/docs/overview/models
- API Create speech: https://elevenlabs.io/docs/api-reference/text-to-speech/convert
- API Create speech with timing: https://elevenlabs.io/docs/api-reference/text-to-speech/convert-with-timestamps
- Request Stitching: https://elevenlabs.io/docs/eleven-api/guides/how-to/text-to-speech/request-stitching
- ElevenCreative Studio: https://elevenlabs.io/docs/eleven-creative/products/studio
- Auto-Regenerate no Studio: https://help.elevenlabs.io/hc/en-us/articles/30204568681745-What-is-Auto-Regenerate
- Voiceover Studio: https://elevenlabs.io/docs/voiceover-studio/overview
- Pronunciation dictionaries: https://elevenlabs.io/docs/api-reference/pronunciation-dictionaries/create-from-rules
- Troubleshooting: https://elevenlabs.io/docs/resources
