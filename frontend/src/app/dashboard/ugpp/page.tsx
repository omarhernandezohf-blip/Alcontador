'use client';

import { useState } from 'react';
import { Users, AlertTriangle, CheckCircle, Calculator, Upload, Brain, FileText, ArrowRight, FileSpreadsheet } from 'lucide-react';
import * as XLSX from 'xlsx';
import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';
import { GlassCard } from '@/components/ui/GlassCard';
import { FileUpload } from '@/components/ui/FileUpload';
import { FileGuide } from '@/components/ui/FileGuide';
import { motion, AnimatePresence } from 'framer-motion';

export default function UgppPage() {
    const [file, setFile] = useState<File | null>(null);
    const [isProcessing, setIsProcessing] = useState(false);
    const [result, setResult] = useState<any>(null);

    const handleAnalyze = () => {
        if (!file) return;
        setIsProcessing(true);
        // Simulación
        setTimeout(() => {
            setIsProcessing(false);
            setResult({
                riesgo: 'ALTO',
                mensaje: 'Riesgo de Fiscalización UGPP Detectado',
                exceso: 15400000,
                nuevo_ibc: 45000000,
                empleados_afectados: 3
            });
        }, 2500);
    };

    const handleDownloadExcel = () => {
        // Mock de Planilla Ajustada
        const mockAdjusted = [
            { Empleado: 'Empleado 1', Ingreso_Total: 12000000, Pagos_No_Salariales: 6000000, Limite_40: 4800000, Exceso_IBC: 1200000, Estado: 'AJUSTADO' },
            { Empleado: 'Empleado 2', Ingreso_Total: 8500000, Pagos_No_Salariales: 4000000, Limite_40: 3400000, Exceso_IBC: 600000, Estado: 'AJUSTADO' },
            { Empleado: 'Empleado 3', Ingreso_Total: 15000000, Pagos_No_Salariales: 8000000, Limite_40: 6000000, Exceso_IBC: 2000000, Estado: 'AJUSTADO' },
        ];

        const worksheet = XLSX.utils.json_to_sheet(mockAdjusted);
        const workbook = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(workbook, worksheet, "Planilla Ajustada UGPP");
        XLSX.writeFile(workbook, `UGPP_Planilla_Ajustada_${new Date().toISOString().split('T')[0]}.xlsx`);
    };

    const handleDownloadPDF = () => {
        const doc = new jsPDF();

        // Header
        doc.setFontSize(20);
        doc.setTextColor(40);
        doc.text("Informe de Riesgo UGPP", 14, 22);
        doc.setFontSize(10);
        doc.text("Análisis de Pagos No Salariales (Ley 1393)", 14, 30);

        // Info Riesgo
        if (result) {
            doc.setFillColor(254, 242, 242); // rose-50
            doc.rect(14, 40, 180, 30, 'F');

            doc.setFontSize(12);
            doc.setTextColor(185, 28, 28); // rose-700
            doc.text(`NIVEL DE RIESGO: ${result.riesgo}`, 20, 50);

            doc.setFontSize(10);
            doc.setTextColor(60);
            doc.text(`Exceso Base Cotización (IBC): $${result.exceso.toLocaleString()}`, 20, 60);
            doc.text(`Empleados Afectados: ${result.empleados_afectados}`, 100, 60);
        }

        // Mock Table (Detalle Planilla)
        const columns = ["Empleado", "Ingreso Total", "Pagos No Salariales", "Límite 40%", "Exceso IBC"];
        const rows = [
            ["Empleado 1", "$12.000.000", "$6.000.000", "$4.800.000", "$1.200.000"],
            ["Empleado 2", "$8.500.000", "$4.000.000", "$3.400.000", "$600.000"],
            ["Empleado 3", "$15.000.000", "$8.000.000", "$6.000.000", "$2.000.000"],
        ];

        autoTable(doc, {
            head: [columns],
            body: rows,
            startY: 80,
            headStyles: { fillColor: [88, 28, 135] }, // Purple header
        });

        doc.save(`Informe_UGPP_${new Date().toISOString().split('T')[0]}.pdf`);
    };

    return (
        <div className="space-y-8 max-w-5xl mx-auto">
            <div className="flex items-center gap-4">
                <div className="p-4 rounded-2xl bg-gradient-to-br from-indigo-500/20 to-purple-500/20 border border-indigo-500/20">
                    <Users className="w-10 h-10 text-indigo-400" />
                </div>
                <div>
                    <h1 className="text-3xl font-bold font-space text-white">Escáner UGPP & Nómina</h1>
                    <p className="text-slate-400">Verifica el cumplimiento de la Ley 1393 y evita sanciones por pagos no salariales excesivos.</p>
                </div>
            </div>

            <AnimatePresence mode="wait">
                {!result ? (
                    <motion.div
                        key="upload"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                    >
                        <GlassCard className="min-h-[400px] flex flex-col items-center justify-center text-center space-y-8 border-indigo-500/30">
                            <div className="p-6 rounded-full bg-indigo-900/20 border border-indigo-500/30 animate-pulse">
                                <Upload className="w-16 h-16 text-indigo-400" />
                            </div>
                            <div className="max-w-lg space-y-2">
                                <h3 className="text-xl font-bold text-white">Auditoría Preventiva de Nómina</h3>
                                <p className="text-slate-400">Sube tu planilla de nómina mensual (.xlsx). Analizaremos la proporción de pagos salariales vs no salariales (regla 60/40).</p>
                            </div>

                            <div className="w-full max-w-md">
                                <div className="flex justify-end mb-2">
                                    <FileGuide
                                        moduleName="UGPP / Nómina"
                                        requiredColumns={['Empleado', 'Ingreso_Total', 'Pagos_No_Salariales']}
                                        exampleRow={{ 'Empleado': 'Juan Perez', 'Ingreso_Total': '5000000', 'Pagos_No_Salariales': '2500000' }}
                                        tips={['El sistema validará si lo NO salarial supera el 40% del total (Ley 1393)']}
                                    />
                                </div>
                                <FileUpload
                                    accept=".xlsx"
                                    label="Cargar Planilla Mensual"
                                    onFilesSelected={(f) => setFile(f[0])}
                                />
                                {file && <p className="mt-2 text-emerald-400 text-sm flex items-center justify-center gap-1 font-medium bg-emerald-500/10 p-2 rounded">✅ Cargado: {file.name}</p>}
                            </div>

                            <button
                                onClick={handleAnalyze}
                                disabled={!file || isProcessing}
                                className="btn-primary px-12 py-3 flex items-center gap-3 disabled:opacity-50"
                            >
                                {isProcessing ? (
                                    <>
                                        <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                                        Analizando Ley 1393...
                                    </>
                                ) : (
                                    <>
                                        <Calculator className="w-5 h-5" />
                                        Ejecutar Escáner UGPP
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
                        {/* KPI Cards */}
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                            <GlassCard className="bg-rose-900/10 border-rose-500/30">
                                <p className="text-xs text-slate-400 uppercase font-bold">Nivel de Riesgo</p>
                                <h2 className="text-3xl font-bold text-rose-400 mt-2">Grave</h2>
                                <p className="text-xs text-rose-300 mt-1">Excede límite 40%</p>
                            </GlassCard>
                            <GlassCard className="bg-white/5">
                                <p className="text-xs text-slate-400 uppercase font-bold">Exceso Detectado</p>
                                <h2 className="text-3xl font-bold text-white mt-2">${result.exceso.toLocaleString()}</h2>
                                <p className="text-xs text-slate-500 mt-1">Base gravable omitida</p>
                            </GlassCard>
                            <GlassCard className="bg-white/5">
                                <p className="text-xs text-slate-400 uppercase font-bold">Empleados Afectados</p>
                                <h2 className="text-3xl font-bold text-white mt-2">{result.empleados_afectados}</h2>
                                <p className="text-xs text-slate-500 mt-1">Requieren ajuste inmediato</p>
                            </GlassCard>
                        </div>

                        {/* Smart Advisor */}
                        <GlassCard className="bg-slate-900/50 border-purple-500/30">
                            <div className="flex items-center gap-3 mb-6">
                                <div className="w-10 h-10 rounded-full bg-purple-500/20 flex items-center justify-center">
                                    <Brain className="w-6 h-6 text-purple-400" />
                                </div>
                                <div>
                                    <h3 className="text-xl font-bold text-white">Smart Advisor / Resumen Inteligente</h3>
                                    <p className="text-sm text-purple-300">Análisis de Impacto Sancionatorio - Unidad de Gestión Pensional</p>
                                </div>
                            </div>

                            <div className="space-y-6 text-sm text-slate-300">
                                <div className="p-4 rounded-lg bg-indigo-900/20 border-l-4 border-indigo-500">
                                    <h4 className="font-bold text-indigo-300 mb-2">Diagnóstico Ley 1393 de 2010</h4>
                                    <p>Hemos detectado que en {result.empleados_afectados} empleados, los pagos no constitutivos de salario superan el 40% del total de la remuneración. El exceso de <strong className="text-white">${result.exceso.toLocaleString()}</strong> debe formar parte de la base de cotización a seguridad social.</p>
                                </div>

                                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                                    <div>
                                        <h4 className="font-bold text-white mb-3 flex items-center gap-2">
                                            <AlertTriangle className="w-4 h-4 text-amber-400" />
                                            Acción Requerida
                                        </h4>
                                        <ul className="list-disc list-inside space-y-2 pl-2 text-slate-400">
                                            <li>Ajustar la planilla PILA inmediatamente realizando la corrección.</li>
                                            <li>Pagar el excedente de aportes antes de cualquier requerimiento persuasivo.</li>
                                            <li>Revisar contratos de "bonificaciones habituales" para evitar reincidencia.</li>
                                        </ul>
                                    </div>
                                    <div>
                                        <h4 className="font-bold text-white mb-3 flex items-center gap-2">
                                            <Users className="w-4 h-4 text-emerald-400" />
                                            Impacto Financiero
                                        </h4>
                                        <p className="mb-2">Si no se corrige voluntariamente:</p>
                                        <ul className="list-disc list-inside space-y-2 pl-2 text-slate-400">
                                            <li>Intereses de mora diarios sobre el aporte omitido.</li>
                                            <li>Sanción del 35% si la UGPP detecta la omisión antes que usted corrija.</li>
                                        </ul>
                                    </div>
                                </div>
                            </div>

                            <div className="mt-8 pt-4 border-t border-white/5 flex flex-col gap-4">
                                <div className="flex flex-col sm:flex-row gap-4">
                                    <button
                                        onClick={handleDownloadExcel}
                                        className="flex-1 btn-primary bg-emerald-600 hover:bg-emerald-500 border-emerald-500/50 flex items-center justify-center gap-2 py-3 shadow-lg hover:shadow-emerald-500/20 transition-all"
                                    >
                                        <FileSpreadsheet className="w-5 h-5" />
                                        Exportar Planilla Ajustada (Excel)
                                    </button>
                                    <button
                                        onClick={handleDownloadPDF}
                                        className="flex-1 btn-secondary border-white/10 hover:bg-white/5 flex items-center justify-center gap-2 py-3 text-white hover:text-emerald-300 transition-colors"
                                    >
                                        <FileText className="w-5 h-5" />
                                        Informe de Riesgo (PDF)
                                    </button>
                                </div>
                                <div className="flex justify-end">
                                    <button onClick={() => setResult(null)} className="text-sm text-slate-500 hover:text-white flex items-center gap-2 transition-colors">
                                        Analizar otro periodo <ArrowRight className="w-4 h-4" />
                                    </button>
                                </div>
                            </div>
                        </GlassCard>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
}
