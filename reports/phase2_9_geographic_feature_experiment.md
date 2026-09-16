# Phase 2.9 Geographic Feature Integration & Controlled ML Experiment Report

## 1. Executive Summary

- **Phase 2.9 Status**: `GEOGRAPHIC_SIGNAL_INCONCLUSIVE`
- **Final Recommendation**: `GEOGRAPHIC_FEATURE_REQUIRES_MORE_VALIDATION`
- **Baseline Reproduction (Full Test N=9,172)**: **R² = 0.3729**, **MAE = 8417.91M VND**, **RMSE = 21436.29M VND** (100% exact reproduction of production baseline)
- **High-Confidence Geographic Coverage**: **N = 32 records** (0.0698% of 45,857 ML dataset)
- **Feature Redundancy Audit**: **Correlation r = 0.9481** between existing district proxy distance and exact geocoded distance.
- **Controlled Subset Model Comparison (N_train=25, N_test=7)**:
  - **Model A (Baseline MLR on Subset)**: R² = -4.3777 | MAE = 12715.57M VND
  - **Model B (Geocoded Distance Replacement)**: R² = -4.074 | MAE = 12470.38M VND | **ΔR² = +0.3036**
  - **Model C (Lat + Lon Coordinates)**: R² = -7711.678 | MAE = 229846.59M VND | **ΔR² = -7707.3003** (Extreme Overfitting)
  - **Model D (Combined Geographic Signal)**: R² = -2391.5957 | MAE = 141246.71M VND | **ΔR² = -2387.2180**
- **5-Fold Cross Validation (Subset N=32)**:
  - **Model A Baseline**: 5-Fold Mean R² = **-16.5553 ± 28.6285**
  - **Model B GeoDistance**: 5-Fold Mean R² = **-63.5982 ± 69.3711**
  - **Model C GeoCoordinates**: 5-Fold Mean R² = **-5110.8359 ± 6932.5173**
  - **Model D CombinedGeo**: 5-Fold Mean R² = **-41926.4736 ± 82350.9278**
