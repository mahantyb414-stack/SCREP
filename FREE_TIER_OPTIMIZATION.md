# 🆓 Free Tier (512MB) অপটিমাইজেশন গাইড

## সমস্যা
- Render Free: 512MB RAM
- Chromium + Python: 400-650MB দরকার
- **ফলাফল**: কাজ করবে কিন্তু crash হওয়ার ঝুঁকি আছে

## সমাধান

### **১. Memory Optimization** (app.py এ)

```python
# current values কমিয়ে দিন:

# OLD (Standard plan এর জন্য)
LOCATION_WORKERS = 8
CTX_POOL_SIZE = 20
MAX_WORKERS = 16

# NEW (Free tier এর জন্য)
LOCATION_WORKERS = 1
CTX_POOL_SIZE = 2
MAX_WORKERS = 2
```

### **২. Timeout বাড়ান**

```python
# scrap_main.py এ
MAX_CTX_USES = 30        # ছোট করুন (মেমোরি recycle করতে দেবে)
SCROLL_ITERS = 20        # কম scroll
SAVE_EVERY = 2           # ছোট batch save করুন
```

### **३. Request Limit**

```python
# app.py এ, _pipeline_worker():
MAX_RESULTS = 50         # এক job এ max 50 records scrape করুন
```

### **४. Disable CSV Export** (Memory সাশ্রয়)

```python
# app.py এ CSV endpoint comment করুন
# @app.route("/api/download-csv/<job_id>", methods=["GET"])
# def download_csv(job_id):
#     ... comment out করুন
```

## সীমাবদ্ধতা

Free Tier এ:

| কাজ | পারবেন? | টাইম |
|------|---------|------|
| 10-50 records | ✅ Yes | 5-10 min |
| 100 records | ⚠️ Maybe | 20+ min |
| 500+ records | ❌ No | Crash হবে |
| Multiple jobs | ❌ No | একবারে একটাই করুন |
| 24/7 uptime | ❌ No | Spins down every 15 min |

## Uptime Issue

```
15 minutes inactivity → Service shut down
↓
Next request → Cold start (30 seconds)
↓
Wait করতে হবে service wake up করতে
```

## Best Practice

### Small Scale (Free Tier)
```
1. Manual API calls
2. একবারে একটা keyword
3. 50-100 records limit
4. Testing/demo purposes
5. Occasional use
```

### Production (Standard $7/month)
```
1. GitHub Actions automation
2. Multiple concurrent jobs
3. 1000+ records
4. 24/7 uptime
5. Consistent performance
```

## সুপারিশ

**আমার মতামত:**

1. **যদি শুধু test করতে চান**: Free tier OK
2. **যদি production use চান**: Standard plan upgrade করুন ($7/month)
3. **যদি কোন টাকা নেই**: 
   - AWS Free Tier
   - Heroku (স্পিন-ডাউন আছে)
   - Railway ($5/month)
   - DigitalOcean ($5/month)

---

## কিভাবে Upgrade করবেন?

### Render এ
1. Dashboard → Select service
2. Settings → Plan → Standard
3. Select $7/month plan
4. Confirm

**এই একটা ক্লিক = Production ready!**

---

## ফ্রি টায়ার সাথে থাকার কৌশল

```bash
# 1. প্রথম optimize করুন
# যেসব changes উপরে আছে তা করুন

# 2. Small jobs run করুন
curl -X POST https://scraping-delhi.onrender.com/api/scrape/keyword \
  -d '{"keyword": "DJ in Delhi"}'
# (বড় keyword না করে, specific keyword করুন)

# 3. Monitor করুন
# Logs check করুন crash না হয় কিনা

# 4. যদি ঠিক থাকে → daily use করুন
# যদি crash হয় → Standard upgrade করুন
```

---

## কস্ট ব্রেকডাউন

| Plan | Monthly | Annual | Best For |
|------|---------|--------|----------|
| Free | $0 | $0 | Testing only |
| Standard | $7 | $84 | Production |
| Pro | $50+ | $600+ | High-traffic |

**আমার recommend**: Standard ($7/month) = কফির দাম!

---

**সারাংশ**: Free tier somewhat কাজ করবে কিন্তু risky। Production use এর জন্য $7/month upgrade করুন।
