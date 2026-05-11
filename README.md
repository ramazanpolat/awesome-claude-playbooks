# awesome-playbooks

Ready-to-use role playbooks for [`claude-playbook`](https://github.com/ramazanpolat/claude-playbooks).

This repo installs as one parent playbook named `awesome` with focused child
playbooks for common engineering, operations, security, data, SEO, and writing
work. Each child has its own `CLAUDE.md`, so Claude Code starts with the right
working style, checklists, and output formats for the job.

## What's Included

| Playbook | Alias | Use it for |
| --- | --- | --- |
| `awesome` | `ap` | Router/overview. Helps pick the right child playbook. |
| `awesome/dba` | `ap-dba` | SQL review, schema design, indexes, migrations, backups, database incidents. |
| `awesome/sre` | `ap-sre` | Incident response, SLOs, observability, Kubernetes/cloud operations, postmortems. |
| `awesome/secops` | `ap-sec` | Defensive security review, threat models, vulnerability triage, hardening. |
| `awesome/frontend` | `ap-fe` | UI implementation, React/Vue/Svelte, accessibility, frontend performance. |
| `awesome/backend` | `ap-be` | API design, services, auth, queues, reliability, backend reviews. |
| `awesome/data` | `ap-data` | SQL analytics, dbt models, pipelines, warehouse design, data quality. |
| `awesome/seo` | `ap-seo` | Technical SEO audits, schema.org JSON-LD, content briefs, Core Web Vitals. |
| `awesome/writer` | `ap-write` | READMEs, API docs, runbooks, release notes, docs rewrites. |

## Install

Install the full bundle:

```bash
claude-playbook install https://github.com/ramazanpolat/awesome-playbooks --alias-all
```

That creates the parent alias `ap` plus child aliases such as `ap-dba`,
`ap-sre`, and `ap-fe`.

Install only one child:

```bash
claude-playbook install https://github.com/ramazanpolat/awesome-playbooks/tree/main/playbooks/dba
```

Install from a local clone:

```bash
git clone https://github.com/ramazanpolat/awesome-playbooks.git
claude-playbook install ./awesome-playbooks --alias-all
```

Update later:

```bash
claude-playbook update awesome
```

## Use

Launch by alias:

```bash
ap          # overview/router
ap-dba      # database work
ap-sre      # reliability and incidents
ap-sec      # defensive security
ap-fe       # frontend
ap-be       # backend
ap-data     # data engineering / analytics
ap-seo      # SEO
ap-write    # technical writing
```

Or use the long form:

```bash
claude-playbook run awesome/frontend
claude-playbook run awesome/secops
```

## Good First Prompts

DBA:

```text
Review this PostgreSQL query for production performance. Ask for anything you need before recommending indexes.
```

SRE:

```text
We have elevated 5xx on checkout. Act as incident commander and give the next 10 minutes of triage.
```

SecOps:

```text
Threat-model this new password reset flow. Focus on abuse cases and concrete controls.
```

Frontend:

```text
Review this component for accessibility, state management, and unnecessary client-side JavaScript.
```

Backend:

```text
Design a production-ready REST API for invoices, including errors, idempotency, pagination, and observability.
```

Data:

```text
Review this dbt model and propose tests, documentation, and grain fixes.
```

SEO:

```text
Create a technical SEO audit checklist for this site before a migration.
```

Writer:

```text
Rewrite this README so a developer can install, verify, and troubleshoot the tool in under five minutes.
```

## Layout

```text
.
├── .playbook
├── CLAUDE.md
├── README.md
├── bin/
│   └── update-playbook.sh
└── playbooks/
    ├── backend/
    │   ├── .playbook
    │   └── CLAUDE.md
    ├── data/
    ├── dba/
    ├── frontend/
    ├── secops/
    ├── seo/
    ├── sre/
    └── writer/
```

The root `.playbook` declares every child. Each child also has its own
`.playbook`, so it can be installed independently with a GitHub `/tree/...`
URL.

## Customize

Fork this repo and edit the `CLAUDE.md` files to match your team's stack,
incident process, style guide, and risk tolerance.

To add a child:

1. Create `playbooks/<name>/CLAUDE.md`.
2. Add `playbooks/<name>/.playbook`.
3. Add a `[[children]]` entry to the root `.playbook`.

Example:

```toml
[[children]]
name = "mobile"
path = "playbooks/mobile"
alias = "ap-mobile"
description = "Mobile engineer: iOS, Android, React Native, release quality."
```

## License

MIT - see [LICENSE](LICENSE).
