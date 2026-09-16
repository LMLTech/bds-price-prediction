# Phase 2.7 Geocoding Pilot Report

**Project:** Real Estate Price Prediction Based on Property and Location Features Using Linear Regression  
**Stage:** Stage 00 Data Collection — Phase 2.7 (Geocoding Pilot)  
**Input Dataset:** [`data/raw/collection/detail_locations_phase2_6.csv`](file:///d:/RealEstatePrediction/bds-price-prediction/data/raw/collection/detail_locations_phase2_6.csv) (500 records)  

---

## 1. Status

### **`CONDITIONAL`**

The geocoding pilot successfully established a reproducible caching framework, rate-limited request policy, and evaluation taxonomy. However, directly submitting raw real-estate address strings (containing promotional adjectives like *Mặt tiền 4m*, *Hẻm xe hơi*, *Nhà đẹp ở ngay*) to strict public geocoders like OpenStreetMap Nominatim yields a low technical coordinate success rate (**10.0%**). An explicit query normalization iteration is required before scaling geocoding.

---

## 2. Objective

The pilot was designed to evaluate whether extracted property addresses from Phase 2.6 can be reliably converted into spatially precise coordinates (`latitude`, `longitude`) without modifying the production ML pipeline or inflating accuracy metrics.

---

## 3. Input Dataset

- **Source File:** [`data/raw/collection/detail_locations_phase2_6.csv`](file:///d:/RealEstatePrediction/bds-price-prediction/data/raw/collection/detail_locations_phase2_6.csv)
- **Total Available Records:** 500
- **Unique Listing IDs:** 500
- **Unique Addresses:** 496
- **Actionable Spatial Records:** 416 (83.2%)

---

## 4. Provider & Infrastructure

- **Provider:** OpenStreetMap Nominatim
- **Endpoint:** `https://nominatim.openstreetmap.org/search`
- **Request Policy:** User-Agent `BDS-Price-Prediction-Research/1.0 (academic.research@local.edu)`
- **Rate Limit:** Polite 1.2s delay between requests
- **Cache Mechanism:** [`data/raw/collection/geocoding_cache.json`](file:///d:/RealEstatePrediction/bds-price-prediction/data/raw/collection/geocoding_cache.json) (80 cached queries)

---

## 5. Sampling Design

- **Target Sample Size:** 80 records
- **Actual Sample Size:** 80 records
- **Random Seed:** `random_state = 42`
- **Stratification Dimensions:** Granularity (House, Street, Alley, Project, Landmark, District-Only) & Province (40 HCMC, 40 Hà Nội)

### Sample Granularity Breakdown

| Granularity Category | Sample Count | Percentage |
|---|---:|---:|
| `STREET_LEVEL` | 35 | 43.8% |
| `ALLEY_OR_LANE` | 21 | 26.2% |
| `DISTRICT_ONLY_OR_COARSE` | 13 | 16.2% |
| `STREET_AND_WARD` | 4 | 5.0% |
| `HOUSE_LEVEL` | 3 | 3.8% |
| `PROJECT_OR_RESIDENTIAL_AREA` | 2 | 2.5% |
| `LANDMARK_OR_NEIGHBORHOOD` | 2 | 2.5% |
| **Total** | **80** | **100.0%** |

---

## 6. Query Construction

Geocoding queries were constructed combining the extracted address representation with administrative context:
```text
[address_normalized] + [district_detail] + [province_detail] + "Việt Nam"
```
*Example:* `Đường Lê Thị Bạch Cát, Phường 11, Quận 11, Hồ Chí Minh, Việt Nam`

---

## 7. Geocoding Results

| Coverage Metric | Count | Percentage |
|---|---:|---:|
| **Total Pilot Records** | 80 | 100.0% |
| **Valid Coordinates Returned** | 8 | **10.0%** |
| **Technical Success Rate** | — | **10.0%** |
| **No Result Count (`NO_RESULT`)** | 72 | **90.0%** |
| **Provider Errors** | 0 | 0.0% |
| **Invalid Coordinates** | 0 | 0.0% |
| **Ambiguous Candidates** | 0 | 0.0% |

---

## 8. Spatial Precision Breakdown

| Spatial Precision Level | Definition | Count | Percentage |
|---|---|---:|---:|
| **HOUSE** | House / building centroid | 0 | 0.0% |
| **STREET** | Street segment interpolation | 2 | 2.5% |
| **WARD** | Ward centroid | 0 | 0.0% |
| **DISTRICT** | District centroid | 0 | 0.0% |
| **PROJECT** | Residential complex centroid | 0 | 0.0% |
| **LANDMARK** | Recognized point of interest | 5 | 6.2% |
| **CITY/PROVINCE** | Province centroid | 1 | 1.2% |
| **UNKNOWN** | No result returned | 72 | 90.0% |
| **Total Spatially Useful (House/Street/Ward/Project/Landmark)** | | **7** | **8.8%** |

---

## 9. Administrative Validation

| Administrative Validation Status | Count | Percentage |
|---|---:|---:|
| **ADMIN_MATCH** | 4 | 5.0% |
| **ADMIN_PARTIAL_MATCH** | 4 | 5.0% |
| **ADMIN_MISMATCH** | 0 | 0.0% |
| **UNKNOWN (NO_RESULT)** | 72 | 90.0% |

---

## 10. Manual Audit (30 Stratified Sample Records)

| Evaluation Category | Count | Percentage | Explanation |
|---|---:|---:|---|
| **CORRECT** | 2 | 6.7% | Verified street/landmark coordinate returned matching physical location |
| **ACCEPTABLE_COARSE** | 0 | 0.0% | — |
| **INCORRECT (NO_RESULT)** | 28 | 93.3% | Nominatim returned zero candidates due to uncleaned promotional text |
| **AMBIGUOUS** | 0 | 0.0% | — |

---

## 11. Failure Analysis

### Primary Failure Cause: Raw Real-Estate Query Noise
Vietnamese real-estate listing titles and descriptions frequently contain promotional adjectives (e.g., *Mặt tiền 4m*, *Hẻm xe hơi*, *Nhà đẹp ở ngay*, *Cực phẩm*, *Lô góc*). 

When these strings are appended to `geocoding_query` verbatim, OpenStreetMap Nominatim's strict string parser fails to match the street in its database, returning `NO_RESULT` for 90% of requests.

*Representative Examples:*
- Query: `MẶT TIỀN 4m ĐƯỜNG NHỰA, Nam Từ Liêm, Hà Nội, Việt Nam` -> `NO_RESULT`
- Query: `Cách Mặt tiền Cống Lở 1 căn, oto vô tận cửa, Tân Bình, Hồ Chí Minh, Việt Nam` -> `NO_RESULT`

*Remedy:* Query normalization in the next iteration must isolate strict street names (e.g. `Đường Lê Đức Thọ`, `Đường Cống Lở`) before submitting to public geocoders.

---

## 12. Cache & Reproducibility

- **Total Pilot Requests:** 80
- **Unique Queries Cached:** 80
- **Cache Hits / Hits on Rerun:** 80 (100% reproducible)
- **Cache File:** [`data/raw/collection/geocoding_cache.json`](file:///d:/RealEstatePrediction/bds-price-prediction/data/raw/collection/geocoding_cache.json)

---

## 13. Key Finding

> **Are the Phase 2.6 addresses sufficiently reliable and spatially precise to justify a larger geocoding experiment?**

### **`CONDITIONAL`**

**Evidence:**
1. The physical addresses extracted in Phase 2.6 are valid and detailed (83.2% actionable spatial granularity).
2. However, directly querying strict public geocoders (OSM Nominatim) using uncleaned text strings achieves only **10.0% technical coordinate success** and **8.8% spatially useful success**.
3. A dedicated query-sanitization step (stripping promotional adjectives to extract clean street names) is required to unlock high geocoding coverage.

---

## 14. Impact on Machine Learning

> [!NOTE]
> The pilot evaluated geocoding feasibility ONLY. The production ML model, `src/` feature pipeline, and model hyperparameters have NOT been modified or retrained.

---

## 15. Production Safety Confirmation

Confirmed 100% UNCHANGED:
- Raw ML Dataset: [`data/raw/house_buying_dec29th_2025.csv`](file:///d:/RealEstatePrediction/bds-price-prediction/data/raw/house_buying_dec29th_2025.csv)
- Processed ML Datasets: `data/processed/*.csv`
- Production Model: `models/linear_regression.pkl`
- Production Source Code: `src/*.py`
- Production ML Notebooks: `notebooks/01_*.ipynb` through `09_*.ipynb`
- Verified Phase 2.6 Output: [`data/raw/collection/detail_locations_phase2_6.csv`](file:///d:/RealEstatePrediction/bds-price-prediction/data/raw/collection/detail_locations_phase2_6.csv)

---

## 16. Files Created

- [`data/raw/collection/geocoding_pilot_sample.csv`](file:///d:/RealEstatePrediction/bds-price-prediction/data/raw/collection/geocoding_pilot_sample.csv): Stratified 80-record pilot sample.
- [`data/raw/collection/geocoding_pilot_results.csv`](file:///d:/RealEstatePrediction/bds-price-prediction/data/raw/collection/geocoding_pilot_results.csv): Pilot geocoding results and precision categories.
- [`data/raw/collection/geocoding_cache.json`](file:///d:/RealEstatePrediction/bds-price-prediction/data/raw/collection/geocoding_cache.json): Caching store for OpenStreetMap Nominatim responses.
- [`data/raw/collection/geocoding_pilot_audit.json`](file:///d:/RealEstatePrediction/bds-price-prediction/data/raw/collection/geocoding_pilot_audit.json): Machine-readable audit metrics.
- [`reports/phase2_7_geocoding_pilot.md`](file:///d:/RealEstatePrediction/bds-price-prediction/reports/phase2_7_geocoding_pilot.md): Phase 2.7 report artifact.

---

## 17. Next Recommended Step

### **`GEOCODING_PILOT_ITERATION_REQUIRED`**

Recommend implementing a dedicated query-sanitization module to strip real-estate noise keywords prior to scaling geocoding processing.
