/* =====================================================
   UNIVERSE.JS — v4 — calmer, smoother, performant
   ===================================================== */

// ─── STARS CANVAS ───────────────────────────────────
function initStars() {
  const canvas = document.getElementById('starsCanvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  let stars = [], W, H;

  function resize() {
    W = canvas.width = window.innerWidth;
    H = canvas.height = window.innerHeight;
    createStars();
  }

  function createStars() {
    stars = [];
    // Fewer stars — quality over quantity
    const count = Math.floor((W * H) / 9000);
    for (let i = 0; i < count; i++) {
      const big = Math.random() > 0.88;
      stars.push({
        x: Math.random() * W,
        y: Math.random() * H,
        r: big ? Math.random() * 1.4 + 0.7 : Math.random() * 0.7 + 0.15,
        alpha: Math.random() * 0.55 + 0.18,
        speed: Math.random() * 0.008 + 0.003,
        offset: Math.random() * Math.PI * 2,
        depth: big ? 0.018 : 0.009,
        color: Math.random() > 0.82 ? 'rgba(232,160,191,' : Math.random() > 0.65 ? 'rgba(179,157,219,' : 'rgba(255,255,255,'
      });
    }
  }

  let mx = 0, my = 0;
  // Throttled mouse — only update every 60ms
  let lastMouse = 0;
  window.addEventListener('mousemove', e => {
    const now = Date.now();
    if (now - lastMouse < 60) return;
    lastMouse = now;
    mx = (e.clientX / W - 0.5) * 16;
    my = (e.clientY / H - 0.5) * 16;
  }, { passive: true });

  let frame = 0;
  function draw() {
    ctx.clearRect(0, 0, W, H);
    frame++;
    stars.forEach(s => {
      const a = s.alpha * (0.72 + 0.28 * Math.sin(frame * s.speed + s.offset));
      ctx.beginPath();
      ctx.arc(s.x + mx * s.depth, s.y + my * s.depth, s.r, 0, Math.PI * 2);
      ctx.fillStyle = `${s.color}${a})`;
      ctx.fill();
    });
    requestAnimationFrame(draw);
  }

  let resizeTimer;
  window.addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(resize, 250);
  });
  resize();
  draw();
}

// ─── FLOATING HEARTS (calmer — fewer, slower) ────────
function initHearts() {
  const container = document.querySelector('.hearts-container');
  if (!container) return;
  const emojis = ['💜', '🌸', '✨'];

  function spawn() {
    const el = document.createElement('div');
    el.className = 'heart';
    el.textContent = emojis[Math.floor(Math.random() * emojis.length)];
    el.style.left = (Math.random() * 88 + 4) + '%';
    el.style.fontSize = (Math.random() * 8 + 9) + 'px';   // smaller
    el.style.opacity = (Math.random() * 0.3 + 0.2).toFixed(2); // subtler
    const dur = Math.random() * 16 + 18;                   // slower
    el.style.animationDuration = dur + 's';
    el.style.animationDelay = (Math.random() * 4) + 's';
    container.appendChild(el);
    setTimeout(() => el.remove(), (dur + 5) * 1000);
  }

  // Only 3 initial hearts instead of 6
  for (let i = 0; i < 3; i++) setTimeout(spawn, i * 2000);
  // Spawn every 5s instead of every 2.2s
  setInterval(spawn, 5000);
}

// ─── PARTICLES (very subtle) ─────────────────────────
function initParticles() {
  const container = document.querySelector('.particles-container');
  if (!container) return;

  function spawn() {
    const el = document.createElement('div');
    el.className = 'particle' + (Math.random() > 0.6 ? ' pink' : '');
    el.style.left = Math.random() * 100 + 'vw';
    el.style.top = Math.random() * 100 + 'vh';
    el.style.setProperty('--dx', (Math.random() - 0.5) * 50 + 'px');
    el.style.setProperty('--dy', (Math.random() - 0.5) * 50 + 'px');
    el.style.animationDuration = (Math.random() * 8 + 7) + 's';
    el.style.animationDelay = Math.random() * 2 + 's';
    container.appendChild(el);
    setTimeout(() => el.remove(), 18000);
  }

  // 6 initial instead of 15
  for (let i = 0; i < 6; i++) setTimeout(spawn, i * 600);
  // Every 2.5s instead of 0.8s
  setInterval(spawn, 2500);
}

// ─── CLOUDS (background drift — very faint) ──────────
function initClouds() {
  const container = document.querySelector('.clouds-container');
  if (!container) return;

  function spawn() {
    const el = document.createElement('div');
    el.className = 'cloud';
    const w = Math.random() * 180 + 100;
    const h = Math.random() * 45 + 18;
    el.style.width = w + 'px';
    el.style.height = h + 'px';
    el.style.top = Math.random() * 65 + '%';
    el.style.opacity = (Math.random() * 0.05 + 0.015).toFixed(3);
    const dur = Math.random() * 70 + 55;
    el.style.animationDuration = dur + 's';
    container.appendChild(el);
    setTimeout(() => el.remove(), (dur + 2) * 1000);
  }

  // Only 2 clouds at a time instead of 4
  for (let i = 0; i < 2; i++) setTimeout(spawn, i * 12000);
  setInterval(spawn, 28000);
}

// ─── SCROLL REVEAL ──────────────────────────────────
function initReveal() {
  const els = document.querySelectorAll('.reveal:not(.visible)');
  if (!els.length) return;
  const obs = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.classList.add('visible');
        obs.unobserve(e.target);
      }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -30px 0px' });
  els.forEach(el => obs.observe(el));
}

// ─── LOADING SCREEN ─────────────────────────────────
function initLoading() {
  const screen = document.getElementById('loadingScreen');
  if (!screen) return;
  window.addEventListener('load', () => {
    setTimeout(() => {
      screen.classList.add('fade-out');
      setTimeout(() => screen.remove(), 900);
    }, 1000);
  });
}

// ─── TRANSITION ─────────────────────────────────────
function navigateTo(url) {
  const overlay = document.getElementById('transitionOverlay');
  if (!overlay) { window.location.href = url; return; }
  overlay.classList.add('active');
  setTimeout(() => { window.location.href = url; }, 650);
}

// ─── BFCACHE (BACK-FORWARD CACHE) HANDLING ──────────
// Reset transition overlay if returning to page via Back/Forward buttons
window.addEventListener('pageshow', (event) => {
  const overlay = document.getElementById('transitionOverlay');
  if (overlay) {
    overlay.classList.remove('active');
  }
});

// ─── INIT ───────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  initStars();
  initHearts();
  initParticles();
  initClouds();
  initReveal();
  initLoading();
});
