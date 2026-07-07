/**
 * Login page
 */
pages.login = {
  render() {
    document.getElementById('app').innerHTML = `
      <div class="login-container">
        <div class="login-card">
          <div class="login-icon">📚</div>
          <h1>LibManager</h1>
          <p class="subtitle">Hệ thống Quản lý Thư viện</p>
          <form id="login-form">
            <div class="form-group">
              <label>Tên đăng nhập</label>
              <input type="text" class="form-control" id="login-username" placeholder="admin" required autofocus>
            </div>
            <div class="form-group">
              <label>Mật khẩu</label>
              <input type="password" class="form-control" id="login-password" placeholder="••••••••" required>
            </div>
            <button type="submit" class="btn btn-primary" style="width:100%; justify-content:center; margin-top:8px; padding:12px;">
              Đăng nhập
            </button>
          </form>
        </div>
      </div>
    `;

    document.getElementById('login-form').addEventListener('submit', async (e) => {
      e.preventDefault();
      const btn = e.target.querySelector('button[type="submit"]');
      const username = document.getElementById('login-username').value.trim();
      const password = document.getElementById('login-password').value;

      btn.disabled = true;
      btn.innerHTML = '<div class="spinner"></div> Đang đăng nhập...';

      try {
        await auth.login(username, password);
        showToast('Đăng nhập thành công!', 'success');
        navigate('#/dashboard');
      } catch (err) {
        showToast(err.message || 'Sai tên đăng nhập hoặc mật khẩu', 'error');
      } finally {
        btn.disabled = false;
        btn.textContent = 'Đăng nhập';
      }
    });
  }
};
