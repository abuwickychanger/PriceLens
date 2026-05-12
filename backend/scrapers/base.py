from abc import ABC, abstractmethod

from app.config import SCRAPER_TIMEOUT

ANTI_BOT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
}


class BaseScraper(ABC):
    def __init__(self, platform: str):
        self.platform = platform
        self.timeout = SCRAPER_TIMEOUT

    @abstractmethod
    async def search(self, product: str) -> list[dict]:
        ...

    def _make_result(self, product_name: str, price: float, currency: str, url: str) -> dict:
        return {
            "platform": self.platform,
            "product_name": product_name,
            "price": price,
            "currency": currency,
            "url": url,
            "in_stock": True,
        }
