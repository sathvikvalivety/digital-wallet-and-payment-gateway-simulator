// Centralized Secure API Client for DWPG Simulator

const API_BASE = '/api';

export function getAuthToken() {
  return localStorage.getItem('dwpg_token');
}

export function setAuthToken(token) {
  if (token) {
    localStorage.setItem('dwpg_token', token);
  } else {
    localStorage.removeItem('dwpg_token');
  }
}

export function getCurrentUser() {
  const user = localStorage.getItem('dwpg_user');
  return user ? JSON.parse(user) : null;
}

export function setCurrentUser(user) {
  if (user) {
    localStorage.setItem('dwpg_user', JSON.stringify(user));
  } else {
    localStorage.removeItem('dwpg_user');
  }
}

export async function apiRequest(endpoint, options = {}) {
  const url = `${API_BASE}${endpoint}`;
  const token = getAuthToken();

  const headers = {
    'Content-Type': 'application/json',
    ...(options.headers || {}),
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const config = {
    ...options,
    headers,
  };

  try {
    const response = await fetch(url, config);
    const contentType = response.headers.get('content-type');
    let data = null;

    if (contentType && contentType.includes('application/json')) {
      data = await response.json();
    } else {
      const text = await response.text();
      data = text ? { message: text } : {};
    }

    if (!response.ok) {
      const errorMsg = data?.message || data?.error || `HTTP error ${response.status}`;
      const error = new Error(errorMsg);
      error.status = response.status;
      error.data = data;
      throw error;
    }

    return data;
  } catch (err) {
    if (err.status === 401) {
      // Token might be expired or invalid
      // Only clear if on protected endpoint
      if (!endpoint.includes('/auth/login')) {
        setAuthToken(null);
        setCurrentUser(null);
      }
    }
    throw err;
  }
}

// Authentication Endpoints
export const authApi = {
  login: (username, password) =>
    apiRequest('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    }),
  loginWithGoogle: (payload) =>
    apiRequest('/auth/oauth/google', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),
  register: (username, email, password, role = 'ROLE_USER') =>
    apiRequest('/auth/register', {
      method: 'POST',
      body: JSON.stringify({ username, email, password, role }),
    }),
  getMe: () => apiRequest('/auth/me', { method: 'GET' }),
};

// UPI Payment & QR Code Endpoints
export const upiApi = {
  initiate: (amount, note = '', purpose = 'TOPUP', merchantId = null) =>
    apiRequest('/upi/initiate', {
      method: 'POST',
      body: JSON.stringify({
        amount: parseFloat(amount),
        note,
        purpose,
        merchantId,
      }),
    }),
  verify: (referenceId, utrNumber) =>
    apiRequest('/upi/verify', {
      method: 'POST',
      body: JSON.stringify({ referenceId, utrNumber }),
    }),
  getStatus: (referenceId) =>
    apiRequest(`/upi/status/${encodeURIComponent(referenceId)}`, { method: 'GET' }),
  simulateBankCallback: (referenceId) =>
    apiRequest(`/upi/simulate-callback/${encodeURIComponent(referenceId)}`, { method: 'POST' }),
  sendWebhook: (referenceId, utrNumber, amount, status = 'SUCCESS') =>
    apiRequest('/upi/webhook', {
      method: 'POST',
      body: JSON.stringify({ referenceId, utrNumber, amount, status }),
    }),
  getMyTransactions: () => apiRequest('/upi/my', { method: 'GET' }),
};

// Wallet Endpoints
export const walletApi = {
  getWallet: () => apiRequest('/wallet', { method: 'GET' }),
  createWallet: () => apiRequest('/wallet/create', { method: 'POST' }),
  topUp: (amount) =>
    apiRequest('/wallet/topup', {
      method: 'POST',
      body: JSON.stringify({ amount: parseFloat(amount) }),
    }),
};

// Merchant Endpoints
export const merchantApi = {
  register: (businessName) =>
    apiRequest('/merchant/register', {
      method: 'POST',
      body: JSON.stringify({ businessName }),
    }),
  getMyMerchant: () => apiRequest('/merchant/me', { method: 'GET' }),
  getMerchant: (id) => apiRequest(`/merchant/${id}`, { method: 'GET' }),
  regenerateApiKey: () => apiRequest('/merchant/regenerate-key', { method: 'POST' }),
};

// Hosted Checkout & Merchant Gateway Integration Endpoints
export const checkoutApi = {
  createSession: (apiKey, sessionData) =>
    apiRequest('/checkout/session', {
      method: 'POST',
      headers: {
        'X-Api-Key': apiKey,
      },
      body: JSON.stringify(sessionData),
    }),
  getSession: (sessionId) =>
    apiRequest(`/checkout/session/${encodeURIComponent(sessionId)}`, { method: 'GET' }),
  completeSession: (sessionId, paymentData = {}) =>
    apiRequest(`/checkout/session/${encodeURIComponent(sessionId)}/complete`, {
      method: 'POST',
      body: JSON.stringify(paymentData),
    }),
};

// Payment Endpoints (with Idempotency Key support)
export const paymentApi = {
  initiatePayment: (merchantId, amount, description, idempotencyKey) => {
    const headers = {};
    if (idempotencyKey) {
      headers['Idempotency-Key'] = idempotencyKey;
    }
    return apiRequest('/payments/initiate', {
      method: 'POST',
      headers,
      body: JSON.stringify({
        merchantId: parseInt(merchantId, 10),
        amount: parseFloat(amount),
        description,
      }),
    });
  },
  getPayment: (id) => apiRequest(`/payments/${id}`, { method: 'GET' }),
};

// Refund Endpoints
export const refundApi = {
  requestRefund: (paymentId, reason, idempotencyKey) => {
    const headers = {};
    if (idempotencyKey) {
      headers['Idempotency-Key'] = idempotencyKey;
    }
    return apiRequest('/refunds', {
      method: 'POST',
      headers,
      body: JSON.stringify({
        paymentId: parseInt(paymentId, 10),
        reason,
      }),
    });
  },
};

// Transaction History Endpoints
export const transactionApi = {
  getMyTransactions: () => apiRequest('/transactions/my', { method: 'GET' }),
};

// Admin Endpoints
export const adminApi = {
  getAuditLogs: (action = null) => {
    const query = action ? `?action=${encodeURIComponent(action)}` : '';
    return apiRequest(`/admin/audit-logs${query}`, { method: 'GET' });
  },
};
