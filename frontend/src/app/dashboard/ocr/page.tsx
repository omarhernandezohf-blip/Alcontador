'use client';

import { useState } from 'react';
import { Camera, Search, FileText } from 'lucide-react';
import { GlassCard } from '@/components/ui/GlassCard';
import { FileUpload } from '@/components/ui/FileUpload';
import { motion } from 'framer-motion';

import { API_URL } from '@/lib/api';

export default function OcrPage() {
    const [result, setResult] = useState<any>(null);
    const [scanning, setScanning] = useState(false);

    const handleScan = async (files: File[]) => {
        if (files.length === 0) return;
        setScanning(true);
        setResult(null);

        const formData = new FormData();
        formData.append('file', files[0]);

        try {
            const res = await fetch(`${API_URL}/api/ocr/scan`, {
                method: 'POST',
                body: formData,
            });
            const data = await res.json();
            if (data.success) {
                setResult(data.data);
            } else {
                alert("Error: " + data.error);
            }
        } catch (e) {
            console.error(e);
        } finally {
            setScanning(false);
        }
    };

    return (
        <div className="space-y-8 max-w-5xl mx-auto">
            <div className="flex items-center gap-4">
                <div className="p-4 rounded-2xl bg-gradient-to-br from-indigo-600/20 to-violet-600/20 border border-indigo-500/20">
                    <Camera className="w-10 h-10 text-indigo-400" />
                </div>
                <div>
                    <h1 className="text-3xl font-bold font-space text-white">OCR Inteligente</h1>
                    <p className="text-slate-400">Transforma fotos de facturas en datos contables JSON usando IA.</p>
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div className="space-y-6">
                    <GlassCard>
                        <div className="aspect-[4/3] rounded-xl border-2 border-dashed border-white/10 flex items-center justify-center relative overflow-hidden bg-black/20">
                            {scanning && (
                                <motion.div
                                    className="absolute inset-0 bg-indigo-500/20 border-b-2 border-indigo-500 z-10"
                                    initial={{ top: '-100%' }}
                                    animate={{ top: '100%' }}
                                    transition={{ repeat: Infinity, duration: 2, ease: "linear" }}
                                />
                            )}
                            <div className="text-center p-6">
                                <FileUpload
                                    accept="image/*"
                                    label="Sube o toma una foto"
                                    onFilesSelected={handleScan}
                                />
                            </div>
                        </div>
                    </GlassCard>
                </div>

                <div>
                    {result ? (
                        <motion.div
                            initial={{ opacity: 0, x: 20 }}
                            animate={{ opacity: 1, x: 0 }}
                            className="space-y-4"
                        >
                            <GlassCard>
                                <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
                                    <FileText className="text-emerald-400" /> Datos Extraídos
                                </h3>
                                <div className="space-y-3">
                                    {Object.entries(result).map(([key, value]) => (
                                        <div key={key} className="flex justify-between border-b border-white/5 pb-2">
                                            <span className="text-slate-400 capitalize">{key}:</span>
                                            <span className="text-white font-medium text-right">{String(value)}</span>
                                        </div>
                                    ))}
                                </div>
                                <div className="mt-6 pt-4 border-t border-white/10">
                                    <button className="w-full btn-primary bg-gradient-to-r from-emerald-600 to-teal-600">
                                        Confirmar y Contabilizar
                                    </button>
                                </div>
                            </GlassCard>
                        </motion.div>
                    ) : (
                        <div className="h-full flex flex-col items-center justify-center opacity-30">
                            <Search className="w-24 h-24 mb-4" />
                            <p className="text-xl">Esperando documento...</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
