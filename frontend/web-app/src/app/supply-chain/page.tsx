'use client';
import React, { useState, useEffect } from 'react';
import StatCard from '../../components/StatCard';
import DataTable from '../../components/DataTable';
import StatusBadge from '../../components/StatusBadge';
import SearchBar from '../../components/SearchBar';
import Modal, { FormField, FormInput, FormSelect } from '../../components/Modal';
import { useToast } from '../../components/Toast';
import { supplyApi } from '../../lib/api';

const seedOrders = [
    { id: 'ORD-2847', supplier: 'TechCorp Ltd', items: 5, total: '$15,200', status: 'Pending', date: '2025-10-08' },
    { id: 'ORD-2846', supplier: 'TextileHub Inc', items: 12, total: '$8,500', status: 'Confirmed', date: '2025-10-07' },
    { id: 'ORD-2845', supplier: 'Machinex GmbH', items: 2, total: '$48,000', status: 'Shipped', date: '2025-10-06' },
    { id: 'ORD-2844', supplier: 'ChemWorld Co', items: 8, total: '$4,600', status: 'Delivered', date: '2025-10-05' },
];

const seedInventory = [
    { productId: 'PROD-001', name: 'Electronic Components', location: 'Warehouse A', quantity: 2450, unitPrice: '$12.50', status: 'Active' },
    { productId: 'PROD-002', name: 'Textile Materials', location: 'Warehouse B', quantity: 890, unitPrice: '$8.30', status: 'Low Stock' },
    { productId: 'PROD-003', name: 'Industrial Machinery Parts', location: 'Warehouse C', quantity: 156, unitPrice: '$245.00', status: 'Active' },
    { productId: 'PROD-004', name: 'Chemical Compounds', location: 'Warehouse A', quantity: 3200, unitPrice: '$5.75', status: 'Active' },
];

