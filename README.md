# awesome-playbooks

A reference **multi-playbook** repository for [`claude-playbook`][spec] — the
CLI for managing isolated Claude Code instances.

This repo is a working example of the layout described in
[`SPEC-v2.1-draft-3.md`](SPEC-v2.1-draft-3.md): a top-level playbook that
declares several role-focused child playbooks under `playbooks/`. Use it as
a template when building your own multi-playbook tree.

## What's inside

| Playbook          | Alias       | Purpose                                                     |
| ----------------- | ----------- | ----------------------------------------------------------- |
| `awesome`         | `ap`        | Umbrella entry point — points users at the right child.     |
| `awesome/dba`     | `ap-dba`    | Database administration: schemas, queries, migrations.      |
| `awesome/sre`     | `ap-sre`    | Site reliability: incidents, observability, postmortems.    |
| `awesome/seo`     | `ap-seo`    | SEO audits, structured data, Core Web Vitals.               |
| `awesome/secops`  | `ap-sec`    | Defensive security: threat modeling, code review, triage.   |
| `awesome/frontend`| `ap-fe`     | Frontend engineering: TypeScript, a11y, performance.        |
| `awesome/backend` | `ap-be`     | Backend engineering: APIs, services, observability.         |
| `awesome/data`    | `ap-data`   | Data engineering: warehouse modeling, dbt, SQL.             |
| `awesome/writer`  | `ap-write`  | Technical writing: docs, READMEs, release notes.            |

Each child has its own `CLAUDE.md` with role-specific defaults and a
companion `.playbook` so it can also be cherry-pick installed on its own.

## Install

### Tree install (recommended)

Install the whole repo and all of its children at once:

```bash
claude-playbook install https://github.com/<owner>/awesome-playbooks
```

That gives you the umbrella alias `ap`. To also create per-child aliases
(`ap-dba`, `ap-sre`, …) in your shell config:

```bash
claude-playbook install https://github.com/<owner>/awesome-playbooks --alias-all
```

### Cherry-pick a single child

If you only want one role's playbook, install it standalone:

```bash
claude-playbook install https://github.com/<owner>/awesome-playbooks/tree/main/playbooks/dba
```

This installs as a flat top-level playbook named `dba` with alias `ap-dba`.

### Local install

If you've cloned the repo:

```bash
claude-playbook install ~/DEV/awesome-playbooks --alias-all
```

## Usage

After install, launch any playbook by its alias:

```bash
ap          # the umbrella
ap-dba      # the DBA child
ap-sre      # the SRE child
# …etc
```

Or via the long form:

```bash
claude-playbook run awesome
claude-playbook run awesome/dba
```

## Layout

```
.
├── .playbook                    ← root manifest, declares [[children]]
├── CLAUDE.md                    ← instructions for the umbrella playbook
├── README.md                    ← this file
├── SPEC-v2.1-draft-3.md         ← the claude-playbook spec
├── bin/
│   └── update-playbook.sh       ← invoked by `claude-playbook update awesome`
└── playbooks/
    ├── dba/{.playbook,CLAUDE.md}
    ├── sre/{.playbook,CLAUDE.md}
    ├── seo/{.playbook,CLAUDE.md}
    ├── secops/{.playbook,CLAUDE.md}
    ├── frontend/{.playbook,CLAUDE.md}
    ├── backend/{.playbook,CLAUDE.md}
    ├── data/{.playbook,CLAUDE.md}
    └── writer/{.playbook,CLAUDE.md}
```

The root `.playbook` is the source of truth for which children exist —
filesystem walking is intentionally not used for child discovery (see
the spec, "Playbook discovery").

## Updating

Once installed, the included `bin/update-playbook.sh` lets you pull the
latest version with:

```bash
claude-playbook update awesome
```

It runs `git pull --ff-only` against the install directory.

## Forking this repo

This is a **demonstration** template. The CLAUDE.md content for each child
is intentionally lightweight — fork it, replace the role guidance with your
own house rules, and publish your own multi-playbook tree.

To add a new child playbook:

1. Create the directory under `playbooks/<name>/`.
2. Add a `CLAUDE.md` (and optionally a `.playbook` so the child can be
   cherry-pick installed).
3. Add a `[[children]]` entry in the root `.playbook`:
   ```toml
   [[children]]
   name = "<name>"
   path = "playbooks/<name>"
   alias = "ap-<name>"
   description = "<one-liner>"
   ```

That's it. There is no registry, no index file, and no install step —
the root `.playbook` is the only source of truth.

## License

MIT — see [LICENSE](LICENSE).

[spec]: SPEC-v2.1-draft-3.md
