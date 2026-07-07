/**
 * SPA Router and app initialization.
 */

// Pages registry
window.pages = {};

/* ---- Toast notifications ---- */
function showToast(message, type = 'info') {
  const container = document.getElementById('toast-container');
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  const icons = { success: '✓', error: '✕', info: 'ℹ' };
  toast.innerHTML = `<span>${icons[type] || 'ℹ'}</span> <span>${message}</span>`;
  container.appendChild(toast);
  setTimeout(() => toast.remove(), 4000);
}

/* ---- Modal helpers ---- */
function openModal(title, bodyHtml, footerHtml = '') {
  closeModal();
  const overlay = document.createElement('div');
  overlay.className = 'modal-overlay';
  overlay.id = 'modal-overlay';
  overlay.innerHTML = `
    <div class="modal">
      <div class="modal-header">
        <h2>${title}</h2>
        <button class="modal-close" onclick="closeModal()">&times;</button>
      </div>
      <div class="modal-body">${bodyHtml}</div>
      ${footerHtml ? `<div class="modal-footer">${footerHtml}</div>` : ''}
    </div>
  `;
  overlay.addEventListener('click', (e) => {
    if (e.target === overlay) closeModal();
  });
  document.body.appendChild(overlay);
}

function closeModal() {
  const el = document.getElementById('modal-overlay');
  if (el) el.remove();
}

/* ---- Confirm dialog ---- */
function confirmDialog(message) {
  return new Promise((resolve) => {
    const body = `<p class="confirm-text">${message}</p>`;
    const footer = `
      <button class="btn btn-secondary" onclick="closeModal(); window.__confirmResolve(false)">Hủy</button>
      <button class="btn btn-danger" onclick="closeModal(); window.__confirmResolve(true)">Xác nhận</button>
    `;
    window.__confirmResolve = resolve;
    openModal('Xác nhận', body, footer);
  });
}

/* ---- Router ---- */
const routes = {
  '#/login': { page: 'login', title: 'Đăng nhập', requireAuth: false },
  '#/dashboard': { page: 'dashboard', title: 'Tổng quan', requireAuth: true },
  '#/readers': { page: 'readers', title: 'Quản lý Độc giả', requireAuth: true },
  '#/documents': { page: 'documents', title: 'Quản lý Tài liệu', requireAuth: true },
  '#/borrows': { page: 'borrows', title: 'Mượn / Trả sách', requireAuth: true },
  '#/fines': { page: 'fines', title: 'Tiền phạt', requireAuth: true },
  '#/users': { page: 'users', title: 'Quản lý User', requireAuth: true, adminOnly: true },
};

function navigate(hash) {
  window.location.hash = hash;
}

function renderLayout() {
  const user = auth.getUser();
  const isAdmin = auth.isAdmin();

  document.getElementById('app').innerHTML = `
    <div class="app-layout">
      <aside class="sidebar">
        <div class="sidebar-brand">
          <h2>📚 LibManager</h2>
          <span>Library Management System</span>
        </div>
        <nav class="sidebar-nav">
          <div class="nav-section-title">Menu chính</div>
          <div class="nav-item" data-route="#/dashboard">
            <span class="nav-icon">📊</span> Tổng quan
          </div>
          <div class="nav-item" data-route="#/readers">
            <span class="nav-icon">👥</span> Độc giả
          </div>
          <div class="nav-item" data-route="#/documents">
            <span class="nav-icon">📖</span> Tài liệu
          </div>
          <div class="nav-item" data-route="#/borrows">
            <span class="nav-icon">🔄</span> Mượn / Trả
          </div>
          <div class="nav-item" data-route="#/fines">
            <span class="nav-icon">💰</span> Tiền phạt
          </div>
          ${isAdmin ? `
          <div class="nav-section-title">Quản trị</div>
          <div class="nav-item" data-route="#/users">
            <span class="nav-icon">⚙️</span> Quản lý User
          </div>` : ''}
        </nav>
        <div class="sidebar-footer">
          <div style="padding: 8px 16px; color: var(--text-secondary); font-size: 0.85rem; margin-bottom: 8px;">
            👤 ${user ? user.username : ''} <span class="badge badge-info" style="margin-left:4px">${user ? user.role : ''}</span>
          </div>
          <button class="logout-btn" onclick="auth.logout()">
            <span>🚪</span> Đăng xuất
          </button>
        </div>
      </aside>
      <main class="main-content" id="page-content">
        <div class="page-loading"><div class="spinner"></div></div>
      </main>
    </div>
  `;

  // Nav click handlers
  document.querySelectorAll('.nav-item[data-route]').forEach(item => {
    item.addEventListener('click', () => navigate(item.dataset.route));
  });
}

function updateActiveNav() {
  const hash = window.location.hash;
  document.querySelectorAll('.nav-item').forEach(item => {
    item.classList.toggle('active', item.dataset.route === hash);
  });
}

async function handleRoute() {
  const hash = window.location.hash || '#/login';
  const route = routes[hash];

  if (!route) {
    navigate(auth.isLoggedIn() ? '#/dashboard' : '#/login');
    return;
  }

  if (route.requireAuth && !auth.isLoggedIn()) {
    navigate('#/login');
    return;
  }

  if (!route.requireAuth && auth.isLoggedIn() && hash === '#/login') {
    navigate('#/dashboard');
    return;
  }

  if (route.adminOnly && !auth.isAdmin()) {
    navigate('#/dashboard');
    return;
  }

  document.title = `${route.title} — LibManager`;

  if (hash === '#/login') {
    document.getElementById('app').innerHTML = '';
    pages.login.render();
    return;
  }

  // Ensure layout is rendered
  if (!document.querySelector('.app-layout')) {
    renderLayout();
  }

  updateActiveNav();

  const content = document.getElementById('page-content');
  if (content) {
    content.innerHTML = '<div class="page-loading"><div class="spinner"></div></div>';
    try {
      await pages[route.page].render(content);
    } catch (err) {
      content.innerHTML = `<p style="color:var(--danger)">Error: ${err.message}</p>`;
    }
  }
}

// Init
window.addEventListener('DOMContentLoaded', () => {
  window.addEventListener('hashchange', handleRoute);
  handleRoute();
});
