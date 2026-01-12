'use client';

import { useState, useEffect } from 'react';
import { TrendingUp, Wallet, ArrowUpRight, ArrowDownRight } from 'lucide-react';
import { TreasuryChart } from '@/components/modules/TreasuryChart';
import { GlassCard } from '@/components/ui/GlassCard';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function TreasuryPage() {
    const [data, setData] = useState<any[]>([]);

    useEffect(() => {
        fetch(`${API_URL}/api/treasury/projection`)
            .then(res => res.json())
            .then(json => {
                if (json.projection) setData(json.projection);
            });
    }, []);

    const totalIngresos = data.reduce((acc, curr) => acc + curr.ingresos, 0);
    const totalEgresos = data.reduce((acc, curr) => acc + curr.egresos, 0);

    return (
        <div className="space-y-8 max-w-7xl mx-auto">
            <div className="flex items-center gap-4">
                <div className="p-4 rounded-2xl bg-gradient-to-br from-cyan-500/20 to-blue-600/20 border border-cyan-500/20">
                    <Wallet className="w-10 h-10 text-cyan-400" />
                </div>
                <div>
                    <h1 className="text-3xl font-bold font-space text-white">Proyección de Tesorería</h1>
                    <p className="text-slate-400">Radar de liquidez y predicción de flujo de caja futuro.</p>
                </div>
            </div>

            {/* KPIs */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <GlassCard gradient className="border-l-4 border-emerald-500">
                    <p className="text-slate-400 text-sm">Ingresos Anuales (Proj)</p>
                    <h2 className="text-3xl font-bold text-white mt-1">${(totalIngresos / 1000000).toFixed(1)}M</h2>
                    <div className="flex items-center text-emerald-400 text-sm mt-2">
                        <ArrowUpRight className="w-4 h-4 mr-1" /> +12% vs año anterior
                    </div>
                </GlassCard>

                <GlassCard gradient className="border-l-4 border-rose-500">
                    <p className="text-slate-400 text-sm">Egresos Anuales (Proj)</p>
                    <h2 className="text-3xl font-bold text-white mt-1">${(totalEgresos / 1000000).toFixed(1)}M</h2>
                    <div className="flex items-center text-rose-400 text-sm mt-2">
                        <ArrowDownRight className="w-4 h-4 mr-1" /> -5% optimización
                    </div>
                </GlassCard>

                <GlassCard gradient className="border-l-4 border-indigo-500">
                    <p className="text-slate-400 text-sm">Margen Operativo</p>
                    <h2 className="text-3xl font-bold text-white mt-1">
                        {((1 - (totalEgresos / totalIngresos)) * 100).toFixed(1)}%
                    </h2>
                    <div className="flex items-center text-indigo-400 text-sm mt-2">
                        <TrendingUp className="w-4 h-4 mr-1" /> Saludable
                    </div>
                </GlassCard>
            </div>

            {data.length > 0 ? (
                <TreasuryChart data={data} />
            ) : (
                <div className="h-[400px] flex items-center justify-center">
                    <span className="animate-pulse text-slate-500">Cargando proyección financiera...</span>
                </div>
            )}
        </div>
    );
}
