# ADR 0001 — Target site for the demo

**Date**: 2026-07-21
**Status**: Accepted

## Context

The Fastwork market for scraping work in Thailand is dominated by e-commerce competitor price monitoring (Shopee, Lazada, JD Central), followed by real estate (DDproperty, Baania) and job listings (JobsDB). These are the highest-value scraping gigs SME actually pay for.

But **demoing directly against those sites is unsafe**:
- Shopee/Lazada ToS explicitly prohibit automated scraping
- All three deploy Cloudflare / anti-bot / JS-rendered content — `requests + BeautifulSoup` won't work anyway
- A public demo scraping those sites signals to prospective clients that we ignore legal boundaries — the wrong first impression

## Decision

Demo target = **`books.toscrape.com`**.

Reasons:
- Explicitly created as a legal scraping sandbox — no ToS or robots.txt issues
- Static HTML — proves the `requests + BeautifulSoup` pattern works
- Structure (product cards, price, pagination) mirrors real e-commerce sites — same code, same shape

The value proposition shown to a Fastwork prospect is "we handle static-HTML product listings, delivered as clean CSV/Excel." The demo proves the pattern. The real gig adapts selectors + config to the client's target.

## What we do NOT commit to

We do NOT demo scraping Shopee/Lazada or any site with an anti-scraping ToS clause. If a prospect asks for that specifically, respond honestly:
1. "Their ToS prohibits it — using it publicly would put both of us at risk."
2. Offer alternatives: their own competitor's public catalog page, marketplace APIs (Lazada/Shopee have official partner APIs with different terms), price aggregators that publish permissive data.

## Real-world Thai targets to consider per client engagement

Rank by legal cleanliness (highest first):

| Target | Value | Legal posture | Difficulty |
|---|---|---|---|
| `data.go.th` (open data) | high for research/BI clients | ✅ explicit public use | static, easy |
| SET listed-company disclosures | high for finance | ✅ public disclosure | mostly static |
| DBD company registration lookup | high for B2B lead-gen | ✅ public record | per-record lookup, slow |
| Small independent Thai e-commerce (JIB, Advice, Powerbuy) | high for price monitoring | ⚠️ verify robots.txt case-by-case | static |
| Real estate (DDproperty, Kaidee) | high for real-estate agents | ⚠️ ToS ambiguous | JS-rendered, needs Playwright |
| Shopee / Lazada / JD Central | highest | ❌ ToS prohibits | JS + anti-bot |

Rule: **always run `curl <site>/robots.txt` before quoting the job**. If any Disallow covers the target path, decline or negotiate an alternative.

## Consequences

- Public demo repo shows a legally-clean scrape, which is the honest signal we want to send.
- We can pivot to a client's specific target during scoping without rewriting the code — only selectors and pagination logic change.
- We lose "demo already scrapes Shopee" as a sales hook. Acceptable — that hook attracts the wrong clients anyway.
