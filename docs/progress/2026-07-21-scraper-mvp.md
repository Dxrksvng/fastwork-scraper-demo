# 2026-07-21 — Scraper MVP

**What changed**
- `src/scraper.py` — three separated concerns (fetch / parse / paginate) + orchestrator + writer
- `tests/test_scraper.py` — 9 tests against a saved HTML fixture, no live network
- `tests/fixtures/listing.html` — mini snapshot with a deliberately-malformed card to test skip logic
- `docs/decisions/0001-target-choice.md` — ADR: demo target = books.toscrape.com, real Thai targets to consider per engagement
- `examples/sample.csv` — 10-row preview of a real run

**Why**
Ship a working MVP that proves the pattern (static HTML → clean CSV) against a legally-clean target. Real Fastwork gigs will adapt selectors + config per client.

**What's affected**
Nothing outside this repo.

**Verify**
- `uv run pytest` → 9 passed
- `uv run python -m src.scraper` → 60 rows to `data/output/products.csv`
- Encoding fix (`resp.apparent_encoding`) applied after initial run showed `Â£` mojibake

**What's next**
- Aim clip 60–90s: run scraper, open CSV in Excel, show clean rows
- Consider adding retry-with-backoff on transient 5xx (currently stops on first failure)
- Adapt to Thai target per first paying client
