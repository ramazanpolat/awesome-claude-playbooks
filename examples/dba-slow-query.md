# The slow query that wanted an index

Playbook: [`dba`](../playbooks/dba/CLAUDE.md) — alias `ap-dba`

A pagination query on a 48-million-row `orders` table has crept past two seconds. The interesting part is not the fix — it's that the playbook refuses to name one until it has evidence.

## Session (abridged)

**You:**

```text
This query got slow. Fix it:
SELECT * FROM orders WHERE customer_id = $1 ORDER BY created_at DESC LIMIT 20;
```

**ap-dba:**

> Before I recommend anything for production, I need:
>
> 1. Engine and version — I'll assume PostgreSQL until told otherwise.
> 2. The plan: `EXPLAIN (ANALYZE, BUFFERS, VERBOSE)` with a representative `customer_id`.
> 3. Row count and write rate for `orders` — any index I add taxes every insert.
> 4. Existing indexes on the table.
> 5. Is this production, and what latency does the product need?
>
> Working hypothesis: a composite index on `(customer_id, created_at DESC)` so the
> `ORDER BY ... LIMIT` becomes an index scan instead of a sort. Not confirmed until
> I see the plan.

**You:**

```text
PostgreSQL 15, production. ~48M rows, maybe 40 inserts/sec. Index on customer_id exists.

Limit  (cost=182734.12..182734.17 rows=20 width=482) (actual time=2140.334..2140.339 rows=20 loops=1)
  ->  Sort  (cost=182734.12..182813.90 rows=31912 width=482) (actual time=2140.332..2140.335 rows=20 loops=1)
        Sort Key: created_at DESC
        Sort Method: top-N heapsort  Memory: 58kB
        ->  Bitmap Heap Scan on orders  (cost=597.15..181884.65 rows=31912 width=482) (actual time=18.221..2094.117 rows=29817 loops=1)
              Recheck Cond: (customer_id = 48213)
              Rows Removed by Index Recheck: 3412890
              Heap Blocks: exact=41210 lossy=182664
              ->  Bitmap Index Scan on idx_orders_customer_id  (actual time=9.312..9.312 rows=29817 loops=1)
                    Index Cond: (customer_id = 48213)
Planning Time: 0.412 ms
Execution Time: 2140.522 ms
```

**ap-dba:**

> ```text
> Finding:
>   The existing index finds the customer's rows fast (9 ms), but the plan then
>   reads ~224k heap blocks to fetch 29,817 full rows and sorts them just to
>   keep 20. The bitmap is lossy (182,664 lossy blocks, 3.4M rows removed by
>   recheck), which means work_mem is too small for a bitmap this size — the
>   heap scan, not the index, is your 2 seconds.
>
> Evidence:
>   Bitmap Heap Scan actual time 2094 ms of 2140 ms total; lossy blocks +
>   "Rows Removed by Index Recheck"; top-N heapsort discarding 29,797 of
>   29,817 fetched rows.
>
> Impact:
>   Every page load for a large customer pays ~2.1 s and floods shared buffers
>   with heap pages it throws away.
>
> Recommendation:
>   Composite index matching both the predicate and the ordering, so Postgres
>   walks the customer's orders newest-first and stops after 20. The existing
>   single-column index becomes redundant — plan to drop it after verifying.
>
> SQL:
>   CREATE INDEX CONCURRENTLY idx_orders_customer_created
>     ON orders (customer_id, created_at DESC);
>   -- after validation, in a later change window:
>   -- DROP INDEX CONCURRENTLY idx_orders_customer_id;
>
> Validation:
>   Re-run EXPLAIN (ANALYZE, BUFFERS). Expect: Index Scan using
>   idx_orders_customer_created, no Sort node, rows=20, single-digit ms.
>   Check pg_stat_user_indexes before dropping the old index — confirm nothing
>   else scans it.
>
> Risk:
>   CONCURRENTLY avoids blocking writes but takes longer and briefly holds two
>   indexes' worth of write amplification (40 inserts/sec is comfortably fine).
>   If the build fails it leaves an INVALID index — check and drop it.
>   Separately: SELECT * fetches width=482 rows; a column list would shrink the
>   fetch, but that is an application change, not required for the win.
> ```

## What the playbook changed

- It did not prescribe on the first turn. The intake list — engine, plan, size, write rate, existing indexes — is mandated by the playbook before any production recommendation.
- It read the plan rather than pattern-matching the query: the diagnosis (lossy bitmap heap scan, sort discarding 99.9% of fetched rows) comes from the `BUFFERS` output it insisted on.
- The recommendation includes the unglamorous parts a hallway answer skips: `CONCURRENTLY`, the INVALID-index failure mode, dropping the now-redundant index only after checking `pg_stat_user_indexes`, and the write-amplification cost stated against the actual insert rate.
- The answer arrives in the playbook's required `Finding / Evidence / Impact / Recommendation / SQL / Validation / Risk` shape — skimmable by a reviewer who wasn't in the session.

## Run it

```bash
claude-playbook install https://github.com/ramazanpolat/awesome-claude-playbooks/tree/main/playbooks/dba
ap-dba
```
