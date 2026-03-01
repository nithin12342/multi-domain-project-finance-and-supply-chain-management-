'use client';
import React, { useState, useEffect } from 'react';
import StatCard from '../../components/StatCard';
import DataTable from '../../components/DataTable';
import StatusBadge from '../../components/StatusBadge';
import SearchBar from '../../components/SearchBar';
import Modal, { FormField, FormInput } from '../../components/Modal';
import { useToast } from '../../components/Toast';
import { financeApi } from '../../lib/api';

const seedInvoices = [
    { id: 'INV-1923', supplier: 'TechCorp Ltd', buyer: 'RetailMax', amount: '$150,000', dueDate: '2025-11-15', status: 'Financed', _id: null as number | null },
    { id: 'INV-1922', supplier: 'TextileHub', buyer: 'FashionCo', amount: '$85,000', dueDate: '2025-11-10', status: 'Approved', _id: null as number | null },
    { id: 'INV-1921', supplier: 'Machinex', buyer: 'BuildCorp', amount: '$320,000', dueDate: '2025-11-08', status: 'Pending', _id: null as number | null },
    { id: 'INV-1920', supplier: 'ChemWorld', buyer: 'PharmaInc', amount: '$195,000', dueDate: '2025-10-30', status: 'Paid', _id: null as number | null },
    { id: 'INV-1919', supplier: 'FoodProd', buyer: 'GroceryKing', amount: '$42,000', dueDate: '2025-10-25', status: 'Overdue', _id: null as number | null },
];

