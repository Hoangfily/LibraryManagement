/**
 * Dashboard page — summary report with stat cards.
 */
pages.dashboard = {
  async render(container) {
    try {
      const res = await api.getSummary();
      const d = res.data;

      container.innerHTML = `
        <div class="page-header">
          <div>
            <h1>📊 Tổng quan</h1>
            <p class="page-desc">Thống kê tổng hợp hệ thống thư viện</p>
          </div>
        </div>

        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-icon">👥</div>
            <div class="stat-value">${d.total_readers}</div>
            <div class="stat-label">Độc giả</div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">📖</div>
            <div class="stat-value">${d.total_documents}</div>
            <div class="stat-label">Tài liệu</div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">📦</div>
            <div class="stat-value">${d.total_copies}</div>
            <div class="stat-label">Tổng bản sao</div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">📗</div>
            <div class="stat-value">${d.available_copies}</div>
            <div class="stat-label">Bản sẵn sàng</div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">📕</div>
            <div class="stat-value">${d.borrowed_copies}</div>
            <div class="stat-label">Đang mượn</div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">🔄</div>
            <div class="stat-value">${d.total_borrow_orders}</div>
            <div class="stat-label">Phiếu mượn</div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">💰</div>
            <div class="stat-value">${Number(d.total_unpaid_fines).toLocaleString('vi-VN')}đ</div>
            <div class="stat-label">Phạt chưa thu</div>
          </div>
        </div>
      `;
    } catch (err) {
      container.innerHTML = `<p style="color:var(--danger)">Lỗi: ${err.message}</p>`;
    }
  }
};
