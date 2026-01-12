'use client';

import { useState } from 'react';
import { ShieldAlert, Info } from 'lucide-react';
import { GlassCard } from '@/components/ui/GlassCard';
import { FileUpload } from '@/components/ui/FileUpload';
import { DataGrid } from '@/components/ui/DataGrid';
import { motion } from 'framer-motion';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function FiscalAuditPage() {
    const [data, setData] = useState<any[]>([]);
    const [loading, setLoading] = useState(false);

    const handleProcess = async (files: File[]) => {
        if (files.length === 0) return;
        setLoading(true);

        const formData = new FormData();
        formData.append('file', files[0]);

        try {
            const res = await fetch(`${API_URL}/api/fiscal/audit`, {
                method: 'POST',
                body: formData,
            });
            const json = await res.json();
            if (json.data) {
                // Transformar data para añadir componentes visuales si fuera necesario,
                // pero DataGrid renderiza texto. El coloreado lo hacemos a nivel de fila/celda custom
                // o modificamos DataGrid. Por ahora texto raw.
                setData(json.data);
            }
        } catch (e) {
            console.error(e);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="space-y-8 max-w-7xl mx-auto">
            <div className="flex items-center gap-4">
                <div className="p-4 rounded-2xl bg-gradient-to-br from-rose-500/20 to-orange-500/20 border border-rose-500/20">
                    <ShieldAlert className="w-10 h-10 text-rose-400" />
                </div>
                <div>
                    <h1 className="text-3xl font-bold font-space text-white">Auditoría Fiscal (Art. 771-5)</h1>
                    <p className="text-slate-400">Detecta pagos en efectivo ilegales y errores en bases de retención.</p>
                </div>
            </div>

            <GlassCard>
                <div className="flex items-start gap-4 mb-6 p-4 bg-indigo-500/10 rounded-xl border border-indigo-500/20">
                    <Info className="w-6 h-6 text-indigo-400 shrink-0 mt-1" />
                    <p className="text-sm text-indigo-200">
                        Sube tu Libro Auxiliar de Gastos en Excel o CSV. El sistema buscará automáticamente columnas de <strong>"Valor"</strong> y <strong>"Método de Pago"</strong> para aplicar las reglas del Estatuto Tributario 2026.
                    </p>
                </div>

                <FileUpload
                    accept=".xlsx,.csv"
                    label="Sube tu reporte de gastos (.xlsx, .csv)"
                    onFilesSelected={handleProcess}
                />
            </GlassCard>

            {loading && (
                <div className="text-center py-10">
                    <div className="w-10 h-10 border-4 border-rose-500 border-t-transparent rounded-full animate-spin mx-auto mb-4" />
                    <p className="text-rose-300 animate-pulse">Auditando transacciones...</p>
                </div>
            )}

            {data.length > 0 && (
                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                    <div className="mb-4 flex gap-4">
                        <div className="px-4 py-2 rounded-lg bg-rose-500/20 text-rose-400 border border-rose-500/20 font-bold">
                            Riesgo Alto: {data.filter(r => r.Nivel_Riesgo === 'ALTO').length}
                        </div>
                        <div className="px-4 py-2 rounded-lg bg-yellow-500/20 text-yellow-400 border border-yellow-500/20 font-bold">
                            Alertas: {data.filter(r => r.Nivel_Riesgo === 'MEDIO').length}
                        </div>
                    </div>
                    <DataGrid data={data} title="Informe de Hallazgos" />
                </motion.div>
            )}
        </div>
    );
}
