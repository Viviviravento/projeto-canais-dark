# Politica de catalogo editorial e playlists v0.1

Data da decisao: 2026-07-24.

## Objetivo

Cada pauta deve funcionar como episodio e como parte de um catalogo futuro. Ao propor um video, o Codex considera quais continuacoes naturais ele permite, quais playlists ele fortalece e qual caminho de proxima visualizacao pode nascer dele.

Isso nao obriga todo tema a virar serie. Uma pauta forte pode ser publicada sozinha, mas sua relacao com o catalogo precisa ser registrada.

## Evidencia de plataforma

- O YouTube permite selecionar mais de uma playlist comum ao editar um video: https://support.google.com/youtube/answer/10232933
- Playlists podem reunir videos e Shorts, e a interface oferece filtros por tipo: https://support.google.com/youtube/answer/57792
- Uma playlist marcada como serie oficial informa ao YouTube que aquele conjunto deve ser visto em conjunto. Um video nao pode pertencer a mais de uma playlist de serie: https://support.google.com/youtube/answer/6084043
- O YouTube preserva dados de tempo de exibicao associados a playlists nos relatorios gerais, embora uma playlist excluida deixe de ser identificada nos relatorios proprios. Playlists devem ser mantidas como ativos editoriais, nao criadas e apagadas casualmente: https://support.google.com/youtube/answer/57792

## Arquitetura em camadas

As playlists comuns funcionam como facetas que podem se cruzar:

1. **Necessidade vivida:** ansiedade, cansaco, sofrimento, culpa, familia, perdao ou recomeco.
2. **Mapa biblico:** Jesus, Jo, Paulo, mulheres da Biblia, livros, capitulos ou versiculos.
3. **Abordagem editorial:** historia de vida, escolhas e consequencias, ensinamentos, versiculos explicados ou reflexoes aplicadas.

Exemplo: um episodio sobre Jo pode pertencer a `Reflexoes biblicas para dias dificeis`, a uma futura playlist sobre personagens e a uma serie sobre sofrimento. Outro episodio sobre uma decisao especifica de Jo pode compartilhar a figura, mas pertencer primariamente a uma playlist de escolhas biblicas.

Nao criar uma playlist diferente para cada combinacao possivel. A organizacao deve ajudar uma pessoa real a escolher o proximo video.

## Nascimento gradual

- `1 video`: semente registrada no catalogo. Nao criar playlist publica de um item, salvo experimento explicitamente justificado.
- `2 videos compativeis`: playlist elegivel para ser criada e receber titulo e descricao publicos.
- `3 ou mais videos`: playlist elegivel para secao da pagina inicial, ordenacao editorial e acompanhamento proprio.
- Playlist vazia nunca e criada no YouTube. Ideias futuras permanecem apenas no catalogo do repositorio.

Esses numeros sao uma politica operacional v0.1 para evitar poluicao. Nao sao regra nem garantia de distribuicao do YouTube.

## Papel de cada pauta

Toda ideia selecionada registra:

- `catalog_role`: abre uma familia, continua uma familia, preenche uma lacuna ou testa uma nova abordagem;
- `primary_playlist`: principal caminho de continuidade daquele episodio;
- ate duas `secondary_playlists`, somente quando houver aderencia real;
- de duas a quatro `future_episode_seeds`, com angulos diferentes e sem repetir o mesmo roteiro;
- `binge_bridge`: qual episodio anterior prepara este e qual proxima pergunta ele desperta;
- se existe ordem narrativa obrigatoria ou se os videos podem ser vistos separadamente.

O planejamento de continuacoes nao autoriza fabricar redundancia. Cada novo episodio sobre a mesma figura precisa mudar a pergunta, o periodo da vida, o conflito, a fonte biblica ou a aplicacao.

## Playlists comuns e series oficiais

- Usar playlists comuns para classificacao cruzada. Um video pode ter uma playlist primaria e ate duas secundarias.
- Usar serie oficial apenas quando houver sequencia canonica ou ordem de consumo claramente desejada.
- Nao transformar playlists tematicas amplas em series oficiais, pois isso impediria o mesmo video de participar de outra serie oficial mais apropriada.
- Titulos e descricoes devem ser escritos para o espectador, com linguagem clara e pesquisavel, sem nomes internos nem empilhamento de palavras-chave.

## Videos horizontais e derivados

- As playlists editoriais principais recebem videos horizontais por padrao.
- Shorts nao entram automaticamente nas mesmas playlists, mesmo que o YouTube permita. O recorte existe para levar ao episodio completo e pode quebrar o fluxo de consumo longo.
- Quando houver pelo menos tres derivados publicados, considerar uma playlist propria de mensagens curtas. A decisao depende dos dados de consumo de Shorts.
- TikToks nao alteram a estrutura de playlists do YouTube, mas seus CTAs podem apontar para o nome pesquisavel de uma playlist quando ela for o melhor destino.

## Publicacao e manutencao

- Antes de publicar, confirmar as playlists planejadas, existencia no YouTube, visibilidade e ordem.
- Depois da publicacao, registrar o ID da playlist e a associacao efetivamente realizada.
- Incluir na descricao apenas a playlist mais relevante; nao despejar uma lista de links.
- Preservar os dois videos individuais na tela final conforme a politica atual. Playlist pode ser destino em descricao, pagina inicial ou card quando houver funcao clara.
- Medir origem de trafego por playlist, tempo de exibicao e proxima visualizacao quando os dados existirem. Nao atribuir causalidade apenas porque o video foi adicionado a uma playlist.

