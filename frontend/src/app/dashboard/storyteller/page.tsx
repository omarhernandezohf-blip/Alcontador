'use client';

import { useState } from 'react';
import { BookOpen, Mic, PlayCircle, Upload, FileText, Sparkles, Brain, AlignLeft } from 'lucide-react';
import { GlassCard } from '@/components/ui/GlassCard';
import { FileUpload } from '@/components/ui/FileUpload';
import { motion, AnimatePresence } from 'framer-motion';

export default function StorytellerPage() {
    const [file, setFile] = useState<File | null>(null);
    const [isGenerating, setIsGenerating] = useState(false);
    const [generatedReport, setGeneratedReport] = useState<boolean>(false);

    const handleGenerate = () => {
        if (!file) return;
        setIsGenerating(true);
        // Simulate AI Generation
        setTimeout(() => {
            setIsGenerating(false);
            setGeneratedReport(true);
        }, 3500);
    };

    return (
        <div className="space-y-8 max-w-6xl mx-auto">
            <div className="flex items-center gap-4">
                <div className="p-4 rounded-2xl bg-gradient-to-br from-violet-500/20 to-fuchsia-600/20 border border-violet-500/20">
                    <BookOpen className="w-10 h-10 text-violet-400" />
                </div>
                <div>
                    <h1 className="text-3xl font-bold font-space text-white">Narrador Financiero & NIIF</h1>
                    <p className="text-slate-400">Transforma estados financieros planos en historias ejecutivas y notas NIIF.</p>
                </div>
            </div>

            <AnimatePresence mode="wait">
                {!generatedReport ? (
                    <motion.div
                        key="input"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                    >
                        <GlassCard className="min-h-[400px] flex flex-col justify-center items-center text-center space-y-8 border-dashed border-2 border-white/10 bg-transparent relative overflow-hidden">
                            {/* Background decorations */}
                            <div className="absolute top-0 left-0 w-full h-full opacity-5 pointer-events-none">
                                <Brain className="absolute top-10 left-10 w-32 h-32 text-violet-400 rotate-12" />
                            </div>

                            <div className="relative z-10 max-w-lg w-full space-y-6">
                                <div className="p-6 rounded-full bg-violet-900/20 mx-auto w-24 h-24 flex items-center justify-center border border-violet-500/30">
                                    <Upload className={`w-10 h-10 text-violet-400 ${isGenerating ? 'animate-bounce' : ''}`} />
                                </div>

                                <div className="space-y-2">
                                    <h3 className="text-xl font-bold text-white">Cargar Estados Financieros</h3>
                                    <p className="text-slate-400 text-sm">Sube tu Balance General y Estado de Resultados en un solo archivo PDF o Excel.</p>
                                </div>

                                <div className="bg-slate-900/50 p-4 rounded-xl border border-white/5 text-left">
                                    <FileUpload
                                        accept=".pdf,.xlsx"
                                        label="Seleccionar Archivo Financiero"
                                        onFilesSelected={(f) => setFile(f[0])}
                                    />
                                    {file && <div className="mt-3 flex items-center gap-2 text-violet-400 text-sm bg-violet-500/10 p-2 rounded">
                                        <FileText className="w-4 h-4" />
                                        <span className="truncate flex-1">{file.name}</span>
                                    </div>}
                                </div>

                                <button
                                    onClick={handleGenerate}
                                    disabled={!file || isGenerating}
                                    className="btn-primary w-full py-4 flex items-center justify-center gap-3 bg-gradient-to-r from-violet-600 to-fuchsia-600 hover:from-violet-500 hover:to-fuchsia-500 disabled:opacity-50 disabled:cursor-not-allowed"
                                >
                                    {isGenerating ? (
                                        <>
                                            <Sparkles className="w-5 h-5 animate-spin" />
                                            Analizando Tendencias...
                                        </>
                                    ) : (
                                        <>
                                            <Brain className="w-5 h-5" />
                                            Generar Informe Inteligente
                                        </>
                                    )}
                                </button>
                            </div>
                        </GlassCard>
                    </motion.div>
                ) : (
                    <motion.div
                        key="report"
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="grid grid-cols-1 lg:grid-cols-3 gap-8"
                    >
                        {/* Sidebar: Key Metrics */}
                        <div className="space-y-6 lg:col-span-1">
                            <GlassCard className="bg-gradient-to-br from-violet-900/50 to-indigo-900/50 border-violet-500/30">
                                <h3 className="font-bold text-white mb-4 flex items-center gap-2">
                                    <Sparkles className="w-4 h-4 text-amber-400" />
                                    Insights Clave
                                </h3>
                                <div className="space-y-4">
                                    <div className="p-3 rounded-lg bg-white/5 border border-white/10">
                                        <p className="text-xs text-slate-400 uppercase">Liquidez Corriente</p>
                                        <p className="text-xl font-bold text-emerald-400">1.8x</p>
                                        <p className="text-xs text-slate-500 mt-1">Salusable (&gt;1.5)</p>
                                    </div>
                                    <div className="p-3 rounded-lg bg-white/5 border border-white/10">
                                        <p className="text-xs text-slate-400 uppercase">Margen EBITDA</p>
                                        <p className="text-xl font-bold text-indigo-400">24.5%</p>
                                        <p className="text-xs text-slate-500 mt-1">Mejora vs mes anterior</p>
                                    </div>
                                    <div className="p-3 rounded-lg bg-white/5 border border-white/10">
                                        <p className="text-xs text-slate-400 uppercase">Endeudamiento</p>
                                        <p className="text-xl font-bold text-amber-400">45%</p>
                                        <p className="text-xs text-slate-500 mt-1">Monitorear apalancamiento</p>
                                    </div>
                                </div>
                            </GlassCard>

                            <GlassCard className="bg-black/20 text-center space-y-4">
                                <div className="mx-auto w-12 h-12 rounded-full bg-white/10 flex items-center justify-center">
                                    <Mic className="w-6 h-6 text-white" />
                                </div>
                                <div>
                                    <h4 className="text-white font-bold">Podcast Generado</h4>
                                    <p className="text-xs text-slate-400">Resumen de audio de 2 min</p>
                                </div>
                                <button className="w-full py-2 rounded-lg bg-white/10 hover:bg-white/20 text-white text-sm flex items-center justify-center gap-2 transition-colors">
                                    <PlayCircle className="w-4 h-4" /> REPRODUCIR
                                </button>
                            </GlassCard>

                            <button onClick={() => setGeneratedReport(false)} className="w-full py-3 text-sm text-slate-400 hover:text-white underline decoration-slate-600 hover:decoration-white underline-offset-4">
                                Analizar otro archivo
                            </button>
                        </div>

                        {/* Main Content: Narrative */}
                        <div className="lg:col-span-2 space-y-6">
                            <GlassCard className="relative overflow-hidden">
                                <div className="absolute top-0 right-0 p-4 opacity-5">
                                    <AlignLeft className="w-32 h-32 text-white" />
                                </div>
                                <h2 className="text-2xl font-bold text-white mb-6">Resumen Ejecutivo de Gestión</h2>

                                <div className="space-y-4 text-slate-300 leading-relaxed text-sm text-justify">
                                    <p>
                                        Durante el periodo analizado de 2026, la compañía ha demostrado una <strong className="text-emerald-400">solidez financiera notable</strong>, impulsada principalmente por un incremento del 15% en los ingresos operativos respecto al periodo anterior. Esta eficiencia se traduce en una mejora del Margen EBITDA, que ahora se sitúa en un competitivo 24.5%.
                                    </p>
                                    <p>
                                        En cuanto a la gestión de activos, la rotación de cartera ha mejorado en 5 días, liberando flujo de caja operativo. Sin embargo, se observa un incremento en los gastos administrativos que requiere atención para no erosionar la utilidad neta.
                                    </p>
                                    <div className="p-4 bg-indigo-900/20 border-l-4 border-indigo-500 rounded-r-lg my-6">
                                        <h4 className="font-bold text-indigo-300 mb-1">Nota NIIF Sugerida: Reconocimiento de Ingresos</h4>
                                        <p className="text-xs text-slate-400 italic">
                                            "La entidad reconoce los ingresos provenientes de contratos con clientes cuando se satisface la obligación de desempeño mediante la transferencia de los bienes o servicios prometidos..."
                                        </p>
                                    </div>
                                    <p>
                                        <strong className="text-white">Recomendación del Asistente:</strong> Se sugiere revisar los contratos de proveedores clave para optimizar la estructura de costos fijos y evaluar opciones de inversión para el excedente de liquidez actual.
                                    </p>
                                </div>
                            </GlassCard>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
}
