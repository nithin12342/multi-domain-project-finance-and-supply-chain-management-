'use client';
import React, { useState } from 'react';
import StatCard from '../../components/StatCard';
import Modal, { FormField, FormInput, FormSelect } from '../../components/Modal';
import { useToast } from '../../components/Toast';

const benchmarks = [
  { name: 'Route Optimization', wasmTime: '12ms', jsTime: '340ms', speedup: '28x' },
  { name: 'Matrix Operations', wasmTime: '3ms', jsTime: '87ms', speedup: '29x' },
  { name: 'Data Compression', wasmTime: '8ms', jsTime: '195ms', speedup: '24x' },
  { name: 'Crypto Hashing', wasmTime: '1ms', jsTime: '45ms', speedup: '45x' },
];

export default function OptimizationPage() {
  const [showModal, setShowModal] = useState(false);
  const [result, setResult] = useState<{ origin: string; dest: string; original: number; optimized: number; savings: string; distance: string } | null>(null);
  const { showToast, ToastComponent } = useToast();
  const [form, setForm] = useState({ origin: '', destination: '', weight: '' });

  const handleOptimize = () => {
    if (!form.origin || !form.destination) return;
    const baseCost = 5000 + Math.random() * 15000;
    const savings = 15 + Math.random() * 15;
    const optimized = baseCost * (1 - savings / 100);
    const distance = (5000 + Math.random() * 15000).toFixed(0);
    setResult({
      origin: form.origin, dest: form.destination,
      original: Math.round(baseCost), optimized: Math.round(optimized),
      savings: savings.toFixed(1) + '%', distance: `${parseInt(distance).toLocaleString()} km`,
    });
    setShowModal(false);
    showToast(`Route optimized! Saving ${savings.toFixed(1)}%`);
  };

  return (
    <div className="page-enter">
      {ToastComponent}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold mb-2"><span className="gradient-text">Optimization</span> Tools</h1>
          <p className="text-slate-400">WebAssembly-powered route optimization and cost analysis</p>
        </div>
        <button onClick={() => { setResult(null); setShowModal(true); }} className="px-4 py-2 text-sm font-medium text-white rounded-xl bg-gradient-to-r from-violet-600 to-indigo-700 hover:from-violet-500 transition-all shadow-lg">🗺️ Optimize Route</button>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5 mb-6">
        <StatCard title="WASM Modules" value="4" icon="⚡" color="violet" />
        <StatCard title="Avg Speedup" value="31.5x" icon="🚀" color="emerald" />
        <StatCard title="Routes Optimized" value="842" icon="🗺️" color="cyan" />
        <StatCard title="Avg Savings" value="21.3%" icon="💰" color="amber" />
      </div>

      {/* Route Optimization Result */}
      {result && (
        <div className="glass-card p-5 mb-6 border-glow-emerald">
          <h3 className="text-sm font-semibold text-emerald-400 mb-3">🗺️ Optimization Result — {result.origin} → {result.dest}</h3>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="bg-slate-800/50 rounded-xl p-4">
              <p className="text-xs text-slate-500 mb-1">Original Cost</p>
              <p className="text-lg font-bold text-slate-400 line-through">${result.original.toLocaleString()}</p>
            </div>
            <div className="bg-slate-800/50 rounded-xl p-4">
              <p className="text-xs text-slate-500 mb-1">Optimized Cost</p>
              <p className="text-lg font-bold text-emerald-400">${result.optimized.toLocaleString()}</p>
            </div>
            <div className="bg-slate-800/50 rounded-xl p-4">
              <p className="text-xs text-slate-500 mb-1">Savings</p>
              <p className="text-lg font-bold text-amber-400">↓ {result.savings}</p>
            </div>
            <div className="bg-slate-800/50 rounded-xl p-4">
              <p className="text-xs text-slate-500 mb-1">Distance</p>
              <p className="text-lg font-bold text-cyan-400">{result.distance}</p>
            </div>
          </div>
        </div>
      )}

      {/* WASM Benchmarks */}
      <div className="glass-card p-6">
        <h3 className="text-sm font-semibold text-slate-200 mb-4">⚡ WebAssembly Performance Benchmarks</h3>
        <div className="space-y-3">
          {benchmarks.map((b, i) => (
            <div key={i} className="flex items-center gap-4 py-3 border-b border-slate-800/50 last:border-0">
              <div className="w-40"><p className="text-sm text-slate-200 font-medium">{b.name}</p></div>
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-[10px] text-slate-500 w-14">WASM</span>
                  <div className="flex-1 h-2 bg-slate-800 rounded-full overflow-hidden"><div className="h-full bg-gradient-to-r from-violet-500 to-indigo-500 rounded-full" style={{ width: '8%' }} /></div>
                  <span className="text-xs text-violet-400 w-16 text-right">{b.wasmTime}</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-[10px] text-slate-500 w-14">JS</span>
                  <div className="flex-1 h-2 bg-slate-800 rounded-full overflow-hidden"><div className="h-full bg-gradient-to-r from-amber-500/60 to-rose-500/40 rounded-full" style={{ width: '95%' }} /></div>
                  <span className="text-xs text-amber-400 w-16 text-right">{b.jsTime}</span>
                </div>
              </div>
              <div className="text-right w-16"><span className="text-lg font-bold text-emerald-400">{b.speedup}</span></div>
            </div>
          ))}
        </div>
      </div>

      <Modal isOpen={showModal} onClose={() => setShowModal(false)} title="🗺️ Optimize Route" onSubmit={handleOptimize} submitLabel="Run Optimization" color="emerald">
        <FormField label="Origin"><FormInput value={form.origin} onChange={v => setForm({ ...form, origin: v })} placeholder="e.g. Shanghai, CN" /></FormField>
        <FormField label="Destination"><FormInput value={form.destination} onChange={v => setForm({ ...form, destination: v })} placeholder="e.g. Los Angeles, US" /></FormField>
        <FormField label="Cargo Weight (kg)"><FormInput value={form.weight} onChange={v => setForm({ ...form, weight: v })} placeholder="e.g. 5000" type="number" /></FormField>
      </Modal>
    </div>
  );
}