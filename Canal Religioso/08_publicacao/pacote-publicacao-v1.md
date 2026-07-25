# Pacote de publicação dos vídeos 001 e 002

Status: tudo que pode ser preparado localmente está pronto. O envio continua bloqueado somente pela restauração da conta Google e, depois dela, pela criação dos IDs dos vídeos no YouTube.

## Arquivos canônicos

- Vídeo 001: `piloto-001-publicacao-v1.json`
- Vídeo 002: `video-002-publicacao-v1.json`
- Registro legal ACF: `registro-citacoes-acf.json`
- Configuracao do canal: `configuracao-canal-v1.json`
- Comandos preparados do yutu: `yutu-pos-restauracao-v1.md`
- Preflight de monetizacao: `../01_briefs/politica-monetizacao-youtube-v1.md`

Cada manifesto contém título, descrição, capítulos, tags, hashtags, comentário fixado, configurações, arquivos, hashes, tela final e pendências externas.

Preflight local: `validar-pacote-publicacao.py`.

Folhas legíveis para publicação manual: `piloto-001-copiar-e-colar-v1.txt` e `video-002-copiar-e-colar-v1.txt`. Elas são geradas por `exportar-textos-publicacao.py`, a partir dos manifestos canônicos, para evitar divergência entre versões.

## Ordem de publicação

1. Restaurar a conta Google e concluir o OAuth do yutu.
2. Enviar os dois vídeos como `não listados`, sem notificar inscritos.
3. Registrar os IDs e URLs devolvidos pelo YouTube nos respectivos manifestos.
4. Adicionar em cada descrição a linha `cross_link.description_line_template` com a URL real do outro vídeo.
5. No vídeo 001, configurar uma recomendação para o vídeo 002 e um elemento de inscrição nos 20 segundos finais.
6. No vídeo 002, configurar uma recomendação para o vídeo 001 e um elemento de inscrição nos 20 segundos finais.
7. Anexar as legendas `pt-BR`, escolher cada thumbnail e confirmar a marcação de conteúdo alterado ou sintético.
8. Esperar o processamento em 1080p e as verificações de direitos autorais.
9. Fazer a checagem humana não listada em celular e computador: título, thumbnail, acentos das legendas, capítulos, volume, tela final e links cruzados.
10. Tornar público somente depois dessa checagem. Registrar as unidades ACF no livro central apenas quando cada vídeo realmente ficar público.

Os dois rascunhos somam `8` unidades de versículo ACF (`5 + 3`). O registro permanece em `0` enquanto nenhum deles estiver público.

## Decisões preservadas

- Os dois masters atuais ficam como estão; não há nova geração paga.
- Ambos usam uma recomendação visual por serem episódios anteriores ao padrão de duas recomendações.
- O piloto 001 continua como exceção de 9:38 à regra posterior de duração mínima de 10 minutos.
- As dívidas aceitas de cada episódio estão registradas nos manifestos e não viram padrão para o vídeo 003.
