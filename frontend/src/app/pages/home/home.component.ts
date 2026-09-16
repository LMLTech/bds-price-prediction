import { Component, OnInit, AfterViewInit, OnDestroy, ElementRef, Renderer2, NgZone } from '@angular/core';
import { RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';

interface StatItem {
  label: string;
  value: number;
  decimals: number;
  prefix?: string;
  suffix?: string;
}

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `
    <div class="home-wrapper">
      <!-- CURSOR SPOTLIGHT (theo chuột, giống hiệu ứng ánh sáng động trong trang mẫu) -->
      <div class="cursor-glow" #cursorGlow></div>

      <!-- ULTRA DYNAMIC PARALLAX SLIDESHOW BACKGROUND -->
      <div class="parallax-bg-wrapper">
        <div class="bg-slide slide-1"></div>
        <div class="bg-slide slide-2"></div>
        <div class="bg-slide slide-3"></div>
        <div class="bg-slide slide-4"></div>
      </div>
      <div class="bg-overlay"></div>

      <!-- DYNAMIC PARTICLES AND LIGHT FLARES -->
      <div class="light-flares">
        <div class="flare f-1"></div>
        <div class="flare f-2"></div>
        <div class="flare f-3"></div>
      </div>

      <!-- MAIN SCROLLABLE CONTENT -->
      <div class="page-container">

        <!-- HERO SECTION WITH LIVE 3D TILT (mousemove) -->
        <section class="hero-section reveal" #heroSection>
          <div class="hero-content tilt-effect" #tiltCard>
            <div class="hero-badge pulse-glow">
              <span class="dot-indicator"></span>
              Nền Tảng AI Tiên Phong 2026
            </div>
            <h1 class="hero-title glitch-text" data-text="Real Estate">Real Estate<br><span class="highlight">Price Prediction</span></h1>
            <p class="hero-subtitle">
              Ứng dụng <strong>Multiple Linear Regression</strong> trên 69.000+ dữ liệu không gian, dự báo giá trị bất động sản siêu chính xác theo thời gian thực.
            </p>
            <div class="hero-actions">
              <a routerLink="/predict" class="btn btn-primary glass-btn magnetic-btn" #magnetBtn>
                <i class="icon">🚀</i> Bắt Đầu Dự Báo Ngay
              </a>
              <a routerLink="/visualization" class="btn btn-secondary glass-btn magnetic-btn" #magnetBtn>
                <i class="icon">✨</i> Khám Phá Biểu Đồ
              </a>
            </div>
          </div>
        </section>

        <!-- FLOATING STATS BAR — SỐ ĐẾM CHẠY LÊN KHI CUỘN TỚI -->
        <section class="stats-bar glass-panel reveal" #statsBar>
          <ng-container *ngFor="let stat of stats; let i = index; let last = last">
            <div class="stat-item">
              <div class="stat-value" #counterEl [attr.data-index]="i">{{ formatStat(0, stat) }}</div>
              <div class="stat-label">{{ stat.label }}</div>
            </div>
            <div class="stat-divider" *ngIf="!last"></div>
          </ng-container>
        </section>

        <!-- TECH STACK MARQUEE (dải chạy vô hạn, thay cho logo carousel của bản mẫu) -->
        <section class="tech-ticker-section reveal">
          <div class="ticker-wrapper">
            <div class="ticker-track">
              <span class="ticker-chip" *ngFor="let tech of techStackLoop">{{ tech }}</span>
            </div>
          </div>
        </section>

        <!-- EXTENDED REAL ESTATE GALLERY (Parallax grid) -->
        <section class="gallery-showcase reveal">
          <h2 class="section-title text-center">Phân Khúc Bất Động Sản Nổi Bật</h2>
          <p class="section-desc text-center">Thuật toán xử lý hiệu quả đa dạng loại hình kiến trúc tại Việt Nam</p>

          <div class="bento-grid">
            <div class="bento-card large-card hover-zoom tilt-card" #tiltCardEl>
              <img src="https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?q=80&w=1200&auto=format&fit=crop" class="bento-img">
              <div class="bento-overlay">
                <h3>Biệt Thự Độc Bản</h3>
                <p>Nội suy giá trị trên không gian rộng</p>
              </div>
            </div>

            <div class="bento-card medium-card hover-zoom tilt-card" #tiltCardEl>
              <img src="https://images.unsplash.com/photo-1512917774080-9991f1c4c750?q=80&w=800&auto=format&fit=crop" class="bento-img">
              <div class="bento-overlay">
                <h3>Nhà Phố Thương Mại</h3>
                <p>Phân tích khoảng cách khu trung tâm</p>
              </div>
            </div>

            <div class="bento-card medium-card hover-zoom tilt-card" #tiltCardEl>
              <img src="https://images.unsplash.com/photo-1564013799919-ab600027ffc6?q=80&w=800&auto=format&fit=crop" class="bento-img">
              <div class="bento-overlay">
                <h3>Căn Hộ Hạng Sang</h3>
                <p>Tính toán hệ số không gian tiện ích</p>
              </div>
            </div>
          </div>
        </section>

        <!-- DYNAMIC PIPELINE STEPS -->
        <section class="dynamic-pipeline glass-panel reveal">
          <div class="pipeline-content">
            <h2 class="section-title text-center">Workflow Xử Lý Dữ Liệu</h2>
            <div class="steps-container">
              <div class="step-item" *ngFor="let step of pipelineSteps; let i = index">
                <div class="step-icon glow-orb">{{ step.icon }}</div>
                <div class="step-details">
                  <h4>{{ step.title }}</h4>
                  <p>{{ step.desc }}</p>
                </div>
                <div class="step-connector" *ngIf="i < pipelineSteps.length - 1"></div>
              </div>
            </div>
          </div>
        </section>
      </div>

      <!-- FLOATING QUICK-ACTION BUTTON (giống nút "AI Summary" nổi ở trang mẫu) -->
      <button class="floating-action-btn" [class.visible]="showFab" (click)="scrollToTop()" aria-label="Về đầu trang">
        <svg viewBox="0 0 24 24" width="20" height="20" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M12 19V5M12 5L6 11M12 5L18 11" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <span>Lên đầu trang</span>
      </button>
    </div>
  `,
  styles: [`
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Outfit:wght@300;400;600;800&display=swap');

    :host {
      display: block;
      font-family: 'Outfit', sans-serif;
      min-height: 100vh;
      position: relative;
    }

    .home-wrapper {
      position: relative;
      min-height: 100vh;
      overflow-x: hidden;
      color: #fff;
      background-color: #020617; /* Fallback dark */
    }

    /* CURSOR SPOTLIGHT */
    .cursor-glow {
      position: fixed;
      top: 0; left: 0;
      width: 500px; height: 500px;
      border-radius: 50%;
      pointer-events: none;
      z-index: 5;
      background: radial-gradient(circle, rgba(56,189,248,0.10) 0%, rgba(139,92,246,0.06) 40%, transparent 70%);
      transform: translate(-50%, -50%);
      opacity: 0;
      transition: opacity 0.4s ease;
      will-change: transform;
    }
    .cursor-glow.active { opacity: 1; }

    /* ULTRA DYNAMIC BACKGROUND SLIDESHOW */
    .parallax-bg-wrapper {
      position: fixed;
      top: -5%; left: -5%;
      width: 110vw; height: 110vh;
      z-index: -4;
      pointer-events: none;
    }

    .bg-slide {
      position: absolute;
      top: 0; left: 0; width: 100%; height: 100%;
      background-size: cover;
      background-position: center;
      opacity: 0;
      animation: ultraKenBurns 32s infinite ease-in-out;
    }

    .slide-1 { background-image: url('https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?q=80&w=2500&auto=format&fit=crop'); animation-delay: 0s; }
    .slide-2 { background-image: url('https://images.unsplash.com/photo-1613490908592-fd5e16f08e5a?q=80&w=2500&auto=format&fit=crop'); animation-delay: 8s; }
    .slide-3 { background-image: url('https://images.unsplash.com/photo-1512917774080-9991f1c4c750?q=80&w=2500&auto=format&fit=crop'); animation-delay: 16s; }
    .slide-4 { background-image: url('https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?q=80&w=2500&auto=format&fit=crop'); animation-delay: 24s; }

    @keyframes ultraKenBurns {
      0% { opacity: 0; transform: scale(1.05) translate(0, 0) rotate(0deg); }
      10% { opacity: 1; transform: scale(1.05) translate(0, 0) rotate(0deg); }
      25% { opacity: 1; }
      35% { opacity: 0; transform: scale(1.15) translate(-20px, -15px) rotate(1deg); }
      100% { opacity: 0; transform: scale(1.15) translate(-20px, -15px) rotate(1deg); }
    }

    .bg-overlay {
      position: fixed;
      top: 0; left: 0; width: 100vw; height: 100vh;
      background: radial-gradient(circle at center, rgba(15,23,42,0.6) 0%, rgba(2,6,23,0.95) 100%);
      z-index: -3;
    }

    /* DYNAMIC LIGHT FLARES */
    .light-flares { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: -2; overflow: hidden; pointer-events: none; }
    .flare { position: absolute; border-radius: 50%; filter: blur(80px); animation: drift 20s infinite alternate ease-in-out; }
    .f-1 { width: 400px; height: 400px; background: rgba(59, 130, 246, 0.2); top: -10%; left: -10%; }
    .f-2 { width: 500px; height: 500px; background: rgba(139, 92, 246, 0.15); bottom: -20%; right: -10%; animation-delay: -5s; }
    .f-3 { width: 300px; height: 300px; background: rgba(56, 189, 248, 0.1); top: 40%; left: 40%; animation-delay: -10s; }

    @keyframes drift {
      0% { transform: translate(0, 0) scale(1); }
      100% { transform: translate(100px, 150px) scale(1.2); }
    }

    .page-container {
      max-width: 1400px;
      margin: 0 auto;
      padding: 6rem 2rem 4rem 2rem;
      position: relative;
      z-index: 1;
    }

    /* SCROLL-REVEAL: ẩn mặc định, JS thêm class .in-view khi cuộn tới */
    .reveal {
      opacity: 0;
      transform: translateY(60px);
      filter: blur(10px);
      transition: opacity 1s cubic-bezier(0.19, 1, 0.22, 1), transform 1s cubic-bezier(0.19, 1, 0.22, 1), filter 1s cubic-bezier(0.19, 1, 0.22, 1);
    }
    .reveal.in-view {
      opacity: 1;
      transform: translateY(0);
      filter: blur(0);
    }

    @keyframes pulse-dot { 0% { transform: scale(1); opacity: 1; } 100% { transform: scale(2); opacity: 0; } }

    /* GLASSMORPHISM UTILS */
    .glass-btn { background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.2); box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3); }
    .glass-panel { background: rgba(15, 23, 42, 0.4); backdrop-filter: blur(25px); -webkit-backdrop-filter: blur(25px); border: 1px solid rgba(255, 255, 255, 0.1); border-top: 1px solid rgba(255, 255, 255, 0.2); border-left: 1px solid rgba(255, 255, 255, 0.2); border-radius: 24px; box-shadow: 0 30px 60px rgba(0, 0, 0, 0.5); }

    /* HERO SECTION — hỗ trợ tilt 3D theo chuột */
    .hero-section { text-align: center; padding: 4rem 0 6rem 0; perspective: 1200px; }
    .hero-content { transform-style: preserve-3d; transition: transform 0.15s ease-out; will-change: transform; }

    .hero-badge { display: inline-flex; align-items: center; gap: 8px; background: rgba(14, 165, 233, 0.15); color: #7dd3fc; border: 1px solid rgba(14, 165, 233, 0.4); padding: 0.6rem 1.8rem; border-radius: 99px; font-size: 0.95rem; font-family: 'Space Grotesk', sans-serif; letter-spacing: 2px; margin-bottom: 2rem; }
    .dot-indicator { width: 8px; height: 8px; background: #38bdf8; border-radius: 50%; box-shadow: 0 0 10px #38bdf8; animation: pulse-dot 1.5s infinite; }

    .hero-title { font-size: 5.5rem; font-weight: 800; line-height: 1.05; margin: 0 0 2rem 0; text-transform: uppercase; letter-spacing: -2px; color: #fff; }
    .hero-title .highlight { background: linear-gradient(135deg, #38bdf8, #818cf8, #c084fc); -webkit-background-clip: text; -webkit-text-fill-color: transparent; display: block; font-size: 6rem; filter: drop-shadow(0 10px 20px rgba(139, 92, 246, 0.3)); }
    .hero-subtitle { font-size: 1.4rem; color: #cbd5e1; max-width: 850px; margin: 0 auto 3.5rem auto; line-height: 1.8; font-weight: 300; font-family: 'Space Grotesk', sans-serif; }
    .hero-actions { display: flex; justify-content: center; gap: 2rem; }

    /* MAGNETIC BUTTON — JS dịch chuyển theo con trỏ trong khu vực nút */
    .btn { padding: 1.3rem 2.8rem; border-radius: 100px; font-weight: 600; font-size: 1.15rem; text-decoration: none; transition: transform 0.25s cubic-bezier(0.25, 1, 0.5, 1), box-shadow 0.3s ease, background 0.3s ease; display: inline-flex; align-items: center; gap: 12px; position: relative; overflow: hidden; will-change: transform; }
    .btn::before { content: ''; position: absolute; top: 0; left: -100%; width: 50%; height: 100%; background: linear-gradient(to right, transparent, rgba(255,255,255,0.2), transparent); transform: skewX(-25deg); transition: 0.6s; }
    .btn:hover::before { left: 150%; }

    .btn-primary { background: linear-gradient(135deg, #2563eb, #7c3aed); color: #fff; border: none; box-shadow: 0 15px 35px rgba(124, 58, 237, 0.4); }
    .btn-primary:hover { box-shadow: 0 20px 45px rgba(124, 58, 237, 0.6); }
    .btn-secondary { background: rgba(255,255,255,0.03); color: #fff; }
    .btn-secondary:hover { background: rgba(255,255,255,0.1); box-shadow: 0 15px 35px rgba(0,0,0,0.4); }

    /* FLOATING STATS BAR */
    .stats-bar { display: flex; justify-content: space-around; align-items: center; padding: 2.5rem; margin-bottom: 4rem; border-radius: 100px; }
    .stat-item { text-align: center; flex: 1; }
    .stat-divider { width: 1px; height: 60px; background: linear-gradient(to bottom, transparent, rgba(255,255,255,0.2), transparent); }
    .stat-value { font-size: 3rem; font-weight: 800; font-family: 'Space Grotesk', sans-serif; background: linear-gradient(to bottom, #fff, #94a3b8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.5rem; font-variant-numeric: tabular-nums; }
    .stat-label { font-size: 1rem; color: #94a3b8; font-weight: 500; text-transform: uppercase; letter-spacing: 1px; }

    /* TECH STACK MARQUEE — dải chạy vô hạn */
    .tech-ticker-section { margin-bottom: 5rem; }
    .ticker-wrapper {
      overflow: hidden;
      border-radius: 100px;
      border: 1px solid rgba(255,255,255,0.08);
      background: rgba(15,23,42,0.35);
      -webkit-mask-image: linear-gradient(90deg, transparent, #000 8%, #000 92%, transparent);
      mask-image: linear-gradient(90deg, transparent, #000 8%, #000 92%, transparent);
    }
    .ticker-track {
      display: flex;
      gap: 1rem;
      width: max-content;
      padding: 1.2rem 1rem;
      animation: tickerScroll 26s linear infinite;
    }
    .ticker-wrapper:hover .ticker-track { animation-play-state: paused; }
    .ticker-chip {
      flex-shrink: 0;
      padding: 0.6rem 1.5rem;
      border-radius: 100px;
      background: rgba(56, 189, 248, 0.08);
      border: 1px solid rgba(56, 189, 248, 0.25);
      color: #7dd3fc;
      font-family: 'Space Grotesk', sans-serif;
      font-size: 0.95rem;
      letter-spacing: 0.5px;
      white-space: nowrap;
    }
    @keyframes tickerScroll {
      0% { transform: translateX(0); }
      100% { transform: translateX(-50%); }
    }

    /* BENTO GRID */
    .section-title { font-size: 2.8rem; font-weight: 800; margin-bottom: 1rem; }
    .section-desc { font-size: 1.2rem; color: #94a3b8; margin-bottom: 4rem; }
    .text-center { text-align: center; }

    .bento-grid { display: grid; grid-template-columns: repeat(3, 1fr); grid-template-rows: 350px 350px; gap: 1.5rem; margin-bottom: 7rem; }
    .bento-card { position: relative; border-radius: 24px; overflow: hidden; border: 1px solid rgba(255,255,255,0.1); cursor: pointer; transition: transform 0.2s ease-out; will-change: transform; }
    .large-card { grid-column: span 2; grid-row: span 2; }
    .medium-card { grid-column: span 1; grid-row: span 1; }

    .bento-img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.9s cubic-bezier(0.25, 1, 0.5, 1); filter: brightness(0.8); }
    .bento-card:hover .bento-img { transform: scale(1.08); filter: brightness(1); }

    .bento-overlay { position: absolute; bottom: 0; left: 0; width: 100%; background: linear-gradient(to top, rgba(2,6,23,0.95), transparent); padding: 3rem 2rem 2rem 2rem; transition: all 0.4s ease; }
    .bento-overlay h3 { font-size: 1.8rem; margin: 0 0 0.5rem 0; font-weight: 700; transform: translateY(10px); transition: 0.4s; }
    .bento-overlay p { font-size: 1.05rem; color: #cbd5e1; margin: 0; opacity: 0.8; transform: translateY(10px); transition: 0.4s; transition-delay: 0.1s; }
    .bento-card:hover .bento-overlay h3, .bento-card:hover .bento-overlay p { transform: translateY(0); opacity: 1; }

    /* DYNAMIC PIPELINE */
    .dynamic-pipeline { padding: 4rem 5rem; margin-bottom: 5rem; }
    .steps-container { display: flex; align-items: flex-start; justify-content: space-between; margin-top: 4rem; }
    .step-item { display: flex; flex-direction: column; align-items: center; text-align: center; flex: 1; position: relative; z-index: 2; }
    .step-icon { width: 70px; height: 70px; border-radius: 50%; background: rgba(15,23,42,0.8); border: 2px solid #38bdf8; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; font-weight: 800; font-family: 'Space Grotesk'; margin-bottom: 1.5rem; box-shadow: 0 0 30px rgba(56, 189, 248, 0.4); transition: 0.4s; }
    .step-item:hover .step-icon { transform: scale(1.15) rotate(5deg); background: #38bdf8; color: #000; box-shadow: 0 0 50px rgba(56, 189, 248, 0.8); }
    .step-details h4 { font-size: 1.3rem; margin: 0 0 0.5rem 0; color: #fff; }
    .step-details p { font-size: 1rem; color: #94a3b8; line-height: 1.6; max-width: 200px; margin: 0 auto; }
    .step-connector { flex: 1; height: 2px; background: linear-gradient(90deg, #38bdf8 0%, rgba(56,189,248,0.2) 100%); margin-top: 35px; z-index: 1; opacity: 0.5; border-radius: 10px; }

    /* FLOATING ACTION BUTTON */
    .floating-action-btn {
      position: fixed;
      right: 2rem;
      bottom: 2rem;
      z-index: 50;
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 0.9rem 1.4rem;
      border-radius: 100px;
      background: linear-gradient(135deg, #2563eb, #7c3aed);
      color: #fff;
      border: none;
      cursor: pointer;
      font-family: 'Space Grotesk', sans-serif;
      font-weight: 600;
      font-size: 0.9rem;
      box-shadow: 0 15px 35px rgba(124, 58, 237, 0.45);
      opacity: 0;
      transform: translateY(20px) scale(0.9);
      pointer-events: none;
      transition: opacity 0.3s ease, transform 0.3s ease, box-shadow 0.3s ease;
    }
    .floating-action-btn.visible { opacity: 1; transform: translateY(0) scale(1); pointer-events: auto; }
    .floating-action-btn:hover { box-shadow: 0 20px 45px rgba(124, 58, 237, 0.65); transform: translateY(-3px) scale(1.02); }

    @media (max-width: 1024px) {
      .hero-title { font-size: 4rem; } .hero-title .highlight { font-size: 4.5rem; }
      .bento-grid { grid-template-columns: 1fr; grid-template-rows: auto; }
      .large-card, .medium-card { grid-column: span 1; height: 350px; }
      .stats-bar { flex-direction: column; gap: 2rem; border-radius: 24px; }
      .stat-divider { width: 60px; height: 1px; }
      .steps-container { flex-direction: column; gap: 3rem; }
      .step-connector { display: none; }
      .step-item { flex-direction: row; text-align: left; gap: 2rem; width: 100%; }
      .step-details p { max-width: 100%; }
      .floating-action-btn span { display: none; }
      .cursor-glow { display: none; }
    }
  `]
})
export class HomeComponent implements OnInit, AfterViewInit, OnDestroy {

