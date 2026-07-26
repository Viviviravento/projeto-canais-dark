---
name: integration-maintainer
description: Diagnose, repair, and safely resume broken API, CLI, browser, OAuth, billing, pricing, schema, selector, or file integrations. Use when an operation fails, a response shape or page changes, authentication expires, a paid request is rejected, an external dependency drifts, or Codex must continue from a checkpoint without duplicating payment, publication, deletion, or another irreversible side effect.
---

# Integration Maintainer

Treat the failure as an incident with a preserved resume point, not as permission
to rerun the operation.

## Required Sequence

1. Detect the first observable failure.
2. Freeze the affected operation before any side effect can repeat.
3. Record symptoms, raw evidence references, checkpoint, and idempotency key.
4. Form one falsifiable hypothesis.
5. Test that hypothesis in isolation using read-only, mocked, dry-run, or free calls.
6. Reject it or confirm the root cause with evidence.
7. Apply the smallest correction that addresses the confirmed cause.
8. Register the correction and affected versions.
9. Run regression checks without repeating the original side effect.
10. Resume from the recorded checkpoint only after regression passes.

Store the incident as `IntegrationIncident`. Read
`references/incident-contract.md` when creating or updating that record.

## Side-Effect Guard

- Never diagnose by repeating a paid generation, publication, deletion, transfer,
  or account mutation.
- Never infer success from a timeout. Reconcile by request ID, idempotency key,
  provider history, or read-only status endpoint.
- A retry of a paid call requires a new live `CostQuote`.
- Preserve partially completed artifacts and the exact next safe action.

## Evidence Discipline

Keep symptom, hypothesis, evidence, cause, and correction separate. Do not patch
before a cause is confirmed. When a test disproves a hypothesis, record that and
start a new cycle.

After three cycles without new evidence, classify the blocker and request only
the necessary human action. Typical human-only actions are credentials,
CAPTCHA/2FA, account ownership, provider support, and destructive confirmation.

## Resume Rule

Resume at the smallest verified checkpoint. Do not restart the whole workflow
when upstream artifacts are valid. Keep the operation frozen if regression
fails or if remote state cannot be reconciled.

