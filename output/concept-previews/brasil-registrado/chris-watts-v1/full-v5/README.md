# Chris Watts — V5 documental

Esta versão interna aplica a direção editorial de `Testemunha do Tempo`:

- registros relevantes são parte ativa da história, não fundo para locução;
- conversa documental relevante preserva áudio original e recebe legenda PT-BR por turno;
- a narração prepara, conecta e interpreta antes ou depois do registro, sem encobri-lo;
- a câmera da porta fica apenas na abertura e no encerramento;
- a tela da TV do vizinho permanece sem `delogo` ou blur artificial.

## Construção reproduzível

1. `build_full_v5.py` monta o núcleo documental: contexto curto, registros de bodycam, entrevista e a evidência da TV do vizinho.
2. `extend_documentary_duration_v5.py` insere antes do desfecho os demais trechos de entrevista com valor próprio, áudio original e legendas PT-BR. Ele não adiciona locução para alcançar duração.
3. `documentary-timeline-v5.json` e `qa-full-v5.json` descrevem o episódio final para revisão; `visual-qa-v5.json` registra a inspeção por quadros.

O render continua `internal-only`, pendente de revisão humana e de liberação de direitos. O MP4 e a pasta de trabalho são ignorados pelo Git; o roteiro visual, a timeline e o QA reproduzíveis são os artefatos versionáveis.
