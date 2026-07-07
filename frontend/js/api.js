/**
 * API client — handles all HTTP requests to the backend.
 * Automatically attaches JWT token from localStorage.
 */

const API_BASE = 'http://127.0.0.1:8000';

async function request(method, path, body = null) {
  const headers = { 'Content-Type': 'application/json' };
  const token = localStorage.getItem('token');
  if (token) headers['Authorization'] = `Bearer ${token}`;

  const opts = { method, headers };
  if (body) opts.body = JSON.stringify(body);

  const res = await fetch(`${API_BASE}${path}`, opts);

  if (res.status === 401) {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.hash = '#/login';
    throw new Error('Session expired');
  }

  const json = await res.json();

  if (!res.ok) {
    const msg = json.detail?.message || json.detail || json.message || 'Request failed';
    throw new Error(msg);
  }

  return json;
}

const api = {
  // Auth
  login: (username, password) => request('POST', '/auth/login', { username, password }),

  // Users
  getUsers: () => request('GET', '/users'),
  createUser: (data) => request('POST', '/users', data),

  // Readers
  getReaders: (keyword = '') => request('GET', `/readers${keyword ? `?keyword=${encodeURIComponent(keyword)}` : ''}`),
  getReader: (id) => request('GET', `/readers/${id}`),
  createReader: (data) => request('POST', '/readers', data),
  updateReader: (id, data) => request('PUT', `/readers/${id}`, data),
  updateReaderStatus: (id, status) => request('PATCH', `/readers/${id}/status`, { status }),

  // Documents
  getDocuments: () => request('GET', '/documents'),
  searchDocuments: (title) => request('GET', `/documents/search?title=${encodeURIComponent(title)}`),
  getDocument: (id) => request('GET', `/documents/${id}`),
  createDocument: (data) => request('POST', '/documents', data),
  updateDocument: (id, data) => request('PUT', `/documents/${id}`, data),
  deleteDocument: (id) => request('DELETE', `/documents/${id}`),

  // Copies
  getCopy: (id) => request('GET', `/copies/${id}`),
  updateCopyStatus: (id, status) => request('PATCH', `/copies/${id}/status`, { status }),
  getDocumentCopies: (documentId) => request('GET', `/documents/${documentId}/copies`),
  addDocumentCopies: (documentId, quantity) => request('POST', `/documents/${documentId}/copies`, { quantity }),

  // Borrows
  getBorrows: (readerId = null, status = null) => {
    const params = new URLSearchParams();
    if (readerId) params.set('reader_id', readerId);
    if (status) params.set('status', status);
    const qs = params.toString();
    return request('GET', `/borrows${qs ? `?${qs}` : ''}`);
  },
  getBorrow: (id) => request('GET', `/borrows/${id}`),
  createBorrow: (data) => request('POST', '/borrows', data),
  returnBorrow: (id, copyIds = null) => request('POST', `/borrows/${id}/return`, copyIds ? { copy_ids: copyIds } : {}),
  cancelBorrow: (id) => request('POST', `/borrows/${id}/cancel`),

  // Fines
  getFines: (readerId = null, status = null) => {
    const params = new URLSearchParams();
    if (readerId) params.set('reader_id', readerId);
    if (status) params.set('status', status);
    const qs = params.toString();
    return request('GET', `/fines${qs ? `?${qs}` : ''}`);
  },
  getFine: (id) => request('GET', `/fines/${id}`),
  payFine: (id) => request('PATCH', `/fines/${id}/pay`),

  // Reports
  getSummary: () => request('GET', '/reports/summary'),
};
