# 🚀 Deploy করার কমান্ড - Copy-Paste করুন!

> এই সব কমান্ড terminal এ run করুন একের পর এক

---

## 📋 **Phase 1: Local Setup** (10 মিনিট)

```bash
# 1. সঠিক folder এ যান
cd /home/redden/Downloads/ScrepingDelhi

# 2. Git configure করুন (প্রথমবার only)
git config --global user.name "Your Name"
git config --global user.email "your.email@gmail.com"

# 3. Repository initialize করুন
git init

# 4. সব ফাইল add করুন
git add .

# 5. Commit করুন
git commit -m "Initial scraper setup for Render"

# 6. Check status
git status
```

---

## 🐙 **Phase 2: GitHub করুন** (মাত্র ওয়েব ব্রাউজার)

### Website এ:
```
1. https://github.com/signup
   → Account তৈরি করুন

2. https://github.com/new
   → Repository name: scraping-delhi
   → Create repository

3. Copy করুন URL: https://github.com/YOUR_USERNAME/scraping-delhi
```

---

## 📤 **Phase 3: Code Push করুন** (Terminal - 5 মিনিট)

```bash
# Replace করুন YOUR_USERNAME আপনার GitHub username দিয়ে

git remote add origin https://github.com/YOUR_USERNAME/scraping-delhi.git
git branch -M main
git push -u origin main

# GitHub password দিন যখন চাবে
```

---

## 🏗️ **Phase 4: Render Deploy করুন** (ওয়েব ব্রাউজার - 15 মিনিট)

### Website এ:
```
1. https://render.com/signup
   → GitHub দিয়ে signup করুন

2. https://render.com/dashboard
   → "New +" → "Web Service"

3. Select: "Deploy an existing repository"
   → Search: scraping-delhi
   → Connect

4. Configuration:
   Name: scraping-delhi
   Runtime: Python 3
   Region: Singapore
   Branch: main

5. Build Command:
   pip install -r requirements.txt && playwright install chromium

6. Start Command:
   python app.py

7. Plan: Free (শুরুতে)

8. "Create Web Service" ক্লিক করুন
```

**Wait করুন 5-10 minutes, status "Live" না হওয়া পর্যন্ত**

---

## ✅ **Phase 5: Testing করুন** (Terminal - 15 মিনিট)

### A. Health Check:
```bash
curl https://scraping-delhi.onrender.com/health
```

**Expected:**
```
{"status": "healthy", "timestamp": "..."}
```

---

### B. প্রথম Scraping Job:

```bash
curl -X POST https://scraping-delhi.onrender.com/api/scrape/keyword \
  -H "Content-Type: application/json" \
  -d '{"keyword": "Photographers Delhi"}'
```

**Expected:**
```json
{
  "job_id": "job_20240703_XXXXX",
  "status": "completed",
  "max_results_limit": 30,
  "download_url": "/api/download/job_20240703_XXXXX"
}
```

**Copy করুন: job_id**

---

### C. Status Check করুন:

```bash
# Replace JOB_ID দিয়ে আপনার job_id
curl https://scraping-delhi.onrender.com/api/jobs/job_20240703_XXXXX
```

**Expected:**
```json
{
  "status": "completed",
  "record_count": 25,
  "keyword": "Photographers Delhi"
}
```

---

### D. Data Download করুন:

```bash
# JSON Format
curl https://scraping-delhi.onrender.com/api/download/job_20240703_XXXXX \
  -o results.json

# Check file
ls -lh results.json
cat results.json | head -10
```

---

## 🔄 **Regular Usage - প্রতিবার** 

```bash
# 1. নতুন keyword দিয়ে scrape করুন
curl -X POST https://scraping-delhi.onrender.com/api/scrape/keyword \
  -H "Content-Type: application/json" \
  -d '{"keyword": "DJs in Delhi"}'

# 2. Job ID copy করুন response থেকে

# 3. Download করুন
curl https://scraping-delhi.onrender.com/api/download/JOB_ID \
  -o data.json

# 4. File check করুন
cat data.json | head -20
```

---

## 📊 **All Jobs দেখুন**

```bash
curl https://scraping-delhi.onrender.com/api/jobs
```

---

## 🌐 **Browser দিয়েও করতে পারেন**

### Health Check:
```
https://scraping-delhi.onrender.com/health
```

### API Docs:
```
https://scraping-delhi.onrender.com/
```

### Download Direct Link:
```
https://scraping-delhi.onrender.com/api/download/job_20240703_XXXXX
```

---

## 📝 **খুব দ্রুত যদি ভুলে যান**

### Quick Reference:
```
Your API: https://scraping-delhi.onrender.com

POST /api/scrape/keyword
  Body: {"keyword": "Photographers Delhi"}
  
GET /api/download/<job_id>
  Download: results.json

GET /api/health
  Test: কাজ করছে কিনা
```

---

## ❌ **যদি Error হয়**

```bash
# 1. Log দেখুন (Render Dashboard → Logs)

# 2. Restart service (Render Dashboard → Manual Deploy)

# 3. Check করুন সব command সঠিক copy করেছেন

# 4. 5 মিনিট অপেক্ষা করুন (deployment থেকে)
```

---

## 💡 **শর্টকাট**

```bash
# সব একসাথে test করতে:

# 1. Git push করুন (যদি changes হয়)
git add .
git commit -m "Updates"
git push

# 2. Render auto-redeploy হবে (~3 min)

# 3. Test করুন
curl https://scraping-delhi.onrender.com/health

# 4. Scrape করুন
curl -X POST https://scraping-delhi.onrender.com/api/scrape/keyword \
  -H "Content-Type: application/json" \
  -d '{"keyword": "Photographers Delhi"}'
```

---

## ✨ **Success Indicators**

```bash
# যখন সব কাজ করছে:

✅ Health check returns 200
✅ Scraping job completes
✅ Record count > 0
✅ File downloads successfully
✅ JSON has data
```

---

## 🎯 **Problems?**

| Problem | Solution |
|---------|----------|
| Build failed | Check Render logs, retry |
| Service timeout | Increase timeout, use Standard plan |
| No data scraped | Check keyword, verify network |
| File not downloading | Check job_id, retry download |
| CORS error | Already fixed in code |

---

**Happy Deploying! 🚀**

প্রতিটি command এক এক করে run করুন এবং আগেরটা complete হওয়ার জন্য অপেক্ষা করুন।
