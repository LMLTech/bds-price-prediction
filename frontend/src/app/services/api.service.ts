import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import {
  PredictRequest,
  PredictResponse,
  ModelInfoResponse,
  LocationsResponse,
  VisualizationsResponse
} from '../models/prediction.model';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private baseUrl = 'http://localhost:8000';

  constructor(private http: HttpClient) {}

  getHealth(): Observable<{ status: string; model_loaded: boolean; model_name: string }> {
    return this.http.get<{ status: string; model_loaded: boolean; model_name: string }>(`${this.baseUrl}/api/health`);
  }

  predict(request: PredictRequest): Observable<PredictResponse> {
    return this.http.post<PredictResponse>(`${this.baseUrl}/api/predict`, request);
  }

  getModelInfo(): Observable<ModelInfoResponse> {
    return this.http.get<ModelInfoResponse>(`${this.baseUrl}/api/model-info`);
  }

  getLocations(): Observable<LocationsResponse> {
    return this.http.get<LocationsResponse>(`${this.baseUrl}/api/locations`);
  }

  getVisualizations(): Observable<VisualizationsResponse> {
    return this.http.get<VisualizationsResponse>(`${this.baseUrl}/api/visualizations`);
  }

  getFigureUrl(filename: string): string {
    return `${this.baseUrl}/static/figures/${filename}`;
  }
}
