'use client';

import { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { motion } from 'framer-motion';
import {
    Home, FileText, Banknote, ShieldCheck, Activity,
    PieChart, Users, FileDigit, Smartphone, Cpu, Settings, CheckCircle,
    Truck, ScrollText, Calculator, BookOpen, LogOut
} from 'lucide-react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';
import { useAuth } from '@/context/AuthContext';

// Definición robusta de los items del menú
const menuItems = [
    { icon: Home, label: 'Inicio / Dashboard', href: '/dashboard' },
    { icon: ShieldCheck, label: 'Auditoría DIAN', href: '/dashboard/dian-audit' },
    { icon: FileText, label: 'Minería XML', href: '/dashboard/xml-mining' },
    { icon: Banknote, label: 'Conciliación Bancaria', href: '/dashboard/bank-reconcile' },
    { icon: Activity, label: 'Auditoría Fiscal', href: '/dashboard/fiscal-audit' },
    { icon: Users, label: 'Nómina UGPP', href: '/dashboard/ugpp' },
    { icon: PieChart, label: 'Tesorería', href: '/dashboard/treasury' },

    // Modules restaurados
    { icon: Calculator, label: 'Costeo Nómina Real', href: '/dashboard/payroll-cost' },

    { icon: Cpu, label: 'Inteligencia Fin.', href: '/dashboard/financial-ai' },

    // Modules restaurados
    { icon: BookOpen, label: 'Narrador NIIF', href: '/dashboard/storyteller' },

    { icon: CheckCircle, label: 'Validador RUT', href: '/dashboard/rut-validator' },
    { icon: FileDigit, label: 'OCR Facturas', href: '/dashboard/ocr' },
    { icon: ScrollText, label: 'Cotizaciones', href: '/dashboard/quotes' },
    { icon: Truck, label: 'Logística', href: '/dashboard/logistics' },
];

export function Sidebar() {
    const pathname = usePathname();
    const [isExpanded, setIsExpanded] = useState(true);
    const { user, logout } = useAuth();

    return (
        <motion.aside
            initial={{ width: 280 }}
            animate={{ width: isExpanded ? 280 : 80 }}
            className="glass-panel h-screen fixed left-0 top-0 z-50 flex flex-col border-r border-white/10"
        >
            <div className="p-6 flex items-center gap-3 border-b border-white/5">
                <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center shadow-lg shadow-indigo-500/30">
                    <span className="font-bold text-white">A</span>
                </div>
                {isExpanded && (
                    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                        <h1 className="font-bold text-lg bg-clip-text text-transparent bg-gradient-to-r from-white to-indigo-200">
                            Asistente Pro
                        </h1>
                        <div className="flex flex-col gap-1 items-start">
                            <p className="text-xs text-slate-400 font-medium">Suite v15.1</p>
                            <span className="px-2 py-0.5 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-[10px] font-bold text-emerald-400 flex items-center gap-1">
                                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
                                Normativa 2026 Activa
                            </span>
                        </div>
                    </motion.div>
                )}
            </div>

            <nav className="flex-1 overflow-y-auto py-4 px-3 space-y-1 custom-scrollbar">
                {menuItems.map((item) => {
                    const isActive = pathname === item.href;
                    return (
                        <Link
                            key={item.href}
                            href={item.href}
                            className={twMerge(
                                "flex items-center gap-3 px-3 py-3 rounded-xl transition-all duration-200 group relative overflow-hidden",
                                isActive
                                    ? "bg-indigo-600/20 text-indigo-300 shadow-lg shadow-indigo-900/20 ring-1 ring-indigo-500/40"
                                    : "text-slate-400 hover:bg-white/5 hover:text-white"
                            )}
                        >
                            <item.icon className={clsx("w-5 h-5 min-w-[20px]", isActive ? "text-indigo-400" : "text-slate-500 group-hover:text-indigo-400")} />
                            {isExpanded && (
                                <span className="text-sm font-medium whitespace-nowrap">{item.label}</span>
                            )}
                            {isActive && <div className="absolute right-0 top-1/2 -translate-y-1/2 w-1 h-8 bg-indigo-500 rounded-l-full blur-[2px]" />}
                        </Link>
                    );
                })}
            </nav>

            {/* Profile Section */}
            <div className="p-4 border-t border-white/5">
                {user && (
                    <div className={clsx("flex items-center gap-3 mb-4", !isExpanded && "justify-center")}>
                        <div className="w-8 h-8 rounded-full bg-slate-700 overflow-hidden border border-white/10 shrink-0">
                            {user.avatar && <img src={user.avatar} alt="Avatar" className="w-full h-full object-cover" />}
                        </div>
                        {isExpanded && (
                            <div className="flex-1 min-w-0">
                                <Link href="/dashboard/profile" className="hover:opacity-80 transition-opacity">
                                    <p className="text-sm font-bold text-white truncate hover:text-indigo-400 transition-colors">{user.name}</p>
                                    <p className="text-xs text-slate-500 truncate">{user.email}</p>
                                </Link>
                            </div>
                        )}
                    </div>
                )}

                {isExpanded && user && (
                    <div className="mb-4">
                        <div className={clsx(
                            "px-3 py-1.5 rounded-lg border text-xs font-bold text-center uppercase tracking-wide",
                            user.plan === 'premium' ? "bg-indigo-500/10 border-indigo-500/30 text-indigo-400" :
                                user.plan === 'pro' ? "bg-blue-500/10 border-blue-500/30 text-blue-400" :
                                    "bg-slate-700/30 border-slate-600 text-slate-400"
                        )}>
                            Plan {user.plan}
                        </div>
                        {user.credits !== undefined && (
                            <div className="mt-2 text-center">
                                <p className="text-[10px] text-slate-500 uppercase tracking-wider mb-0.5">Créditos Disponibles</p>
                                <div className="text-sm font-bold text-white bg-slate-800/50 rounded-md py-1 border border-white/5">
                                    {user.credits} <span className="text-slate-500 text-[10px]">/ {user.plan === 'premium' ? 2000 : user.plan === 'pro' ? 400 : 5}</span>
                                </div>
                            </div>
                        )}
                    </div>
                )}

                <button
                    onClick={logout}
                    className="w-full flex items-center gap-3 p-3 rounded-xl text-slate-400 hover:bg-rose-500/10 hover:text-rose-400 border border-transparent hover:border-rose-500/20 transition-all group"
                >
                    <LogOut className="w-5 h-5 group-hover:rotate-180 transition-transform duration-300" />
                    {isExpanded && <span className="text-sm font-medium">Cerrar Sesión</span>}
                </button>
            </div>
        </motion.aside>
    );
}
