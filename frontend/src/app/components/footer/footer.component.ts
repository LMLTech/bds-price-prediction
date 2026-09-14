import { Component } from '@angular/core';

@Component({
  selector: 'app-footer',
  standalone: true,
  template: `
    <footer class="footer">
      <div class="footer-container">
        <div class="footer-info">
          <h4>Real Estate Price Prediction Web Application</h4>
          <p>Mô hình dự báo giá bất động sản sử dụng Multiple Linear Regression trên dữ liệu thực tế tại Việt Nam.</p>
        </div>
        <div class="footer-meta">
          <span class="tech-tag">Angular 19</span>
          <span class="tech-tag">FastAPI</span>
          <span class="tech-tag">scikit-learn</span>
          <span class="tech-tag">Multiple Linear Regression</span>
        </div>
      </div>
    </footer>
  `,
  styles: [`
    .footer {
      background: #090d16;
      border-top: 1px solid rgba(255, 255, 255, 0.08);
      color: #64748b;
      padding: 2rem 1.5rem;
      margin-top: auto;
    }
    .footer-container {
      max-width: 1240px;
      margin: 0 auto;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 1rem;
    }
    .footer-info h4 {
      color: #e2e8f0;
      font-size: 0.95rem;
      margin: 0 0 0.25rem 0;
    }
    .footer-info p {
      font-size: 0.85rem;
      margin: 0;
    }
    .footer-meta {
      display: flex;
      gap: 0.5rem;
      flex-wrap: wrap;
    }
    .tech-tag {
      background: #1e293b;
      color: #94a3b8;
      padding: 0.25rem 0.6rem;
      border-radius: 6px;
      font-size: 0.75rem;
      border: 1px solid rgba(255, 255, 255, 0.05);
    }
  `]
})
export class FooterComponent {}
