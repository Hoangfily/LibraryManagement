/**
 * Borrows management page — create, list, return, cancel.
 */
pages.borrows = {
  async render(container) {
    container.innerHTML = `
      <div class="page-header">
        <div>
          <h1>🔄 Mượn / Trả sách</h1>
          <p class="page-desc">Quản lý phiếu mượn, trả sách và theo dõi tình trạng</p>
        </div>
        <button class="btn btn-primary" onclick="pages.borrows.showCreateModal()">+ Tạo phiếu mượn</button>
      </div>
      <div class="toolbar">
        <select class="filter-select" id="borrow-status-filter">
          <option value="">Tất cả trạng thái</option>
          <option value="borrowing">Đang mượn</option>
          <option value="returned">Đã trả</option>
          <option value="overdue">Quá hạn</option>
          <option value="cancelled">Đã hủy</option>
        </select>
      </div>
      <div id="borrows-table"></div>
    `;

    document.getElementById('borrow-status-filter').addEventListener('change', () => this.loadTable());
    await this.loadTable();
  },

  async loadTable() {
    const status = document.getElementById('borrow-status-filter')?.value || null;
    try {
      const res = await api.getBorrows(null, status);
      const orders = res.data || [];
      const statusBadge = (s) => {
        const map = { borrowing: 'badge-info', returned: 'badge-success', overdue: 'badge-danger', cancelled: 'badge-neutral' };
        const labels = { borrowing: 'Đang mượn', returned: 'Đã trả', overdue: 'Quá hạn', cancelled: 'Đã hủy' };
        return `<span class="badge ${map[s] || 'badge-neutral'}">${labels[s] || s}</span>`;
      };

      const tbody = orders.length ? orders.map(o => `
        <tr>
          <td>${o.id}</td>
          <td>${o.reader_id}</td>
          <td>${o.borrow_date}</td>
          <td>${o.due_date}</td>
          <td>${statusBadge(o.status)}</td>
          <td>${o.items ? o.items.length : 0} cuốn</td>
          <td>
            <div class="action-btns">
              <button class="btn-icon" title="Chi tiết" onclick="pages.borrows.showDetail(${o.id})">👁️</button>
              ${o.status === 'borrowing' || o.status === 'overdue' ? `
                <button class="btn-icon" title="Trả sách" onclick="pages.borrows.returnOrder(${o.id})">📥</button>
                ${o.status === 'borrowing' ? `<button class="btn-icon" title="Hủy" onclick="pages.borrows.cancelOrder(${o.id})">❌</button>` : ''}
              ` : ''}
            </div>
          </td>
        </tr>
      `).join('') : '<tr><td colspan="7" class="table-empty">Không có phiếu mượn nào</td></tr>';

      document.getElementById('borrows-table').innerHTML = `
        <div class="table-container">
          <table>
            <thead><tr><th>ID</th><th>Reader ID</th><th>Ngày mượn</th><th>Hạn trả</th><th>Trạng thái</th><th>Số sách</th><th>Hành động</th></tr></thead>
            <tbody>${tbody}</tbody>
          </table>
        </div>
      `;
    } catch (err) { showToast(err.message, 'error'); }
  },

  showCreateModal() {
    const body = `
      <div class="form-group">
        <label>Reader ID</label>
        <input type="number" class="form-control" id="f-borrow-reader" placeholder="ID độc giả">
      </div>
      <div class="form-group">
        <label>Copy IDs (cách nhau bởi dấu phẩy)</label>
        <input type="text" class="form-control" id="f-borrow-copies" placeholder="1, 2, 3">
      </div>
      <div class="form-group">
        <label>Số ngày mượn</label>
        <input type="number" class="form-control" id="f-borrow-days" value="14" placeholder="14">
      </div>
    `;
    openModal('Tạo Phiếu mượn', body, `
      <button class="btn btn-secondary" onclick="closeModal()">Hủy</button>
      <button class="btn btn-primary" onclick="pages.borrows.submitCreate()">Tạo phiếu</button>
    `);
  },

  async submitCreate() {
    try {
      const readerId = parseInt(document.getElementById('f-borrow-reader').value);
      const copyIds = document.getElementById('f-borrow-copies').value.split(',').map(s => parseInt(s.trim())).filter(n => !isNaN(n));
      const borrowDays = parseInt(document.getElementById('f-borrow-days').value) || 14;

      await api.createBorrow({ reader_id: readerId, copy_ids: copyIds, borrow_days: borrowDays });
      closeModal();
      showToast('Tạo phiếu mượn thành công!', 'success');
      await this.loadTable();
    } catch (err) { showToast(err.message, 'error'); }
  },

  async showDetail(id) {
    try {
      const res = await api.getBorrow(id);
      const o = res.data;
      const itemRows = (o.items || []).map(i => `
        <tr>
          <td>${i.copy_id}</td>
          <td><span class="badge ${i.status === 'returned' ? 'badge-success' : i.status === 'borrowing' ? 'badge-info' : 'badge-neutral'}">${i.status}</span></td>
          <td>${i.returned_date || '—'}</td>
        </tr>
      `).join('') || '<tr><td colspan="3" class="table-empty">Không có</td></tr>';

      const body = `
        <div style="margin-bottom:16px;">
          <p><strong>Reader ID:</strong> ${o.reader_id}</p>
          <p><strong>Ngày mượn:</strong> ${o.borrow_date}</p>
          <p><strong>Hạn trả:</strong> ${o.due_date}</p>
          <p><strong>Trạng thái:</strong> ${o.status}</p>
        </div>
        <h3 style="margin-bottom:8px;">Danh sách sách</h3>
        <div class="table-container">
          <table>
            <thead><tr><th>Copy ID</th><th>Trạng thái</th><th>Ngày trả</th></tr></thead>
            <tbody>${itemRows}</tbody>
          </table>
        </div>
      `;
      openModal(`Phiếu mượn #${id}`, body, `<button class="btn btn-secondary" onclick="closeModal()">Đóng</button>`);
    } catch (err) { showToast(err.message, 'error'); }
  },

  async returnOrder(id) {
    const ok = await confirmDialog('Trả TẤT CẢ sách trong phiếu mượn này?');
    if (!ok) return;
    try {
      const res = await api.returnBorrow(id);
      const fines = res.data?.fines || [];
      if (fines.length > 0) {
        const total = fines.reduce((s, f) => s + f.amount, 0);
        showToast(`Đã trả sách. Phạt trễ hạn: ${total.toLocaleString('vi-VN')}đ`, 'warning');
      } else {
        showToast('Trả sách thành công!', 'success');
      }
      await this.loadTable();
    } catch (err) { showToast(err.message, 'error'); }
  },

  async cancelOrder(id) {
    const ok = await confirmDialog('Hủy phiếu mượn này?');
    if (!ok) return;
    try {
      await api.cancelBorrow(id);
      showToast('Đã hủy phiếu mượn', 'success');
      await this.loadTable();
    } catch (err) { showToast(err.message, 'error'); }
  },
};
