'use client';

import { motion } from 'framer-motion';
import { History, Trash2, Clock, AlertTriangle, Search, Download } from 'lucide-react';
import { JobHistoryTable } from '@/components/dashboard/JobHistoryTable';

export default function HistoryPage() {
    return (
        <div className="space-y-8">
            {/* Header Section */}
            <div className="relative p-8 rounded-3xl bg-slate-900/50 border border-white/5 overflow-hidden group">
                <div className="absolute inset-0 bg-gradient-to-r from-indigo-500/10 via-purple-500/5 to-transparent blur-3xl" />

                <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
                    <div>
                        <motion.div
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            className="flex items-center gap-3 mb-2"
                        >
                            <div className="p-2 rounded-lg bg-indigo-500/20 text-indigo-400">
                                <History className="w-6 h-6" />
                            </div>
                            <h1 className="text-3xl font-bold text-white font-space">
                                Historial de <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-cyan-400">Trabajos</span>
                            </h1>
                        </motion.div>
                        <p className="text-slate-400 max-w-xl">
                            Accede a tus documentos procesados recientemente. Visualiza, audita y vuelve a descargar tus reportes.
                        </p>
                    </div>

                    {/* Retention Warning Card */}
                    <motion.div
                        initial={{ opacity: 0, scale: 0.9 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ delay: 0.2 }}
                        className="px-5 py-4 rounded-xl bg-orange-500/5 border border-orange-500/10 flex items-start gap-4 max-w-md backdrop-blur-md"
                    >
                        <AlertTriangle className="w-5 h-5 text-orange-400 shrink-0 mt-0.5" />
                        <div>
                            <h4 className="text-sm font-bold text-orange-300 mb-1">Política de Retención de Datos</h4>
                            <p className="text-xs text-orange-200/60 leading-relaxed">
                                Por seguridad y privacidad, los archivos procesados se eliminan automáticamente de nuestros servidores cada <span className="text-orange-200 font-bold">7 días</span>.
                            </p>
                        </div>
                    </motion.div>
                </div>
            </div>

            {/* Main Content Area */}
            <JobHistoryTable />
        </div>
    );
}
