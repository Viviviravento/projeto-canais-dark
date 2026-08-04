# Metricas e aprendizagem

Os dados brutos de plataforma entram como `MetricObservation` imutavel nos
snapshots de 24h, 72h, 7d e 28d. Diagnosticos e mudancas editoriais entram como
`LearningDecision` versionado.

O piloto 001 foi publicado publicamente em 23 de julho de 2026, com ID
`ZkmCkF6XR_g`, conforme
`operations/a-palavra-que-cuida/08_publicacao/piloto-001-publicacao-v1.json`.

O primeiro `MetricObservation` do piloto 001 foi persistido em 2026-07-24 como
auditoria inicial anterior a 24 horas. A amostra tinha apenas tres visualizacoes
e uma impressao, portanto serve como linha de base operacional, nao como linha
de base confiavel de desempenho. O diagnostico separado esta em
`piloto-001/diagnostico-inicial-v0.1.md`.

Os proximos passos desta camada sao coletar os snapshots reais de 24h, 72h, 7d
e 28d sem reconstruir ou inventar janelas que a plataforma ja nao consiga
fornecer. Os videos 002 e 003 continuam sem publicacao registrada.
