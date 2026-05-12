import logging

from fastapi import APIRouter, Query

from app.schemas.models import DetectionResponse, PriceEntry
from app.services.scraper import search_product_prices
from app.services.cache import get_cached_prices, set_cached_prices

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/prices", response_model=DetectionResponse)
async def get_prices(product: str = Query(..., min_length=1)):
    cached = await get_cached_prices(product)
    if cached is not None:
        return DetectionResponse(
            success=True,
            prices=cached,
            cached=True,
        )
    prices = await search_product_prices(product)
    price_entries = [PriceEntry(**p) for p in prices]
    await set_cached_prices(product, price_entries)
    return DetectionResponse(
        success=True,
        prices=price_entries,
        cached=False,
    )
