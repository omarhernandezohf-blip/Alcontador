import { Info } from 'lucide-react';
import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface FileGuideProps {
    moduleName: string;
    requiredColumns: string[];
    exampleRow: Record<string, string | number>;
    tips?: string[];
}

export function FileGuide({ moduleName, requiredColumns, exampleRow, tips }: FileGuideProps) {
    const [isOpen, setIsOpen] = useState(false);

    return (
        <>
            <button
                onClick={() => setIsOpen(true)}
                className="flex items-center gap-2 text-sm text-emerald-400 hover:text-emerald-300 transition-colors bg-emerald-950/30 px-3 py-1.5 rounded-lg border border-emerald-500/20"
            >
                <Info className="w-4 h-4" />
                <span>¿Cómo debe ser el archivo?</span>
            </button>

            <AnimatePresence>
                {isOpen && (
                    <>
                        {/* Backdrop */}
                        <motion.div
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                            onClick={() => setIsOpen(false)}
                            className="fixed inset-0 bg-black/60 backdrop-blur-sm z-[9998]"
                        />

                        {/* Modal Content */}
                        <motion.div
                            initial={{ opacity: 0, scale: 0.95, y: 20 }}
                            animate={{ opacity: 1, scale: 1, y: 0 }}
                            exit={{ opacity: 0, scale: 0.95, y: 20 }}
                            className="fixed left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 z-[9999] w-full max-w-lg p-6 rounded-2xl bg-slate-900 border border-emerald-500/30 shadow-2xl shadow-emerald-900/20"
                        >
                            <div className="space-y-6">
                                <div className="flex items-start justify-between">
                                    <div>
                                        <h4 className="text-xl font-bold text-white mb-1">Estructura para {moduleName}</h4>
                                        <p className="text-sm text-slate-400">Tu archivo Excel o CSV debe tener estas columnas:</p>
                                    </div>
                                    <button
                                        onClick={() => setIsOpen(false)}
                                        className="text-slate-500 hover:text-white transition-colors"
                                    >
                                        <span className="sr-only">Cerrar</span>
                                        <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" /></svg>
                                    </button>
                                </div>

                                <div className="bg-slate-950/50 rounded-xl p-4 border border-white/5 overflow-x-auto">
                                    <table className="w-full text-sm text-left">
                                        <thead>
                                            <tr className="border-b border-white/10 text-emerald-400">
                                                {requiredColumns.map(col => (
                                                    <th key={col} className="pb-3 px-3 whitespace-nowrap">{col}</th>
                                                ))}
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <tr className="text-slate-300">
                                                {Object.values(exampleRow).map((val, i) => (
                                                    <td key={i} className="pt-3 px-3 whitespace-nowrap font-mono text-xs">{val}</td>
                                                ))}
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>

                                {tips && (
                                    <div className="bg-emerald-500/5 rounded-lg p-4 border border-emerald-500/10">
                                        <h5 className="text-xs font-bold text-emerald-400 uppercase tracking-wider mb-2">Recomendaciones</h5>
                                        <ul className="text-sm text-slate-300 space-y-2 list-disc pl-4">
                                            {tips.map((tip, i) => (
                                                <li key={i}>{tip}</li>
                                            ))}
                                        </ul>
                                    </div>
                                )}

                                <button
                                    onClick={() => setIsOpen(false)}
                                    className="w-full py-3 text-sm font-medium bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl transition-colors shadow-lg shadow-emerald-900/20"
                                >
                                    ¡Entendido, gracias!
                                </button>
                            </div>
                        </motion.div>
                    </>
                )}
            </AnimatePresence>
        </>
    );
}
