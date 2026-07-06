# Scraping Delhi - Deployment Guide

## Overview
This is a Google Maps scraper for photographers/DJs in Delhi NCR region. It can be deployed on Render using GitHub.

## Prerequisites
- GitHub account
- Render account (free tier available at https://render.com)
- This repository

## Step 1: Prepare Repository for GitHub

```bash
# Initialize git repo (if not already)
git init
git add .
git commit -m "Initial commit - scraper setup for Render"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/scraping-delhi.git
git push -u origin main
```

## Step 2: Deploy to Render

### Option A: Quick Deploy (Recommended)

1. Go to https://render.com/dashboard
2. Click "New +" → "Web Service"
3. Select "Deploy an existing GitHub repository"
4. Search for "scraping-delhi" and connect
5. Configuration:
   - **Name**: `scraping-delhi`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt && playwright install chromium`
   - **Start Command**: `python app.py`
   - **Plan**: Standard (recommended for scraping jobs)
   - **Memory**: 2GB minimum (for Playwright/Chromium)

6. Click "Deploy"

### Option B: Using render.yaml

Just commit `render.yaml` to your repo. Render will auto-detect it.

## Step 3: Using the API

### 1. Health Check
```bash
curl https://scraping-delhi.onrender.com/health
```

### 2. Start Scraping Job
```bash
curl -X POST https://scraping-delhi.onrender.com/api/scrape/keyword \
  -H "Content-Type: application/json" \
  -d '{"keyword": "Djs in Delhi"}'
```

Response:
```json
{
  "job_id": "job_20240703_120000",
  "status": "completed",
  "download_url": "/api/download/job_20240703_120000"
}
```

### 3. Check Job Status
```bash
curl https://scraping-delhi.onrender.com/api/jobs/job_20240703_120000
```

### 4. Download Results (JSON)
```bash
curl https://scraping-delhi.onrender.com/api/download/job_20240703_120000 \
  -o results.json
```

### 5. Download Results (CSV)
```bash
curl https://scraping-delhi.onrender.com/api/download-csv/job_20240703_120000 \
  -o results.csv
```

### 6. List All Jobs
```bash
curl https://scraping-delhi.onrender.com/api/jobs
```

## GitHub Workflow Integration

### Automated Scraping via GitHub Actions

Create `.github/workflows/scrape.yml`:

```yaml
name: Scheduled Scraping

on:
  schedule:
    - cron: '0 2 * * *'  # Run daily at 2 AM UTC
  workflow_dispatch:  # Allow manual trigger

jobs:
  scrape:
    runs-on: ubuntu-latest
    steps:
      - name: Trigger scraping on Render
        run: |
          curl -X POST ${{ secrets.RENDER_API_URL }}/api/scrape/keyword \
            -H "Content-Type: application/json" \
            -d '{"keyword": "Photographers in Delhi"}'
```

Add `RENDER_API_URL` to GitHub Secrets (e.g., `https://scraping-delhi.onrender.com`)

## Downloading Data

### From Terminal
```bash
# Download latest results
JOB_ID="job_20240703_120000"
curl -o data.json https://scraping-delhi.onrender.com/api/download/$JOB_ID
```

### From Browser
Simply visit: `https://scraping-delhi.onrender.com/api/download/job_20240703_120000`

### From Python
```python
import requests
import json

API_URL = "https://scraping-delhi.onrender.com"

# Start scraping
response = requests.post(
    f"{API_URL}/api/scrape/keyword",
    json={"keyword": "Photographers in Delhi"}
)
job_id = response.json()["job_id"]

# Download results
download_url = f"{API_URL}/api/download/{job_id}"
data = requests.get(download_url).json()
print(f"Scraped {len(data)} records")
```

## Monitoring

- **Logs**: View in Render dashboard → Service → Logs
- **Status**: https://scraping-delhi.onrender.com/health
- **Jobs**: https://scraping-delhi.onrender.com/api/jobs

## Important Notes

1. **Render Free Tier**: Services spin down after 15 min of inactivity
2. **Scraping Duration**: Adjust timeouts for longer jobs
3. **Memory**: Ensure 2GB+ for Chromium
4. **Rate Limiting**: Google Maps may rate-limit aggressively - adjust delays in code
5. **Data Persistence**: Data stored in `/outputs` (temp storage on Render)

## Advanced: Add Data Persistence

For persistent storage beyond Render's temp filesystem, integrate with:
- **PostgreSQL**: Render includes free PostgreSQL addon
- **MongoDB Atlas**: Free tier available
- **AWS S3**: Store JSON files in S3 bucket

## Troubleshooting

### Playwright not found
```
Error: Chromium not installed
```
Solution: Render build command already includes `playwright install chromium`

### Service crashes
- Check memory limit (increase to 2GB+)
- Check logs in Render dashboard
- Reduce concurrent workers in app.py

### Jobs not completing
- Extend service timeout
- Check if Google Maps is blocking requests
- Add rotating proxies

## Next Steps

1. ✅ Push to GitHub
2. ✅ Deploy to Render
3. ✅ Test API endpoints
4. ✅ Set up GitHub Actions for automation
5. ✅ Monitor logs and jobs

---

**Questions?** Check Render docs: https://render.com/docs
