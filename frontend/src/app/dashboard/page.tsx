'use client';

import { motion } from 'framer-motion';
import { Activity, TrendingUp, Users, AlertTriangle, ArrowUpRight, ArrowDownRight, DollarSign, FileText, Zap, Shield, Crown } from 'lucide-react';
import Link from 'next/link';
import { HeroSection } from '@/components/dashboard/HeroSection';
import { LuxuryCard } from '@/components/ui/LuxuryCard';
import { PricingSection } from '@/components/modules/PricingSection';

const container = {
    hidden: { opacity: 0 },
    show: {
        opacity: 1,
        transition: {
            staggerChildren: 0.1
        }
    }
};

const item = {
    hidden: { y: 20, opacity: 0 },
    show: { y: 0, opacity: 1 }
};

export default function DashboardPage() {
    return (
        <div className="min-h-screen pb-20">
            {/* Cinematic Hero */}
            <HeroSection />

            {/* Asymmetrical Grid */}
            <motion.div
                variants={container}
                initial="hidden"
                animate="show"
                className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 px-2"
            >
                {/* Featured Metric - Treasury */}
                <LuxuryCard featured className="relative group overflow-hidden">
                    <div className="absolute top-0 right-0 p-4 opacity-50 group-hover:opacity-100 transition-opacity">
                        <Crown className="w-24 h-24 text-amber-500/10 -rotate-12" />
                    </div>

                    <div className="flex flex-col justify-between h-full">
                        <div>
                            <div className="flex items-center justify-between mb-4">
                                <div className="p-3 rounded-xl bg-gradient-to-br from-amber-500/20 to-yellow-600/20 border border-amber-500/30">
                                    <DollarSign className="w-6 h-6 text-amber-400" />
                                </div>
                                <span className="px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-400 text-xs font-bold border border-emerald-500/20 backdrop-blur-sm">
                                    +122.5% vs Año Pasado
                                </span>
                            </div>
                            <h3 className="text-slate-400 font-medium">Patrimonio Líquido Proyectado</h3>
                            <h2 className="text-5xl font-bold text-white mt-2 tracking-tight">$452.8M</h2>
                        </div>

                        <div className="mt-8">
                            <div className="w-full bg-white/5 rounded-full h-2 mb-2 overflow-hidden">
                                <motion.div
                                    initial={{ width: 0 }}
                                    animate={{ width: "85%" }}
                                    transition={{ duration: 1.5, delay: 0.5 }}
                                    className="bg-gradient-to-r from-amber-400 to-yellow-600 h-full rounded-full"
                                />
                            </div>
                            <p className="text-xs text-slate-500 text-right">Objetivo Q1: 85% Completado</p>
                        </div>
                    </div>
                </LuxuryCard>

                {/* Satellite Metrics */}
                <LuxuryCard className="border-t-4 border-purple-500">
                    <div className="flex justify-between items-start mb-4">
                        <div className="p-3 rounded-lg bg-purple-500/10 text-purple-400">
                            <Activity className="w-6 h-6" />
                        </div>
                        <Zap className="w-4 h-4 text-purple-500/50" />
                    </div>
                    <p className="text-slate-400 text-sm">Gastos Auditados IA</p>
                    <h3 className="text-3xl font-bold text-white mt-1">1,240</h3>
                    <p className="text-xs text-slate-500 mt-2">100% Verificado DIAN</p>
                </LuxuryCard>

                <LuxuryCard className="border-t-4 border-rose-500">
                    <div className="flex justify-between items-start mb-4">
                        <div className="p-3 rounded-lg bg-rose-500/10 text-rose-400">
                            <AlertTriangle className="w-6 h-6" />
                        </div>
                        <div />
                    </div>
                    <p className="text-slate-400 text-sm">Riesgo Fiscal</p>
                    <h3 className="text-3xl font-bold text-white mt-1">Bajo</h3>
                    <p className="text-xs text-emerald-400 mt-2 flex items-center gap-1">
                        <Shield className="w-3 h-3" /> Blindaje Activo
                    </p>
                </LuxuryCard>

                <LuxuryCard className="border-t-4 border-blue-500">
                    <div className="flex justify-between items-start mb-6">
                        <div className="p-3 rounded-lg bg-blue-500/10 text-blue-400">
                            <Users className="w-6 h-6" />
                        </div>
                    </div>
                    <p className="text-slate-400 text-sm">Nómina Inteligente</p>
                    <h3 className="text-3xl font-bold text-white mt-1">14 Activos</h3>
                    <div className="mt-4 flex -space-x-2">
                        {[1, 2, 3, 4].map(i => (
                            <div key={i} className="w-8 h-8 rounded-full bg-slate-800 border-2 border-slate-900 flex items-center justify-center text-xs text-slate-500">
                                {String.fromCharCode(64 + i)}
                            </div>
                        ))}
                    </div>
                </LuxuryCard>

                {/* Action Modules */}
                <LuxuryCard className="md:col-span-2 min-h-[200px] group cursor-pointer hover:border-indigo-500/50">
                    <Link href="/dashboard/xml-mining" className="block h-full">
                        <div className="flex flex-col h-full justify-between">
                            <div className="flex items-center gap-4">
                                <div className="p-4 rounded-full bg-indigo-500/20 text-indigo-400 group-hover:scale-110 transition-transform duration-300">
                                    <FileText className="w-8 h-8" />
                                </div>
                                <div>
                                    <h3 className="text-xl font-bold text-white group-hover:text-indigo-300 transition-colors">Minería de Datos XML</h3>
                                    <p className="text-slate-400 text-sm">Procesamiento masivo de facturación electrónica.</p>
                                </div>
                            </div>
                            <div className="w-full h-32 bg-indigo-900/10 rounded-xl mt-4 relative overflow-hidden flex items-center justify-center">
                                <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-20" />
                                <span className="text-indigo-500/50 font-mono text-sm">Iniciando Motor de Extracción...</span>
                            </div>
                        </div>
                    </Link>
                </LuxuryCard>

                <LuxuryCard className="md:col-span-2 min-h-[200px] group cursor-pointer hover:border-emerald-500/50">
                    <Link href="/dashboard/treasury" className="block h-full">
                        <div className="flex flex-col h-full justify-between">
                            <div className="flex items-center gap-4">
                                <div className="p-4 rounded-full bg-emerald-500/20 text-emerald-400 group-hover:scale-110 transition-transform duration-300">
                                    <TrendingUp className="w-8 h-8" />
                                </div>
                                <div>
                                    <h3 className="text-xl font-bold text-white group-hover:text-emerald-300 transition-colors">Tesorería Proyectiva</h3>
                                    <p className="text-slate-400 text-sm">Forward-looking cash flow analysis.</p>
                                </div>
                            </div>
                            <div className="w-full h-32 bg-emerald-900/10 rounded-xl mt-4 relative overflow-hidden flex items-end px-4 pb-2 gap-1">
                                {[40, 60, 45, 70, 50, 80, 65, 90].map((h, i) => (
                                    <motion.div
                                        key={i}
                                        initial={{ height: 0 }}
                                        animate={{ height: `${h}%` }}
                                        transition={{ duration: 1, delay: i * 0.1 }}
                                        className="flex-1 bg-emerald-500/30 rounded-t-sm hover:bg-emerald-400 transition-colors"
                                    />
                                ))}
                            </div>
                        </div>
                    </Link>
                </LuxuryCard>

            </motion.div>

            {/* Subscription Plans */}
            <PricingSection />
        </div>
    );
}
