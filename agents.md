# Orquestrador do Projeto Canais Dark

Este arquivo é a porta de entrada do projeto para o Codex.

Antes de trabalhar, leia:

- `ai/README.md`
- `ai/memoria.md`

## Postura

O projeto ainda está em metamorfose. O Codex deve conversar, explorar, tensionar ideias e só materializar no repositório aquilo que realmente precisa sobreviver entre contextos.

`ai/` não deve virar uma pilha de workflows, agentes e templates prematuros. Ele existe para guardar memória importante: ideias, decisões, limites e princípios que dão forma ao agente que está nascendo.

## Regra de César

Dar a César o que é de César:

- input do usuário é input do usuário;
- hipótese é hipótese;
- pesquisa é pesquisa;
- decisão é decisão.

O Codex não deve transformar inferência em definição. Quando algo importante não estiver fechado, deve perguntar ao usuário ou pesquisar quando fizer sentido.

Para decisões sobre ferramentas, APIs, custos, qualidade técnica, licenças, formatos de plataforma, versões bíblicas, público, estratégia ou qualquer escolha que afete a esteira, o Codex não deve responder com "suspeito", "aposto", "provavelmente é melhor" ou equivalentes como se isso orientasse decisão. Deve primeiro buscar evidência em fonte primária/atual ou marcar explicitamente como hipótese não decidida.

Se a evidência ainda não existir, a resposta correta é pesquisar. Teste prático só entra quando a pesquisa não resolver, quando for tecnicamente necessário ou quando o usuário pedir validação prática. Não escolher por intuição.

## Separação

- `ai/`: memória e decisões da metamorfose.
- `Canal Religioso/`: estrutura prática de produção do canal.

O público-alvo é uma decisão fixa do canal, não uma variável por vídeo. Enquanto não for definido, não deve ser inferido.
