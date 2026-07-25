# Pesquisa pratica v1 - Prosodia e interpretacao em TTS

Data: 2026-07-22.

## Pergunta operacional

Como criadores estao resolvendo narracoes que soam como leitura escolar: pausas dentro de ideias, finais de frase errados, enfase sem relacao com o sentido e pouca compreensao aparente do texto?

Esta pesquisa substitui a confianca excessiva depositada em `pesquisa-direcao-voz-elevenlabs-v0.md`. A documentacao continua util para saber o que uma API aceita, mas nao prova que o resultado funciona em producao.

## Sintoma observado no video 003

- A narracao integral com Bruno Cardoso, Multilingual v2 e Request Stitching foi reprovada.
- A nova partitura oral, dividida em tres amostras representativas, tambem foi reprovada.
- O defeito principal nao e apenas duracao de silencio. E cadencia dentro da frase, foco prosodico e fechamento semantico.
- Portanto, inserir silencio no editor pode corrigir intervalos, mas nao faz a voz compreender qual ideia esta sendo concluida.

## Auditoria local do input e do payload

A pesquisa externa encontrou defeitos da mesma classe, mas ela nao diagnostica sozinha o nosso caso. A auditoria do que realmente entrou na API mostrou:

- `performance_contract` e demais instrucoes narrativas do manifesto nao foram enviados ao ElevenLabs. O endpoint recebeu apenas `text`, `model_id`, `language_code`, `voice_settings`, `seed` e, quando presentes, contexto textual anterior/posterior.
- A calibracao v2 nao usou Request Stitching. Cada amostra foi independente e recebeu, no maximo, uma frase curta e semanticamente coerente em `previous_text` e `next_text`.
- Nao foram encontrados caracteres de substituicao, controles invisiveis, espacos especiais ou outro lixo Unicode nos manifestos dos videos 002 e 003.
- Bruno Cardoso, Multilingual v2, `language_code=pt`, seed `271828` e os mesmos ajustes produziram o audio aprovado do video 002. Logo, essa combinacao nao pode ser declarada incapaz com base na calibracao atual.
- A partitura v2 introduziu uma diferenca forte: 8 de 31 frases, ou 25,8%, possuem ate quatro palavras. No audio aprovado do video 002, sao 9 de 107, ou 8,4%. A taxa de microfrases ficou aproximadamente tres vezes maior.
- As pausas fisicas medidas pelos alinhamentos nao ficaram maiores: media de 0,531 segundo depois de final de frase na calibracao v2, contra 0,547 segundo no video 002 aprovado. Os intervalos entre palavras sem pontuacao tambem ficaram proximos, 0,088 contra 0,094 segundo.

Conclusao local: o efeito descrito como `Ele... fala... assim...` nao aparece principalmente como silencio adicional. Ele e percebido como reinicio de contorno melodico, foco e fraseado. Na calibracao mais recente, a causa mais sustentada e a nossa supersegmentacao do texto, uma correcao excessiva feita para tentar dirigir a voz pela pontuacao.

`Overprompting` foi descartado para a calibracao v2 porque nenhum prompt de atuacao foi enviado. `Rotten context` tambem foi descartado para essa calibracao: nao havia cadeia de geracoes anteriores nem contexto longo. Na narracao integral v1, Request Stitching condicionou cada bloco aos anteriores e pode ter preservado uma cadencia ruim iniciada no primeiro bloco; isso continua como hipotese, pois o video 002 aprovado usou o mesmo mecanismo.

## Evidencia externa que explica o sintoma

Um experimento perceptivo apresentado no Speech Prosody 2026 comparou fala humana e varios TTS. No teste em ingles, ouvintes reconheceram o foco pretendido em apenas 29,92% das amostras do ElevenLabs, quase ao acaso. Os autores o colocaram na zona `natural but confusing`: fala suave, mas com pouco contraste para marcar a informacao importante. O estudo nao testa portugues brasileiro nem a voz Bruno; ele sustenta o mecanismo do defeito, nao uma generalizacao direta para todo uso.

Fonte: https://www.isca-archive.org/speechprosody_2026/kuang26_speechprosody.pdf

## Casos praticos encontrados

### 1. Pausas no meio da frase e inflexao errada no final

