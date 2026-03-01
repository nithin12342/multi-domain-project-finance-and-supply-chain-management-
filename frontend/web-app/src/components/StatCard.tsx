import React from 'react';

interface StatCardProps {
    title: string;
    value: string | number;
    subtitle?: string;
    icon: string;
    color: 'emerald' | 'amber' | 'violet' | 'cyan' | 'rose' | 'indigo' | 'slate';
    trend?: { value: number; label: string };
}

const colorMap = {
    emerald: { bg: 'from-emerald-500/20 to-emerald-600/5', text: 'text-emerald-400', border: 'border-emerald-500/20', glow: 'border-glow-emerald' },
    amber: { bg: 'from-amber-500/20 to-amber-600/5', text: 'text-amber-400', border: 'border-amber-500/20', glow: 'border-glow-amber' },
    violet: { bg: 'from-violet-500/20 to-violet-600/5', text: 'text-violet-400', border: 'border-violet-500/20', glow: 'border-glow-violet' },
    cyan: { bg: 'from-cyan-500/20 to-cyan-600/5', text: 'text-cyan-400', border: 'border-cyan-500/20', glow: 'border-glow-cyan' },
    rose: { bg: 'from-rose-500/20 to-rose-600/5', text: 'text-rose-400', border: 'border-rose-500/20', glow: 'border-glow-rose' },
    indigo: { bg: 'from-indigo-500/20 to-indigo-600/5', text: 'text-indigo-400', border: 'border-indigo-500/20', glow: 'border-glow-indigo' },
    slate: { bg: 'from-slate-500/20 to-slate-600/5', text: 'text-slate-300', border: 'border-slate-500/20', glow: '' },
};

export default function StatCard({ title, value, subtitle, icon, color, trend }: StatCardProps) {
    const c = colorMap[color];
    return (
        <div className={`glass-card p-5 bg-gradient-to-br ${c.bg} ${c.glow}`}>
            <div className="flex items-start justify-between mb-3">
                <span className="text-2xl">{icon}</span>
                {trend && (
                    <span className={`text-xs font-semibold px-2 py-0.5 rounded-full ${trend.value >= 0 ? 'bg-emerald-500/20 text-emerald-400' : 'bg-rose-500/20 text-rose-400'}`}>
                        {trend.value >= 0 ? '↑' : '↓'} {Math.abs(trend.value)}%
                    </span>
                )}
            </div>
            <p className="text-xs text-slate-400 uppercase tracking-wider mb-1">{title}</p>
            <p className={`text-2xl font-bold ${c.text}`}>{value}</p>
            {subtitle && <p className="text-xs text-slate-500 mt-1">{subtitle}</p>}
        </div>
    );
}
