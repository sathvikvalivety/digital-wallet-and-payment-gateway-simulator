import React, { useState, useEffect } from 'react';
import { transactionApi, refundApi } from '../api';

function generateUUID() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
    const r = (Math.random() * 16) | 0;
    const v = c === 'x' ? r : (r & 0x3) | 0x8;
    return v.toString(16);
  });
}

export default function TransactionLedgerView() {
  const [transactions, setTransactions] = useState([]);
  const [filterType, setFilterType] = useState('ALL');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [successMsg, setSuccessMsg] = useState('');

  // Refund Modal State
  const [refundModalOpen, setRefundModalOpen] = useState(false);
  const [selectedTx, setSelectedTx] = useState(null);
  const [refundReason, setRefundReason] = useState('Defective goods / simulator cancellation');
  const [refundIdempotencyKey, setRefundIdempotencyKey] = useState(generateUUID());
  const [refundLoading, setRefundLoading] = useState(false);

  const loadTransactions = async () => {
    setError('');
    try {
      const data = await transactionApi.getMyTransactions();
      setTransactions(data);
    } catch (err) {
      setError(err.message || 'Failed to load transaction ledger');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadTransactions();
  }, []);

  const openRefundModal = (tx) => {
    setSelectedTx(tx);
    setRefundReason('Customer cancellation test');
    setRefundIdempotencyKey(generateUUID());
    setRefundModalOpen(true);
  };

  const closeRefundModal = () => {
    setRefundModalOpen(false);
    setSelectedTx(null);
  };

  const handleProcessRefund = async (e) => {
    e.preventDefault();
    const pid = selectedTx ? (selectedTx.paymentId || selectedTx.referencePaymentId) : null;
    if (!selectedTx || !pid) {
      setError('Cannot refund: Missing payment reference ID');
      return;
    }

    setRefundLoading(true);
    setError('');
    setSuccessMsg('');

    try {
      await refundApi.requestRefund(pid, refundReason, refundIdempotencyKey);
      setSuccessMsg(`Refund successfully processed for Transaction #${selectedTx.id}! Funds restored to wallet.`);
      closeRefundModal();
      await loadTransactions();
    } catch (err) {
      setError(err.message || 'Refund failed');
    } finally {
      setRefundLoading(false);
    }
  };

  const filtered = transactions.filter((tx) => {
    if (filterType === 'ALL') return true;
    return tx.type === filterType;
  });

  if (loading) {
    return <div className="card"><p>Loading ledger entries...</p></div>;
  }

  return (
    <div>
      <div className="security-banner">
        <div>
          <h3>Tamper-Evident Transaction Ledger</h3>
          <p style={{ fontSize: '0.85rem', opacity: 0.9 }}>
            Append-only financial records protected by SHA-256 state hashes and distributed correlation IDs.
          </p>
        </div>
        <div className="security-badges">
          <span className="sec-badge">🔒 Immutable Ledger</span>
          <span className="sec-badge">⛓️ Hash Chained</span>
          <span className="sec-badge">🛡️ Non-Repudiation</span>
        </div>
      </div>

      {error && <div className="alert alert-danger">{error}</div>}
      {successMsg && <div className="alert alert-success">{successMsg}</div>}

      <div className="card">
        <div className="card-header">
          <div>
            <h2 className="card-title">Audit Ledger & Transaction History</h2>
            <p className="card-subtitle">Showing {filtered.length} of {transactions.length} total entries</p>
          </div>

          <div style={{ display: 'flex', gap: '0.5rem' }}>
            {['ALL', 'PAYMENT', 'TOPUP', 'REFUND'].map((t) => (
              <button
                key={t}
                className={`btn btn-sm ${filterType === t ? 'btn-primary' : 'btn-secondary'}`}
                onClick={() => setFilterType(t)}
              >
                {t}
              </button>
            ))}
          </div>
        </div>

        {filtered.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '3rem 1rem', color: 'var(--text-muted)' }}>
            <p>No transaction records found matching the active filter.</p>
          </div>
        ) : (
          <div className="table-responsive">
            <table className="table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Type</th>
                  <th>Amount</th>
                  <th>Balance After</th>
                  <th>Status</th>
                  <th>Correlation ID</th>
                  <th>Tamper Hash</th>
                  <th>Timestamp</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                {filtered.map((tx) => (
                  <tr key={tx.id}>
                    <td className="code-pill">#{tx.id}</td>
                    <td>
                      <span className={`badge badge-${tx.type}`}>{tx.type}</span>
                    </td>
                    <td style={{ fontWeight: 600, color: (tx.type === 'TOP_UP' || tx.type === 'TOPUP' || tx.type === 'REFUND' || tx.type === 'CREDIT') ? '#16a34a' : '#dc2626' }}>
                      {(tx.type === 'TOP_UP' || tx.type === 'TOPUP' || tx.type === 'REFUND' || tx.type === 'CREDIT') ? '+' : '-'}₹{parseFloat(tx.amount).toFixed(2)}
                    </td>
                    <td>₹{parseFloat(tx.balanceAfter).toFixed(2)}</td>
                    <td>
                      <span className={`badge badge-${tx.status || 'CONFIRMED'}`}>{tx.status || 'CONFIRMED'}</span>
                    </td>
                    <td className="code-pill" style={{ fontSize: '0.7rem' }}>
                      {tx.correlationId ? tx.correlationId.substring(0, 8) + '...' : 'N/A'}
                    </td>
                    <td className="code-pill" title={tx.tamperHash} style={{ fontSize: '0.65rem' }}>
                      {tx.tamperHash ? tx.tamperHash.substring(0, 10) + '...' : 'VALID'}
                    </td>
                    <td style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                      {new Date(tx.createdAt).toLocaleString()}
                    </td>
                    <td>
                      {(tx.type === 'DEBIT' || tx.type === 'PAYMENT') && (tx.paymentId != null || tx.referencePaymentId != null) && (
                        <button
                          className="btn btn-secondary btn-sm"
                          style={{ fontSize: '0.75rem', padding: '0.2rem 0.5rem' }}
                          onClick={() => openRefundModal(tx)}
                        >
                          Refund
                        </button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Refund Modal */}
      {refundModalOpen && selectedTx && (
        <div className="modal-backdrop">
          <div className="modal-content">
            <div className="card-header">
              <h3 className="card-title">Process Transaction Refund</h3>
              <button
                onClick={closeRefundModal}
                style={{ background: 'none', border: 'none', fontSize: '1.25rem', cursor: 'pointer' }}
              >
                ✕
              </button>
            </div>

            <p style={{ fontSize: '0.875rem', color: 'var(--text-muted)', marginBottom: '1rem' }}>
              Refunding Transaction #{selectedTx.id} (Payment #{selectedTx.referencePaymentId}) of{' '}
              <strong>₹{parseFloat(selectedTx.amount).toFixed(2)}</strong>.
            </p>

            <form onSubmit={handleProcessRefund}>
              <div className="form-group">
                <label className="form-label">Refund Reason</label>
                <input
                  type="text"
                  className="form-input"
                  value={refundReason}
                  onChange={(e) => setRefundReason(e.target.value)}
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label">Idempotency Key (Refund)</label>
                <input
                  type="text"
                  className="form-input code-pill"
                  value={refundIdempotencyKey}
                  onChange={(e) => setRefundIdempotencyKey(e.target.value)}
                  required
                />
                <p className="form-help">Prevents double-refunding if network times out.</p>
              </div>

              <div style={{ display: 'flex', gap: '0.75rem', justifyContent: 'flex-end', marginTop: '1.5rem' }}>
                <button type="button" className="btn btn-secondary" onClick={closeRefundModal}>
                  Cancel
                </button>
                <button type="submit" className="btn btn-danger" disabled={refundLoading}>
                  {refundLoading ? 'Processing Refund...' : 'Confirm Refund'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
