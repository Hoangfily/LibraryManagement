/**
 * Fines management page — list + filter.
 */
pages.fines = {
  async render(container) {
    container.innerHTML = `
      <div class="page-header">
        <div>
          <h1>💰 Tiền phạt</h1>
          <p class="page-desc">Theo dõi các khoản phạt trả sách trễ, mất sách</p>
        </div>
      </div>
      <div class="toolbar">
        <select class="filter-select" id="fine-status-filter">
          <option value="">Tất cả</option>
          <option value="unpaid">Chưa thanh toán</option>
          <option value="paid">Đã thanh toán</option>
        </select>
      </div>
      <div id="fines-table"></div>
    `;

    document.getElementById('fine-status-filter').addEventListener('change', () => this.loadTable());
    await this.loadTable();
  },

  async loadTable() {
    const status = document.getElementById('fine-status-filter')?.value || null;
    try {
      const res = await api.getFines(null, status);
      const fines = res.data || [];

      const tbody = fines.length ? fines.map(f => `
        <tr>
          <td>${f.id}</td>
          <td>${f.reader_id}</td>
          <td>${f.borrow_item_id}</td>
          <td><span class="badge badge-warning">${f.fine_type}</span></td>
          <td><strong>${Number(f.amount).toLocaleString('vi-VN')}đ</strong></td>
          <td>${f.reason || '—'}</td>
          <td><span class="badge ${f.status === 'paid' ? 'badge-success' : 'badge-danger'}">${f.status === 'paid' ? '✓ Đã trả' : '✕ Chưa trả'}</span></td>
          <td>${new Date(f.created_at).toLocaleDateString('vi-VN')}</td>
          <td>
            ${f.status === 'unpaid' ? `<button class="btn-icon" title="Đánh dấu đã thanh toán" onclick="pages.fines.payFine(${f.id})">💵</button>` : '—'}
          </td>
        </tr>
      `).join('') : '<tr><td colspan="9" class="table-empty">Không có khoản phạt nào</td></tr>';

      document.getElementById('fines-table').innerHTML = `
        <div class="table-container">
          <table>
            <thead><tr><th>ID</th><th>Reader ID</th><th>Borrow Item</th><th>Loại</th><th>Số tiền</th><th>Lý do</th><th>Trạng thái</th><th>Ngày tạo</th><th>Hành động</th></tr></thead>
            <tbody>${tbody}</tbody>
          </table>
        </div>
      `;
    } catch (err) { showToast(err.message, 'error'); }
  },

  async payFine(id) {
    const ok = await confirmDialog('Xác nhận đã thu tiền phạt này?');
    if (!ok) return;
    try {
      await api.payFine(id);
      showToast('Đã đánh dấu thanh toán!', 'success');
      await this.loadTable();
    } catch (err) { showToast(err.message, 'error'); }
  },
};
