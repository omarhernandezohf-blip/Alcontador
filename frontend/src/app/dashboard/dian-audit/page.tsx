'use client';

import { useState } from 'react';
import { ShieldCheck, Upload, FileSpreadsheet, ArrowRight, Brain, AlertTriangle, FileText } from 'lucide-react';
import * as XLSX from 'xlsx';
import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';
import { GlassCard } from '@/components/ui/GlassCard';
import { FileUpload } from '@/components/ui/FileUpload';
import { motion, AnimatePresence } from 'framer-motion';

export default function DianAuditPage() {
    const [dianFile, setDianFile] = useState<File | null>(null);
    const [contaFile, setContaFile] = useState<File | null>(null);
    const [isProcessing, setIsProcessing] = useState(false);
    const [results, setResults] = useState<any[] | null>(null);

    const handleAudit = () => {
        if (!dianFile || !contaFile) return;
        setIsProcessing(true);
        setResults(null);

        // Simulación de proceso
        setTimeout(() => {
            setIsProcessing(false);
            setResults([
                { nit: '900123456', razon: 'PROVEEDOR EJEMPLO S.A.S', valorDian: 5000000, valorConta: 4800000, diff: 200000, tipo: 'INEXACTITUD' },
                { nit: '800987654', razon: 'SERVICIOS LOGISTICOS LTDA', valorDian: 1200000, valorConta: 0, diff: 1200000, tipo: 'OMISIÓN' },
                { nit: '901222333', razon: 'PAPELERIA EL CENTRO', valorDian: 350000, valorConta: 350000, diff: 0, tipo: 'OK' },
            ]);
        }, 2500);
    };

    const handleDownloadExcel = () => {
        if (!results) return;
        const worksheet = XLSX.utils.json_to_sheet(results);
        const workbook = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(workbook, worksheet, "Auditoría DIAN");
        XLSX.writeFile(workbook, `Auditoria_DIAN_${new Date().toISOString().split('T')[0]}.xlsx`);
    };

    const handleDownloadPDF = () => {
        if (!results) return;
        const doc = new jsPDF();

        // Header
        doc.setFontSize(20);
        doc.setTextColor(40, 40, 40);
        doc.text("Auditoría de Exógena (Cruce DIAN)", 14, 22);

        doc.setFontSize(10);
        doc.setTextColor(100);
        doc.text(`Generado el: ${new Date().toLocaleDateString()}`, 14, 30);

        // Indicadores
        doc.setFillColor(254, 242, 242); // rose-50
        doc.roundedRect(14, 40, 180, 25, 3, 3, 'F');

        doc.setFontSize(10);
        doc.setTextColor(60);
        doc.text("Total Diferencias Detectadas", 20, 50);
        doc.setFontSize(16);
        doc.setTextColor(220, 38, 38); // rose-600
        doc.text(`$24.300.000`, 20, 60);

        // Tabla
        const tableColumn = ["NIT", "Razón Social", "Valor DIAN", "Valor Conta", "Diferencia", "Tipo"];
        const tableRows = results.map(row => [
            row.nit,
            row.razon,
            `$${row.valorDian.toLocaleString()}`,
            `$${row.valorConta.toLocaleString()}`,
            `$${row.diff.toLocaleString()}`,
            row.tipo
        ]);

        autoTable(doc, {
            head: [tableColumn],
            body: tableRows,
            startY: 75,
            theme: 'grid',
            headStyles: { fillColor: [37, 99, 235], textColor: 255 }, // Blue header
            styles: { fontSize: 8 },
            columnStyles: {
                2: { halign: 'right' },
                3: { halign: 'right' },
                4: { halign: 'right', fontStyle: 'bold', textColor: [220, 38, 38] }
            }
        });

        // Footer Smart Advisor
        const finalY = (doc as any).lastAutoTable.finalY || 120;
        doc.setFontSize(12);
        doc.setTextColor(40);
        doc.text("Análisis de Riesgo (IA)", 14, finalY + 15);
        doc.setFontSize(9);
        doc.setTextColor(80);
        const splitText = doc.splitTextToSize("Se detectaron inconsistencias críticas que podrían activar una sanción por inexactitud. Se recomienda corregir los terceros indicados antes de la firmeza de la declaración.", 180);
        doc.text(splitText, 14, finalY + 22);

        doc.save(`Auditoria_DIAN_${new Date().toISOString().split('T')[0]}.pdf`);
    };

    return (
        <div className="space-y-8 max-w-6xl mx-auto">
            <div className="flex items-center gap-4">
                <div className="p-4 rounded-2xl bg-gradient-to-br from-blue-600/20 to-indigo-600/20 border border-blue-500/20">
                    <ShieldCheck className="w-10 h-10 text-blue-400" />
                </div>
                <div>
                    <h1 className="text-3xl font-bold font-space text-white">Auditoría de Exógena (Cruce DIAN)</h1>
                    <p className="text-slate-400">Detecta discrepancias entre lo reportado para evitar la sanción del Art. 651.</p>
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8 relative">
                {/* Connector Line */}
                <div className="hidden md:block absolute top-[40%] left-[50%] -translate-x-1/2 -translate-y-1/2 z-10">
                    <div className="w-12 h-12 rounded-full bg-slate-900 border border-white/10 flex items-center justify-center animate-pulse">
                        <ArrowRight className="w-6 h-6 text-indigo-400" />
                    </div>
                </div>

                <GlassCard className="relative overflow-hidden group border-blue-500/30">
                    <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
                        <ShieldCheck className="w-24 h-24 rotate-12" />
                    </div>
                    <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
                        <span className="w-8 h-8 rounded-full bg-blue-500/20 flex items-center justify-center text-sm">1</span>
                        Archivo DIAN
                    </h3>
                    <p className="text-sm text-slate-400 mb-6">Sube el Excel descargado del portal de la DIAN ("Información Reportada por Terceros").</p>
                    <FileUpload
                        accept=".xlsx"
                        label="Reporte DIAN (.xlsx)"
                        onFilesSelected={(files) => setDianFile(files[0])}
                    />
                    {dianFile && <p className="mt-2 text-emerald-400 text-sm flex items-center gap-1 font-medium bg-emerald-500/10 p-2 rounded">✅ Archivo Cargado: {dianFile.name}</p>}
                </GlassCard>

                <GlassCard className="relative overflow-hidden group border-indigo-500/30">
                    <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
                        <FileSpreadsheet className="w-24 h-24 rotate-12" />
                    </div>
                    <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
                        <span className="w-8 h-8 rounded-full bg-indigo-500/20 flex items-center justify-center text-sm">2</span>
                        Contabilidad
                    </h3>
                    <p className="text-sm text-slate-400 mb-6">Sube tu Libro Auxiliar por Terceros para cruzar la información.</p>
                    <FileUpload
                        accept=".xlsx"
                        label="Auxiliar Contable (.xlsx)"
                        onFilesSelected={(files) => setContaFile(files[0])}
                    />
                    {contaFile && <p className="mt-2 text-emerald-400 text-sm flex items-center gap-1 font-medium bg-emerald-500/10 p-2 rounded">✅ Archivo Cargado: {contaFile.name}</p>}
                </GlassCard>
            </div>

            <div className="flex justify-center">
                <button
                    onClick={handleAudit}
                    disabled={!dianFile || !contaFile || isProcessing}
                    className="btn-primary text-lg px-12 py-4 flex items-center gap-3 disabled:opacity-50 disabled:cursor-not-allowed shadow-[0_0_30px_rgba(59,130,246,0.3)] hover:shadow-[0_0_50px_rgba(59,130,246,0.5)] transition-all"
                >
                    {isProcessing ? (
                        <>
                            <div className="w-6 h-6 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                            <span>Procesando Cruce de Datos...</span>
                        </>
                    ) : (
                        <>
                            <ShieldCheck className="w-6 h-6" />
                            Ejecutar Auditoría Maestra
                        </>
                    )}
                </button>
            </div>

            {/* Results Section */}
            {results && (
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="space-y-6"
                >
                    <div className="flex items-center gap-4 mb-4">
                        <div className="h-px flex-1 bg-gradient-to-r from-transparent via-white/20 to-transparent"></div>
                        <h3 className="text-2xl font-bold text-white">Resultados del Hallazgo</h3>
                        <div className="h-px flex-1 bg-gradient-to-r from-transparent via-white/20 to-transparent"></div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                        <GlassCard className="border-rose-500/30">
                            <h4 className="text-rose-300 font-bold">Total Diferencias</h4>
                            <p className="text-3xl font-bold text-white mt-2">$24.3M</p>
                            <p className="text-sm text-slate-400">Riesgo Sancionatorio Alto</p>
                        </GlassCard>
                        <GlassCard className="border-amber-500/30">
                            <h4 className="text-amber-300 font-bold">Terceros con Error</h4>
                            <p className="text-3xl font-bold text-white mt-2">12</p>
                            <p className="text-sm text-slate-400">De 1,450 registros analizados</p>
                        </GlassCard>
                        <GlassCard className="border-emerald-500/30">
                            <h4 className="text-emerald-300 font-bold">Coincidencia Exacta</h4>
                            <p className="text-3xl font-bold text-white mt-2">98.2%</p>
                            <p className="text-sm text-slate-400">Calidad de Información</p>
                        </GlassCard>
                    </div>

                    <GlassCard>
                        <table className="w-full text-sm">
                            <thead className="text-slate-400 border-b border-white/10">
                                <tr>
                                    <th className="py-3 text-left">NIT</th>
                                    <th className="py-3 text-left">Razón Social</th>
                                    <th className="py-3 text-right">Valor DIAN</th>
                                    <th className="py-3 text-right">Valor Contabilidad</th>
                                    <th className="py-3 text-right">Diferencia</th>
                                    <th className="py-3 text-center">Tipo</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-white/5">
                                {results.map((r, i) => (
                                    <tr key={i} className="hover:bg-white/5 transition-colors">
                                        <td className="py-3 text-slate-300 font-mono">{r.nit}</td>
                                        <td className="py-3 text-slate-300">{r.razon}</td>
                                        <td className="py-3 text-right text-slate-400">${r.valorDian.toLocaleString()}</td>
                                        <td className="py-3 text-right text-slate-400">${r.valorConta.toLocaleString()}</td>
                                        <td className={`py-3 text-right font-bold ${r.diff > 0 ? 'text-rose-400' : 'text-emerald-400'}`}>
                                            ${r.diff.toLocaleString()}
                                        </td>
                                        <td className="py-3 text-center">
                                            <span className={`px-2 py-1 rounded text-xs font-bold ${r.tipo === 'OK' ? 'bg-emerald-500/20 text-emerald-400' :
                                                r.tipo === 'OMISIÓN' ? 'bg-rose-500/20 text-rose-400' : 'bg-amber-500/20 text-amber-400'
                                                }`}>
                                                {r.tipo}
                                            </span>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </GlassCard>

                    {/* Smart Advisor Section */}
                    <GlassCard className="bg-slate-900/50 border-indigo-500/30">
                        <div className="flex items-center gap-3 mb-6">
                            <div className="w-10 h-10 rounded-full bg-indigo-500/20 flex items-center justify-center">
                                <Brain className="w-6 h-6 text-indigo-400" />
                            </div>
                            <div>
                                <h3 className="text-xl font-bold text-white">Smart Advisor / Resumen Inteligente</h3>
                                <p className="text-sm text-indigo-300">Análisis de Riesgos Fiscales y de Seguridad Social (IA)</p>
                            </div>
                        </div>

                        <div className="space-y-6 text-sm text-slate-300">
                            <div className="p-4 rounded-lg bg-rose-500/10 border border-rose-500/20 flex items-start gap-4">
                                <AlertTriangle className="w-6 h-6 text-rose-400 shrink-0" />
                                <div>
                                    <h4 className="font-bold text-rose-400 mb-1">Escenario Detectado: Inconsistencia Crítica</h4>
                                    <p>Se ha detectado una diferencia acumulada de <strong className="text-white">$1,400,000</strong>. Este hallazgo conlleva riesgos significativos tanto en el ámbito tributario (DIAN) como en el de seguridad social (UGPP).</p>
                                </div>
                            </div>

                            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                                <div>
                                    <h4 className="text-lg font-bold text-white mb-3 text-indigo-400 flex items-center gap-2">
                                        <span className="w-6 h-6 rounded-full bg-indigo-500/20 flex items-center justify-center text-xs">I</span>
                                        Riesgos ante la DIAN
                                    </h4>
                                    <p className="mb-4 text-xs text-slate-400">La DIAN podría interpretar esta diferencia como una <strong className="text-white">Omisión de Ingresos</strong> o un <strong className="text-white">Pasivo Inexistente</strong>, afectando Renta e IVA.</p>
                                    <ul className="list-disc list-inside space-y-2 pl-2">
                                        <li><span className="text-white font-bold">Riesgo Sistémico:</span> Si el error es reiterado, podría activar una Auditoría Integral.</li>
                                        <li><span className="text-white font-bold">Sanción de Inexactitud:</span> Multa de hasta el 100% de la diferencia del impuesto a cargo.</li>
                                    </ul>
                                </div>

                                <div>
                                    <h4 className="text-lg font-bold text-white mb-3 text-purple-400 flex items-center gap-2">
                                        <span className="w-6 h-6 rounded-full bg-purple-500/20 flex items-center justify-center text-xs">II</span>
                                        Riesgos ante la UGPP
                                    </h4>
                                    <p className="mb-4 text-xs text-slate-400">Si la diferencia corresponde a pagos a terceros no reportados correctamente:</p>
                                    <ul className="list-disc list-inside space-y-2 pl-2">
                                        <li><span className="text-white font-bold">Base de Cotización (IBC):</span> La UGPP podría recalcular el IBC sumando estos valores como pagos ocultos.</li>
                                        <li><span className="text-white font-bold">Sanción por Omisión:</span> Multa equivalente al 35% del valor de los aportes dejados de pagar.</li>
                                    </ul>
                                </div>
                            </div>
                        </div>

                        {/* Download Actions */}
                        <div className="flex flex-col sm:flex-row gap-4 mt-8">
                            <button
                                onClick={handleDownloadExcel}
                                className="flex-1 btn-primary bg-emerald-600 hover:bg-emerald-500 border-emerald-500/50 flex items-center justify-center gap-2 py-4 shadow-lg hover:shadow-emerald-500/20 transition-all"
                            >
                                <FileSpreadsheet className="w-5 h-5" />
                                Descargar Reporte Excel
                            </button>
                            <button
                                onClick={handleDownloadPDF}
                                className="flex-1 btn-secondary border-white/10 hover:bg-white/5 flex items-center justify-center gap-2 py-4 text-white hover:text-emerald-300 transition-colors"
                            >
                                <FileText className="w-5 h-5" />
                                Descargar Informe PDF
                            </button>
                        </div>
                    </GlassCard>
                </motion.div>
            )}

            {/* Info Card - (Mantener abajo) */}
            <GlassCard className="bg-indigo-900/10 border-indigo-500/20 mt-8">
                <h4 className="font-bold text-indigo-300 mb-2"> BENEFICIOS CLAVE</h4>
                <ul className="list-disc list-inside text-slate-400 text-sm space-y-1">
                    <li>Evita sanciones del Art. 651 ET.</li>
                    <li>Cruce automático de NITs y verificación de Dígitos de Verificación.</li>
                    <li>Reporte detallado de diferencias (Omitidos vs Inexactos).</li>
                </ul>
            </GlassCard>
        </div>
    );
}
