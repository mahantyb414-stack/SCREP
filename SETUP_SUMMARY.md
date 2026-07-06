# 📦 Deployment Setup - Complete Summary

## ✅ সব কিছু প্রস্তুত!

আপনার code base-কে Render-এ deploy করার জন্য সব কিছু সেট আপ করে দিয়েছি।

---

## 📂 নতুন তৈরি ফাইল সমূহ

### **Deployment Files** (Render-এ চলানোর জন্য)
| ফাইল | উদ্দেশ্য |
|------|---------|
| `app.py` | Flask REST API server (HTTP endpoints) |
| `Procfile` | Render-কে বলে কোন কমান্ড চালাতে হবে |
| `render.yaml` | Render configuration (optional) |
| `.gitignore` | Git থেকে ignore করার ফাইল list |

### **Documentation** (গাইড ফাইল)
| ফাইল | বিষয় |
|------|------|
| `README.md` | সম্পূর্ণ প্রজেক্ট documentation |
| `DEPLOYMENT.md` | বিস্তারিত deployment গাইড (ইংরেজি) |
| `QUICK_START_BN.md` | দ্রুত শুরু গাইড (বাংলা) |

### **Automation** (GitHub Actions)
| ফাইল | কাজ |
|------|-----|
| `.github/workflows/scrape.yml` | সপ্তাহে একবার automatic scraping |

### **Configuration**
| ফাইল | ব্যবহার |
|------|--------|
| `.env.example` | Environment variables template |
| `requirements.txt` | Updated with Flask & dependencies |

---

## 🎯 কাজের ফ্লো

```
Step 1: GitHub Repo তৈরি করুন
    ↓
Step 2: Code push করুন (git push)
    ↓
Step 3: Render-এ deploy করুন (auto-deploy)
    ↓
Step 4: API দিয়ে scraping শুরু করুন
    ↓
Step 5: Data download করুন (JSON/CSV)
    ↓
Step 6: (Optional) GitHub Actions automation setup
```

---

## 🚀 করার কাজ

### **১. GitHub তে রেপোজিটরি তৈরি করুন**

```bash
cd /home/redden/Downloads/ScrepingDelhi

# Git initialize করুন
git init
git add .
git commit -m "Initial commit - scraper setup"

# GitHub-এ যান: github.com/new
# Repository name: scraping-delhi
# Public or Private যেটা চান নির্বাচন করুন

# Local repo-কে remote এর সাথে connect করুন:
git remote add origin https://github.com/YOUR_USERNAME/scraping-delhi.git
git branch -M main
git push -u origin main
```

### **২. Render-এ Deploy করুন**

1. https://render.com এ যান (Free account তৈরি করুন)
2. **Dashboard → New → Web Service**
3. **GitHub** select করুন → `scraping-delhi` search করুন
4. **Connect করুন**
5. Settings:
   - Name: `scraping-delhi`
   - Build Command: 
     ```
     pip install -r requirements.txt && playwright install chromium
     ```
   - Start Command: `python app.py`
   - Region: Singapore বা India (আপনার কাছাকাছি)
   - Plan: Standard ($7/month) বা Free tier দিয়ে শুরু করুন

6. **Create Web Service** বাটন চাপুন

**Deploy হতে ৫-১০ মিনিট সময় লাগবে।**

---

## 📡 API Endpoints

যখন deploy হয়ে যাবে, আপনার URL হবে:
```
https://scraping-delhi.onrender.com
```

### **Test করুন:**
```bash
curl https://scraping-delhi.onrender.com/health
```

### **Main Endpoints:**

| Method | Endpoint | কাজ |
|--------|----------|-----|
| GET | `/health` | Health check |
| GET | `/` | API documentation |
| POST | `/api/scrape/keyword` | Scraping শুরু করুন |
| GET | `/api/jobs/<job_id>` | Status চেক করুন |
| GET | `/api/download/<job_id>` | JSON download করুন |
| GET | `/api/download-csv/<job_id>` | CSV download করুন |
| GET | `/api/jobs` | সব jobs দেখুন |

---

## 💻 ব্যবহারের উদাহরণ

### **Scraping শুরু করুন:**
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
  "download_url": "/api/download/job_20240703_143022"
}
```

### **Status চেক করুন:**
```bash
curl https://scraping-delhi.onrender.com/api/jobs/job_20240703_143022
```

### **Data download করুন:**

**Browser থেকে:**
```
https://scraping-delhi.onrender.com/api/download/job_20240703_143022
```

**Terminal থেকে:**
```bash
curl -o data.json \
  https://scraping-delhi.onrender.com/api/download/job_20240703_143022
