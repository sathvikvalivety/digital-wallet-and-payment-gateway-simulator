import React, { useState, useEffect } from 'react';
import { adminApi } from '../api';

export default function AdminAuditView() {
  const [logs, setLogs] = useState([]);
  const [selectedAction, setSelectedAction] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const loadLogs = async (actionFilter = null) => {
    setLoading(true);
    setError('');
    try {
      const data = await adminApi.getAuditLogs(actionFilter);
      setLogs(data);
    } catch (err) {
      setError(err.message || 'Failed to fetch admin audit logs');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadLogs(selectedAction || null);
  }, [selectedAction]);

  const auditActions = [
    { label: 'All Actions', value: '' },
    { label: 'Login Success', value: 'LOGIN_SUCCESS' },
    { label: 'Login Failure', value: 'LOGIN_FAILURE' },
    { label: 'Authorization Failure', value: 'AUTHORIZATION_FAILURE' },
    { label: 'Wallet Created', value: 'WALLET_CREATED' },
    { label: 'Funds Added', value: 'FUNDS_ADDED' },
    { label: 'Payment Initiated', value: 'PAYMENT_INITIATED' },
    { label: 'Payment Confirmed', value: 'PAYMENT_CONFIRMED' },
    { label: 'Payment Refunded', value: 'PAYMENT_REFUNDED' },
    { label: 'Payment Failed', value: 'PAYMENT_FAILED' },
    { label: 'Replay Detected', value: 'REPLAY_DETECTED' },
    { label: 'Duplicate Payment', value: 'DUPLICATE_PAYMENT' },
    { label: 'Suspicious Activity', value: 'SUSPICIOUS_ACTIVITY' },
  ];

  const displayedLogs = selectedAction
    ? logs.filter((l) => (l.eventType || l.action || '') === selectedAction)
    : logs;

  return (
    <div>
      <div className="security-banner">
        <div>
          <h3>SIEM & Forensic Security Audit Explorer</h3>
          <p style={{ fontSize: '0.85rem', opacity: 0.9 }}>
            Immutable administrative stream recording all authentication, financial mutations, and adversarial replay attempts.
          </p>
        </div>
        <div className="security-badges">
          <span className="sec-badge">🚨 Threat Detection</span>
          <span className="sec-badge">📜 SIEM Ready</span>
          <span className="sec-badge">🔒 SOC2 Compliant</span>
        </div>
      </div>

      {error && <div className="alert alert-danger">{error}</div>}

      <div className="card">
        <div className="card-header">
          <div>
            <h2 className="card-title">Security Event Audit Trail</h2>
            <p className="card-subtitle">Showing {displayedLogs.length} logged administrative events</p>
          </div>

          <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
            <label style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-muted)' }}>Action Filter:</label>
            <select
              className="form-select"
              style={{ width: 'auto', padding: '0.35rem 0.75rem', fontSize: '0.85rem' }}
              value={selectedAction}
              onChange={(e) => setSelectedAction(e.target.value)}
            >
              {auditActions.map((act) => (
                <option key={act.value} value={act.value}>
                  {act.label}
                </option>
              ))}
            </select>
            <button className="btn btn-secondary btn-sm" onClick={() => loadLogs(selectedAction || null)}>
              Refresh
            </button>
          </div>
        </div>

        {loading ? (
          <p style={{ padding: '2rem', textAlign: 'center' }}>Loading security telemetry...</p>
        ) : displayedLogs.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '3rem 1rem', color: 'var(--text-muted)' }}>
            <p>No audit records found matching the active filter.</p>
          </div>
        ) : (
          <div className="table-responsive">
            <table className="table">
              <thead>
                <tr>
                  <th>Log ID</th>
                  <th>Timestamp</th>
                  <th>Event Type</th>
                  <th>Outcome</th>
                  <th>Actor</th>
                  <th>Resource ID</th>
                  <th>IP Address</th>
                  <th>Forensic Details</th>
                </tr>
              </thead>
              <tbody>
                {displayedLogs.map((log) => {
                  const evType = log.eventType || log.action || 'EVENT';
                  const outcome = log.outcome || log.result || 'SUCCESS';
                  const isAdversarial =
                    evType.includes('REPLAY') ||
                    evType.includes('FAIL') ||
                    evType.includes('SUSPICIOUS') ||
                    outcome === 'FAILURE';

                  return (
                    <tr
                      key={log.id}
                      style={{
                        backgroundColor: isAdversarial ? '#fff1f2' : 'transparent',
                      }}
                    >
                      <td className="code-pill">#{log.id}</td>
                      <td style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                        {new Date(log.createdAt || log.timestamp || Date.now()).toLocaleString()}
                      </td>
                      <td>
                        <span
                          className={`badge ${
                            isAdversarial ? 'badge-FAILED' : 'badge-SUCCESS'
                          }`}
                        >
                          {evType}
                        </span>
                      </td>
                      <td>
                        <span
                          className={`badge ${
                            outcome === 'SUCCESS' ? 'badge-CONFIRMED' : 'badge-FAILED'
                          }`}
                        >
                          {outcome}
                        </span>
                      </td>
                      <td style={{ fontWeight: 600 }}>{log.actorUsername || log.actor || 'SYSTEM'}</td>
                      <td>
                        {log.resourceId ? `#${log.resourceId}` : 'N/A'}
                      </td>
                      <td style={{ fontSize: '0.8rem' }}>{log.ipAddress || '127.0.0.1'}</td>
                      <td style={{ fontSize: '0.75rem', maxWidth: 300, wordBreak: 'break-word' }}>
                        {log.details || '-'}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
