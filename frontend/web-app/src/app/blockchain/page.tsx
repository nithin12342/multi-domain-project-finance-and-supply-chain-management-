'use client';
import React, { useState } from 'react';
import StatCard from '../../components/StatCard';
import DataTable from '../../components/DataTable';
import StatusBadge from '../../components/StatusBadge';
import SearchBar from '../../components/SearchBar';
import Modal, { FormField, FormInput, FormSelect } from '../../components/Modal';
import { useToast } from '../../components/Toast';

const initContracts = [
    { id: 'SC-0x7f3a', name: 'Supply Verification', network: 'Hyperledger Fabric', status: 'Active', transactions: 1247, deployed: '2025-08-15' },
    { id: 'SC-0x4b2c', name: 'Payment Escrow', network: 'Ethereum L2', status: 'Active', transactions: 892, deployed: '2025-09-01' },
    { id: 'SC-0x9d1e', name: 'Trade Finance', network: 'Hyperledger Fabric', status: 'Active', transactions: 456, deployed: '2025-09-20' },
];

const initTxs = [
    { hash: '0x7f3a...8bc2', type: 'Verification', from: 'TechCorp', to: 'RetailMax', value: '$150K', block: '#12,847', time: '2 min ago' },
    { hash: '0x4b2c...9de3', type: 'Payment', from: 'FashionCo', to: 'TextileHub', value: '$85K', block: '#12,846', time: '8 min ago' },
    { hash: '0x9d1e...1fg4', type: 'Finance', from: 'CapitalBank', to: 'Machinex', value: '$320K', block: '#12,845', time: '15 min ago' },
];

export default function BlockchainPage() {
    const [contracts, setContracts] = useState(initContracts);
    const [txs] = useState(initTxs);
    const [search, setSearch] = useState('');
    const [showModal, setShowModal] = useState(false);
    const { showToast, ToastComponent } = useToast();
    const [form, setForm] = useState({ name: '', network: '' });

    const handleDeploy = () => {
        if (!form.name) return;
        const hex = Math.random().toString(16).substr(2, 4);
        const c = { id: `SC-0x${hex}`, name: form.name, network: form.network || 'Hyperledger Fabric', status: 'Pending', transactions: 0, deployed: new Date().toISOString().split('T')[0] };
        setContracts([c, ...contracts]);
        setForm({ name: '', network: '' });
        setShowModal(false);
        showToast(`Contract ${c.id} deployed!`);
    };

    const filtered = contracts.filter(c => Object.values(c).some(v => String(v).toLowerCase().includes(search.toLowerCase())));

    return (
        <div className="page-enter">
            {ToastComponent}
            <div className="flex items-center justify-between mb-8">
                <div>
                    <h1 className="text-3xl font-bold mb-2"><span className="text-cyan-400">Blockchain</span> Integration</h1>
                    <p className="text-slate-400">Smart contracts, transaction ledger, and cross-chain bridge</p>
                </div>
                <button onClick={() => setShowModal(true)} className="px-4 py-2 text-sm font-medium text-white rounded-xl bg-gradient-to-r from-cyan-600 to-cyan-700 hover:from-cyan-500 transition-all shadow-lg">➕ Deploy Contract</button>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5 mb-6">
                <StatCard title="Contracts" value={contracts.length} icon="📜" color="cyan" />
                <StatCard title="Transactions" value={contracts.reduce((s, c) => s + c.transactions, 0).toLocaleString()} icon="🔗" color="cyan" />
                <StatCard title="Networks" value="3" icon="🌐" color="cyan" />
                <StatCard title="Block Height" value="#12,847" icon="⛓️" color="cyan" />
            </div>
            <div className="mb-4 max-w-sm"><SearchBar value={search} onChange={setSearch} placeholder="Search contracts..." /></div>
            <div className="grid grid-cols-1 xl:grid-cols-2 gap-6 mb-6">
                <DataTable title="📜 Smart Contracts" columns={[
                    { key: 'id', label: 'Contract', render: (v: string) => <span className="text-cyan-400 font-mono text-xs">{v}</span> },
                    { key: 'name', label: 'Name' }, { key: 'network', label: 'Network' },
                    { key: 'transactions', label: 'TXs', render: (v: number) => v.toLocaleString() },
                    { key: 'status', label: 'Status', render: (v: string) => <StatusBadge status={v} variant="dot" /> },
                ]} data={filtered} />
                <DataTable title="🔗 Transaction Ledger" columns={[
                    { key: 'hash', label: 'TX Hash', render: (v: string) => <span className="text-cyan-400 font-mono text-xs">{v}</span> },
                    { key: 'type', label: 'Type' }, { key: 'value', label: 'Value' }, { key: 'time', label: 'Time' },
                ]} data={txs} />
            </div>
            <Modal isOpen={showModal} onClose={() => setShowModal(false)} title="➕ Deploy Smart Contract" onSubmit={handleDeploy} submitLabel="Deploy" color="cyan">
                <FormField label="Contract Name"><FormInput value={form.name} onChange={v => setForm({ ...form, name: v })} placeholder="e.g. Escrow Agreement" /></FormField>
                <FormField label="Network"><FormSelect value={form.network} onChange={v => setForm({ ...form, network: v })} options={[{ value: 'Hyperledger Fabric', label: 'Hyperledger Fabric' }, { value: 'Ethereum L2', label: 'Ethereum L2' }, { value: 'Polygon', label: 'Polygon' }]} /></FormField>
            </Modal>
        </div>
    );
}