export default function FinancePage() {
    const [invoices, setInvoices] = useState(seedInvoices);
    const [search, setSearch] = useState('');
    const [showModal, setShowModal] = useState(false);
    const { showToast, ToastComponent } = useToast();
    const [form, setForm] = useState({ supplier: '', buyer: '', amount: '', dueDate: '' });

    // Load from backend
    useEffect(() => {
        async function load() {
            const res = await financeApi.getInvoices();
            if (res.data && Array.isArray(res.data) && res.data.length > 0) {
                setInvoices(res.data.map((i: any) => ({
                    id: `INV-${String(i.id).padStart(4, '0')}`,
                    supplier: i.supplierName || i.supplier || 'N/A',
                    buyer: i.buyerName || i.buyer || 'N/A',
                    amount: `$${(i.amount ?? 0).toLocaleString()}`,
                    dueDate: i.dueDate || 'N/A',
                    status: i.status || 'Pending',
                    _id: i.id,
                })));
            }
        }
        load();
    }, []);

    const handleCreate = async () => {
        if (!form.supplier || !form.amount) return;
        const body = {
            supplierName: form.supplier, buyerName: form.buyer || 'TBD',
            amount: parseInt(form.amount), dueDate: form.dueDate || new Date().toISOString().split('T')[0],
        };
        const res = await financeApi.createInvoice(body);
        const inv = {
            id: res.data?.id ? `INV-${String(res.data.id).padStart(4, '0')}` : `INV-${1923 + invoices.length}`,
            supplier: form.supplier, buyer: form.buyer || 'TBD',
            amount: `$${parseInt(form.amount).toLocaleString()}`,
            dueDate: form.dueDate || new Date().toISOString().split('T')[0],
            status: 'Pending', _id: res.data?.id ?? null,
        };
        setInvoices([inv, ...invoices]);
        setForm({ supplier: '', buyer: '', amount: '', dueDate: '' });
        setShowModal(false);
        showToast(res.error ? `Invoice created locally (backend offline)` : `Invoice ${inv.id} saved to database!`);
    };

    const handleAction = async (id: string, action: string, _id: number | null) => {
        if (_id && action === 'Approved') await financeApi.approveInvoice(_id);
        if (_id && action === 'Financed') await financeApi.financeInvoice(_id, { financierId: 1, interestRate: 5.0 });
        setInvoices(invoices.map(i => i.id === id ? { ...i, status: action } : i));
        showToast(`Invoice ${id} → ${action}`);
    };

    const filtered = invoices.filter(o => Object.values(o).some(v => String(v).toLowerCase().includes(search.toLowerCase())));
    const totalFinanced = invoices.filter(i => i.status === 'Financed' || i.status === 'Paid').length;

    return (
        <div className="page-enter">
            {ToastComponent}
            <div className="flex items-center justify-between mb-8">
                <div>
                    <h1 className="text-3xl font-bold mb-2"><span className="text-amber-400">Finance</span> Management</h1>
                    <p className="text-slate-400">Invoice processing, payments, and credit risk management</p>
                </div>
                <button onClick={() => setShowModal(true)} className="px-4 py-2 text-sm font-medium text-white rounded-xl bg-gradient-to-r from-amber-600 to-amber-700 hover:from-amber-500 transition-all shadow-lg">➕ Create Invoice</button>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5 mb-6">
                <StatCard title="Total Invoices" value={invoices.length} icon="📄" color="amber" />
                <StatCard title="Financed/Paid" value={totalFinanced} icon="💳" color="amber" />
                <StatCard title="Pending" value={invoices.filter(i => i.status === 'Pending').length} icon="⏳" color="amber" />
                <StatCard title="Overdue" value={invoices.filter(i => i.status === 'Overdue').length} icon="⚠️" color="rose" />
            </div>
            <div className="mb-4 max-w-sm"><SearchBar value={search} onChange={setSearch} placeholder="Search invoices..." /></div>
            <DataTable title="📄 Invoice Management" columns={[
                { key: 'id', label: 'Invoice', render: (v: string) => <span className="text-amber-400 font-medium">{v}</span> },
                { key: 'supplier', label: 'Supplier' }, { key: 'buyer', label: 'Buyer' },
                { key: 'amount', label: 'Amount' }, { key: 'dueDate', label: 'Due Date' },
                { key: 'status', label: 'Status', render: (v: string) => <StatusBadge status={v} variant="dot" /> },
                {
                    key: 'id', label: 'Actions', render: (_: any, row: any) => (
                        <div className="flex gap-1.5">
                            {row.status === 'Pending' && (
                                <>
                                    <button onClick={() => handleAction(row.id, 'Approved', row._id)} className="px-2 py-0.5 text-[10px] rounded-md bg-emerald-500/20 text-emerald-400 hover:bg-emerald-500/30">✓ Approve</button>
                                    <button onClick={() => handleAction(row.id, 'Cancelled', row._id)} className="px-2 py-0.5 text-[10px] rounded-md bg-rose-500/20 text-rose-400 hover:bg-rose-500/30">✕ Reject</button>
                                </>
                            )}
                            {row.status === 'Approved' && (
                                <button onClick={() => handleAction(row.id, 'Financed', row._id)} className="px-2 py-0.5 text-[10px] rounded-md bg-indigo-500/20 text-indigo-400 hover:bg-indigo-500/30">💰 Finance</button>
                            )}
                        </div>
                    )
                },
            ]} data={filtered} />
            <div className="glass-card p-6 mt-6">
                <h3 className="text-sm font-semibold text-slate-200 mb-4">📈 Monthly Revenue</h3>
                <div className="flex items-end gap-2 h-40">
                    {[40, 55, 45, 72, 65, 80, 68, 92, 85, 95, 88, 100].map((h, i) => (
                        <div key={i} className="flex-1 flex flex-col items-center gap-1">
                            <div className="w-full bg-gradient-to-t from-amber-500/60 to-amber-300/30 rounded-t-md hover:from-amber-500/80 transition-all" style={{ height: `${h}%` }} />
                            <span className="text-[9px] text-slate-500">{['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'][i]}</span>
                        </div>
                    ))}
                </div>
            </div>
            <Modal isOpen={showModal} onClose={() => setShowModal(false)} title="➕ New Invoice" onSubmit={handleCreate} submitLabel="Create Invoice" color="amber">
                <FormField label="Supplier"><FormInput value={form.supplier} onChange={v => setForm({ ...form, supplier: v })} placeholder="e.g. TechCorp Ltd" /></FormField>
                <FormField label="Buyer"><FormInput value={form.buyer} onChange={v => setForm({ ...form, buyer: v })} placeholder="e.g. RetailMax" /></FormField>
                <FormField label="Amount ($)"><FormInput value={form.amount} onChange={v => setForm({ ...form, amount: v })} placeholder="e.g. 150000" type="number" /></FormField>
                <FormField label="Due Date"><FormInput value={form.dueDate} onChange={v => setForm({ ...form, dueDate: v })} type="date" /></FormField>
            </Modal>
        </div>
    );
}
