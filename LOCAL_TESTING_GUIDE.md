# 🧪 Local Testing - এখনই করুন!

> আপনার local PC এ test করার complete guide

---

## **BEFORE YOU START**

আপনার কাছে থাকতে হবে:

```
✅ Python 3.7+ (আপনার কাছে আছে)
✅ Playwright installed (requirements.txt এ আছে)
✅ Terminal access (Linux/Mac/Windows সব এ কাজ করে)
✅ This folder: /home/redden/Downloads/ScrepingDelhi
```

---

## **METHOD 1: Terminal (Easy)**

### **Step 1: Terminal খুলুন**

```bash
# Terminal 1 - এটা Server চালাবে
cd /home/redden/Downloads/ScrepingDelhi

# Virtual environment activate করুন (যদি থাকে)
source venv/bin/activate

# app.py run করুন
python app.py
```

**Output দেখবেন:**
```
* Running on http://127.0.0.1:5000
* WARNING: This is a development server. Do not use it in production.
* Press CTRL+C to quit
```

**Server চলছে!**

---

### **Step 2: নতুন Terminal খুলুন** (Separate window)

```bash
# Terminal 2 - এটা request পাঠাবে

# Health check
curl http://127.0.0.1:5000/health

# Output:
# {"status": "healthy", "timestamp": "2024-07-03T..."}
```

✅ **Server respond করছে!**

---

### **Step 3: প্রথম Job চালান**

Terminal 2 এ:

```bash
curl -X POST http://127.0.0.1:5000/api/scrape/keyword \
  -H "Content-Type: application/json" \
  -d '{"keyword": "Photographer in Delhi"}'
```

**Output (Response):**
```json
{
  "job_id": "job_20240703_143022",
  "status": "completed",
  "keyword": "Photographer in Delhi",
  "max_results_limit": 30,
  "note": "Free tier - limited to 30 results",
  "download_url": "/api/download/job_20240703_143022"
}
```

**Copy করুন: job_id** (পরবর্তী step এ লাগবে)

---

### **Step 4: Server Log দেখুন**

Terminal 1 এ (যেখানে server চলছে):

```
127.0.0.1 - - [03/Jul/2024 14:30:22] "POST /api/scrape/keyword HTTP/1.1" 200
```

এখানে সব activity দেখা যাবে!

---

### **Step 5: Job Status Check করুন**

Terminal 2 এ:

```bash
# Replace job_20240703_143022 দিয়ে আপনার job_id
curl http://127.0.0.1:5000/api/jobs/job_20240703_143022

# Output:
# {"status": "completed", "record_count": 25, ...}
```

---

### **Step 6: Data Download করুন**

Terminal 2 এ:

```bash
curl http://127.0.0.1:5000/api/download/job_20240703_143022 \
  -o results.json

# Check file
ls -lh results.json
cat results.json | head -20
```

**সাফল্য! 🎉 Local testing কাজ করছে!**

---

## **METHOD 2: Postman (Professional)**

### **Step 0: Postman Install করুন**

```
https://www.postman.com/downloads/
Download করুন → Install → Open
```

---

### **Step 1: Server চালু করুন** (Terminal)

```bash
cd /home/redden/Downloads/ScrepingDelhi
python app.py

# Output: Running on http://127.0.0.1:5000
```

---

### **Step 2: Postman এ Request তৈরি করুন**

### **Request 1: Health Check**

```
Method: GET
URL: http://127.0.0.1:5000/health

[SEND]

Response:
{
  "status": "healthy",
  "timestamp": "2024-07-03T..."
}
```

---

### **Request 2: Start Scraping Job**

```
Method: POST
URL: http://127.0.0.1:5000/api/scrape/keyword

Headers Tab:
  Key: Content-Type
  Value: application/json

Body Tab:
  Select: raw
  Select: JSON
  
  Content:
  {
    "keyword": "Photographer in Delhi"
  }

[SEND]

Response:
{
  "job_id": "job_20240703_143022",
  "status": "completed",
  "record_count": 25,
  "download_url": "/api/download/job_20240703_143022"
}
```

**Copy করুন: job_id**

---

### **Request 3: Check Job Status**

```
Method: GET
URL: http://127.0.0.1:5000/api/jobs/job_20240703_143022

[SEND]

Response:
{
  "status": "completed",
  "keyword": "Photographer in Delhi",
  "record_count": 25,
  "created_at": "2024-07-03T14:30:22",
  "completed_at": "2024-07-03T14:40:33"
}
```

---

### **Request 4: Download Data**

