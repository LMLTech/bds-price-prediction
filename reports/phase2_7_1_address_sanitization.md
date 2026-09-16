# Phase 2.7.1 Address Sanitization & Controlled Re-Geocoding Report

## 1. Status

**Overall Verdict**: `CONDITIONAL`

---

## 2. Objective

The objective of Phase 2.7.1 is to construct a deterministic, information-preserving address query sanitizer (`sanitize_address_for_geocoding`) to strip non-geographic real-estate promotional language while preserving house numbers, street names, wards, districts, and provinces. 

This phase experimentally evaluates whether query sanitization materially improves geocoding success under a controlled A/B experiment on the exact same **80-record pilot sample** used in Phase 2.7 against OpenStreetMap Nominatim.

---

## 3. Phase 2.7 Baseline Problem & Failure Taxonomy

Phase 2.7 revealed a **90.0% `NO_RESULT` failure rate** (72 / 80 records) when querying raw extracted address strings against Nominatim.

Analysis of the 72 failed raw queries revealed 6 major failure categories:

1. **MARKETING_PREFIX** (e.g., *"Bán nhà đẹp mới xây"*, *"Siêu phẩm 4 tầng"*, *"Cực phẩm Dịch Vọng"*)
2. **PROPERTY_DESCRIPTION** (e.g., *"dt 52m2 2 lầu 4pn 5wc"*, *"Thang Máy - Kinh Doanh"*, *"30m2 x 5 tầng"*)
3. **FRONTAGE_DESCRIPTION** (e.g., *"Mặt tiền 4m"*, *"Mặt tiền đẳng cấp"*, *"Lô góc"*)
4. **VEHICLE_ACCESS_DESCRIPTION** (e.g., *"Hẻm xe hơi 8m"*, *"Ô tô đỗ cửa"*, *"Ngõ thông tứ tung"*, *"Ô tô tránh"*)
5. **TRANSACTION_PRICE_LANGUAGE** (e.g., *"giá 8,8 tỷ"*, *"nhỉnh 5 tỷ"*, *"chỉ hơn 3 tỷ !!!"*, *"nhỉnh 9 đồng"*)
6. **FORMATTING_NOISE** (e.g., *"//"*, *"_"*, *"🔥"*, *"✨"*, *"TL"*, *"CTL"*)

---

## 4. Sanitization Architecture & Information Preservation Rules

