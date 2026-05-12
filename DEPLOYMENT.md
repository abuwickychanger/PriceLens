# PriceLens Deployment Guide

## Overview

This project consists of two separate applications:
- **Frontend**: Next.js 16 (deployed on Vercel)
- **Backend**: FastAPI (deployed on Railway.app or similar)

## Backend Deployment (FastAPI on Railway)

### Step 1: Deploy Backend to Railway

1. Go to [railway.app](https://railway.app)
2. Create a new project and connect your GitHub repo
3. Set up environment variables in Railway dashboard:
   ```
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_key
   MODEL_PATH=yolov8n.pt
   CONFIDENCE_THRESHOLD=0.5
   CACHE_TTL_HOURS=1
   FRAME_WIDTH=640
   FRAME_HEIGHT=480
   SCRAPER_TIMEOUT=15
   ```

4. Railway will automatically use `railway.toml` for build configuration
5. Copy your deployed backend URL (e.g., `https://price-lens-backend.railway.app`)

### Step 2: Test Backend

```bash
curl https://your-backend-url/health
# Should return: {"status":"ok"}
```

## Frontend Deployment (Next.js on Vercel)

### Step 1: Deploy Frontend to Vercel

1. Go to [vercel.com](https://vercel.com)
2. Import your GitHub repository
3. In Project Settings > Environment Variables, add:
   ```
   NEXT_PUBLIC_API_URL=https://your-backend-url
   ```

4. Vercel will automatically detect `frontend/` directory
5. Deploy!

### Step 2: Configure Custom Domain (Optional)

1. Go to Vercel > Settings > Domains
2. Add your custom domain
3. Update DNS records as instructed

## Local Development

### Backend
```bash
cd backend
pip install -r requirements.txt
playwright install chromium
cp .env.example .env
# Edit .env with your credentials
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
# Open http://localhost:3000
```

## Environment Variables

### Backend (.env in backend/ directory)
- `SUPABASE_URL`: Your Supabase project URL
- `SUPABASE_KEY`: Your Supabase service key
- `MODEL_PATH`: YOLOv8 model (default: yolov8n.pt)
- `CONFIDENCE_THRESHOLD`: Detection confidence (default: 0.5)
- `CACHE_TTL_HOURS`: Cache duration (default: 1)
- `FRAME_WIDTH`: Camera width (default: 640)
- `FRAME_HEIGHT`: Camera height (default: 480)
- `SCRAPER_TIMEOUT`: Scraper timeout in seconds (default: 15)

### Frontend (Vercel Environment Variables)
- `NEXT_PUBLIC_API_URL`: Backend API URL

## Troubleshooting

### Backend fails to start
- Check that all environment variables are set
- Verify Supabase credentials are valid
- Ensure `playwright install chromium` was run

### Frontend can't reach backend
- Verify `NEXT_PUBLIC_API_URL` is set correctly
- Check CORS settings in backend (currently allows all)
- Ensure backend is running and accessible

### Model download hangs
- YOLOv8 model downloads on first run
- This may take 2-5 minutes depending on network
- Check backend logs in Railway dashboard

## Security Notes

⚠️ **IMPORTANT**: 
- Never commit `.env` files
- Rotate your Supabase credentials if exposed
- Use Railway secrets for sensitive data
- Keep API keys out of frontend code (use `NEXT_PUBLIC_` prefix only for public data)

## CI/CD Pipeline

Add GitHub Actions workflow for automated testing and deployment:
- Test backend on push to main
- Run linting checks
- Automatic Railway deployment on main branch

See `.github/workflows/` directory for CI/CD configuration.
