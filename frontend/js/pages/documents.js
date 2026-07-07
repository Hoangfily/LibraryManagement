/**
 * Documents management page — CRUD + search.
 */
pages.documents = {
  async render(container) {
    container.innerHTML = `
      <div class="page-header">
        <div>
          <h1>📖 Quản lý Tài liệu</h1>
          <p class="page-desc">Thêm, sửa, xóa sách và tài liệu trong thư viện</p>
        </div>
        <button class="btn btn-primary" onclick="pages.documents.showCreateModal()">+ Thêm tài liệu</button>
      </div>
      <div class="toolbar">
        <div class="search-box">
          <span class="search-icon">🔍</span>
          <input type="text" id="doc-search" placeholder="Tìm theo tiêu đề...">
        </div>
      </div>
      <div id="docs-table"></div>
    `;

    document.getElementById('doc-search').addEventListener('input', this.debounce(() => this.loadTable(), 400));
    await this.loadTable();
  },

  async loadTable() {
    const keyword = document.getElementById('doc-search')?.value?.trim() || '';
    try {
      const res = keyword ? await api.searchDocuments(keyword) : await api.getDocuments();
      const docs = res.data || [];
      const tbody = docs.length ? docs.map(d => `
        <tr>
          <td>${d.id}</td>
          <td><strong>${d.title}</strong></td>
          <td>${d.author || '—'}</td>
          <td>${d.publisher || '—'}</td>
          <td>${d.publish_year || '—'}</td>
          <td>${d.category || '—'}</td>
          <td>${d.total_copies}</td>
          <td>
            <div class="action-btns">
              <button class="btn-icon" title="Bản sao" onclick="pages.documents.showCopiesModal(${d.id})">📚</button>
              <button class="btn-icon" title="Sửa" onclick="pages.documents.showEditModal(${d.id})">✏️</button>
              <button class="btn-icon" title="Xóa" onclick="pages.documents.deleteDoc(${d.id})">🗑️</button>
            </div>
          </td>
        </tr>
      `).join('') : '<tr><td colspan="8" class="table-empty">Không có tài liệu nào</td></tr>';

      document.getElementById('docs-table').innerHTML = `
        <div class="table-container">
          <table>
            <thead><tr><th>ID</th><th>Tiêu đề</th><th>Tác giả</th><th>NXB</th><th>Năm</th><th>Thể loại</th><th>Bản sao</th><th>Hành động</th></tr></thead>
            <tbody>${tbody}</tbody>
          </table>
        </div>
      `;
    } catch (err) { showToast(err.message, 'error'); }
  },

  formHtml(data = {}) {
    return `
      <div class="form-group">
        <label>Tiêu đề *</label>
        <input type="text" class="form-control" id="f-doc-title" value="${data.title || ''}" placeholder="Tên sách">
      </div>
      <div class="form-row">
        <div class="form-group">
          <label>Tác giả</label>
          <input type="text" class="form-control" id="f-doc-author" value="${data.author || ''}" placeholder="Tác giả">
        </div>
        <div class="form-group">
          <label>Nhà xuất bản</label>
          <input type="text" class="form-control" id="f-doc-publisher" value="${data.publisher || ''}" placeholder="NXB">
        </div>
      </div>
      <div class="form-row">
        <div class="form-group">
          <label>Năm xuất bản</label>
          <input type="number" class="form-control" id="f-doc-year" value="${data.publish_year || ''}" placeholder="2024">
        </div>
        <div class="form-group">
          <label>Thể loại</label>
          <input type="text" class="form-control" id="f-doc-category" value="${data.category || ''}" placeholder="Văn học, CNTT...">
        </div>
      </div>
      <div class="form-group">
        <label>ISBN</label>
        <input type="text" class="form-control" id="f-doc-isbn" value="${data.isbn || ''}" placeholder="978-xxx-xxx">
      </div>
      <div class="form-group">
        <label>Mô tả</label>
        <textarea class="form-control" id="f-doc-desc" rows="3" placeholder="Mô tả ngắn...">${data.description || ''}</textarea>
      </div>
    `;
  },

  getFormData() {
    return {
      title: document.getElementById('f-doc-title').value.trim(),
      author: document.getElementById('f-doc-author').value.trim() || null,
      publisher: document.getElementById('f-doc-publisher').value.trim() || null,
      publish_year: parseInt(document.getElementById('f-doc-year').value) || null,
      category: document.getElementById('f-doc-category').value.trim() || null,
      isbn: document.getElementById('f-doc-isbn').value.trim() || null,
      description: document.getElementById('f-doc-desc').value.trim() || null,
    };
  },

  showCreateModal() {
    openModal('Thêm Tài liệu', this.formHtml(), `
      <button class="btn btn-secondary" onclick="closeModal()">Hủy</button>
      <button class="btn btn-primary" onclick="pages.documents.submitCreate()">Tạo</button>
    `);
  },

  async showEditModal(id) {
    try {
      const res = await api.getDocument(id);
      openModal('Sửa Tài liệu', this.formHtml(res.data), `
        <button class="btn btn-secondary" onclick="closeModal()">Hủy</button>
        <button class="btn btn-primary" onclick="pages.documents.submitEdit(${id})">Cập nhật</button>
      `);
    } catch (err) { showToast(err.message, 'error'); }
  },

  async submitCreate() {
    try {
      await api.createDocument(this.getFormData());
      closeModal();
      showToast('Thêm tài liệu thành công!', 'success');
      await this.loadTable();
    } catch (err) { showToast(err.message, 'error'); }
  },

  async submitEdit(id) {
    try {
      await api.updateDocument(id, this.getFormData());
      closeModal();
      showToast('Cập nhật thành công!', 'success');
      await this.loadTable();
    } catch (err) { showToast(err.message, 'error'); }
  },

  async deleteDoc(id) {
    const ok = await confirmDialog('Bạn chắc chắn muốn xóa tài liệu này?');
    if (!ok) return;
    try {
      await api.deleteDocument(id);
      showToast('Đã xóa tài liệu', 'success');
      await this.loadTable();
    } catch (err) { showToast(err.message, 'error'); }
  },

  debounce(fn, ms) {
    let t;
    return (...args) => { clearTimeout(t); t = setTimeout(() => fn(...args), ms); };
  },

  async showCopiesModal(documentId) {
    this._copiesDocId = documentId;
    await this.renderCopiesModal();
  },

  async renderCopiesModal() {
    const documentId = this._copiesDocId;
    try {
      const res = await api.getDocumentCopies(documentId);
      const copies = res.data || [];
      const statusBadge = (s) => {
        const map = { available: 'badge-success', borrowed: 'badge-info', lost: 'badge-danger', damaged: 'badge-neutral' };
        const labels = { available: 'Sẵn có', borrowed: 'Đang mượn', lost: 'Mất', damaged: 'Hỏng' };
        return `<span class="badge ${map[s] || 'badge-neutral'}">${labels[s] || s}</span>`;
      };
      const rows = copies.length ? copies.map(c => `
        <tr>
          <td>${c.id}</td>
          <td>${c.copy_code}</td>
          <td>${statusBadge(c.status)}</td>
        </tr>
      `).join('') : '<tr><td colspan="3" class="table-empty">Chưa có bản sao nào</td></tr>';

      const body = `
        <div class="form-row" style="align-items:flex-end;">
          <div class="form-group">
            <label>Số lượng thêm</label>
            <input type="number" class="form-control" id="f-copy-qty" value="1" min="1" max="100">
          </div>
          <div class="form-group">
            <button class="btn btn-primary" onclick="pages.documents.addCopies()">+ Thêm bản sao</button>
          </div>
        </div>
        <div class="table-container">
          <table>
            <thead><tr><th>Copy ID</th><th>Mã bản sao</th><th>Trạng thái</th></tr></thead>
            <tbody>${rows}</tbody>
          </table>
        </div>
        <p style="margin-top:8px;color:var(--text-secondary);font-size:0.85rem;">Dùng Copy ID ở trên khi tạo phiếu mượn.</p>
      `;
      openModal('Bản sao tài liệu', body, `<button class="btn btn-secondary" onclick="closeModal()">Đóng</button>`);
    } catch (err) { showToast(err.message, 'error'); }
  },

  async addCopies() {
    const documentId = this._copiesDocId;
    const qty = parseInt(document.getElementById('f-copy-qty').value) || 1;
    try {
      await api.addDocumentCopies(documentId, qty);
      showToast(`Đã thêm ${qty} bản sao!`, 'success');
      await this.renderCopiesModal();
      await this.loadTable();
    } catch (err) { showToast(err.message, 'error'); }
  },
};
