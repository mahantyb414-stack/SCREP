# 📚 সম্পূর্ণ Deploy গাইড - স্টেপ বাই স্টেপ

> **জন্য:** আপনার Google Maps Scraper কে Render-এ চালু করতে  
> **সময়:** ~১ ঘণ্টা  
> **খরচ:** FREE (শুরুতে)

---

## 🎯 সবকিছুর ওভারভিউ

```
Your Code
   ↓ (Step 1-3)
GitHub Repository
   ↓ (Step 4-6)
Render Server (Live!)
   ↓ (Step 7-9)
API Running
   ↓ (Step 10)
Scraping & Download Data
```

---

# ✅ STEP-BY-STEP DEPLOYMENT

## **STEP 1: Git Repository Initialize করুন** (5 মিনিট)

যেটা terminal এ করবেন:

```bash
# 1.1: সঠিক folder এ যান
cd /home/redden/Downloads/ScrepingDelhi

# 1.2: Check করুন git installed আছে কিনা
git --version
# Output হওয়া উচিত: git version 2.x.x

# 1.3: Git configure করুন (প্রথমবার)
git config --global user.name "Your Name"
git config --global user.email "your.email@gmail.com"

# 1.4: Repository initialize করুন
git init

# 1.5: সব ফাইল add করুন
git add .

# 1.6: Commit করুন
git commit -m "Initial commit - scraper setup for Render deployment"

# 1.7: Check status
git status
# Output: "On branch master/main, nothing to commit"
```

✅ **চেক করুন:**
- `git status` কোন error দেখায় না
- সব ফাইল committed দেখা যায়

---

## **STEP 2: GitHub Account তৈরি করুন** (5 মিনিট)

### 2.1: GitHub যান
```
https://github.com/signup
```

### 2.2: ফর্ম ভরুন
- **Email**: আপনার email
- **Password**: Strong password
- **Username**: কিছু সহজ (যেমন: `redden-scraper`)

### 2.3: Verify করুন
- Email verification link ক্লিক করুন
- GitHub এ login করুন

✅ **চেক করুন:**
- GitHub dashboard এ আছেন
- "Create repository" button দেখা যায়

---

## **STEP 3: GitHub Repository তৈরি করুন** (3 মিনিট)

### 3.1: GitHub এ নতুন repo বানান
```
https://github.com/new
```

### 3.2: ফর্ম ভরুন:
```
Repository name: scraping-delhi
Description: Google Maps photographer & DJ scraper
Visibility: Public (GitHub Pages এর জন্য)
Initialize with: DON'T check anything (আমরা local push করব)
```

### 3.3: "Create repository" ক্লিক করুন

✅ **আপনি দেখবেন:**
```
https://github.com/YOUR_USERNAME/scraping-delhi
```

এই URL copy করুন (পরবর্তী step এ লাগবে)

---

## **STEP 4: Local Code কে GitHub এ Push করুন** (5 মিনিট)

Terminal এ:

```bash
# 4.1: GitHub repository কে remote হিসেবে add করুন
# REPLACE করুন YOUR_USERNAME দিয়ে
git remote add origin https://github.com/YOUR_USERNAME/scraping-delhi.git

# 4.2: Branch rename করুন
git branch -M main

# 4.3: Code GitHub এ push করুন
git push -u origin main
# GitHub username password চাইবে (আপনার login info দিন)
```

**যদি error হয়:**
```bash
# Error: "fatal: remote origin already exists"
# সমাধান:
git remote remove origin
# Then retry step 4.1
```

✅ **চেক করুন:**
- GitHub page refresh করুন
- সব Python files দেখা যায়
- README.md, app.py, requirements.txt দৃশ্যমান

---

## **STEP 5: Render Account তৈরি করুন** (3 মিনিট)

### 5.1: Render যান
```
https://render.com
```

### 5.2: "Sign Up" ক্লিক করুন

### 5.3: GitHub দিয়ে Login করুন (সহজ)
```
"Continue with GitHub" বাটন
→ আপনার GitHub account select করুন
→ Authorize করুন
```

### 5.4: Dashboard দেখবেন

