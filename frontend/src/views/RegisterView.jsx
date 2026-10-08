import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';

export default function RegisterView({ onSuccess, onSwitchToLogin }) {
  const { register, login } = useAuth();
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState('ROLE_USER');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await register(username, email, password, role);
      // Auto login upon successful registration
      await login(username, password);
      onSuccess();
    } catch (err) {
      setError(err.message || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 460, margin: '2rem auto' }}>
      <div className="card">
        <div className="card-header">
          <div>
            <h2 className="card-title">Register Account</h2>
            <p className="card-subtitle">Join the secure digital payment simulator</p>
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
              placeholder="Username (letters & numbers)"
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label">Email Address</label>
            <input
              type="email"
              className="form-input"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@domain.com"
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
              placeholder="At least 8 chars, 1 digit, 1 special symbol"
              required
            />
            <p className="form-help">Must satisfy NIST SP 800-63B password complexity.</p>
          </div>

          <div className="form-group">
            <label className="form-label">Account Role</label>
            <select className="form-select" value={role} onChange={(e) => setRole(e.target.value)}>
              <option value="ROLE_USER">Standard Consumer (User Wallet)</option>
              <option value="ROLE_MERCHANT">Merchant / Business</option>
              <option value="ROLE_ADMIN">Compliance Auditor / Admin</option>
            </select>
          </div>

          <button type="submit" className="btn btn-primary btn-block" disabled={loading}>
            {loading ? 'Creating Account...' : 'Register'}
          </button>
        </form>

        <div style={{ marginTop: '1.5rem', textAlign: 'center', fontSize: '0.85rem' }}>
          Already have an account?{' '}
          <button
            onClick={onSwitchToLogin}
            style={{ color: 'var(--primary)', background: 'none', border: 'none', cursor: 'pointer', fontWeight: 600 }}
          >
            Sign In
          </button>
        </div>
      </div>
    </div>
  );
}