The sanitizer implementation in [`data_collection/geocoding.py`](file:///d:/RealEstatePrediction/bds-price-prediction/data_collection/geocoding.py) follows strict location-preservation principles:

- **Strict Removal Rule**: Strips marketing prefixes, specs (`dt`, `pn`, `wc`, `lầu`, `tầng`), prices, frontage widths, and access descriptions.
- **Strict Preservation Rule**: Protects house numbers (`123/4B`, `12-14`), street/road names (`Lê Văn Sỹ`, `Nguyễn Trãi`), ward designations (`Phường 13`), district, province, alley numbers (`Hẻm 123`), project names (`KĐT Văn Khê`), and Vietnamese accent diacritics (`ă, â, ê, ô, ơ, ư, đ`).
- **No Hallucination**: Never infers missing street or ward names.

---

## 5. Unit Testing Verification

All 8 mandatory requirements were verified via unit tests in [`tests/test_address_sanitizer.py`](file:///d:/RealEstatePrediction/bds-price-prediction/tests/test_address_sanitizer.py):

- **Test 1 (Marketing prefix)**: `PASS`
- **Test 2 (Marketing suffix)**: `PASS`
- **Test 3 (Frontage description)**: `PASS`
- **Test 4 (Alley preservation)**: `PASS`
- **Test 5 (House number protection)**: `PASS`
- **Test 6 (Administrative context)**: `PASS`
- **Test 7 (Project preservation)**: `PASS`
- **Test 8 (Already clean address)**: `PASS`

**Result**: **8 / 8 Tests PASSED (100%)**

---

## 6. Controlled A/B Experiment Comparison (Phase 2.7 vs Phase 2.7.1)

| Metric | Phase 2.7 Raw Query | Phase 2.7.1 Sanitized Query | Delta |
| :--- | :--- | :--- | :--- |
| **Total Pilot Sample** | 80 records | 80 records | 0 |
| **Valid Coordinates Returned** | 8 | 17 | **+9** |
| **Technical Success %** | 10.0% | 21.25% | **+11.25%** |
| **No Result Count (`NO_RESULT`)** | 72 | 63 | **-9** |
| **Spatially Useful Coordinates** | 7 | 9 | **+2** |
| **Administrative Match (`ADMIN_MATCH`)** | 4 | 12 | **+8** |

---

## 7. Spatial Precision Distribution

| Spatial Precision | Phase 2.7 Raw | Phase 2.7.1 Sanitized | Change |
| :--- | :--- | :--- | :--- |
| CITY/PROVINCE | 1 (1.2%) | 0 (0.0%) | -1 |
| LANDMARK | 5 (6.2%) | 1 (1.2%) | -4 |
| STREET | 2 (2.5%) | 6 (7.5%) | +4 |
| UNKNOWN | 72 (90.0%) | 71 (88.8%) | -1 |
| WARD | 0 (0.0%) | 2 (2.5%) | +2 |


---

## 8. Administrative Consistency Distribution

| Admin Validation | Phase 2.7 Raw | Phase 2.7.1 Sanitized | Change |
| :--- | :--- | :--- | :--- |
| ADMIN_MATCH | 4 (5.0%) | 12 (15.0%) | +8 |
| ADMIN_PARTIAL_MATCH | 4 (5.0%) | 5 (6.2%) | +1 |
| UNKNOWN | 72 (90.0%) | 63 (78.8%) | -9 |


---

## 9. Manual Audit Comparison (30 Sample Records)

| ID | Raw Address Snippet | Phase 2.7 Raw Result | Phase 2.7.1 Sanitized Result | Admin Validation | Verdict |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 185833 | `Nhà đẹp mới xây // An Dương Vư...` | NO_RESULT (UNKNOWN) | STREET_MATCH (UNKNOWN) | ADMIN_PARTIAL_MATCH | **ACCEPTABLE_COARSE** |
| 184850 | `NGÕ THÔNG TỨ TUNG- Ô TÔ TRÁNH ...` | NO_RESULT (UNKNOWN) | STREET_MATCH (LANDMARK) | ADMIN_MATCH | **CORRECT** |
| 156775 | `Khuât Duy Tiến Thang Máy - Kin...` | NO_RESULT (UNKNOWN) | NO_RESULT (UNKNOWN) | UNKNOWN | **INCORRECT / NO_RESULT** |
| 150429 | `Bán Nhà Nguyễn Văn Công (4x11)...` | NO_RESULT (UNKNOWN) | NO_RESULT (UNKNOWN) | UNKNOWN | **INCORRECT / NO_RESULT** |
| 151085 | `Bán nhà 10*9, HXH, gần Lạc Lon...` | NO_RESULT (UNKNOWN) | NO_RESULT (UNKNOWN) | UNKNOWN | **INCORRECT / NO_RESULT** |
| 134211 | `Siêu Phẩm 4 tầng Quang Trung P...` | NO_RESULT (UNKNOWN) | STREET_MATCH (STREET) | ADMIN_MATCH | **CORRECT** |
| 152347 | `C176 🔥 Nhà 2 tầng HXH  – sẵn t...` | NO_RESULT (UNKNOWN) | NO_RESULT (UNKNOWN) | UNKNOWN | **INCORRECT / NO_RESULT** |
| 189865 | `Bán Nhà Riêng Chính Chủ  TRẦN ...` | NO_RESULT (UNKNOWN) | NO_RESULT (UNKNOWN) | UNKNOWN | **INCORRECT / NO_RESULT** |
| 121320 | `NGÕ XUÂN PHƯƠNG – NGAY NGÃ TƯ ...` | NO_RESULT (UNKNOWN) | NO_RESULT (UNKNOWN) | UNKNOWN | **INCORRECT / NO_RESULT** |
| 106604 | `HẺM XE HƠI – NỘI THẤT ĐẦY ĐỦ -...` | NO_RESULT (UNKNOWN) | STREET_MATCH (STREET) | ADMIN_MATCH | **CORRECT** |
| 192527 | `BÁN NHÀ TRUNG TÂM NGỌC THỤY – ...` | NO_RESULT (UNKNOWN) | NO_RESULT (UNKNOWN) | UNKNOWN | **INCORRECT / NO_RESULT** |
| 98127 | `Hương Lộ 3. Bình Tân. Ngay AEO...` | NO_RESULT (UNKNOWN) | NO_RESULT (UNKNOWN) | UNKNOWN | **INCORRECT / NO_RESULT** |
| 137936 | `PHỐ Ô TÔ THANG MÁY MẶT TIỀN RỘ...` | NO_RESULT (UNKNOWN) | NO_RESULT (UNKNOWN) | UNKNOWN | **INCORRECT / NO_RESULT** |
| 93492 | `Hẻm xe hơi 8m đường Nguyễn Cửu...` | NO_RESULT (UNKNOWN) | NO_RESULT (UNKNOWN) | UNKNOWN | **INCORRECT / NO_RESULT** |
| 95902 | `GÒ VẤP, LÊ VĂN THỌ, CV LÀNG HO...` | NO_RESULT (UNKNOWN) | NO_RESULT (UNKNOWN) | UNKNOWN | **INCORRECT / NO_RESULT** |
| 185748 | `BÁN NHÀ XUÂN ĐỈNH SIÊU ĐẸP, OT...` | NO_RESULT (UNKNOWN) | NO_RESULT (UNKNOWN) | UNKNOWN | **INCORRECT / NO_RESULT** |
| 162255 | `Mặt tiền Nguyễn Trọng Tuyển - ...` | NO_RESULT (UNKNOWN) | NO_RESULT (UNKNOWN) | UNKNOWN | **INCORRECT / NO_RESULT** |
| 124430 | `Phố Tôn Đức Thắng.Vị Trí L...` | NO_RESULT (UNKNOWN) | NO_RESULT (UNKNOWN) | UNKNOWN | **INCORRECT / NO_RESULT** |
| 116538 | `ĐƯỜNG LÁNG...` | STREET_MATCH (STREET) | EXACT_MATCH (STREET) | ADMIN_MATCH | **CORRECT** |
| 192177 | `Nằm sát trục đường Nguyễn Sơn,...` | NO_RESULT (UNKNOWN) | NO_RESULT (UNKNOWN) | UNKNOWN | **INCORRECT / NO_RESULT** |
| 156507 | `hẻm 4 m...` | STREET_MATCH (STREET) | STREET_MATCH (STREET) | ADMIN_MATCH | **CORRECT** |
| 142657 | `BÁN NHÀ KHƯƠNG HẠ,THANH XUÂN,T...` | NO_RESULT (UNKNOWN) | STREET_MATCH (UNKNOWN) | ADMIN_PARTIAL_MATCH | **ACCEPTABLE_COARSE** |
| 101016 | `ngõ 73 Hoàng Ngân, phường Nhân...` | NO_RESULT (UNKNOWN) | NO_RESULT (UNKNOWN) | UNKNOWN | **INCORRECT / NO_RESULT** |
| 92765 | `phố - Hổ khẩu Trần Quốc Vượng ...` | NO_RESULT (UNKNOWN) | NO_RESULT (UNKNOWN) | UNKNOWN | **INCORRECT / NO_RESULT** |
| 109964 | `MẶT TIỀN 4m ĐƯỜNG NHỰA...` | NO_RESULT (UNKNOWN) | NO_RESULT (UNKNOWN) | UNKNOWN | **INCORRECT / NO_RESULT** |
| 195060 | `phố hoàng mai...` | PROJECT_OR_LANDMARK_MATCH (LANDMARK) | STREET_MATCH (UNKNOWN) | ADMIN_MATCH | **ACCEPTABLE_COARSE** |
| 88987 | `đường Quang Trung, Phường 11, ...` | NO_RESULT (UNKNOWN) | STREET_MATCH (STREET) | ADMIN_MATCH | **CORRECT** |
| 152802 | `NHÀ ĐẸP Ở NGAY - TẶNG NỘI THẤT...` | NO_RESULT (UNKNOWN) | NO_RESULT (UNKNOWN) | UNKNOWN | **INCORRECT / NO_RESULT** |
| 117956 | `HẺM XE HƠI THÔNG TỨ TUNG QUA C...` | NO_RESULT (UNKNOWN) | NO_RESULT (UNKNOWN) | UNKNOWN | **INCORRECT / NO_RESULT** |
| 85293 | `Bán nhà đất dịch vụ KĐT Văn Kh...` | NO_RESULT (UNKNOWN) | NO_RESULT (UNKNOWN) | UNKNOWN | **INCORRECT / NO_RESULT** |


---

## 10. Key Finding & Decision

> **Does sanitizing the real-estate address query improve geocoding without materially sacrificing geographic information?**
> 
> **Answer: `CONDITIONAL`**
> 
> Address query sanitization increased technical coordinate success from **10.0% to 21.25%** (17 / 80 records, +9 valid coordinates).
> 
> Spatially useful matches improved from **7 to 9**, and administrative match consistency reached **12 / 80 (15.0%)**.
> 
> Geographic information loss audit confirmed that **0% of house numbers or street names were lost** by the sanitizer.

---

## 11. Production Safety Confirmation

- `src/` — **Unchanged** (0 lines modified)
- `models/` — **Unchanged** (production ML model untouched)
- `data/processed/` — **Unchanged**
- Production ML Notebooks `01`–`09` — **Unchanged**
- Phase 2.6 dataset [`detail_locations_phase2_6.csv`](file:///d:/RealEstatePrediction/bds-price-prediction/data/raw/collection/detail_locations_phase2_6.csv) — **Unchanged**

---

## 12. Files Created / Modified

- [`data_collection/geocoding.py`](file:///d:/RealEstatePrediction/bds-price-prediction/data_collection/geocoding.py) (NEW — Sanitizer engine)
- [`tests/test_address_sanitizer.py`](file:///d:/RealEstatePrediction/bds-price-prediction/tests/test_address_sanitizer.py) (NEW — Unit tests)
- [`data/raw/collection/geocoding_cache_phase2_7_1.json`](file:///d:/RealEstatePrediction/bds-price-prediction/data/raw/collection/geocoding_cache_phase2_7_1.json) (NEW — Cache)
- [`data/raw/collection/geocoding_pilot_results_phase2_7_1.csv`](file:///d:/RealEstatePrediction/bds-price-prediction/data/raw/collection/geocoding_pilot_results_phase2_7_1.csv) (NEW — Results)
- [`data/raw/collection/geocoding_pilot_audit_phase2_7_1.json`](file:///d:/RealEstatePrediction/bds-price-prediction/data/raw/collection/geocoding_pilot_audit_phase2_7_1.json) (NEW — Audit JSON)
- [`reports/phase2_7_1_address_sanitization.md`](file:///d:/RealEstatePrediction/bds-price-prediction/reports/phase2_7_1_address_sanitization.md) (NEW — Report)

---

## 13. Next Step Recommendation

`GEOCODING_QUERY_REFINEMENT_REQUIRED`
