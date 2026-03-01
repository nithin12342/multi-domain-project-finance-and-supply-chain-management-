'use client';
import React, { useState, useEffect, useCallback } from 'react';

interface ToastProps {
    message: string;
    type?: 'success' | 'error' | 'info';
    onClose: () => void;
}

const typeStyles = {
    success: 'border-emerald-500/30 bg-emerald-500/10 text-emerald-400',
    error: 'border-rose-500/30 bg-rose-500/10 text-rose-400',
    info: 'border-cyan-500/30 bg-cyan-500/10 text-cyan-400',
};

const typeIcons = { success: '✓', error: '✕', info: 'ℹ' };

export default function Toast({ message, type = 'success', onClose }: ToastProps) {
    const [visible, setVisible] = useState(false);

    useEffect(() => {
        setVisible(true);
        const timer = setTimeout(() => { setVisible(false); setTimeout(onClose, 300); }, 3000);
        return () => clearTimeout(timer);
    }, [onClose]);

    return (
        <div className={`fixed top-6 right-6 z-[200] transition-all duration-300 ${visible ? 'translate-x-0 opacity-100' : 'translate-x-8 opacity-0'}`}>
            <div className={`flex items-center gap-3 px-4 py-3 rounded-xl border backdrop-blur-xl shadow-2xl ${typeStyles[type]}`}>
                <span className="text-lg font-bold">{typeIcons[type]}</span>
                <span className="text-sm font-medium">{message}</span>
                <button onClick={() => { setVisible(false); setTimeout(onClose, 300); }} className="ml-2 opacity-60 hover:opacity-100 transition-opacity">✕</button>
            </div>
        </div>
    );
}

// Hook for easy toast management
export function useToast() {
    const [toast, setToast] = useState<{ message: string; type: 'success' | 'error' | 'info' } | null>(null);

    const showToast = useCallback((message: string, type: 'success' | 'error' | 'info' = 'success') => {
        setToast({ message, type });
    }, []);

    const ToastComponent = toast ? <Toast message={toast.message} type={toast.type} onClose={() => setToast(null)} /> : null;

    return { showToast, ToastComponent };
}
