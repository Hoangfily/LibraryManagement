/**
 * Readers management page — CRUD + search + lock/unlock.
 */
pages.readers = {
  async render(container) {
    container.innerHTML = `
      <div class="page-header">
        <div>
          <h1>👥 Quản lý Độc giả</h1>
          <p class="page-desc">Thêm, sửa, khóa/mở khóa tài khoản độc giả</p>
        </div>
        <button class="btn btn-primary" onclick="pages.readers.showCreateModal()">+ Thêm độc giả</button>
      </div>
      <div class="toolbar">
        <div class="search-box">
          <span class="search-icon">🔍</span>
          <input type="text" id="reader-search" placeholder="Tìm theo tên hoặc mã...">
        </div>
      </div>
      <div id="readers-table"></div>
    `;

    document.getElementById('reader-search').addEventListener('input', this.debounce(() => this.loadTable(), 400));
    await this.loadTable();
  },

  async loadTable() {
    const keyword = document.getElementById('reader-search')?.value || '';
    try {
      const res = await api.getReaders(keyword);
      const readers = res.data || [];
      const tbody = readers.length ? readers.map(r => `
        <tr>
          <td>${r.id}</td>
          <td><strong>${r.reader_code}</strong></td>
          <td>${r.full_name}</td>
          <td>${r.email || '—'}</td>
          <td>${r.phone || '—'}</td>
          <td><span class="badge ${r.status === 'active' ? 'badge-success' : 'badge-danger'}">${r.status === 'active' ? '✓ Active' : '✕ Inactive'}</span></td>
          <td>
            <div class="action-btns">
              <button class="btn-icon" title="Sửa" onclick="pages.readers.showEditModal(${r.id})">✏️</button>
              <button class="btn-icon" title="${r.status === 'active' ? 'Khóa' : 'Mở khóa'}" onclick="pages.readers.toggleStatus(${r.id}, '${r.status}')">
                ${r.status === 'active' ? '🔒' : '🔓'}
              </button>
            </div>
          </td>
        </tr>
      `).join('') : '<tr><td colspan="7" class="table-empty">Không có độc giả nào</td></tr>';

      document.getElementById('readers-table').innerHTML = `
        <div class="table-container">
          <table>
            <thead><tr><th>ID</th><th>Mã</th><th>Họ tên</th><th>Email</th><th>SĐT</th><th>Trạng thái</th><th>Hành động</th></tr></thead>
            <tbody>${tbody}</tbody>
          </table>
        </div>
      `;
    } catch (err) {
      showToast(err.message, 'error');
    }
  },

  showCreateModal() {
    const body = this.formHtml();
    const footer = `
      <button class="btn btn-secondary" onclick="closeModal()">Hủy</button>
      <button class="btn btn-primary" onclick="pages.readers.submitCreate()">Tạo</button>
    `;
    openModal('Thêm Độc giả', body, footer);
  },

  async showEditModal(id) {
    try {
      const res = await api.getReader(id);
      const r = res.data;
      const body = this.formHtml(r);
      const footer = `
        <button class="btn btn-secondary" onclick="closeModal()">Hủy</button>
        <button class="btn btn-primary" onclick="pages.readers.submitEdit(${id})">Cập nhật</button>
      `;
      openModal('Sửa Độc giả', body, footer);
    } catch (err) {
      showToast(err.message, 'error');
    }
  },

  formHtml(data = {}) {
    return `
      <div class="form-group">
        <label>Mã độc giả</label>
        <input type="text" class="form-control" id="f-reader-code" value="${data.reader_code || ''}" ${data.reader_code ? 'disabled' : ''} placeholder="DG001">
      </div>
      <div class="form-group">
        <label>Họ tên</label>
        <input type="text" class="form-control" id="f-reader-name" value="${data.full_name || ''}" placeholder="Nguyễn Văn A">
      </div>
      <div class="form-row">
        <div class="form-group">
          <label>Email</label>
          <input type="email" class="form-control" id="f-reader-email" value="${data.email || ''}" placeholder="email@example.com">
        </div>
        <div class="form-group">
          <label>Số điện thoại</label>
          <input type="text" class="form-control" id="f-reader-phone" value="${data.phone || ''}" placeholder="0901234567">
        </div>
      </div>
      <div class="form-group">
        <label>Địa chỉ</label>
        <input type="text" class="form-control" id="f-reader-address" value="${data.address || ''}" placeholder="123 Đường ABC, Quận XYZ">
      </div>
    `;
  },

  getFormData() {
    return {
      reader_code: document.getElementById('f-reader-code').value.trim(),
      full_name: document.getElementById('f-reader-name').value.trim(),
      email: document.getElementById('f-reader-email').value.trim() || null,
      phone: document.getElementById('f-reader-phone').value.trim() || null,
      address: document.getElementById('f-reader-address').value.trim() || null,
    };
  },

  async submitCreate() {
    try {
      await api.createReader(this.getFormData());
      closeModal();
      showToast('Thêm độc giả thành công!', 'success');
      await this.loadTable();
    } catch (err) { showToast(err.message, 'error'); }
  },

  async submitEdit(id) {
    try {
      const data = this.getFormData();
      delete data.reader_code;
      await api.updateReader(id, data);
      closeModal();
      showToast('Cập nhật thành công!', 'success');
      await this.loadTable();
    } catch (err) { showToast(err.message, 'error'); }
  },

  async toggleStatus(id, current) {
    const newStatus = current === 'active' ? 'inactive' : 'active';
    const msg = current === 'active' ? 'Bạn muốn KHÓA độc giả này?' : 'Bạn muốn MỞ KHÓA độc giả này?';
    const ok = await confirmDialog(msg);
    if (!ok) return;
    try {
      await api.updateReaderStatus(id, newStatus);
      showToast(`Đã ${newStatus === 'active' ? 'mở khóa' : 'khóa'} thành công`, 'success');
      await this.loadTable();
    } catch (err) { showToast(err.message, 'error'); }
  },

  debounce(fn, ms) {
    let t;
    return (...args) => { clearTimeout(t); t = setTimeout(() => fn(...args), ms); };
  },
};
