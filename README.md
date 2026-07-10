# awesome-claude-playbooks

Ready-to-use role playbooks for [`claude-playbook`](https://github.com/ramazanpolat/claude-playbooks).

This repo installs as one parent playbook named `awesome` with focused child
playbooks for common engineering, operations, security, data, SEO, and writing
work. Each child has its own `CLAUDE.md`, so Claude Code starts with the right
working style, checklists, and output formats for the job.

## What's Included

| Playbook | Alias | Use it for |
| --- | --- | --- |
| `awesome` | `ap` | Router/overview. Helps pick the right role playbook. |
| `dba` | `ap-dba` | SQL review, schema design, indexes, migrations, backups, database incidents. |
| `sre` | `ap-sre` | Incident response, SLOs, observability, Kubernetes/cloud operations, postmortems. |
| `secops` | `ap-sec` | Defensive security review, threat models, vulnerability triage, hardening. |
| `frontend` | `ap-fe` | UI implementation, React/Vue/Svelte, accessibility, frontend performance. |
| `backend` | `ap-be` | API design, services, auth, queues, reliability, backend reviews. |
| `data` | `ap-data` | SQL analytics, dbt models, pipelines, warehouse design, data quality. |
| `seo` | `ap-seo` | Technical SEO audits, schema.org JSON-LD, content briefs, Core Web Vitals. |
| `writer` | `ap-write` | READMEs, API docs, runbooks, release notes, docs rewrites. |

## Install

Install the router overview playbook:

```bash
claude-playbook install https://github.com/ramazanpolat/awesome-claude-playbooks --name awesome --alias ap
```

Install individual role playbooks using the `--subdir` parameter:

```bash
claude-playbook install https://github.com/ramazanpolat/awesome-claude-playbooks --subdir playbooks/dba --name ap-dba --alias ap-dba
claude-playbook install https://github.com/ramazanpolat/awesome-claude-playbooks --subdir playbooks/sre --name ap-sre --alias ap-sre
# Repeat for secops, frontend, backend, data, seo, writer
```

Install from a local clone:

```bash
git clone https://github.com/ramazanpolat/awesome-claude-playbooks.git
claude-playbook install ./awesome-claude-playbooks/playbooks/dba --name ap-dba --alias ap-dba
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

Or use the full name:

```bash
claude-playbook run ap-fe
claude-playbook run ap-sec
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

Each directory acts as an independent, flat playbook with its own `.playbook` manifest. You can install them individually utilizing the `--subdir` parameter.

## Customize

Fork this repo and edit the `CLAUDE.md` files to match your team's stack,
incident process, style guide, and risk tolerance.

To add a new role playbook:

1. Create `playbooks/<name>/CLAUDE.md`.
2. Add `playbooks/<name>/.playbook`.

## License

MIT - see [LICENSE](LICENSE).
