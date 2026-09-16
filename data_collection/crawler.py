"""
Polite Web Crawler for Real Estate Detail Pages.
Fetches HTML pages with rate-limiting, retries, checkpointing, and incremental saving.
"""

import json
import os
import time
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
import requests
import pandas as pd

from .parser import parse_detail_page

# Set up logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("DetailLocationCrawler")


class DetailLocationCrawler:
    """
    Polite crawler with checkpointing, rate-limiting, retry logic, and incremental CSV saving.
    """

    DEFAULT_USER_AGENT = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36 BDS-Price-Prediction-Research/1.0"
    )

    COLUMNS = [
        "id", "detail_url", "original_location", "title",
        "address_raw", "address_normalized", "street", "ward",
        "district_detail", "province_detail", "address_source",
        "validation_status", "address_category", "crawl_status", "crawl_error"
    ]

    def __init__(
        self,
        output_dir: str = "data/raw/collection",
        csv_filename: str = "detail_locations_sample.csv",
        state_filename: str = "crawler_state.json",
        delay_seconds: float = 1.2,
        timeout_seconds: float = 10.0,
        max_retries: int = 2
    ):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.csv_path = self.output_dir / csv_filename
        self.state_path = self.output_dir / state_filename
        
        self.delay_seconds = delay_seconds
        self.timeout_seconds = timeout_seconds
        self.max_retries = max_retries

        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": self.DEFAULT_USER_AGENT,
            "Accept-Language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
        })

        self.state = self._load_state()

    def _load_state(self) -> Dict[str, Any]:
        """Loads state checkpoint if exists."""
        if self.state_path.exists():
            try:
                with open(self.state_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Could not load state file {self.state_path}: {e}. Starting fresh state.")
        return {}

    def _save_state(self):
        """Saves crawler state atomically to JSON."""
        temp_path = self.state_path.with_suffix(".tmp")
        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(self.state, f, ensure_ascii=False, indent=2)
        os.replace(temp_path, self.state_path)

    def _load_existing_results(self) -> pd.DataFrame:
        """Loads existing CSV results if available."""
        if self.csv_path.exists():
            try:
                df = pd.read_csv(self.csv_path, encoding="utf-8")
                # Ensure all required columns exist
                for col in self.COLUMNS:
                    if col not in df.columns:
                        df[col] = None
                return df[self.COLUMNS]
            except Exception as e:
                logger.warning(f"Could not read existing CSV {self.csv_path}: {e}")
        
        return pd.DataFrame(columns=self.COLUMNS)

    def _save_record_to_csv(self, record: Dict[str, Any]):
        """Appends or updates a record in the CSV file."""
        df_existing = self._load_existing_results()
        
        # Ensure record has all schema keys
        record_clean = {col: record.get(col, None) for col in self.COLUMNS}
        
        rec_id = str(record_clean.get("id"))
        if not df_existing.empty and "id" in df_existing.columns:
            df_existing["id_str"] = df_existing["id"].astype(str)
            if rec_id in df_existing["id_str"].values:
                # Update existing row
                idx = df_existing.index[df_existing["id_str"] == rec_id][0]
                for k, v in record_clean.items():
                    df_existing.loc[idx, k] = v
                df_existing.drop(columns=["id_str"], inplace=True, errors="ignore")
                df_existing[self.COLUMNS].to_csv(self.csv_path, index=False, encoding="utf-8")
                return
            df_existing.drop(columns=["id_str"], inplace=True, errors="ignore")

        # Append new row
        df_new_row = pd.DataFrame([record_clean])
        df_combined = pd.concat([df_existing, df_new_row], ignore_index=True)
        df_combined[self.COLUMNS].to_csv(self.csv_path, index=False, encoding="utf-8")

    def crawl_urls(self, candidate_records: List[Dict[str, Any]]) -> pd.DataFrame:
        """
        Crawls a list of candidate records.
        Each candidate dict must contain: 'id', 'detail_url', 'original_location', 'title'.
        """
        logger.info(f"Starting crawl for {len(candidate_records)} candidate records.")
        
        for idx, item in enumerate(candidate_records, 1):
            url = item.get("detail_url")
            item_id = item.get("id")
            title = item.get("title", "")
            location = item.get("location", item.get("original_location", ""))

            if not url or not isinstance(url, str):
                logger.warning(f"Record {item_id} has invalid URL: {url}. Skipping.")
                continue

            url_key = str(url).strip()
            
            # Check state checkpoint - skip if already successfully collected
            if url_key in self.state and self.state[url_key].get("status") in ["success", "missing_address"]:
                logger.info(f"[{idx}/{len(candidate_records)}] URL already in state ({self.state[url_key]['status']}). Skipping: {url_key}")
                continue

            logger.info(f"[{idx}/{len(candidate_records)}] Requesting ({item_id}): {url_key}")
            
            # Execute request with retry loop
            status, html_content, error_msg = self._fetch_url(url_key)

            record = {
                "id": item_id,
                "detail_url": url_key,
                "original_location": location,
                "title": title,
                "address_raw": None,
                "address_normalized": None,
                "street": None,
                "ward": None,
                "district_detail": None,
                "province_detail": None,
                "address_source": "unknown",
                "validation_status": "insufficient_information",
                "address_category": "missing",
                "crawl_status": status,
                "crawl_error": error_msg
            }

            if status == "success" and html_content:
                try:
                    parsed = parse_detail_page(
                        html_content=html_content,
                        detail_url=url_key,
                        original_title=title,
                        original_location=location
                    )
                    record.update(parsed)
                    
                    if not record["address_raw"]:
                        record["crawl_status"] = "missing_address"
                        record["crawl_error"] = "Address element not found in HTML"

                except Exception as parse_err:
                    logger.error(f"Parse error for {url_key}: {parse_err}")
                    record["crawl_status"] = "parse_error"
                    record["crawl_error"] = str(parse_err)

            # Update state checkpoint
            self.state[url_key] = {
                "id": item_id,
                "status": record["crawl_status"],
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "error": record["crawl_error"]
            }
            self._save_state()

            # Save incremental record to CSV
            self._save_record_to_csv(record)

            # Polite rate limiting delay
            time.sleep(self.delay_seconds)

        logger.info(f"Crawl completed. Results saved to {self.csv_path}")
        return self._load_existing_results()

    def _fetch_url(self, url: str) -> tuple[str, Optional[str], Optional[str]]:
        """
        Fetches HTML with retry logic and polite error handling.
        Returns tuple: (status_code_name, html_content, error_message)
        """
        for attempt in range(self.max_retries + 1):
            try:
                resp = self.session.get(url, timeout=self.timeout_seconds)
                if resp.status_code == 200:
                    return "success", resp.text, None
                else:
                    return "http_error", None, f"HTTP Status {resp.status_code}"

            except requests.exceptions.Timeout:
                if attempt < self.max_retries:
                    logger.warning(f"Timeout on {url}, retrying ({attempt + 1}/{self.max_retries})...")
                    time.sleep(2.0)
                else:
                    return "timeout", None, f"Request timed out after {self.timeout_seconds}s"

            except requests.exceptions.RequestException as req_err:
                if attempt < self.max_retries:
                    logger.warning(f"Request error on {url}, retrying ({attempt + 1}/{self.max_retries}): {req_err}")
                    time.sleep(2.0)
                else:
                    return "http_error", None, str(req_err)

        return "http_error", None, "Max retries exceeded"
