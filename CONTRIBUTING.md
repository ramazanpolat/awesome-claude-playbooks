# Contributing

Three kinds of contributions are welcome:

1. **Improve an existing role** — sharpen a checklist, add a missing red line, fix an inaccuracy.
2. **Add a new role playbook** — `mobile`, `ml`, `compliance`, `platform`, or something we haven't thought of.
3. **List a community playbook** — built or found a playbook that stretches the format? Add it to the "More playbooks" section of the README.

## Adding a role playbook

A role is two files plus a worked example:

```text
playbooks/<name>/
├── .playbook      # manifest
└── CLAUDE.md      # the standing instructions
examples/<name>-<scenario>.md
```

### 1. The manifest

```toml
version = "1.0.0"
name = "<name>"          # must equal the directory name
alias = "ap-<short>"     # unique across the repo; ap- prefix
description = "<Role>: three to six words on what it covers."
```

### 2. The CLAUDE.md — follow the four-part pattern

Every role in this collection has the same skeleton. Match it:

1. **Identity** — one paragraph. Who the model is, what it optimizes for. A job description, not a costume ("You are a senior X. You help with A, B, C.").
2. **Intake** — what it must find out before prescribing. This is the highest-leverage section: the DBA asks for the execution plan, the data engineer asks for the grain, the writer asks for the audience. What does your role refuse to guess?
3. **Checklists and output formats** — the domain's craft as structures the model must fill in. Use fenced `text` blocks for output formats (`Finding: / Evidence: / ...`). Checklists beat prose: they are harder to skip.
4. **Red lines** — a `## Red Lines` section is mandatory. What does this role refuse to do even when asked nicely? Good red lines are specific and slightly uncomfortable ("Do not call anything 'low risk' without explaining the exposure"), not generic ("be careful").

Style:

- ATX headings, bullet lists, lowercase-with-dashes filenames.
- No emojis.
- Tool-agnostic where possible; when a default is needed, name it and say how to ask for alternatives (the DBA defaults to PostgreSQL but asks for the engine).
- Keep it under ~120 lines. A playbook is standing policy, not documentation — every line competes for the model's attention on every request.

### 3. The worked example

Every role needs one file in `examples/`: a realistic prompt, the abridged session it produces, and a short "What the playbook changed" section contrasting it with generic behavior. Model it on [examples/dba-slow-query.md](examples/dba-slow-query.md). The example must be consistent with the playbook's actual intake questions, output formats, and red lines — it is the role's specification by demonstration.

### 4. Wire it up

- Add a row to the README's "The collection" table (including the "Will not" column — quote a real red line).
- Add a row to "See them in action".

### 5. Validate

```bash
python3 tests/validate.py   # Python 3.11+
```

CI runs the same check on every push. It verifies manifests, name/directory agreement, alias uniqueness, required files, and the update script.

## PR checklist

- [ ] `python3 tests/validate.py` passes
- [ ] `CLAUDE.md` follows the four-part pattern and has a `## Red Lines` section
- [ ] Alias is unique and `ap-`-prefixed
- [ ] Worked example added under `examples/` and linked from the README
- [ ] README collection table updated
- [ ] No emojis, no trademarked or private material, no secrets

## Listing a community playbook

Add one bullet to "More playbooks" in the README: link, then one sentence on what it does and one on why it is interesting as a playbook (what it shows the format can do). Playbooks listed there must be public and installable via `claude-playbook install <url>`.
