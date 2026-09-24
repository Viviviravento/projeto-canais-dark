# Incident Contract

Use `factory/contracts/v1/IntegrationIncident.schema.json`.

State progression:

`detected -> frozen -> investigating -> fixed -> verified -> resumed`

`blocked` is allowed only after three diagnostic cycles without new evidence.

Required evidence by transition:

- `detected -> frozen`: symptom and affected operation.
- `frozen -> investigating`: checkpoint, idempotency key, one hypothesis.
- `investigating -> fixed`: confirmed root cause and evidence references.
- `fixed -> verified`: correction and regression checks.
- `verified -> resumed`: passed regression and safe resume point.

Side-effect flags identify operations that may never be repeated during
diagnosis: `paid_call`, `publication`, and `deletion`.