Um usuario com ALS relatou exatamente pausas sem pontuacao e frases afirmativas terminando como pergunta. A solucao sugerida por outro usuario foi um processo em duas etapas: gerar primeiro uma atuacao natural com outro modelo e depois passar esse audio pelo Voice Changer do ElevenLabs. A ideia e separar `interpretacao` de `timbre`.

Fonte: https://www.reddit.com/r/ElevenLabs/comments/1l25lg8/any_way_of_changing_my_clone_voice_rhythm/

### 2. Controle de atuacao por performance-guia

Um criador demonstrou usar o modo de voz do ChatGPT como ator e enviar a gravacao ao Voice Changer/Actor Mode do ElevenLabs. Os comentarios avaliaram a entrega como muito mais realista e o proprio representante da ElevenLabs reconheceu a falta de um modo diretor nativo. O autor informa que o metodo serve para monologos, mas trabalha linha por linha para lapidar; outro usuario observou que sao passos demais para uso pratico. Tambem houve relato de timbre hibrido ao converter a atuacao de outra pessoa.

Fonte: https://www.reddit.com/r/ElevenLabs/comments/1jv9hxx/controlling_elevenlabs_voices_with_chatgpts/

### 3. Solucoes de silencio nao resolvem interpretacao

Criadores usam Audacity, FL Studio e Shotcut para separar frases e adicionar silencios quando tags de pausa falham. Isso resolve o comprimento do intervalo e alguns cortes, mas exige edicao humana e nao corrige enfase, continuidade ou conclusao dentro da frase.

Fontes:

- https://www.reddit.com/r/ElevenLabs/comments/1pydvb9/anyone_else_annoyed_by_how_long_elevenlabs_break/
- https://www.reddit.com/r/ElevenLabs/comments/1s70mwx/how_to_create_long_pauses_with_a_duration_around/

### 4. O fluxo comum de alta qualidade continua manual

Em testes de TTS longo, usuarios recomendam segmentos curtos, varias tomadas de cada segmento, escolha da melhor e montagem posterior. Outro criador afirma que passou dias lapidando cinco minutos. Isso pode produzir qualidade, mas viola nosso requisito de baixa operacao humana e torna o custo imprevisivel.

Fontes:

- https://www.reddit.com/r/TextToSpeech/comments/1ts1qfn/i_tested_local_tts_models_for_longform_audio/
- https://www.reddit.com/r/ElevenLabs/comments/1feoflh/can_you_make_ai_voices_have_emotional_tones_or/

### 5. Tamanho de bloco ajuda deriva, nao garante foco semantico

Ha relatos de que blocos de uma ou duas frases reduzem respiracoes e mudancas de velocidade. Tambem ha relatos de que Stability, Similarity, amostras mais expressivas e chunking trazem apenas melhora marginal quando o problema e a personalidade ou prosodia que se perde. Segmentacao continua util para consistencia e recuperacao, mas nao deve ser vendida como solucao para interpretacao.

Fontes:

- https://www.reddit.com/r/finevoice/comments/1to02mq/how_i_finally_fixed_those_awkward_ai_breathing/
- https://www.reddit.com/r/ElevenLabs/comments/1tii8w0/anyone_actually_getting_a_voice_to_stay_in/

### 6. Trocar de modelo tambem tem compromissos

- Um usuario comparando MiniMax Speech 2.8 e ElevenLabs percebeu melhor entonacao em outros idiomas no MiniMax, mas voz ainda mais robotica. E um relato individual.
- Um usuario que testou varios modelos para voice-over manteve MiniMax como solucao em uso e descreveu o servico como muito bom, enquanto encontrou exagero, ritmo incorreto ou alucinacoes em alternativas locais.
- Sobre Qwen3-TTS, um relato o descreve como consistente e capaz de receber mais de 10 mil caracteres; outro diz que o clone perde controle de tom e exige varias tomadas. O modo com voz predefinida aceita instrucao de estilo; o modo com embedding clonado no fal.ai ignora o prompt de estilo.
- Um pedido praticamente identico ao nosso, de narracao espiritual, relata Gemini TTS robotico, plano e sem respeito a pontuacao. Gemini nao e uma fuga comprovada por si so.

Fontes:

- https://www.reddit.com/r/TextToSpeech/comments/1rmz8dz/elevenlabs_ai_audio_model_or_minimax_hailuo_in/
- https://www.reddit.com/r/LocalLLaMA/comments/1n4hkar/i_tried_almost_every_tts_model_on_my_ryzen_7_5000/
- https://www.reddit.com/r/TextToSpeech/comments/1ssktby/text_to_speech_best_model/
- https://www.reddit.com/r/LocalLLaMA/comments/1s09uox/question_about_tts_models_and_qwen_3_tts/

