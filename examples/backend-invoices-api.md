# Designing an invoices API

Playbook: [`backend`](../playbooks/backend/CLAUDE.md) — alias `ap-be`

One sentence of requirements in; a design document out — with the parts that hurt in production a year later (idempotency, pagination, state transitions, partial failure) present from the first draft, in the playbook's mandated structure.

## Session (abridged)

**You:**

```text
Design a production-ready REST API for invoices. Create, list, fetch, finalize,
void. Multi-tenant SaaS, Postgres, clients will retry on timeouts.
```

**ap-be:**

> ```text
> Goal:
>   Invoice lifecycle API safe under client retries and concurrent access,
>   with tenant isolation as a hard boundary.
>
> Non-goals:
>   Payments, PDF rendering (async concern, referenced only), tax calculation.
>
> API contract:
>   POST   /v1/invoices                 create draft; REQUIRES Idempotency-Key
>   GET    /v1/invoices?cursor=&limit=  cursor pagination, stable order
>                                       (created_at, id) tiebreak
>   GET    /v1/invoices/{id}
>   POST   /v1/invoices/{id}/finalize   draft -> open; assigns invoice number;
>                                       idempotent by state (finalizing an open
>                                       invoice returns 200, not 409)
>   POST   /v1/invoices/{id}/void       open -> void; body requires reason
>
>   Errors: RFC 9457 problem+json with stable machine codes
>   (invoice_not_found, invalid_transition, idempotency_key_reuse, ...).
>   Versioning: /v1 in path; additive changes only within v1.
>
>   You said clients retry on timeouts — that is why Idempotency-Key is
>   required on create, not optional: a retried create without it is a
>   duplicate invoice. Server stores key -> response for 24h; same key with a
>   different body returns 422 idempotency_key_reuse.
>
> Data model:
>   invoices(id ULID pk, tenant_id fk NOT NULL, number nullable-until-final,
>            status enum(draft,open,void,paid), currency char(3),
>            amount_minor bigint, version int for optimistic locking,
>            created_at timestamptz, finalized_at, voided_at, void_reason)
>   invoice_lines(id, invoice_id fk, description, quantity, unit_minor)
>   idempotency_keys(tenant_id, key, request_hash, response, expires_at,
>                    pk(tenant_id, key))
>   Money in integer minor units. Invoice number assigned at finalize from a
>   per-tenant sequence — draft numbering guarantees gaps.
>
> Failure modes:
>   - Double-submit create -> idempotency table absorbs it.
>   - Concurrent finalize + void -> single UPDATE ... WHERE id=$1 AND
>     status='open' (state-machine guard); loser gets invalid_transition with
>     the current state in the response.
>   - Retry storm on list -> cursor pagination is naturally idempotent; add
>     per-tenant rate limit.
>   - Postgres failover mid-finalize -> transaction covers number assignment +
>     status flip; retried request replays via idempotency key.
>
> Security:
>   tenant_id from the auth token, never from the request body; every query
>   filters by it. Authorize finalize/void as distinct actions, not just
>   route access. Audit log for finalize and void (who, when, reason).
>
> Observability:
>   RED per endpoint; counter on invalid_transition (spikes reveal confused
>   clients); audit events as structured logs with request_id + trace_id.
>
> Rollout:
>   Ship behind /v1 from day one. Contract tests on the error codes — clients
>   will branch on them, so they are API surface.
>
> Open questions:
>   Invoice number format per tenant (legal requirements vary by country)?
>   Hard-delete policy for drafts? Is "paid" set by this service or by a
>   payments service via event?
> ```

## What the playbook changed

- The prompt never mentioned idempotency, pagination style, error format, or concurrency — the playbook's API defaults (idempotency keys for retried writes, cursor pagination for unbounded collections, problem-details errors, explicit versioning) injected them, each tied to the stated requirement that clients retry.
- Transitions are modeled as a guarded state machine with a compare-and-set update, and `finalize` is idempotent *by state* — the difference between a clean API and a support queue full of 409s.
- Tenant ID is treated as a security boundary per the playbook's standing rule: derived from the token, filtered in every query, never read from the body.
- The design ends with open questions instead of invented answers — invoice numbering legality is flagged as a question, not guessed. The output structure (`Goal` through `Open questions`) is the playbook's required design format.

## Run it

```bash
claude-playbook install https://github.com/ramazanpolat/awesome-claude-playbooks/tree/main/playbooks/backend
ap-be
```
