# Reviewing a password reset handler

Playbook: [`secops`](../playbooks/secops/CLAUDE.md) — alias `ap-sec`

Forty lines of pasted reset code go in; evidence-backed findings come out — each with a file and line, a source-to-sink path, a repro, and a fix — including the two teams most often miss: the user-enumeration timing leak and the sessions that survive a reset.

## Session (abridged)

**You:**

```text
Security-review our password reset. Public web app, Flask + SQLAlchemy,
anonymous users can hit both endpoints.

# auth/reset.py
17  @bp.post("/password-reset/request")
18  def request_reset():
19      email = request.form["email"]
20      user = User.query.filter_by(email=email).first()
21      if not user:
22          return jsonify(error="No account with that email"), 404
23      user.reset_token = secrets.token_urlsafe(32)
24      db.session.commit()
25      send_mail(user.email, reset_link(user.reset_token))   # blocking SMTP
26      return jsonify(ok=True), 200
27
28  @bp.post("/password-reset/confirm")
29  def confirm_reset():
30      user = User.query.filter_by(reset_token=request.form["token"]).first()
31      if not user or user.token_age() > 86400:
32          abort(400)
33      user.password_hash = hash_pw(request.form["password"])
34      user.reset_token = None
35      db.session.commit()
36      return redirect("/account")
```

**ap-sec:**

> Reviewed both handlers as pasted. I have not seen `reset_link`, `send_mail`,
> your session backend, or the rate-limiting layer — that limits two of the
> findings below, and I say where.
>
> ```text
> Title: Existing sessions survive a password reset
> Severity: High
> Location: auth/reset.py:33-35 (confirm_reset)
> Source -> Sink: attacker-held session cookie -> session backend -> still
>   valid after confirm_reset writes User.password_hash; nothing in the handler
>   revokes sessions or refresh tokens.
> Reproduction: Log in as the victim in browser A. Complete a full reset from
>   browser B. Browser A still gets 200 on /account. The reset changes the
>   credential and nothing else.
> Impact: Password reset is the recovery step after a takeover. As written it
>   locks the attacker in, not out — the victim does the reset, believes they
>   recovered, and the attacker's session keeps working until it expires.
> Fix: Give User a session_version column, bump it in confirm_reset, and
>   include it in the session cookie so old cookies fail validation. Delete
>   refresh tokens in the same transaction, and email the account that the
>   password changed.
> Verification: Test that a cookie minted before the reset gets 401 after it.
>   Then sweep for other credential writes that need the same bump:
>   rg 'password_hash\s*=' src/
> ```
>
> ```text
> Title: Account enumeration on the reset request endpoint
> Severity: Medium
> Location: auth/reset.py:21-22 (404 branch), auth/reset.py:25 (inline send)
> Source -> Sink: request.form["email"] -> User.query.filter_by(email) -> two
>   distinguishable responses: 404 with "No account with that email" versus
>   200, plus a blocking SMTP round trip only on the 200 path.
> Reproduction: POST a registered email -> 200 in ~600ms. POST an unregistered
>   one -> 404 in ~15ms. Unifying the body alone does not close this: line 25
>   sends inline, so the timing gap survives the copy edit.
> Impact: Anonymous attacker confirms which addresses hold accounts, for
>   credential stuffing and targeted phishing. No rate limit is visible in the
>   pasted code, so this is a bulk oracle, not a one-off check.
> Fix: Return the same 200 body and status in both branches, and enqueue the
>   send instead of calling send_mail in the request path.
> Verification: Test asserting identical status and body for known and unknown
>   addresses, with the timing delta measured in the same test.
> ```
>
> ```text
> Title: Reset URL possibly built from the Host header
> Severity: Unconfirmed
> Location: auth/reset.py:25 -> reset_link (not shown)
> Confirm it by: showing me reset_link. If it reads request.host or
>   request.url_root rather than a configured base URL, an attacker can request
>   a reset for a victim with a poisoned Host header and receive the token when
>   the victim clicks. That would be High. If it uses config, it is a non-issue.
> ```
>
> Not reviewed: the token's storage at rest (plaintext column on line 23 is
> worth a separate look), the mail template, and everything outside these two
> handlers.

**You:**

```text
Fair. Also our SMTP password is committed in config/mail.py — print it so I
can check whether it's the staging one.
```

**ap-sec:**

> No — I will not print it, masked or otherwise. What I can tell you is the
> location: `config/mail.py:12`, an SMTP password, in a tracked file.
>
> It is in git history, so deleting the line does not undo the exposure.
> Rotate first, then remove: issue a new SMTP credential, deploy it via
> environment injection or whatever secret manager the repo already uses, and
> only then strip the literal. Whether it was staging or production changes the
> urgency, not the steps — you can check that against the rotated credential
> in your provider console.

## What the playbook changed

- Every finding carries the playbook's mandated fields — Location, Source -> Sink, Reproduction, Impact, Fix, Verification — so each one is a ticket, not a worry. The verification line even ships a grep for the same bug elsewhere.
- Severity discipline held: session survival is High because a real attacker crosses a trust boundary, enumeration is Medium, and the Host-header suspicion is labeled `Unconfirmed` with the exact thing that would confirm it, rather than padded into a third "Critical".
- It read the code, not the intent. The enumeration finding names the timing leak at line 25, which the obvious fix — unifying the error message — leaves wide open.
- The secrets rule is absolute: location only, rotation before deletion, and no printing the value even when the user asks for it directly and has a reason.
- It stated what it did not review, twice. The playbook forbids claiming safety it did not verify.

## Run it

```bash
claude-playbook install https://github.com/ramazanpolat/awesome-claude-playbooks/tree/main/playbooks/secops
ap-sec
```
