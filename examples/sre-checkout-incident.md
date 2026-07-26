# Nine percent of checkouts are failing

Playbook: [`sre`](../playbooks/sre/CLAUDE.md) — alias `ap-sre`

An error-rate spike on the money path. The playbook detects incident mode from the first message and switches to terse, action-first output: hypothesis, checks, mitigation, rollback, comms. No essays during an outage.

## Session (abridged)

**You:**

```text
5xx on /checkout jumped from 0.1% to 9% eight minutes ago. Act as incident
commander and give me the next 10 minutes.
```

**ap-sre:**

> Incident mode.
>
> **Hypothesis:** a change. At 8 minutes in, the prior is a deploy, config/flag
> change, or a dependency (payment provider, database) — not gradual capacity.
>
> **Next five minutes of checks, in order:**
>
> 1. What shipped in the last 60 min — deploys, flags, migrations, config. One command/dashboard, whatever your platform gives you.
> 2. Error class breakdown on /checkout: timeouts vs 500s vs 502/503. Timeout-shaped and 500-shaped incidents have different suspects.
> 3. Scope: all regions? all tenants? checkout only, or is /cart degrading too? Global-and-endpoint-specific points harder at code; regional points at infra.
> 4. Dependency health: payment provider status + latency, DB connection pool utilization, queue depth.
> 5. Saturation quick pass: CPU, memory, pod restarts on the checkout service.
>
> **Safest mitigation:** if a deploy correlates, roll it back now. You do not
> need root cause to roll back; you need correlation. If no deploy correlates,
> disable the most recently changed flag on the path.
>
> **Rollback path:** confirm the previous version is still deployable before
> you need it. Know the command; don't run it yet if checks 1–3 take under
> three minutes.
>
> **Communicate:** post in the incident channel — impact ("9% of checkouts
> failing since 14:02"), owner (you), next update in 15 min. Status page if
> customer-visible checkout failures exceed your public threshold.
>
> Report back with 1–3; I'll narrow.

**You:**

```text
Deploy 14 minutes ago (checkout-svc v2026.07.24.1). Errors are all 500s,
logs say "connection pool exhausted, timeout acquiring connection". All regions.
```

**ap-sre:**

> Correlated deploy + pool exhaustion + all regions = roll back now.
>
> 1. **Mitigate:** roll back checkout-svc to the previous version. Say the word and paste your rollout tool; I'll give the exact command.
> 2. **Verify:** 5xx on /checkout back under 0.5% within ~2 min of pods cycling; pool acquisition timeouts stop. Watch p95 latency too — recovering pools drain queued requests first.
> 3. **Do not** raise the pool size as the fix. That treats the symptom and can move the bottleneck to the database.
> 4. **Preserve:** keep one bad-version pod's logs/metrics if your platform allows; you'll want them for the postmortem.
> 5. **Comms:** update the channel — "rolling back, expect recovery by :24".
>
> Likely root cause to check tomorrow, not now: v2026.07.24.1 holding
> connections across an await, a leaked transaction, or a new query slow enough
> to pin the pool. When you're stable, say "postmortem" and I'll draft the
> timeline in the standard format.

## What the playbook changed

- Mode detection: the playbook maps "act as incident commander" (and any "production is down" phrasing) to incident mode — terse, numbered, action-first. The observability lecture is explicitly deferred.
- Its first block is the exact five-part structure the playbook mandates: hypothesis, next five minutes, safest mitigation, rollback path, comms — including the "next update in 15 min" discipline most ad-hoc responses forget.
- Rollback on correlation, not on root cause. And its red lines forbid the classic panic moves: nothing gets deleted, and the pool doesn't get resized to make the graph go green.
- It ends by setting up the after: evidence preservation and a one-word path ("postmortem") into the playbook's blameless postmortem format.

## Run it

```bash
claude-playbook install https://github.com/ramazanpolat/awesome-claude-playbooks/tree/main/playbooks/sre
ap-sre
```
