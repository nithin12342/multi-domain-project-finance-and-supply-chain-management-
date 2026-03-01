import React, { createContext, useState, useContext, useEffect } from 'react';
import AuthService from '../services/authService';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [token, setToken] = useState(null);

  useEffect(() => {
    // Check if user is already logged in (from localStorage)
    const storedToken = localStorage.getItem('authToken');
    const storedUser = localStorage.getItem('user');
    
    if (storedToken && storedUser) {
      setToken(storedToken);
      setUser(JSON.parse(storedUser));
    }
    
    setLoading(false);
  }, []);

  const login = async (email, password, role) => {
    try {
      const response = await AuthService.login(email, password);
      const authToken = response.data;
      
      // Fetch user details
      const userResponse = await AuthService.getCurrentUser();
      const userData = {
        ...userResponse.data,
        role: role || userResponse.data.role || 'user'
      };
      
      setUser(userData);
      setToken(authToken);
      
      // Store in localStorage for persistence
      localStorage.setItem('authToken', authToken);
      localStorage.setItem('user', JSON.stringify(userData));
      
      return userData;
    } catch (error) {
      throw new Error(error.message || 'Invalid credentials');
    }
  };

  const register = async (userData) => {
    try {
      const response = await AuthService.register(userData);
      return response.data;
    } catch (error) {
      throw new Error(error.message || 'Registration failed');
    }
  };

  const logout = async () => {
    try {
      await AuthService.logout();
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      setUser(null);
      setToken(null);
      localStorage.removeItem('authToken');
      localStorage.removeItem('user');
    }
  };

  const getPermissionsForRole = (role) => {
    const permissions = {
      admin: [
        'view_dashboard',
        'manage_users',
        'manage_suppliers',
        'manage_financiers',
        'view_analytics',
        'manage_shipments',
        'view_settings',
        'approve_requests'
      ],
      supplier: [
        'view_dashboard',
        'manage_products',
        'view_shipments',
        'update_inventory',
        'view_financials'
      ],
      financier: [
        'view_dashboard',
        'view_invoices',
        'process_payments',
        'view_risk_assessments',
        'view_analytics'
      ],
      user: [
        'view_dashboard',
        'view_profile'
      ]
    };
    
    return permissions[role] || permissions.user;
  };

  const hasPermission = (permission) => {
    if (!user || !user.permissions) return false;
    return user.permissions.includes(permission);
  };

  const isAuthenticated = !!user;

  const value = {
    user,
    token,
    loading,
    login,
    register,
    logout,
    hasPermission,
    isAuthenticated
  };

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  );
};