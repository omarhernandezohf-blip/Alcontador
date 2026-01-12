'use client';

import { useState } from 'react';
import { FileText, Download } from 'lucide-react';
import { FileUpload } from '@/components/ui/FileUpload';
import { DataGrid } from '@/components/ui/DataGrid';
import { GlassCard } from '@/components/ui/GlassCard';
import { FileGuide } from '@/components/ui/FileGuide';
import { motion } from 'framer-motion';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function XmlMiningPage() {
    const [data, setData] = useState<any[]>([]);
    const [isProcessing, setIsProcessing] = useState(false);

    const handleProcess = async (files: File[]) => {
        if (files.length === 0) return;

        setIsProcessing(true);
        const formData = new FormData();
        files.forEach(file => formData.append('files', file));

        try {
            const res = await fetch(`${API_URL}/api/xml/process`, {
                method: 'POST',
                body: formData,
            });
            const json = await res.json();
            if (json.data) {
                setData(json.data);
            }
        } catch (e) {
            console.error("Error processing XML:", e);
        } finally {
            setIsProcessing(false);
        }
    };

    return (
        <div className="space-y-8 max-w-7xl mx-auto">
            <div className="flex items-center gap-4">
                <div className="p-4 rounded-2xl bg-gradient-to-br from-indigo-500/20 to-blue-500/20 border border-indigo-500/20">
                    <FileText className="w-10 h-10 text-indigo-400" />
                </div>
                <div>
                    <h1 className="text-3xl font-bold font-space text-white">Minería XML</h1>
                    <p className="text-slate-400">Extrae datos estructurados de tus Facturas Electrónicas (XML) masivamente.</p>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <GlassCard className="lg:col-span-1 h-fit">
                    <div className="flex justify-between items-center mb-4">
                        <h3 className="text-lg font-bold text-indigo-300">Cargar Archivos</h3>
                        <FileGuide
                            moduleName="Minería de Facturas"
                            requiredColumns={['Estructura UBL 2.1']}
                            exampleRow={{ 'Requisito': 'XML Válido DIAN', 'Versión': 'UBL 2.1', 'Tipo': 'Factura/Nota' }}
                            tips={['Puedes subir múltiples archivos XML a la vez', 'El sistema ignora archivos que no sean XML válidos']}
                        />
                    </div>
                    <FileUpload
                        accept=".xml"
                        multiple
                        onFilesSelected={handleProcess}
                        label="Arrastra tus XML aquí"
                    />
                    {isProcessing && (
                        <div className="mt-4 flex items-center gap-2 text-indigo-400 text-sm animate-pulse">
                            <span className="w-2 h-2 rounded-full bg-indigo-400" />
                            Procesando documentos...
                        </div>
                    )}
                </GlassCard>

                <div className="lg:col-span-2">
                    {data.length > 0 ? (
                        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
                            <DataGrid
                                data={data}
                                title={`Resultados (${data.length} documentos)`}
                            />
                            <button className="mt-4 flex items-center gap-2 text-emerald-400 hover:text-emerald-300 transition-colors text-sm font-semibold">
                                <Download className="w-4 h-4" />
                                Exportar a Excel (Próximamente)
                            </button>
                        </motion.div>
                    ) : (
                        <div className="h-64 flex flex-col items-center justify-center text-slate-500 border-2 border-dashed border-white/5 rounded-2xl bg-white/5">
                            <FileText className="w-12 h-12 mb-4 opacity-50" />
                            <p>Los datos extraídos aparecerán aquí</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
