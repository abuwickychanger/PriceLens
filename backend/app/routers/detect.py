import base64
import logging

from fastapi import APIRouter, HTTPException

from app.schemas.models import DetectionRequest, DetectionResponse, DetectionResult, PriceEntry
from app.services.detector import detect_product
from app.services.scraper import search_product_prices
from app.services.cache import get_cached_prices, set_cached_prices

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/detect", response_model=DetectionResponse)
async def detect(req: DetectionRequest):
    try:
        image_bytes = base64.b64decode(req.image)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid base64: {e}")

    detection = detect_product(image_bytes)
    if detection is None:
        return DetectionResponse(success=False, error="No product detected")

    det_result = DetectionResult(
        label=detection["label"],
        confidence=detection["confidence"],
        bbox=detection["bbox"],
    )

    cached = await get_cached_prices(detection["label"])
    if cached is not None:
        return DetectionResponse(
            success=True,
            detection=det_result,
            prices=cached,
            cached=True,
        )

    prices = await search_product_prices(detection["label"])
    price_entries = [PriceEntry(**p) for p in prices]

    await set_cached_prices(detection["label"], price_entries)

    return DetectionResponse(
        success=True,
        detection=det_result,
        prices=price_entries,
        cached=False,
    )
