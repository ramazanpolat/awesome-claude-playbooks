# The revenue model that double-counted

Playbook: [`data`](../playbooks/data/CLAUDE.md) — alias `ap-data`

A dbt mart that has quietly inflated revenue since the day partial payments shipped. The playbook's first question — "what is the grain?" — is the one that finds it, and its red lines turn the fix into a communicated metric restatement instead of a silent Tuesday deploy.

## Session (abridged)

**You:**

````text
Finance says our revenue dashboard reads high. Review this dbt model:

```sql
-- models/marts/fct_revenue.sql
select
    o.order_id,
    o.customer_id,
    o.ordered_at::date as order_date,
    p.amount as revenue
from {{ ref('stg_orders') }} o
join {{ ref('stg_payments') }} p on p.order_id = o.order_id
where o.status = 'completed'
```
````

**ap-data:**

> Two questions before the verdict: can one order have multiple payments
> (partial payments, retries, refunds as negative rows)? And what is this
> model's intended grain — one row per order, or per payment?

**You:**

```text
Partial payments shipped in March, so yes — multiple rows per order in
stg_payments. Refunds are separate negative-amount rows. Intended grain is
one row per order. Warehouse is Snowflake, dashboard sums revenue by order_date.
```

**ap-data:**

> ```text
> Model grain:
>   Declared: one row per order. Actual: one row per (order, payment) — the
>   join fans out every multi-payment order. Finance is right: any order paid
>   in N installments appears N times, and its full row context with it.
>   Since refunds are separate rows, `p.amount` here is also gross, not net.
>
> Problems:
>   1. Fanout: join to stg_payments multiplies order rows. Sum(revenue) is
>      inflated by exactly the multi-payment orders since March.
>   2. Revenue is gross-of-refunds — negative rows only partially and
>      accidentally offset, depending on refund timing vs order status.
>   3. `ordered_at::date` — naive truncation. Confirm warehouse TZ vs
>      finance's reporting TZ (UTC truncation shifts late-evening orders to
>      the next day for most US/EU zones).
>   4. No tests would have let this in silently: a unique test on order_id
>      fails the moment the first partial payment lands.
>
> Tests to add:
>   - unique + not_null on order_id (fct_revenue)
>   - relationships: fct_revenue.order_id -> stg_orders.order_id
>   - accepted_values on stg_orders.status
>   - dbt_utils.expression_is_true: revenue_net >= 0 or documented-negative
>
> Documentation to add:
>   Model description declaring the grain in one sentence; column docs for
>   revenue_gross vs revenue_net; note the March partial-payments change.
>
> SQL changes:
>   Pre-aggregate payments to order grain, then join:
>
>   with payments as (
>       select
>           order_id,
>           sum(amount) as revenue_net,
>           sum(iff(amount > 0, amount, 0)) as revenue_gross
>       from {{ ref('stg_payments') }}
>       group by order_id
>   )
>   select
>       o.order_id, o.customer_id,
>       o.ordered_at::date as order_date,   -- pending TZ decision
>       p.revenue_net, p.revenue_gross
>   from {{ ref('stg_orders') }} o
>   join payments p on p.order_id = o.order_id
>   where o.status = 'completed'
>
> Backfill/rollout:
>   This is a metric restatement, not a bug fix — March-to-today numbers will
>   drop, and finance may have reported the old ones. Do not ship silently:
>   1. Quantify: run old vs new side by side, get the monthly deltas.
>   2. Tell finance the number and the date range before merging.
>   3. Full-refresh the model (it is not incremental; cost is one rebuild).
>   4. Merge with the tests above so the class of error cannot recur.
> ```

## What the playbook changed

- Grain first: the playbook's standing rule — state the grain of every model — is precisely the question that exposes a fanout. Generic SQL review comments on style; this one asked what a row *means*.
- It asked about payment cardinality and refund representation before judging, so the diagnosis ("inflated by exactly the multi-payment orders since March") is specific, not hypothetical.
- The fix pre-aggregates to the declared grain and splits gross from net — and the missing `unique` test is called out as the guard that would have caught it on day one.
- Its red line — never change a metric definition without a migration and communication plan — turned the rollout section into "quantify the delta and tell finance first", which is the difference between fixing a dashboard and torching its credibility.

## Run it

```bash
claude-playbook install https://github.com/ramazanpolat/awesome-claude-playbooks/tree/main/playbooks/data
ap-data
```
