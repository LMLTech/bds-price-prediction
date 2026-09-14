import { Component } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [RouterLink, RouterLinkActive],
  template: `
    <header class="navbar-header">
      <div class="navbar-container">
        <a routerLink="/" class="brand-logo">
          <span class="logo-badge">ML</span>
          <span class="brand-text">BĐS Price Predictor</span>
        </a>
        <nav class="nav-links">
          <a routerLink="/" routerLinkActive="active" [routerLinkActiveOptions]="{exact: true}">Tổng quan</a>
          <a routerLink="/predict" routerLinkActive="active">Dự báo giá</a>
          <a routerLink="/visualization" routerLinkActive="active">Trực quan hóa</a>
          <a routerLink="/model" routerLinkActive="active">Thông tin mô hình</a>
        </nav>
      </div>
    </header>
  `,
  styles: [`
    .navbar-header {
      background: rgba(15, 23, 42, 0.92);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
      position: sticky;
      top: 0;
      z-index: 1000;
    }
    .navbar-container {
      max-width: 1240px;
      margin: 0 auto;
      padding: 0.85rem 1.5rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .brand-logo {
      display: flex;
      align-items: center;
      gap: 0.6rem;
      text-decoration: none;
      color: #f8fafc;
      font-weight: 700;
      font-size: 1.15rem;
      letter-spacing: -0.02em;
    }
    .logo-badge {
      background: linear-gradient(135deg, #3b82f6, #6366f1);
      color: #ffffff;
      padding: 0.25rem 0.55rem;
      border-radius: 6px;
      font-size: 0.75rem;
      font-weight: 800;
    }
    .nav-links {
      display: flex;
      gap: 0.5rem;
    }
    .nav-links a {
      color: #94a3b8;
      text-decoration: none;
      padding: 0.5rem 0.9rem;
      border-radius: 8px;
      font-size: 0.92rem;
      font-weight: 500;
      transition: all 0.2s ease;
    }
    .nav-links a:hover {
      color: #f8fafc;
      background: rgba(255, 255, 255, 0.05);
    }
    .nav-links a.active {
      color: #60a5fa;
      background: rgba(59, 130, 246, 0.12);
      font-weight: 600;
    }
  `]
})
export class NavbarComponent {}
