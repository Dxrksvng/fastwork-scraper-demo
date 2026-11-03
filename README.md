<div align="center">

# Fastwork Scraper Demo

**Clean product and price data from public pages, exported to CSV or Excel.**

![Python 3.11+](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white) ![Tests pytest](https://img.shields.io/badge/Tests-pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white) ![Lint ruff](https://img.shields.io/badge/Lint-ruff-D7FF64?style=for-the-badge&logo=ruff&logoColor=white) ![License All Rights Reserved](https://img.shields.io/badge/License-All_Rights_Reserved-lightgrey?style=for-the-badge)

</div>

> A portfolio demo that scrapes publicly available listing pages. Respect each site's terms and robots.txt before pointing it at a target.

## Tech stack

<p align="center">
  <img src="https://skillicons.dev/icons?i=py,pandas&perline=10" alt="Tech stack" />
</p>

## How it works

```mermaid
flowchart LR
    ENV[".env\ntarget URL, user agent"] --> M["main()"]
    M --> F["fetch_html\nrequests, apparent_encoding"]
    F --> P["parse_products\nBeautifulSoup -> Product"]
    P --> N{"find_next_page"}
    N -- "next page" --> F
    N -- "last page" --> W["write_output\npandas"]
    W --> C[("CSV / Excel")]
```

### Design

Three concerns stay separate so each is testable alone: `fetch_html` (network only), `parse_products` (HTML to objects, skips malformed cards, never raises) and `find_next_page` (pagination). Only `main()` reads environment variables.

---

Web scraper demo — clean product/price data from public sources exported to CSV/Excel.

## Demo
- Walkthrough clip (60–90s): TODO paste demo video link (YouTube unlisted recommended)
- Example output: `examples/sample.csv`

## Run in 3 commands
```bash
uv sync                         # or: pip install -r requirements.txt
cp .env.example .env            # then edit .env with your target URL
uv run python src/scraper.py
```

## What's inside
- `src/scraper.py` — the scraper
- `tests/` — pytest suite (run with `uv run pytest`)
- `examples/` — sample output the client can preview
- `demo/` — screenshots + clip link
- `docs/decisions/` — architectural decision records
- `docs/progress/` — session-by-session work log

## License
All Rights Reserved — see `LICENSE`.

## Contact
- Fastwork profile: TODO paste link once profile is live
- Email: nattakamon@cloudnurse.co
- Response: within 1 business day
