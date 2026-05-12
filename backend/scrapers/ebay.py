import re
import logging

import httpx
from bs4 import BeautifulSoup

from scrapers.base import BaseScraper, ANTI_BOT_HEADERS

logger = logging.getLogger(__name__)


class EbayScraper(BaseScraper):
    def __init__(self):
        super().__init__("eBay")

    async def search(self, product: str) -> list[dict]:
        url = f"https://www.ebay.com/sch/i.html?_nkw={product.replace(' ', '+')}"
        results = []
        try:
            async with httpx.AsyncClient(headers=ANTI_BOT_HEADERS, timeout=self.timeout) as client:
                resp = await client.get(url)
                resp.raise_for_status()
                soup = BeautifulSoup(resp.text, "lxml")
                items = soup.select("li.s-item") or soup.select(".s-item")
                for item in items[:4]:
                    try:
                        title_el = item.select_one(".s-item__title")
                        price_el = item.select_one(".s-item__price")
                        link_el = item.select_one("a.s-item__link")
                        if not title_el or not link_el:
                            continue
                        title = title_el.get_text(strip=True)
                        href = link_el.get("href", "")
                        price = 0.0
                        currency = "USD"
                        if price_el:
                            raw = price_el.get_text(strip=True)
                            match = re.search(r"[\d,.]+", raw)
                            if match:
                                price = float(match.group(0).replace(",", ""))
                        results.append(self._make_result(title, price, currency, href.split("?")[0]))
                    except Exception as e:
                        logger.debug(f"eBay item parse error: {e}")
        except Exception as e:
            logger.warning(f"eBay scraper failed: {e}")
        return results
