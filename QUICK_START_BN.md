# 🚀 দ্রুত শুরু করুন - Render-এ Deploy

## সম্পূর্ণ ফ্লো (GitHub → Render → Download Data)

```
┌─────────────────────────────────────────────────────────────┐
│ 1. GitHub Repository তৈরি করুন                           │
│    - Code push করুন                                        │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. Render-এ Deploy করুন                                   │
│    - GitHub repo connect করুন                             │
│    - Automatic deployment enable করুন                     │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. API দিয়ে Scraping শুরু করুন                           │
│    - POST /api/scrape/keyword                              │
│    - Job ID পাবেন                                          │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. Job Status চেক করুন                                    │
│    - GET /api/jobs/<job_id>                                │
│    - Status: running/completed                             │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. Data Download করুন                                      │
│    - JSON: /api/download/<job_id>                          │
│    - CSV: /api/download-csv/<job_id>                       │
└─────────────────────────────────────────────────────────────┘
```

## ধাপে ধাপে গাইড

### ধাপ ১: GitHub রেপোজিটরি প্রস্তুত করুন

```bash
# এক্সিস্টিং repo এ (ইতিমধ্যে এই folder এ আছেন)
cd /home/redden/Downloads/ScrepingDelhi

# Git initialize করুন (যদি না করা থাকে)
git init
git add .
git commit -m "Scraper setup for Render deployment"

# GitHub ওয়েবসাইটে যান:
# github.com/new → Repository name: scraping-delhi → Create

# Local repo-কে remote এর সাথে connect করুন:
git remote add origin https://github.com/YOUR_USERNAME/scraping-delhi.git
git branch -M main
git push -u origin main
```

### ধাপ ২: Render-এ Deploy করুন

**৩০ সেকেন্ডে Deploy:**

1. https://render.com → Sign up/Login
2. Dashboard → **New** → **Web Service**
3. **Deploy an existing repository** → Search `scraping-delhi`
4. ফলো করুন:
   - **Name**: scraping-delhi
   - **Build Command**: `pip install -r requirements.txt && playwright install chromium`
   - **Start Command**: `python app.py`
   - **Region**: Singapore (Asia-তে ভালো performance)
   - **Plan**: Standard ($7/month - কিন্তু free tier দিয়ে শুরু করতে পারেন)
5. **Create Web Service** ক্লিক করুন

**Deploy হতে ৫-১০ মিনিট সময় লাগবে।**

### ধাপ ৩: API টেস্ট করুন

যখন deployment complete হবে, আপনার URL পাবেন:
```
https://scraping-delhi.onrender.com
```

**Test করুন:**

```bash
# Health check
curl https://scraping-delhi.onrender.com/health

# Response:
# {"status": "healthy", "timestamp": "..."}
```

### ধাপ ৪: Scraping শুরু করুন

```bash
curl -X POST https://scraping-delhi.onrender.com/api/scrape/keyword \
  -H "Content-Type: application/json" \
  -d '{"keyword": "Photographers in Delhi"}'
```

**Response:**
```json
{
  "job_id": "job_20240703_143022",
  "status": "completed",
  "keyword": "Photographers in Delhi",
  "download_url": "/api/download/job_20240703_143022"
}
```

### ধাপ ৫: Status চেক করুন

```bash
curl https://scraping-delhi.onrender.com/api/jobs/job_20240703_143022
```

### ধাপ ৬: Data Download করুন

**JSON এ:**
```bash
curl https://scraping-delhi.onrender.com/api/download/job_20240703_143022 \
  -o results.json
```

**CSV এ:**
```bash
curl https://scraping-delhi.onrender.com/api/download-csv/job_20240703_143022 \
  -o results.csv
```

**Browser দিয়ে:**
Simply visit: https://scraping-delhi.onrender.com/api/download/job_20240703_143022

## GitHub Actions দিয়ে Automated Scraping

`.github/workflows/scrape.yml` ইতিমধ্যে তৈরি করা হয়েছে।

**Setup করুন:**

1. GitHub Repo Settings → **Secrets and variables** → **New repository secret**
2. নিচের secrets add করুন:
   - `RENDER_API_URL`: `https://scraping-delhi.onrender.com`
   - `RENDER_DOMAIN`: `scraping-delhi.onrender.com`

3. **Actions** → **Automated Scraping** → **Run workflow** (Manual trigger)

**Automatic Schedule:**
- Default: প্রতি সপ্তাহে রবিবার সকাল ২টায়
- Edit করতে: `.github/workflows/scrape.yml` → `cron` value change করুন

## সবচেয়ে গুরুত্বপূর্ণ জিনিস

| কী | যা করবে |
|---|---|
| **requirements.txt** | সব dependencies auto-install হবে Render-এ |
| **Procfile** | কোন command চালাতে হবে তা বলে |
| **.gitignore** | Data, venv, __pycache__ ignore করবে |
| **render.yaml** | Render config (optional but recommended) |
| **DEPLOYMENT.md** | বিস্তারিত documentation |

## সাধারণ সমস্যা

### ❌ "Playwright not found"
```
✅ Solution: Build command-এ playwright install chromium আছে
```

### ❌ "Memory exceeded"
```
✅ Solution: Render dashboard → Environment → Memory বাড়ান (2GB recommended)
```

### ❌ "Service spinning down"
```
✅ Solution: Free tier-এ এটা normal - paid plan এ stay awake থাকবে
```

### ❌ "Requests timeout"
```
✅ Solution: Google rate limiting করছে - app.py এ delays বাড়ান
```

## কখন ডেটা পাবেন?

**Timeline:**
- Scraping start → চেষ্টা করে প্রতি URL থেকে data extract করবে
- প্রতি 5টি record এ save করবে (SAVE_EVERY = 5)
- Job complete হলে download ready
- JSON + CSV উভয় format available

## আরও সহায়তা

- 📖 Full guide: [DEPLOYMENT.md](DEPLOYMENT.md)
- 📚 README: [README.md](README.md)
- 🎯 API Docs: https://scraping-delhi.onrender.com/

---

**এখানে শুরু করুন:** 
1. GitHub করুন
2. Render connect করুন
3. API call করুন
4. Data download করুন

✨ **শুভকামনা!**
