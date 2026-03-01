// Centralized API helper for all backend services
const API_URLS = {
    supply: 'http://localhost:8080/api/supply',
    auth: 'http://localhost:8081/api/auth',
    ai: 'http://localhost:8082/api/ai',
    finance: 'http://localhost:8083/api/finance',
};

export async function api<T>(
    service: keyof typeof API_URLS,
    path: string,
    options?: { method?: string; body?: any }
): Promise<{ data: T | null; error: string | null }> {
    try {
        const url = `${API_URLS[service]}${path}`;
        const res = await fetch(url, {
            method: options?.method || 'GET',
            headers: { 'Content-Type': 'application/json' },
            body: options?.body ? JSON.stringify(options.body) : undefined,
            signal: AbortSignal.timeout(5000),
        });
        const json = await res.json();
        // Spring Boot wraps in ApiResponse { data, message }
        return { data: json.data ?? json, error: null };
    } catch (e: any) {
        return { data: null, error: e.message || 'API unavailable' };
    }
}

// Typed helpers
export const supplyApi = {
    getInventory: () => api<any[]>('supply', '/inventory'),
    createInventory: (body: any) => api<any>('supply', '/inventory', { method: 'POST', body }),
    deleteInventory: (id: number) => api<any>('supply', `/inventory/${id}`, { method: 'DELETE' }),
    getShipments: () => api<any[]>('supply', '/shipments'),
    createShipment: (body: any) => api<any>('supply', '/shipments', { method: 'POST', body }),
    getSuppliers: () => api<any[]>('supply', '/suppliers'),
    createSupplier: (body: any) => api<any>('supply', '/suppliers', { method: 'POST', body }),
    getAnalytics: () => api<any>('supply', '/analytics/metrics'),
};

export const financeApi = {
    getInvoices: () => api<any[]>('finance', '/invoices'),
    createInvoice: (body: any) => api<any>('finance', '/invoices', { method: 'POST', body }),
    approveInvoice: (id: number) => api<any>('finance', `/invoices/${id}/approve`, { method: 'POST' }),
    financeInvoice: (id: number, body: any) => api<any>('finance', `/invoices/${id}/finance`, { method: 'POST', body }),
    getAnalytics: () => api<any>('finance', '/analytics'),
    getRisk: (supplierId: number) => api<any>('finance', `/risk-assessment?supplierId=${supplierId}`),
};

export const aiApi = {
    predict: (body: any) => api<any>('ai', '/demand/predict', { method: 'POST', body }),
    detectFraud: (body: any) => api<any>('ai', '/fraud/detect', { method: 'POST', body }),
    assessRisk: (supplierId: string) => api<any>('ai', `/risk/${supplierId}`, { method: 'POST' }),
    retrain: () => api<any>('ai', '/models/retrain', { method: 'POST' }),
    getAnalytics: () => api<any>('ai', '/analytics'),
};

export const authApi = {
    register: (body: any) => api<any>('auth', '/register', { method: 'POST', body }),
    login: (body: any) => api<any>('auth', '/login', { method: 'POST', body }),
};