```
Method: GET
URL: http://127.0.0.1:5000/api/download/job_20240703_143022

[SEND]

Response Tab এ JSON দেখবেন:
[
  {
    "gmaps_url": "https://www.google.com/maps/place/...",
    "gmaps_name": "Studio Name",
    "gmaps_address": "Address",
    ...
  },
  ...
]

Save করতে:
  [Save Response]
  Select: Save to file
  Choose location & filename
```

---

## **METHOD 3: Browser (Simplest)**

### **Step 1: Server চালু করুন**

```bash
python app.py
```

---

### **Step 2: Browser এ খুলুন**

```
http://127.0.0.1:5000/
```

**দেখবেন:**
```json
{
  "name": "Scraping Delhi API",
  "version": "1.0",
  "endpoints": {
    "health": "GET /health",
    "scrape": "POST /api/scrape/keyword",
    ...
  }
}
```

---

### **Step 3: Health Check**

```
http://127.0.0.1:5000/health
```

**Response:**
```json
{"status": "healthy", "timestamp": "..."}
```

---

### **Step 4: Download Data** (সহজ!)

একবার job চালানোর পর:

```
http://127.0.0.1:5000/api/download/job_20240703_143022
```

**File auto-download হবে!**

---

## **Troubleshooting**

### ❌ Error: "Connection refused"

```
Reason: Server চলছে না
Solution:
  Terminal 1 এ python app.py আছে কিনা চেক করুন
  না থাকলে চালান
```

---

### ❌ Error: "localhost not found"

```
Reason: URL গলত
Solution:
  Check: http://127.0.0.1:5000
  NOT: http://localhost:5000 (sometimes doesn't work)
```

---

### ❌ Error: Port 5000 already in use

```
Reason: অন্য কিছু port 5000 use করছে
Solution:
  app.py এ change করুন:
  app.run(port=5001, ...)
  
  Then use: http://127.0.0.1:5001
```

---

### ❌ Error: "ModuleNotFoundError"

```
Reason: Dependencies install নেই
Solution:
  pip install -r requirements.txt
  playwright install chromium
```

---

## **Real-time Testing Sequence**

```
TIME    ACTION                  WHERE              STATUS
────────────────────────────────────────────────────────────
T+0     Start server            Terminal 1         Server starting...
T+2     Check health            Terminal 2 / curl  ✅ Healthy
T+5     POST scrape job         Postman            ✅ Job created
T+10    Scraping running        Server logs        📊 In progress
T+20    Job completes           Server logs        ✅ Done
T+21    Check status            Terminal 2 / GET   ✅ Completed
T+22    Download data           Terminal 2 / curl  ✅ results.json saved
T+23    Verify data             cat results.json   ✅ 25 records
────────────────────────────────────────────────────────────
        TOTAL TIME: ~23 MINUTES
```

---

## **Common Testing Keywords**

```bash
# ছোট keyword (দ্রুত)
"Photographer Delhi"

# মাঝারি keyword
"Wedding photographer Delhi"

# বড় keyword (আরও data)
"DJ Delhi"

# Specific
"Studio in Delhi"

# City specific
"Photographer in New Delhi"
```

---

## **Success Checklist**

```
✅ Server starts without error
✅ Health check returns 200
✅ POST request returns job_id
✅ Job status shows "completed"
✅ Record count > 0
✅ JSON data downloads
✅ Data contains photographer names
✅ Logs visible in server terminal
✅ Can run multiple jobs
✅ Each job creates unique job_id
```

---

## **Next Steps**

### After Local Testing Works:

1. ✅ Local testing passed? **YES!**
2. 👉 Deploy to Render (STEP_BY_STEP_DEPLOY_BN.md)
3. 👉 Use production API
4. 👉 Setup automation (GitHub Actions)
5. 👉 Scale as needed

---

## **Command Reference (Copy-Paste)**

### Terminal 1 - Start Server:
```bash
cd /home/redden/Downloads/ScrepingDelhi
python app.py
```

### Terminal 2 - Test Commands:

```bash
# Health
curl http://127.0.0.1:5000/health

# Start job
curl -X POST http://127.0.0.1:5000/api/scrape/keyword \
  -H "Content-Type: application/json" \
  -d '{"keyword": "Photographer Delhi"}'

# Check status (replace JOB_ID)
curl http://127.0.0.1:5000/api/jobs/JOB_ID

# Download
curl http://127.0.0.1:5000/api/download/JOB_ID -o data.json

# View data
cat data.json | head -20

# List all jobs
curl http://127.0.0.1:5000/api/jobs
```

---

**এখন শুরু করুন! 🚀**

Local test করে নিশ্চিত করুন সবকিছু কাজ করছে।
তারপর Render-এ deploy করুন।