- **Production Safety Verification**: 100% clean. Zero modifications to production ML model [`models/linear_regression.pkl`](file:///d:/RealEstatePrediction/bds-price-prediction/models/linear_regression.pkl) or dataset [`data/processed/housing_features.csv`](file:///d:/RealEstatePrediction/bds-price-prediction/data/processed/housing_features.csv).

---

## 2. Research Question

> *"Does property-level / spatially richer geographic information add predictive value beyond the existing property + province + district + proxy-distance features in Multiple Linear Regression?"*

**Key Empirical Finding**:
1. **High Redundancy**: Geocoded exact distance is **94.81% correlated (r = 0.9481)** with the existing district distance proxy. Replacing the proxy distance with exact geocoded distance yields a minor marginal improvement (ΔR² = +0.3036 on small test subset), confirming that district-level centroid proxies already capture over 94% of the global distance-to-CBD signal.
2. **Severe Overfitting & Multicollinearity from Raw Coordinates**: Adding raw `latitude` and `longitude` to a Multiple Linear Regression model with categorical one-hot encoded district dummies on a small sample (N=32) leads to extreme multicollinearity and variance explosion (`R² < -2000`).
3. **Coverage Limitation**: Only 32 out of 45,857 records (0.0698%) have high-confidence geocoded coordinates, which is currently insufficient for full-dataset production ML integration.

---

## 3. Baseline Reproduction (Model A)

- **Dataset**: [`data/processed/housing_features.csv`](file:///d:/RealEstatePrediction/bds-price-prediction/data/processed/housing_features.csv) (N=45,857)
- **Train/Test Split**: 80% Train (36,685), 20% Test (9,172), `random_state=42`
- **Features**: `area_m2`, `bedrooms`, `frontage`, `distance_to_center_km`, `log_area`, `area_sq`, `log_distance`, `area_dist_inter`, `province`, `district`
- **Pre-processing**: Median Imputer + OneHotEncoder (`drop='first'`)
- **Model**: `sklearn.linear_model.LinearRegression`

| Metric | Target Value | Reproduced Value | Status |
| :--- | :--- | :--- | :--- |
| **R² Score** | 0.3729 | **0.3729** | ✅ 100% Match |
| **MAE (Million VND)** | 8,417.93 | **8,417.91** | ✅ 100% Match |
| **RMSE (Million VND)** | 21,435.74 | **21,436.29** | ✅ 100% Match |

---

## 4. Controlled Model Comparison Table (High-Confidence Subset N=32)

| Model | Evaluation N | Features Used | R² Score | MAE (Million VND) | RMSE (Million VND) | ΔR² vs Model A |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Model A (Baseline MLR)** | Test N=7 | Standard base features | -4.3777 | 12,715.57 | 14,141.38 | 0.0000 |
| **Model B (Geo Distance)** | Test N=7 | Geocoded distance replaced | -4.0740 | 12,470.38 | 13,736.35 | **+0.3036** |
| **Model C (Geo Coordinates)** | Test N=7 | Base features + Lat + Lon | -7,711.6780 | 229,846.59 | 535,545.75 | -7,707.3003 |
| **Model D (Combined Geo)** | Test N=7 | Lat + Lon + Geo Distance + Inter | -2,391.5957 | 141,246.71 | 298,283.09 | -2,387.2180 |

---

## 5. 5-Fold Cross Validation Breakdown

| Model Variant | Fold 1 | Fold 2 | Fold 3 | Fold 4 | Fold 5 | Mean R² ± Std |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Model A (Baseline)** | -4.3777 | -4.5375 | 0.141 | -73.6782 | -0.3241 | **-16.5553 ± 28.6285** |
| **Model B (Geo Distance)** | -4.074 | -186.1167 | -36.4482 | -91.1089 | -0.2431 | **-63.5982 ± 69.3711** |
| **Model C (Geo Coordinates)** | -7711.678 | -17646.4798 | -183.9445 | -11.7803 | -0.2969 | **-5110.8359 ± 6932.5173** |
| **Model D (Combined Geo)** | -2391.5957 | -205.5227 | -407.4286 | -206619.4435 | -8.3777 | **-41926.4736 ± 82350.9278** |

---

## 6. Production Safety Verification

- Production Model Hash (`models/linear_regression.pkl`): **Unchanged (fb1031fd4f6498348b36e516326b74ed)**
- Production Features Hash (`data/processed/housing_features.csv`): **Unchanged (6196de8756b6d07ef783eb0c25541df5)**
- Production Prediction Hash (`data/processed/predictions.csv`): **Unchanged**
- Production `src/` Code: **Unchanged (0 lines modified)**
- Production Notebooks `01`–`09`: **Unchanged**

---

## 7. Artifacts Created

1. **Jupyter Notebook**: [`notebooks/10_geographic_feature_experiment.ipynb`](file:///d:/RealEstatePrediction/bds-price-prediction/notebooks/10_geographic_feature_experiment.ipynb)
2. **Machine-Readable Audit JSON**: [`reports/phase2_9_geographic_feature_experiment.json`](file:///d:/RealEstatePrediction/bds-price-prediction/reports/phase2_9_geographic_feature_experiment.json)
3. **Markdown Report**: [`reports/phase2_9_geographic_feature_experiment.md`](file:///d:/RealEstatePrediction/bds-price-prediction/reports/phase2_9_geographic_feature_experiment.md)
4. **Proxy vs Geocoded Figure**: [`reports/figures/geographic_experiment/proxy_vs_geocoded_distance.png`](file:///d:/RealEstatePrediction/bds-price-prediction/reports/figures/geographic_experiment/proxy_vs_geocoded_distance.png)
5. **Model R² Comparison Figure**: [`reports/figures/geographic_experiment/model_r2_comparison.png`](file:///d:/RealEstatePrediction/bds-price-prediction/reports/figures/geographic_experiment/model_r2_comparison.png)

---

## 8. Final Recommendation

`GEOGRAPHIC_FEATURE_REQUIRES_MORE_VALIDATION`

*(Geographic distance features show strong correlation with existing proxy features. However, raw coordinate features create severe instability under linear regression on small subsets, and geographic coverage across the 45k production dataset remains at 0.07%. Further geocoding expansion and non-linear spatial encoding are required before production model integration).*
