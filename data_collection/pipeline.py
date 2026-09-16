"""
Pipeline orchestrator for Stage 00 Data Collection (Phase 2 - 500 URLs).
Loads raw data, excludes already crawled Phase 1 URLs, samples 450 new candidate URLs,
executes crawl, enriches records, and computes comprehensive quality audit metrics.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Tuple, List
import pandas as pd

from .crawler import DetailLocationCrawler
from .parser import (
    _normalize_address,
    _classify_address_category,
    _validate_location_consistency,
    _extract_raw_address_and_source
)


def load_and_filter_candidates(
    raw_csv_path: str = "data/raw/house_buying_dec29th_2025.csv"
) -> Tuple[pd.DataFrame, Dict[str, int]]:
    """
    Loads raw CSV and filters records belonging to Hồ Chí Minh or Hà Nội.
    Returns filtered candidate DataFrame and dictionary of statistics.
    """
    if not os.path.exists(raw_csv_path):
        raise FileNotFoundError(f"Raw CSV dataset not found at {raw_csv_path}")

    df_raw = pd.read_csv(raw_csv_path)
    total_records = len(df_raw)

    is_hcm = df_raw["location"].astype(str).str.contains("Hồ Chí Minh|HCM|TP.HCM", case=False, na=False)
    is_hn = df_raw["location"].astype(str).str.contains("Hà Nội|HN", case=False, na=False)

    hcm_count = is_hcm.sum()
    hn_count = is_hn.sum()

    df_candidates = df_raw[is_hcm | is_hn].copy()
    candidate_count = len(df_candidates)

    stats = {
        "Total original records": total_records,
        "Hồ Chí Minh records": int(hcm_count),
        "Hà Nội records": int(hn_count),
        "Total candidate records": candidate_count
    }

    return df_candidates, stats


def select_phase2_sample(
    df_candidates: pd.DataFrame,
    existing_csv_path: str = "data/raw/collection/detail_locations_sample.csv",
    target_total: int = 500,
    random_state: int = 42
) -> Tuple[pd.DataFrame, int]:
    """
    Selects NEW candidates to reach target_total (500) while excluding already crawled IDs/URLs.
    """
    existing_ids = set()
    existing_urls = set()

    if os.path.exists(existing_csv_path):
        try:
            df_exist = pd.read_csv(existing_csv_path, encoding="utf-8")
            if "id" in df_exist.columns:
                existing_ids = set(df_exist["id"].astype(str).values)
            if "detail_url" in df_exist.columns:
                existing_urls = set(df_exist["detail_url"].astype(str).values)
        except Exception as e:
            print(f"Warning loading existing CSV: {e}")

    df_candidates["id_str"] = df_candidates["id"].astype(str)
    df_candidates["url_str"] = df_candidates["detail_url"].astype(str)

    # Exclude already processed records
    df_unseen = df_candidates[
        (~df_candidates["id_str"].isin(existing_ids)) &
        (~df_candidates["url_str"].isin(existing_urls))
    ].copy()

    already_count = len(existing_ids)
    needed = max(0, target_total - already_count)

    print(f"Phase 1 already crawled: {already_count} records.")
    print(f"Needed new records for Phase 2: {needed} (Target total: {target_total}).")

    if needed == 0 or len(df_unseen) == 0:
        return pd.DataFrame(), already_count

    # Balance HCMC and Hanoi in the new sample
    df_hcm = df_unseen[df_unseen["location"].astype(str).str.contains("Hồ Chí Minh|HCM", case=False, na=False)]
    df_hn = df_unseen[df_unseen["location"].astype(str).str.contains("Hà Nội|HN", case=False, na=False)]

    half_needed = needed // 2

    sample_hcm = df_hcm.sample(n=min(half_needed, len(df_hcm)), random_state=random_state)
    sample_hn = df_hn.sample(n=min(needed - len(sample_hcm), len(df_hn)), random_state=random_state)

    sample_new = pd.concat([sample_hcm, sample_hn], ignore_index=True)
    sample_new.drop(columns=["id_str", "url_str"], errors="ignore", inplace=True)

    return sample_new, already_count


def run_collection_pipeline_phase2(
    raw_csv_path: str = "data/raw/house_buying_dec29th_2025.csv",
    output_dir: str = "data/raw/collection",
    csv_filename: str = "detail_locations_sample.csv",
    target_total: int = 500,
    random_state: int = 42,
    delay_seconds: float = 1.0
) -> Tuple[pd.DataFrame, Dict[str, Any], Dict[str, Any]]:
    """
    Executes Phase 2 collection pipeline targeting 500 total URLs.
    """
    df_candidates, candidate_stats = load_and_filter_candidates(raw_csv_path)

    existing_path = os.path.join(output_dir, csv_filename)

    df_new_sample, already_count = select_phase2_sample(
        df_candidates=df_candidates,
        existing_csv_path=existing_path,
        target_total=target_total,
        random_state=random_state
    )

    crawler = DetailLocationCrawler(
        output_dir=output_dir,
        csv_filename=csv_filename,
        delay_seconds=delay_seconds
    )

    if not df_new_sample.empty:
        candidate_records = df_new_sample.to_dict(orient="records")
        df_all_results = crawler.crawl_urls(candidate_records)
    else:
        df_all_results = crawler._load_existing_results()

    # Post-process & enrich missing schema fields for all records
    df_all_results = enrich_all_records(df_all_results)
    df_all_results.to_csv(existing_path, index=False, encoding="utf-8")

    audit_metrics = calculate_phase2_audit(df_all_results)

    return df_all_results, candidate_stats, audit_metrics


def enrich_all_records(df: pd.DataFrame) -> pd.DataFrame:
    """Enriches and standardizes columns for all rows in the dataset."""
    for idx, row in df.iterrows():
        addr_raw = str(row["address_raw"]) if pd.notna(row["address_raw"]) else None
        street = str(row["street"]) if pd.notna(row["street"]) else None
        ward = str(row["ward"]) if pd.notna(row["ward"]) else None
        dist = str(row["district_detail"]) if pd.notna(row["district_detail"]) else None
        prov = str(row["province_detail"]) if pd.notna(row["province_detail"]) else None
        orig_loc = str(row["original_location"]) if pd.notna(row["original_location"]) else ""

        if pd.isna(row.get("address_normalized")) or not row.get("address_normalized"):
            df.loc[idx, "address_normalized"] = _normalize_address(addr_raw, street, ward, dist, prov)

        if pd.isna(row.get("address_category")) or not row.get("address_category"):
            df.loc[idx, "address_category"] = _classify_address_category(addr_raw, street, ward, dist, prov)

        if pd.isna(row.get("validation_status")) or not row.get("validation_status"):
            df.loc[idx, "validation_status"] = _validate_location_consistency(orig_loc, addr_raw, dist, prov)

        if pd.isna(row.get("address_source")) or not row.get("address_source") or row.get("address_source") == "unknown":
            if addr_raw:
                if "Đường" in addr_raw or "Phường" in addr_raw or "Quận" in addr_raw:
                    df.loc[idx, "address_source"] = "title" if "Chính Chủ" in addr_raw or "Bán" in addr_raw else "dedicated_address"
                else:
                    df.loc[idx, "address_source"] = "description"
            else:
                df.loc[idx, "address_source"] = "unknown"

    return df


def calculate_phase2_audit(df_results: pd.DataFrame) -> Dict[str, Any]:
    """Calculates comprehensive quality metrics for Phase 2 audit."""
    total_records = len(df_results)
    if total_records == 0:
        return {}

    status_counts = df_results["crawl_status"].value_counts().to_dict()
    http_success = status_counts.get("success", 0) + status_counts.get("missing_address", 0)
    http_failure = status_counts.get("http_error", 0) + status_counts.get("timeout", 0)
    parsing_failure = status_counts.get("parse_error", 0)

    address_extracted = df_results["address_raw"].notna().sum()
    address_missing = total_records - address_extracted

    street_extracted = df_results["street"].notna().sum()
    ward_extracted = df_results["ward"].notna().sum()
    district_extracted = df_results["district_detail"].notna().sum()
    province_extracted = df_results["province_detail"].notna().sum()

    provenance_counts = df_results["address_source"].value_counts().to_dict()
    category_counts = df_results["address_category"].value_counts().to_dict()
    validation_counts = df_results["validation_status"].value_counts().to_dict()

    # Duplicate analysis
    dup_ids = total_records - df_results["id"].nunique()
    dup_urls = total_records - df_results["detail_url"].nunique()
    repeated_addresses = total_records - df_results["address_raw"].nunique()

    suspicious_count = validation_counts.get("suspicious", 0)

    metrics = {
        "Total URLs collected": total_records,
        "Unique IDs": df_results["id"].nunique(),
        "Unique URLs": df_results["detail_url"].nunique(),
        "Duplicate IDs": dup_ids,
        "Duplicate URLs": dup_urls,
        "Repeated Raw Addresses": repeated_addresses,
        "HTTP Success Count": http_success,
        "HTTP Failure Count": http_failure,
        "HTTP Success Rate": f"{(http_success / total_records * 100):.1f}%",
        "Address Extracted Count": int(address_extracted),
        "Address Missing Count": int(address_missing),
        "Address Extraction Rate": f"{(address_extracted / total_records * 100):.1f}%",
        "Street Extraction Count": int(street_extracted),
        "Street Extraction Rate": f"{(street_extracted / total_records * 100):.1f}%",
        "Ward Extraction Count": int(ward_extracted),
        "Ward Extraction Rate": f"{(ward_extracted / total_records * 100):.1f}%",
        "District Extraction Count": int(district_extracted),
        "District Extraction Rate": f"{(district_extracted / total_records * 100):.1f}%",
        "Province Extraction Count": int(province_extracted),
        "Province Extraction Rate": f"{(province_extracted / total_records * 100):.1f}%",
        "Provenance Breakdown": provenance_counts,
        "Address Category Breakdown": category_counts,
        "Validation Breakdown": validation_counts,
        "Suspicious Extraction Count": suspicious_count,
        "Suspicious Rate": f"{(suspicious_count / total_records * 100):.1f}%"
    }

    return metrics