## Opcoes que cabem na nossa esteira

| Rota | O que resolve | Custo operacional | Risco principal | Estado |
|---|---|---:|---|---|
| Bruno + Multilingual v2 com escrita oral continua | Isola a supersegmentacao sem trocar a identidade | uma unica amostra paga | ainda pode revelar limitacao real da voz/modelo | proximo teste diagnostico |
| ElevenLabs Studio e selecao de tomadas | Permite corrigir localmente | alto trabalho humano | vira edicao frase a frase | rejeitada como padrao |
| MiniMax Speech 2.8 direto via fal.ai | Troca o motor e oferece vozes portuguesas, emocao e pausa controlada | US$ 0,06/1.000 caracteres no Turbo | pode ter melhor entonacao e ainda soar robotico | adiada ate isolar o input local |
| Qwen3-TTS 1.7B direto via fal.ai | Aceita instrucao de estilo com voz predefinida | US$ 0,09/1.000 caracteres | sotaque pt-BR e consistencia ainda nao foram ouvidos por nos | candidata |
| Performance-guia + ElevenLabs Voice Changer | Separa atuacao de timbre e preserva Bruno como identidade | duas geracoes e mais complexidade | timbre hibrido, custo duplo e dependencia da guia | candidata de segunda linha |
| Edicao manual de pausas | Corrige silencios exatos | alto trabalho humano | nao corrige compreensao semantica | apenas resgate |

Precos vigentes consultados em 2026-07-22:

- MiniMax Speech 2.8 Turbo no fal.ai: https://fal.ai/models/fal-ai/minimax/speech-2.8-turbo
- Qwen3-TTS 1.7B no fal.ai: https://fal.ai/models/fal-ai/qwen-3-tts/text-to-speech/1.7b

O MiniMax possui vozes portuguesas orientadas a narracao, incluindo `Portuguese_CaptivatingStoryteller`, `Portuguese_ThoughtfulMan` e `Portuguese_Deep-VoicedGentleman`. Isso e disponibilidade de catalogo, nao aprovacao de qualidade.

Fonte: https://platform.minimax.io/docs/faq/system-voice-id

## Restricao local

Em 2026-07-22, `Win32_VideoController` identificou apenas `AMD Radeon(TM) Graphics` com memoria dedicada reportada de 512 MB. Os modelos locais mais promissores exigem uma instalacao e capacidade de GPU que esta maquina nao oferece de forma pratica. Local TTS continua possivel para rascunho leve, mas nao e candidato comprovado para o master do canal.

## Diagnostico consolidado

1. A pesquisa externa encontrou casos muito proximos, mas parte dela explica a classe do defeito, nao a causa especifica do nosso arquivo.
2. A calibracao v2 nao foi um teste limpo da voz: ela tentou dirigir a fala com microfrases e elevou em cerca de tres vezes a proporcao de frases com ate quatro palavras.
3. Nao houve overprompting, sujeira Unicode ou rotten context na calibracao v2.
4. Request Stitching preserva continuidade entre chamadas e pode tambem preservar uma entrega inicial ruim, mas isso nao esta provado como causa da v1.
5. Ainda nao ha evidencia suficiente para abandonar Bruno + Multilingual v2 ou afirmar que outro motor resolvera o problema.

## Proximo experimento recomendado

Nao gerar novamente o roteiro inteiro. Reescrever apenas a amostra densa `02-citacao-e-explicacao`, com aproximadamente 565 caracteres, como fala continua: frases de extensao moderada, subordinacao clara e nenhuma sequencia de palavras isoladas. Manter Bruno, Multilingual v2, idioma, ajustes, seed e contexto iguais. Assim, uma unica chamada A/B isola a variavel `partitura textual`.

Se essa amostra for aprovada, reescrever o roteiro inteiro pelo mesmo criterio e testar blocos antes da narracao final. Se ela for reprovada, testar contexto e seed separadamente. So depois desses controles locais a cotacao MiniMax ja registrada volta a ser candidata. Toda chamada paga continua exigindo cotacao vigente e aprovacao humana explicita.

## Metodo v0.1 para evitar fala excessivamente pausada

### Principio

