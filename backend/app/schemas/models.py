from pydantic import BaseModel
from typing import Optional


class DetectionRequest(BaseModel):
    image: str


class DetectionResult(BaseModel):
    label: str
    confidence: float
    bbox: Optional[list[float]] = None


class PriceEntry(BaseModel):
    platform: str
    product_name: str
    price: float
    currency: str
    url: str
    in_stock: bool = True


class DetectionResponse(BaseModel):
    success: bool
    detection: Optional[DetectionResult] = None
    prices: list[PriceEntry] = []
    cached: bool = False
    error: Optional[str] = None