export default function SupplyChainPage() {
    const [orders, setOrders] = useState(seedOrders);
    const [inventory, setInventory] = useState(seedInventory);
    const [shipments, setShipments] = useState<any[]>([]);
    const [search, setSearch] = useState('');
    const [showOrderModal, setShowOrderModal] = useState(false);
    const [showInvModal, setShowInvModal] = useState(false);
    const { showToast, ToastComponent } = useToast();
    const [orderForm, setOrderForm] = useState({ supplier: '', items: '', total: '' });
    const [invForm, setInvForm] = useState({ name: '', location: '', quantity: '', unitPrice: '' });
    const [loading, setLoading] = useState(true);

    // Fetch live data on mount
    useEffect(() => {
        async function loadData() {
            const [invRes, shpRes] = await Promise.all([
                supplyApi.getInventory(),
                supplyApi.getShipments(),
            ]);
            if (invRes.data && Array.isArray(invRes.data) && invRes.data.length > 0) {
                setInventory(invRes.data.map((i: any) => ({
                    productId: `PROD-${String(i.id).padStart(3, '0')}`,
                    name: i.name || i.productName || 'Unknown',
                    location: i.location || 'Warehouse A',
                    quantity: i.quantity ?? 0,
                    unitPrice: `$${i.unitPrice ?? i.price ?? 0}`,
                    status: i.quantity < 100 ? 'Low Stock' : 'Active',
                    _id: i.id,
                })));
            }
            if (shpRes.data && Array.isArray(shpRes.data) && shpRes.data.length > 0) {
                setShipments(shpRes.data.map((s: any) => ({
                    id: `SHP-${String(s.id).padStart(4, '0')}`,
                    origin: s.origin || 'N/A',
                    destination: s.destination || 'N/A',
                    status: s.status || 'Processing',
                    eta: s.estimatedArrival || s.eta || 'TBD',
                    _id: s.id,
                })));
            } else {
                setShipments([
                    { id: 'SHP-1001', origin: 'Shanghai, CN', destination: 'Los Angeles, US', status: 'In Transit', eta: '2025-10-15' },
                    { id: 'SHP-1002', origin: 'Mumbai, IN', destination: 'Rotterdam, NL', status: 'Delivered', eta: '2025-10-03' },
                ]);
            }
            setLoading(false);
        }
        loadData();
    }, []);

    const handleAddOrder = () => {
        if (!orderForm.supplier || !orderForm.total) return;
        const newOrder = {
            id: `ORD-${2847 + orders.length}`, supplier: orderForm.supplier,
            items: parseInt(orderForm.items) || 1, total: `$${orderForm.total}`,
            status: 'Pending', date: new Date().toISOString().split('T')[0],
        };
        setOrders([newOrder, ...orders]);
        setOrderForm({ supplier: '', items: '', total: '' });
        setShowOrderModal(false);
        showToast(`Order ${newOrder.id} created!`);
    };

    const handleAddInventory = async () => {
        if (!invForm.name) return;
        const body = {
            productName: invForm.name, name: invForm.name,
            location: invForm.location || 'Warehouse A',
            quantity: parseInt(invForm.quantity) || 0,
            unitPrice: parseFloat(invForm.unitPrice) || 0,
            price: parseFloat(invForm.unitPrice) || 0,
        };
        // Try real API first
        const res = await supplyApi.createInventory(body);
        const newItem = {
            productId: res.data?.id ? `PROD-${String(res.data.id).padStart(3, '0')}` : `PROD-${String(inventory.length + 1).padStart(3, '0')}`,
            name: invForm.name, location: invForm.location || 'Warehouse A',
            quantity: parseInt(invForm.quantity) || 0, unitPrice: `$${invForm.unitPrice || '0.00'}`,
            status: 'Active', _id: res.data?.id,
        };
        setInventory([newItem, ...inventory]);
        setInvForm({ name: '', location: '', quantity: '', unitPrice: '' });
        setShowInvModal(false);
        showToast(res.error ? `${invForm.name} added locally (backend offline)` : `${invForm.name} saved to database!`);
    };

    const handleDeleteOrder = (id: string) => {
        setOrders(orders.filter(o => o.id !== id));
        showToast(`Order ${id} deleted`, 'info');
    };

    const filteredOrders = orders.filter(o => Object.values(o).some(v => String(v).toLowerCase().includes(search.toLowerCase())));
    const filteredInventory = inventory.filter(o => Object.values(o).some(v => String(v).toLowerCase().includes(search.toLowerCase())));

    return (
        <div className="page-enter">
            {ToastComponent}
            <div className="flex items-center justify-between mb-8">
                <div>
                    <h1 className="text-3xl font-bold mb-2"><span className="text-emerald-400">Supply Chain</span> Management</h1>
                    <p className="text-slate-400">Product inventory, orders, suppliers, and shipment tracking</p>
                </div>
                <div className="flex gap-2">
                    <button onClick={() => setShowOrderModal(true)} className="px-4 py-2 text-sm font-medium text-white rounded-xl bg-gradient-to-r from-emerald-600 to-emerald-700 hover:from-emerald-500 transition-all shadow-lg">➕ Add Order</button>
                    <button onClick={() => setShowInvModal(true)} className="px-4 py-2 text-sm font-medium text-white rounded-xl bg-gradient-to-r from-emerald-600 to-emerald-700 hover:from-emerald-500 transition-all shadow-lg">➕ Add Item</button>
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5 mb-6">
                <StatCard title="Inventory Items" value={loading ? '...' : inventory.length.toLocaleString()} icon="📦" color="emerald" />
                <StatCard title="Active Orders" value={orders.length} icon="📋" color="emerald" />
                <StatCard title="Suppliers" value="87" icon="🏭" color="emerald" subtitle="12 pending" />
                <StatCard title="Shipments" value={shipments.length} icon="🚛" color="emerald" />
            </div>

            <div className="mb-4 max-w-sm"><SearchBar value={search} onChange={setSearch} placeholder="Search orders, inventory, shipments..." /></div>

            <div className="grid grid-cols-1 xl:grid-cols-2 gap-6 mb-6">
                <DataTable title="📦 Inventory" columns={[
                    { key: 'productId', label: 'ID' }, { key: 'name', label: 'Name' }, { key: 'location', label: 'Location' },
                    { key: 'quantity', label: 'Qty', render: (v: number) => <span className={v < 100 ? 'text-rose-400 font-semibold' : 'text-slate-300'}>{typeof v === 'number' ? v.toLocaleString() : v}</span> },
                    { key: 'status', label: 'Status', render: (v: string) => <StatusBadge status={v} variant="dot" /> },
                ]} data={filteredInventory} />
                <DataTable title="📋 Orders" columns={[
                    { key: 'id', label: 'Order', render: (v: string) => <span className="text-emerald-400 font-medium">{v}</span> },
                    { key: 'supplier', label: 'Supplier' }, { key: 'total', label: 'Total' },
                    { key: 'status', label: 'Status', render: (v: string) => <StatusBadge status={v} /> },
                    { key: 'id', label: '', render: (_: any, row: any) => <button onClick={() => handleDeleteOrder(row.id)} className="text-rose-400 hover:text-rose-300 text-xs">✕ Del</button> },
                ]} data={filteredOrders} />
            </div>

            <DataTable title="🚛 Shipments" columns={[
                { key: 'id', label: 'ID', render: (v: string) => <span className="text-emerald-400 font-medium">{v}</span> },
                { key: 'origin', label: 'Origin' }, { key: 'destination', label: 'Destination' },
                { key: 'status', label: 'Status', render: (v: string) => <StatusBadge status={v.replace(/\s+/g, '_')} variant="dot" /> },
                { key: 'eta', label: 'ETA' },
            ]} data={shipments} />

            <Modal isOpen={showOrderModal} onClose={() => setShowOrderModal(false)} title="➕ New Order" onSubmit={handleAddOrder} submitLabel="Create Order" color="emerald">
                <FormField label="Supplier"><FormInput value={orderForm.supplier} onChange={v => setOrderForm({ ...orderForm, supplier: v })} placeholder="e.g. TechCorp Ltd" /></FormField>
                <FormField label="Number of Items"><FormInput value={orderForm.items} onChange={v => setOrderForm({ ...orderForm, items: v })} placeholder="e.g. 5" type="number" /></FormField>
                <FormField label="Total Amount ($)"><FormInput value={orderForm.total} onChange={v => setOrderForm({ ...orderForm, total: v })} placeholder="e.g. 15200" type="number" /></FormField>
            </Modal>

            <Modal isOpen={showInvModal} onClose={() => setShowInvModal(false)} title="➕ New Inventory Item" onSubmit={handleAddInventory} submitLabel="Add Item" color="emerald">
                <FormField label="Product Name"><FormInput value={invForm.name} onChange={v => setInvForm({ ...invForm, name: v })} placeholder="e.g. Sensor Modules" /></FormField>
                <FormField label="Location"><FormSelect value={invForm.location} onChange={v => setInvForm({ ...invForm, location: v })} options={[{ value: 'Warehouse A', label: 'Warehouse A' }, { value: 'Warehouse B', label: 'Warehouse B' }, { value: 'Warehouse C', label: 'Warehouse C' }, { value: 'Warehouse D', label: 'Warehouse D' }]} /></FormField>
                <FormField label="Quantity"><FormInput value={invForm.quantity} onChange={v => setInvForm({ ...invForm, quantity: v })} placeholder="e.g. 500" type="number" /></FormField>
                <FormField label="Unit Price ($)"><FormInput value={invForm.unitPrice} onChange={v => setInvForm({ ...invForm, unitPrice: v })} placeholder="e.g. 12.50" /></FormField>
            </Modal>
        </div>
    );
}
