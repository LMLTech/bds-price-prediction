# Phase 2.6 Final Report: Parser Bug Fix & 500-Record Reprocessing Audit

**Project:** Real Estate Price Prediction Based on Property and Location Features Using Linear Regression  
**Stage:** Stage 00 Data Collection — Phase 2.6 (Parser Bug Fix & Reprocessing)  
**Target Dataset:** `data/raw/collection/detail_locations_phase2_6.csv` (500 records)  

---

## 1. Status

### **PASS**

The confirmed Phase 2.5 sidebar address extraction bug has been reproduced, structurally fixed using DOM-context-aware container isolation, verified with automated regression and generalized tests, and proven eliminated across the reprocessed 500-record collection.

---

## 2. Root Cause Analysis

On `batdongsan.vn`, listing detail pages render a bottom/sidebar recommendation grid (`div.row.mt-5 > div.address`) containing popular district/area names (e.g. `Tân Phú, Hồ Chí Minh` or `Hoài Đức, Hà Nội`).

The previous parser used global unconstrained element selection:
```python
soup.select_one("div.address")
```
When an explicit listing address tag was absent inside the property's detail container, this global search traversed the entire HTML document and picked up the first item of the bottom recommendation grid. This caused `Tân Phú, Hồ Chí Minh` to be extracted 235 times and `Hoài Đức, Hà Nội` 230 times as false positive listing addresses.

---

## 3. Parser Fix Description

