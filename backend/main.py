import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import detect, prices
from app.services.detector import load_model

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Price Comparison AI", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(detect.router, prefix="/api", tags=["detect"])
app.include_router(prices.router, prefix="/api", tags=["prices"])


@app.on_event("startup")
def startup():
    logger.info("Starting up - preloading YOLOv8 model...")
    load_model()
    logger.info("Model preloaded. Ready for inference.")


@app.get("/health")
def health():
    return {"status": "ok"}
