export interface User {
  id: number;
  name: string;
  email: string;
  role: 'Admin' | 'Supplier' | 'Financier';
  status: 'Active' | 'Inactive' | 'Pending';
  lastLogin: string | null;
}