/**
 * Users management page (Admin only) — list + create.
 */
pages.users = {
  async render(container) {
    container.innerHTML = `
      <div class="page-header">
        <div>
          <h1>⚙️ Quản lý User</h1>
          <p class="page-desc">Tạo tài khoản admin và thủ thư (chỉ Admin)</p>
        </div>
        <button class="btn btn-primary" onclick="pages.users.showCreateModal()">+ Thêm user</button>
      </div>
      <div id="users-table"></div>
    `;
    await this.loadTable();
  },

  async loadTable() {
    try {
      const res = await api.getUsers();
      const users = res.data || [];
      const tbody = users.length ? users.map(u => `
        <tr>
          <td>${u.id}</td>
          <td><strong>${u.username}</strong></td>
          <td>${u.full_name}</td>
          <td><span class="badge ${u.role === 'admin' ? 'badge-danger' : 'badge-info'}">${u.role}</span></td>
          <td><span class="badge ${u.is_active ? 'badge-success' : 'badge-neutral'}">${u.is_active ? 'Active' : 'Disabled'}</span></td>
        </tr>
      `).join('') : '<tr><td colspan="5" class="table-empty">Không có user nào</td></tr>';

      document.getElementById('users-table').innerHTML = `
        <div class="table-container">
          <table>
            <thead><tr><th>ID</th><th>Username</th><th>Họ tên</th><th>Vai trò</th><th>Trạng thái</th></tr></thead>
            <tbody>${tbody}</tbody>
          </table>
        </div>
      `;
    } catch (err) { showToast(err.message, 'error'); }
  },

  showCreateModal() {
    const body = `
      <div class="form-group">
        <label>Username</label>
        <input type="text" class="form-control" id="f-user-username" placeholder="username">
      </div>
      <div class="form-group">
        <label>Mật khẩu</label>
        <input type="password" class="form-control" id="f-user-password" placeholder="••••••••">
      </div>
      <div class="form-group">
        <label>Họ tên</label>
        <input type="text" class="form-control" id="f-user-fullname" placeholder="Nguyễn Văn B">
      </div>
      <div class="form-group">
        <label>Vai trò</label>
        <select class="form-control" id="f-user-role">
          <option value="librarian">Thủ thư (Librarian)</option>
          <option value="admin">Quản trị (Admin)</option>
        </select>
      </div>
    `;
    openModal('Thêm User', body, `
      <button class="btn btn-secondary" onclick="closeModal()">Hủy</button>
      <button class="btn btn-primary" onclick="pages.users.submitCreate()">Tạo</button>
    `);
  },

  async submitCreate() {
    try {
      await api.createUser({
        username: document.getElementById('f-user-username').value.trim(),
        password: document.getElementById('f-user-password').value,
        full_name: document.getElementById('f-user-fullname').value.trim(),
        role: document.getElementById('f-user-role').value,
      });
      closeModal();
      showToast('Tạo user thành công!', 'success');
      await this.loadTable();
    } catch (err) { showToast(err.message, 'error'); }
  },
};
