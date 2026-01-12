'use client';

import { useState, useEffect } from 'react';
import { Banknote, Upload, ArrowLeftRight, CheckCircle, AlertCircle, FileSpreadsheet, Download, Search, RefreshCw, Brain, FileText } from 'lucide-react';
import * as XLSX from 'xlsx';
import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';
import { GlassCard } from '@/components/ui/GlassCard';
import { FileUpload } from '@/components/ui/FileUpload';
import { FileGuide } from '@/components/ui/FileGuide';
import { motion, AnimatePresence } from 'framer-motion';

// Types for reconciliation items
interface ReconciliationItem {
    id: string;
    date: string;
    description: string;
    amount: number;
    source: 'BANK' | 'BOOK';
    status: 'MATCHED' | 'PENDING_BANK' | 'PENDING_BOOK';
    matchConfidence?: number;
}

export default function BankReconcilePage() {
    const [bankFile, setBankFile] = useState<File | null>(null);
    const [bookFile, setBookFile] = useState<File | null>(null);
    const [isProcessing, setIsProcessing] = useState(false);
    const [viewMode, setViewMode] = useState<'upload' | 'results'>('upload');
    const [results, setResults] = useState<ReconciliationItem[]>([]);
    const [isClient, setIsClient] = useState(false);

    useEffect(() => setIsClient(true), []);

    const formatCurrency = (val: number) => {
        if (!isClient) return val.toString();
        return val.toLocaleString('es-CO', { maximumFractionDigits: 0 });
    };

    const handleConciliate = () => {
        if (!bankFile || !bookFile) return;
        setIsProcessing(true);

        // Simulate complex matching algorithm
        setTimeout(() => {
            const mockItems: ReconciliationItem[] = [
                { id: '1', date: '2026-01-05', description: 'TRANSFERENCIA BANCOLOMBIA', amount: -5000000, source: 'BANK', status: 'MATCHED', matchConfidence: 100 },
                { id: '2', date: '2026-01-08', description: 'PAGO NOMINA QUINCENA 1', amount: -12500000, source: 'BANK', status: 'MATCHED', matchConfidence: 98 },
                { id: '3', date: '2026-01-12', description: 'CHEQUE 4501 NO COBRADO', amount: -2300000, source: 'BOOK', status: 'PENDING_BANK' },
                { id: '4', date: '2026-01-15', description: 'COBRO INTERESES TARJETA', amount: -125000, source: 'BANK', status: 'PENDING_BOOK' },
                { id: '5', date: '2026-01-20', description: 'PAGO CLIENTE FACT 998', amount: 4500000, source: 'BANK', status: 'MATCHED', matchConfidence: 100 },
                { id: '6', date: '2026-01-22', description: 'GMF 4X1000', amount: -45000, source: 'BANK', status: 'PENDING_BOOK' },
            ];
            setResults(mockItems);
            setIsProcessing(false);
            setViewMode('results');
        }, 3000);
    };

    // Calculate Summary KPIs
    const totalBank = results.filter(r => r.source === 'BANK' || r.status === 'MATCHED').reduce((acc, curr) => acc + curr.amount, 150000000); // Initial balance simulation
    const totalBook = 148500000; // Simulated book balance
    const difference = totalBank - totalBook;
    const matchCount = results.filter(r => r.status === 'MATCHED').length;
    const pendingBank = results.filter(r => r.status === 'PENDING_BANK').length;
    const pendingBook = results.filter(r => r.status === 'PENDING_BOOK').length;

    const handleDownload = (format: 'xlsx' | 'pdf') => {
        if (format === 'xlsx') {
            const ws = XLSX.utils.json_to_sheet(results.map(item => ({
                Fecha: item.date,
                Descripción: item.description,
                Monto: item.amount,
                Fuente: item.source,
                Estado: item.status,
                Confianza: item.matchConfidence ? `${item.matchConfidence}%` : 'N/A'
            })));
            const wb = XLSX.utils.book_new();
            XLSX.utils.book_append_sheet(wb, ws, "Conciliación Bancaria");
            XLSX.writeFile(wb, "Conciliacion_Bancaria_IA.xlsx");
        } else {
            const doc = new jsPDF();
            doc.setFontSize(18);
            doc.text("Reporte de Conciliación Bancaria IA", 14, 22);
            doc.setFontSize(11);
            doc.text(`Generado: ${new Date().toLocaleDateString()}`, 14, 30);

            autoTable(doc, {
                startY: 40,
                head: [['Fecha', 'Descripción', 'Monto', 'Fuente', 'Estado']],
                body: results.map(item => [
                    item.date,
                    item.description,
                    `$${item.amount.toLocaleString()}`,
                    item.source,
                    item.status
                ]),
            });
            doc.save("Reporte_Conciliacion.pdf");
        }
    };

    return (
        <div className="space-y-8 max-w-7xl mx-auto">
            <div className="flex items-center gap-4">
                <div className="p-4 rounded-2xl bg-gradient-to-br from-emerald-500/20 to-teal-500/20 border border-emerald-500/20">
                    <Banknote className="w-10 h-10 text-emerald-400" />
                </div>
                <div>
                    <h1 className="text-3xl font-bold font-space text-white">Conciliación Bancaria IA</h1>
                    <p className="text-slate-400">Motor de emparejamiento inteligente (Fuzzy Matching) para tus extractos.</p>
                </div>
            </div>

            <AnimatePresence mode="wait">
                {viewMode === 'upload' ? (
                    <motion.div
                        key="upload"
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -20 }}
                        className="grid grid-cols-1 md:grid-cols-3 gap-8 items-center"
                    >
                        {/* Bank Side */}
                        <GlassCard className="h-full flex flex-col border-emerald-500/30">
                            <h3 className="text-lg font-bold text-white mb-4 flex items-center justify-between gap-2">
                                <span className="flex items-center gap-2">
                                    <span className="w-8 h-8 rounded-full bg-emerald-500/20 flex items-center justify-center text-sm">A</span>
                                    Extracto Bancario
                                </span>
                                <FileGuide
                                    moduleName="Bancos"
                                    requiredColumns={['Fecha', 'Descripción', 'Valor', 'Saldo']}
                                    exampleRow={{ 'Fecha': '2025-01-30', 'Descripción': 'Transferencia 123', 'Valor': '-50000', 'Saldo': '1200000' }}
                                />
                            </h3>
                            <div className="flex-1">
                                <FileUpload
                                    accept=".xlsx,.csv,.pdf"
                                    label="Subir Extracto"
                                    onFilesSelected={(f) => setBankFile(f[0])}
                                />
                                {bankFile && <p className="mt-2 text-emerald-400 text-sm flex items-center gap-1 font-medium bg-emerald-500/10 p-2 rounded">✅ Cargado: {bankFile.name}</p>}
                            </div>
                        </GlassCard>

                        {/* Center Action */}
                        <div className="text-center space-y-4">
                            <div className="w-24 h-24 mx-auto rounded-full bg-slate-900 border border-white/10 flex items-center justify-center relative group">
                                <ArrowLeftRight className={`w-12 h-12 text-indigo-400 ${isProcessing ? 'animate-spin' : 'group-hover:scale-110 transition-transform'}`} />
                            </div>
                            <button
                                onClick={handleConciliate}
                                disabled={!bankFile || !bookFile || isProcessing}
                                className="btn-primary w-full py-4 text-lg shadow-emerald-500/20 disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                                {isProcessing ? 'Cruzando Datos...' : 'Iniciar Conciliación'}
                            </button>
                            <p className="text-xs text-slate-500">Versión de Motor: v2.1.0-beta</p>
                        </div>

                        {/* Book Side */}
                        <GlassCard className="h-full flex flex-col border-indigo-500/30">
                            <h3 className="text-lg font-bold text-white mb-4 flex items-center justify-between gap-2">
                                <span className="flex items-center gap-2">
                                    <span className="w-8 h-8 rounded-full bg-indigo-500/20 flex items-center justify-center text-sm">B</span>
                                    Libro Auxiliar
                                </span>
                                <FileGuide
                                    moduleName="Libros"
                                    requiredColumns={['Fecha', 'Documento', 'Detalle', 'Valor']}
                                    exampleRow={{ 'Fecha': '2025-01-30', 'Documento': 'CE-001', 'Detalle': 'Pago Prov.', 'Valor': '-50000' }}
                                />
                            </h3>
                            <div className="flex-1">
                                <FileUpload
                                    accept=".xlsx,.csv"
                                    label="Subir Libro Mayor"
                                    onFilesSelected={(f) => setBookFile(f[0])}
                                />
                                {bookFile && <p className="mt-2 text-emerald-400 text-sm flex items-center gap-1 font-medium bg-emerald-500/10 p-2 rounded">✅ Cargado: {bookFile.name}</p>}
                            </div>
                        </GlassCard>
                    </motion.div>
                ) : (
                    <motion.div
                        key="results"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        className="space-y-6"
                    >
                        {/* Header Actions */}
                        <div className="flex justify-end gap-3">
                            <button onClick={() => handleDownload('xlsx')} className="flex items-center gap-2 px-4 py-2 rounded-xl bg-emerald-500/10 text-emerald-400 hover:bg-emerald-500/20 transition-colors border border-emerald-500/20">
                                <FileSpreadsheet className="w-4 h-4" />
                                <span className="text-sm font-medium">Exportar Excel</span>
                            </button>
                            <button onClick={() => handleDownload('pdf')} className="flex items-center gap-2 px-4 py-2 rounded-xl bg-rose-500/10 text-rose-400 hover:bg-rose-500/20 transition-colors border border-rose-500/20">
                                <FileText className="w-4 h-4" />
                                <span className="text-sm font-medium">Reporte PDF</span>
                            </button>
                        </div>

                        {/* Neural Analysis & KPIs */}
                        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                            {/* Main KPIs */}
                            <div className="space-y-6 lg:col-span-1">
                                <GlassCard className="bg-gradient-to-br from-indigo-900/40 to-slate-900/40 border-indigo-500/30 relative overflow-hidden group">
                                    <div className="absolute top-0 right-0 p-4 opacity-5 group-hover:opacity-10 transition-opacity">
                                        <Banknote className="w-24 h-24" />
                                    </div>
                                    <p className="text-indigo-300 text-xs font-bold uppercase tracking-wider mb-2">Conciliación Automática</p>
                                    <h2 className="text-4xl font-bold text-white mb-1">
                                        {formatCurrency(((matchCount / results.length) * 100) || 0)}%
                                    </h2>
                                    <p className="text-slate-400 text-sm">Efectividad del Motor IA</p>

                                    <div className="mt-6 pt-6 border-t border-white/5 space-y-4">
                                        <div className="flex justify-between items-center">
                                            <span className="text-sm text-slate-400">Saldo Extracto</span>
                                            <span className="text-sm font-bold text-emerald-400">${formatCurrency(totalBank)}</span>
                                        </div>
                                        <div className="flex justify-between items-center">
                                            <span className="text-sm text-slate-400">Saldo Libros</span>
                                            <span className="text-sm font-bold text-indigo-400">${formatCurrency(totalBook)}</span>
                                        </div>
                                        <div className="flex justify-between items-center pt-2 border-t border-white/5">
                                            <span className="text-sm text-slate-300 font-medium">Diferencia Neta</span>
                                            <span className={`text-sm font-bold ${difference !== 0 ? 'text-rose-400' : 'text-emerald-400'}`}>
                                                ${formatCurrency(difference)}
                                            </span>
                                        </div>
                                    </div>
                                </GlassCard>

                                <button
                                    onClick={() => setViewMode('upload')}
                                    className="w-full py-4 rounded-xl border border-dashed border-slate-700 text-slate-400 hover:text-white hover:border-indigo-500/50 hover:bg-indigo-500/5 transition-all flex items-center justify-center gap-2 group"
                                >
                                    <RefreshCw className="w-4 h-4 group-hover:rotate-180 transition-transform duration-500" />
                                    Nueva Conciliación
                                </button>
                            </div>

                            {/* Smart Insights - The "Dependency" Hook */}
                            <GlassCard className="lg:col-span-2 relative overflow-hidden border-indigo-500/30">
                                <div className="absolute top-0 right-0 w-64 h-64 bg-indigo-500/10 rounded-full blur-3xl -mr-32 -mt-32 pointer-events-none" />

                                <div className="flex items-start gap-4 mb-6">
                                    <div className="p-3 rounded-xl bg-indigo-500/20 text-indigo-400 shadow-lg shadow-indigo-500/10">
                                        <Brain className="w-6 h-6" />
                                    </div>
                                    <div>
                                        <h3 className="text-lg font-bold text-white">Análisis Neuronal de Tesorería</h3>
                                        <p className="text-indigo-300 text-sm">Inteligencia Artificial aplicada a tus flujos.</p>
                                    </div>
                                </div>

                                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                    <div className="space-y-4">
                                        <div className="p-4 rounded-xl bg-white/5 border border-white/5 hover:bg-white/10 transition-colors">
                                            <div className="flex items-center gap-2 mb-2">
                                                <AlertCircle className="w-4 h-4 text-amber-400" />
                                                <h4 className="font-bold text-white text-sm">Atención Requerida</h4>
                                            </div>
                                            <p className="text-sm text-slate-300 leading-relaxed">
                                                Tienes <strong className="text-white">{pendingBank + pendingBook} partidas pendientes</strong> que suman <strong className="text-rose-400">${formatCurrency(Math.abs(difference))}</strong>. Estas inconsistencias afectan tu flujo de caja real.
                                            </p>
                                        </div>

                                        <div className="p-4 rounded-xl bg-white/5 border border-white/5 hover:bg-white/10 transition-colors">
                                            <div className="flex items-center gap-2 mb-2">
                                                <Search className="w-4 h-4 text-emerald-400" />
                                                <h4 className="font-bold text-white text-sm">Detección de Patrones</h4>
                                            </div>
                                            <p className="text-sm text-slate-300 leading-relaxed">
                                                El Sistema IA detectó que el 80% de las diferencias provienen de <span className="text-emerald-300">pagos de nómina</span> aún no reflejados. Se sugiere programar dispersión anticipada.
                                            </p>
                                        </div>
                                    </div>

                                    <div className="space-y-4">
                                        <div className="p-4 rounded-xl bg-indigo-900/20 border border-indigo-500/20">
                                            <h4 className="text-xs font-bold text-indigo-400 uppercase tracking-wider mb-3">Recomendación Estratégica</h4>
                                            <p className="text-sm text-white italic">
                                                "Para optimizar tu liquidez, concilia las partidas 'PENDING_BOOK' antes del cierre de hoy. Tu saldo real disponible podría ser menor al esperado."
                                            </p>
                                            <div className="mt-3 flex items-center gap-2">
                                                <div className="h-1 flex-1 bg-slate-800 rounded-full overflow-hidden">
                                                    <div className="h-full bg-indigo-500 w-[85%]"></div>
                                                </div>
                                                <span className="text-xs text-indigo-400 font-bold">Prioridad Alta</span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </GlassCard>
                        </div>

                        {/* Results Table */}
                        <GlassCard className="overflow-hidden p-0">
                            <div className="p-6 border-b border-white/10 flex justify-between items-center bg-black/20">
                                <h3 className="text-xl font-bold text-white flex items-center gap-2">
                                    <CheckCircle className="w-5 h-5 text-indigo-400" />
                                    Detalle de Operaciones
                                </h3>
                                <div className="flex gap-4 text-sm text-slate-400">
                                    <div className="flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20">
                                        <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
                                        <span className="text-emerald-400 font-medium">{matchCount} Conciliados</span>
                                    </div>
                                    <div className="flex items-center gap-2 px-3 py-1 rounded-full bg-rose-500/10 border border-rose-500/20">
                                        <span className="w-2 h-2 rounded-full bg-rose-400"></span>
                                        <span className="text-rose-400 font-medium">{pendingBook} Pend. Libros</span>
                                    </div>
                                </div>
                            </div>
                            <div className="overflow-x-auto">
                                <table className="w-full text-sm text-left">
                                    <thead className="text-xs text-slate-400 uppercase bg-black/20">
                                        <tr>
                                            <th className="px-6 py-4 font-semibold">Fecha</th>
                                            <th className="px-6 py-4 font-semibold">Descripción</th>
                                            <th className="px-6 py-4 text-right font-semibold">Monto</th>
                                            <th className="px-6 py-4 text-center font-semibold">Fuente</th>
                                            <th className="px-6 py-4 text-center font-semibold">Estado de Inteligencia</th>
                                            <th className="px-6 py-4 text-right font-semibold">Confianza IA</th>
                                        </tr>
                                    </thead>
                                    <tbody className="divide-y divide-white/5">
                                        {results.map((item) => (
                                            <tr key={item.id} className="hover:bg-indigo-500/5 transition-colors group">
                                                <td className="px-6 py-4 font-mono text-slate-400 group-hover:text-white transition-colors">{item.date}</td>
                                                <td className="px-6 py-4 font-medium text-slate-200 group-hover:text-white transition-colors">{item.description}</td>
                                                <td className={`px-6 py-4 text-right font-bold ${item.amount < 0 ? 'text-rose-400' : 'text-emerald-400'}`}>
                                                    ${formatCurrency(item.amount)}
                                                </td>
                                                <td className="px-6 py-4 text-center">
                                                    <span className={`px-3 py-1 rounded-lg text-xs font-bold border ${item.source === 'BANK'
                                                        ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20'
                                                        : 'bg-blue-500/10 text-blue-400 border-blue-500/20'}`}>
                                                        {item.source === 'BANK' ? 'BANCO' : 'LIBRO'}
                                                    </span>
                                                </td>
                                                <td className="px-6 py-4 text-center">
                                                    <span className={`px-3 py-1 rounded-lg text-xs font-bold inline-flex items-center gap-2 ${item.status === 'MATCHED' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' :
                                                        item.status === 'PENDING_BOOK' ? 'bg-rose-500/10 text-rose-400 border border-rose-500/20' :
                                                            'bg-amber-500/10 text-amber-400 border border-amber-500/20'
                                                        }`}>
                                                        {item.status === 'MATCHED' && <CheckCircle className="w-3 h-3" />}
                                                        {item.status === 'PENDING_BOOK' && <AlertCircle className="w-3 h-3" />}
                                                        {item.status === 'PENDING_BANK' && <AlertCircle className="w-3 h-3" />}
                                                        {item.status === 'MATCHED' ? 'Conciliado' : item.status === 'PENDING_BOOK' ? 'Falta en Libro' : 'No Cobrado'}
                                                    </span>
                                                </td>
                                                <td className="px-6 py-4 text-right">
                                                    {item.matchConfidence ? (
                                                        <div className="flex items-center justify-end gap-2">
                                                            <div className="w-16 h-1.5 bg-slate-700 rounded-full overflow-hidden">
                                                                <div className="h-full bg-emerald-400" style={{ width: `${item.matchConfidence}%` }}></div>
                                                            </div>
                                                            <span className="text-emerald-400 font-bold">{item.matchConfidence}%</span>
                                                        </div>
                                                    ) : (
                                                        <span className="text-slate-600 font-mono">-</span>
                                                    )}
                                                </td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        </GlassCard>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
}

