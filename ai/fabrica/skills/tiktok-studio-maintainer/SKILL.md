---
name: tiktok-studio-maintainer
description: Maintain browser-based TikTok Studio metric collection and workflow mappings. Use when TikTok Studio navigation, labels, selectors, session state, metric tables, date ranges, exports, or response contracts change; when login expires; or when Codex must repair and resume TikTok Studio automation without duplicating uploads, publications, or account changes.
---

# TikTok Studio Maintainer

Use the universal `integration-maintainer` incident sequence first. This skill
adds TikTok Studio semantics; it does not weaken its side-effect guard.

## Inspect Before Acting

1. Confirm account identity, locale, timezone, and session health.
2. Capture the visible page structure and current URL.
3. Locate controls by role, accessible name, heading, label, and surrounding
   text before considering CSS or positional selectors.
4. Compare observed fields with the metric contract.
5. Use read-only navigation or export to test repaired selectors.
6. Never use a publish, delete, or account control as a diagnostic probe.

Read `references/screen-map.md` for semantic landmarks and selector fallback
order. Read `references/metrics-contract.md` before storing a snapshot.

## Session Health

Classify the session as `healthy`, `expired`, `challenged`, `wrong_account`, or
`unknown`. Login, CAPTCHA, 2FA, account switching, and consent acceptance are
human gates. Preserve the target page and resume point while waiting.

## Selector Maintenance

Prefer semantic selectors. Keep at least one alternate landmark for each
required field. Treat a missing metric as `unavailable` until the page or API
proves it is zero. Record locale-dependent labels separately from the semantic
field name.

After a repair, validate a read-only snapshot for one known item and one date
range. Do not publish or upload as a regression test.

