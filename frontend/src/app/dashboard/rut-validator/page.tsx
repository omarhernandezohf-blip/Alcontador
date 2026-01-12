'use client';

import { useState } from 'react';
import { CheckCircle, Hash, Copy } from 'lucide-react';
import { GlassCard } from '@/components/ui/GlassCard';
import { motion, AnimatePresence } from 'framer-motion';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function RutValidatorPage() {
    const [nit, setNit] = useState('');
    const [dv, setDv] = useState<string | null>(null);

    const handleCalculate = async (value: string) => {
        setNit(value);
        if (value.length > 4) {
            try {
                const res = await fetch(`${API_URL}/api/rut/calculate/${value}`);
                const data = await res.json();
                setDv(data.dv);
            } catch (e) {
                console.error(e);
            }
        } else {
            setDv(null);
        }
    };

    return (
        <div className="space-y-8 max-w-2xl mx-auto mt-10">
            <div className="flex items-center gap-4">
                <div className="p-4 rounded-2xl bg-gradient-to-br from-yellow-500/20 to-orange-500/20 border border-yellow-500/20">
                    <Hash className="w-10 h-10 text-yellow-400" />
                </div>
                <div>
                    <h1 className="text-3xl font-bold font-space text-white">Validador RUT Oficial</h1>
                    <p className="text-slate-400">Calcula el Dígito de Verificación (DV) oficial de la DIAN.</p>
                </div>
            </div>

            <GlassCard className="p-10 text-center">
                <label className="block text-slate-400 mb-4 text-lg">Ingresa el NIT (Sin guiones ni espacios)</label>
                <div className="relative max-w-md mx-auto">
                    <input
                        type="number"
                        value={nit}
                        onChange={(e) => handleCalculate(e.target.value)}
                        className="w-full bg-white/5 border-2 border-white/10 rounded-2xl px-6 py-4 text-3xl font-mono text-center text-white focus:outline-none focus:border-yellow-500 transition-all placeholder:text-white/10"
                        placeholder="900123456"
                    />
                </div>

                <AnimatePresence>
                    {dv && (
                        <motion.div
                            initial={{ scale: 0.5, opacity: 0 }}
                            animate={{ scale: 1, opacity: 1 }}
                            exit={{ scale: 0.5, opacity: 0 }}
                            className="mt-12"
                        >
                            <p className="text-slate-500 uppercase tracking-widest text-sm mb-2">Dígito de Verificación</p>
                            <div className="flex items-center justify-center gap-4">
                                <div className="text-6xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-yellow-400 to-orange-500 font-mono">
                                    {dv}
                                </div>
                                <CheckCircle className="w-8 h-8 text-emerald-500" />
                            </div>

                            <div className="mt-8 p-4 bg-white/5 rounded-xl flex items-center justify-center gap-2 cursor-pointer hover:bg-white/10 transition-colors" onClick={() => navigator.clipboard.writeText(`${nit}-${dv}`)}>
                                <code className="text-xl text-slate-300">{nit}-{dv}</code>
                                <Copy className="w-4 h-4 text-slate-500" />
                            </div>
                        </motion.div>
                    )}
                </AnimatePresence>
            </GlassCard>
        </div>
    );
}