```

**Python দিয়ে:**
```python
import requests

response = requests.get(
    "https://scraping-delhi.onrender.com/api/download/job_20240703_143022"
)
data = response.json()
print(f"Scraped {len(data)} records")
```

---

## 🤖 GitHub Actions Setup (Optional)

Automatic weekly scraping চালানোর জন্য:

1. GitHub repo → **Settings → Secrets and variables → Actions**
2. **New repository secret** তে যোগ করুন:
   - **Name**: `RENDER_API_URL`
   - **Value**: `https://scraping-delhi.onrender.com`

3. **Actions → Automated Scraping → Run workflow**

এখন প্রতি সপ্তাহে রবিবার সকাল ২টায় automatic scraping হবে।

---

## 📊 Output ফরম্যাট

প্রতিটি record এ আছে:
```json
{
  "gmaps_url": "https://www.google.com/maps/place/...",
  "gmaps_name": "Studio/DJ Name",
  "gmaps_address": "Full Address",
  "gmaps_phone": "+91 98765 43210",
  "gmaps_rating": "4.8",
  "gmaps_reviews_count": "123",
  "gmaps_category": "Photography studio",
  "gmaps_website": "https://website.com",
  "gmaps_about": "About description..."
}
```

---

## ⚠️ গুরুত্বপূর্ণ নোট

| বিষয় | মনে রাখবেন |
|------|-----------|
| **Memory** | Render-এ 2GB memory দিন (Chromium চলানোর জন্য) |
| **Free Tier** | Services ১৫ মিনিট inactivity পরে spin down হয় |
| **Rate Limit** | Google Maps rate limiting করতে পারে - delays বাড়ান |
| **Data Storage** | Render-এ temp storage - persistent storage লাগলে DB যোগ করুন |
| **Cost** | Free tier দিয়ে শুরু করুন, পরে প্রয়োজন অনুযায়ী upgrade করুন |

---

## 🔍 Monitoring

### **Logs দেখুন:**
1. https://render.com/dashboard
2. Service select করুন
3. **Logs** tab-এ যান

### **Performance Monitor করুন:**
- CPU usage
- Memory usage
- Request count
- Error rate

---

## 🐛 সাধারণ সমস্যা ও সমাধান

### ❌ "Playwright not found"
```
❓ কারণ: Chromium install হয়নি
✅ সমাধান: Build command চেক করুন - 
         playwright install chromium আছে কিনা
```

### ❌ "Service keeps restarting"
```
❓ কারণ: Memory overflow
✅ সমাধান: Render dashboard → Increase memory to 2GB+
```

### ❌ "Requests timeout"
```
❓ কারণ: Google rate limiting
✅ সমাধান: JITTER_PRE & JITTER_GOTO values বাড়ান (scrap_main.py)
```

### ❌ "Data not saving"
```
❓ কারণ: Permission issue
✅ সমাধান: outputs/ folder create হচ্ছে কিনা চেক করুন
```

---

## 📚 আরও তথ্যের জন্য

- **Deployment guide**: [DEPLOYMENT.md](DEPLOYMENT.md)
- **Quick start (Bengali)**: [QUICK_START_BN.md](QUICK_START_BN.md)
- **Project README**: [README.md](README.md)
- **Render docs**: https://render.com/docs
- **Playwright docs**: https://playwright.dev/python/

---

## ✨ সবকিছু চেক লিস্ট

- [ ] GitHub account তৈরি করেছি
- [ ] Local repo git initialize করেছি
- [ ] GitHub-এ repository তৈরি করেছি
- [ ] Code push করেছি (git push)
- [ ] Render account তৈরি করেছি
- [ ] Render এ deploy করেছি
- [ ] Health check টেস্ট করেছি (`/health`)
- [ ] একটি scraping job চালু করেছি
- [ ] Data download করেছি

---

## 🎉 সফলতার গল্প

যখন সব কিছু কাজ করবে:

1. ✅ API call করবেন
2. ✅ Scraping হবে
3. ✅ Data save হবে
4. ✅ Download করতে পারবেন
5. ✅ GitHub automation চলবে

---

**শুভকামনা! 🚀**

কোনো প্রশ্ন থাকলে documentation ফাইলগুলো দেখুন।
