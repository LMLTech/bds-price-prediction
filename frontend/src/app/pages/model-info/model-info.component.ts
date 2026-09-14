import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../services/api.service';
import { ModelInfoResponse } from '../../models/prediction.model';

@Component({
  selector: 'app-model-info',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="page-container">
      <div class="header-block">
        <h1 class="page-title">Thông Tin Chi Tiết Mô Hình Học Máy</h1>
        <p class="page-subtitle">Kiến trúc, tập đặc trưng, chỉ số đánh giá và hạn chế học thuật của mô hình Multiple Linear Regression</p>
      </div>

      <!-- MAIN MODEL INFO CARD -->
      <div class="info-grid">
        <div class="card model-card">
          <h2 class="card-title">MÔ HÌNH DỰ BÁO CHÍNH</h2>
          <div class="model-name">Multiple Linear Regression</div>
          <div class="model-lib">Thuật toán: <code>sklearn.linear_model.LinearRegression</code></div>
          <div class="model-file">Model File: <code>models/linear_regression.pkl</code></div>

          <div class="badge-list">
            <span class="badge">280 Feature Dimensions</span>
            <span class="badge">ColumnTransformer Preprocessing</span>
            <span class="badge">One-Hot Encoding (Ignore Unknown)</span>
          </div>
        </div>

        <!-- METRICS CARD -->
        <div class="card metrics-card">
          <h2 class="card-title">CHỈ SỐ ĐÁNH GIÁ (TEST SET METRICS)</h2>

          <div class="metrics-comparison">
            <div class="metric-box">
              <div class="box-tag">Raw Linear Regression</div>
              <div class="m-item">
                <span class="m-label">R² (Explained Variance):</span>
                <span class="m-val highlight">0.3729</span>
              </div>
              <div class="m-item">
                <span class="m-label">MAE (Mean Absolute Error):</span>
                <span class="m-val">8,417.93 triệu VNĐ</span>
              </div>
              <div class="m-item">
                <span class="m-label">RMSE (Root Mean Sq Error):</span>
                <span class="m-val">21,435.74 triệu VNĐ</span>
              </div>
            </div>

            <div class="metric-box">
              <div class="box-tag">Clipped Post-Processing</div>
              <div class="m-item">
                <span class="m-label">R² (Clipped):</span>
                <span class="m-val highlight">0.3839</span>
              </div>
              <div class="m-item">
                <span class="m-label">MAE (Clipped):</span>
                <span class="m-val">8,065.00 triệu VNĐ</span>
              </div>
              <div class="m-item">
                <span class="m-label">RMSE (Clipped):</span>
                <span class="m-val">21,247.69 triệu VNĐ</span>
              </div>
            </div>
          </div>

          <p class="metric-note">
            * Kích thước tập kiểm thử: <strong>9,172 mẫu</strong> (Test Set độc lập).
          </p>
        </div>
      </div>

      <!-- FEATURE ENGINEERING & PREPROCESSING -->
      <div class="card full-card">
        <h2 class="card-title">TẬP ĐẶC TRƯNG VÀ TIỀN XỬ LÝ (FEATURE SPACE)</h2>
        <div class="features-split">
          <div class="f-col">
            <h4>1. Đặc trưng số nguyên bản & biến đổi (Numerical Features):</h4>
            <ul>
              <li><code>area_m2</code>: Diện tích mặt bằng bất động sản (m²)</li>
              <li><code>log_area</code>: <code>np.log1p(area_m2)</code> - Xử lý tính tiệm cận của diện tích</li>
              <li><code>area_sq</code>: <code>area_m2²</code> - Đặc trưng bậc 2 trong khuôn khổ tuyến tính</li>
              <li><code>bedrooms</code>: Số phòng ngủ</li>
              <li><code>frontage</code>: Chiều rộng mặt tiền (m)</li>
              <li><code>distance_to_center_km</code>: Khoảng cách Haversine tới trung tâm (Location Spatial Proxy)</li>
              <li><code>log_distance</code>: <code>np.log1p(distance_to_center_km)</code></li>
              <li><code>area_dist_inter</code>: <code>area_m2 * distance_to_center_km</code> - Biến tương tác không gian</li>
            </ul>
          </div>
          <div class="f-col">
            <h4>2. Đặc trưng phân loại (Categorical Dummy Features):</h4>
            <ul>
              <li><code>province</code>: Tỉnh / Thành phố (Hà Nội, TP. Hồ Chí Minh)</li>
              <li><code>district</code>: Quận / Huyện (272 danh mục sau khi One-Hot Encoding)</li>
              <li>Xử lý giá trị thiếu: <code>SimpleImputer(strategy='most_frequent')</code></li>
              <li>Xử lý danh mục mới: <code>OneHotEncoder(handle_unknown='ignore')</code></li>
            </ul>
          </div>
        </div>
      </div>

      <!-- ACADEMIC LIMITATIONS -->
      <div class="card full-card limitations-card">
        <h2 class="card-title">HẠN CHẾ VÀ GHI CHÚ HỌC THUẬT (ACADEMIC LIMITATIONS)</h2>
        <div class="limitations-list">
          <div class="limit-item">
            <span class="limit-num">1</span>
            <div>
              <strong>Location Spatial Proxy</strong>: Giá trị <code>distance_to_center_km</code> được tính dựa trên tọa độ trung tâm đại diện cấp Quận/Huyện (District Representative Center), không phải tọa độ GPS chính xác của từng căn nhà.
            </div>
          </div>
          <div class="limit-item">
            <span class="limit-num">2</span>
            <div>
              <strong>Biến Không Quan Sát Được (Unobserved Attributes)</strong>: Thị trường bất động sản phụ thuộc nhiều vào tình trạng nội thất, chất lượng xây dựng, pháp lý (sổ đỏ/sổ hồng), phong thủy - các yếu tố chưa ghi nhận đầy đủ trong tin đăng.
            </div>
          </div>
          <div class="limit-item">
            <span class="limit-num">3</span>
            <div>
              <strong>Post-Processing Clipping</strong>: Phép xấp xỉ <code>np.maximum(prediction, 0)</code> là bước hậu xử lý nhằm đảm bảo tính thực tế của giá trị đầu ra, không phải là thuộc tính tự nhiên của mô hình Hồi quy Tuyến tính.
            </div>
          </div>
          <div class="limit-item">
            <span class="limit-num">4</span>
            <div>
              <strong>Đuôi Phân Phối Giá Cao</strong>: RMSE lớn hơn MAE đáng kể phản ảnh ảnh hưởng của các bất động sản phân khúc siêu sang hoặc giá trị lớn trong tập dữ liệu.
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
    .info-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1.5rem;
      margin-bottom: 2rem;
    }
    @media (max-width: 860px) {
      .info-grid {
        grid-template-columns: 1fr;
      }
    }
    .card {
      background: #0f172a;
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 16px;
      padding: 2rem;
    }
    .full-card {
      margin-bottom: 2rem;
    }
    .card-title {
      font-size: 1.1rem;
      font-weight: 700;
      color: #38bdf8;
      letter-spacing: 0.04em;
      margin: 0 0 1.2rem 0;
      padding-bottom: 0.6rem;
      border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    }
    .model-name {
      font-size: 1.8rem;
      font-weight: 800;
      color: #f8fafc;
      margin-bottom: 0.5rem;
    }
    .model-lib, .model-file {
      font-size: 0.9rem;
      color: #94a3b8;
      margin-bottom: 0.4rem;
    }
    code {
      font-family: monospace;
      background: #1e293b;
      color: #60a5fa;
      padding: 0.2rem 0.5rem;
      border-radius: 6px;
      font-size: 0.85rem;
    }
    .badge-list {
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
      margin-top: 1.2rem;
    }
    .badge {
      background: rgba(99, 102, 241, 0.15);
      color: #818cf8;
      border: 1px solid rgba(99, 102, 241, 0.25);
      padding: 0.35rem 0.75rem;
      border-radius: 8px;
      font-size: 0.8rem;
      font-weight: 600;
    }
    .metrics-comparison {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1rem;
      margin-bottom: 1rem;
    }
    .metric-box {
      background: #1e293b;
      border-radius: 12px;
      padding: 1.2rem;
    }
    .box-tag {
      font-size: 0.78rem;
      font-weight: 700;
      color: #94a3b8;
      text-transform: uppercase;
      margin-bottom: 0.8rem;
    }
    .m-item {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 0.5rem;
      font-size: 0.88rem;
    }
    .m-label {
      color: #cbd5e1;
    }
    .m-val {
      font-weight: 700;
      color: #f8fafc;
    }
    .m-val.highlight {
      color: #34d399;
      font-size: 1.1rem;
    }
    .metric-note {
      font-size: 0.82rem;
      color: #64748b;
      margin: 0;
    }
    .features-split {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 2rem;
    }
    @media (max-width: 768px) {
      .features-split {
        grid-template-columns: 1fr;
      }
    }
    .f-col h4 {
      color: #f1f5f9;
      margin: 0 0 0.8rem 0;
      font-size: 1rem;
    }
    .f-col ul {
      padding-left: 1.2rem;
      margin: 0;
      color: #94a3b8;
      font-size: 0.9rem;
      line-height: 1.6;
    }
    .limitations-list {
      display: flex;
      flex-direction: column;
      gap: 1rem;
    }
    .limit-item {
      display: flex;
      align-items: flex-start;
      gap: 1rem;
      background: #1e293b;
      padding: 1.2rem;
      border-radius: 12px;
      color: #cbd5e1;
      font-size: 0.92rem;
      line-height: 1.5;
    }
    .limit-num {
      background: rgba(244, 63, 94, 0.15);
      color: #fb7185;
      font-weight: 800;
      font-size: 0.9rem;
      width: 28px;
      height: 28px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
    }
  `]
})
export class ModelInfoComponent implements OnInit {
  modelInfo: ModelInfoResponse | null = null;

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    this.apiService.getModelInfo().subscribe({
      next: (res) => {
        this.modelInfo = res;
      }
    });
  }
}
