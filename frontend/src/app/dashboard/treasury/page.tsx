'use client';

import { useState, useRef } from 'react';
import * as XLSX from 'xlsx';
import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';
import {
    TrendingUp, Wallet, ArrowUpRight, ArrowDownRight,
    UploadCloud, FileSpreadsheet, Info, CheckCircle2, AlertCircle,
    Download, FileText, Brain
} from 'lucide-react';
import { TreasuryChart } from '@/components/modules/TreasuryChart';
import { GlassCard } from '@/components/ui/GlassCard';
import { FileUpload } from '@/components/ui/FileUpload';
import { FileGuide } from '@/components/ui/FileGuide';
import { motion, AnimatePresence } from 'framer-motion';

export default function TreasuryPage() {
    const [viewState, setViewState] = useState<'upload' | 'analyzing' | 'results'>('upload');
    const [data, setData] = useState<any[]>([]);
    const [error, setError] = useState<string | null>(null);
    const fileInputRef = useRef<HTMLInputElement>(null);

    const triggerFileUpload = () => {
        fileInputRef.current?.click();
    };

    const processFile = async (file: File) => {
        if (!file) return;

        setViewState('analyzing');
        setError(null);

        try {
            const buffer = await file.arrayBuffer();
            const workbook = XLSX.read(buffer, { type: 'array' });
            const sheetName = workbook.SheetNames[0];
            const sheet = workbook.Sheets[sheetName];
            const rawData = XLSX.utils.sheet_to_json<any>(sheet);

            if (rawData.length === 0) throw new Error("El archivo parece estar vacío.");

            // 1. Detect Columns (Simple Heuristic for Realism)
            const keys = Object.keys(rawData[0]).map(k => k.toLowerCase());
            const dateKey = keys.find(k => k.includes('fecha') || k.includes('date') || k.includes('mes'));
            const incomeKey = keys.find(k => k.includes('ingreso') || k.includes('haber') || k.includes('crédito') || k.includes('credito'));
            const expenseKey = keys.find(k => k.includes('egreso') || k.includes('gasto') || k.includes('debe') || k.includes('débito') || k.includes('debito'));

            // 2. Process & Aggregate Real Data
            const monthlyStats: Record<string, { ingresos: number, egresos: number }> = {};

            rawData.forEach((row: any) => {
                // Normalize keys
                const rowNormalized: any = {};
                Object.keys(row).forEach(k => rowNormalized[k.toLowerCase()] = row[k]);

                const dateVal = rowNormalized[dateKey || 'fecha'];
                const incomeVal = Number(rowNormalized[incomeKey || 'ingresos'] || 0);
                const expenseVal = Number(rowNormalized[expenseKey || 'egresos'] || 0);

                // Simple Month Grouping
                let monthLabel = "General";
                if (dateVal) {
                    // Try to parse date
                    try {
                        const dateObj = new Date(dateVal); // Works for some string formats
                        // If generic string or excel serial, simplistic handling for MVP realism:
                        if (!isNaN(dateObj.getTime())) {
                            monthLabel = dateObj.toLocaleString('es-CO', { month: 'long', year: 'numeric' });
                        } else {
                            // Fallback for strings like "Enero", "Feb"
                            monthLabel = String(dateVal);
                        }
                    } catch (err) {
                        monthLabel = String(dateVal);
                    }
                }

                if (!monthlyStats[monthLabel]) monthlyStats[monthLabel] = { ingresos: 0, egresos: 0 };
                monthlyStats[monthLabel].ingresos += isNaN(incomeVal) ? 0 : incomeVal;
                monthlyStats[monthLabel].egresos += isNaN(expenseVal) ? 0 : expenseVal;
            });

            // 3. Format for Chart
            const finalData = Object.entries(monthlyStats).map(([mes, vals]) => ({
                mes: mes.charAt(0).toUpperCase() + mes.slice(1),
                ingresos: vals.ingresos,
                egresos: vals.egresos,
                flujoNeto: vals.ingresos - vals.egresos,
                margen: vals.ingresos > 0 ? ((vals.ingresos - vals.egresos) / vals.ingresos) * 100 : 0
            }));

            if (finalData.length === 0) {
                // Fallback if columns not found, treat as single summary row from raw if numeric
                // This is just to ensure SOMETHING shows if the user uploads a valid but weirdly named file
                throw new Error("No pudimos detectar columnas de 'Fecha', 'Ingresos' o 'Egresos'.");
            }

            // Real delay just for UI transition smoothness (not fake processing)
            setTimeout(() => {
                setData(finalData);
                setViewState('results');
            }, 800);

        } catch (err) {
            console.error(err);
            setError(err instanceof Error ? err.message : "Error procesando el archivo");
            setViewState('upload');
        } finally {
            // Reset input
            if (fileInputRef.current) fileInputRef.current.value = '';
        }
    };

    const handleDownload = (format: 'xlsx' | 'pdf') => {
        if (format === 'xlsx') {
            const ws = XLSX.utils.json_to_sheet(data.map(item => ({
                Mes: item.mes,
                Ingresos: item.ingresos,
                Egresos: item.egresos,
                'Flujo Neto': item.flujoNeto,
                'Margen %': item.margen.toFixed(2) + '%'
            })));
            const wb = XLSX.utils.book_new();
            XLSX.utils.book_append_sheet(wb, ws, "Tesorería Real");
            XLSX.writeFile(wb, "Reporte_Tesoreria_Pro.xlsx");
        } else {
            const doc = new jsPDF();
            doc.setFontSize(20);
            doc.text("Reporte de Tesorería - Asistente Pro", 14, 22);

            doc.setFontSize(11);
            doc.text(`Generado: ${new Date().toLocaleDateString()}`, 14, 30);

            autoTable(doc, {
                startY: 40,
                head: [['Mes', 'Ingresos', 'Egresos', 'Flujo Neto', 'Margen']],
                body: data.map(item => [
                    item.mes || 'N/A',
                    `$${item.ingresos?.toLocaleString('es-CO') || '0'}`,
                    `$${item.egresos?.toLocaleString('es-CO') || '0'}`,
                    `$${item.flujoNeto?.toLocaleString('es-CO') || '0'}`,
                    `${item.margen?.toFixed(2) || '0.00'}%`
                ]),
            });
            doc.save("Reporte_Tesoreria_Pro.pdf");
        }
    };

    const totalIngresos = data.reduce((acc, curr) => acc + (curr.ingresos || 0), 0);
    const totalEgresos = data.reduce((acc, curr) => acc + (curr.egresos || 0), 0);
    const netCashflow = totalIngresos - totalEgresos;
    const margenpromedio = totalIngresos > 0 ? ((netCashflow / totalIngresos) * 100).toFixed(1) : "0.0";

    const bestMonth = [...data].sort((a, b) => b.flujoNeto - a.flujoNeto)[0];
    const riskCount = data.filter(d => d.flujoNeto < 0).length;

    return (
        <div className="space-y-8 max-w-7xl mx-auto">
            {/* Hidden Input */}
            <input
                type="file"
                ref={fileInputRef}
                onChange={(e) => {
                    const file = e.target.files?.[0];
                    if (file) processFile(file);
                }}
                className="hidden"
                accept=".xlsx,.xls,.csv"
            />

            {/* Header */}
            <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                    <div className="p-4 rounded-2xl bg-gradient-to-br from-cyan-500/20 to-blue-600/20 border border-cyan-500/20">
                        <Wallet className="w-10 h-10 text-cyan-400" />
                    </div>
                    <div>
                        <h1 className="text-3xl font-bold font-space text-white">Tesorería Real</h1>
                        <p className="text-slate-400">Análisis financiero basado en evidencia documental.</p>
                    </div>
                </div>
                {viewState === 'results' && (
                    <div className="flex gap-2">
                        <button onClick={() => handleDownload('xlsx')} className="p-2 rounded-lg bg-green-500/20 text-green-400 hover:bg-green-500/30 transition-colors">
                            <FileSpreadsheet className="w-5 h-5" />
                        </button>
                        <button onClick={() => handleDownload('pdf')} className="p-2 rounded-lg bg-red-500/20 text-red-400 hover:bg-red-500/30 transition-colors">
                            <FileText className="w-5 h-5" />
                        </button>
                    </div>
                )}
            </div>

            <AnimatePresence mode="wait">
                {viewState === 'upload' && (
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -20 }}
                        className="grid grid-cols-1 lg:grid-cols-2 gap-8"
                    >
                        <div className="flex justify-between items-center mb-6">
                            <div>
                                <h2 className="text-xl font-bold text-white mb-2">Cargar Movimientos</h2>
                                <p className="text-slate-400 text-sm">Sube tu reporte de banco o contabilidad</p>
                            </div>
                            <FileGuide
                                moduleName="Tesorería"
                                requiredColumns={['Fecha', 'Ingresos', 'Egresos', 'Concepto']}
                                exampleRow={{ 'Fecha': '2025-01-15', 'Ingresos': '5000000', 'Egresos': '0', 'Concepto': 'Pago Cliente' }}
                                tips={[
                                    'Las fechas pueden estar en formato YYYY-MM-DD o DD/MM/YYYY',
                                    'Los valores numéricos no deben tener símbolos de moneda, solo números',
                                    'Si no tienes columna "Concepto", el sistema la dejará en blanco'
                                ]}
                            />
                        </div>

                        <FileUpload
                            onFilesSelected={(files) => files[0] && processFile(files[0])}
                            accept=".xlsx, .xls, .csv"
                            label="Arrastra tu Excel de Flujo de Caja aquí"
                        />
                    </motion.div>
                )}

                {viewState === 'analyzing' && (
                    <motion.div
                        initial={{ opacity: 0, scale: 0.95 }}
                        animate={{ opacity: 1, scale: 1 }}
                        exit={{ opacity: 0, scale: 1.05 }}
                        className="flex flex-col items-center justify-center h-[500px]"
                    >
                        <div className="relative w-24 h-24 mb-8">
                            <div className="absolute inset-0 border-4 border-indigo-500/30 rounded-full animate-ping" />
                            <div className="absolute inset-2 border-4 border-t-indigo-500 border-r-transparent border-b-purple-500 border-l-transparent rounded-full animate-spin" />
                        </div>
                        <h2 className="text-2xl font-bold text-white mb-2">Procesando Matriz de Datos...</h2>
                        <p className="text-slate-400">Calculando totales reales y generando proyecciones</p>
                    </motion.div>
                )}

                {viewState === 'results' && (
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="space-y-8"
                    >
                        {/* KPIs Reales */}
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                            <GlassCard gradient className="border-l-4 border-emerald-500">
                                <p className="text-slate-400 text-sm">Ingresos Totales</p>
                                <h2 className="text-3xl font-bold text-white mt-1">
                                    ${new Intl.NumberFormat('es-CO', { notation: "compact" }).format(totalIngresos)}
                                </h2>
                            </GlassCard>

                            <GlassCard gradient className="border-l-4 border-rose-500">
                                <p className="text-slate-400 text-sm">Egresos Totales</p>
                                <h2 className="text-3xl font-bold text-white mt-1">
                                    ${new Intl.NumberFormat('es-CO', { notation: "compact" }).format(totalEgresos)}
                                </h2>
                            </GlassCard>

                            <GlassCard gradient className={`border-l-4 ${netCashflow >= 0 ? 'border-indigo-500' : 'border-amber-500'}`}>
                                <p className="text-slate-400 text-sm">Flujo Neto Real</p>
                                <h2 className={`text-3xl font-bold mt-1 ${netCashflow >= 0 ? 'text-white' : 'text-amber-400'}`}>
                                    ${new Intl.NumberFormat('es-CO', { notation: "compact" }).format(netCashflow)}
                                </h2>
                            </GlassCard>
                        </div>

                        <div className="h-[400px]">
                            <TreasuryChart data={data} />
                        </div>

                        {/* Smart Analysis Section */}
                        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                            {/* Analysis Text */}
                            <GlassCard className="p-6 relative overflow-hidden">
                                <div className="absolute top-0 right-0 p-4 opacity-10">
                                    <Brain className="w-24 h-24 text-indigo-400" />
                                </div>
                                <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
                                    <Brain className="w-5 h-5 text-indigo-400" />
                                    Análisis Inteligente Exclusivo
                                </h3>
                                <ul className="space-y-4 text-sm text-slate-300">
                                    <li className="flex gap-3">
                                        <CheckCircle2 className="w-5 h-5 text-emerald-400 flex-shrink-0" />
                                        <span>
                                            Tu mejor mes fue <strong className="text-white">{bestMonth?.mes || 'N/A'}</strong> con un flujo neto de
                                            <span className="text-emerald-400 ml-1">
                                                ${bestMonth?.flujoNeto?.toLocaleString('es-CO') || '0'}
                                            </span>.
                                        </span>
                                    </li>
                                    <li className="flex gap-3">
                                        <TrendingUp className="w-5 h-5 text-indigo-400 flex-shrink-0" />
                                        <span>
                                            El margen operativo promedio del periodo analizado es del <strong className="text-white">{margenpromedio}%</strong>.
                                        </span>
                                    </li>
                                    <li className="flex gap-3">
                                        {riskCount > 0 ? (
                                            <AlertCircle className="w-5 h-5 text-amber-400 flex-shrink-0" />
                                        ) : (
                                            <CheckCircle2 className="w-5 h-5 text-emerald-400 flex-shrink-0" />
                                        )}
                                        <span>
                                            {riskCount > 0
                                                ? `Se detectaron ${riskCount} periodos con flujo de caja negativo. Requiere atención.`
                                                : "No se detectaron periodos con flujo de caja negativo. Gestión saludable."
                                            }
                                        </span>
                                    </li>
                                </ul>
                            </GlassCard>

                            {/* Data Table */}
                            <GlassCard className="p-0 overflow-hidden">
                                <div className="p-4 bg-white/5 border-b border-white/5">
                                    <h3 className="font-bold text-white">Detalle Mensual</h3>
                                </div>
                                <div className="max-h-[300px] overflow-y-auto">
                                    <table className="w-full text-sm text-left">
                                        <thead className="text-xs text-slate-400 uppercase bg-black/20 sticky top-0">
                                            <tr>
                                                <th className="px-4 py-3">Mes</th>
                                                <th className="px-4 py-3 text-right">Ingresos</th>
                                                <th className="px-4 py-3 text-right">Egresos</th>
                                                <th className="px-4 py-3 text-right">Neto</th>
                                            </tr>
                                        </thead>
                                        <tbody className="divide-y divide-white/5">
                                            {data.map((row, i) => (
                                                <tr key={i} className="hover:bg-white/5 transition-colors">
                                                    <td className="px-4 py-3 text-white font-medium">{row.mes}</td>
                                                    <td className="px-4 py-3 text-right text-emerald-400">${row.ingresos?.toLocaleString()}</td>
                                                    <td className="px-4 py-3 text-right text-rose-400">${row.egresos?.toLocaleString()}</td>
                                                    <td className={`px-4 py-3 text-right font-bold ${row.flujoNeto >= 0 ? 'text-indigo-400' : 'text-amber-400'}`}>
                                                        ${row.flujoNeto?.toLocaleString()}
                                                    </td>
                                                </tr>
                                            ))}
                                        </tbody>
                                    </table>
                                </div>
                            </GlassCard>
                        </div>

                        <div className="flex justify-end p-4">
                            <button
                                onClick={() => { setViewState('upload'); setData([]); }}
                                className="px-4 py-2 text-slate-400 hover:text-white transition-colors text-sm flex items-center gap-2 hover:bg-white/5 rounded-lg"
                            >
                                <UploadCloud className="w-4 h-4" />
                                Cargar otro archivo
                            </button>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
}
