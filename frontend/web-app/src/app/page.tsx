import React from 'react';
import Link from 'next/link';
import StatCard from '../components/StatCard';

const domains = [
  { name: 'Supply Chain', href: '/supply-chain', icon: '📦', color: 'emerald' as const, status: 'Operational', items: '4 Services', desc: 'Inventory, Orders, Suppliers, Shipments' },
  { name: 'Finance', href: '/finance', icon: '💰', color: 'amber' as const, status: 'Operational', items: '3 Services', desc: 'Invoices, Payments, Risk Assessment' },
  { name: 'AI / ML Analytics', href: '/analytics', icon: '🧠', color: 'violet' as const, status: 'Operational', items: '6 Services', desc: 'Forecasting, Fraud Detection, AutoML' },
  { name: 'Blockchain', href: '/blockchain', icon: '⛓️', color: 'cyan' as const, status: 'Operational', items: '3 Services', desc: 'Smart Contracts, Ledger, Cross-chain' },
  { name: 'IoT', href: '/iot', icon: '📡', color: 'rose' as const, status: 'Operational', items: '4 Services', desc: 'Devices, Sensors, Edge Computing' },
  { name: 'DeFi', href: '/defi', icon: '🔮', color: 'indigo' as const, status: 'Operational', items: '3 Services', desc: 'Yield, Liquidity, Protocol Metrics' },
];

const colorBorder: Record<string, string> = {
  emerald: 'border-emerald-500/30 hover:border-emerald-400/50',
  amber: 'border-amber-500/30 hover:border-amber-400/50',
  violet: 'border-violet-500/30 hover:border-violet-400/50',
  cyan: 'border-cyan-500/30 hover:border-cyan-400/50',
  rose: 'border-rose-500/30 hover:border-rose-400/50',
  indigo: 'border-indigo-500/30 hover:border-indigo-400/50',
};

const colorText: Record<string, string> = {
  emerald: 'text-emerald-400',
  amber: 'text-amber-400',
  violet: 'text-violet-400',
  cyan: 'text-cyan-400',
  rose: 'text-rose-400',
  indigo: 'text-indigo-400',
};

export default function Home() {
  return (
    <div className="page-enter">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">
          Welcome to <span className="gradient-text">SCF Platform</span>
        </h1>
        <p className="text-slate-400">Multi-Domain Supply Chain Finance • Executive Overview</p>
      </div>

      {/* Top KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5 mb-8">
        <StatCard title="Total Orders" value="2,847" icon="📋" color="emerald" trend={{ value: 12.5, label: 'vs last month' }} />
        <StatCard title="Revenue" value="$4.2M" icon="💵" color="amber" trend={{ value: 8.3, label: 'vs last month' }} />
        <StatCard title="Active Shipments" value="342" icon="🚚" color="cyan" trend={{ value: -2.1, label: 'vs last week' }} />
        <StatCard title="AI Risk Score" value="78/100" icon="🛡️" color="violet" subtitle="Low risk detected" />
      </div>

      {/* Domain Cards Grid */}
      <div className="mb-6">
        <h2 className="text-lg font-semibold text-slate-200 mb-4">Platform Domains</h2>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5 mb-8">
        {domains.map((domain) => (
          <Link key={domain.name} href={domain.href}>
            <div className={`glass-card p-5 border ${colorBorder[domain.color]} cursor-pointer group`}>
              <div className="flex items-center gap-3 mb-3">
                <span className="text-2xl">{domain.icon}</span>
                <div>
                  <h3 className={`text-base font-semibold ${colorText[domain.color]}`}>{domain.name}</h3>
                  <p className="text-[11px] text-slate-500">{domain.items}</p>
                </div>
                <div className="ml-auto flex items-center gap-1.5">
                  <span className="w-2 h-2 rounded-full bg-emerald-400 pulse-dot" />
                  <span className="text-[10px] text-emerald-400 font-medium">{domain.status}</span>
                </div>
              </div>
              <p className="text-xs text-slate-400">{domain.desc}</p>
              <div className="mt-3 text-xs text-slate-500 group-hover:text-slate-300 transition-colors">
                View Dashboard →
              </div>
            </div>
          </Link>
        ))}
      </div>

      {/* Activity Feed */}
      <div className="glass-card p-5">
        <h3 className="text-sm font-semibold text-slate-200 mb-4">Recent Platform Activity</h3>
        <div className="space-y-3">
          {[
            { time: '2 min ago', event: 'New order #ORD-2847 created by Supplier TechCorp', color: 'text-emerald-400' },
            { time: '5 min ago', event: 'Invoice #INV-1923 approved and financed ($150,000)', color: 'text-amber-400' },
            { time: '12 min ago', event: 'AI fraud detection flagged transaction TX-8821', color: 'text-violet-400' },
            { time: '18 min ago', event: 'Smart contract SC-0x7f deployed to Hyperledger', color: 'text-cyan-400' },
            { time: '25 min ago', event: 'IoT sensor SN-4401 temperature alert triggered', color: 'text-rose-400' },
            { time: '31 min ago', event: 'DeFi yield pool APY updated to 8.2%', color: 'text-indigo-400' },
          ].map((item, i) => (
            <div key={i} className="flex items-start gap-3 py-2 border-b border-slate-800/50 last:border-0">
              <span className="text-[10px] text-slate-500 w-20 shrink-0 pt-0.5">{item.time}</span>
              <p className={`text-sm ${item.color}`}>{item.event}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}