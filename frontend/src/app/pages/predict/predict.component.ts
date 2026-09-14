import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../services/api.service';
import { PredictRequest, PredictResponse, LocationProvince } from '../../models/prediction.model';

@Component({
  selector: 'app-predict',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="page-container">
      <div class="header-block">
        <h1 class="page-title">Dự Báo Giá Bất Động Sản</h1>
        <p class="page-subtitle">Nhập thuộc tính tài sản và vị trí để mô hình Multiple Linear Regression tính toán giá ước tính</p>
      </div>

      <div class="predict-grid">
        <!-- FORM CONTAINER -->
        <div class="card form-card">
          <h2 class="card-title">THÔNG TIN BẤT ĐỘNG SẢN</h2>
          
          <form (ngSubmit)="onPredict()" #predictForm="ngForm">
            <!-- AREA -->
            <div class="form-group">
              <label for="area_m2">Diện tích (m²) <span class="required">*</span></label>
              <input
                type="number"
                id="area_m2"
                name="area_m2"
                [(ngModel)]="form.area_m2"
                required
                min="1"
                step="0.5"
                placeholder="Ví dụ: 85"
                class="form-control"
              />
              <span class="field-hint">Nhập diện tích sử dụng lớn hơn 0 m²</span>
            </div>

            <!-- BEDROOMS & FRONTAGE -->
            <div class="form-row">
              <div class="form-group">
                <label for="bedrooms">Số phòng ngủ <span class="required">*</span></label>
                <input
                  type="number"
                  id="bedrooms"
                  name="bedrooms"
                  [(ngModel)]="form.bedrooms"
                  required
                  min="0"
                  placeholder="Ví dụ: 3"
                  class="form-control"
                />
              </div>

              <div class="form-group">
                <label for="frontage">Mặt tiền (m) <span class="required">*</span></label>
                <input
                  type="number"
                  id="frontage"
                  name="frontage"
                  [(ngModel)]="form.frontage"
                  required
                  min="0"
                  step="0.5"
                  placeholder="Ví dụ: 5.0"
                  class="form-control"
                />
              </div>
            </div>

            <!-- PROVINCE -->
            <div class="form-group">
              <label for="province">Tỉnh / Thành phố <span class="required">*</span></label>
              <select
                id="province"
                name="province"
                [(ngModel)]="form.province"
                (change)="onProvinceChange()"
                required
                class="form-control"
              >
                <option value="" disabled selected>-- Chọn Tỉnh/Thành phố --</option>
                <option *ngFor="let p of provinces" [value]="p.name">{{ p.name }}</option>
              </select>
            </div>

            <!-- DISTRICT -->
            <div class="form-group">
              <label for="district">Quận / Huyện <span class="required">*</span></label>
              <select
                id="district"
                name="district"
                [(ngModel)]="form.district"
                [disabled]="!availableDistricts.length"
                required
                class="form-control"
              >
                <option value="" disabled selected>-- Chọn Quận/Huyện --</option>
                <option *ngFor="let d of availableDistricts" [value]="d">{{ d }}</option>
              </select>
            </div>

            <!-- ERROR ALERT -->
            <div *ngIf="errorMessage" class="alert alert-danger">
              ⚠️ {{ errorMessage }}
            </div>

            <!-- SUBMIT BUTTON -->
            <button
              type="submit"
              [disabled]="loading || !predictForm.form.valid"
              class="btn-submit"
            >
              <span *ngIf="!loading">⚡ Predict Price (Dự Báo Giá)</span>
              <span *ngIf="loading">⌛ Đang tính toán...</span>
            </button>
          </form>
        </div>

        <!-- RESULT CONTAINER -->
        <div class="card result-card">
          <div *ngIf="!result && !loading" class="empty-state">
            <div class="empty-icon">🏠</div>
            <h3>Chưa có kết quả dự báo</h3>
            <p>Vui lòng điền thông tin thuộc tính bên trái và nhấn <strong>Predict Price</strong></p>
          </div>

          <div *ngIf="loading" class="loading-state">
            <div class="spinner"></div>
            <p>Mô hình đang thực thi Pipeline và quy đổi đặc trưng...</p>
          </div>

          <div *ngIf="result && !loading" class="result-content">
            <div class="result-badge">GIÁ DỰ BÁO ƯỚC TÍNH</div>

            <div class="price-hero">
              <div class="price-formatted">{{ result.predicted_price_formatted }}</div>
              <div class="price-sub">≈ {{ result.predicted_price_million_vnd | number:'1.2-2' }} triệu VNĐ</div>
              <div class="price-raw">({{ result.predicted_price_vnd | number:'1.0-0' }} VNĐ)</div>
            </div>

            <!-- SUMMARY PILLS -->
            <div class="summary-box">
              <div class="box-title">Tóm Tắt Bất Động Sản</div>
              <div class="pills-grid">
                <span class="pill">📐 {{ result.inputs.area_m2 }} m²</span>
                <span class="pill">🛏️ {{ result.inputs.bedrooms }} Phòng ngủ</span>
                <span class="pill">🚪 {{ result.inputs.frontage }}m Mặt tiền</span>
                <span class="pill">📍 {{ result.inputs.district }}, {{ result.inputs.province }}</span>
              </div>
            </div>

            <!-- DERIVED FEATURES EDUCATIONAL SECTION -->
            <div class="derived-box">
              <div class="derived-header" (click)="toggleDerived()">
                <span>💡 Đặc Trưng Biến Đổi Nội Bộ (Backend Derived Features)</span>
                <span>{{ showDerived ? '▲' : '▼' }}</span>
              </div>

              <div *ngIf="showDerived" class="derived-body">
                <div class="derived-item">
                  <span class="derived-key">Distance Proxy:</span>
                  <span class="derived-val">{{ result.derived_features.distance_to_center_km }} km</span>
                </div>
                <div class="derived-item">
                  <span class="derived-key">log_area (log1p):</span>
                  <span class="derived-val">{{ result.derived_features.log_area }}</span>
                </div>
                <div class="derived-item">
                  <span class="derived-key">area_sq (m²²):</span>
                  <span class="derived-val">{{ result.derived_features.area_sq }}</span>
                </div>
                <div class="derived-item">
                  <span class="derived-key">log_distance:</span>
                  <span class="derived-val">{{ result.derived_features.log_distance }}</span>
                </div>
                <div class="derived-item">
                  <span class="derived-key">area_dist_inter:</span>
                  <span class="derived-val">{{ result.derived_features.area_dist_inter }}</span>
                </div>
              </div>
            </div>

            <div class="model-footnote">
              Mô hình: <strong>{{ result.model_name }}</strong> (scikit-learn Pipeline)
            </div>
          </div>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .page-container {
      max-width: 1240px;
      margin: 0 auto;
      padding: 2.5rem 1.5rem;
    }
    .header-block {
      margin-bottom: 2rem;
    }
    .page-title {
      font-size: 2.2rem;
      font-weight: 800;
      color: #f8fafc;
      margin: 0 0 0.4rem 0;
    }
    .page-subtitle {
      color: #94a3b8;
      font-size: 1.05rem;
      margin: 0;
    }
    .predict-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 2rem;
    }
    @media (max-width: 860px) {
      .predict-grid {
        grid-template-columns: 1fr;
      }
    }
    .card {
      background: #0f172a;
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 16px;
      padding: 2rem;
    }
    .card-title {
      font-size: 1.15rem;
      font-weight: 700;
      color: #38bdf8;
      letter-spacing: 0.04em;
      margin: 0 0 1.5rem 0;
      padding-bottom: 0.8rem;
      border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    }
    .form-group {
      margin-bottom: 1.2rem;
    }
    .form-row {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1rem;
    }
    label {
      display: block;
      font-weight: 600;
      color: #cbd5e1;
      font-size: 0.9rem;
      margin-bottom: 0.4rem;
    }
    .required {
      color: #f43f5e;
    }
    .form-control {
      width: 100%;
      background: #1e293b;
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 10px;
      padding: 0.75rem 1rem;
      color: #f8fafc;
      font-size: 0.95rem;
      box-sizing: border-box;
      transition: all 0.2s ease;
    }
    .form-control:focus {
      outline: none;
      border-color: #3b82f6;
      box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.25);
    }
    .field-hint {
      display: block;
      font-size: 0.75rem;
      color: #64748b;
      margin-top: 0.3rem;
    }
    .alert-danger {
      background: rgba(225, 29, 72, 0.15);
      border: 1px solid rgba(225, 29, 72, 0.3);
      color: #fda4af;
      padding: 0.8rem 1rem;
      border-radius: 8px;
      font-size: 0.88rem;
      margin-bottom: 1.2rem;
    }
    .btn-submit {
      width: 100%;
      background: linear-gradient(135deg, #2563eb, #4f46e5);
      color: #ffffff;
      border: none;
      padding: 0.9rem;
      border-radius: 10px;
      font-weight: 700;
      font-size: 1.05rem;
      cursor: pointer;
      transition: all 0.2s ease;
      box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35);
    }
    .btn-submit:hover:not(:disabled) {
      transform: translateY(-2px);
      box-shadow: 0 6px 20px rgba(37, 99, 235, 0.5);
    }
    .btn-submit:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }
    .empty-state {
      text-align: center;
      padding: 4rem 1.5rem;
      color: #64748b;
    }
    .empty-icon {
      font-size: 3.5rem;
      margin-bottom: 1rem;
    }
    .empty-state h3 {
      color: #cbd5e1;
      font-size: 1.2rem;
      margin: 0 0 0.5rem 0;
    }
    .loading-state {
      text-align: center;
      padding: 5rem 1.5rem;
      color: #94a3b8;
    }
    .spinner {
      width: 40px;
      height: 40px;
      border: 4px solid rgba(255, 255, 255, 0.1);
      border-top-color: #3b82f6;
      border-radius: 50%;
      animation: spin 0.8s linear infinite;
      margin: 0 auto 1.2rem auto;
    }
    @keyframes spin {
      to { transform: rotate(360deg); }
    }
    .result-badge {
      display: inline-block;
      background: rgba(34, 197, 94, 0.15);
      color: #4ade80;
      border: 1px solid rgba(34, 197, 94, 0.3);
      padding: 0.3rem 0.75rem;
      border-radius: 99px;
      font-size: 0.75rem;
      font-weight: 700;
      margin-bottom: 1.2rem;
    }
    .price-hero {
      text-align: center;
      background: rgba(15, 23, 42, 0.6);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 14px;
      padding: 1.8rem;
      margin-bottom: 1.5rem;
    }
    .price-formatted {
      font-size: 3rem;
      font-weight: 900;
      color: #38bdf8;
      letter-spacing: -0.02em;
      line-height: 1.1;
      margin-bottom: 0.5rem;
    }
    .price-sub {
      font-size: 1.1rem;
      font-weight: 600;
      color: #e2e8f0;
    }
    .price-raw {
      font-size: 0.85rem;
      color: #64748b;
      margin-top: 0.2rem;
    }
    .summary-box {
      background: #1e293b;
      border-radius: 12px;
      padding: 1.2rem;
      margin-bottom: 1.2rem;
    }
    .box-title {
      font-size: 0.85rem;
      font-weight: 700;
      color: #94a3b8;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 0.8rem;
    }
    .pills-grid {
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
    }
    .pill {
      background: #0f172a;
      color: #e2e8f0;
      border: 1px solid rgba(255, 255, 255, 0.06);
      padding: 0.4rem 0.8rem;
      border-radius: 8px;
      font-size: 0.85rem;
      font-weight: 500;
    }
    .derived-box {
      background: #1e293b;
      border-radius: 12px;
      overflow: hidden;
      margin-bottom: 1.2rem;
    }
    .derived-header {
      padding: 0.9rem 1.2rem;
      background: rgba(255, 255, 255, 0.03);
      color: #cbd5e1;
      font-size: 0.85rem;
      font-weight: 600;
      display: flex;
      justify-content: space-between;
      cursor: pointer;
    }
    .derived-body {
      padding: 0.9rem 1.2rem;
      border-top: 1px solid rgba(255, 255, 255, 0.05);
    }
    .derived-item {
      display: flex;
      justify-content: space-between;
      font-size: 0.82rem;
      padding: 0.3rem 0;
    }
    .derived-key {
      color: #94a3b8;
      font-family: monospace;
    }
    .derived-val {
      color: #38bdf8;
      font-weight: 600;
      font-family: monospace;
    }
    .model-footnote {
      font-size: 0.8rem;
      color: #64748b;
      text-align: center;
    }
  `]
})
export class PredictComponent implements OnInit {
  provinces: LocationProvince[] = [];
  availableDistricts: string[] = [];

  form: PredictRequest = {
    area_m2: 85,
    bedrooms: 3,
    frontage: 5,
    province: 'TP. Hồ Chí Minh',
    district: 'Quận 7'
  };

  loading = false;
  errorMessage = '';
  result: PredictResponse | null = null;
  showDerived = false;

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    this.loadLocations();
  }

  loadLocations(): void {
    this.apiService.getLocations().subscribe({
      next: (res) => {
        this.provinces = res.provinces;
        if (this.provinces.length > 0) {
          // Default selection matching initial form values
          const matchedProv = this.provinces.find(p => p.name === this.form.province) || this.provinces[0];
          this.form.province = matchedProv.name;
          this.availableDistricts = matchedProv.districts;
          if (!this.availableDistricts.includes(this.form.district)) {
            this.form.district = this.availableDistricts[0] || '';
          }
        }
      },
      error: () => {
        this.errorMessage = 'Không thể tải danh sách vị trí từ Backend.';
      }
    });
  }

  onProvinceChange(): void {
    const selected = this.provinces.find(p => p.name === this.form.province);
    if (selected) {
      this.availableDistricts = selected.districts;
      this.form.district = this.availableDistricts[0] || '';
    } else {
      this.availableDistricts = [];
      this.form.district = '';
    }
  }

  onPredict(): void {
    if (this.form.area_m2 <= 0) {
      this.errorMessage = 'Diện tích phải lớn hơn 0 m².';
      return;
    }
    if (this.form.bedrooms < 0 || this.form.frontage < 0) {
      this.errorMessage = 'Số phòng ngủ và mặt tiền không được nhỏ hơn 0.';
      return;
    }

    this.errorMessage = '';
    this.loading = true;
    this.result = null;

    this.apiService.predict(this.form).subscribe({
      next: (res) => {
        this.result = res;
        this.loading = false;
      },
      error: (err) => {
        this.loading = false;
        this.errorMessage = err.error?.detail || 'Không thể tạo dự báo. Vui lòng kiểm tra lại thông tin đầu vào.';
      }
    });
  }

  toggleDerived(): void {
    this.showDerived = !this.showDerived;
  }
}
