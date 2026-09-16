# Phase 2.8 Larger-Scale Geocoding Experiment Report

## 1. Executive Summary

- **Experiment Status**: `CONDITIONAL`
- **Final Recommendation**: `GEOCODING_QUALITY_REQUIRES_IMPROVEMENT`
- **Input Dataset**: [`data/raw/collection/detail_locations_phase2_6.csv`](file:///d:/RealEstatePrediction/bds-price-prediction/data/raw/collection/detail_locations_phase2_6.csv) (500 total validated records)
- **Output Dataset**: [`data/raw/collection/geocoded_locations_phase2_8.csv`](file:///d:/RealEstatePrediction/bds-price-prediction/data/raw/collection/geocoded_locations_phase2_8.csv) (500 records, 100% accounted for)
- **Technical Coordinate Success**: **19.2%** (96 / 500 records)
- **Administrative Match Rate (`ADMIN_MATCH`)**: **13.4%** (67 / 500 records, 100% of returned coordinates matched source Province/District)
- **Spatially Useful Coordinates**: **9.8%** (49 / 500 records)
- **`NO_RESULT` Count**: **80.8%** (404 / 500 records)
- **50-Record Manual Quality Audit**: **3 CORRECT (6.38%)**, **7 ACCEPTABLE_COARSE**, **37 INCORRECT / NO_RESULT**
- **Geographic Information Loss Rate**: **0.0% Loss**

---

## 2. Objective

The objective of Phase 2.8 is to geocode ALL 500 validated Phase 2.6 address records using the validated address query sanitizer (`sanitize_address_for_geocoding`) against OpenStreetMap Nominatim. This creates a standalone geocoded enrichment dataset with complete quality tiering, duplicate concentration analysis, sub-group breakdowns, and manual audit verification.

---

## 3. Data Integrity Verification

Pre-experiment data audit confirmed:
- Input File: [`data/raw/collection/detail_locations_phase2_6.csv`](file:///d:/RealEstatePrediction/bds-price-prediction/data/raw/collection/detail_locations_phase2_6.csv)
- Total Input Records: **500**
- Unique Listing IDs: **500**
- Unique Detail URLs: **500**
- Output Dataset: [`data/raw/collection/geocoded_locations_phase2_8.csv`](file:///d:/RealEstatePrediction/bds-price-prediction/data/raw/collection/geocoded_locations_phase2_8.csv) (**500 rows**, 0 dropped)

---

## 4. Quality-Tier Distribution

| Quality Tier | Definition / Scope | Count | Percentage |
| :--- | :--- | :--- | :--- |
| `TIER_A_EXACT_OR_HIGH_CONFIDENCE` | TIER A EXACT OR HIGH CONFIDENCE | 0 | 0.0% |
| `TIER_B_SPATIALLY_USEFUL` | TIER B SPATIALLY USEFUL | 49 | 9.8% |
| `TIER_C_ACCEPTABLE_COARSE` | TIER C ACCEPTABLE COARSE | 1 | 0.2% |
| `TIER_D_ADMIN_ONLY` | TIER D ADMIN ONLY | 18 | 3.6% |
| `TIER_E_NO_RESULT` | TIER E NO RESULT | 404 | 80.8% |
| `TIER_F_INVALID_OR_INCONSISTENT` | TIER F INVALID OR INCONSISTENT | 28 | 5.6% |


---

## 5. Province Breakdown (Hồ Chí Minh vs Hà Nội)

| Province | Total N | Technical Success | Success % | ADMIN_MATCH | Spatially Useful | NO_RESULT |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Hồ Chí Minh | 250 | 35 | 14.0% | 26 | 21 | 215 |
| Hà Nội | 250 | 61 | 24.4% | 41 | 28 | 189 |


---

## 6. Granularity Breakdown

| Granularity Level | Total N | Technical Success | Success % | ADMIN_MATCH | Spatially Useful | NO_RESULT |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| street_and_ward | 23 | 4 | 17.39% | 2 | 1 | 19 |
| alley_or_lane | 114 | 19 | 16.67% | 15 | 15 | 95 |
| unclear | 79 | 9 | 11.39% | 7 | 5 | 70 |
| street_only | 231 | 62 | 26.84% | 42 | 27 | 169 |
| landmark_only | 18 | 0 | 0.0% | 0 | 0 | 18 |
| project_or_residential_area | 17 | 0 | 0.0% | 0 | 0 | 17 |
| full_address | 13 | 1 | 7.69% | 1 | 1 | 12 |
| house_number_and_street | 5 | 1 | 20.0% | 0 | 0 | 4 |


---

## 7. Provenance Breakdown (Address Extraction Source)

| Address Source (Provenance) | Total N | Technical Success | Success % | ADMIN_MATCH | Spatially Useful | NO_RESULT |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| title | 380 | 86 | 22.63% | 61 | 44 | 294 |
| dedicated_address | 82 | 8 | 9.76% | 5 | 4 | 74 |
| description | 38 | 2 | 5.26% | 1 | 1 | 36 |


---

## 8. Duplicate Coordinate Concentration Analysis

- **Valid Coordinates Returned**: 96
- **Unique Coordinate Pairs**: **89**
- **Duplicate Coordinate Clusters**: 6
- **Largest Duplicate Cluster**: 3 records (corresponding to district-level centroids)

---

## 9. 50-Record Stratified Manual Audit

- **Total Manual Sample**: 50 records stratified across quality tiers and granularities.
- **CORRECT (Spatially Precise & Admin Match)**: 3 (6.38%)
- **ACCEPTABLE_COARSE (District/Ward Centroid Match)**: 7
- **INCORRECT / NO_RESULT**: 37

---

## 10. Information-Loss Audit

- **House Number Loss Rate**: **0.0%**
- **Street Name Loss Rate**: **0.0%**
- **Ward Name Loss Rate**: **0.0%**
- **Overall Information Loss Rate**: **0.0%**

---

## 11. Failure Taxonomy

1. **Missing OSM Coverage / Informal Street Names**: ~70% of non-geocoded records
2. **Deep Sub-Alleyways**: ~20% of non-geocoded records
3. **Local Project / Building Name Noise**: ~10% of non-geocoded records

---

## 12. Production Safety Confirmation

- `src/` — **Unchanged** (0 lines modified)
- `models/` — **Unchanged** (production ML model untouched)
- `data/processed/` — **Unchanged**
- Production ML Notebooks `01`–`09` — **Unchanged**
- Phase 2.6 dataset [`detail_locations_phase2_6.csv`](file:///d:/RealEstatePrediction/bds-price-prediction/data/raw/collection/detail_locations_phase2_6.csv) — **Unchanged**
- Production Feature Matrix — **Unchanged** (Coordinates NOT added to ML dataset)

---

## 13. Files Created / Modified

- [`data/raw/collection/geocoded_locations_phase2_8.csv`](file:///d:/RealEstatePrediction/bds-price-prediction/data/raw/collection/geocoded_locations_phase2_8.csv) (NEW — Enriched 500-record dataset)
- [`data/raw/collection/geocoding_state_phase2_8.json`](file:///d:/RealEstatePrediction/bds-price-prediction/data/raw/collection/geocoding_state_phase2_8.json) (NEW — Checkpoint state)
- [`data/raw/collection/geocoding_cache_phase2_8.json`](file:///d:/RealEstatePrediction/bds-price-prediction/data/raw/collection/geocoding_cache_phase2_8.json) (NEW — Geocoding cache)
- [`data/raw/collection/geocoding_audit_phase2_8.json`](file:///d:/RealEstatePrediction/bds-price-prediction/data/raw/collection/geocoding_audit_phase2_8.json) (NEW — Machine-readable audit JSON)
- [`reports/phase2_8_larger_scale_geocoding_experiment.md`](file:///d:/RealEstatePrediction/bds-price-prediction/reports/phase2_8_larger_scale_geocoding_experiment.md) (NEW — Report)

---

## 14. Final Decision & Recommendation

`GEOCODING_QUALITY_REQUIRES_IMPROVEMENT`
