# Price Comparison AI

Real-time product detection and price comparison using AI. Point your camera at any product — YOLOv8 identifies it and fetches prices from Amazon, eBay, and Walmart in under 5 seconds.

## Architecture

```
frontend/     Next.js 16 + Tailwind CSS (WebRTC camera interface)
backend/      FastAPI + YOLOv8 (detection) + Playwright/BS4 (scraping)
model/        YOLOv8 weights (auto-downloaded by ultralytics)
```

## Prerequisites

- Python 3.10+
- Node.js 20+
- Playwright browsers (see setup)

## Setup

### Backend

```bash
pip install -r backend/requirements.txt
playwright install chromium
```

Copy `.env.example` to `.env` and fill in your Supabase credentials:

```bash
cp backend/.env.example backend/.env
```

Start the backend:

```bash
uvicorn backend.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000

## How It Works

1. **Scan**: Point camera at a product — frames captured every 1s via WebRTC
2. **Detect**: YOLOv8 identifies the product with confidence score
3. **Cache**: Supabase cache checked (1-hour TTL); returns instantly if found
4. **Scrape**: Concurrent Playwright/BS4 scrapers fetch prices from 3 platforms
5. **Compare**: Sorted price cards with platform icons and direct links

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `SUPABASE_URL` | — | Supabase project URL |
| `SUPABASE_KEY` | — | Supabase service role key |
| `MODEL_PATH` | `yolov8n.pt` | YOLOv8 model name/path |
| `CONFIDENCE_THRESHOLD` | `0.5` | Minimum detection confidence |
| `CACHE_TTL_HOURS` | `1` | Cache duration before re-scraping |
| `FRAME_WIDTH` | `640` | Camera capture width |
| `FRAME_HEIGHT` | `480` | Camera capture height |
| `SCRAPER_TIMEOUT` | `15` | Timeout (s) per scraper |

## Supabase Setup

Create a `price_cache` table:

```sql
CREATE TABLE price_cache (
  id BIGSERIAL PRIMARY KEY,
  product_label TEXT NOT NULL,
  prices JSONB NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX idx_price_cache_lookup ON price_cache (product_label, created_at DESC);
```
