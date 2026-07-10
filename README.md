# awesome-claude-playbooks

Ready-to-use role playbooks for [`claude-playbook`](https://github.com/ramazanpolat/claude-playbooks).

This repository contains an overview/router playbook plus eight independently
installable role playbooks for engineering, operations, security, data, SEO,
and writing work.

`claude-playbook` uses a flat model: installing the repository root creates only
the `awesome` router. Directories under `playbooks/` are ordinary files in that
installation, not automatically discovered children. Install each role you want
as its own playbook using a GitHub tree URL or `--subdir`.

## What's Included

| Playbook name | Default alias | Use it for |
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
claude-playbook install https://github.com/ramazanpolat/awesome-claude-playbooks
```

Install individual roles directly. Their manifests provide the playbook name
and default alias, so overrides are unnecessary:

```bash
claude-playbook install https://github.com/ramazanpolat/awesome-claude-playbooks/tree/main/playbooks/dba
claude-playbook install https://github.com/ramazanpolat/awesome-claude-playbooks/tree/main/playbooks/sre
# Repeat for secops, frontend, backend, data, seo, writer
```

The equivalent explicit form is:

```bash
claude-playbook install https://github.com/ramazanpolat/awesome-claude-playbooks --subdir playbooks/dba
```

Install from a local clone:

```bash
git clone https://github.com/ramazanpolat/awesome-claude-playbooks.git
claude-playbook install ./awesome-claude-playbooks/playbooks/dba
```

Update later:

```bash
claude-playbook update awesome
claude-playbook update dba
```

The router ships a delegated Git update script. Individually installed roles
use the source metadata recorded by `claude-playbook` for native updates.

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
claude-playbook run frontend
claude-playbook run secops
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

The repository root and every `playbooks/<role>` directory are valid independent
playbook sources with their own manifest and `CLAUDE.md`. Install role directories
individually; nesting them in this repository does not create runtime hierarchy.

## Customize

Fork this repo and edit the `CLAUDE.md` files to match your team's stack,
incident process, style guide, and risk tolerance.

To add a new role playbook:

1. Create `playbooks/<name>/CLAUDE.md`.
2. Add `playbooks/<name>/.playbook`.

Validate manifests, names, aliases, required files, and update-script permissions
with Python 3.11 or newer:

```bash
python3 tests/validate.py
```

## License

Apache-2.0 - see [LICENSE](LICENSE).
