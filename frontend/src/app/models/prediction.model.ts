export interface PredictRequest {
  area_m2: number;
  bedrooms: number;
  frontage: number;
  province: string;
  district: string;
}

export interface DerivedFeatures {
  log_area: number;
  area_sq: number;
  distance_to_center_km: number;
  log_distance: number;
  area_dist_inter: number;
}

export interface PredictResponse {
  predicted_price_million_vnd: number;
  predicted_price_vnd: number;
  predicted_price_formatted: string;
  inputs: PredictRequest;
  derived_features: DerivedFeatures;
  model_name: string;
}

export interface ModelMetrics {
  r2: number;
  mae_million_vnd: number;
  rmse_million_vnd: number;
}

export interface ModelInfoResponse {
  model_name: string;
  algorithm: string;
  model_path: string;
  test_metrics: {
    raw: ModelMetrics;
    clipped: ModelMetrics;
  };
  test_samples: number;
  total_features: number;
  numerical_features: string[];
  categorical_features: string[];
  target_unit: string;
}

export interface LocationProvince {
  name: string;
  districts: string[];
}

export interface LocationsResponse {
  provinces: LocationProvince[];
}

export interface VisualizationItem {
  id: string;
  title: string;
  category: string;
  filename: string;
  url: string;
  description: string;
  exists: boolean;
}

export interface VisualizationsResponse {
  visualizations: VisualizationItem[];
  categories: string[];
}