✅ **চেক করুন:**
- Render dashboard এ আছেন
- "New +" বাটন দেখা যায়

---

## **STEP 6: Render এ Web Service Deploy করুন** (10 মিনিট)

### 6.1: Dashboard এ "New +" → "Web Service" ক্লিক করুন

### 6.2: Repository Connect করুন
```
"Connect your GitHub repository" page এ:
  - Search করুন: scraping-delhi
  - Select করুন আপনার repo
  - "Connect" ক্লিক করুন
```

### 6.3: Configuration Set করুন

**এই field গুলো fill করুন:**

```
Name:
  scraping-delhi

Environment:
  Python 3

Region:
  Singapore (Asia এ best) 
  অথবা কাছাকাছি region

Branch:
  main
```

### 6.4: Build & Start Commands

**Build Command:**
```
pip install -r requirements.txt && playwright install chromium
```
*(Copy-paste এই exact text)*

**Start Command:**
```
python app.py
```
*(Copy-paste এই exact text)*

### 6.5: Plan নির্বাচন করুন
```
Free (শুরুতে)
  - $0/month
  - 512 MB RAM
  - Spins down every 15 min
  
Standard ($7/month) - RECOMMENDED
  - 2 GB RAM
  - 24/7 uptime
  - Better for production
```

**এখন "Create Web Service" ক্লিক করুন**

✅ **চেক করুন:**
- Render dashboard এ নতুন service দেখা যায়
- Status: "Building..." অথবা "Deploying..."

---

## **STEP 7: Deploy সম্পন্ন হওয়ার জন্য অপেক্ষা করুন** (5-10 মিনিট)

Render dashboard এ যান এবং দেখুন:

```
Status: Building...
  ↓ (2-3 মিনিট)
Status: Deploying...
  ↓ (2-5 মিনিট)
Status: Live ✅ (GREEN)
```

**Logs tab এ দেখুন:**
```
npm install...
Building...
deployed to https://scraping-delhi.onrender.com
Service is live
```

**যখন "Live" (GREEN) দেখবেন, ready!**

✅ **আপনার Service URL:**
```
https://scraping-delhi.onrender.com
```

---

## **STEP 8: Health Check করুন** (1 মিনিট)

Terminal এ:

```bash
# 8.1: Health check URL test করুন
curl https://scraping-delhi.onrender.com/health

# Expected response:
# {"status": "healthy", "timestamp": "2024-07-03T..."}
```

**যদি error হয়:**
```
Error: Connection refused
→ Service এখনও starting, ২-৩ মিনিট অপেক্ষা করুন
```

**যদি successful:**
```
✅ API Server চলছে!
```

---

## **STEP 9: প্রথম Scraping Job চালান** (10 মিনিট)

### 9.1: छোট job দিয়ে test করুন

Terminal এ:

```bash
# 9.1: Scraping শুরু করুন
curl -X POST https://scraping-delhi.onrender.com/api/scrape/keyword \
  -H "Content-Type: application/json" \
  -d '{"keyword": "Photographers Delhi"}'
```

**Response দেখবেন:**
```json
{
  "job_id": "job_20240703_143022",
  "status": "completed",
  "keyword": "Photographers Delhi",
  "max_results_limit": 30,
  "note": "Free tier - limited to 30 results",
  "download_url": "/api/download/job_20240703_143022"
}
```

**Copy করুন: `job_id`** (পরবর্তী step এ লাগবে)

### 9.2: Job Status চেক করুন

```bash
# Replace JOB_ID_HERE দিয়ে আপনার job_id
curl https://scraping-delhi.onrender.com/api/jobs/job_20240703_143022

# Response:
# {"status": "completed", "record_count": 25, ...}
```

---

## **STEP 10: Data Download করুন** (2 মিনিট)

### Option A: JSON Download (সহজ)

```bash
# Terminal দিয়ে download করুন
curl https://scraping-delhi.onrender.com/api/download/job_20240703_143022 \
  -o results.json

# Check করুন
ls -lh results.json
cat results.json | head -20
```

### Option B: Browser দিয়ে Download করুন

এই link browser এ খুলুন:
```
https://scraping-delhi.onrender.com/api/download/job_20240703_143022
```

