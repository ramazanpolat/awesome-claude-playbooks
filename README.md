# awesome-claude-playbooks

[![Validate](https://github.com/ramazanpolat/awesome-claude-playbooks/actions/workflows/validate.yml/badge.svg)](https://github.com/ramazanpolat/awesome-claude-playbooks/actions/workflows/validate.yml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

Installable playbooks that turn [Claude Code](https://claude.com/claude-code) into a specific senior professional: a DBA that refuses to recommend an index before seeing the execution plan, an SRE that answers an outage with the next five minutes of checks, a security engineer that stays strictly defensive no matter how the question is phrased.

Each playbook is a complete, isolated Claude Code instance managed by [`claude-playbook`](https://github.com/ramazanpolat/claude-playbooks) — its own instructions, settings, history, and memory. You don't paste a prompt; you launch a mode.

## The difference, in one prompt

Ask plain Claude Code:

```text
This query got slow. Fix it:
SELECT * FROM orders WHERE customer_id = $1 ORDER BY created_at DESC LIMIT 20;
```

You get a reasonable, generic answer — immediately, and unverified:

> Add an index on `customer_id`, avoid `SELECT *`, consider caching hot
> customers, maybe paginate with keyset pagination...

Ask `ap-dba` the same thing and it declines to prescribe before it has evidence:

> Before I recommend anything for production, I need:
>
> 1. Engine and version (I'll assume PostgreSQL until told otherwise).
> 2. The plan: `EXPLAIN (ANALYZE, BUFFERS, VERBOSE)` for this query.
> 3. Row count of `orders` and its write rate — an index here taxes every insert.
> 4. Existing indexes on `orders`.
>
> My working hypothesis is a composite index on `(customer_id, created_at DESC)`
> replacing a single-column index, which would turn the sort into a backward
> index scan — but I won't confirm until I see the plan.

Then it answers in its mandated format — `Finding / Evidence / Impact / Recommendation / SQL / Validation / Risk` — and its playbook forbids it from suggesting destructive SQL without a row-count check.

Same model. Same question. The playbook changes what counts as an acceptable answer. [Read the full session.](examples/dba-slow-query.md)

## Quick start

```bash
# 1. Install the playbook manager (once)
curl -fsSL https://raw.githubusercontent.com/ramazanpolat/claude-playbooks/main/install.sh | sh

# 2. Install a role
claude-playbook install https://github.com/ramazanpolat/awesome-claude-playbooks/tree/main/playbooks/dba

# 3. Launch it
ap-dba
```

Every role installs the same way — swap `dba` for any directory under [`playbooks/`](playbooks/). Installing creates the shell alias automatically; the manifest in each role provides the name and alias.

## The collection

| Playbook | Alias | Optimized for | Will not |
| --- | --- | --- | --- |
| [`dba`](playbooks/dba/CLAUDE.md) | `ap-dba` | Schema design, query tuning, safe migrations, database incidents | Guess an index without a plan; write destructive SQL without a row-count check |
| [`sre`](playbooks/sre/CLAUDE.md) | `ap-sre` | Incident command, SLOs, observability, Kubernetes, postmortems | Delete things as a first mitigation; page on causes instead of symptoms |
| [`secops`](playbooks/secops/CLAUDE.md) | `ap-sec` | Threat models, secure code review, vulnerability triage, hardening | Go offensive; call anything "low risk" without stating the exposure |
| [`frontend`](playbooks/frontend/CLAUDE.md) | `ap-fe` | UI implementation, accessibility, state design, Core Web Vitals | Ship div-buttons; silence type errors it doesn't understand |
| [`backend`](playbooks/backend/CLAUDE.md) | `ap-be` | API contracts, services, auth, queues, partial-failure design | Invent custom crypto; break an API without a migration path |
| [`data`](playbooks/data/CLAUDE.md) | `ap-data` | Analytics SQL, dbt models, pipelines, metric definitions | Change a metric silently; run unbounded backfills |
| [`seo`](playbooks/seo/CLAUDE.md) | `ap-seo` | Technical audits, structured data, migrations, content briefs | Cloaking, link buying, doorway pages; promise rankings |
| [`writer`](playbooks/writer/CLAUDE.md) | `ap-write` | READMEs, API references, runbooks, release notes | Invent product behavior; call anything "easy" |
| [`awesome`](CLAUDE.md) | `ap` | Router: names the right role for a request and hands you the launch command | Duplicate the deep role checklists |

The "Will not" column is not marketing — each is a literal red line written into the playbook's standing instructions. That is what separates a playbook from a persona: it holds its constraints even when the question invites shortcuts.

## See them in action

Every role has a worked example: a realistic prompt and the abridged session it produces, with notes on what the playbook did that a generic assistant would not.

| Example session | The moment that matters |
| --- | --- |
| [The slow query that wanted an index](examples/dba-slow-query.md) | Refuses to prescribe until it sees `EXPLAIN (ANALYZE, BUFFERS)` — then reads a lossy bitmap heap scan correctly |
| [Nine percent of checkouts are failing](examples/sre-checkout-incident.md) | Answers with a hypothesis and the next five minutes of checks, not a lecture on observability |
| [Threat-modeling a password reset flow](examples/secops-password-reset.md) | Finds the user-enumeration timing leak and the sessions that survive the reset |
| [The modal that only worked with a mouse](examples/frontend-modal-review.md) | Catches the div-button, the missing focus trap, and the derived state that drifts |
| [Designing an invoices API](examples/backend-invoices-api.md) | Idempotency keys, cursor pagination, and a state machine — before you asked |
| [The revenue model that double-counted](examples/data-dbt-fanout.md) | Spots the join fanout that has inflated revenue since partial payments shipped — and treats the fix as a metric restatement |
| [Moving docs to a new domain without losing rankings](examples/seo-site-migration.md) | Builds the one-hop redirect map and schedules the 24h/7d/30d checkpoints |
| [Rewriting a README nobody could follow](examples/writer-readme-rewrite.md) | Five editing passes, applied visibly — accuracy first, hype deleted, prerequisites moved above the commands |

## Why a playbook and not a pasted prompt?

A prompt you paste evaporates when the session ends and competes with everything else in your `~/.claude`. A playbook is standing policy:

- **Isolated.** Each playbook runs in its own `CLAUDE_CONFIG_DIR`. Your daily setup, history, and permissions are untouched.
- **Persistent.** The same rules apply tomorrow, and next month, without re-pasting.
- **Concurrent.** Run `ap-sre` on an incident in one terminal while `ap-dba` reviews a migration in another — separate instances, separate histories.
- **Shareable.** A playbook is a directory in a git repo. Your whole team installs the same senior engineer.
- **Versioned.** `claude-playbook update dba` pulls improvements; your own forks evolve in git like any other code.

## Anatomy of a playbook

All eight roles follow the same four-part pattern. The pattern, more than the prose, is what makes them work:

1. **Identity** — one paragraph: who the model is and what it optimizes for. Not a costume; a job description.
2. **Intake** — what it must find out before prescribing. This is where "ask for the execution plan" and "ask who consumes the data" live. Intake is the single biggest quality lever: it converts guesses into diagnoses.
3. **Checklists and output formats** — the domain's craft, encoded as structures the model must fill in. A checklist is harder to skip than a paragraph of advice is to ignore.
4. **Red lines** — what it refuses to do even when asked nicely. These hold the role's shape under pressure.

A complete playbook is just two files. Here is a minimal, real one — a release captain:

```text
release-captain/
├── .playbook
└── CLAUDE.md
```

`.playbook`:

```toml
version = "1.0.0"
name = "release-captain"
alias = "capt"
description = "Runs software releases: preflight, go/no-go, rollout, rollback."
```

`CLAUDE.md`:

```markdown
# Release Captain

You run software releases. You optimize for boring deploys and fast, clean
rollbacks. You never celebrate a release until the verification step passes.

## Intake

Before any go/no-go call, establish: what is shipping (diff or changelog),
rollback mechanism and how long it takes, feature flags involved, migration
status, current error budget, and who is on call.

## Go / No-Go Format

Ship? (yes / no / yes-with-conditions)
Risk summary:
Preflight checks:
Rollout plan:
Verification (with owner and deadline):
Rollback trigger and command:

## Red Lines

- No release without a tested rollback path.
- No schema migration and dependent code in the same deploy.
- A missed verification deadline is an automatic rollback conversation.
```

Install it straight from the directory:

```bash
claude-playbook install ./release-captain
capt
```

## Build your own role here

Want a `mobile`, `ml`, `compliance`, or `platform` playbook in this collection?

1. Create `playbooks/<name>/CLAUDE.md` following the four-part pattern.
2. Add `playbooks/<name>/.playbook` with a unique `ap-` alias.
3. Add a worked example in `examples/`.
4. Run `python3 tests/validate.py` (Python 3.11+).
5. Open a PR.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full checklist and style rules.

## More playbooks

Playbooks go well beyond roles. Anything you can express as standing instructions plus configuration can be a playbook:

- [**Kommander**](https://github.com/ramazanpolat/kommander-playbook) — a full engineering-log operating system on top of Claude Code: folder-based tasks, session logs, guarded locks so concurrent instances can't corrupt each other's work, fork/switch/park operations, TODO and cron registries. The most advanced published playbook, and a good study in how far the format stretches.

Built or found a playbook worth listing? Open a PR and add it here.

## Install details

- **Individual roles** (recommended): install via GitHub tree URL as in the quick start, or the explicit form `claude-playbook install https://github.com/ramazanpolat/awesome-claude-playbooks --subdir playbooks/dba`, or from a local clone: `claude-playbook install ./awesome-claude-playbooks/playbooks/dba`.
- **The router**: `claude-playbook install https://github.com/ramazanpolat/awesome-claude-playbooks` installs only the root `awesome` playbook (alias `ap`). `claude-playbook` uses a flat model — the role directories under `playbooks/` ride along as ordinary files, not as discovered children. Install each role you want as its own playbook.
- **Updates**: `claude-playbook update dba` (or `awesome`, or any installed name). Roles update natively from recorded source metadata; the router ships a delegated git update script.
- **Validation**: `python3 tests/validate.py` checks every manifest, name, alias, and required file; CI runs it on every push.

## License

Apache-2.0 — see [LICENSE](LICENSE).
