import asyncio
import logging

from scrapers.amazon import AmazonScraper
from scrapers.ebay import EbayScraper
from scrapers.walmart import WalmartScraper

logger = logging.getLogger(__name__)

_scrapers = [AmazonScraper(), EbayScraper(), WalmartScraper()]


async def search_product_prices(product: str) -> list[dict]:
    logger.info(f"Searching prices for: {product}")
    tasks = [scraper.search(product) for scraper in _scrapers]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    all_prices = []
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            logger.warning(f"Scraper {_scrapers[i].platform} error: {result}")
            continue
        all_prices.extend(result)
    all_prices.sort(key=lambda x: x["price"] if x["price"] > 0 else float("inf"))
    logger.info(f"Found {len(all_prices)} price entries for: {product}")
    return all_prices
