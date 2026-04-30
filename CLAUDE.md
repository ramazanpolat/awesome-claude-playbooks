# awesome-playbooks

You are operating in the **awesome** playbook — the umbrella entry point for a
collection of role-focused Claude Code playbooks. Most real work happens inside
one of the child playbooks (`awesome/dba`, `awesome/sre`, `awesome/seo`,
`awesome/secops`, `awesome/frontend`, `awesome/backend`, `awesome/data`,
`awesome/writer`).

## When the user lands here

- They probably want one of the children. If their question is clearly
  role-specific, suggest the matching child playbook by name and the alias
  they can use to launch it directly (e.g. `ap-dba`, `ap-sre`).
- If they want a quick overview of what's available, list the children and
  one-line descriptions from `.playbook` rather than re-deriving them.

## Conventions

- Every child has its own `CLAUDE.md`. Defer to it when a child's domain is in
  scope — its instructions are more specific than this file.
- The repo is a *demonstration* of the multi-playbook layout described in
  `SPEC-v2.1-draft-3.md`. The CLAUDE.md content is intentionally lightweight;
  fork the repo and replace it with your own house rules.
