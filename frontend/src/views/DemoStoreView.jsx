import React, { useState, useEffect } from 'react';
import { checkoutApi, merchantApi } from '../api';

export default function DemoStoreView() {
  const [apiKey, setApiKey] = useState('');
  const [customerName, setCustomerName] = useState('Alice Wonder');
  const [customerEmail, setCustomerEmail] = useState('alice.wonder@example.com');
  const [amount, setAmount] = useState('799.00');
  const [productName, setProductName] = useState('Sony WH-1000XM5 Pro Wireless Headphones');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [merchantLoaded, setMerchantLoaded] = useState(false);

  // Check if returning from a successful payment
  const [orderResult, setOrderResult] = useState(null);

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const status = params.get('status');
    const orderId = params.get('orderId');
    const sessionId = params.get('sessionId');
    const paidAmount = params.get('amount');
    const ref = params.get('ref');

    if (status === 'SUCCESS' && orderId) {
      setOrderResult({
        orderId,
        sessionId,
        amount: paidAmount,
        ref,
      });
    }

    // Try to auto-populate the logged-in merchant's API key
    const fetchMyKey = async () => {
      try {
        const m = await merchantApi.getMyMerchant();
        if (m && m.apiKey) {
          setApiKey(m.apiKey);
          setMerchantLoaded(true);
        }
      } catch {
        // user might not be a registered merchant yet
      }
    };
    fetchMyKey();
  }, []);

  const handleCheckout = async (e) => {
    e.preventDefault();
    if (!apiKey || apiKey.trim().length < 5) {
      setError('Please provide a valid Merchant API Key (e.g. from the Merchant tab).');
      return;
    }

    setLoading(true);
    setError('');

    const generatedOrderId = 'ORD-' + Math.floor(100000 + Math.random() * 900000);
    const returnUrl = `${window.location.origin}/?tab=demo-store&order=success`;
    const cancelUrl = `${window.location.origin}/?tab=demo-store&order=cancel`;

    try {
      const session = await checkoutApi.createSession(apiKey.trim(), {
        amount: parseFloat(amount),
        currency: 'INR',
        orderId: generatedOrderId,
        productName,
        customerName,
        customerEmail,
        returnUrl,
        cancelUrl,
      });

      // Redirect browser to Hosted Checkout Page!
      window.location.href = session.checkoutUrl;
    } catch (err) {
      setError(err.message || 'Failed to initialize checkout session with DWPG Gateway');
      setLoading(false);
    }
  };

  const handleClearOrderResult = () => {
    setOrderResult(null);
    window.history.replaceState({}, document.title, window.location.pathname);
  };

  return (
    <div style={{ maxWidth: 880, margin: '0 auto', paddingBottom: '2rem' }}>
      {/* Banner */}
      <div className="security-banner" style={{ background: 'linear-gradient(135deg, #1e293b 0%, #0f172a 100%)' }}>
        <div>
          <h3>🛒 External E-Commerce Project Integration Demo</h3>
          <p style={{ fontSize: '0.85rem', opacity: 0.9 }}>
            This simulates an external e-commerce website (like Shopify, WooCommerce, or custom Next.js/Django store) using your DWPG API Key to redirect payments to your gateway.
          </p>
        </div>
        <div className="security-badges">
          <span className="sec-badge">🔑 API Key Auth</span>
          <span className="sec-badge">🔄 Seamless Redirect</span>
        </div>
      </div>

      {/* Return from payment confirmation */}
      {orderResult && (
        <div
          style={{
            background: '#ecfdf5',
            border: '2px solid #10b981',
            borderRadius: '0.75rem',
            padding: '1.5rem',
            marginBottom: '1.5rem',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.75rem' }}>
            <span style={{ fontSize: '1.75rem' }}>🎉</span>
            <div>
              <h3 style={{ margin: 0, color: '#065f46' }}>Order Confirmed & Paid via DWPG Gateway!</h3>
              <p style={{ margin: 0, color: '#047857', fontSize: '0.85rem' }}>
                DWPG redirected customer back to external store callback URL
              </p>
            </div>
          </div>
          <div style={{ background: '#fff', padding: '1rem', borderRadius: '0.5rem', fontSize: '0.875rem' }}>
            <div><strong>Order ID:</strong> <code>{orderResult.orderId}</code></div>
            <div><strong>Session ID:</strong> <code>{orderResult.sessionId}</code></div>
            {orderResult.amount && <div><strong>Amount Settled:</strong> ₹{orderResult.amount}</div>}
            {orderResult.ref && <div><strong>Payment Ref:</strong> <code>{orderResult.ref}</code></div>}
          </div>
          <button
            type="button"
            className="btn btn-secondary btn-sm"
            style={{ marginTop: '0.75rem' }}
            onClick={handleClearOrderResult}
          >
            Start New Test Order
          </button>
        </div>
      )}

      {error && <div className="alert alert-danger">{error}</div>}

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem', alignItems: 'start' }}>
        {/* Left: Product Card */}
        <div className="card" style={{ margin: 0 }}>
          <div className="card-header">
            <div>
              <span style={{ fontSize: '0.75rem', color: '#64748b', textTransform: 'uppercase', fontWeight: 600 }}>
                Demo Store Item
              </span>
              <h3 className="card-title" style={{ marginTop: '0.25rem' }}>{productName}</h3>
            </div>
            <span className="badge badge-ACTIVE">In Stock</span>
          </div>

          <div
            style={{
              height: 180,
              background: 'linear-gradient(135deg, #e2e8f0 0%, #cbd5e1 100%)',
              borderRadius: '0.5rem',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '4rem',
              marginBottom: '1rem',
            }}
          >
            🎧
          </div>

          <p style={{ fontSize: '0.9rem', color: '#475569', marginBottom: '1rem' }}>
            Industry-leading noise canceling with Auto NC Optimizer, crystal clear hands-free calling, and up to 30-hour battery life.
          </p>

          <div style={{ background: '#f8fafc', padding: '0.75rem 1rem', borderRadius: '0.5rem', border: '1px solid var(--border)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span style={{ fontWeight: 600 }}>Price</span>
            <span style={{ fontSize: '1.4rem', fontWeight: 'bold', color: '#16a34a' }}>₹{amount}</span>
          </div>
        </div>

        {/* Right: Integration Configuration & Checkout Form */}
        <div className="card" style={{ margin: 0 }}>
          <div className="card-header">
            <div>
              <h3 className="card-title">External Store Checkout</h3>
              <p className="card-subtitle">Connects to DWPG Gateway API with your key</p>
            </div>
          </div>

          <form onSubmit={handleCheckout}>
            <div className="form-group">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.25rem' }}>
                <label className="form-label" style={{ margin: 0 }}>Merchant API Key</label>
                {merchantLoaded && (
                  <span style={{ fontSize: '0.75rem', color: '#16a34a', fontWeight: 600 }}>
                    ✓ Loaded from your account
                  </span>
                )}
              </div>
              <input
                type="text"
                className="form-input"
                placeholder="dwpg_live_xxxxxxxxxxxxxxxx"
                value={apiKey}
                onChange={(e) => setApiKey(e.target.value)}
                required
              />
              <small style={{ color: '#64748b', fontSize: '0.75rem' }}>
                Found in your DWPG <strong>Merchant Portal</strong>.
              </small>
            </div>

            <div className="form-group">
              <label className="form-label">Customer Name</label>
              <input
                type="text"
                className="form-input"
                value={customerName}
                onChange={(e) => setCustomerName(e.target.value)}
                required
              />
            </div>

            <div className="form-group">
              <label className="form-label">Customer Email</label>
              <input
                type="email"
                className="form-input"
                value={customerEmail}
                onChange={(e) => setCustomerEmail(e.target.value)}
                required
              />
            </div>

            <div className="form-group">
              <label className="form-label">Amount (₹)</label>
              <input
                type="number"
                step="0.01"
                className="form-input"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
                required
              />
            </div>

            <button
              type="submit"
              className="btn btn-primary btn-block"
              disabled={loading}
              style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem', padding: '0.75rem', fontSize: '1rem' }}
            >
              ⚡ {loading ? 'Redirecting to Gateway...' : 'Pay with DWPG Gateway →'}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
