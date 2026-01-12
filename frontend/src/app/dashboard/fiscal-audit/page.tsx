'use client';

import { useState } from 'react';
import { ShieldAlert, Info, Upload, Brain, AlertOctagon, FileText, ArrowRight, FileSpreadsheet } from 'lucide-react';
import * as XLSX from 'xlsx';
import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';
import { GlassCard } from '@/components/ui/GlassCard';
import { FileUpload } from '@/components/ui/FileUpload';
import { DataGrid } from '@/components/ui/DataGrid';
import { motion, AnimatePresence } from 'framer-motion';

export default function FiscalAuditPage() {
    const [file, setFile] = useState<File | null>(null);
    const [loading, setLoading] = useState(false);
    const [data, setData] = useState<any[]>([]);
    const [riskAnalysis, setRiskAnalysis] = useState<any>(null);

    const handleProcess = () => {
        if (!file) return;
        setLoading(true);

        // Simulation
        setTimeout(() => {
            const mockData = [
                { Fecha: '2026-01-15', Tercero: 'DISTRIBUIDORA XYZ', NIT: '900123000', Concepto: 'Compra Mercancia', Valor: 12500000, Medio_Pago: 'Efectivo', Nivel_Riesgo: 'ALTO' },
                { Fecha: '2026-01-18', Tercero: 'TRANSPORTES RAPIDOS', NIT: '800555666', Concepto: 'Flete', Valor: 2500000, Medio_Pago: 'Transferencia', Nivel_Riesgo: 'BAJO' },
                { Fecha: '2026-01-22', Tercero: 'PAPELERIA CENTRAL', NIT: '901222333', Concepto: 'Insumos', Valor: 450000, Medio_Pago: 'Caja Menor', Nivel_Riesgo: 'MEDIO' },
            ];

            setRiskAnalysis({
                total_riesgo: 12500000,
                hallazgos_altos: 1,
                hallazgos_medios: 1,
                mensaje_clave: "Posible Desconocimiento de Costos por Pagos en Efectivo"
            });
            setData(mockData);
            setLoading(false);
        }, 2500);
    };

    const handleDownloadExcel = () => {
        if (data.length === 0) return;
        const worksheet = XLSX.utils.json_to_sheet(data);
        const workbook = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(workbook, worksheet, "Hallazgos Fiscales");
        XLSX.writeFile(workbook, `Auditoria_Fiscal_771-5_${new Date().toISOString().split('T')[0]}.xlsx`);
    };

    const handleDownloadPDF = () => {
        if (data.length === 0) return;
        const doc = new jsPDF();

        // Header
        doc.setFontSize(20);
        doc.setTextColor(40);
        doc.text("Auditoría Fiscal - Art. 771-5 E.T.", 14, 22);

        doc.setFontSize(10);
        doc.setTextColor(100);
        doc.text("Validación de Bancarización y Medios de Pago", 14, 30);

        // Resumen
        if (riskAnalysis) {
            doc.setFillColor(255, 241, 242); // rose-50
            doc.rect(14, 40, 180, 25, 'F');

            doc.setFontSize(11);
            doc.setTextColor(190, 18, 60); // rose-700
            doc.text(`Riesgo de Rechazo Fiscal Detectado: $${riskAnalysis.total_riesgo.toLocaleString()}`, 20, 52);
            doc.setFontSize(9);
            doc.setTextColor(80);
            doc.text(riskAnalysis.mensaje_clave, 20, 60);
        }

        // Tabla Hallazgos
        const columns = ["Fecha", "Tercero", "NIT", "Concepto", "Valor", "Medio Pago", "Riesgo"];
        const rows = data.map(d => [
            d.Fecha,
            d.Tercero,
            d.NIT,
            d.Concepto,
            `$${d.Valor.toLocaleString()}`,
            d.Medio_Pago,
            d.Nivel_Riesgo
        ]);

        autoTable(doc, {
            head: [columns],
            body: rows,
            startY: 75,
            headStyles: { fillColor: [225, 29, 72] }, // Red header
            styles: { fontSize: 8 },
            columnStyles: {
                4: { halign: 'right' },
                6: { fontStyle: 'bold' } // Riesgo bold
            }
        });

        doc.save(`Auditoria_Fiscal_${new Date().toISOString().split('T')[0]}.pdf`);
    };

    return (
        <div className="space-y-8 max-w-7xl mx-auto">
            <div className="flex items-center gap-4">
                <div className="p-4 rounded-2xl bg-gradient-to-br from-rose-500/20 to-orange-500/20 border border-rose-500/20">
                    <ShieldAlert className="w-10 h-10 text-rose-400" />
                </div>
                <div>
                    <h1 className="text-3xl font-bold font-space text-white">Auditoría Fiscal (Art. 771-5)</h1>
                    <p className="text-slate-400">Validación de Bancarización y Medios de Pago legales.</p>
                </div>
            </div>

            <AnimatePresence mode="wait">
                {data.length === 0 ? (
                    <motion.div
                        key="upload"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                    >
                        <GlassCard className="min-h-[400px] flex flex-col justify-center items-center text-center space-y-8 border-rose-500/30">
                            <div className="p-6 rounded-full bg-rose-900/20 border border-rose-500/30 animate-pulse">
                                <Upload className="w-16 h-16 text-rose-400" />
                            </div>
                            <div className="max-w-lg space-y-2">
                                <h3 className="text-xl font-bold text-white">Auditoría de Pagos y Bancarización</h3>
                                <p className="text-slate-400">Sube tu Auxiliar de Gastos. Detectaremos pagos en efectivo que superen los topes legales y pongan en riesgo la deducibilidad.</p>
                            </div>

                            <div className="w-full max-w-md bg-slate-900/50 p-4 rounded-xl border border-white/5">
                                <FileUpload
                                    accept=".xlsx,.csv"
                                    label="Cargar Auxiliar de Gastos"
                                    onFilesSelected={(f) => setFile(f[0])}
                                />
                                {file && <p className="mt-2 text-emerald-400 text-sm flex items-center justify-center gap-1 font-medium bg-emerald-500/10 p-2 rounded">✅ Listo: {file.name}</p>}
                            </div>

                            <button
                                onClick={handleProcess}
                                disabled={!file || loading}
                                className="btn-primary flex items-center gap-3 disabled:opacity-50"
                            >
                                {loading ? (
                                    <>
                                        <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                                        Validando Art. 771-5...
                                    </>
                                ) : (
                                    <>
                                        <AlertOctagon className="w-5 h-5" />
                                        Iniciar Auditoría Fiscal
                                    </>
                                )}
                            </button>
                        </GlassCard>
                    </motion.div>
                ) : (
                    <motion.div
                        key="results"
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="space-y-8"
                    >
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                            <GlassCard className="bg-rose-900/20 border-rose-500/30">
                                <p className="text-xs text-slate-400 uppercase font-bold">Riesgo de Rechazo</p>
                                <h2 className="text-3xl font-bold text-rose-400 mt-2">${riskAnalysis.total_riesgo.toLocaleString()}</h2>
                                <p className="text-xs text-rose-300 mt-1">Costos no deducibles potenciales</p>
                            </GlassCard>
                            <GlassCard className="bg-white/5">
                                <p className="text-xs text-slate-400 uppercase font-bold">Transacciones Críticas</p>
                                <h2 className="text-3xl font-bold text-white mt-2">{riskAnalysis.hallazgos_altos}</h2>
                                <p className="text-xs text-slate-500 mt-1">Requieren soporte bancario</p>
                            </GlassCard>
                            <GlassCard className="bg-white/5">
                                <p className="text-xs text-slate-400 uppercase font-bold">Alertas Medias</p>
                                <h2 className="text-3xl font-bold text-white mt-2">{riskAnalysis.hallazgos_medios}</h2>
                                <p className="text-xs text-slate-500 mt-1">Caja menor / Soportes</p>
                            </GlassCard>
                        </div>

                        {/* Smart Advisor */}
                        <GlassCard className="bg-slate-900/50 border-orange-500/30">
                            <div className="flex items-center gap-3 mb-6">
                                <div className="w-10 h-10 rounded-full bg-orange-500/20 flex items-center justify-center">
                                    <Brain className="w-6 h-6 text-orange-400" />
                                </div>
                                <div>
                                    <h3 className="text-xl font-bold text-white">Smart Advisor / Recomendación Fiscal</h3>
                                    <p className="text-sm text-orange-300">Análisis basado en Estatuto Tributario Art. 771-5 (Bancarización)</p>
                                </div>
                            </div>

                            <div className="space-y-6 text-sm text-slate-300">
                                <div className="p-4 rounded-lg bg-rose-900/10 border border-rose-500/20 flex items-start gap-4">
                                    <div className="p-2 bg-rose-500/20 rounded-lg">
                                        <AlertOctagon className="w-6 h-6 text-rose-400" />
                                    </div>
                                    <div>
                                        <h4 className="font-bold text-rose-400 mb-1">Alerta Crítica: Pagos en Efectivo Superiores al Límite</h4>
                                        <p>Se identificaron pagos a "DISTRIBUIDORA XYZ" por valor de $12.5M realizados en efectivo. Según el Art. 771-5, estos pagos <strong>NO serán deducibles</strong> en Renta ni el IVA descontable, ya que superan los topes individuales permitidos para efectivo.</p>
                                    </div>
                                </div>

                                <div>
                                    <h4 className="text-lg font-bold text-white mb-3 text-orange-400">Recomendaciones del Experto</h4>
                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                        <div className="bg-white/5 p-4 rounded-xl">
                                            <p className="font-bold text-white mb-2">1. Bancarización Inmediata</p>
                                            <p className="text-xs text-slate-400">Implementar política de "Cero Efectivo" para proveedores recurrentes. Usar transferencias o cheques de primer beneficiario.</p>
                                        </div>
                                        <div className="bg-white/5 p-4 rounded-xl">
                                            <p className="font-bold text-white mb-2">2. Declaración de Renta</p>
                                            <p className="text-xs text-slate-400">Depurar estos $12.5M como "Gastos No Deducibles" en la conciliación fiscal para evitar correcciones provocadas por la DIAN.</p>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            {/* Download Actions */}
                            <div className="flex flex-col sm:flex-row gap-4 mt-8 pt-6 border-t border-white/5">
                                <button
                                    onClick={handleDownloadExcel}
                                    className="flex-1 btn-primary bg-emerald-600 hover:bg-emerald-500 border-emerald-500/50 flex items-center justify-center gap-2 py-4 shadow-lg hover:shadow-emerald-500/20 transition-all"
                                >
                                    <FileSpreadsheet className="w-5 h-5" />
                                    Descargar Papeles de Trabajo (Excel)
                                </button>
                                <button
                                    onClick={handleDownloadPDF}
                                    className="flex-1 btn-secondary border-white/10 hover:bg-white/5 flex items-center justify-center gap-2 py-4 text-white hover:text-emerald-300 transition-colors"
                                >
                                    <FileText className="w-5 h-5" />
                                    Informe Ejecutivo (PDF)
                                </button>
                            </div>
                        </GlassCard>

                        <DataGrid data={data} title="Hallazgos Transaccionales" />

                        <div className="flex justify-center mt-4">
                            <button onClick={() => { setData([]); setFile(null); }} className="text-slate-500 hover:text-white flex items-center gap-2 transition-colors">
                                <ArrowRight className="w-4 h-4 rotate-180" /> Analizar otro archivo
                            </button>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
}