In [`data_collection/parser.py`](file:///d:/RealEstatePrediction/bds-price-prediction/data_collection/parser.py), we introduced a structural DOM tree scope isolation function `_isolate_main_listing_container`:

1. **Tree Scope Isolation:** The parser decomposes non-listing sidebar, footer, recommendation grids, and related news containers (`div.row.mt-5`, `div.box-right`, `div.sidebar`, `footer`, `.recommended-area`, `.box-location`, `div.related-news`) before running element searches.
2. **Container Restriction:** Extraction priority rules strictly run inside the scoped main listing container (`div.left-detail`, `div.main-content`, `div.col-lg-9`, `div.product-detail`).
3. **No Blacklists or Hacks:**
   - **NO** hard-coded `"Tân Phú"` or `"Hoài Đức"` blacklists used.
   - **NO** string matching shortcuts or artificial randomization.
   - **NO** `drop_duplicates("address_raw")` shortcuts.
   - The fix is 100% DOM-context aware.

---

## 4. Reprocessing Integrity

- **Input Records:** 500
- **Output Records:** 500
- **Unique Listing IDs:** 500 (100% ID overlap with Phase 2)
- **Unique Detail URLs:** 500 (100% URL overlap with Phase 2)
- **Identity Preservation:** Verified. Exactly the same 500 listing IDs and URLs were reprocessed.

---

## 5. Before vs After Comparative Table

| Metric | Phase 2 (Before) | Phase 2.6 (After) | Quantitative Change |
|---|---:|---:|---|
| **Total Reprocessed Records** | 500 | 500 | 0 |
| **Unique Listing IDs** | 500 | 500 | 0 |
| **Unique Detail URLs** | 500 | 500 | 0 |
| **Unique `address_raw` Values** | 35 | **496** | **+461 unique addresses** |
| **Duplicated Address Groups** | 2 | **4** | +2 (Legitimate small duplicate street listings) |
| **Rows in Duplicated Groups** | 467 | **8** | **-459 rows** (Sidebar widget pollution eliminated) |
| **Duplicate Occurrences Beyond First** | 465 | **4** | **-461 duplicate occurrences** |
| **"Tân Phú..." Occurrences** | 235 | **13** | **-222 false positives** (Only 13 legitimate listings with "Tân Phú" in title/content remain) |
| **"Hoài Đức..." Occurrences** | 230 | **0** | **-230 false positives** (Sidebar widget artifacts eliminated) |
| **Dedicated Address Provenance** | 457 (91.4%) | **188 (37.6%)** | Shifted to true listing tags/headings |
| **Title Provenance** | 0 (0.0%) | **269 (53.8%)** | Real property H1 title address extraction |
| **Description Provenance** | 43 (8.6%) | **43 (8.6%)** | 100% preserved |
| **Actionable Spatial Records (Levels 1–6)** | 410 (82.0%) | **416 (83.2%)** | **+6 actionable records** |
| **Administrative Consistency** | 497 (99.4%) | **497 (99.4%)** | 100% preserved consistency |
| **Manual Audit Exact Match** | 37 (74.0%) | **38 (76.0%)** | Higher exact semantic accuracy |

---

## 6. Automated Regression Test Results

We created [`tests/test_address_parser.py`](file:///d:/RealEstatePrediction/bds-price-prediction/tests/test_address_parser.py) containing automated unit tests:

1. `test_sidebar_recommendation_bug_regression`: **PASS**
   - Verifies HTML fixture with sidebar `div.address` containing `"Tân Phú, Hồ Chí Minh"` extracts `"Đường Lê Thị Bạch Cát, Phường 11, Quận 11"` from the main container.
2. `test_generalized_sidebar_protection`: **PASS**
   - Verifies HTML fixture with arbitrary sidebar `div.address` containing `"Quận Cầu Giấy, Hà Nội"` extracts `"45 Phố Huế, Phường Hàng Bài, Quận Hoàn Kiếm"` from the main container.
3. `test_main_container_dedicated_address`: **PASS**
   - Verifies proper extraction of dedicated address element inside main listing container.

*Execution output:* `Ran 3 tests in 0.019s — OK`

---

## 7. Manual Quality Audit (50 Stratified Records)

- **EXACT Match:** 38 / 50 (**76.0%**) — Exact house/street/ward address.
- **PARTIAL Match:** 12 / 50 (**24.0%**) — Accurate district/province with landmark/neighborhood details.
- **INCORRECT Match:** 0 / 50 (**0.0%**)
- **SUSPICIOUS:** 0 / 50 (**0.0%**)

**Audit Confirmation:** The previous sidebar extraction pattern (`Tân Phú` / `Hoài Đức` sidebar widget) no longer appears on any listing.

---

## 8. Spatial Granularity Distribution (Phase 2.6)

- **LEVEL 1 — HOUSE_LEVEL:** 22 (4.4%)
- **LEVEL 2 — STREET_LEVEL:** 223 (44.6%)
- **LEVEL 3 — STREET + WARD:** 19 (3.8%)
- **LEVEL 4 — ALLEY / NGÕ / HẺM:** 132 (26.4%)
- **LEVEL 5 — PROJECT / KĐT:** 8 (1.6%)
- **LEVEL 6 — LANDMARK / NEIGHBORHOOD:** 12 (2.4%)
- **LEVEL 8 — UNKNOWN / COARSE:** 84 (16.8%)
- **Actionable Spatial Records (Levels 1–6):** **416 / 500 (83.2%)**

---

## 9. Semantic Validation

- **Administrative Consistency:** 497 / 500 (**99.4%**) consistent with original district/province labels.
- **Zero Suspicious Regressions:** Zero location contradictions observed.

---

## 10. Bug Verdict

> **Has the Phase 2.5 sidebar-address extraction bug been demonstrated to be fixed?**

### **YES**

**Evidence:**
1. Unique address count expanded from 35 to **496** distinct addresses.
2. Duplicate address rows dropped from 467 to **8** rows.
3. `"Hoài Đức..."` false positive sidebar widget occurrences dropped from 230 to **0**.
4. `"Tân Phú..."` false positive sidebar widget occurrences dropped from 235 to **13** (where "Tân Phú" is actually part of the legitimate listing title/location).
5. All automated unit tests in `tests/test_address_parser.py` pass cleanly.

---

## 11. Files Changed & Created

- [`data_collection/parser.py`](file:///d:/RealEstatePrediction/bds-price-prediction/data_collection/parser.py): Updated with DOM-context-aware scope isolation.
- [`tests/__init__.py`](file:///d:/RealEstatePrediction/bds-price-prediction/tests/__init__.py): Added test package init.
- [`tests/test_address_parser.py`](file:///d:/RealEstatePrediction/bds-price-prediction/tests/test_address_parser.py): Created automated unit regression test suite.
- [`data/raw/collection/detail_locations_phase2_6.csv`](file:///d:/RealEstatePrediction/bds-price-prediction/data/raw/collection/detail_locations_phase2_6.csv): Reprocessed 500-record dataset.
- [`data/raw/collection/audit_summary_phase2_6.json`](file:///d:/RealEstatePrediction/bds-price-prediction/data/raw/collection/audit_summary_phase2_6.json): Comparative JSON audit summary.
- [`reports/phase2_6_parser_bugfix_audit.md`](file:///d:/RealEstatePrediction/bds-price-prediction/reports/phase2_6_parser_bugfix_audit.md): Comparative Phase 2.6 audit report.

---

## 12. Production Safety Confirmation

The following production files remain **100% UNCHANGED**:
- Raw ML Dataset: [`data/raw/house_buying_dec29th_2025.csv`](file:///d:/RealEstatePrediction/bds-price-prediction/data/raw/house_buying_dec29th_2025.csv)
- Processed ML Datasets: `data/processed/*.csv`
- Production Model: `models/linear_regression.pkl`
- Production Source Code: `src/*.py`
- Production ML Notebooks: `notebooks/01_*.ipynb` through `09_*.ipynb`
- Backend & Frontend: `backend/`, `frontend/`

---

## 13. Next Recommended Step

### **`READY_FOR_GEOCODING_PILOT`**

With the parser bug structurally eliminated and 83.2% actionable spatial granularity established across 496 unique addresses, the Stage 00 dataset is verified and ready to support a small geocoding pilot experiment.
