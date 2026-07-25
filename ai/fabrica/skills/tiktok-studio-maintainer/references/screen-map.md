# TikTok Studio Semantic Map

This map stores roles, not brittle selectors. Update observed labels with date,
locale, and page URL when the product changes.

## Session

- Account identity: profile image/menu plus visible account name or handle.
- Login challenge: password, verification, CAPTCHA, consent, or account picker.
- Healthy session: Studio navigation and account identity are both visible.

## Content List

- Landmark: heading or navigation item equivalent to content/posts.
- Item identity: caption/title, publication timestamp, thumbnail, or content ID.
- Safe actions: open details, change date range, read metrics, export.
- Unsafe diagnostic actions: upload, publish, delete, privacy change.

## Analytics

- Landmark: analytics/overview/content/audience navigation.
- Date range: explicit start/end labels; record timezone.
- Metric card: semantic label plus value and optional comparison period.
- Table: preserve headers, row identity, pagination, and sort state.

## Selector Fallback Order

1. Accessible role and exact accessible name.
2. Associated label and form-control relationship.
3. Heading or landmark plus nearby semantic text.
4. Stable test identifier observed in the product.
5. CSS structure scoped to a semantic container.

Never use absolute screen coordinates as a maintained selector.

