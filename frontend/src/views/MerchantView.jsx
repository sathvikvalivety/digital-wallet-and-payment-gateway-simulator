import React, { useState, useEffect } from 'react';
import { merchantApi } from '../api';

export default function MerchantView({ onOpenDemoStore }) {
  const [merchant, setMerchant] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [businessName, setBusinessName] = useState('');
  const [actionLoading, setActionLoading] = useState(false);
  const [successMsg, setSuccessMsg] = useState('');
  const [showApiKey, setShowApiKey] = useState(false);
  const [copiedKey, setCopiedKey] = useState(false);
  const [activeTab, setActiveTab] = useState('OVERVIEW'); // 'OVERVIEW' | 'DOCS' | 'TEST'
  const [selectedLang, setSelectedLang] = useState('NODE'); // 'NODE' | 'PYTHON' | 'CURL'

  const loadMerchant = async () => {
    setError('');
    try {
      const data = await merchantApi.getMyMerchant();
      setMerchant(data);
    } catch (err) {
      if (err.status === 404) {
        setMerchant(null);
      } else {
        setError(err.message || 'Failed to fetch merchant profile');
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadMerchant();
  }, []);

  const handleRegister = async (e) => {
    e.preventDefault();
    setActionLoading(true);
    setError('');
    setSuccessMsg('');

    try {
      const newMerchant = await merchantApi.register(businessName);
      setMerchant(newMerchant);
      setSuccessMsg('Merchant account registered successfully!');
    } catch (err) {
      setError(err.message || 'Merchant registration failed');
    } finally {
      setActionLoading(false);
    }
  };

  const handleRegenerateKey = async () => {
    if (!window.confirm('Are you sure you want to regenerate your API Key? Any existing integrations using the old key will stop working.')) {
      return;
    }

    setActionLoading(true);
    setError('');
    try {
      const updated = await merchantApi.regenerateApiKey();
      setMerchant(updated);
      setSuccessMsg('New API key generated successfully!');
      setShowApiKey(true);
    } catch (err) {
      setError(err.message || 'Failed to regenerate API key');
    } finally {
      setActionLoading(false);
    }
  };

  const handleCopyKey = () => {
    if (merchant?.apiKey) {
      navigator.clipboard.writeText(merchant.apiKey);
      setCopiedKey(true);
      setTimeout(() => setCopiedKey(false), 2000);
    }
  };

  if (loading) {
    return <div className="card"><p>Loading merchant profile...</p></div>;
  }

  const currentApiKey = merchant?.apiKey || 'dwpg_live_your_api_key_here';

  const snippets = {
    NODE: `// 1. Install & import in your Node.js / Express backend
const DWPG_API_KEY = "${currentApiKey}";
const GATEWAY_URL = "http://localhost:3000/api/checkout/session";

// 2. When customer clicks "Checkout" on your site:
async function createCheckoutSession(orderData) {
  const response = await fetch(GATEWAY_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-Api-Key": DWPG_API_KEY
    },
    body: JSON.stringify({
      amount: orderData.amount, // e.g. 499.00
      currency: "INR",
      orderId: orderData.orderId, // e.g. "ORD-9842"
      productName: orderData.productName,
      customerName: orderData.customerName,
      customerEmail: orderData.customerEmail,
      returnUrl: "https://your-store.com/order-success",
      cancelUrl: "https://your-store.com/cart"
    })
  });

  const session = await response.json();
  // 3. Redirect your user's browser to the hosted checkout:
  // res.redirect(session.checkoutUrl);
  return session.checkoutUrl;
}`,

    PYTHON: `# 1. Import requests in your Django / Flask / FastAPI backend
import requests

DWPG_API_KEY = "${currentApiKey}"
GATEWAY_URL = "http://localhost:3000/api/checkout/session"

def create_checkout_session(order):
    headers = {
        "Content-Type": "application/json",
        "X-Api-Key": DWPG_API_KEY
    }
    payload = {
        "amount": 499.00,
        "currency": "INR",
        "order_id": order["id"],
        "product_name": order["title"],
        "customer_name": "Alice Wonder",
        "customer_email": "alice@example.com",
        "return_url": "https://your-store.com/success",
        "cancel_url": "https://your-store.com/cancel"
    }
    
    response = requests.post(GATEWAY_URL, json=payload, headers=headers)
    session_data = response.json()
    
    # Redirect user to DWPG Hosted Checkout:
    return session_data["checkoutUrl"]`,

    CURL: `# Test session creation via command line
curl -X POST http://localhost:3000/api/checkout/session \\
  -H "Content-Type: application/json" \\
  -H "X-Api-Key: ${currentApiKey}" \\
  -d '{
    "amount": 499.00,
    "currency": "INR",
    "orderId": "ORD-12345",
    "productName": "Pro Gaming Headset",
    "customerName": "John Doe",
    "customerEmail": "john@example.com",
    "returnUrl": "http://localhost:3000/?tab=demo-store&order=success",
    "cancelUrl": "http://localhost:3000/?tab=demo-store&order=cancel"
  }'`
  };

  return (
    <div>
      <div className="security-banner">
        <div>
          <h3>Payment Gateway & Merchant API Hub</h3>
          <p style={{ fontSize: '0.85rem', opacity: 0.9 }}>
            Integrate DWPG into any external website. Provide your API key to redirect customers to your hosted checkout with dynamic UPI QR & Card support.
          </p>
        </div>
        <div className="security-badges">
          <span className="sec-badge">🔑 Merchant API Key</span>
          <span className="sec-badge">🌐 Hosted Checkout</span>
          <span className="sec-badge">⚡ Instant Settlements</span>
        </div>
      </div>

      {error && <div className="alert alert-danger">{error}</div>}
      {successMsg && <div className="alert alert-success">{successMsg}</div>}

      {!merchant ? (
        <div className="card" style={{ maxWidth: 520, margin: '1rem auto' }}>
          <div className="card-header">
            <div>
              <h2 className="card-title">Register Merchant Profile</h2>
              <p className="card-subtitle">Accept payments from external stores and apps</p>
            </div>
          </div>

          <form onSubmit={handleRegister}>
            <div className="form-group">
              <label className="form-label">Business / Store Name</label>
              <input
                type="text"
                className="form-input"
                placeholder="e.g. Acme Tech Stores, Sathvik Electronics"
                value={businessName}
                onChange={(e) => setBusinessName(e.target.value)}
                required
              />
            </div>

            <button type="submit" className="btn btn-primary btn-block" disabled={actionLoading}>
              {actionLoading ? 'Registering...' : 'Provision Merchant Profile & API Key'}
            </button>
          </form>
        </div>
      ) : (
        <div>
          {/* Navigation Tabs */}
          <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '1.25rem' }}>
            <button
              type="button"
              className={`btn ${activeTab === 'OVERVIEW' ? 'btn-primary' : 'btn-secondary'}`}
              onClick={() => setActiveTab('OVERVIEW')}
            >
              📊 Account & API Keys
            </button>
            <button
              type="button"
              className={`btn ${activeTab === 'DOCS' ? 'btn-primary' : 'btn-secondary'}`}
              onClick={() => setActiveTab('DOCS')}
            >
              📖 Integration Guide (Code Snippets)
            </button>
            {onOpenDemoStore && (
              <button
                type="button"
                className="btn btn-secondary"
                style={{ marginLeft: 'auto', background: '#ecfdf5', borderColor: '#a7f3d0', color: '#065f46', fontWeight: 600 }}
                onClick={onOpenDemoStore}
              >
                🛒 Open Demo Store →
              </button>
            )}
          </div>

          {/* TAB 1: OVERVIEW & CREDENTIALS */}
          {activeTab === 'OVERVIEW' && (
            <div className="card">
              <div className="card-header">
                <div>
                  <h2 className="card-title">{merchant.businessName}</h2>
                  <p className="card-subtitle">Merchant Account #{merchant.id}</p>
                </div>
                <span className={`badge badge-${merchant.status}`}>{merchant.status}</span>
              </div>

              <div className="grid-2">
                <div className="metric-box">
                  <span className="metric-label">Merchant Identifier</span>
                  <div className="metric-value">#{merchant.id}</div>
                  <p className="metric-desc">Your unique account ID on DWPG</p>
                </div>

                <div className="metric-box">
                  <span className="metric-label">Settlement Wallet</span>
                  <div className="metric-value" style={{ color: '#16a34a' }}>ACTIVE</div>
                  <p className="metric-desc">Wallet ID #{merchant.walletId} automatically credited</p>
                </div>
              </div>

              {/* API Key Box */}
              <div style={{ marginTop: '1.5rem', background: '#f8fafc', padding: '1.25rem', borderRadius: 'var(--radius)', border: '1px solid var(--border)' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                  <label className="form-label" style={{ marginBottom: 0, fontWeight: 600 }}>
                    Live Merchant API Key (Secret)
                  </label>
                  <div style={{ display: 'flex', gap: '0.5rem' }}>
                    <button
                      type="button"
                      className="btn btn-secondary btn-sm"
                      onClick={() => setShowApiKey(!showApiKey)}
                    >
                      {showApiKey ? 'Hide Key' : 'Reveal Key'}
                    </button>
                    <button
                      type="button"
                      className="btn btn-secondary btn-sm"
                      onClick={handleCopyKey}
                    >
                      {copiedKey ? '✓ Copied' : 'Copy Key'}
                    </button>
                    <button
                      type="button"
                      className="btn btn-secondary btn-sm"
                      style={{ color: '#dc2626' }}
                      onClick={handleRegenerateKey}
                      disabled={actionLoading}
                    >
                      Regenerate
                    </button>
                  </div>
                </div>

                <div className="code-pill" style={{ padding: '0.75rem 1rem', fontSize: '0.9rem', wordBreak: 'break-all', fontFamily: 'monospace' }}>
                  {showApiKey ? merchant.apiKey : '••••••••••••••••••••••••••••••••••••••••••••••••'}
                </div>
                <p className="form-help" style={{ marginTop: '0.5rem' }}>
                  Keep this secret key safe. Paste this into your project backend to create checkout sessions.
                </p>
              </div>

              {/* Quick How-It-Works Flow */}
              <div style={{ marginTop: '1.5rem', borderTop: '1px solid var(--border)', paddingTop: '1.25rem' }}>
                <h4>How Integration Works (3 Steps):</h4>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '1rem', marginTop: '1rem' }}>
                  <div style={{ background: '#f8fafc', padding: '1rem', borderRadius: '0.5rem', border: '1px solid var(--border)' }}>
                    <div style={{ fontWeight: 600, color: 'var(--primary)', marginBottom: '0.25rem' }}>1. Create Session</div>
                    <p style={{ fontSize: '0.8rem', color: '#64748b', margin: 0 }}>
                      Your website calls <code>POST /api/checkout/session</code> with your API Key and order amount.
                    </p>
                  </div>
                  <div style={{ background: '#f8fafc', padding: '1rem', borderRadius: '0.5rem', border: '1px solid var(--border)' }}>
                    <div style={{ fontWeight: 600, color: 'var(--primary)', marginBottom: '0.25rem' }}>2. Customer Pays</div>
                    <p style={{ fontSize: '0.8rem', color: '#64748b', margin: 0 }}>
                      Customer is redirected to DWPG Hosted Checkout to pay via UPI QR (valivetysathvik@ibl) or Card.
                    </p>
                  </div>
                  <div style={{ background: '#f8fafc', padding: '1rem', borderRadius: '0.5rem', border: '1px solid var(--border)' }}>
                    <div style={{ fontWeight: 600, color: 'var(--primary)', marginBottom: '0.25rem' }}>3. Auto Redirect</div>
                    <p style={{ fontSize: '0.8rem', color: '#64748b', margin: 0 }}>
                      Customer is automatically returned to your store's <code>returnUrl</code> with verified payment status.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* TAB 2: CODE SNIPPETS & DOCS */}
          {activeTab === 'DOCS' && (
            <div className="card">
              <div className="card-header">
                <div>
                  <h3 className="card-title">Integration Code Snippets</h3>
                  <p className="card-subtitle">Copy-paste into your project to start accepting payments</p>
                </div>
                <div style={{ display: 'flex', gap: '0.25rem' }}>
                  {['NODE', 'PYTHON', 'CURL'].map((lang) => (
                    <button
                      key={lang}
                      type="button"
                      className={`btn btn-sm ${selectedLang === lang ? 'btn-primary' : 'btn-secondary'}`}
                      onClick={() => setSelectedLang(lang)}
                    >
                      {lang === 'NODE' ? 'Node.js / Express' : lang === 'PYTHON' ? 'Python' : 'cURL'}
                    </button>
                  ))}
                </div>
              </div>

              <div style={{ position: 'relative' }}>
                <pre
                  style={{
                    background: '#0f172a',
                    color: '#e2e8f0',
                    padding: '1.25rem',
                    borderRadius: '0.5rem',
                    overflowX: 'auto',
                    fontSize: '0.85rem',
                    lineHeight: 1.5,
                  }}
                >
                  <code>{snippets[selectedLang]}</code>
                </pre>
                <button
                  type="button"
                  className="btn btn-secondary btn-sm"
                  style={{ position: 'absolute', top: 10, right: 10, background: '#1e293b', color: '#fff', border: '1px solid #475569' }}
                  onClick={() => {
                    navigator.clipboard.writeText(snippets[selectedLang]);
                    alert('Copied code snippet to clipboard!');
                  }}
                >
                  📋 Copy Code
                </button>
              </div>

              <div style={{ marginTop: '1.5rem', background: '#ecfdf5', padding: '1rem', borderRadius: '0.5rem', border: '1px solid #a7f3d0' }}>
                <strong style={{ color: '#065f46' }}>💡 Return URL Format:</strong>
                <p style={{ color: '#047857', fontSize: '0.85rem', margin: '0.25rem 0 0 0' }}>
                  When the customer finishes payment, DWPG redirects to your <code>returnUrl</code> appending:<br />
                  <code>?orderId=ORD-12345&status=SUCCESS&sessionId=cs_dwpg_...&amount=499.00</code>
                </p>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