File automatically download হবে।

### Option C: CSV Format

```bash
curl https://scraping-delhi.onrender.com/api/download-csv/job_20240703_143022 \
  -o results.csv
```

---

# 🎉 **DEPLOYMENT COMPLETE!**

```
✅ GitHub Repository Setup
✅ Render Server Deployed
✅ API Running (Live)
✅ Scraping Tested
✅ Data Downloaded
```

---

## 📊 **Output Data Structure**

আপনার downloaded JSON file এ থাকবে:

```json
[
  {
    "gmaps_url": "https://www.google.com/maps/place/...",
    "gmaps_name": "Studio Name",
    "gmaps_address": "Full Address",
    "gmaps_phone": "+91 98765 43210",
    "gmaps_rating": "4.8",
    "gmaps_reviews_count": "123",
    "gmaps_category": "Photography studio",
    "gmaps_website": "https://website.com"
  },
  ...
]
```

---

## 🔄 **Continuous Usage**

### প্রতিবার Scraping করতে:

```bash
# নতুন keyword দিয়ে
curl -X POST https://scraping-delhi.onrender.com/api/scrape/keyword \
  -H "Content-Type: application/json" \
  -d '{"keyword": "DJ in Delhi"}'

# Job ID পাবেন, download করুন
curl https://scraping-delhi.onrender.com/api/download/JOB_ID \
  -o data_DJ.json
```

### সব jobs দেখুন:

```bash
curl https://scraping-delhi.onrender.com/api/jobs
```

---

## 🚀 **Advanced: GitHub Actions Setup** (Optional)

সাপ্তাহে একবার automatic scraping করতে:

### একবার setup করলে, সবসময় চলবে:

```
আপনার জন্য GitHub Actions:
- প্রতি সপ্তাহে রবিবার সকাল ২টায় run হয়
- 3 different keywords scrape করে
- Data automatically Render এ save হয়
- আপনি download করেন যখন দরকার
```

---

## ⚠️ **Troubleshooting**

### ❌ "Build failed"
```
Check logs in Render → Logs tab
Common issues:
  - playwright install chromium command wrong
  - requirements.txt invalid
  - Solution: Check DEPLOYMENT.md
```

### ❌ "Service keeps restarting"
```
Memory issue (Free tier):
  - Upgrade to Standard ($7/month)
  - OR reduce job size (already done)
```

### ❌ "Timeout error"
```
Google Maps rate limiting:
  - Google thinks you're bot
  - Solution: Increase delays in code
  - Or use specific keywords
```

### ❌ "CORS error"
```
Browser calling API:
  - Already fixed in app.py
  - Should work now
```

---

## 📞 **Support**

**যদি problem হয়:**

1. **Render Logs দেখুন:**
   - Render Dashboard → Service → Logs tab
   - Error message খুঁজুন

2. **Documentation পড়ুন:**
   - DEPLOYMENT.md
   - FREE_TIER_OPTIMIZATION.md
   - README.md

3. **GitHub Issue create করুন:**
   - Your GitHub repo → Issues → New Issue
   - Problem describe করুন

---

## 🎯 **Next Steps**

### Done with Testing?
```
1. ✅ Small jobs test করেছেন
2. ✅ Data download করেছেন
3. → Ready for production!
```

### Production Setup:
```
1. Upgrade to Standard plan ($7/month)
2. Setup GitHub Actions
3. Monitor jobs regularly
4. Scale up as needed
```

---

## ✨ **Summary**

| Step | কী | সময় |
|------|-----|------|
| 1 | Git setup | 5 min |
| 2 | GitHub account | 5 min |
| 3 | GitHub repo | 3 min |
| 4 | Push code | 5 min |
| 5 | Render account | 3 min |
| 6 | Deploy | 10 min |
| 7 | Wait | 5-10 min |
| 8 | Test | 1 min |
| 9 | Run job | 10 min |
| 10 | Download | 2 min |
| **TOTAL** | **Ready!** | **~1 hour** |

---

**আপনি successful হয়েছেন! 🎉**

এখন আপনার Scraper Render-এ live!

---

**Questions?** এই guide এ কোন confusing thing আছে কিনা বলুন।
