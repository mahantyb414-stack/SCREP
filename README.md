<<<<<<< HEAD
# SCREP
for screaping data 
=======
# Scraping Delhi - Google Maps Photographer & DJ Scraper

A high-performance async web scraper for extracting photographer and DJ business data from Google Maps across Delhi NCR region.

## 🎯 Features

- **Async Playwright-based scraper** with context pooling
- **Bulk scraping** across 2000+ Delhi NCR locations
- **Smart filtering** using YAML configuration
- **Data persistence** with progress tracking
- **REST API** for server deployment
- **Render deployment** ready with GitHub integration

## 📋 Project Structure

```
.
├── scrap_main.py           # Core async scraper engine
├── bulk_scraper.py         # Multi-location scraper
├── matcher.yaml            # Filter rules (categories & keywords)
├── app.py                  # Flask REST API
├── requirements.txt        # Python dependencies
├── Procfile                # Render deployment config
├── render.yaml             # Render service definition
├── DEPLOYMENT.md           # Detailed deployment guide
├── Top_2k_Delhi_NCR_ARE_covered.xlsx  # Location data
├── Data/                   # Output directory for JSON files
└── .github/workflows/scrape.yml  # GitHub Actions automation

```

## 🚀 Quick Start (Local)

### Installation

```bash
# Clone repo
git clone https://github.com/YOUR_USERNAME/scraping-delhi.git
cd scraping-delhi

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browser
playwright install chromium
```

### Usage

#### Option 1: Single Keyword Scraping
```python
from scrap_main import GoogleMapsKeywordScraper, ContextPool
from playwright.async_api import async_playwright
import asyncio

async def main():
    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        pool = ContextPool(browser, size=16)
        await pool.initialize()
        
        scraper = GoogleMapsKeywordScraper("Photographers in Delhi", "output.json")
        await scraper.scrape_all_async(browser, pool, max_workers=16)
        
        await pool.close()
        await browser.close()

asyncio.run(main())
```

#### Option 2: Bulk Scraping (All Locations)
```bash
python bulk_scraper.py
```

## 🌐 Server Deployment (Render)

### One-Click Deploy

1. **Push to GitHub** (see DEPLOYMENT.md)
2. **Go to** https://render.com/dashboard
3. **New Web Service → GitHub Repo → Deploy**

### API Endpoints

```bash
# Health check
curl https://scraping-delhi.onrender.com/health

# Start scraping
curl -X POST https://scraping-delhi.onrender.com/api/scrape/keyword \
  -H "Content-Type: application/json" \
  -d '{"keyword": "Photographers in Delhi"}'

# Check job status
curl https://scraping-delhi.onrender.com/api/jobs/job_20240703_120000

# Download results
curl https://scraping-delhi.onrender.com/api/download/job_20240703_120000 > data.json
```

See [DEPLOYMENT.md](./DEPLOYMENT.md) for complete guide.

## ⚙️ Configuration

### Filter Rules (matcher.yaml)
```yaml
categories:
  - Photography studio
  - Wedding photographer
  - Event photographer
  # Add more...

name_keywords:
  - photographer
  - dj
  - videographer
```

### Tuning Performance

Edit `scrap_main.py` constants:
```python
MAX_CTX_USES = 60        # Context recycling threshold
LOCATION_WORKERS = 2     # Concurrent location scraping
CTX_POOL_SIZE = 3        # Reusable browser contexts
```

## 📊 Output Format

Each record contains:
```json
{
  "original_data": {...},
  "gmaps_url": "https://www.google.com/maps/place/...",
  "gmaps_name": "Studio Name",
  "gmaps_address": "Address",
  "gmaps_phone": "+91...",
  "gmaps_rating": "4.8",
  "gmaps_reviews_count": "123",
  "gmaps_category": "Photography studio",
  "gmaps_website": "https://...",
  "gmaps_about": "About text..."
}
```

## 🔄 GitHub Actions Automation

Workflow file: `.github/workflows/scrape.yml`

**Manual Trigger:**
```bash
# From GitHub UI: Actions → Automated Scraping → Run workflow
```

**Scheduled Trigger:**
```yaml
schedule:
  - cron: '0 2 * * 0'  # Weekly Sunday 2 AM UTC
```

## 🛠️ Development

### Local Testing
```bash
python app.py
# Visit http://localhost:5000
```

### Run Tests
```bash
pytest tests/
```

### Code Structure

- **ContextPool**: Reusable browser context management
- **GoogleMapsKeywordScraper**: Main scraping logic
- **bulk_scraper**: Multi-location coordination

## ⚠️ Important Notes

1. **Google Maps Rate Limiting**: Adjust jitter/delays for stability
2. **Memory Usage**: ~80MB per Chromium context, ensure 2GB+ on Render
3. **Data Privacy**: Ensure compliance with Google Maps ToS
4. **Captcha Handling**: May need proxy rotation for large jobs

## 📝 Logging

View logs:
- **Local**: Console output with timestamps
- **Render**: Service logs in https://render.com/dashboard

## 🐛 Troubleshooting

### Issue: Browser crashes
```
Solution: Increase memory, reduce workers, add delays
```

### Issue: Timeout errors
```
Solution: Increase timeout values, reduce DATA_URLS limit
```

### Issue: Google blocking
```
Solution: Add rotating proxies, reduce request frequency
```

## 📚 References

- [Playwright Docs](https://playwright.dev/python/)
- [Render Deployment](https://render.com/docs)
- [GitHub Actions](https://docs.github.com/en/actions)

## 📄 License

MIT License - See LICENSE file for details

## 👨‍💻 Contributing

1. Fork repository
2. Create feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open Pull Request

## 📧 Support

For issues, questions, or improvements:
- Open GitHub Issue
- Check logs: `tail -f app.log`
- Review error messages in console

---

**Status**: Production Ready ✅
**Last Updated**: July 2024
>>>>>>> 7700be5 (first commit)
