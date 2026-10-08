import React, { createContext, useContext, useState, useEffect } from 'react';
import { authApi, getAuthToken, setAuthToken, getCurrentUser, setCurrentUser } from '../api';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(getCurrentUser());
  const [token, setToken] = useState(getAuthToken());
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function initAuth() {
      const storedToken = getAuthToken();
      if (storedToken) {
        try {
          const userData = await authApi.getMe();
          setUser(userData);
          setCurrentUser(userData);
        } catch (err) {
          console.error('Session expired or invalid', err);
          logout();
        }
      }
      setLoading(false);
    }
    initAuth();
  }, []);

  const login = async (username, password) => {
    const data = await authApi.login(username, password);
    setToken(data.token);
    setAuthToken(data.token);
    const userData = {
      id: data.id,
      username: data.username,
      email: data.email,
      role: data.role,
    };
    setUser(userData);
    setCurrentUser(userData);
    return userData;
  };

  const loginWithGoogle = async (payload) => {
    const data = await authApi.loginWithGoogle(payload);
    setToken(data.token);
    setAuthToken(data.token);
    const userData = {
      id: data.id,
      username: data.username,
      email: data.email,
      role: data.role,
    };
    setUser(userData);
    setCurrentUser(userData);
    return userData;
  };

  const register = async (username, email, password, role) => {
    return await authApi.register(username, email, password, role);
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    setAuthToken(null);
    setCurrentUser(null);
  };

  const refreshUser = async () => {
    if (getAuthToken()) {
      try {
        const userData = await authApi.getMe();
        setUser(userData);
        setCurrentUser(userData);
      } catch (err) {
        console.error('Failed to refresh user', err);
      }
    }
  };

  const value = {
    user,
    token,
    isAuthenticated: !!token && !!user,
    role: user?.role || 'ANONYMOUS',
    isAdmin: user?.role === 'ROLE_ADMIN',
    isMerchant: user?.role === 'ROLE_MERCHANT',
    login,
    loginWithGoogle,
    register,
    logout,
    refreshUser,
    loading,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
