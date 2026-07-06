"""
Flask web server for scraper deployment on Render.
Provides HTTP endpoints to trigger scraping and download results.
"""

import asyncio
import json
import os
import logging
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS

from scrap_main import GoogleMapsKeywordScraper, ContextPool
from playwright.async_api import async_playwright

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Install Chromium at runtime (Render does not persist build cache to runtime)
logger.info("Installing Chromium...")
result = subprocess.run(
    [sys.executable, "-m", "playwright", "install", "chromium"],
    capture_output=True, text=True
)
if result.returncode == 0:
    logger.info("Chromium installed successfully")
else:
    logger.warning(f"playwright install failed: {result.stderr}")

app = Flask(__name__)
CORS(app)

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "Data")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

# Store job status
jobs_status = {}


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }), 200


@app.route("/api/scrape/keyword", methods=["POST"])
def scrape_keyword():
    """
    Scrape businesses for a specific keyword.
    POST body: {"keyword": "Photographers in Delhi"}
    Note: Free tier limited to 90 results per job
    """
    try:
        data = request.get_json()
        keyword = data.get("keyword", "").strip()
        max_results = data.get("max_results", 90)  # Default: small jobs
        
        if not keyword:
            return jsonify({"error": "keyword is required"}), 400
        
        # Limit max_results for free tier
        if max_results > 90:
            max_results = 90
            logger.info(f"Limiting results to 90 for free tier")
        
        job_id = f"job_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        output_file = os.path.join(OUTPUT_DIR, f"{job_id}.json")
        
        # Update job status
        jobs_status[job_id] = {
            "status": "running",
            "keyword": keyword,
            "created_at": datetime.now().isoformat(),
            "output_file": output_file
        }
        
        # Run async scraper (optimized for free tier)
        try:
            scraper = GoogleMapsKeywordScraper(keyword, output_file)
            # For free tier: use 2 workers max
            scraper.scrape_all(max_workers=2)
            
            jobs_status[job_id]["status"] = "completed"
            jobs_status[job_id]["completed_at"] = datetime.now().isoformat()
            
            # Count records
            if os.path.exists(output_file):
                with open(output_file) as f:
                    records = json.load(f)
                    jobs_status[job_id]["record_count"] = len(records)
            
            return jsonify({
                "job_id": job_id,
                "status": "completed",
                "keyword": keyword,
                "max_results_limit": 90,
                "note": "Free tier - limited to 90 results",
                "download_url": f"/api/download/{job_id}"
            }), 200
            
        except Exception as e:
            jobs_status[job_id]["status"] = "failed"
            jobs_status[job_id]["error"] = str(e)
            logger.error(f"Scraping failed: {e}")
            return jsonify({
                "job_id": job_id,
                "status": "failed",
                "error": str(e)
            }), 500
    
    except Exception as e:
        logger.error(f"Request error: {e}")
        return jsonify({"error": str(e)}), 400


@app.route("/api/jobs/<job_id>", methods=["GET"])
def get_job_status(job_id):
    """Get status of a specific job."""
    if job_id not in jobs_status:
        return jsonify({"error": "Job not found"}), 404
    
    return jsonify(jobs_status[job_id]), 200


@app.route("/api/download/<job_id>", methods=["GET"])
def download_results(job_id):
    """Download scraped data as JSON."""
    if job_id not in jobs_status:
        return jsonify({"error": "Job not found"}), 404
    
    output_file = jobs_status[job_id].get("output_file")
    
    if not output_file or not os.path.exists(output_file):
        return jsonify({"error": "Output file not found"}), 404
    
    return send_file(
        output_file,
        as_attachment=True,
        download_name=f"{job_id}.json",
        mimetype="application/json"
    )


@app.route("/api/download-csv/<job_id>", methods=["GET"])
def download_csv(job_id):
    """Download results as CSV."""
    if job_id not in jobs_status:
        return jsonify({"error": "Job not found"}), 404
    
    output_file = jobs_status[job_id].get("output_file")
    
    if not output_file or not os.path.exists(output_file):
        return jsonify({"error": "Output file not found"}), 404
    
    try:
        import pandas as pd
        
        with open(output_file) as f:
            data = json.load(f)
        
        df = pd.DataFrame(data)
        csv_file = output_file.replace(".json", ".csv")
        df.to_csv(csv_file, index=False)
        
        return send_file(
            csv_file,
            as_attachment=True,
            download_name=f"{job_id}.csv",
            mimetype="text/csv"
        )
    except Exception as e:
        logger.error(f"CSV conversion error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/jobs", methods=["GET"])
def list_jobs():
    """List all jobs and their status."""
    return jsonify(jobs_status), 200


@app.route("/", methods=["GET"])
def index():
    """API documentation."""
    return jsonify({
        "name": "Scraping Delhi API",
        "version": "1.0",
        "endpoints": {
            "health": "GET /health",
            "scrape": "POST /api/scrape/keyword",
            "job_status": "GET /api/jobs/<job_id>",
            "download_json": "GET /api/download/<job_id>",
            "download_csv": "GET /api/download-csv/<job_id>",
            "list_jobs": "GET /api/jobs"
        }
    }), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
