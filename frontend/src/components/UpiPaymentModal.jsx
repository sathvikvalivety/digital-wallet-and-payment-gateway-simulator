import React, { useState } from 'react';
import { QRCodeSVG } from 'qrcode.react';
import { upiApi } from '../api';

export default function UpiPaymentModal({ isOpen, onClose, onSuccess, initialAmount = '500', purpose = 'TOPUP' }) {
  if (!isOpen) return null;

  const [amount, setAmount] = useState(initialAmount);
  const [note, setNote] = useState('DWPG Digital Wallet Top-up');
  const [step, setStep] = useState('AMOUNT'); // 'AMOUNT' | 'QR' | 'VERIFIED'
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [initiateData, setInitiateData] = useState(null);
  const [utrNumber, setUtrNumber] = useState('');
  const [verifyResult, setVerifyResult] = useState(null);
  const [copied, setCopied] = useState(false);

  const handleGenerateQR = async (e) => {
    e.preventDefault();
    const val = parseFloat(amount);
    if (isNaN(val) || val <= 0) {
      setError('Please enter a valid positive amount.');
      return;
    }

    setLoading(true);
    setError('');
    try {
      const data = await upiApi.initiate(val, note, purpose);
      setInitiateData(data);
      setStep('QR');
    } catch (err) {
      setError(err.message || 'Failed to initiate UPI transaction');
    } finally {
      setLoading(false);
    }
  };

  const handleCopyUpi = () => {
    if (initiateData?.payeeVpa) {
      navigator.clipboard.writeText(initiateData.payeeVpa);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const fillRandomUtr = () => {
    // Generate valid 12-digit random UTR for test/academic review
    const random12 = Math.floor(100000000000 + Math.random() * 900000000000).toString();
    setUtrNumber(random12);
  };

  const handleVerifyUtr = async (e) => {
    e.preventDefault();
    if (!utrNumber || utrNumber.trim().length < 6) {
      setError('Please enter a valid 12-digit UPI UTR number.');
      return;
    }

    setLoading(true);
    setError('');
    try {
      const result = await upiApi.verify(initiateData.referenceId, utrNumber.trim());
      setVerifyResult(result);
      setStep('VERIFIED');
      if (onSuccess) {
        onSuccess(result);
      }
    } catch (err) {
      setError(err.message || 'Failed to verify UTR number.');
    } finally {
      setLoading(false);
    }
  };

  const resetAndClose = () => {
    setStep('AMOUNT');
    setInitiateData(null);
    setVerifyResult(null);
    setUtrNumber('');
    setError('');
    onClose();
  };

  return (
    <div
      style={{
        position: 'fixed',
        inset: 0,
        backgroundColor: 'rgba(0,0,0,0.6)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 9999,
        padding: '1rem',
      }}
    >
      <div
        className="card"
        style={{
          maxWidth: 480,
          width: '100%',
          maxHeight: '90vh',
          overflowY: 'auto',
          margin: 0,
          boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.3)',
        }}
      >
        <div className="card-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <h3 className="card-title" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <span style={{ fontSize: '1.25rem' }}>⚡</span>
              {purpose === 'TOPUP' ? 'UPI Wallet Recharge' : 'UPI Payment'}
            </h3>
            <p className="card-subtitle">Pay via Google Pay, PhonePe, Paytm, or BHIM</p>
          </div>
          <button
            onClick={resetAndClose}
            style={{
              background: 'none',
              border: 'none',
              fontSize: '1.5rem',
              cursor: 'pointer',
              color: 'var(--text-muted)',
            }}
          >
            ×
          </button>
        </div>

        {error && <div className="alert alert-danger">{error}</div>}

        {/* STEP 1: Enter Amount */}
        {step === 'AMOUNT' && (
          <form onSubmit={handleGenerateQR}>
            <div className="form-group">
              <label className="form-label">Payee Details</label>
              <div
                style={{
                  background: 'var(--bg-muted, #f8fafc)',
                  padding: '0.75rem',
                  borderRadius: '0.5rem',
                  border: '1px solid var(--border)',
                  fontSize: '0.9rem',
                }}
              >
                <div><strong>Payee Name:</strong> sathvikvalivety</div>
                <div><strong>UPI ID:</strong> <code style={{ color: 'var(--primary)' }}>valivetysathvik@ibl</code></div>
              </div>
            </div>

            <div className="form-group">
              <label className="form-label">Amount (₹ INR)</label>
              <input
                type="number"
                step="0.01"
                min="1"
                max="50000"
                className="form-input"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
                placeholder="e.g. 500"
                required
              />
              <div style={{ display: 'flex', gap: '0.5rem', marginTop: '0.5rem', flexWrap: 'wrap' }}>
                {['100', '250', '500', '1000', '2500'].map((val) => (
                  <button
                    key={val}
                    type="button"
                    className="btn btn-secondary btn-sm"
                    onClick={() => setAmount(val)}
                  >
                    ₹{val}
                  </button>
                ))}
              </div>
            </div>

            <div className="form-group">
              <label className="form-label">Transaction Purpose / Note</label>
              <input
                type="text"
                className="form-input"
                value={note}
                onChange={(e) => setNote(e.target.value)}
                placeholder="Transaction description"
              />
            </div>

            <button type="submit" className="btn btn-primary btn-block" disabled={loading}>
              {loading ? 'Generating QR Code...' : 'Generate Dynamic UPI QR Code'}
            </button>
          </form>
        )}

        {/* STEP 2: Show QR Code & UTR input */}
        {step === 'QR' && initiateData && (
          <div>
            <div
              style={{
                textAlign: 'center',
                padding: '1rem',
                background: '#ffffff',
                borderRadius: '0.75rem',
                border: '1px solid var(--border)',
                marginBottom: '1rem',
              }}
            >
              <div style={{ display: 'inline-block', padding: '0.5rem', background: '#ffffff', borderRadius: '0.5rem' }}>
                <QRCodeSVG
                  value={initiateData.upiUri}
                  size={200}
                  level="H"
                  includeMargin={true}
                />
              </div>
              <div style={{ marginTop: '0.5rem', fontSize: '1.25rem', fontWeight: 'bold', color: 'var(--text-color)' }}>
                ₹{parseFloat(initiateData.amount).toFixed(2)}
              </div>
              <div style={{ fontSize: '0.85rem', color: '#64748b', marginTop: '0.25rem' }}>
                Scan with GPay / PhonePe / Paytm / BHIM
              </div>
            </div>

            <div
              style={{
                background: 'var(--bg-muted, #f8fafc)',
                padding: '0.75rem',
                borderRadius: '0.5rem',
                border: '1px solid var(--border)',
                fontSize: '0.85rem',
                marginBottom: '1rem',
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                  <strong>UPI ID:</strong> <code>{initiateData.payeeVpa}</code>
                </div>
                <button
                  type="button"
                  onClick={handleCopyUpi}
                  className="btn btn-secondary btn-sm"
                  style={{ padding: '0.2rem 0.5rem', fontSize: '0.75rem' }}
                >
                  {copied ? '✓ Copied' : 'Copy'}
                </button>
              </div>
              <div style={{ marginTop: '0.25rem' }}>
                <strong>Ref ID:</strong> <code>{initiateData.referenceId}</code>
              </div>
            </div>

            <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '1rem' }}>
              <a
                href={initiateData.upiUri}
                className="btn btn-secondary btn-block"
                style={{ textAlign: 'center', textDecoration: 'none' }}
              >
                📲 Open in UPI App
              </a>
            </div>

            <form onSubmit={handleVerifyUtr} style={{ borderTop: '1px solid var(--border)', paddingTop: '1rem' }}>
              <div className="form-group">
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.25rem' }}>
                  <label className="form-label" style={{ margin: 0 }}>
                    Enter 12-Digit Bank UTR / Ref No
                  </label>
                  <button
                    type="button"
                    onClick={fillRandomUtr}
                    style={{
                      background: 'none',
                      border: 'none',
                      color: 'var(--primary)',
                      fontSize: '0.75rem',
                      cursor: 'pointer',
                      fontWeight: 600,
                    }}
                  >
                    🎲 Fill Test UTR
                  </button>
                </div>
                <input
                  type="text"
                  maxLength="20"
                  className="form-input"
                  value={utrNumber}
                  onChange={(e) => setUtrNumber(e.target.value)}
                  placeholder="e.g. 428192847192"
                  required
                />
                <small style={{ color: 'var(--text-muted)', fontSize: '0.75rem' }}>
                  Found on your GPay/PhonePe/Paytm transaction confirmation screen.
                </small>
              </div>

              <div style={{ display: 'flex', gap: '0.5rem' }}>
                <button
                  type="button"
                  className="btn btn-secondary"
                  onClick={() => setStep('AMOUNT')}
                  disabled={loading}
                >
                  Back
                </button>
                <button type="submit" className="btn btn-primary" style={{ flex: 1 }} disabled={loading}>
                  {loading ? 'Verifying...' : 'Verify & Complete Payment'}
                </button>
              </div>
            </form>
          </div>
        )}

        {/* STEP 3: Payment Verified Success */}
        {step === 'VERIFIED' && verifyResult && (
          <div style={{ textAlign: 'center', padding: '1rem 0' }}>
            <div style={{ fontSize: '3rem', color: '#16a34a', marginBottom: '0.5rem' }}>✓</div>
            <h4 style={{ margin: '0 0 0.5rem 0', color: '#16a34a' }}>Payment Verified Successfully!</h4>
            <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)', marginBottom: '1.5rem' }}>
              {verifyResult.message}
            </p>

            <div
              style={{
                background: 'var(--bg-muted, #f8fafc)',
                padding: '1rem',
                borderRadius: '0.5rem',
                border: '1px solid var(--border)',
                textAlign: 'left',
                fontSize: '0.85rem',
                marginBottom: '1.5rem',
              }}
            >
              <div><strong>Amount Credited:</strong> ₹{parseFloat(verifyResult.amount).toFixed(2)}</div>
              <div><strong>UTR Number:</strong> <code>{verifyResult.utrNumber}</code></div>
              <div><strong>Reference ID:</strong> <code>{verifyResult.referenceId}</code></div>
              {verifyResult.newWalletBalance !== undefined && (
                <div style={{ marginTop: '0.5rem', paddingTop: '0.5rem', borderTop: '1px solid var(--border)' }}>
                  <strong>New Wallet Balance:</strong>{' '}
                  <span style={{ color: 'var(--primary)', fontWeight: 'bold' }}>
                    ${parseFloat(verifyResult.newWalletBalance).toFixed(2)}
                  </span>
                </div>
              )}
            </div>

            <button type="button" className="btn btn-primary btn-block" onClick={resetAndClose}>
              Done
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
