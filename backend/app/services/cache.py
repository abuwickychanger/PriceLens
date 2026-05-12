import asyncio
import json
import logging
from datetime import datetime, timedelta, timezone
from typing import Optional

from supabase import create_client, Client

from app.config import SUPABASE_URL, SUPABASE_KEY, CACHE_TTL_HOURS
from app.schemas.models import PriceEntry

logger = logging.getLogger(__name__)

_supabase: Optional[Client] = None


def _get_client() -> Optional[Client]:
    global _supabase
    if _supabase is None and SUPABASE_URL and SUPABASE_KEY:
        _supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    return _supabase


async def get_cached_prices(product_label: str) -> Optional[list[PriceEntry]]:
    client = _get_client()
    if client is None:
        return None
    try:
        cutoff = (datetime.now(timezone.utc) - timedelta(hours=CACHE_TTL_HOURS)).isoformat()
        result = await asyncio.to_thread(
            lambda: client.table("price_cache")
            .select("*")
            .eq("product_label", product_label.lower())
            .gte("created_at", cutoff)
            .order("created_at", desc=True)
            .limit(1)
            .execute()
        )
        if result.data and len(result.data) > 0:
            prices_json = result.data[0].get("prices", "[]")
            prices = [PriceEntry(**p) for p in json.loads(prices_json)]
            logger.info(f"Cache HIT for '{product_label}' ({len(prices)} entries)")
            return prices
    except Exception as e:
        logger.warning(f"Cache read error: {e}")
    return None


async def set_cached_prices(product_label: str, prices: list[PriceEntry]) -> None:
    client = _get_client()
    if client is None:
        return
    try:
        await asyncio.to_thread(
            lambda: client.table("price_cache")
            .insert({
                "product_label": product_label.lower(),
                "prices": json.dumps([p.model_dump() for p in prices]),
                "created_at": datetime.now(timezone.utc).isoformat(),
            })
            .execute()
        )
        logger.info(f"Cached {len(prices)} prices for '{product_label}'")
    except Exception as e:
        logger.warning(f"Cache write error: {e}")
