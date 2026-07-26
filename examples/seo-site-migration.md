# Moving docs to a new domain without losing rankings

Playbook: [`seo`](../playbooks/seo/CLAUDE.md) — alias `ap-seo`

A subdomain-to-path migration — the kind that silently costs sites a third of their organic traffic when a redirect map is an afterthought. The playbook runs its migration checklist and schedules the follow-up before launch, not after the traffic graph dips.

## Session (abridged)

**You:**

```text
We're moving docs.example.com to example.com/docs next Thursday. About 1,400
pages, Next.js on Vercel, we have Search Console for both. What do we do so
rankings survive?
```

**ap-seo:**

> Three intake points that change the plan: does the URL *path structure*
> change too, or only the host? Do any docs pages have external backlinks you
> know of (they get priority in the redirect map)? And is staging currently
> behind noindex or robots disallow? Assuming host-only change until you say
> otherwise — here is the plan.
>
> **Before launch (this week):**
>
> 1. **URL inventory.** Union of: full crawl of docs.example.com, Search
>    Console (both Performance pages and Coverage), analytics top pages, and
>    server logs if reachable. The crawl alone misses orphan pages that only
>    Google still remembers — those 404 loudest after launch.
> 2. **Redirect map: one hop, 1:1.** `docs.example.com/<path>` →
>    `301 example.com/docs/<path>`. Not to the docs home, not via an interim
>    redirect. On Vercel this is one host-level rule if paths are preserved —
>    verify with 20 spot checks including query strings and trailing slashes.
> 3. **The staging trap (check this twice).** Staging for example.com/docs is
>    presumably noindexed or robots-blocked. The classic migration killer is
>    shipping that noindex/meta-robots or the staging robots.txt to
>    production. Make "no noindex, robots allows /docs" an explicit launch
>    checklist item, verified *in production* at T+5 minutes.
> 4. **Internal links and canonicals.** Update in-app links, sitemaps, and
>    canonical tags to the new URLs — do not rely on redirects to clean up
>    internal traffic. Old sitemap stays live temporarily (see below).
>
> **Launch day:**
>
> - Deploy redirects and the new site together; spot-check the top-50 pages.
> - Submit the new sitemap under example.com in Search Console; keep the old
>   sitemap accessible so Google recrawls old URLs and sees the 301s faster.
>   (Change of Address in GSC does not apply to subdomain→path moves; both
>   properties just stay verified.)
>
> **Checkpoints — put these in the calendar now:**
>
> - **24h:** logs/GSC for 404s on old URLs (holes in the map); confirm
>   production /docs is indexable; redirect spot checks from a clean network.
> - **7d:** GSC Coverage for the new prefix rising, old subdomain falling;
>   compare top-100 query clicks week-over-week.
> - **14d:** hunt redirect *chains* (old URL → new URL → moved-again URL);
>   flatten to one hop.
> - **30d:** traffic parity check. Expect turbulence for 2–6 weeks on a move
>   this size; investigate only pages down >20% vs pre-migration baseline,
>   starting with backlinked ones.
>
> To be clear on expectations: done right this usually recovers fully, but I
> can't guarantee rankings — nobody honestly can. What I can guarantee is that
> every lost page will be visible in the 24h/7d checkpoints while it is still
> cheap to fix.

## What the playbook changed

- The URL inventory comes from four sources, not a crawl — the playbook's migration checklist knows orphan pages that only the index remembers are the ones that 404 after launch.
- One-hop 1:1 redirects are stated as a requirement with verification steps, and the 14-day checkpoint explicitly hunts the chains that accrete anyway.
- The staging noindex trap — the single most common self-inflicted migration wound — is a named launch-checklist item verified in production, because the playbook's audit order starts at crawlability/indexability, not content.
- Monitoring is scheduled before launch with concrete things to look at per checkpoint. And per its red lines, it corrected the question's premise instead of promising rankings.

## Run it

```bash
claude-playbook install https://github.com/ramazanpolat/awesome-claude-playbooks/tree/main/playbooks/seo
ap-seo
```