  // ===== DỮ LIỆU (giữ nguyên logic/số liệu gốc) =====
  stats: StatItem[] = [
    { label: 'Hệ số R² (Độ giải thích)', value: 0.3729, decimals: 4 },
    { label: 'MAE (Triệu VNĐ)', value: 8417.93, decimals: 2 },
    { label: 'RMSE (Sai số bình phương)', value: 21435.74, decimals: 2 },
    { label: 'Dữ liệu Test', value: 9172, decimals: 0 },
  ];

  pipelineSteps = [
    { icon: '01', title: 'Cào Dữ Liệu (Crawling)', desc: 'Hàng vạn tin đăng được trích xuất.' },
    { icon: '02', title: 'Làm Sạch (Cleaning)', desc: 'Loại bỏ nhiễu và xử lý Missing Values.' },
    { icon: '03', title: 'Máy Học (Modeling)', desc: 'Linear Regression 280 tính năng.' },
    { icon: '04', title: 'Triển Khai (Deploy)', desc: 'API FastAPI và giao diện Web Angular.' },
  ];

  techStack = ['FastAPI', 'Angular', 'Scikit-learn', 'Pandas', 'NumPy', 'Multiple Linear Regression', 'Docker', 'PostgreSQL'];
  techStackLoop: string[] = [...this.techStack, ...this.techStack]; // nhân đôi để cuộn vô hạn liền mạch

