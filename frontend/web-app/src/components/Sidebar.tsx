'use client';
import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

const navItems = [
    { href: '/', label: 'Dashboard', icon: '◈', color: 'text-slate-300' },
    { href: '/supply-chain', label: 'Supply Chain', icon: '🟢', color: 'text-emerald-400' },
    { href: '/finance', label: 'Finance', icon: '🟡', color: 'text-amber-400' },
    { href: '/analytics', label: 'AI / ML', icon: '🟣', color: 'text-violet-400' },
    { href: '/blockchain', label: 'Blockchain', icon: '🔵', color: 'text-cyan-400' },
    { href: '/iot', label: 'IoT', icon: '🔴', color: 'text-rose-400' },
    { href: '/defi', label: 'DeFi', icon: '🔷', color: 'text-indigo-400' },
    { href: '/users', label: 'Users', icon: '👥', color: 'text-slate-300' },
    { href: '/optimization', label: 'Optimize', icon: '⚡', color: 'text-slate-300' },
    { href: '/settings', label: 'Settings', icon: '⚙️', color: 'text-slate-300' },
];

export default function Sidebar() {
    const pathname = usePathname();

    return (
        <aside className="fixed left-0 top-0 h-screen w-64 bg-slate-900/95 backdrop-blur-xl border-r border-slate-700/50 flex flex-col z-50">
            {/* Logo */}
            <div className="p-6 border-b border-slate-700/50">
                <h1 className="text-xl font-bold gradient-text">SCF Platform</h1>
                <p className="text-xs text-slate-500 mt-1">Multi-Domain Enterprise</p>
            </div>

            {/* Navigation */}
            <nav className="flex-1 py-4 px-3 overflow-y-auto">
                <p className="text-[10px] uppercase tracking-widest text-slate-600 px-3 mb-3">Domains</p>
                {navItems.map((item) => {
                    const isActive = pathname === item.href;
                    return (
                        <Link
                            key={item.href}
                            href={item.href}
                            className={`flex items-center gap-3 px-3 py-2.5 rounded-xl mb-1 text-sm font-medium transition-all duration-200
                ${isActive
                                    ? 'bg-slate-700/60 text-white shadow-lg'
                                    : 'text-slate-400 hover:bg-slate-800/60 hover:text-slate-200'
                                }`}
                        >
                            <span className="text-base">{item.icon}</span>
                            <span>{item.label}</span>
                            {isActive && (
                                <span className="ml-auto w-1.5 h-1.5 rounded-full bg-violet-400 pulse-dot" />
                            )}
                        </Link>
                    );
                })}
            </nav>

            {/* Footer */}
            <div className="p-4 border-t border-slate-700/50">
                <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-full bg-gradient-to-br from-violet-500 to-indigo-600 flex items-center justify-center text-xs font-bold">A</div>
                    <div>
                        <p className="text-xs font-medium text-slate-300">Admin</p>
                        <p className="text-[10px] text-slate-500">Platform Owner</p>
                    </div>
                </div>
            </div>
        </aside>
    );
}
