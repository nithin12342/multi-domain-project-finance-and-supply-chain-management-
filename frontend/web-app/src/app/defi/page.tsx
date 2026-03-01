'use client';
import React, { useState } from 'react';
import StatCard from '../../components/StatCard';
import DataTable from '../../components/DataTable';
import StatusBadge from '../../components/StatusBadge';
import Modal, { FormField, FormInput, FormSelect } from '../../components/Modal';
import { useToast } from '../../components/Toast';

const initPools = [
    { name: 'SCF Yield Pool', protocol: 'Compound Fork', tvl: 4200000, apy: 8.2, utilization: 78, status: 'Active' },
    { name: 'Invoice Liquidity', protocol: 'Aave Fork', tvl: 2800000, apy: 6.5, utilization: 65, status: 'Active' },
    { name: 'Trade Finance Pool', protocol: 'Custom AMM', tvl: 1500000, apy: 11.3, utilization: 92, status: 'Active' },
    { name: 'Stablecoin Reserve', protocol: 'Curve Fork', tvl: 8100000, apy: 3.8, utilization: 45, status: 'Active' },
];

export default function DeFiPage() {
    const [pools, setPools] = useState(initPools);
    const [showModal, setShowModal] = useState(false);
    const { showToast, ToastComponent } = useToast();
    const [form, setForm] = useState({ pool: '', amount: '' });

    const totalTvl = pools.reduce((s, p) => s + p.tvl, 0);
    const avgApy = pools.reduce((s, p) => s + p.apy, 0) / pools.length;

    const handleAddLiquidity = () => {
        if (!form.pool || !form.amount) return;
        const amount = parseInt(form.amount);
        setPools(pools.map(p => p.name === form.pool ? { ...p, tvl: p.tvl + amount, utilization: Math.min(99, p.utilization + Math.round(amount / 100000)) } : p));
        showToast(`$${amount.toLocaleString()} added to ${form.pool}!`);
        setForm({ pool: '', amount: '' });
        setShowModal(false);
    };

    return (
        <div className="page-enter">
            {ToastComponent}
            <div className="flex items-center justify-between mb-8">
                <div>
                    <h1 className="text-3xl font-bold mb-2"><span className="text-indigo-400">DeFi</span> Protocols</h1>
                    <p className="text-slate-400">Yield generation, liquidity pools, and protocol metrics</p>
                </div>
                <button onClick={() => setShowModal(true)} className="px-4 py-2 text-sm font-medium text-white rounded-xl bg-gradient-to-r from-indigo-600 to-indigo-700 hover:from-indigo-500 transition-all shadow-lg">💰 Add Liquidity</button>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5 mb-6">
                <StatCard title="Total TVL" value={`$${(totalTvl / 1e6).toFixed(1)}M`} icon="🏦" color="indigo" />
                <StatCard title="Avg APY" value={`${avgApy.toFixed(2)}%`} icon="📈" color="indigo" />
                <StatCard title="Active Pools" value={pools.length} icon="🌊" color="indigo" />
                <StatCard title="LPs" value="287" icon="👥" color="indigo" />
            </div>
            <DataTable title="🌊 Yield Pools" columns={[
                { key: 'name', label: 'Pool', render: (v: string) => <span className="text-indigo-400 font-medium">{v}</span> },
                { key: 'protocol', label: 'Protocol' },
                { key: 'tvl', label: 'TVL', render: (v: number) => `$${(v / 1e6).toFixed(2)}M` },
                { key: 'apy', label: 'APY', render: (v: number) => <span className="text-emerald-400 font-semibold">{v}%</span> },
                {
                    key: 'utilization', label: 'Util.', render: (v: number) => (
                        <div className="flex items-center gap-2">
                            <div className="w-12 h-1.5 bg-slate-700 rounded-full overflow-hidden">
                                <div className={`h-full rounded-full ${v > 85 ? 'bg-rose-500' : v > 70 ? 'bg-amber-500' : 'bg-indigo-500'}`} style={{ width: `${v}%` }} />
                            </div>
                            <span className="text-xs">{v}%</span>
                        </div>
                    )
                },
                { key: 'status', label: 'Status', render: (v: string) => <StatusBadge status={v} variant="dot" /> },
            ]} data={pools} />

            <Modal isOpen={showModal} onClose={() => setShowModal(false)} title="💰 Add Liquidity" onSubmit={handleAddLiquidity} submitLabel="Add Liquidity" color="indigo">
                <FormField label="Select Pool"><FormSelect value={form.pool} onChange={v => setForm({ ...form, pool: v })} options={pools.map(p => ({ value: p.name, label: `${p.name} (${p.apy}% APY)` }))} /></FormField>
                <FormField label="Amount ($)"><FormInput value={form.amount} onChange={v => setForm({ ...form, amount: v })} placeholder="e.g. 50000" type="number" /></FormField>
            </Modal>
        </div>
    );
}
