import React from 'react';

interface StatusBadgeProps {
    status: string;
    variant?: 'default' | 'dot';
}

const statusColors: Record<string, string> = {
    active: 'bg-emerald-500/20 text-emerald-400',
    completed: 'bg-emerald-500/20 text-emerald-400',
    delivered: 'bg-emerald-500/20 text-emerald-400',
    paid: 'bg-emerald-500/20 text-emerald-400',
    online: 'bg-emerald-500/20 text-emerald-400',
    processing: 'bg-cyan-500/20 text-cyan-400',
    in_transit: 'bg-cyan-500/20 text-cyan-400',
    approved: 'bg-violet-500/20 text-violet-400',
    financed: 'bg-indigo-500/20 text-indigo-400',
    pending: 'bg-amber-500/20 text-amber-400',
    confirmed: 'bg-amber-500/20 text-amber-400',
    overdue: 'bg-rose-500/20 text-rose-400',
    cancelled: 'bg-rose-500/20 text-rose-400',
    failed: 'bg-rose-500/20 text-rose-400',
    offline: 'bg-rose-500/20 text-rose-400',
    inactive: 'bg-slate-500/20 text-slate-400',
    warning: 'bg-amber-500/20 text-amber-400',
    critical: 'bg-rose-500/20 text-rose-400',
    low: 'bg-emerald-500/20 text-emerald-400',
    medium: 'bg-amber-500/20 text-amber-400',
    high: 'bg-rose-500/20 text-rose-400',
};

export default function StatusBadge({ status, variant = 'default' }: StatusBadgeProps) {
    const normalizedStatus = status.toLowerCase().replace(/\s+/g, '_');
    const colorClass = statusColors[normalizedStatus] || 'bg-slate-500/20 text-slate-400';

    return (
        <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold ${colorClass}`}>
            {variant === 'dot' && <span className="w-1.5 h-1.5 rounded-full bg-current pulse-dot" />}
            {status}
        </span>
    );
}
