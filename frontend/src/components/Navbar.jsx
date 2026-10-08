import React from 'react';
import { useAuth } from '../context/AuthContext';

export default function Navbar({ activeTab, setActiveTab }) {
  const { user, isAuthenticated, isAdmin, isMerchant, logout } = useAuth();

  return (
    <header className="navbar">
      <div className="nav-brand">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ color: '#2563eb' }}>
          <rect x="2" y="4" width="20" height="16" rx="2" />
          <path d="M10 4v4" />
          <path d="M2 10h20" />
        </svg>
        <span>DWPG Simulator</span>
        <span className="brand-badge">Secure v1.0</span>
      </div>

      <nav className="nav-links">
        {isAuthenticated ? (
          <>
            <button
              className={`nav-item ${activeTab === 'wallet' ? 'active' : ''}`}
              onClick={() => setActiveTab('wallet')}
            >
              Wallet
            </button>

            <button
              className={`nav-item ${activeTab === 'payment' ? 'active' : ''}`}
              onClick={() => setActiveTab('payment')}
            >
              Checkout / Payment
            </button>

            <button
              className={`nav-item ${activeTab === 'transactions' ? 'active' : ''}`}
              onClick={() => setActiveTab('transactions')}
            >
              Ledger & History
            </button>

            <button
              className={`nav-item ${activeTab === 'merchant' ? 'active' : ''}`}
              onClick={() => setActiveTab('merchant')}
            >
              Merchant
            </button>

            <button
              className={`nav-item ${activeTab === 'demo-store' ? 'active' : ''}`}
              onClick={() => setActiveTab('demo-store')}
              style={{ color: '#4f46e5', fontWeight: 600 }}
            >
              🛒 Demo Store
            </button>

            {isAdmin && (
              <button
                className={`nav-item ${activeTab === 'admin' ? 'active' : ''}`}
                onClick={() => setActiveTab('admin')}
              >
                Security Audit
              </button>
            )}

            <div className="user-pill">
              <span>{user?.username}</span>
              <span className="role-tag">{user?.role?.replace('ROLE_', '')}</span>
            </div>

            <button className="btn btn-secondary btn-sm" onClick={logout}>
              Sign Out
            </button>
          </>
        ) : (
          <>
            <button
              className={`nav-item ${activeTab === 'login' ? 'active' : ''}`}
              onClick={() => setActiveTab('login')}
            >
              Sign In
            </button>
            <button
              className={`nav-item ${activeTab === 'register' ? 'active' : ''}`}
              onClick={() => setActiveTab('register')}
            >
              Register
            </button>
          </>
        )}
      </nav>
    </header>
  );
}
