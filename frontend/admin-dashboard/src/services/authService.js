import apiClient from './api';

class AuthService {
  static async login(email, password) {
    try {
      const response = await apiClient.post('/auth/login', { email, password });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Login failed');
    }
  }

  static async register(userData) {
    try {
      const response = await apiClient.post('/auth/register', userData);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Registration failed');
    }
  }

  static async getCurrentUser() {
    try {
      const response = await apiClient.get('/auth/user');
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to fetch user data');
    }
  }

  static async logout() {
    try {
      await apiClient.post('/auth/logout');
    } catch (error) {
      // Even if logout fails, we still want to clear local data
      console.error('Logout error:', error);
    } finally {
      // Clear local storage regardless of API response
      localStorage.removeItem('authToken');
      localStorage.removeItem('user');
    }
  }
}

export default AuthService;