import React, { useState, useEffect } from 'react';
import { QRCodeSVG } from 'qrcode.react';
import { checkoutApi } from '../api';

export default function HostedCheckoutView({ sessionId: initialSessionId }) {
  const [sessionId, setSessionId] = useState(initialSessionId || '');
  const [session, setSession] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [activeMethod, setActiveMethod] = useState('UPI'); // 'UPI' | 'CARD' | 'WALLET'
  const [processing, setProcessing] = useState(false);
  const [result, setResult] = useState(null);
  const [redirectCountdown, setRedirectCountdown] = useState(null);

  // UPI State
  const [utrNumber, setUtrNumber] = useState('');
  const [upiUri, setUpiUri] = useState('');

  // Card State
  const [cardNumber, setCardNumber] = useState('');
  const [cardExpiry, setCardExpiry] = useState('');
  const [cardCvv, setCardCvv] = useState('');

  const payeeVpa = 'valivetysathvik@ibl';
  const payeeName = 'sathvikvalivety';

  useEffect(() => {
    // If sessionId not passed as prop, inspect query params
    if (!sessionId) {
      const params = new URLSearchParams(window.location.search);
      const s = params.get('session') || params.get('session_id');
      if (s) {
        setSessionId(s);
      } else {
        setError('No checkout session ID provided.');
        setLoading(false);
        return;
      }
    }
  }, [sessionId]);

  useEffect(() => {
    if (!sessionId) return;
    const fetchSession = async () => {
      setLoading(true);
      setError('');
      try {
        const data = await checkoutApi.getSession(sessionId);
        setSession(data);
        if (data.status === 'COMPLETED') {
          setResult({
            success: true,
            status: 'COMPLETED',
            orderId: data.orderId,
            amount: data.amount,
            currency: data.currency,
            redirectUrl: data.returnUrl + (data.returnUrl.includes('?') ? '&' : '?') + 'orderId=' + encodeURIComponent(data.orderId) + '&status=SUCCESS&sessionId=' + data.sessionId,
            message: 'Payment was already completed for this order.',
            paymentReference: data.paymentReference,
          });
        } else {
          // Construct NPCI UPI URI
          const note = encodeURIComponent(`Order ${data.orderId} - ${data.merchantBusinessName}`);
          const uri = `upi://pay?pa=${encodeURIComponent(payeeVpa)}&pn=${encodeURIComponent(payeeName)}&am=${parseFloat(data.amount).toFixed(2)}&cu=${data.currency || 'INR'}&tn=${note}&tr=${encodeURIComponent(data.sessionId)}`;
          setUpiUri(uri);
        }
      } catch (err) {
        setError(err.message || 'Failed to load checkout session');
      } finally {
        setLoading(false);
      }
    };
    fetchSession();
  }, [sessionId]);

  // Handle countdown when payment completes
  useEffect(() => {
    if (result && result.redirectUrl && redirectCountdown === null) {
      setRedirectCountdown(4);
    }
  }, [result, redirectCountdown]);

  useEffect(() => {
    if (redirectCountdown === null) return;
    if (redirectCountdown <= 0) {
      if (result?.redirectUrl) {
        window.location.href = result.redirectUrl;
      }
      return;
    }
    const timer = setTimeout(() => {
      setRedirectCountdown((prev) => (prev > 0 ? prev - 1 : 0));
    }, 1000);
    return () => clearTimeout(timer);
  }, [redirectCountdown, result]);

  const handleCompleteUpi = async (customUtr = null) => {
    const finalUtr = customUtr || utrNumber;
    if (!finalUtr || finalUtr.trim().length < 6) {
      setError('Please enter a valid 12-digit UPI UTR number.');
      return;
    }

    setProcessing(true);
    setError('');
    try {
      const res = await checkoutApi.completeSession(sessionId, {
        paymentMethod: 'UPI',
        utrNumber: finalUtr.trim(),
      });
      setResult(res);
    } catch (err) {
      setError(err.message || 'Failed to complete UPI payment');
    } finally {
      setProcessing(false);
    }
  };

  const handleSimulateBankCallback = () => {
    const randomUtr = Math.floor(428000000000 + Math.random() * 9999999999).toString();
    setUtrNumber(randomUtr);
    handleCompleteUpi(randomUtr);
  };

  const handleCompleteCard = async (e) => {
    e.preventDefault();
    if (!cardNumber || cardNumber.replace(/\s/g, '').length < 15) {
      setError('Please enter a valid 16-digit card number.');
      return;
    }

    setProcessing(true);
    setError('');
    try {
      const res = await checkoutApi.completeSession(sessionId, {
        paymentMethod: 'CARD',
        cardNumber: cardNumber.replace(/\s/g, ''),
        cardExpiry,
        cardCvv,
      });
      setResult(res);
    } catch (err) {
      setError(err.message || 'Card payment processing failed');
    } finally {
      setProcessing(false);
    }
  };

  const fillTestCard = () => {
    setCardNumber('4532 8923 1184 9021');
    setCardExpiry('12/28');
    setCardCvv('892');
  };

  if (loading) {
    return (
      <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: '#f1f5f9' }}>
        <div style={{ textAlign: 'center', padding: '2rem' }}>
          <div style={{ fontSize: '2rem', marginBottom: '1rem' }}>⚡</div>
          <h3>Connecting to DWPG Secure Gateway...</h3>
          <p style={{ color: '#64748b' }}>Verifying checkout session #{sessionId}</p>
        </div>
      </div>
    );
  }

  if (error && !session) {
    return (
      <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: '#f1f5f9' }}>
        <div className="card" style={{ maxWidth: 480, textAlign: 'center', padding: '2rem' }}>
          <div style={{ fontSize: '2.5rem', color: '#ef4444', marginBottom: '1rem' }}>⚠️</div>
          <h3 style={{ color: '#ef4444' }}>Invalid Checkout Session</h3>
          <p style={{ color: '#64748b', marginBottom: '1.5rem' }}>{error}</p>
          <a href="/" className="btn btn-secondary">Return Home</a>
        </div>
      </div>
    );
  }

  // SUCCESS / REDIRECT SCREEN
  if (result) {
    return (
      <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: '#f8fafc', padding: '1rem' }}>
        <div className="card" style={{ maxWidth: 520, width: '100%', textAlign: 'center', padding: '2.5rem', boxShadow: '0 20px 25px -5px rgba(0,0,0,0.1)' }}>
          <div style={{ width: 64, height: 64, background: '#dcfce7', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 1.5rem auto' }}>
            <span style={{ fontSize: '2rem', color: '#16a34a' }}>✓</span>
          </div>
          <h2 style={{ color: '#16a34a', margin: '0 0 0.5rem 0' }}>Payment Successful!</h2>
          <p style={{ color: '#64748b', fontSize: '0.95rem', marginBottom: '1.5rem' }}>
            {result.message || 'Your payment has been settled successfully.'}
          </p>

          <div style={{ background: '#f8fafc', border: '1px solid #e2e8f0', borderRadius: '0.5rem', padding: '1rem', textAlign: 'left', fontSize: '0.875rem', marginBottom: '1.5rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
              <span style={{ color: '#64748b' }}>Merchant:</span>
              <strong>{session?.merchantBusinessName}</strong>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
              <span style={{ color: '#64748b' }}>Order ID:</span>
              <code>{result.orderId}</code>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
              <span style={{ color: '#64748b' }}>Amount Paid:</span>
              <strong style={{ color: '#16a34a', fontSize: '1.1rem' }}>₹{parseFloat(result.amount).toFixed(2)}</strong>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <span style={{ color: '#64748b' }}>Payment Ref:</span>
              <code>{result.paymentReference}</code>
            </div>
          </div>

          <div style={{ marginBottom: '1.5rem' }}>
            <p style={{ color: '#0284c7', fontSize: '0.9rem', fontWeight: 500, margin: 0 }}>
              🔄 Automatically returning to merchant in <strong>{redirectCountdown}</strong> seconds...
            </p>
          </div>

          <a
            href={result.redirectUrl}
            className="btn btn-primary btn-block"
            style={{ textDecoration: 'none', display: 'block', padding: '0.75rem' }}
          >
            Return to Merchant Store Now →
          </a>
        </div>
      </div>
    );
  }

  // MAIN HOSTED CHECKOUT SCREEN
  return (
    <div style={{ minHeight: '100vh', background: '#f1f5f9', padding: '2rem 1rem' }}>
      <div style={{ maxWidth: 860, margin: '0 auto' }}>
        {/* Gateway Security Header */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem', padding: '0 0.5rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <div style={{ width: 36, height: 36, borderRadius: '0.5rem', background: '#4f46e5', color: '#fff', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 'bold' }}>
              DW
            </div>
            <div>
              <h3 style={{ margin: 0, fontSize: '1.1rem' }}>DWPG Secure Checkout</h3>
              <p style={{ margin: 0, fontSize: '0.75rem', color: '#64748b' }}>Encrypted & Verified Payment Gateway</p>
            </div>
          </div>
          <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
            <span style={{ fontSize: '0.75rem', background: '#ecfdf5', color: '#065f46', padding: '0.25rem 0.6rem', borderRadius: '1rem', border: '1px solid #a7f3d0' }}>
              🔒 256-Bit SSL
            </span>
          </div>
        </div>

        {error && <div className="alert alert-danger" style={{ marginBottom: '1rem' }}>{error}</div>}

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1.25fr', gap: '1.5rem', alignItems: 'start' }}>
          {/* LEFT: Order Summary */}
          <div className="card" style={{ margin: 0 }}>
            <div style={{ borderBottom: '1px solid var(--border)', paddingBottom: '1rem', marginBottom: '1rem' }}>
              <span style={{ fontSize: '0.75rem', textTransform: 'uppercase', color: '#64748b', fontWeight: 600 }}>
                Merchant
              </span>
              <h2 style={{ margin: '0.25rem 0 0 0', fontSize: '1.35rem' }}>{session.merchantBusinessName}</h2>
              <span style={{ fontSize: '0.8rem', color: '#16a34a' }}>✓ Verified Merchant Partner</span>
            </div>

            <div style={{ marginBottom: '1.5rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                <span style={{ color: '#475569' }}>Order ID:</span>
                <code>{session.orderId}</code>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                <span style={{ color: '#475569' }}>Item:</span>
                <strong>{session.productName}</strong>
              </div>
              {session.customerName && (
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                  <span style={{ color: '#475569' }}>Customer:</span>
                  <span>{session.customerName}</span>
                </div>
              )}
            </div>

            <div style={{ background: '#f8fafc', padding: '1rem', borderRadius: '0.5rem', border: '1px solid var(--border)' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ fontSize: '1rem', fontWeight: 600 }}>Total Due</span>
                <span style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#4f46e5' }}>
                  ₹{parseFloat(session.amount).toFixed(2)}
                </span>
              </div>
              <small style={{ color: '#64748b', display: 'block', marginTop: '0.25rem' }}>
                Includes all applicable taxes & gateway fees
              </small>
            </div>

            <div style={{ marginTop: '1.5rem', textAlign: 'center' }}>
              <a
                href={session.cancelUrl || session.returnUrl}
                style={{ fontSize: '0.85rem', color: '#64748b', textDecoration: 'none' }}
              >
                ← Cancel and return to store
              </a>
            </div>
          </div>

          {/* RIGHT: Payment Methods */}
          <div className="card" style={{ margin: 0 }}>
            {/* Tabs */}
            <div style={{ display: 'flex', gap: '0.5rem', borderBottom: '1px solid var(--border)', paddingBottom: '0.75rem', marginBottom: '1.25rem' }}>
              <button
                type="button"
                className={`btn btn-sm ${activeMethod === 'UPI' ? 'btn-primary' : 'btn-secondary'}`}
                onClick={() => setActiveMethod('UPI')}
              >
                ⚡ UPI QR / Intent
              </button>
              <button
                type="button"
                className={`btn btn-sm ${activeMethod === 'CARD' ? 'btn-primary' : 'btn-secondary'}`}
                onClick={() => setActiveMethod('CARD')}
              >
                💳 Credit / Debit Card
              </button>
            </div>

            {/* UPI TAB */}
            {activeMethod === 'UPI' && (
              <div>
                <div style={{ textAlign: 'center', background: '#fff', padding: '1rem', borderRadius: '0.5rem', border: '1px solid var(--border)', marginBottom: '1rem' }}>
                  <div style={{ display: 'inline-block', padding: '0.5rem', background: '#fff', borderRadius: '0.5rem' }}>
                    <QRCodeSVG value={upiUri} size={180} level="H" includeMargin={true} />
                  </div>
                  <div style={{ marginTop: '0.5rem', fontSize: '1.2rem', fontWeight: 'bold', color: '#1e293b' }}>
                    ₹{parseFloat(session.amount).toFixed(2)}
                  </div>
                  <div style={{ fontSize: '0.8rem', color: '#64748b' }}>
                    Scan with GPay, PhonePe, Paytm, or BHIM
                  </div>
                </div>

                <div style={{ background: '#f8fafc', padding: '0.75rem', borderRadius: '0.5rem', border: '1px solid var(--border)', fontSize: '0.85rem', marginBottom: '1rem' }}>
                  <div><strong>Payee UPI ID:</strong> <code>{payeeVpa}</code></div>
                  <div style={{ marginTop: '0.2rem' }}><strong>Payee Name:</strong> {payeeName}</div>
                </div>

                <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '0.75rem' }}>
                  <a
                    href={upiUri}
                    className="btn btn-secondary btn-block"
                    style={{ textAlign: 'center', textDecoration: 'none' }}
                  >
                    📲 Open in UPI App
                  </a>
                </div>

                <button
                  type="button"
                  className="btn btn-block"
                  style={{
                    backgroundColor: '#f59e0b',
                    color: '#fff',
                    border: 'none',
                    fontWeight: 600,
                    marginBottom: '1rem',
                    padding: '0.65rem',
                    borderRadius: '0.375rem',
                    cursor: 'pointer',
                  }}
                  onClick={handleSimulateBankCallback}
                  disabled={processing}
                >
                  ⚡ {processing ? 'Verifying...' : 'Simulate Bank Callback (Instant Auto-Verify)'}
                </button>

                <div style={{ borderTop: '1px solid var(--border)', paddingTop: '1rem' }}>
                  <label className="form-label" style={{ fontSize: '0.85rem' }}>
                    Or Enter 12-Digit Bank UTR / Reference
                  </label>
                  <div style={{ display: 'flex', gap: '0.5rem' }}>
                    <input
                      type="text"
                      className="form-input"
                      placeholder="e.g. 428192847192"
                      value={utrNumber}
                      onChange={(e) => setUtrNumber(e.target.value)}
                    />
                    <button
                      type="button"
                      className="btn btn-primary"
                      onClick={() => handleCompleteUpi()}
                      disabled={processing}
                    >
                      Verify
                    </button>
                  </div>
                </div>
              </div>
            )}

            {/* CARD TAB */}
            {activeMethod === 'CARD' && (
              <form onSubmit={handleCompleteCard}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                  <label className="form-label" style={{ margin: 0 }}>Card Details</label>
                  <button
                    type="button"
                    onClick={fillTestCard}
                    style={{ background: 'none', border: 'none', color: 'var(--primary)', fontSize: '0.75rem', cursor: 'pointer', fontWeight: 600 }}
                  >
                    🎲 Fill Test Card
                  </button>
                </div>

                <div className="form-group">
                  <label className="form-label" style={{ fontSize: '0.8rem' }}>Card Number</label>
                  <input
                    type="text"
                    className="form-input"
                    placeholder="4532 8923 1184 9021"
                    value={cardNumber}
                    onChange={(e) => setCardNumber(e.target.value)}
                    required
                  />
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.75rem' }}>
                  <div className="form-group">
                    <label className="form-label" style={{ fontSize: '0.8rem' }}>Expiry (MM/YY)</label>
                    <input
                      type="text"
                      className="form-input"
                      placeholder="12/28"
                      value={cardExpiry}
                      onChange={(e) => setCardExpiry(e.target.value)}
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label className="form-label" style={{ fontSize: '0.8rem' }}>CVV</label>
                    <input
                      type="password"
                      maxLength="4"
                      className="form-input"
                      placeholder="892"
                      value={cardCvv}
                      onChange={(e) => setCardCvv(e.target.value)}
                      required
                    />
                  </div>
                </div>

                <button
                  type="submit"
                  className="btn btn-primary btn-block"
                  disabled={processing}
                  style={{ marginTop: '0.5rem' }}
                >
                  {processing ? 'Authorizing Payment...' : `Pay ₹${parseFloat(session.amount).toFixed(2)}`}
                </button>
              </form>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
