"""
bulk_scraper.py  –  Optimised async Playwright bulk scraper.

Key optimisations over v1:
  ① Shared ContextPool   — one pool of N reusable BrowserContexts for ALL
                            locations, created once at start-up.  No per-URL
                            context create/destroy overhead.
  ② Queue-based workers  — location workers pull from an asyncio.Queue instead
                            of waiting for a whole batch to finish.  All
                            LOCATION_WORKERS slots stay busy at all times.
  ③ Tuned concurrency    — LOCATION_WORKERS=8, CTX_POOL_SIZE=20 (was 6 / 12).
                            Adjust based on available RAM (~80 MB per context).
  ④ Reduced break times  — medium break cut to 60-120 s (was 300-600 s).
                            Long break unchanged for stealth safety.
"""

import asyncio
import json
import logging
import os
import random
import re
import time
from pathlib import Path

import pandas as pd
from playwright.async_api import async_playwright

from scrap_main import GoogleMapsKeywordScraper, ContextPool

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Config  (tune to your machine)
# ---------------------------------------------------------------------------
BASE_DIR       = os.path.dirname(os.path.abspath(__file__))
LOCATIONS_FILE = os.path.join(BASE_DIR, "Top_2k_Delhi_NCR_ARE_covered.xlsx")
DATA_DIR       = os.path.join(BASE_DIR, "Data")
PROGRESS_FILE  = os.path.join(BASE_DIR, "progress.json")

# ① Each location task uses the shared pool; these control parallelism:
LOCATION_WORKERS = 2    # how many locations are scraped concurrently
CTX_POOL_SIZE    = 3   # total reusable BrowserContexts
                        # rule of thumb: CTX_POOL_SIZE >= LOCATION_WORKERS * 2
                        # RAM: ~80 MB per context → 20 ctx ≈ 1.6 GB


# ---------------------------------------------------------------------------
# Progress helpers  (unchanged from v1)
# ---------------------------------------------------------------------------

def load_progress() -> dict:
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE) as f:
            data = json.load(f)
        if isinstance(data, list):
            return {"completed": set(data), "started": set()}
        return {
            "completed": set(data.get("completed", [])),
            "started":   set(data.get("started",   [])),
        }
    return {"completed": set(), "started": set()}


def save_progress(completed: set, started: set):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(
            {"completed": sorted(completed), "started": sorted(started)},
            f, indent=2,
        )


def safe_filename(name: str) -> str:
    return re.sub(r"[^\w\s-]", "", name).strip().replace(" ", "_")


def loc_key(loc: dict) -> str:
    return safe_filename(f"{loc['area']}_{loc['postalCode']}")


def build_keyword(loc: dict) -> str:
    """Build a rich search keyword using all available location fields."""
    area     = str(loc.get("area",     "") or "").strip()
    city     = str(loc.get("city",     "") or "").strip()
    district = str(loc.get("district", "") or "").strip()
    pincode  = str(loc.get("postalCode", "") or "").strip()
    country  = str(loc.get("country",  "") or "").strip()

    # Build location suffix: area, city/district, pincode, country
    parts = [p for p in [area, city or district, pincode, country] if p]
    location_str = " ".join(parts)
    return f"Djs in {location_str}"


def _is_empty_output(path: str) -> bool:
    try:
        with open(path) as f:
            return len(json.load(f)) == 0
    except Exception:
        return True


# ---------------------------------------------------------------------------
# Async break strategy  (medium break shortened)
# ---------------------------------------------------------------------------

class AsyncBreakStrategy:
    def __init__(self):
        self._completed       = 0
        self._long_break_after = random.uniform(5400, 7200)   # 1.5–2 h unchanged
        self._last_long_break  = time.monotonic()

    async def _sleep(self, seconds: float, label: str):
        logger.info(f"⏸  {label}: {seconds/60:.1f} min")
        await asyncio.sleep(seconds)

    async def on_location_complete(self):
        self._completed += 1
        elapsed = time.monotonic() - self._last_long_break

        if elapsed >= self._long_break_after:
            await self._sleep(
                random.uniform(1200, 2700),
                f"Long break after {elapsed/3600:.2f} h",
            )
            self._last_long_break  = time.monotonic()
            self._long_break_after = random.uniform(5400, 7200)
            return

        if self._completed % 5 == 0:
            # ④ was 300-600 s; cut to 60-120 s
            await self._sleep(
                random.uniform(60, 120),
                f"Medium break after {self._completed} locations",
            )
            return

        delay = random.uniform(5, 15)  # ← was 10-30 s
        logger.info(f"⏳ Next location in {delay:.1f}s")
        await asyncio.sleep(delay)

    async def on_blocked(self):
        await self._sleep(
            random.uniform(1800, 3600),
            "🚨 Blocking detected — emergency pause",
        )
        self._last_long_break  = time.monotonic()
        self._long_break_after = random.uniform(5400, 7200)


# ---------------------------------------------------------------------------
# Per-location scrape task (used by queue workers)
# ---------------------------------------------------------------------------