Nao dirigir a voz inserindo uma pausa grafica em cada lugar onde se deseja expressividade. A unidade de escrita deve ser a ideia falada, nao a palavra enfatizada. Pontuacao continua gramatical; ritmo nasce principalmente da sintaxe, da ordem das informacoes, dos conectivos e do contexto do paragrafo.

A ElevenLabs afirma que o ritmo pode ser guiado por estilo narrativo natural e que texto, gramatica, pontuacao e formatacao afetam a entrega. Tambem alerta que marcacao excessiva de pausas pode causar instabilidade. Em relatos de long-form de 2026, criadores recomendam blocos um pouco maiores e baseados em sentido, avaliados como paragrafo, em vez de gerar sentenca por sentenca.

Fontes:

- https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices
- https://elevenlabs.io/docs/eleven-creative/playground/text-to-speech
- https://www.reddit.com/r/TextToSpeech/comments/1rzj5pr/what_am_i_missing_with_elevenlabs_text_to_speech/
- https://www.reddit.com/r/TextToSpeech/comments/1sai1gv/tried_text_to_speech_with_elevenlabs_but_the/

### Regras de escrita

1. Um ponto final encerra uma ideia completa. Nao separar sujeito, acao, causa, contraste ou consequencia em frases independentes apenas para produzir enfase.
2. Transformar listas dramaticas em enumeracoes dentro da frase quando cada item nao precisa de uma parada propria. Exemplo: `uma doenca, uma perda ou uma injustica`, e nao `Uma doenca. Uma perda. Uma injustica.`
3. Usar conectivos que tornem audivel a relacao logica: `porque`, `mas`, `ainda assim`, `por isso`, `embora`, `quando`, `enquanto`, `nao... mas...`.
4. Manter variacao de comprimento. Frase curta pode concluir ou destacar uma ideia, mas nao deve virar o ritmo dominante nem aparecer em cascata.
5. Cada paragrafo representa um movimento semantico, como afirmacao, explicacao, aplicacao ou transicao. Quebra de paragrafo nao entra entre frases que dependem diretamente uma da outra.
6. Reticencias, travessoes repetidos, caixa alta e tags de pausa ficam proibidos por padrao. Entram somente quando a hesitacao, interrupcao ou pausa for parte literal da intencao e puder ser justificada.
7. Numeros, referencias, siglas e simbolos devem ser escritos como serao falados. Isso reduz ambiguidade sem usar pontuacao como remendo.
8. O primeiro bloco precisa comecar com duas ou mais frases completas e fluidas antes de qualquer fragmento retorico. Request Stitching so continua depois de essa cadencia inicial passar no gate humano.

### Preflight local do canal

O video 002 aprovado vira referencia empirica, nao benchmark universal. Antes de pagar pela voz, o texto deve emitir alerta se:

- mais de 15% das frases tiverem quatro palavras ou menos;
- houver tres frases consecutivas com sete palavras ou menos;
- um paragrafo tiver mais fragmentos retoricos do que frases completas;
- houver reticencias, pontuacao repetida, tags de pausa ou quebras de linha usadas como direcao invisivel;
- uma lista puder ser unida gramaticalmente sem perder sentido e ainda estiver fragmentada em varias frases.

Os alertas exigem revisao, nao reescrita automatica cega. Uma frase curta pode ser correta quando conclui uma ideia importante. O objetivo e impedir padroes acidentais como o da calibracao v2.

### Geracao

- Gerar por movimento semantico, nao por frase isolada.
- Manter inicialmente Bruno Cardoso, Multilingual v2, `language_code=pt`, stability `0.50`, similarity `0.75`, style `0`, speed `1.0` e seed atual, pois essa combinacao ja produziu um audio aprovado.
- No teste de recuperacao, alterar somente a escrita. Contexto, seed e configuracoes permanecem fixos.
- Depois de uma primeira amostra aprovada, gerar o primeiro bloco integral sem cadeia anterior. Somente entao usar Request Stitching para os blocos seguintes.
- Avaliar um paragrafo completo pela continuidade da ideia; nao aprovar ou reprovar palavras isoladas.

## Regra que nasce desta falha

Calibracao humana aprova uma combinacao de `texto + voz + modelo + modo de geracao + tipo de episodio`. Ela nao transforma uma voz em padrao universal. Uma tentativa que altera a escrita de forma extrema nao pode condenar o provedor; primeiro se audita o payload e se isola uma variavel por vez.
