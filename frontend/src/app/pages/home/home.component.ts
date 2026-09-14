import { Component, OnInit } from '@angular/core';
import { RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `
    <div class="page-container">
      <!-- HERO SECTION -->
      <section class="hero-section">
        <div class="hero-content">
          <div class="hero-badge">Hệ Thống Dự Báo Bất Động Sản Học Thuật</div>
          <h1 class="hero-title">Real Estate Price Prediction</h1>
          <p class="hero-subtitle">
            Dự báo giá bất động sản tại Việt Nam dựa trên thuộc tính tài sản và đặc trưng không gian
            sử dụng mô hình <strong>Multiple Linear Regression</strong>.
          </p>
          <div class="hero-actions">
            <a routerLink="/predict" class="btn btn-primary">
              ⚡ Dự Báo Giá Ngay
            </a>
            <a routerLink="/visualization" class="btn btn-secondary">
              📊 Khám Phá Trực Quan Hóa
            </a>
          </div>
        </div>
      </section>

      <!-- METRICS BANNER -->
      <section class="metrics-grid">
        <div class="metric-card">
          <div class="metric-value">0.3729</div>
          <div class="metric-label">Hệ số xác định (R²)</div>
          <div class="metric-sub">Giải thích 37.29% độ biến thiên giá trên tập test</div>
        </div>
        <div class="metric-card">
          <div class="metric-value">8,417.93</div>
          <div class="metric-label">Sai số tuyệt đối trung bình (MAE)</div>
          <div class="metric-sub">Đơn vị: Triệu VNĐ (≈ 8.42 Tỷ VNĐ)</div>
        </div>
        <div class="metric-card">
          <div class="metric-value">21,435.74</div>
          <div class="metric-label">Căn bậc hai sai số bình phương (RMSE)</div>
          <div class="metric-sub">Phản ánh ảnh hưởng của các điểm giá trị lớn</div>
        </div>
        <div class="metric-card">
          <div class="metric-value">9,172</div>
          <div class="metric-label">Kích thước tập kiểm thử</div>
          <div class="metric-sub">Mẫu bất động sản kiểm thử độc lập</div>
        </div>
      </section>

      <!-- PIPELINE WORKFLOW -->
      <section class="section-block">
        <h2 class="section-title">Quy Trình Xử Lý & Mô Hình Học Máy</h2>
        <p class="section-desc">Pipeline end-to-end từ dữ liệu thô đến dự báo thời gian thực trên giao diện web</p>
        
        <div class="pipeline-flow">
          <div class="pipeline-step">
            <div class="step-num">01</div>
            <div class="step-title">Dữ Liệu Thô</div>
            <div class="step-desc">69,000+ tin đăng bất động sản tại HN & TP.HCM</div>
          </div>
          <div class="flow-arrow">➔</div>
          <div class="pipeline-step">
            <div class="step-num">02</div>
            <div class="step-title">Làm Sạch</div>
            <div class="step-desc">Lọc ngưỡng miền thuộc tính & xử lý outlier</div>
          </div>
          <div class="flow-arrow">➔</div>
          <div class="pipeline-step">
            <div class="step-num">03</div>
            <div class="step-title">Feature Engineering</div>
            <div class="step-desc">Log transform, diện tích bậc 2, khoảng cách đại diện CBD</div>
          </div>
          <div class="flow-arrow">➔</div>
          <div class="pipeline-step">
            <div class="step-num">04</div>
            <div class="step-title">Linear Regression</div>
            <div class="step-desc">Huấn luyện Pipeline scikit-learn (280 đặc trưng)</div>
          </div>
          <div class="flow-arrow">➔</div>
          <div class="pipeline-step">
            <div class="step-num">05</div>
            <div class="step-title">FastAPI & Angular</div>
            <div class="step-desc">Dự báo real-time qua REST API thời gian thực</div>
          </div>
        </div>
      </section>

      <!-- SYSTEM HIGHLIGHTS -->
      <section class="features-grid">
        <div class="feature-box">
          <div class="feature-icon">🎯</div>
          <h3>Đơn Vị Nhất Quán</h3>
          <p>Mô hình sử dụng duy nhất mô hình huấn luyện <code>linear_regression.pkl</code>. Không huấn luyện lại khi gọi API.</p>
        </div>
        <div class="feature-box">
          <div class="feature-icon">📍</div>
          <h3>Distance Spatial Proxy</h3>
          <p>Khoảng cách tới trung tâm (distance_to_center_km) được nội suy tự động từ vị trí địa bàn Quận/Huyện đại diện.</p>
        </div>
        <div class="feature-box">
          <div class="feature-icon">📈</div>
          <h3>15 Báo Cáo Trực Quan</h3>
          <p>Tái sử dụng toàn bộ 15 biểu đồ chuẩn học thuật phân tích dữ liệu, tương quan, hiệu năng và sai số mô hình.</p>
        </div>
      </section>
    </div>
  `,
  styles: [`
    .page-container {
      max-width: 1240px;
      margin: 0 auto;
      padding: 2.5rem 1.5rem;
    }
    .hero-section {
      text-align: center;
      padding: 3rem 1rem 3.5rem 1rem;
      background: radial-gradient(circle at top, rgba(59, 130, 246, 0.15) 0%, transparent 70%);
      border-radius: 20px;
      border: 1px solid rgba(255, 255, 255, 0.06);
      margin-bottom: 2.5rem;
    }
    .hero-badge {
      display: inline-block;
      background: rgba(99, 102, 241, 0.15);
      color: #818cf8;
      border: 1px solid rgba(99, 102, 241, 0.3);
      padding: 0.35rem 0.9rem;
      border-radius: 99px;
      font-size: 0.85rem;
      font-weight: 600;
      margin-bottom: 1.2rem;
    }
    .hero-title {
      font-size: 2.8rem;
      font-weight: 800;
      color: #f8fafc;
      letter-spacing: -0.03em;
      margin: 0 0 1rem 0;
      line-height: 1.15;
    }
    .hero-subtitle {
      font-size: 1.15rem;
      color: #94a3b8;
      max-width: 720px;
      margin: 0 auto 2rem auto;
      line-height: 1.6;
    }
    .hero-actions {
      display: flex;
      justify-content: center;
      gap: 1rem;
    }
    .btn {
      padding: 0.8rem 1.6rem;
      border-radius: 10px;
      font-weight: 600;
      text-decoration: none;
      font-size: 0.98rem;
      transition: all 0.2s ease;
      cursor: pointer;
    }
    .btn-primary {
      background: linear-gradient(135deg, #2563eb, #4f46e5);
      color: #ffffff;
      box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35);
    }
    .btn-primary:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 20px rgba(37, 99, 235, 0.5);
    }
    .btn-secondary {
      background: #1e293b;
      color: #e2e8f0;
      border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .btn-secondary:hover {
      background: #334155;
      color: #ffffff;
    }
    .metrics-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 1.2rem;
      margin-bottom: 3rem;
    }
    .metric-card {
      background: #0f172a;
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 14px;
      padding: 1.5rem;
      text-align: center;
    }
    .metric-value {
      font-size: 2rem;
      font-weight: 800;
      color: #60a5fa;
      margin-bottom: 0.3rem;
    }
    .metric-label {
      font-weight: 600;
      color: #e2e8f0;
      font-size: 0.95rem;
      margin-bottom: 0.3rem;
    }
    .metric-sub {
      font-size: 0.8rem;
      color: #64748b;
    }
    .section-block {
      background: #0f172a;
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 16px;
      padding: 2.2rem;
      margin-bottom: 3rem;
    }
    .section-title {
      font-size: 1.6rem;
      font-weight: 700;
      color: #f8fafc;
      margin: 0 0 0.4rem 0;
    }
    .section-desc {
      color: #94a3b8;
      margin: 0 0 2rem 0;
      font-size: 0.98rem;
    }
    .pipeline-flow {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 0.8rem;
      overflow-x: auto;
      padding-bottom: 0.5rem;
    }
    .pipeline-step {
      background: #1e293b;
      border: 1px solid rgba(255, 255, 255, 0.06);
      border-radius: 12px;
      padding: 1.2rem;
      flex: 1;
      min-width: 170px;
    }
    .step-num {
      font-size: 0.75rem;
      font-weight: 800;
      color: #818cf8;
      margin-bottom: 0.4rem;
    }
    .step-title {
      font-weight: 700;
      color: #f1f5f9;
      font-size: 0.95rem;
      margin-bottom: 0.4rem;
    }
    .step-desc {
      font-size: 0.8rem;
      color: #94a3b8;
      line-height: 1.4;
    }
    .flow-arrow {
      color: #475569;
      font-size: 1.2rem;
      font-weight: 700;
    }
    .features-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 1.5rem;
    }
    .feature-box {
      background: #0f172a;
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 14px;
      padding: 1.6rem;
    }
    .feature-icon {
      font-size: 1.8rem;
      margin-bottom: 0.8rem;
    }
    .feature-box h3 {
      font-size: 1.1rem;
      color: #f8fafc;
      margin: 0 0 0.5rem 0;
    }
    .feature-box p {
      font-size: 0.9rem;
      color: #94a3b8;
      margin: 0;
      line-height: 1.5;
    }
  `]
})
export class HomeComponent {}
