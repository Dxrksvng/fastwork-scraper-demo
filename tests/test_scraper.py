"""
Unit tests — no live network calls. Parsing is tested against a saved fixture,
which is how a scraper stays testable when the target site is down or you're offline.
"""

from pathlib import Path

import pytest

from src.scraper import Product, find_next_page, parse_products, write_output

FIXTURE = Path(__file__).parent / "fixtures" / "listing.html"


def _fixture_html() -> str:
    return FIXTURE.read_text(encoding="utf-8")


def test_parse_products_extracts_valid_cards():
    items = parse_products(_fixture_html(), "https://books.toscrape.com/catalogue/page-1.html")
    assert len(items) == 3
    titles = {i.title for i in items}
    assert "A Light in the Attic" in titles
    assert "Tipping the Velvet" in titles


def test_parse_products_resolves_relative_urls():
    items = parse_products(_fixture_html(), "https://books.toscrape.com/catalogue/page-1.html")
    for item in items:
        assert item.url.startswith("https://books.toscrape.com/")


def test_parse_products_captures_price_and_availability():
    items = parse_products(_fixture_html(), "https://books.toscrape.com/")
    first = next(i for i in items if i.title == "A Light in the Attic")
    assert first.price == "£51.77"
    assert first.availability == "In stock"


def test_parse_products_skips_malformed_card():
    items = parse_products(_fixture_html(), "https://x/")
    assert not any(i.title == "bad card" for i in items)


def test_parse_products_returns_empty_when_no_cards():
    items = parse_products("<html><body>nothing here</body></html>", "https://x/")
    assert items == []


def test_find_next_page_returns_absolute_url():
    result = find_next_page(_fixture_html(), "https://books.toscrape.com/catalogue/page-1.html")
    assert result == "https://books.toscrape.com/catalogue/page-2.html"


def test_find_next_page_returns_none_on_last_page():
    html = '<html><body><ul class="pager"><li class="current">last</li></ul></body></html>'
    assert find_next_page(html, "https://x/") is None


def test_write_output_creates_csv(tmp_path: Path):
    items = [
        Product(title="A", price="£1", url="https://x/a", availability="In stock"),
        Product(title="B", price="£2", url="https://x/b", availability="In stock"),
    ]
    out = write_output(items, tmp_path, "csv")
    assert out.exists()
    content = out.read_text(encoding="utf-8-sig")
    assert "title,price,url,availability" in content
    assert "A,£1,https://x/a,In stock" in content


def test_write_output_raises_on_empty(tmp_path: Path):
    with pytest.raises(ValueError):
        write_output([], tmp_path, "csv")
