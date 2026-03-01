import apiClient from './api';

class SupplyService {
  static async getInventory(location = null, page = 0, size = 10) {
    try {
      const params = { page, size };
      if (location) {
        params.location = location;
      }
      const response = await apiClient.get('/supply/inventory', { params });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to fetch inventory');
    }
  }

  static async createShipment(shipmentData) {
    try {
      const response = await apiClient.post('/supply/shipments', shipmentData);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to create shipment');
    }
  }

  static async trackShipment(shipmentId) {
    try {
      const response = await apiClient.get(`/supply/shipments/${shipmentId}/track`);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to track shipment');
    }
  }

  static async updateInventory(inventoryData) {
    try {
      const response = await apiClient.post('/supply/inventory/update', inventoryData);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to update inventory');
    }
  }

  static async getInventoryAnalytics() {
    try {
      const response = await apiClient.get('/supply/analytics/inventory');
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to fetch analytics');
    }
  }

  static async getSuppliers() {
    try {
      const response = await apiClient.get('/supply/suppliers');
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to fetch suppliers');
    }
  }

  static async createOrder(orderData) {
    try {
      const response = await apiClient.post('/supply/orders', orderData);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to create order');
    }
  }
}

export default SupplyService;