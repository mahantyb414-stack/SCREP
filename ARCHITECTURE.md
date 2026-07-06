# 🔄 System Architecture & Data Flow

## সম্পূর্ণ সিস্টেম ডায়াগ্রাম

```
┌──────────────────────────────────────────────────────────────────┐
│                        Your Local Machine                        │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │ Code Directory: /home/redden/Downloads/ScrepingDelhi       │  │
│  │ - scrap_main.py (Core scraper)                             │  │
│  │ - bulk_scraper.py (Multi-location)                         │  │
│  │ - app.py (Flask API server)                                │  │
│  │ - requirements.txt (Dependencies)                          │  │
│  └────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────┘
                              ↓ git push
                    (Upload to GitHub)
┌──────────────────────────────────────────────────────────────────┐
│                     GitHub Repository                            │
│ ┌────────────────────────────────────────────────────────────┐  │
│ │ scraping-delhi                                             │  │
│ │ - All source code                                          │  │
│ │ - .github/workflows/scrape.yml (Automation)               │  │
│ └────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────┘
                    ↓ (GitHub webhook trigger)
            (Render detects new code changes)
┌──────────────────────────────────────────────────────────────────┐
│                    Render Platform                               │
│ ┌────────────────────────────────────────────────────────────┐  │
│ │ Web Service: scraping-delhi.onrender.com                   │  │
│ │                                                             │  │
│ │ ┌──────────────────────────────────────────────────────┐   │  │
│ │ │ Build Process                                        │   │  │
│ │ │ 1. pip install -r requirements.txt                   │   │  │
│ │ │ 2. playwright install chromium                       │   │  │
│ │ │ 3. Start: python app.py                              │   │  │
│ │ └──────────────────────────────────────────────────────┘   │  │
│ │                                                             │  │
│ │ ┌──────────────────────────────────────────────────────┐   │  │
│ │ │ Running Service (24/7)                               │   │  │
│ │ │ - Flask app listening on port 5000                   │   │  │
│ │ │ - Accepts HTTP requests                              │   │  │
│ │ │ - Stores data in /outputs folder                     │   │  │
│ │ └──────────────────────────────────────────────────────┘   │  │
│ └────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────┘
                   ↑ HTTP Requests  ↓ Data Response
        ┌──────────┴────────────────┴──────────┐
        │                                      │
        ↓                                      ↑
┌─────────────────┐              ┌──────────────────────┐
│ Your Browser    │              │ Your Application     │
│ /Terminal       │              │ Python/Node/etc      │
│                 │              │                      │
│ curl API        │──HTTP POST──→│ GET /api/download    │
│ calls           │              │                      │
└─────────────────┘←─JSON DATA───└──────────────────────┘
        ↓ (Save)
    results.json
    results.csv
```

---

## API Request Flow (বিস্তারিত)

```
┌─────────────────────────────────────────────────────────────┐
│ 1. CLIENT sends HTTP POST request                           │
│    POST /api/scrape/keyword                                 │
│    Body: {"keyword": "Photographers in Delhi"}              │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. RENDER API SERVER receives request                       │
│    - app.py processes request                               │
│    - Creates unique job_id                                  │
│    - Returns: {job_id, status, download_url}               │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. SCRAPER starts async task                                │
│    - Launches browser context                               │
│    - Searches Google Maps                                   │
│    - Extracts business data                                 │
│    - Saves to JSON file                                     │
└─────────────────────────────────────────────────────────────┘
                    ↙ (while running)
        ┌──────────────────────────┐
        │ CLIENT can check status  │
        │ GET /api/jobs/<job_id>   │
        │ Response: {status, ...}  │
        └──────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. SCRAPING COMPLETE                                        │
│    - Status changed to "completed"                          │
│    - Data saved in /outputs/job_20240703_*.json            │
│    - Records count updated                                  │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. CLIENT downloads data                                    │
│    GET /api/download/<job_id>                               │
│    Response: File stream (JSON)                             │
│    OR                                                       │
│    GET /api/download-csv/<job_id>                           │
│    Response: File stream (CSV)                              │
└─────────────────────────────────────────────────────────────┘
                         ↓
        ┌──────────────────────────┐
        │ Save file locally        │
        │ results.json or .csv     │
        └──────────────────────────┘
```

---

## GitHub Actions Automation Flow

```
┌────────────────────────────────────┐
│ Schedule: Every Sunday 2 AM UTC    │
│ OR Manual Trigger                  │
└────────────────────────────────────┘
                ↓
┌────────────────────────────────────┐
│ GitHub Actions Workflow starts     │
│ (.github/workflows/scrape.yml)     │
└────────────────────────────────────┘
                ↓
┌────────────────────────────────────┐
│ 1. Checkout latest code            │
│ 2. Setup Python 3.11               │
│ 3. Install dependencies            │
│ 4. Install Playwright              │
└────────────────────────────────────┘
                ↓
┌────────────────────────────────────────────────────────┐
│ 5. Send POST to Render API                             │
│    /api/scrape/keyword                                 │
│    Keywords: [                                         │
│      "Photographers in Delhi",                         │
│      "Wedding Photographers in Delhi",                 │
│      "DJs in Delhi"                                    │
│    ]                                                   │
└────────────────────────────────────────────────────────┘
                ↓
┌────────────────────────────────────────────────────────┐
│ 6. Render processes each keyword                       │
│    - 3 parallel scraping jobs                          │
│    - Each extracts business data                       │
│    - Results saved separately                          │
└────────────────────────────────────────────────────────┘
                ↓
┌────────────────────────────────────────────────────────┐
│ 7. Workflow completes                                  │
│    ✓ All jobs finished                                 │
│    ✓ Data available at /api/jobs                      │
│    ✓ Notification (if configured)                     │
└────────────────────────────────────────────────────────┘
```

