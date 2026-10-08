import React, { useState } from 'react';
import { AuthProvider, useAuth } from './context/AuthContext';
import Navbar from './components/Navbar';
import LoginView from './views/LoginView';
import RegisterView from './views/RegisterView';
import WalletView from './views/WalletView';
import PaymentView from './views/PaymentView';
import MerchantView from './views/MerchantView';
import TransactionLedgerView from './views/TransactionLedgerView';
import AdminAuditView from './views/AdminAuditView';

function MainLayout() {
  const { isAuthenticated, loading } = useAuth();
  const [activeTab, setActiveTab] = useState('wallet');

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
        <p>Loading application security context...</p>
      </div>
    );
  }

  // If not authenticated, allow switching between login and register
  if (!isAuthenticated) {
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
        {activeTab === 'merchant' && <MerchantView />}
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
