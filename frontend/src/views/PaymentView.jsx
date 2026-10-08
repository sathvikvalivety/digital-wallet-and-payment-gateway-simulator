import React, { useState, useEffect } from 'react';
import { paymentApi, walletApi } from '../api';

function generateUUID() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
    const r = (Math.random() * 16) | 0;
    const v = c === 'x' ? r : (r & 0x3) | 0x8;
    return v.toString(16);
  });
}

export default function PaymentView() {
  const [merchantId, setMerchantId] = useState('1');
  const [amount, setAmount] = useState('25.00');
  const [description, setDescription] = useState('Simulator order checkout test');
  const [idempotencyKey, setIdempotencyKey] = useState(generateUUID());
  const [walletBalance, setWalletBalance] = useState(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [result, setResult] = useState(null);
  const [replayHistory, setReplayHistory] = useState([]);

  useEffect(() => {
    walletApi.getWallet()
      .then((w) => setWalletBalance(parseFloat(w.balance)))
      .catch(() => setWalletBalance(null));
  }, []);

  const handlePay = async (e) => {
    if (e) e.preventDefault();
    setLoading(true);
    setError('');

    const startTs = Date.now();
    try {
      const res = await paymentApi.initiatePayment(merchantId, amount, description, idempotencyKey);
      const elapsed = Date.now() - startTs;
      setResult(res);

      // Record in replay history tracker
      setReplayHistory((prev) => [
        {
          timestamp: new Date().toLocaleTimeString(),
          idempotencyKey,
          status: res.status,
          paymentId: res.id,
          elapsedMs: elapsed,
          isDuplicate: prev.some((p) => p.idempotencyKey === idempotencyKey),
        },
        ...prev,
      ]);

      // Refresh balance
      const updatedWallet = await walletApi.getWallet();
      setWalletBalance(parseFloat(updatedWallet.balance));
    } catch (err) {
      setError(err.message || 'Payment initiation failed');
    } finally {
      setLoading(false);
    }
  };

  const handleSimulateReplay = async () => {
    if (!result) {
      setError('Please execute an initial payment first before replaying.');
      return;
    }
    // Fire exact duplicate request using the active idempotencyKey
    await handlePay(null);
  };

  const handleNewKey = () => {
    setIdempotencyKey(generateUUID());
    setResult(null);
    setError('');
  };

  return (
    <div>
      <div className="security-banner">
        <div>
          <h3>Idempotency & Replay Attack Defense Lab</h3>
          <p style={{ fontSize: '0.85rem', opacity: 0.9 }}>
            Submit payments with an Idempotency-Key. Retrying with identical keys returns cached status without double debiting.
          </p>
        </div>
        <div className="security-badges">
          <span className="sec-badge">🛡️ Idempotent API</span>
          <span className="sec-badge">🔐 SHA-256 Tamper Sealed</span>
          <span className="sec-badge">⚡ Anti-Replay Guard</span>
        </div>
      </div>

      {error && <div className="alert alert-danger">{error}</div>}

      <div className="grid-2">
        {/* Payment Initiation Card */}
        <div className="card">
          <div className="card-header">
            <div>
              <h2 className="card-title">Initiate Payment</h2>
              <p className="card-subtitle">
                Available Wallet Balance: {walletBalance !== null ? `$${walletBalance.toFixed(2)}` : 'Loading...'}
              </p>
            </div>
          </div>

          <form onSubmit={handlePay}>
            <div className="form-group">
              <label className="form-label">Merchant ID</label>
              <input
                type="number"
                className="form-input"
                value={merchantId}
                onChange={(e) => setMerchantId(e.target.value)}
                required
              />
              <p className="form-help">Enter target registered merchant ID (e.g. 1)</p>
            </div>

            <div className="form-group">
              <label className="form-label">Amount (USD)</label>
              <input
                type="number"
                step="0.01"
                min="0.01"
                className="form-input"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
                required
              />
            </div>

            <div className="form-group">
              <label className="form-label">Description / Order Reference</label>
              <input
                type="text"
                className="form-input"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                required
              />
            </div>

            <div className="form-group">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.4rem' }}>
                <label className="form-label" style={{ marginBottom: 0 }}>Idempotency-Key (Header)</label>
                <button
                  type="button"
                  className="btn btn-secondary btn-sm"
                  style={{ padding: '0.2rem 0.5rem', fontSize: '0.75rem' }}
                  onClick={handleNewKey}
                >
                  Generate New UUID
                </button>
              </div>
              <input
                type="text"
                className="form-input code-pill"
                value={idempotencyKey}
                onChange={(e) => setIdempotencyKey(e.target.value)}
                required
              />
              <p className="form-help">Unique request identifier enforcing strictly once-only processing.</p>
            </div>

            <div style={{ display: 'flex', gap: '0.75rem' }}>
              <button type="submit" className="btn btn-primary" style={{ flex: 1 }} disabled={loading}>
                {loading ? 'Processing...' : 'Submit Payment'}
              </button>

              <button
                type="button"
                className="btn btn-warning"
                onClick={handleSimulateReplay}
                disabled={loading || !result}
                title="Resends the identical request with unchanged Idempotency-Key"
              >
                Simulate Replay Attack
              </button>
            </div>
          </form>
        </div>

        {/* Live Execution Result & Replay Verification */}
        <div className="card">
          <div className="card-header">
            <div>
              <h2 className="card-title">Transaction Receipt</h2>
              <p className="card-subtitle">Verified cryptographic receipt</p>
            </div>
            {result && <span className={`badge badge-${result.status}`}>{result.status}</span>}
          </div>

          {!result ? (
            <div style={{ textAlign: 'center', padding: '3rem 1rem', color: 'var(--text-muted)' }}>
              <p>No active payment transaction submitted yet.</p>
              <p style={{ fontSize: '0.8rem', marginTop: '0.5rem' }}>Submit the form to inspect response telemetry.</p>
            </div>
          ) : (
            <div>
              <div className="metric-box" style={{ marginBottom: '1.25rem' }}>
                <span className="metric-label">Paid Amount</span>
                <div className="metric-value">${parseFloat(result.amount).toFixed(2)}</div>
                <p className="metric-desc">Status: {result.status}</p>
              </div>

              <div style={{ fontSize: '0.825rem', display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span style={{ color: 'var(--text-muted)' }}>Payment ID:</span>
                  <span className="code-pill">#{result.id}</span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span style={{ color: 'var(--text-muted)' }}>Merchant ID:</span>
                  <span className="code-pill">#{result.merchantId}</span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span style={{ color: 'var(--text-muted)' }}>Correlation ID:</span>
                  <span className="code-pill">{result.correlationId}</span>
                </div>
                <div>
                  <span style={{ color: 'var(--text-muted)', display: 'block', marginBottom: '0.2rem' }}>
                    SHA-256 Tamper-Evident Hash:
                  </span>
                  <span className="code-pill" style={{ wordBreak: 'break-all', display: 'block', fontSize: '0.725rem' }}>
                    {result.tamperHash}
                  </span>
                </div>
              </div>

              {replayHistory.length > 1 && (
                <div className="alert alert-info" style={{ marginTop: '1.25rem' }}>
                  <div>
                    <strong>Replay Verification Successful:</strong>
                    <p style={{ fontSize: '0.8rem', marginTop: '0.25rem' }}>
                      Identical response returned safely. Wallet balance was NOT deducted multiple times.
                    </p>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Replay History Inspector */}
      {replayHistory.length > 0 && (
        <div className="card">
          <div className="card-header">
            <h2 className="card-title">Idempotency & Replay Audit Feed</h2>
            <span className="badge badge-SUCCESS">{replayHistory.length} Invocations Logged</span>
          </div>
          <div className="table-responsive">
            <table className="table">
              <thead>
                <tr>
                  <th>Timestamp</th>
                  <th>Idempotency Key</th>
                  <th>Payment ID</th>
                  <th>Status</th>
                  <th>Latency</th>
                  <th>Security Verification</th>
                </tr>
              </thead>
              <tbody>
                {replayHistory.map((item, idx) => (
                  <tr key={idx}>
                    <td>{item.timestamp}</td>
                    <td className="code-pill">{item.idempotencyKey.substring(0, 18)}...</td>
                    <td>#{item.paymentId}</td>
                    <td><span className={`badge badge-${item.status}`}>{item.status}</span></td>
                    <td>{item.elapsedMs}ms</td>
                    <td>
                      {item.isDuplicate ? (
                        <span className="badge badge-CONFIRMED">REPLAY PREVENTED (CACHED)</span>
                      ) : (
                        <span className="badge badge-TOPUP">FIRST SUBMISSION (ATOMIC)</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
