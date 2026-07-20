"""
Product listing scraper — static HTML pages to CSV/Excel.

Design: three concerns kept separate so each is testable in isolation:
    fetch_html        network I/O only
    parse_products    HTML -> Product objects
    find_next_page    pagination discovery

The scrape() function orchestrates the loop; write_output() handles export.
Only main() touches env vars — the library functions are pure(-ish) and
importable from tests without side effects.
"""

from __future__ import annotations

import logging
import os
import sys
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from urllib.parse import urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

log = logging.getLogger(__name__)


@dataclass
class Product:
    title: str
    price: str
    url: str
    availability: str


def fetch_html(url: str, user_agent: str, timeout: int = 30) -> str:
    """GET a URL and return HTML text. Raises requests.HTTPError on 4xx/5xx.

    Uses apparent_encoding (chardet-based) so pages that omit charset in
    Content-Type still decode correctly. Without this, requests falls back
    to ISO-8859-1 and produces mojibake on UTF-8 content (£ -> Â£).
    """
    resp = requests.get(url, headers={"User-Agent": user_agent}, timeout=timeout)
    resp.raise_for_status()
    resp.encoding = resp.apparent_encoding or resp.encoding
    return resp.text


def parse_products(html: str, base_url: str) -> list[Product]:
    """Extract products from a listing page. Skips malformed cards; never raises."""
    soup = BeautifulSoup(html, "html.parser")
    items: list[Product] = []
    for card in soup.select("article.product_pod"):
        try:
            title_el = card.select_one("h3 a")
            price_el = card.select_one("p.price_color")
            avail_el = card.select_one("p.instock.availability")
            if not (title_el and price_el):
                continue
            items.append(
                Product(
                    title=title_el.get("title") or title_el.get_text(strip=True),
                    price=price_el.get_text(strip=True),
                    url=urljoin(base_url, title_el.get("href", "")),
                    availability=(avail_el.get_text(strip=True) if avail_el else "unknown"),
                )
            )
        except (AttributeError, KeyError) as e:
            log.warning("skipping malformed card: %s", e)
            continue
    return items


def find_next_page(html: str, current_url: str) -> str | None:
    """Return absolute URL of the next page, or None if this is the last."""
    soup = BeautifulSoup(html, "html.parser")
    nxt = soup.select_one("li.next a")
    if not nxt or not nxt.get("href"):
        return None
    return urljoin(current_url, nxt["href"])


def scrape(
    target_url: str,
    user_agent: str,
    delay_seconds: float,
    max_pages: int,
) -> list[Product]:
    """Walk paginated listing politely; stop on network error rather than crash."""
    collected: list[Product] = []
    url: str | None = target_url
    page = 0
    while url and page < max_pages:
        page += 1
        log.info("fetching page %d: %s", page, url)
        try:
            html = fetch_html(url, user_agent)
        except requests.RequestException as e:
            log.error("page %d failed, stopping loop: %s", page, e)
            break
        items = parse_products(html, url)
        log.info("  parsed %d items", len(items))
        collected.extend(items)
        url = find_next_page(html, url)
        if url:
            time.sleep(delay_seconds)
    return collected


def write_output(items: list[Product], out_dir: Path, fmt: str) -> Path:
    """Write items to CSV (default) or XLSX. utf-8-sig makes Thai text render in Excel."""
    if not items:
        raise ValueError("no items to write")
    out_dir.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame([asdict(i) for i in items])
    if fmt.lower() in ("excel", "xlsx"):
        out = out_dir / "products.xlsx"
        df.to_excel(out, index=False)
    else:
        out = out_dir / "products.csv"
        df.to_csv(out, index=False, encoding="utf-8-sig")
    return out


def main() -> int:
    load_dotenv()
    logging.basicConfig(
        level=os.getenv("LOG_LEVEL", "INFO").upper(),
        format="%(levelname)s: %(message)s",
    )

    target = os.getenv("TARGET_URL")
    if not target:
        log.error("TARGET_URL not set — copy .env.example to .env and edit")
        return 2

    user_agent = os.getenv("USER_AGENT", "portfolio-demo-scraper/0.1")
    delay = float(os.getenv("SCRAPE_DELAY_SECONDS", "2"))
    max_pages = int(os.getenv("MAX_PAGES", "5"))
    out_dir = Path(os.getenv("OUTPUT_DIR", "data/output"))
    fmt = os.getenv("OUTPUT_FORMAT", "csv")

    items = scrape(target, user_agent, delay, max_pages)
    if not items:
        log.warning("no items scraped — check TARGET_URL and selectors")
        return 1

    out_path = write_output(items, out_dir, fmt)
    log.info("wrote %d rows to %s", len(items), out_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
