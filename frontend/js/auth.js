/**
 * Auth helpers — manage JWT token and user session.
 */

const auth = {
  getToken() {
    return localStorage.getItem('token');
  },

  getUser() {
    const raw = localStorage.getItem('user');
    return raw ? JSON.parse(raw) : null;
  },

  isLoggedIn() {
    return !!this.getToken();
  },

  /** Decode JWT payload (without verification — just for display). */
  decodeToken(token) {
    try {
      const payload = token.split('.')[1];
      return JSON.parse(atob(payload));
    } catch {
      return null;
    }
  },

  async login(username, password) {
    const res = await api.login(username, password);
    const token = res.data.access_token;
    localStorage.setItem('token', token);

    const payload = this.decodeToken(token);
    const user = {
      id: payload.sub,
      username: payload.username,
      role: payload.role,
    };
    localStorage.setItem('user', JSON.stringify(user));
    return user;
  },

  logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.hash = '#/login';
  },

  isAdmin() {
    const user = this.getUser();
    return user && user.role === 'admin';
  },
};
