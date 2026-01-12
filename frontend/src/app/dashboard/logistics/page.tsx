'use client';

import { useState } from 'react';
import { Truck, MapPin, Package, Clock } from 'lucide-react';
import { GlassCard } from '@/components/ui/GlassCard';
import { motion } from 'framer-motion';

export default function LogisticsPage() {
    const [origin, setOrigin] = useState('');
    const [dest, setDest] = useState('');
    const [weight, setWeight] = useState(0);

    // Simulación de cálculo
    const cost = weight * 450 + 12000;
    const time = Math.floor(Math.random() * 3) + 1;

    return (
        <div className="space-y-8 max-w-5xl mx-auto">
            <div className="flex items-center gap-4">
                <div className="p-4 rounded-2xl bg-gradient-to-br from-amber-500/20 to-orange-600/20 border border-amber-500/20">
                    <Truck className="w-10 h-10 text-amber-400" />
                </div>
                <div>
                    <h1 className="text-3xl font-bold font-space text-white">Generador Logístico</h1>
                    <p className="text-slate-400">Calculadora de fletes y optimización de rutas de transporte.</p>
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <GlassCard>
                    <h3 className="text-lg font-bold text-white mb-6">Cotizar Envío</h3>
                    <div className="space-y-4">
                        <div className="relative">
                            <MapPin className="absolute left-3 top-3 w-5 h-5 text-slate-500" />
                            <input
                                className="input-field w-full pl-10"
                                placeholder="Ciudad de Origen"
                                value={origin}
                                onChange={e => setOrigin(e.target.value)}
                            />
                        </div>
                        <div className="relative">
                            <MapPin className="absolute left-3 top-3 w-5 h-5 text-indigo-400" />
                            <input
                                className="input-field w-full pl-10"
                                placeholder="Ciudad de Destino"
                                value={dest}
                                onChange={e => setDest(e.target.value)}
                            />
                        </div>
                        <div className="relative">
                            <Package className="absolute left-3 top-3 w-5 h-5 text-slate-500" />
                            <input
                                type="number"
                                className="input-field w-full pl-10"
                                placeholder="Peso (Kg)"
                                value={weight || ''}
                                onChange={e => setWeight(Number(e.target.value))}
                            />
                        </div>

                        <button className="w-full btn-primary mt-4">
                            Calcular Flete
                        </button>
                    </div>
                </GlassCard>

                <div className="space-y-6">
                    <GlassCard className="bg-gradient-to-br from-indigo-900/40 via-purple-900/40 to-slate-900/40">
                        <h3 className="text-slate-400 text-sm mb-2">Costo Estimado</h3>
                        <div className="flex items-end gap-2">
                            <span className="text-4xl font-bold text-white">${cost.toLocaleString()}</span>
                            <span className="text-emerald-400 text-sm mb-1 px-2 py-0.5 rounded-full bg-emerald-500/10">Tarifa Económica</span>
                        </div>
                    </GlassCard>

                    <GlassCard className="bg-gradient-to-br from-amber-900/20 via-orange-900/20 to-slate-900/40">
                        <div className="flex items-center gap-4">
                            <div className="p-3 rounded-full bg-amber-500/20 text-amber-400">
                                <Clock className="w-6 h-6" />
                            </div>
                            <div>
                                <h3 className="text-slate-400 text-sm">Tiempo de Tránsito</h3>
                                <p className="text-2xl font-bold text-white text-amber-200">{time} - {time + 1} Días Hábiles</p>
                            </div>
                        </div>
                    </GlassCard>

                    {/* Simulated Map Visual */}
                    <div className="h-32 rounded-xl bg-slate-800/50 border border-white/10 relative overflow-hidden flex items-center justify-center">
                        <div className="absolute inset-0 opacity-20 bg-[url('https://upload.wikimedia.org/wikipedia/commons/e/ec/World_map_blank_without_borders.svg')] bg-cover bg-center" />
                        <p className="z-10 text-xs text-slate-500 font-mono">MAPA DE RUTA SIMULADO</p>

                        {/* Animated dots */}
                        <div className="absolute top-1/2 left-1/4 w-2 h-2 bg-indigo-500 rounded-full" />
                        <div className="absolute top-1/2 right-1/4 w-2 h-2 bg-rose-500 rounded-full" />
                        <motion.div
                            className="absolute top-1/2 left-1/4 h-0.5 bg-gradient-to-r from-indigo-500 to-rose-500"
                            initial={{ width: 0 }}
                            animate={{ width: '50%' }}
                            transition={{ duration: 1, repeat: Infinity, repeatDelay: 1 }}
                        />
                    </div>
                </div>
            </div>
        </div>
    );
}
