'use client';
import React, { useState } from 'react';
import StatusBadge from '../../components/StatusBadge';
import { useToast } from '../../components/Toast';

const initServices = [
    { name: 'Supply Chain Service', port: 8080, endpoint: '/api/supply', status: 'Unknown', color: 'text-emerald-400' },
    { name: 'Auth Service', port: 8081, endpoint: '/api/auth', status: 'Unknown', color: 'text-violet-400' },
    { name: 'AI Service', port: 8082, endpoint: '/api/ai', status: 'Unknown', color: 'text-violet-400' },
    { name: 'Finance Service', port: 8083, endpoint: '/api/finance', status: 'Unknown', color: 'text-amber-400' },
    { name: 'Blockchain Service', port: 8084, endpoint: '/api/blockchain', status: 'Unknown', color: 'text-cyan-400' },
    { name: 'DeFi Service', port: 8085, endpoint: '/api/defi', status: 'Unknown', color: 'text-indigo-400' },
];

export default function SettingsPage() {
    const [services, setServices] = useState(initServices);
    const [testing, setTesting] = useState<string | null>(null);
    const { showToast, ToastComponent } = useToast();

    const testConnection = async (port: number) => {
        setTesting(String(port));
        try {
            const res = await fetch(`http://localhost:${port}/actuator/health`, { signal: AbortSignal.timeout(3000) });
            if (res.ok) {
                setServices(s => s.map(sv => sv.port === port ? { ...sv, status: 'Online' } : sv));
                showToast(`Port ${port} is reachable!`);
            } else {
                setServices(s => s.map(sv => sv.port === port ? { ...sv, status: 'Online' } : sv));
                showToast(`Port ${port} responded (status ${res.status})`, 'info');
            }
        } catch {
            setServices(s => s.map(sv => sv.port === port ? { ...sv, status: 'Offline' } : sv));
            showToast(`Port ${port} is unreachable`, 'error');
        }
        setTesting(null);
    };

    const testAll = () => { services.forEach(s => testConnection(s.port)); };

    return (
        <div className="page-enter">
            {ToastComponent}
            <div className="flex items-center justify-between mb-8">
                <div>
                    <h1 className="text-3xl font-bold mb-2"><span className="gradient-text">Platform</span> Settings</h1>
                    <p className="text-slate-400">Backend service health and system configuration</p>
                </div>
                <button onClick={testAll} className="px-4 py-2 text-sm font-medium text-white rounded-xl bg-gradient-to-r from-violet-600 to-indigo-700 hover:from-violet-500 transition-all shadow-lg">🔄 Test All</button>
            </div>

            <div className="glass-card p-6 mb-6">
                <h3 className="text-sm font-semibold text-slate-200 mb-4">🩺 Backend Service Health</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {services.map((s, i) => (
                        <div key={i} className={`bg-slate-800/50 rounded-xl p-4 border ${s.status === 'Online' ? 'border-emerald-500/20' : s.status === 'Offline' ? 'border-rose-500/20' : 'border-slate-700/30'}`}>
                            <div className="flex items-center justify-between mb-3">
                                <h4 className={`text-sm font-semibold ${s.color}`}>{s.name}</h4>
                                <StatusBadge status={s.status} variant="dot" />
                            </div>
                            <div className="space-y-1.5 mb-3">
                                <div className="flex justify-between text-xs"><span className="text-slate-500">Port</span><span className="text-slate-300 font-mono">{s.port}</span></div>
                                <div className="flex justify-between text-xs"><span className="text-slate-500">Endpoint</span><span className="text-slate-300 font-mono">{s.endpoint}</span></div>
                            </div>
                            <button onClick={() => testConnection(s.port)} disabled={testing === String(s.port)}
                                className="w-full px-3 py-1.5 text-xs font-medium rounded-lg bg-slate-700/50 text-slate-300 hover:bg-slate-700 hover:text-white transition-all disabled:opacity-50">
                                {testing === String(s.port) ? '⏳ Testing...' : '🔄 Test Connection'}
                            </button>
                        </div>
                    ))}
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div className="glass-card p-6">
                    <h3 className="text-sm font-semibold text-slate-200 mb-4">ℹ️ System Info</h3>
                    {[['Platform Version', 'v2.1.0'], ['Build', '2025.10.08-rc1'], ['Environment', 'Development (Local)'], ['Java Runtime', 'OpenJDK 17'], ['Spring Boot', '3.x'], ['Frontend', 'Next.js 13.5'], ['Database', 'H2 In-Memory'], ['Node.js', 'v18.x']].map(([k, v], i) => (
                        <div key={i} className="flex justify-between py-2 border-b border-slate-800/50 last:border-0">
                            <span className="text-xs text-slate-500">{k}</span><span className="text-xs text-slate-300">{v}</span>
                        </div>
                    ))}
                </div>
                <div className="glass-card p-6">
                    <h3 className="text-sm font-semibold text-slate-200 mb-4">🎨 Domain Colors</h3>
                    {[['Supply Chain', 'bg-emerald-500', 'text-emerald-400'], ['Finance', 'bg-amber-500', 'text-amber-400'], ['AI / ML', 'bg-violet-500', 'text-violet-400'], ['Blockchain', 'bg-cyan-500', 'text-cyan-400'], ['IoT', 'bg-rose-500', 'text-rose-400'], ['DeFi', 'bg-indigo-500', 'text-indigo-400']].map(([d, bg, t], i) => (
                        <div key={i} className="flex items-center gap-3 py-1"><span className={`w-3 h-3 rounded-full ${bg}`} /><span className={`text-sm ${t}`}>{d}</span></div>
                    ))}
                </div>
            </div>
        </div>
    );
}
