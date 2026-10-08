import React, { useState, useEffect } from 'react';
import { merchantApi } from '../api';

export default function MerchantView() {
  const [merchant, setMerchant] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [businessName, setBusinessName] = useState('');
  const [actionLoading, setActionLoading] = useState(false);
  const [successMsg, setSuccessMsg] = useState('');
  const [showApiKey, setShowApiKey] = useState(false);

  const loadMerchant = async () => {
    setError('');
    try {
      const data = await merchantApi.getMyMerchant();
      setMerchant(data);
    } catch (err) {
      if (err.status === 404) {
        setMerchant(null);
      } else {
        setError(err.message || 'Failed to fetch merchant profile');
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadMerchant();
  }, []);

  const handleRegister = async (e) => {
    e.preventDefault();
    setActionLoading(true);
    setError('');
    setSuccessMsg('');

    try {
      const newMerchant = await merchantApi.register(businessName);
      setMerchant(newMerchant);
      setSuccessMsg('Merchant account registered successfully!');
    } catch (err) {
      setError(err.message || 'Merchant registration failed');
    } finally {
      setActionLoading(false);
    }
  };

  if (loading) {
    return <div className="card"><p>Loading merchant profile...</p></div>;
  }

  return (
    <div>
      <div className="security-banner">
        <div>
          <h3>Merchant Credential & API Security</h3>
          <p style={{ fontSize: '0.85rem', opacity: 0.9 }}>
            Merchants receive a unique 256-bit API key for HMAC signing and merchant-only operational authorization.
          </p>
        </div>
        <div className="security-badges">
          <span className="sec-badge">🔑 256-Bit API Key</span>
          <span className="sec-badge">🛡️ Role Protected</span>
        </div>
      </div>

      {error && <div className="alert alert-danger">{error}</div>}
      {successMsg && <div className="alert alert-success">{successMsg}</div>}

      {!merchant ? (
        <div className="card" style={{ maxWidth: 520, margin: '1rem auto' }}>
          <div className="card-header">
            <div>
              <h2 className="card-title">Register Merchant Profile</h2>
              <p className="card-subtitle">Accept simulated payments from registered wallets</p>
            </div>
          </div>

          <form onSubmit={handleRegister}>
            <div className="form-group">
              <label className="form-label">Business / Store Name</label>
              <input
                type="text"
                className="form-input"
                placeholder="e.g. Acme Tech Stores, SuperMart Simulator"
                value={businessName}
                onChange={(e) => setBusinessName(e.target.value)}
                required
              />
            </div>

            <button type="submit" className="btn btn-primary btn-block" disabled={actionLoading}>
              {actionLoading ? 'Registering...' : 'Provision Merchant Profile'}
            </button>
          </form>
        </div>
      ) : (
        <div className="card">
          <div className="card-header">
            <div>
              <h2 className="card-title">{merchant.businessName}</h2>
              <p className="card-subtitle">Merchant Account #{merchant.id}</p>
            </div>
            <span className={`badge badge-${merchant.status}`}>{merchant.status}</span>
          </div>

          <div className="grid-2">
            <div className="metric-box">
              <span className="metric-label">Merchant Identifier</span>
              <div className="metric-value">#{merchant.id}</div>
              <p className="metric-desc">Users submit this ID when making payments.</p>
            </div>

            <div className="metric-box">
              <span className="metric-label">Account Status</span>
              <div className="metric-value" style={{ color: '#16a34a' }}>ACTIVE</div>
              <p className="metric-desc">Provisioned on {new Date(merchant.createdAt).toLocaleDateString()}</p>
            </div>
          </div>

          <div style={{ marginTop: '1.5rem', background: '#f8fafc', padding: '1.25rem', borderRadius: 'var(--radius)', border: '1px solid var(--border)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
              <label className="form-label" style={{ marginBottom: 0 }}>API Security Key</label>
              <button
                type="button"
                className="btn btn-secondary btn-sm"
                onClick={() => setShowApiKey(!showApiKey)}
              >
                {showApiKey ? 'Hide Key' : 'Reveal Key'}
              </button>
            </div>
            <div className="code-pill" style={{ padding: '0.6rem 0.8rem', fontSize: '0.85rem' }}>
              {showApiKey ? merchant.apiKey : '••••••••••••••••••••••••••••••••••••••••••••••••'}
            </div>
            <p className="form-help">Keep this API key confidential. Never expose in public client-side scripts.</p>
          </div>
        </div>
      )}
    </div>
  );
}
