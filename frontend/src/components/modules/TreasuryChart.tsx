'use client';

import {
    AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
    BarChart, Bar, Legend, ComposedChart, Line
} from 'recharts';
import { GlassCard } from '@/components/ui/GlassCard';

interface TreeMapProps {
    data: any[];
}

export function TreasuryChart({ data }: TreeMapProps) {
    return (
        <GlassCard className="h-[500px] w-full">
            <h3 className="text-xl font-bold text-white mb-6">Proyección de Flujo de Caja 2026</h3>

            <ResponsiveContainer width="100%" height="90%">
                <ComposedChart data={data} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                    <defs>
                        <linearGradient id="colorIngreso" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="#10b981" stopOpacity={0.8} />
                            <stop offset="95%" stopColor="#10b981" stopOpacity={0} />
                        </linearGradient>
                        <linearGradient id="colorEgreso" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="#f43f5e" stopOpacity={0.8} />
                            <stop offset="95%" stopColor="#f43f5e" stopOpacity={0} />
                        </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" vertical={false} />
                    <XAxis dataKey="month" stroke="#94a3b8" tick={{ fill: '#94a3b8' }} axisLine={false} />
                    <YAxis stroke="#94a3b8" tick={{ fill: '#94a3b8' }} axisLine={false} tickFormatter={(value) => `$${value / 1000000}M`} />
                    <Tooltip
                        contentStyle={{ backgroundColor: '#1e293b', borderColor: 'rgba(255,255,255,0.1)', borderRadius: '12px', color: '#fff' }}
                        itemStyle={{ color: '#fff' }}
                        formatter={(value: any) => [`$${Number(value).toLocaleString()}`, '']}
                    />
                    <Legend />

                    <Area type="monotone" dataKey="ingresos" name="Ingresos Proyectados" stroke="#10b981" fillOpacity={1} fill="url(#colorIngreso)" />
                    <Area type="monotone" dataKey="egresos" name="Egresos Estimados" stroke="#f43f5e" fillOpacity={1} fill="url(#colorEgreso)" />
                    <Line type="monotone" dataKey="flujo" name="Flujo Neto" stroke="#6366f1" strokeWidth={3} dot={{ r: 4, fill: '#6366f1', strokeWidth: 2, stroke: '#fff' }} />
                </ComposedChart>
            </ResponsiveContainer>
        </GlassCard>
    );
}
