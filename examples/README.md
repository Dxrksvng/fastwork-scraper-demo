# Example output

`sample.csv` is a real-run output preview against `books.toscrape.com`. Clients can eyeball this to see what they'd get.

Regenerate with:
```bash
uv sync
cp .env.example .env
uv run python -m src.scraper
cp data/output/products.csv examples/sample.csv
```
