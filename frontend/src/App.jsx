import React, { useState, useEffect } from 'react';
import { AuthProvider, useAuth } from './context/AuthContext';
import Navbar from './components/Navbar';
import LoginView from './views/LoginView';
import RegisterView from './views/RegisterView';
import WalletView from './views/WalletView';
import PaymentView from './views/PaymentView';
import MerchantView from './views/MerchantView';
import TransactionLedgerView from './views/TransactionLedgerView';
import AdminAuditView from './views/AdminAuditView';
import HostedCheckoutView from './views/HostedCheckoutView';
import DemoStoreView from './views/DemoStoreView';

function MainLayout() {
  const { isAuthenticated, loading } = useAuth();
  const [activeTab, setActiveTab] = useState('wallet');

  // Check if this page load is for a Hosted Checkout session
  const queryParams = new URLSearchParams(window.location.search);
  const checkoutSessionId = queryParams.get('session') || queryParams.get('session_id');
  const isCheckoutRoute = window.location.pathname.startsWith('/checkout') || !!checkoutSessionId;

  useEffect(() => {
    const tabParam = queryParams.get('tab');
    if (tabParam === 'demo-store') {
      setActiveTab('demo-store');
    }
  }, []);

  // If this is a hosted checkout request, bypass login and show Hosted Checkout page
  if (isCheckoutRoute) {
    return <HostedCheckoutView sessionId={checkoutSessionId} />;
  }

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
        <p>Loading application security context...</p>
      </div>
    );
  }

  // If not authenticated, allow switching between login, register, or demo-store
  if (!isAuthenticated) {
    if (activeTab === 'demo-store') {
      return (
        <div>
          <Navbar activeTab="demo-store" setActiveTab={setActiveTab} />
          <main className="container">
            <DemoStoreView />
          </main>
        </div>
      );
    }

    return (
      <div>
        <Navbar activeTab={activeTab === 'register' ? 'register' : 'login'} setActiveTab={setActiveTab} />
        <main className="container">
          {activeTab === 'register' ? (
            <RegisterView
              onSuccess={() => setActiveTab('wallet')}
              onSwitchToLogin={() => setActiveTab('login')}
            />
          ) : (
            <LoginView
              onSuccess={() => setActiveTab('wallet')}
              onSwitchToRegister={() => setActiveTab('register')}
            />
          )}
        </main>
      </div>
    );
  }

  return (
    <div>
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />
      <main className="container">
        {activeTab === 'wallet' && <WalletView />}
        {activeTab === 'payment' && <PaymentView />}
        {activeTab === 'transactions' && <TransactionLedgerView />}
        {activeTab === 'merchant' && <MerchantView onOpenDemoStore={() => setActiveTab('demo-store')} />}
        {activeTab === 'demo-store' && <DemoStoreView />}
        {activeTab === 'admin' && <AdminAuditView />}
      </main>
    </div>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <MainLayout />
    </AuthProvider>
  );
}
