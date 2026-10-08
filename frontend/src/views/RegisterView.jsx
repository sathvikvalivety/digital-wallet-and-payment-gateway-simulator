import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';

export default function RegisterView({ onSuccess, onSwitchToLogin }) {
  const { register, login, loginWithGoogle } = useAuth();
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

        <div style={{ margin: '1.25rem 0', textAlign: 'center', position: 'relative' }}>
          <span style={{ background: 'var(--card-bg, #ffffff)', padding: '0 0.5rem', color: 'var(--text-muted)', fontSize: '0.8rem' }}>
            OR REGISTER WITH
          </span>
        </div>

        <button
          type="button"
          className="btn btn-secondary btn-block"
          onClick={async () => {
            setError('');
            setLoading(true);
            try {
              const googleEmail = prompt('Enter Google email to create account with Google OAuth:', 'sathvikvalivety@gmail.com');
              if (!googleEmail) {
                setLoading(false);
                return;
              }
              await loginWithGoogle({
                email: googleEmail.trim(),
                name: googleEmail.split('@')[0],
                googleId: 'google_' + Date.now(),
              });
              onSuccess();
            } catch (err) {
              setError(err.message || 'Google registration failed');
            } finally {
              setLoading(false);
            }
          }}
          disabled={loading}
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '0.75rem',
            fontWeight: 600,
            border: '1px solid #dadce0',
            backgroundColor: '#ffffff',
            color: '#3c4043',
            boxShadow: '0 1px 2px rgba(0,0,0,0.05)',
          }}
        >
          <svg width="18" height="18" viewBox="0 0 18 18">
            <path fill="#4285F4" d="M17.64 9.2c0-.637-.057-1.251-.164-1.84H9v3.481h4.844c-.209 1.125-.843 2.078-1.796 2.717v2.258h2.908c1.702-1.567 2.684-3.874 2.684-6.616z"/>
            <path fill="#34A853" d="M9 18c2.43 0 4.467-.806 5.956-2.184l-2.908-2.258c-.806.54-1.837.86-3.048.86-2.344 0-4.328-1.584-5.036-3.711H.957v2.332C2.438 15.983 5.482 18 9 18z"/>
            <path fill="#FBBC05" d="M3.964 10.707c-.18-.54-.282-1.117-.282-1.707s.102-1.167.282-1.707V4.961H.957C.347 6.175 0 7.55 0 9s.347 2.825.957 4.039l3.007-2.332z"/>
            <path fill="#EA4335" d="M9 3.58c1.321 0 2.508.454 3.44 1.345l2.582-2.58C13.463.891 11.426 0 9 0 5.482 0 2.438 2.017.957 4.961L3.964 7.293C4.672 5.166 6.656 3.58 9 3.58z"/>
          </svg>
          Sign up with Google
        </button>

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
