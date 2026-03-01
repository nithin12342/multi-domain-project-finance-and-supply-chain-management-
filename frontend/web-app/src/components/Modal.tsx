'use client';
import React, { useEffect } from 'react';

interface ModalProps {
    isOpen: boolean;
    onClose: () => void;
    title: string;
    children: React.ReactNode;
    onSubmit?: () => void;
    submitLabel?: string;
    color?: string;
}

export default function Modal({ isOpen, onClose, title, children, onSubmit, submitLabel = 'Create', color = 'violet' }: ModalProps) {
    useEffect(() => {
        if (isOpen) document.body.style.overflow = 'hidden';
        else document.body.style.overflow = '';
        return () => { document.body.style.overflow = ''; };
    }, [isOpen]);

    if (!isOpen) return null;

    const colorMap: Record<string, string> = {
        emerald: 'from-emerald-600 to-emerald-700 hover:from-emerald-500',
        amber: 'from-amber-600 to-amber-700 hover:from-amber-500',
        violet: 'from-violet-600 to-violet-700 hover:from-violet-500',
        cyan: 'from-cyan-600 to-cyan-700 hover:from-cyan-500',
        rose: 'from-rose-600 to-rose-700 hover:from-rose-500',
        indigo: 'from-indigo-600 to-indigo-700 hover:from-indigo-500',
    };

    return (
        <div className="fixed inset-0 z-[100] flex items-center justify-center">
            <div className="absolute inset-0 bg-black/60 backdrop-blur-sm" onClick={onClose} />
            <div className="relative bg-slate-800 border border-slate-700/50 rounded-2xl shadow-2xl w-full max-w-lg mx-4 max-h-[90vh] overflow-y-auto">
                <div className="flex items-center justify-between p-5 border-b border-slate-700/50">
                    <h2 className="text-lg font-semibold text-slate-100">{title}</h2>
                    <button onClick={onClose} className="text-slate-400 hover:text-slate-200 text-xl transition-colors">✕</button>
                </div>
                <div className="p-5 space-y-4">
                    {children}
                </div>
                {onSubmit && (
                    <div className="flex justify-end gap-3 p-5 border-t border-slate-700/50">
                        <button onClick={onClose} className="px-4 py-2 text-sm text-slate-400 hover:text-slate-200 rounded-lg transition-colors">Cancel</button>
                        <button onClick={onSubmit} className={`px-5 py-2 text-sm font-medium text-white rounded-lg bg-gradient-to-r ${colorMap[color] || colorMap.violet} transition-all shadow-lg`}>
                            {submitLabel}
                        </button>
                    </div>
                )}
            </div>
        </div>
    );
}

// Reusable form field
export function FormField({ label, children }: { label: string; children: React.ReactNode }) {
    return (
        <div>
            <label className="block text-xs font-medium text-slate-400 mb-1.5">{label}</label>
            {children}
        </div>
    );
}

// Reusable input
export function FormInput({ value, onChange, placeholder, type = 'text' }: { value: string; onChange: (v: string) => void; placeholder?: string; type?: string }) {
    return (
        <input
            type={type}
            value={value}
            onChange={(e) => onChange(e.target.value)}
            placeholder={placeholder}
            className="w-full px-3 py-2 bg-slate-900/50 border border-slate-700/50 rounded-lg text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:border-violet-500/50 focus:ring-1 focus:ring-violet-500/30 transition-all"
        />
    );
}

// Reusable select
export function FormSelect({ value, onChange, options }: { value: string; onChange: (v: string) => void; options: { value: string; label: string }[] }) {
    return (
        <select
            value={value}
            onChange={(e) => onChange(e.target.value)}
            className="w-full px-3 py-2 bg-slate-900/50 border border-slate-700/50 rounded-lg text-sm text-slate-200 focus:outline-none focus:border-violet-500/50 transition-all"
        >
            <option value="">Select...</option>
            {options.map((o) => <option key={o.value} value={o.value}>{o.label}</option>)}
        </select>
    );
}
