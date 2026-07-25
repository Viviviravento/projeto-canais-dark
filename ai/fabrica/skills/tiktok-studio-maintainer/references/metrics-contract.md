# TikTok Metric Contract

Public API fields and Studio-only observations must keep separate provenance.

## Public API Layer

The common video object exposes basic counters such as views, likes, comments,
and shares when the account and scopes permit them. Store the exact endpoint,
response capture hash, and collection time.

Reference: https://developers.tiktok.com/doc/tiktok-api-v2-video-object

## Studio Layer

Studio may expose deeper consumption, audience, retention, traffic, and profile
signals. Treat every field as observed UI data. Record:

- semantic metric name;
- displayed label and locale;
- value and unit;
- account and content identity;
- start/end date and timezone;
- captured timestamp;
- page URL and screenshot/export reference;
- unavailable versus displayed zero.

## Snapshots

Use `24h`, `72h`, `7d`, and `28d` windows. Store raw observations immutably as
`MetricObservation`; place interpretations in versioned `LearningDecision`
records. Never overwrite an older snapshot after the platform revises data.

