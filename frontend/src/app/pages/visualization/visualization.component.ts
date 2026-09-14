import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../services/api.service';
import { VisualizationItem } from '../../models/prediction.model';

@Component({
  selector: 'app-visualization',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="page-container">
      <div class="header-block">
        <h1 class="page-title">Trực Quan Hóa Báo Cáo Học Thuật</h1>
        <p class="page-subtitle">Tập hợp 15 biểu đồ báo cáoEDA, đặc trưng không gian, hiệu năng mô hình và phân tích sai số</p>
      </div>

      <!-- CATEGORY TABS -->
      <div class="tabs-container">
        <button
          *ngFor="let cat of categories"
          [class.active]="selectedCategory === cat"
          (click)="selectCategory(cat)"
          class="tab-btn"
        >
          {{ getCategoryLabel(cat) }}
        </button>
      </div>

      <!-- VISUALIZATIONS GRID -->
      <div *ngIf="loading" class="loading-box">
        ⌛ Đang tải danh sách trực quan hóa...
      </div>

      <div *ngIf="!loading" class="viz-grid">
        <div *ngFor="let item of filteredVisualizations" class="viz-card">
          <div class="viz-header">
            <span class="viz-category">{{ item.category }}</span>
            <h3 class="viz-title">{{ item.title }}</h3>
          </div>

          <div class="viz-image-wrapper">
            <img
              [src]="apiService.getFigureUrl(item.filename)"
              [alt]="item.title"
              class="viz-image"
              loading="lazy"
            />
          </div>

          <div class="viz-footer">
            <p class="viz-description">{{ item.description }}</p>
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
    .tabs-container {
      display: flex;
      gap: 0.6rem;
      margin-bottom: 2rem;
      overflow-x: auto;
      padding-bottom: 0.4rem;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }
    .tab-btn {
      background: #1e293b;
      color: #94a3b8;
      border: 1px solid rgba(255, 255, 255, 0.06);
      padding: 0.65rem 1.2rem;
      border-radius: 10px;
      font-weight: 600;
      font-size: 0.92rem;
      cursor: pointer;
      transition: all 0.2s ease;
      white-space: nowrap;
    }
    .tab-btn:hover {
      color: #f8fafc;
      background: #334155;
    }
    .tab-btn.active {
      background: linear-gradient(135deg, #2563eb, #4f46e5);
      color: #ffffff;
      border-color: transparent;
      box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
    }
    .loading-box {
      text-align: center;
      padding: 4rem;
      color: #94a3b8;
    }
    .viz-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
      gap: 2rem;
    }
    @media (max-width: 640px) {
      .viz-grid {
        grid-template-columns: 1fr;
      }
    }
    .viz-card {
      background: #0f172a;
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 16px;
      overflow: hidden;
      display: flex;
      flex-direction: column;
    }
    .viz-header {
      padding: 1.2rem 1.5rem 0.8rem 1.5rem;
    }
    .viz-category {
      display: inline-block;
      background: rgba(99, 102, 241, 0.15);
      color: #818cf8;
      padding: 0.2rem 0.6rem;
      border-radius: 6px;
      font-size: 0.72rem;
      font-weight: 700;
      margin-bottom: 0.4rem;
    }
    .viz-title {
      font-size: 1.15rem;
      font-weight: 700;
      color: #f8fafc;
      margin: 0;
    }
    .viz-image-wrapper {
      background: #020617;
      padding: 1rem;
      display: flex;
      justify-content: center;
      align-items: center;
      border-top: 1px solid rgba(255, 255, 255, 0.04);
      border-bottom: 1px solid rgba(255, 255, 255, 0.04);
    }
    .viz-image {
      max-width: 100%;
      height: auto;
      border-radius: 8px;
    }
    .viz-footer {
      padding: 1.2rem 1.5rem;
    }
    .viz-description {
      font-size: 0.9rem;
      color: #cbd5e1;
      line-height: 1.55;
      margin: 0;
    }
  `]
})
export class VisualizationComponent implements OnInit {
  visualizations: VisualizationItem[] = [];
  categories: string[] = ['All', 'Dataset', 'Property', 'Location', 'Model', 'Error'];
  selectedCategory = 'All';
  loading = true;

  constructor(public apiService: ApiService) {}

  ngOnInit(): void {
    this.loadVisualizations();
  }

  loadVisualizations(): void {
    this.apiService.getVisualizations().subscribe({
      next: (res) => {
        this.visualizations = res.visualizations;
        this.loading = false;
      },
      error: () => {
        this.loading = false;
      }
    });
  }

  selectCategory(cat: string): void {
    this.selectedCategory = cat;
  }

  get filteredVisualizations(): VisualizationItem[] {
    if (this.selectedCategory === 'All') {
      return this.visualizations;
    }
    return this.visualizations.filter(v => v.category === this.selectedCategory);
  }

  getCategoryLabel(cat: string): string {
    const map: Record<string, string> = {
      'All': '🌐 Tất Cả (15 Charts)',
      'Dataset': '📁 Dataset Overview',
      'Property': '🏠 Đặc Trưng BĐS',
      'Location': '📍 Vị Trí & Khoảng Cách',
      'Model': '📈 Hiệu Năng Mô Hình',
      'Error': '⚠️ Phân Tích Sai Số'
    };
    return map[cat] || cat;
  }
}
