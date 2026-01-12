'use client';

import { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { motion } from 'framer-motion';
import {
    Home, FileText, Banknote, ShieldCheck, Activity,
    PieChart, Users, FileDigit, Smartphone, Cpu, Settings, CheckCircle
} from 'lucide-react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

const menuItems = [
    { icon: Home, label: 'Inicio / Dashboard', href: '/dashboard' },
    { icon: ShieldCheck, label: 'Auditoría DIAN', href: '/dashboard/dian-audit' },
    { icon: FileText, label: 'Minería XML', href: '/dashboard/xml-mining' },
    { icon: Banknote, label: 'Conciliación Bancaria', href: '/dashboard/bank-reconcile' },
    { icon: Activity, label: 'Auditoría Fiscal', href: '/dashboard/fiscal-audit' },
    { icon: Users, label: 'Nómina UGPP', href: '/dashboard/ugpp' },
    { icon: PieChart, label: 'Tesorería', href: '/dashboard/treasury' },
    { icon: Cpu, label: 'Inteligencia Fin.', href: '/dashboard/financial-ai' },
    { icon: FileDigit, label: 'OCR Facturas', href: '/dashboard/ocr' },
    { icon: CheckCircle, label: 'Validador RUT', href: '/dashboard/rut-validator' },
];

export function Sidebar() {
    const pathname = usePathname();
    const [isExpanded, setIsExpanded] = useState(true);

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
                        <p className="text-xs text-slate-400">Enterprise Suite v15.0</p>
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

            <div className="p-4 border-t border-white/5">
                <button className="w-full flex items-center gap-3 p-3 rounded-xl hover:bg-white/5 text-slate-400 hover:text-white transition-colors">
                    <Settings className="w-5 h-5" />
                    {isExpanded && <span className="text-sm">Configuración</span>}
                </button>
            </div>
        </motion.aside>
    );
}
