'use client';
import React, { useState } from 'react';
import StatCard from '../../components/StatCard';
import DataTable from '../../components/DataTable';
import StatusBadge from '../../components/StatusBadge';
import SearchBar from '../../components/SearchBar';
import Modal, { FormField, FormInput, FormSelect } from '../../components/Modal';
import { useToast } from '../../components/Toast';
import { authApi } from '../../lib/api';

const initUsers = [
  { id: 'USR-001', name: 'Sarah Johnson', email: 'sarah@techcorp.com', role: 'Admin', status: 'Active', lastLogin: '2025-10-08 09:15' },
  { id: 'USR-002', name: 'James Chen', email: 'james@textilehub.com', role: 'Supplier', status: 'Active', lastLogin: '2025-10-08 08:42' },
  { id: 'USR-003', name: 'Maria Garcia', email: 'maria@capitalpartners.com', role: 'Financier', status: 'Active', lastLogin: '2025-10-07 16:30' },
  { id: 'USR-004', name: 'Ahmed Hassan', email: 'ahmed@retailmax.com', role: 'Buyer', status: 'Active', lastLogin: '2025-10-07 14:20' },
  { id: 'USR-005', name: 'Lisa Wang', email: 'lisa@machinex.de', role: 'Supplier', status: 'Active', lastLogin: '2025-10-06 11:45' },
  { id: 'USR-006', name: 'Robert Taylor', email: 'robert@investcorp.com', role: 'Financier', status: 'Inactive', lastLogin: '2025-09-28 09:00' },
];

const roleColors: Record<string, string> = { Admin: 'bg-violet-500/20 text-violet-400', Supplier: 'bg-emerald-500/20 text-emerald-400', Financier: 'bg-amber-500/20 text-amber-400', Buyer: 'bg-cyan-500/20 text-cyan-400' };

export default function UsersPage() {
  const [users, setUsers] = useState(initUsers);
  const [search, setSearch] = useState('');
  const [showModal, setShowModal] = useState(false);
  const { showToast, ToastComponent } = useToast();
  const [form, setForm] = useState({ name: '', email: '', role: '', password: '' });

  const handleAdd = async () => {
    if (!form.name || !form.email) return;
    // Try real auth API
    const res = await authApi.register({ name: form.name, email: form.email, password: form.password || 'DefaultPass123!', role: form.role || 'BUYER' });
    const u = {
      id: res.data?.id ? `USR-${String(res.data.id).padStart(3, '0')}` : `USR-${String(users.length + 1).padStart(3, '0')}`,
      name: form.name, email: form.email, role: form.role || 'Buyer',
      status: 'Active', lastLogin: 'Never',
    };
    setUsers([u, ...users]);
    setForm({ name: '', email: '', role: '', password: '' });
    setShowModal(false);
    showToast(res.error ? `${form.name} added locally (auth service offline)` : `${form.name} registered in database!`);
  };

  const handleDelete = (id: string) => { setUsers(users.filter(u => u.id !== id)); showToast(`User ${id} deleted`, 'info'); };
  const handleToggle = (id: string) => { setUsers(users.map(u => u.id === id ? { ...u, status: u.status === 'Active' ? 'Inactive' : 'Active' } : u)); showToast(`User ${id} toggled`, 'info'); };

  const filtered = users.filter(u => Object.values(u).some(v => String(v).toLowerCase().includes(search.toLowerCase())));

  return (
    <div className="page-enter">
      {ToastComponent}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold mb-2"><span className="gradient-text">User</span> Management</h1>
          <p className="text-slate-400">Manage platform users and permissions</p>
        </div>
        <button onClick={() => setShowModal(true)} className="px-4 py-2 text-sm font-medium text-white rounded-xl bg-gradient-to-r from-violet-600 to-indigo-700 hover:from-violet-500 transition-all shadow-lg">➕ Add User</button>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5 mb-6">
        <StatCard title="Total Users" value={users.length} icon="👥" color="slate" />
        <StatCard title="Admins" value={users.filter(u => u.role === 'Admin').length} icon="🛡️" color="violet" />
        <StatCard title="Suppliers" value={users.filter(u => u.role === 'Supplier').length} icon="🏭" color="emerald" />
        <StatCard title="Financiers" value={users.filter(u => u.role === 'Financier').length} icon="💰" color="amber" />
      </div>
      <div className="mb-4 max-w-sm"><SearchBar value={search} onChange={setSearch} placeholder="Search by name, email, or role..." /></div>
      <DataTable title="👥 Platform Users" columns={[
        { key: 'name', label: 'Name', render: (v: string) => <span className="text-slate-200 font-medium">{v}</span> },
        { key: 'email', label: 'Email' },
        { key: 'role', label: 'Role', render: (v: string) => <span className={`px-2.5 py-1 rounded-full text-xs font-semibold ${roleColors[v] || ''}`}>{v}</span> },
        { key: 'status', label: 'Status', render: (v: string) => <StatusBadge status={v} variant="dot" /> },
        { key: 'lastLogin', label: 'Last Login' },
        {
          key: 'id', label: 'Actions', render: (_: any, row: any) => (
            <div className="flex gap-1.5">
              <button onClick={() => handleToggle(row.id)} className="px-2 py-0.5 text-[10px] rounded-md bg-amber-500/20 text-amber-400 hover:bg-amber-500/30">{row.status === 'Active' ? '⏸' : '▶'}</button>
              <button onClick={() => handleDelete(row.id)} className="px-2 py-0.5 text-[10px] rounded-md bg-rose-500/20 text-rose-400 hover:bg-rose-500/30">✕</button>
            </div>
          )
        },
      ]} data={filtered} />
      <Modal isOpen={showModal} onClose={() => setShowModal(false)} title="➕ Add User" onSubmit={handleAdd} submitLabel="Create User" color="violet">
        <FormField label="Full Name"><FormInput value={form.name} onChange={v => setForm({ ...form, name: v })} placeholder="e.g. John Doe" /></FormField>
        <FormField label="Email"><FormInput value={form.email} onChange={v => setForm({ ...form, email: v })} placeholder="e.g. john@company.com" type="email" /></FormField>
        <FormField label="Password"><FormInput value={form.password} onChange={v => setForm({ ...form, password: v })} placeholder="e.g. SecurePass123!" type="password" /></FormField>
        <FormField label="Role"><FormSelect value={form.role} onChange={v => setForm({ ...form, role: v })} options={[{ value: 'Admin', label: 'Admin' }, { value: 'Supplier', label: 'Supplier' }, { value: 'Financier', label: 'Financier' }, { value: 'Buyer', label: 'Buyer' }]} /></FormField>
      </Modal>
    </div>
  );
}