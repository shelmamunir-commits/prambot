/* ============================================
   Prambot — App JS v2.0
   Interaksi halaman yang elegan & animatif
   ============================================ */

document.addEventListener('DOMContentLoaded', () => {

  // ============ SIDEBAR TOGGLE (MOBILE) ============
  const toggle    = document.getElementById('sidebarToggle');
  const sidebar   = document.getElementById('sidebar');
  const overlay   = document.getElementById('sidebarOverlay');
  const mainEl    = document.getElementById('mainContent');

  function openSidebar() {
    sidebar?.classList.add('open');
    if (overlay) { overlay.style.display = 'block'; requestAnimationFrame(() => { overlay.style.opacity = '1'; }); }
  }

  function closeSidebar() {
    sidebar?.classList.remove('open');
    if (overlay) { overlay.style.opacity = '0'; setTimeout(() => { overlay.style.display = 'none'; }, 300); }
  }

  if (overlay) { overlay.style.transition = 'opacity 0.3s ease'; overlay.style.opacity = '0'; }

  toggle?.addEventListener('click', (e) => {
    e.stopPropagation();
    sidebar?.classList.contains('open') ? closeSidebar() : openSidebar();
  });

  overlay?.addEventListener('click', closeSidebar);

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeSidebar();
  });

  // ============ BACK TO TOP ============
  const backToTop = document.getElementById('backToTop');
  if (backToTop) {
    window.addEventListener('scroll', () => {
      backToTop.classList.toggle('show', window.scrollY > 300);
    }, { passive: true });

    backToTop.addEventListener('click', (e) => {
      e.preventDefault();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // ============ FLASH MESSAGE AUTO-DISMISS ============
  document.querySelectorAll('.alert').forEach((alert) => {
    setTimeout(() => {
      alert.style.transition = 'all 0.5s ease';
      alert.style.opacity = '0';
      alert.style.transform = 'translateY(-8px)';
      setTimeout(() => alert.remove(), 500);
    }, 5000);
  });

  // ============ DATE INPUT MAX = TODAY ============
  const today = new Date().toISOString().split('T')[0];
  document.querySelectorAll('input[type="date"]').forEach((input) => {
    if (!input.id.includes('acara')) {
      input.max = today;
    }
  });

  // ============ STAGGERED CARD ANIMATIONS ============
  const animCards = document.querySelectorAll('.card, .stat-card, .result-item');
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry, i) => {
      if (entry.isIntersecting) {
        setTimeout(() => {
          entry.target.style.opacity = '1';
          entry.target.style.transform = 'translateY(0)';
        }, 60 * i);
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  animCards.forEach((card, i) => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(16px)';
    card.style.transition = 'all 0.5s cubic-bezier(0.4, 0, 0.2, 1)';
    observer.observe(card);
  });

  // ============ RESULT CARD ANIMATE IN ============
  const resultCards = document.querySelectorAll('.result-card');
  resultCards.forEach((card) => {
    card.style.animation = 'scaleIn 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) both';
  });

  // ============ BUTTON RIPPLE EFFECT ============
  document.querySelectorAll('.btn').forEach((btn) => {
    btn.addEventListener('click', function(e) {
      const rect = this.getBoundingClientRect();
      const ripple = document.createElement('span');
      const size = Math.max(rect.width, rect.height);
      const x = e.clientX - rect.left - size / 2;
      const y = e.clientY - rect.top - size / 2;

      ripple.style.cssText = `
        position: absolute;
        width: ${size}px;
        height: ${size}px;
        left: ${x}px;
        top: ${y}px;
        background: rgba(255,255,255,0.25);
        border-radius: 50%;
        transform: scale(0);
        animation: rippleEffect 0.5s ease-out forwards;
        pointer-events: none;
        z-index: 100;
      `;

      this.style.position = 'relative';
      this.style.overflow = 'hidden';
      this.appendChild(ripple);
      setTimeout(() => ripple.remove(), 500);
    });
  });

  // ============ FORM VALIDATION ============
  document.querySelectorAll('form[method="POST"]').forEach((form) => {
    form.addEventListener('submit', (e) => {
      let valid = true;
      const namaInputs = form.querySelectorAll('input[name="nama"], input[name="nama_a"], input[name="nama_b"]');
      const namaRegex = /^[A-Za-z\u00C0-\u017E][A-Za-z\u00C0-\u017E .'\\-]*$/;

      namaInputs.forEach((input) => {
        const val = input.value.trim();
        if (!val || !namaRegex.test(val) || val.length > 60) {
          e.preventDefault();
          valid = false;
          input.style.borderColor = '#A53428';
          input.style.boxShadow = '0 0 0 4px rgba(165, 52, 40, 0.1)';
          input.focus();

          // Shake animation
          input.style.animation = 'shakeInput 0.4s ease';
          setTimeout(() => {
            input.style.animation = '';
            input.style.borderColor = '';
            input.style.boxShadow = '';
          }, 1500);
        } else {
          input.style.borderColor = '';
          input.style.boxShadow = '';
        }
      });

      if (!valid) {
        showToast('⚠️ Harap perbaiki input nama sebelum melanjutkan.', 'error');
      }
    });
  });

  // ============ TOAST NOTIFICATION ============
  function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    const bgColor = type === 'error' ? 'rgba(165,52,40,0.95)' : 'rgba(93,58,26,0.95)';

    toast.style.cssText = `
      position: fixed;
      bottom: 2rem;
      left: 50%;
      transform: translateX(-50%) translateY(20px);
      background: ${bgColor};
      color: white;
      padding: 0.85rem 1.5rem;
      border-radius: 100px;
      font-size: 0.875rem;
      font-weight: 500;
      z-index: 9999;
      box-shadow: 0 8px 32px rgba(0,0,0,0.25);
      opacity: 0;
      transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
      backdrop-filter: blur(10px);
      border: 1px solid rgba(255,255,255,0.1);
      white-space: nowrap;
    `;
    toast.textContent = message;
    document.body.appendChild(toast);

    requestAnimationFrame(() => {
      toast.style.opacity = '1';
      toast.style.transform = 'translateX(-50%) translateY(0)';
    });

    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateX(-50%) translateY(10px)';
      setTimeout(() => toast.remove(), 300);
    }, 3500);
  }

  // ============ ACTIVE NAV HIGHLIGHT ============
  const currentPath = window.location.pathname;
  document.querySelectorAll('.sidebar-nav a').forEach((link) => {
    const href = link.getAttribute('href');
    if (href && currentPath.startsWith(href) && href !== '/') {
      link.classList.add('active');
    }
  });

  // ============ CONFIRM DIALOGS ============
  document.querySelectorAll('[data-confirm]').forEach((link) => {
    link.addEventListener('click', (e) => {
      if (!confirm(link.dataset.confirm)) e.preventDefault();
    });
  });

  // ============ NUMBER COUNTER ANIMATION ============
  document.querySelectorAll('.stat-card .value, .neptu-big').forEach((el) => {
    const target = parseInt(el.textContent);
    if (isNaN(target)) return;

    let start = 0;
    const duration = 800;
    const startTime = performance.now();

    const updateCount = (currentTime) => {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const easeOut = 1 - Math.pow(1 - progress, 3);
      el.textContent = Math.round(start + (target - start) * easeOut);
      if (progress < 1) requestAnimationFrame(updateCount);
    };

    requestAnimationFrame(updateCount);
  });

  // ============ TABLE ROW HOVER ENHANCEMENT ============
  document.querySelectorAll('tbody tr').forEach((row, i) => {
    row.style.animationDelay = `${i * 0.03}s`;
    row.style.animation = 'fadeInUp 0.3s ease both';
  });

});

// ============ CSS KEYFRAMES (injected) ============
const style = document.createElement('style');
style.textContent = `
  @keyframes rippleEffect {
    to { transform: scale(2.5); opacity: 0; }
  }
  @keyframes shakeInput {
    0%, 100% { transform: translateX(0); }
    20%       { transform: translateX(-6px); }
    40%       { transform: translateX(6px); }
    60%       { transform: translateX(-4px); }
    80%       { transform: translateX(4px); }
  }
  @keyframes scaleIn {
    from { opacity: 0; transform: scale(0.95); }
    to   { opacity: 1; transform: scale(1); }
  }
  @keyframes fadeInUp {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
  }
  @keyframes fadeInDown {
    from { opacity: 0; transform: translateY(-12px); }
    to   { opacity: 1; transform: translateY(0); }
  }
  @keyframes fadeIn {
    from { opacity: 0; }
    to   { opacity: 1; }
  }
`;
document.head.appendChild(style);
