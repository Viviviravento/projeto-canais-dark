# QA obrigatório da narração — Ruptura Oculta

Este gate incorpora as falhas já observadas em produções anteriores, especialmente erros de acentuação, pontuação, pronúncia e ênfase.

## Antes de gerar

- Revisar o texto final em português brasileiro.
- Preservar todos os acentos: `até`, `aeroporto`, `justiça`, `cenário`, nomes próprios e datas por extenso quando isso melhorar a fala.
- Não enviar texto sem acentos para economizar tempo ou evitar problemas de encoding.
- Quebrar frases longas em blocos curtos.
- Usar pontuação com intenção: vírgula para pausa curta, ponto para fechamento, dois-pontos ou pergunta para mudança de entrega.
- Conferir se cada tag emocional está coerente com o trecho e não substitui a pontuação.
- Identificar palavras com risco de pronúncia e testá-las em uma frase curta.
- Separar no arquivo o texto narrado das instruções de edição.

## Geração de teste

- Gerar primeiro um bloco de naturalidade, um de tensão e um de encerramento.
- Não gerar o episódio inteiro antes da aprovação dos testes.
- Regenerar somente o bloco que apresentar erro.
- Registrar versão, texto enviado, modelo e parâmetros usados.

## Escuta crítica

Conferir o áudio contra o texto escrito, palavra por palavra:

- Acento e sílaba tônica.
- Vogais iniciais, especialmente em palavras como `aeroporto`.
- Nomes próprios.
- Números e datas.
- Pontuação audível e pausas naturais.
- Ênfase correta em palavras importantes, como `justiça`.
- Nenhuma palavra engolida, cortada ou pronunciada de forma estranha.
- Emoção presente, mas sem prejudicar a compreensão.

## Aprovação

O áudio só pode seguir para montagem depois que:

1. O texto estiver aprovado.
2. A pronúncia estiver conferida.
3. A pontuação estiver audível.
4. O arquivo tiver sido escutado do início ao fim.
5. As divergências estiverem registradas e corrigidas.

Se houver dúvida sobre uma palavra, ela deve ser testada antes de continuar. Nunca corrigir um erro de áudio apenas durante a edição.
