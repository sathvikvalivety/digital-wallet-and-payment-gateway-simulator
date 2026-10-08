import React, { useState, useEffect } from 'react';
import { walletApi } from '../api';
import UpiPaymentModal from '../components/UpiPaymentModal';

export default function WalletView() {
  const [wallet, setWallet] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [topUpAmount, setTopUpAmount] = useState('');
  const [actionLoading, setActionLoading] = useState(false);
  const [successMsg, setSuccessMsg] = useState('');
  const [showUpiModal, setShowUpiModal] = useState(false);

  const loadWallet = async () => {
    setError('');
    try {
      const data = await walletApi.getWallet();
      setWallet(data);
    } catch (err) {
      if (err.status === 404) {
        setWallet(null);
      } else {
        setError(err.message || 'Failed to fetch wallet');
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadWallet();
  }, []);

  const handleCreateWallet = async () => {
    setActionLoading(true);
    setError('');
    try {
      const newWallet = await walletApi.createWallet();
      setWallet(newWallet);
      setSuccessMsg('Wallet created successfully with zero balance!');
    } catch (err) {
      setError(err.message || 'Failed to create wallet');
    } finally {
      setActionLoading(false);
    }
  };

  const handleTopUp = async (e) => {
    e.preventDefault();
    const amount = parseFloat(topUpAmount);
    if (isNaN(amount) || amount <= 0) {
      setError('Please enter a valid positive amount.');
      return;
    }

    setActionLoading(true);
    setError('');
    setSuccessMsg('');

    try {
      const updated = await walletApi.topUp(amount);
      setWallet(updated);
      setSuccessMsg(`Successfully added ₹${amount.toFixed(2)} simulated funds!`);
      setTopUpAmount('');
    } catch (err) {
      setError(err.message || 'Top-up failed');
    } finally {
      setActionLoading(false);
    }
  };

  if (loading) {
    return <div className="card"><p>Loading wallet profile...</p></div>;
  }

  return (
    <div>
      <div className="security-banner">
        <div>
          <h3>Simulated Vault & Wallet Safeguards</h3>
          <p style={{ fontSize: '0.85rem', opacity: 0.9 }}>
            Row-level pessimistic locking & ACID boundaries prevent negative balance or double spending.
          </p>
        </div>
        <div className="security-badges">
          <span className="sec-badge">🔒 Row-Lock Active</span>
          <span className="sec-badge">🛡️ Balance Non-Negative</span>
          <span className="sec-badge">⚡ Atomic Top-Up</span>
        </div>
      </div>

      {error && <div className="alert alert-danger">{error}</div>}
      {successMsg && <div className="alert alert-success">{successMsg}</div>}

      {!wallet ? (
        <div className="card" style={{ textAlign: 'center', padding: '3rem 1.5rem' }}>
          <h2 style={{ marginBottom: '0.5rem' }}>No Active Wallet Found</h2>
          <p style={{ color: 'var(--text-muted)', marginBottom: '1.5rem' }}>
            You haven't initialized a simulated digital wallet yet. Click below to provision one securely.
          </p>
          <button className="btn btn-primary" onClick={handleCreateWallet} disabled={actionLoading}>
            {actionLoading ? 'Initializing...' : 'Create My Simulated Wallet'}
          </button>
        </div>
      ) : (
        <div className="grid-2">
          {/* Balance & Account Card */}
          <div className="card">
            <div className="card-header">
              <div>
                <h2 className="card-title">Digital Wallet</h2>
                <p className="card-subtitle">Account #{wallet.accountNumber}</p>
              </div>
              <span className={`badge badge-${wallet.status}`}>{wallet.status}</span>
            </div>

            <div className="metric-box" style={{ background: '#f0fdf4', borderColor: '#bbf7d0' }}>
              <span className="metric-label">Available Balance</span>
              <div className="metric-value" style={{ color: '#15803d' }}>
                ₹{parseFloat(wallet.balance).toFixed(2)} <span style={{ fontSize: '1rem', fontWeight: 500 }}>{wallet.currency || 'INR'}</span>
              </div>
              <p className="metric-desc">Zero real fiat money. Strictly simulated educational funds.</p>
            </div>

            <div style={{ marginTop: '1.25rem', fontSize: '0.85rem', display: 'flex', flexDirection: 'column', gap: '0.4rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: 'var(--text-muted)' }}>Wallet ID:</span>
                <span className="code-pill">#{wallet.id}</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: 'var(--text-muted)' }}>Created At:</span>
                <span>{new Date(wallet.createdAt).toLocaleString()}</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: 'var(--text-muted)' }}>Last Updated:</span>
                <span>{new Date(wallet.updatedAt).toLocaleString()}</span>
              </div>
            </div>
          </div>

          {/* Simulated Funds Top-Up Card */}
          <div className="card">
            <div className="card-header">
              <div>
                <h2 className="card-title">Add Simulated Funds</h2>
                <p className="card-subtitle">Top up your wallet balance instantly</p>
              </div>
            </div>

            <form onSubmit={handleTopUp}>
              <div className="form-group">
                <label className="form-label">Amount (₹ INR)</label>
                <input
                  type="number"
                  step="0.01"
                  min="0.01"
                  max="50000.00"
                  className="form-input"
                  placeholder="0.00"
                  value={topUpAmount}
                  onChange={(e) => setTopUpAmount(e.target.value)}
                  required
                />
              </div>

              <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '1.25rem', flexWrap: 'wrap' }}>
                {[50, 100, 250, 500, 1000].map((amt) => (
                  <button
                    key={amt}
                    type="button"
                    className="btn btn-secondary btn-sm"
                    onClick={() => setTopUpAmount(amt.toString())}
                  >
                    +₹{amt}
                  </button>
                ))}
              </div>

              <button type="submit" className="btn btn-primary btn-block" disabled={actionLoading}>
                {actionLoading ? 'Processing Top-Up...' : 'Top-Up Wallet'}
              </button>

              <div style={{ margin: '1rem 0', textAlign: 'center', position: 'relative' }}>
                <span style={{ background: 'var(--card-bg, #ffffff)', padding: '0 0.5rem', color: 'var(--text-muted)', fontSize: '0.8rem' }}>
                  OR PAY WITH UPI
                </span>
              </div>

              <button
                type="button"
                className="btn btn-secondary btn-block"
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  gap: '0.5rem',
                  borderColor: '#0284c7',
                  color: '#0284c7',
                  fontWeight: 600,
                }}
                onClick={() => setShowUpiModal(true)}
              >
                <span>⚡</span> Pay via UPI QR (valivetysathvik@ibl)
              </button>
            </form>
          </div>
        </div>
      )}

      <UpiPaymentModal
        isOpen={showUpiModal}
        onClose={() => setShowUpiModal(false)}
        initialAmount={topUpAmount || '500'}
        purpose="TOPUP"
        onSuccess={() => {
          loadWallet();
          setSuccessMsg('UPI payment verified and wallet balance updated!');
        }}
      />
    </div>
  );
}
