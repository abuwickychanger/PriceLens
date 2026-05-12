import re
import logging

from playwright.async_api import async_playwright

from scrapers.base import BaseScraper, ANTI_BOT_HEADERS

logger = logging.getLogger(__name__)


class AmazonScraper(BaseScraper):
    def __init__(self):
        super().__init__("Amazon")

    async def search(self, product: str) -> list[dict]:
        url = f"https://www.amazon.com/s?k={product.replace(' ', '+')}"
        results = []
        try:
            async with async_playwright() as pw:
                browser = await pw.chromium.launch(headless=True)
                ctx = await browser.new_context(
                    user_agent=ANTI_BOT_HEADERS["User-Agent"],
                    extra_http_headers=ANTI_BOT_HEADERS,
                )
                page = await ctx.new_page()
                await page.goto(url, timeout=self.timeout * 1000, wait_until="domcontentloaded")
                await page.wait_for_selector("[data-component-type='s-search-result']", timeout=8000)
                items = await page.query_selector_all("[data-component-type='s-search-result']")
                for item in items[:3]:
                    try:
                        title_el = await item.query_selector("h2 a span")
                        price_el = await item.query_selector(".a-price .a-offscreen")
                        link_el = await item.query_selector("h2 a")
                        if not title_el or not link_el:
                            continue
                        title = await title_el.inner_text()
                        href = await link_el.get_attribute("href")
                        full_url = f"https://www.amazon.com{href}" if href else url
                        price = 0.0
                        currency = "USD"
                        if price_el:
                            raw = await price_el.inner_text()
                            match = re.search(r"[\d,.]+", raw)
                            if match:
                                price = float(match.group(0).replace(",", ""))
                        results.append(self._make_result(title.strip(), price, currency, full_url))
                    except Exception as e:
                        logger.debug(f"Amazon item parse error: {e}")
                await browser.close()
        except Exception as e:
            logger.warning(f"Amazon scraper failed: {e}")
        return results
