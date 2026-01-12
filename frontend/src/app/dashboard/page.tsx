'use client';

import { motion } from 'framer-motion';
import { GlassCard } from '@/components/ui/GlassCard';
import { Activity, TrendingUp, Users, AlertTriangle, ArrowUpRight, DollarSign, FileText } from 'lucide-react';
import Link from 'next/link';

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
        <div className="space-y-8">
            {/* Header Section */}
            <div className="flex justify-between items-end">
                <div>
                    <h1 className="text-4xl font-bold font-space bg-clip-text text-transparent bg-gradient-to-r from-white via-indigo-200 to-indigo-400">
                        Resumen Ejecutivo
                    </h1>
                    <p className="text-slate-400 mt-2 text-lg">
                        Bienvenido, Operador. Estado del sistema: <span className="text-emerald-400">● En Línea</span>
                    </p>
                </div>
                <div className="text-right hidden md:block">
                    <p className="text-sm text-slate-500">Última sincronización</p>
                    <p className="font-mono text-indigo-300">2026-01-12 10:45 AM</p>
                </div>
            </div>

            {/* Metrics Grid */}
            <motion.div
                variants={container}
                initial="hidden"
                animate="show"
                className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
            >
                <Link href="/dashboard/treasury">
                    <GlassCard gradient className="cursor-pointer hover:border-emerald-500/50 transition-colors">
                        <div className="flex justify-between items-start mb-4">
                            <div className="p-3 rounded-lg bg-indigo-500/20 text-indigo-400">
                                <DollarSign className="w-6 h-6" />
                            </div>
                            <span className="flex items-center text-emerald-400 text-sm font-medium bg-emerald-500/10 px-2 py-1 rounded-full">
                                +12.5% <ArrowUpRight className="w-3 h-3 ml-1" />
                            </span>
                        </div>
                        <p className="text-slate-400 text-sm">Flujo de Caja (Mes)</p>
                        <h3 className="text-3xl font-bold text-white mt-1">$45.2M</h3>
                    </GlassCard>
                </Link>

                <Link href="/dashboard/fiscal-audit">
                    <GlassCard gradient className="cursor-pointer hover:border-rose-500/50 transition-colors">
                        <div className="flex justify-between items-start mb-4">
                            <div className="p-3 rounded-lg bg-purple-500/20 text-purple-400">
                                <Activity className="w-6 h-6" />
                            </div>
                        </div>
                        <p className="text-slate-400 text-sm">Gastos Auditados</p>
                        <h3 className="text-3xl font-bold text-white mt-1">1,240</h3>
                    </GlassCard>
                </Link>


                <GlassCard gradient>
                    <div className="flex justify-between items-start mb-4">
                        <div className="p-3 rounded-lg bg-rose-500/20 text-rose-400">
                            <AlertTriangle className="w-6 h-6" />
                        </div>
                        <span className="flex items-center text-rose-400 text-sm font-medium bg-rose-500/10 px-2 py-1 rounded-full">
                            3 Pendientes
                        </span>
                    </div>
                    <p className="text-slate-400 text-sm">Alertas Fiscales</p>
                    <h3 className="text-3xl font-bold text-white mt-1">Riesgo Bajo</h3>
                </GlassCard>

                <Link href="/dashboard/ugpp">
                    <GlassCard gradient className="cursor-pointer hover:border-blue-500/50 transition-colors">
                        <div className="flex justify-between items-start mb-4">
                            <div className="p-3 rounded-lg bg-blue-500/20 text-blue-400">
                                <Users className="w-6 h-6" />
                            </div>
                        </div>
                        <p className="text-slate-400 text-sm">Nómina Activa</p>
                        <h3 className="text-3xl font-bold text-white mt-1">14 Empleados</h3>
                    </GlassCard>
                </Link>
            </motion.div>

            {/* Main Content Area (Placeholder for Charts) */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <GlassCard className="lg:col-span-2 min-h-[400px] flex items-center justify-center relative overflow-hidden">
                    <div className="absolute inset-0 bg-gradient-to-tr from-indigo-500/10 to-purple-500/10" />
                    <div className="text-center z-10">
                        <TrendingUp className="w-16 h-16 text-white/20 mx-auto mb-4" />
                        <h3 className="text-xl font-bold text-white">Analíticas en Tiempo Real</h3>
                        <p className="text-slate-400 mt-2">Los gráficos de tesorería se han movido a su <Link href="/dashboard/treasury" className="text-indigo-400 hover:underline">Módulo Dedicado</Link>.</p>
                    </div>
                </GlassCard>

                <GlassCard className="min-h-[400px]">
                    <h3 className="text-xl font-bold mb-6">Actividad Reciente</h3>
                    <div className="space-y-4">
                        {[1, 2, 3, 4].map((i) => (
                            <div key={i} className="flex items-center gap-4 p-3 rounded-lg hover:bg-white/5 transition-colors cursor-pointer group">
                                <div className="w-2 h-2 rounded-full bg-indigo-500 group-hover:bg-indigo-400 transition-colors" />
                                <div>
                                    <p className="text-sm font-medium text-slate-200">Proceso XML #{1000 + i}</p>
                                    <p className="text-xs text-slate-500">Hace {i * 15} minutos • Completado</p>
                                </div>
                                <FileText className="w-4 h-4 text-slate-600 ml-auto group-hover:text-white" />
                            </div>
                        ))}
                    </div>
                </GlassCard>
            </div>
        </div>
    );
}
