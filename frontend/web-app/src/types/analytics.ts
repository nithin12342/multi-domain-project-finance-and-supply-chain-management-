export interface Transaction {
  id: number;
  supplier: string;
  financier: string;
  amount: number;
  status: 'Completed' | 'Processing' | 'Approved' | 'Pending';
}

export interface ProductData {
  name: string;
  value: number;
}

export interface AnalyticsData {
  totalTransactions: number;
  totalValue: number;
  activeSuppliers: number;
  activeFinanciers: number;
  pendingApprovals: number;
  monthlyGrowth: number;
  riskScore: number;
  topProducts: ProductData[];
  recentTransactions: Transaction[];
}