# Stage 00: Detailed Location Data Collection & Quality Audit Component

This component is an isolated data collection and parsing module designed to extract detailed address and location information from real-estate detail listing pages (`detail_url`).

---

## 1. Architectural Scoping

Data collection is positioned as **Stage 00**, preceding Data Understanding (`01_data_understanding.ipynb`):

```text
00_data_collection
        ↓
01_data_understanding
        ↓
02_data_cleaning
        ↓
...
```

**Key Isolation Rules:**
- The existing production ML pipeline (`src/*.py`, `models/`, `backend/`, `frontend/`) is **not modified** and does not depend on this crawler.
- Original raw dataset (`data/raw/house_buying_dec29th_2025.csv`) remains 100% untouched.
- Output files are saved in `data/raw/collection/`.

---

## 2. Directory Structure

```text
data_collection/
├── __init__.py         # Package initialization
├── crawler.py          # Polite HTTP crawler with rate-limiting, retries, & state checkpoints
├── parser.py           # HTML parser for raw address, provenance, categories, & validation
├── pipeline.py         # Filtering, stratified sampling, orchestration, and metrics calculation
└── README.md           # Documentation
```

---

## 3. Output Schema (`detail_locations_sample.csv`)

| Column Name | Description | Example |
|---|---|---|
| `id` | Listing ID matching raw dataset | `178659` |
| `detail_url` | Listing detail page URL | `https://batdongsan.vn/...` |
| `original_location` | Coarse location from original CSV | `Quận 11, Hồ Chí Minh` |
| `title` | Listing title string | `Chính Chủ Bán HXH 182M Đường Lê Thị Bạch Cát...` |
| `address_raw` | Unfiltered raw address text from detail page | `Đường Lê Thị Bạch Cát, Phường 11, Quận 11` |
| `address_normalized` | Standardized address representation | `Đường Lê Thị Bạch Cát, Phường 11, Quận 11` |
| `street` | Extracted street name | `Đường Lê Thị Bạch Cát` |
| `ward` | Extracted ward name | `Phường 11` |
| `district_detail` | Extracted district name | `Quận 11` |
| `province_detail` | Extracted province/city | `Hồ Chí Minh` |
| `address_source` | Provenance source (`dedicated_address`, `title`, `description`, `fallback`) | `dedicated_address` |
| `validation_status` | Automated consistency check (`consistent`, `partially_consistent`, `suspicious`) | `consistent` |
| `address_category` | Address structural category (`full_address`, `street_and_ward`, `street_only`, `alley_or_lane`, `unclear`) | `street_only` |
| `crawl_status` | `success`, `missing_address`, `http_error`, `timeout`, `parse_error` | `success` |
| `crawl_error` | Error details if request or parsing failed | `None` |

---

## 4. Phase 2 Quality Audit Summary (500 Records)

- **Total Records Collected:** 500 unique URLs (50 Phase 1 + 450 Phase 2).
- **HTTP Success Rate:** 100.0% (500 / 500 successful HTTP requests).
- **Address Extraction Rate:** 100.0% (500 / 500 records).
- **Street Extraction Rate:** 73.2% (366 / 500 records).
- **District Extraction Rate:** 100.0% (500 / 500 records).
- **Province Extraction Rate:** 100.0% (500 / 500 records).
- **Automated Validation Consistency:** 99.4% consistent (`consistent`), 0.6% `partially_consistent`, 0.0% `suspicious`.
- **Manual Quality Audit (50 Records):** 74.0% confirmed correct, 26.0% partially correct, 0.0% suspicious.

---

## 5. Final Assessment & Scalability Decision

- **Decision:** `READY_FOR_LARGER_BATCH`
- **Reasoning:** 
  1. The crawler achieved 100% HTTP request success with zero timeouts or anti-bot blocks using conservative rate limiting (1.0s delay).
  2. Provenance tracking confirms 91.4% of extracted addresses originate from dedicated address elements or explicit location labels.
  3. Zero suspicious location contradictions observed across 500 sampled listings in HCMC and Hà Nội.
  4. Resuming checkpointing (`crawler_state.json`) functions reliably with zero duplicate requests.
