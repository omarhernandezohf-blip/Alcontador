'use client';

import { useState } from 'react';
import { Users, AlertTriangle, CheckCircle, Calculator } from 'lucide-react';
import { GlassCard } from '@/components/ui/GlassCard';
import { motion, AnimatePresence } from 'framer-motion';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function UgppPage() {
    const [salario, setSalario] = useState(0);
    const [noSalarial, setNoSalarial] = useState(0);
    const [result, setResult] = useState<any>(null);

    const handleCalculate = async () => {
        try {
            const res = await fetch(`${API_URL}/api/ugpp/analyze`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ salario, no_salarial: noSalarial })
            });
            const data = await res.json();
            setResult(data);
        } catch (e) {
            console.error(e);
        }
    };

    return (
        <div className="space-y-8 max-w-4xl mx-auto">
            <div className="flex items-center gap-4">
                <div className="p-4 rounded-2xl bg-gradient-to-br from-indigo-500/20 to-purple-500/20 border border-indigo-500/20">
                    <Users className="w-10 h-10 text-indigo-400" />
                </div>
                <div>
                    <h1 className="text-3xl font-bold font-space text-white">Escáner UGPP</h1>
                    <p className="text-slate-400">Verifica el cumplimiento de la Ley 1393 (Pagos no salariales &lt; 40%).</p>
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <GlassCard>
                    <h3 className="text-lg font-bold mb-6 text-white flex items-center gap-2">
                        <Calculator className="w-5 h-5" />
                        Simulador Rápido
                    </h3>

                    <div className="space-y-4">
                        <div>
                            <label className="block text-sm text-slate-400 mb-2">Salario Base Mensual</label>
                            <input
                                type="number"
                                value={salario || ''}
                                onChange={e => setSalario(Number(e.target.value))}
                                className="input-field w-full"
                                placeholder="Ej. 2500000"
                            />
                        </div>
                        <div>
                            <label className="block text-sm text-slate-400 mb-2">Total Pagos No Salariales</label>
                            <input
                                type="number"
                                value={noSalarial || ''}
                                onChange={e => setNoSalarial(Number(e.target.value))}
                                className="input-field w-full"
                                placeholder="Ej. 1000000"
                            />
                        </div>

                        <button
                            onClick={handleCalculate}
                            className="btn-primary w-full mt-4"
                        >
                            Analizar Riesgo
                        </button>
                    </div>
                </GlassCard>

                {/* Result Panel */}
                <AnimatePresence>
                    {result && (
                        <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }}>
                            <GlassCard className="h-full flex flex-col justify-center bg-white/5 border border-white/10">
                                <div className="text-center mb-6">
                                    {result.riesgo === 'OK' ? (
                                        <div className="w-16 h-16 rounded-full bg-emerald-500/20 flex items-center justify-center mx-auto mb-4">
                                            <CheckCircle className="w-8 h-8 text-emerald-400" />
                                        </div>
                                    ) : (
                                        <div className="w-16 h-16 rounded-full bg-rose-500/20 flex items-center justify-center mx-auto mb-4 animate-pulse">
                                            <AlertTriangle className="w-8 h-8 text-rose-400" />
                                        </div>
                                    )}
                                    <h2 className="text-xl font-bold text-white mb-1">{result.mensaje}</h2>
                                    <p className="text-sm text-slate-400">{result.riesgo === 'OK' ? 'Cumple con la normativa' : 'Requiere corrección inmediata'}</p>
                                </div>

                                <div className="space-y-4 border-t border-white/10 pt-4">
                                    <div className="flex justify-between">
                                        <span className="text-slate-400">Total Remuneración:</span>
                                        <span className="text-white font-mono">${(salario + noSalarial).toLocaleString()}</span>
                                    </div>
                                    <div className="flex justify-between">
                                        <span className="text-slate-400">Exceso Detectado:</span>
                                        <span className={result.exceso > 0 ? "text-rose-400 font-bold" : "text-emerald-400"}>
                                            ${result.exceso.toLocaleString()}
                                        </span>
                                    </div>
                                    <div className="flex justify-between">
                                        <span className="text-slate-400">IBC Ajustado:</span>
                                        <span className="text-indigo-300 font-bold text-lg">${result.nuevo_ibc.toLocaleString()}</span>
                                    </div>
                                </div>
                            </GlassCard>
                        </motion.div>
                    )}
                </AnimatePresence>
            </div>
        </div>
    );
}
