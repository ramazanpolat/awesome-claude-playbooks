# Threat-modeling a password reset flow

Playbook: [`secops`](../playbooks/secops/CLAUDE.md) — alias `ap-sec`

A three-sentence feature description goes in; a structured STRIDE threat model comes out — including the two findings teams most often miss: the user-enumeration timing leak and the logged-in sessions that survive a reset.

## Session (abridged)

**You:**

```text
Threat-model our new password reset. Flow: user enters email, we send a link
with a token, link opens a form, user sets a new password. Token expires in
24 hours. Focus on abuse cases and concrete controls.
```

**ap-sec:**

> Three questions first, because they change the model: is the token stored
> hashed or plaintext? Is it single-use? And does a successful reset invalidate
> existing sessions? I'll model with the risky defaults assumed and mark where
> your answers change the picture.
>
> ```text
> System:
>   Email-based password reset for the main web app.
>
> Assets:
>   Account takeover capability (the reset token IS the account while valid),
>   user email addresses (enumeration target), password database.
>
> Actors:
>   Legitimate user, attacker with target's email, attacker with a list of
>   emails (credential-stuffing prep), attacker with mailbox access.
>
> Trust boundaries:
>   Browser -> app (request form, reset form); app -> email provider;
>   email inbox itself (outside your control).
>
> Entry points:
>   POST /password-reset/request, GET/POST /password-reset/confirm?token=...
>
> Threats (STRIDE, top findings):
>   [S] Account takeover via token: 24h is long for an inbox-resident
>       credential. Forwarded emails, shared inboxes, and mail scanners all
>       see the link.
>   [I] User enumeration: if "email not found" and "email sent" differ in
>       response body, status, or timing (sending is slower than not sending),
>       the endpoint is an oracle for valid accounts.
>   [S] Host-header/link injection: if the reset URL is built from the request
>       Host header, an attacker can request a reset for the victim and
>       receive the token when the victim clicks a poisoned link.
>   [T] Token replay: a non-single-use token turns one interception into
>       standing access.
>   [S] Surviving sessions: resetting the password without killing existing
>       sessions locks the attacker IN, not out — the #1 miss in real
>       incidents where reset is the recovery step.
>   [D] Email bombing: an unthrottled request endpoint lets anyone flood a
>       victim's inbox and your sending reputation.
>
> Controls:
>   - Token: >=128 bits from a CSPRNG, stored hashed, single-use, 15-30 min
>     expiry. 24h is a red flag — shorten it.
>   - Uniform response: same body, status, and comparable timing whether or
>     not the email exists (queue the send; don't send inline).
>   - Build reset URLs from configured base URL, never the Host header.
>   - On success: invalidate all sessions and refresh tokens, require fresh
>     login, notify the account email ("your password was changed").
>   - Rate limit per-account and per-IP on the request endpoint.
>   - Log request + confirm events with IP/UA for detection; never log tokens.
>
> Residual risk:
>   Mailbox compromise defeats any email-based reset — that is an accepted
>   risk of the channel; MFA-gated reset raises the bar if warranted.
>
> Open questions:
>   Token storage (hashed?), single-use (?), session invalidation (?), and
>   whether password managers/SSO users need this flow at all.
> ```

## What the playbook changed

- The output is the playbook's mandated threat-model structure, so nothing is silently skipped — every model it produces has trust boundaries, residual risk, and open questions, not just a scary list.
- It caught the two findings that dominate real-world reset incidents: the enumeration oracle (including the *timing* variant, not just differing messages) and session survival after reset.
- Controls are concrete enough to file as tickets — bit-length, hashing at rest, expiry window, uniform-response tactic — not "use secure tokens".
- Its red lines keep it defensive: it will model abuse of your own system all day, but asking it to attack someone else's reset flow gets a refusal and a redirect to detection and hardening. It also refuses to write "low risk" without stating the exposure and assumptions.

## Run it

```bash
claude-playbook install https://github.com/ramazanpolat/awesome-claude-playbooks/tree/main/playbooks/secops
ap-sec
```