  showFab = false;

  private observer?: IntersectionObserver;
  private statsCounted = false;
  private mouseMoveHandler?: (e: MouseEvent) => void;
  private scrollHandler?: () => void;
  private magnetHandlers: Array<{ el: HTMLElement; move: (e: MouseEvent) => void; leave: () => void }> = [];

  constructor(private el: ElementRef, private renderer: Renderer2, private zone: NgZone) {}

  ngOnInit(): void {}

  ngAfterViewInit(): void {
    this.zone.runOutsideAngular(() => {
      this.setupScrollReveal();
      this.setupCounters();
      this.setupCursorGlow();
      this.setupTilt();
      this.setupMagneticButtons();
      this.setupFabVisibility();
    });
  }

  ngOnDestroy(): void {
    this.observer?.disconnect();
    if (this.mouseMoveHandler) window.removeEventListener('mousemove', this.mouseMoveHandler);
    if (this.scrollHandler) window.removeEventListener('scroll', this.scrollHandler);
    this.magnetHandlers.forEach(({ el, move, leave }) => {
      el.removeEventListener('mousemove', move);
      el.removeEventListener('mouseleave', leave);
    });
  }

  scrollToTop(): void {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  formatStat(value: number, stat: StatItem): string {
    return value.toLocaleString('en-US', {
      minimumFractionDigits: stat.decimals,
      maximumFractionDigits: stat.decimals,
    });
  }

  /** Scroll-reveal: các phần tử .reveal chỉ hiện khi cuộn tới gần viewport */
  private setupScrollReveal(): void {
    const targets = this.el.nativeElement.querySelectorAll('.reveal');
    this.observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('in-view');

            if (entry.target.classList.contains('stats-bar') && !this.statsCounted) {
              this.statsCounted = true;
              this.animateCounters();
            }
            this.observer?.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.2, rootMargin: '0px 0px -50px 0px' }
    );
    targets.forEach((t: Element) => this.observer!.observe(t));
  }

  /** Chuẩn bị (không tự chạy ở đây, chờ IntersectionObserver kích hoạt qua stats-bar) */
  private setupCounters(): void {}

  /** Đếm số chạy từ 0 lên giá trị thật bằng requestAnimationFrame */
  private animateCounters(): void {
    const counterEls: NodeListOf<HTMLElement> = this.el.nativeElement.querySelectorAll('.stat-value');
    const duration = 1800;

    counterEls.forEach((elRef) => {
      const idx = Number(elRef.getAttribute('data-index'));
      const stat = this.stats[idx];
      if (!stat) return;

      const start = performance.now();
      const target = stat.value;

      const tick = (now: number) => {
        const progress = Math.min((now - start) / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
        const current = target * eased;
        elRef.textContent = this.formatStat(current, stat);
        if (progress < 1) {
          requestAnimationFrame(tick);
        } else {
          elRef.textContent = this.formatStat(target, stat);
        }
      };
      requestAnimationFrame(tick);
    });
  }

  /** Ánh sáng theo con trỏ chuột trên toàn trang */
  private setupCursorGlow(): void {
    const glow: HTMLElement | null = this.el.nativeElement.querySelector('.cursor-glow');
    if (!glow) return;

    this.mouseMoveHandler = (e: MouseEvent) => {
      glow.classList.add('active');
      glow.style.transform = `translate(${e.clientX}px, ${e.clientY}px) translate(-50%, -50%)`;
    };
    window.addEventListener('mousemove', this.mouseMoveHandler, { passive: true });
  }

  /** Tilt 3D cho khối hero theo vị trí con trỏ */
  private setupTilt(): void {
    const card: HTMLElement | null = this.el.nativeElement.querySelector('.tilt-effect');
    const heroSection: HTMLElement | null = this.el.nativeElement.querySelector('.hero-section');
    if (!card || !heroSection) return;

    heroSection.addEventListener('mousemove', (e: MouseEvent) => {
      const rect = heroSection.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      const rotateX = ((y - rect.height / 2) / rect.height) * -8;
      const rotateY = ((x - rect.width / 2) / rect.width) * 8;
      card.style.transform = `rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
    });
    heroSection.addEventListener('mouseleave', () => {
      card.style.transform = 'rotateX(0deg) rotateY(0deg)';
    });

    // Tilt nhẹ cho các bento card
    const tiltCards: NodeListOf<HTMLElement> = this.el.nativeElement.querySelectorAll('.tilt-card');
    tiltCards.forEach((tc) => {
      tc.addEventListener('mousemove', (e: MouseEvent) => {
        const rect = tc.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        const rotateX = ((y - rect.height / 2) / rect.height) * -6;
        const rotateY = ((x - rect.width / 2) / rect.width) * 6;
        tc.style.transform = `perspective(800px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(1.01)`;
      });
      tc.addEventListener('mouseleave', () => {
        tc.style.transform = 'perspective(800px) rotateX(0deg) rotateY(0deg) scale(1)';
      });
    });
  }

  /** Nút "hút chuột" — dịch chuyển nhẹ theo vị trí con trỏ trong phạm vi nút */
  private setupMagneticButtons(): void {
    const buttons: NodeListOf<HTMLElement> = this.el.nativeElement.querySelectorAll('.magnetic-btn');
    buttons.forEach((btn) => {
      const move = (e: MouseEvent) => {
        const rect = btn.getBoundingClientRect();
        const x = e.clientX - rect.left - rect.width / 2;
        const y = e.clientY - rect.top - rect.height / 2;
        btn.style.transform = `translate(${x * 0.25}px, ${y * 0.25}px)`;
      };
      const leave = () => {
        btn.style.transform = 'translate(0, 0)';
      };
      btn.addEventListener('mousemove', move);
      btn.addEventListener('mouseleave', leave);
      this.magnetHandlers.push({ el: btn, move, leave });
    });
  }

  /** Hiện nút "Lên đầu trang" sau khi cuộn quá một ngưỡng */
  private setupFabVisibility(): void {
    this.scrollHandler = () => {
      const shouldShow = window.scrollY > 600;
      this.zone.run(() => {
        this.showFab = shouldShow;
      });
    };
    window.addEventListener('scroll', this.scrollHandler, { passive: true });
  }
}