---

## Data Structure

### Request Format
```json
{
  "keyword": "Photographers in Delhi"
}
```

### Job Response
```json
{
  "job_id": "job_20240703_143022",
  "status": "completed",
  "keyword": "Photographers in Delhi",
  "record_count": 45,
  "created_at": "2024-07-03T14:30:22.123456",
  "completed_at": "2024-07-03T14:45:33.654321",
  "download_url": "/api/download/job_20240703_143022"
}
```

### Output Data (প্রতিটি Record)
```json
{
  "gmaps_url": "https://www.google.com/maps/place/Studio+Name/...",
  "gmaps_name": "Studio Name",
  "gmaps_address": "123 Main Street, Delhi 110001",
  "gmaps_phone": "+91 98765 43210",
  "gmaps_rating": "4.8",
  "gmaps_reviews_count": "156",
  "gmaps_opening_hours": "10:00 AM - 8:00 PM",
  "gmaps_category": "Photography studio",
  "gmaps_website": "https://studioweb.com",
  "gmaps_image_urls": [],
  "gmaps_about": "Professional photography services...",
  "original_data": { ... }
}
```

---

## Component Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    app.py (Flask)                        │
│  ┌────────────────────────────────────────────────────┐  │
│  │  HTTP Routes                                       │  │
│  │  - GET  /health                                   │  │
│  │  - POST /api/scrape/keyword                       │  │
│  │  - GET  /api/jobs/<job_id>                        │  │
│  │  - GET  /api/download/<job_id>                    │  │
│  │  - GET  /api/download-csv/<job_id>                │  │
│  │  - GET  /api/jobs                                 │  │
│  └────────────────────────────────────────────────────┘  │
│                         ↓                                  │
│  ┌────────────────────────────────────────────────────┐  │
│  │  Job Status Manager                                │  │
│  │  - Track running jobs                             │  │
│  │  - Store results                                  │  │
│  │  - Handle errors                                  │  │
│  └────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
                         ↓
┌──────────────────────────────────────────────────────────┐
│              scrap_main.py (Scraper)                     │
│  ┌────────────────────────────────────────────────────┐  │
│  │  GoogleMapsKeywordScraper                          │  │
│  │  - _collect_urls() - Find business URLs           │  │
│  │  - _scrape_details() - Extract data               │  │
│  │  - _pipeline_worker() - Async processing          │  │
│  │  - _save() - Persist to JSON                       │  │
│  └────────────────────────────────────────────────────┘  │
│                         ↓                                  │
│  ┌────────────────────────────────────────────────────┐  │
│  │  ContextPool                                       │  │
│  │  - Reusable Browser Contexts                       │  │
│  │  - Recycle after MAX_CTX_USES                     │  │
│  │  - Resource pooling                               │  │
│  └────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
                         ↓
┌──────────────────────────────────────────────────────────┐
│          Playwright (Browser Automation)                 │
│  - Launch Chromium instance                             │
│  - Navigate to Google Maps                              │
│  - Extract HTML content                                 │
│  - Run JavaScript for dynamic data                      │
└──────────────────────────────────────────────────────────┘
                         ↓
┌──────────────────────────────────────────────────────────┐
│                  Google Maps API                         │
│  (via Web Scraping - no API key needed)                  │
└──────────────────────────────────────────────────────────┘
```

---

## Deployment Timeline

```
Day 1:
  └─ Setup GitHub repo ..................... 10 min
  └─ Deploy to Render ..................... 10 min
  └─ Test API ............................ 5 min
  └─ First scraping job .................. 15 min
  └─ Download data ....................... 5 min
     TOTAL: ~45 minutes to working system!

Week 1:
  └─ Run multiple scraping jobs
  └─ Monitor performance
  └─ Setup GitHub Actions (optional)

Ongoing:
  └─ Automated weekly scraping
  └─ Download data as needed
  └─ Scale up if needed
```

---

## File Structure in Render

```
/app
├── app.py                          # Flask server
├── scrap_main.py                   # Core scraper
├── bulk_scraper.py                 # Multi-location scraper
├── matcher.yaml                    # Filter rules
├── requirements.txt                # Dependencies
├── Procfile                        # Start command
├── outputs/                        # Generated data
│   ├── job_20240703_143022.json
│   ├── job_20240703_143022.csv
│   ├── job_20240704_120000.json
│   └── ...
├── Data/                           # Input location data
│   └── Top_2k_Delhi_NCR_ARE_covered.xlsx
└── logs/                           # Application logs
```

---

## Success Indicators ✅

কখন বুঝবেন সবকিছু ঠিকঠাক কাজ করছে:

```
✅ GitHub repo active
✅ Render deployment "Live" status
✅ /health endpoint returns 200
✅ POST /api/scrape/keyword accepts requests
✅ Job status changes from "running" to "completed"
✅ Data files exist in /outputs/
✅ JSON download possible
✅ CSV export working
✅ GitHub Actions triggering (if enabled)
✅ Data regularly scraped and available
```

---

**এই সিস্টেম সম্পূর্ণভাবে automated এবং স্কেলেবল!**
