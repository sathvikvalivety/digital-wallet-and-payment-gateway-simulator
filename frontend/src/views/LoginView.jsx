import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';

export default function LoginView({ onSuccess, onSwitchToRegister }) {
  const { login } = useAuth();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await login(username, password);
      onSuccess();
    } catch (err) {
      setError(err.message || 'Invalid username or password');
    } finally {
      setLoading(false);
    }
  };

  const fillQuickAccount = (user, pass) => {
    setUsername(user);
    setPassword(pass);
  };

  return (
    <div style={{ maxWidth: 440, margin: '2rem auto' }}>
      <div className="card">
        <div className="card-header">
          <div>
            <h2 className="card-title">Sign In</h2>
            <p className="card-subtitle">Access your secure digital wallet</p>
          </div>
        </div>

        {error && <div className="alert alert-danger">{error}</div>}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label">Username</label>
            <input
              type="text"
              className="form-input"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="e.g. alice, merchant_bob, admin"
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label">Password</label>
            <input
              type="password"
              className="form-input"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••••••"
              required
            />
          </div>

          <button type="submit" className="btn btn-primary btn-block" disabled={loading}>
            {loading ? 'Authenticating...' : 'Sign In'}
          </button>
        </form>

        <div style={{ marginTop: '1.5rem', textAlign: 'center', fontSize: '0.85rem' }}>
          Don't have an account?{' '}
          <button
            onClick={onSwitchToRegister}
            style={{ color: 'var(--primary)', background: 'none', border: 'none', cursor: 'pointer', fontWeight: 600 }}
          >
            Create an Account
          </button>
        </div>

        <div style={{ marginTop: '1.5rem', paddingTop: '1rem', borderTop: '1px solid var(--border)' }}>
          <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginBottom: '0.5rem', fontWeight: 600 }}>
            SIMULATOR TEST SHORTCUTS:
          </p>
          <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
            <button
              type="button"
              className="btn btn-secondary btn-sm"
              onClick={() => fillQuickAccount('alice', 'SecurePass123!')}
            >
              Fill Alice (User)
            </button>
            <button
              type="button"
              className="btn btn-secondary btn-sm"
              onClick={() => fillQuickAccount('merchant_bob', 'SecurePass123!')}
            >
              Fill Bob (Merchant)
            </button>
            <button
              type="button"
              className="btn btn-secondary btn-sm"
              onClick={() => fillQuickAccount('admin', 'AdminPass123!')}
            >
              Fill Admin
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