async def scrape_location(
    loc: dict,
    pool: ContextPool,
    completed: set,
    started: set,
    all_count: int,
    breaks: AsyncBreakStrategy,
    progress_lock: asyncio.Lock,
) -> tuple[str, bool, bool]:
    """Scrape one location. Returns (key, success, blocked)."""
    key         = loc_key(loc)
    output_path = os.path.join(DATA_DIR, f"{key}.json")

    async with progress_lock:
        started.add(key)
        save_progress(completed, started)

    await asyncio.sleep(random.uniform(0.5, 2.0))  # ← was 1-3 s

    keyword = build_keyword(loc)
    logger.info(f"▶ Starting: {keyword}")

    try:
        scraper = GoogleMapsKeywordScraper(keyword, output_path)
        # Pass shared pool; max_workers = pool size / location workers
        await scraper.scrape_all_async(
            pool._browser, pool,
            max_workers=max(2, CTX_POOL_SIZE // LOCATION_WORKERS),
        )

        blocked = os.path.exists(output_path) and _is_empty_output(output_path)
        if blocked:
            logger.warning(f"⚠ Empty results for {key} — possible block")

        logger.info(f"✓ Done: {key}")
        return key, True, blocked

    except Exception as exc:
        logger.error(f"✗ Failed: {key} — {exc}")
        return key, False, True


# ---------------------------------------------------------------------------
# ② Queue-based location consumer
# ---------------------------------------------------------------------------

async def location_worker(
    worker_id: int,
    loc_queue: asyncio.Queue,
    pool: ContextPool,
    completed: set,
    started: set,
    all_count: int,
    breaks: AsyncBreakStrategy,
    progress_lock: asyncio.Lock,
):
    while True:
        loc = await loc_queue.get()
        if loc is None:            # sentinel
            loc_queue.task_done()
            break

        key, success, blocked = await scrape_location(
            loc, pool, completed, started, all_count, breaks, progress_lock,
        )

        if blocked:
            await breaks.on_blocked()

        if success:
            async with progress_lock:
                completed.add(key)
                started.discard(key)
                save_progress(completed, started)
            logger.info(f"[W{worker_id}] Progress: {len(completed)}/{all_count}")
            await breaks.on_location_complete()

        loc_queue.task_done()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

async def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    while True:
        try:
            await _run()
            break
        except Exception as exc:
            logger.error(f"Top-level crash ({exc}), restarting in 30s…")
            await asyncio.sleep(30)


async def _run():  # noqa: C901
    os.makedirs(DATA_DIR, exist_ok=True)

    df = pd.read_excel(LOCATIONS_FILE)
    df = df[["area", "city", "district", "state", "country", "postalCode"]].dropna(
        subset=["area"]
    )
    all_locations = df.to_dict("records")
    logger.info(f"Total locations: {len(all_locations)}")

    progress  = load_progress()
    completed = progress["completed"]
    started   = progress["started"]

    if started:
        recovered = {k for k in started if not _is_empty_output(os.path.join(DATA_DIR, f"{k}.json"))}
        if recovered:
            logger.info(f"↩ Auto-completing {len(recovered)} location(s) with existing data")
            completed.update(recovered)
        requeue = started - recovered
        if requeue:
            logger.info(f"↩ Re-queuing {len(requeue)} incomplete location(s)")
        started.clear()
        save_progress(completed, started)

    pending = [loc for loc in all_locations if loc_key(loc) not in completed]

    logger.info("=" * 60)
    logger.info(f"Total    : {len(all_locations)}")
    logger.info(f"Completed: {len(completed)}")
    logger.info(f"Pending  : {len(pending)}")
    logger.info(f"Workers  : {LOCATION_WORKERS} locations × ~{CTX_POOL_SIZE // LOCATION_WORKERS} detail ctx")
    logger.info(f"Pool     : {CTX_POOL_SIZE} total contexts")
    logger.info("=" * 60)

    if not pending:
        logger.info("All locations already scraped!")
        return

    breaks        = AsyncBreakStrategy()
    progress_lock = asyncio.Lock()

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--disable-extensions",
                "--memory-pressure-off",
                "--disable-blink-features=AutomationControlled",
            ],
        )

        # ① Create one shared pool for the whole run
        pool = ContextPool(browser, size=CTX_POOL_SIZE)
        pool._browser = browser          # make browser accessible to scraper
        await pool.initialize()

        # ② Fill the queue and start workers
        loc_queue: asyncio.Queue = asyncio.Queue()
        for loc in pending:
            await loc_queue.put(loc)
        for _ in range(LOCATION_WORKERS):   # sentinels
            await loc_queue.put(None)

        workers = [
            asyncio.create_task(
                location_worker(
                    i, loc_queue, pool, completed, started,
                    len(all_locations), breaks, progress_lock,
                )
            )
            for i in range(LOCATION_WORKERS)
        ]

        try:
            await asyncio.gather(*workers)
        except Exception as exc:
            logger.error(f"Worker crash: {exc}")
        finally:
            try:
                await pool.close()
            except Exception:
                pass
            try:
                await browser.close()
            except Exception:
                pass

    logger.info("🎉 All done!")


if __name__ == "__main__":
    asyncio.run(main())