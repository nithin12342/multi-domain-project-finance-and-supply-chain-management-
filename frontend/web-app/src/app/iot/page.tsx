'use client';
import React, { useState } from 'react';
import StatCard from '../../components/StatCard';
import DataTable from '../../components/DataTable';
import StatusBadge from '../../components/StatusBadge';
import Modal, { FormField, FormInput, FormSelect } from '../../components/Modal';
import { useToast } from '../../components/Toast';

const initDevices = [
    { id: 'IOT-4401', name: 'Temperature Sensor A1', type: 'Temperature', value: '23.5°C', status: 'Online', battery: '87%' },
    { id: 'IOT-4402', name: 'Humidity Sensor B1', type: 'Humidity', value: '62%', status: 'Online', battery: '94%' },
    { id: 'IOT-4403', name: 'GPS Tracker T1', type: 'GPS', value: '34.05°N', status: 'Online', battery: '72%' },
    { id: 'IOT-4404', name: 'Vibration Sensor M1', type: 'Vibration', value: '0.3g', status: 'Warning', battery: '45%' },
    { id: 'IOT-4405', name: 'Pressure Sensor P1', type: 'Pressure', value: '4.2 bar', status: 'Online', battery: '91%' },
    { id: 'IOT-4406', name: 'Weight Sensor W1', type: 'Weight', value: '2,450 kg', status: 'Offline', battery: '12%' },
];

export default function IoTPage() {
    const [devices, setDevices] = useState(initDevices);
    const [showModal, setShowModal] = useState(false);
    const { showToast, ToastComponent } = useToast();
    const [form, setForm] = useState({ name: '', type: '', location: '' });

    const handleRegister = () => {
        if (!form.name) return;
        const d = { id: `IOT-${4406 + devices.length}`, name: form.name, type: form.type || 'Generic', value: '—', status: 'Online', battery: '100%' };
        setDevices([d, ...devices]);
        setForm({ name: '', type: '', location: '' });
        setShowModal(false);
        showToast(`Device ${d.id} registered!`);
    };

    const toggleDevice = (id: string) => {
        setDevices(devices.map(d => d.id === id ? { ...d, status: d.status === 'Online' ? 'Offline' : 'Online' } : d));
        showToast(`Device ${id} toggled`, 'info');
    };

    return (
        <div className="page-enter">
            {ToastComponent}
            <div className="flex items-center justify-between mb-8">
                <div>
                    <h1 className="text-3xl font-bold mb-2"><span className="text-rose-400">IoT</span> Dashboard</h1>
                    <p className="text-slate-400">Device management, sensor monitoring, and predictive maintenance</p>
                </div>
                <button onClick={() => setShowModal(true)} className="px-4 py-2 text-sm font-medium text-white rounded-xl bg-gradient-to-r from-rose-600 to-rose-700 hover:from-rose-500 transition-all shadow-lg">➕ Register Device</button>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5 mb-6">
                <StatCard title="Total Devices" value={devices.length} icon="📡" color="rose" />
                <StatCard title="Online" value={devices.filter(d => d.status === 'Online').length} icon="✅" color="emerald" />
                <StatCard title="Warnings" value={devices.filter(d => d.status === 'Warning').length} icon="⚠️" color="amber" />
                <StatCard title="Offline" value={devices.filter(d => d.status === 'Offline').length} icon="🔴" color="rose" />
            </div>
            <DataTable title="📡 Devices" columns={[
                { key: 'id', label: 'Device', render: (v: string) => <span className="text-rose-400 font-mono text-xs">{v}</span> },
                { key: 'name', label: 'Name' }, { key: 'type', label: 'Type' },
                { key: 'value', label: 'Reading', render: (v: string) => <span className="text-rose-300 font-medium">{v}</span> },
                {
                    key: 'battery', label: 'Battery', render: (v: string) => {
                        const p = parseInt(v);
                        return <span className={p > 50 ? 'text-emerald-400' : p > 20 ? 'text-amber-400' : 'text-rose-400'}>{v}</span>;
                    }
                },
                { key: 'status', label: 'Status', render: (v: string) => <StatusBadge status={v} variant="dot" /> },
                {
                    key: 'id', label: 'Toggle', render: (_: any, row: any) => (
                        <button onClick={() => toggleDevice(row.id)} className={`px-2 py-0.5 text-[10px] rounded-md ${row.status === 'Online' ? 'bg-rose-500/20 text-rose-400' : 'bg-emerald-500/20 text-emerald-400'}`}>
                            {row.status === 'Online' ? '⏸ Off' : '▶ On'}
                        </button>
                    )
                },
            ]} data={devices} />
            <Modal isOpen={showModal} onClose={() => setShowModal(false)} title="➕ Register Device" onSubmit={handleRegister} submitLabel="Register" color="rose">
                <FormField label="Device Name"><FormInput value={form.name} onChange={v => setForm({ ...form, name: v })} placeholder="e.g. Temp Sensor X2" /></FormField>
                <FormField label="Sensor Type"><FormSelect value={form.type} onChange={v => setForm({ ...form, type: v })} options={[{ value: 'Temperature', label: 'Temperature' }, { value: 'Humidity', label: 'Humidity' }, { value: 'GPS', label: 'GPS' }, { value: 'Vibration', label: 'Vibration' }, { value: 'Pressure', label: 'Pressure' }, { value: 'Weight', label: 'Weight' }]} /></FormField>
                <FormField label="Location"><FormInput value={form.location} onChange={v => setForm({ ...form, location: v })} placeholder="e.g. Factory Floor" /></FormField>
            </Modal>
        </div>
    );
}
