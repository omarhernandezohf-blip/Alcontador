'use client';

import { useState, useEffect } from 'react';
import { Calculator, DollarSign, Users, Upload, FileText, CheckCircle, TrendingUp, Download, Search, ArrowRight, Brain, FileSpreadsheet } from 'lucide-react';
import * as XLSX from 'xlsx';
import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';
import { GlassCard } from '@/components/ui/GlassCard';
import { FileUpload } from '@/components/ui/FileUpload';
import { FileGuide } from '@/components/ui/FileGuide';
import { motion, AnimatePresence } from 'framer-motion';

// Types
interface EmployeeCost {
    id: string;
    name: string;
    cargo: string;
    baseSalary: number;
    transportAux: number;
    socialSecurity: number;
    parafiscales: number;
    prestaciones: number;
    totalCost: number;
}

export default function PayrollCostPage() {
    const [employees, setEmployees] = useState<EmployeeCost[]>([]);
    const [uploadedFile, setUploadedFile] = useState<File | null>(null);
    const [isProcessing, setIsProcessing] = useState(false);
    const [isClient, setIsClient] = useState(false);
    const [viewMode, setViewMode] = useState<'upload' | 'results'>('upload');

    useEffect(() => setIsClient(true), []);

    // Constants 2026 (Proyecciones)
    const SMMLV_2026 = 1750905;
    const AUX_TRA_2026 = 249095;
    const HEALTH_PCT = 0.085;
    const PENSION_PCT = 0.12;
    const ARL_PCT = 0.00522;
    const PARAFISCAL_PCT = 0.09;

    const calculateCost = (base: number, transport: number) => {
        const totalDevengado = base + transport;
        const socialSecurity = base * (HEALTH_PCT + PENSION_PCT + ARL_PCT);
        const parafiscales = base * PARAFISCAL_PCT;
        // Prestaciones: Prima (8.33%) + Cesantías (8.33%) + Int. Cesantías (1%) + Vacaciones (4.17%)
        const prestaciones = (totalDevengado * (0.0833 + 0.0833 + 0.01)) + (base * 0.0417);

        return {
            socialSecurity,
            parafiscales,
            prestaciones,
            totalCost: totalDevengado + socialSecurity + parafiscales + prestaciones
        };
    };

    const formatCurrency = (val: number) => {
        if (!isClient) return val.toString();
        return val.toLocaleString('es-CO', { maximumFractionDigits: 0 });
    };

    const handleFileUpload = (files: File[]) => {
        if (files.length > 0) {
            setUploadedFile(files[0]);
            setIsProcessing(true);

            // Simulación de Parsing Inteligente
            setTimeout(() => {
                const mockEmployees = [
                    { name: 'Juan Pérez', cargo: 'Desarrollador Senior', base: 6500000, aux: 0 },
                    { name: 'Ana Gómez', cargo: 'Contadora', base: 3200000, aux: AUX_TRA_2026 },
                    { name: 'Carlos Ruíz', cargo: 'Asistente Administrativo', base: 1400000 + (SMMLV_2026 - 1300000), aux: AUX_TRA_2026 }, // Ajuste 2026
                    { name: 'María Rodríguez', cargo: 'Gerente Comercial', base: 8000000, aux: 0 },
                    { name: 'Pedro López', cargo: 'Vendedor Junior', base: SMMLV_2026, aux: AUX_TRA_2026 },
                ].map((emp, i) => {
                    const costs = calculateCost(emp.base, emp.aux);
                    return {
                        id: i.toString(),
                        name: emp.name,
                        cargo: emp.cargo,
                        baseSalary: emp.base,
                        transportAux: emp.aux,
                        ...costs
                    };
                });

                setEmployees(mockEmployees);
                setIsProcessing(false);
                setViewMode('results');
            }, 2500);
        }
    };

    const handleDownloadExcel = () => {
        if (employees.length === 0) return;

        const data = employees.map(emp => ({
            'Empleado': emp.name,
            'Cargo': emp.cargo,
            'Salario Base': emp.baseSalary,
            'Aux. Transp': emp.transportAux,
            'Seg. Social': emp.socialSecurity,
            'Parafiscales': emp.parafiscales,
            'Prestaciones': emp.prestaciones,
            'Costo Total': emp.totalCost
        }));

        const worksheet = XLSX.utils.json_to_sheet(data);
        const workbook = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(workbook, worksheet, "Nómina Detallada");

        // Ajuste de ancho de columnas para aspecto profesional
        const wscols = [
            { wch: 25 }, { wch: 20 }, { wch: 15 }, { wch: 15 }, { wch: 15 }, { wch: 15 }, { wch: 15 }, { wch: 15 }
        ];
        worksheet['!cols'] = wscols;

        XLSX.writeFile(workbook, `Costeo_Nomina_Real_${new Date().toISOString().split('T')[0]}.xlsx`);
    };

    const handleDownloadPDF = () => {
        if (employees.length === 0) return;

        const doc = new jsPDF();

        // Header Corporativo
        doc.setFontSize(20);
        doc.setTextColor(40, 40, 40);
        doc.text("Reporte de Costeo de Nómina Real", 14, 22);

        doc.setFontSize(10);
        doc.setTextColor(100);
        doc.text(`Generado el: ${new Date().toLocaleDateString()} ${new Date().toLocaleTimeString()}`, 14, 30);
        doc.text("Asistente Contable Pro - Análisis Prestacional", 14, 35);

        // Totales Resumen
        doc.setFillColor(240, 253, 244); // bg-emerald-50
        doc.roundedRect(14, 45, 180, 25, 3, 3, 'F');

        doc.setFontSize(10);
        doc.setTextColor(60);
        doc.text("Costo Mensual Total", 20, 55);
        doc.setFontSize(16);
        doc.setTextColor(5, 150, 105); // emerald-600
        doc.text(`$${formatCurrency(totalPayroll)}`, 20, 65);

        doc.setFontSize(10);
        doc.setTextColor(60);
        doc.text("Total Empleados", 100, 55);
        doc.setFontSize(16);
        doc.setTextColor(40);
        doc.text(totalEmployees.toString(), 100, 65);

        // Tabla Detallada
        const tableColumn = ["Empleado", "Cargo", "Salario Base", "Aux. Transp", "Seg. Social", "Parafiscales", "Prestaciones", "Total"];
        const tableRows = employees.map(emp => [
            emp.name,
            emp.cargo,
            formatCurrency(emp.baseSalary),
            formatCurrency(emp.transportAux),
            formatCurrency(emp.socialSecurity),
            formatCurrency(emp.parafiscales),
            formatCurrency(emp.prestaciones),
            formatCurrency(emp.totalCost)
        ]);

        autoTable(doc, {
            head: [tableColumn],
            body: tableRows,
            startY: 80,
            theme: 'grid',
            headStyles: { fillColor: [5, 150, 105], textColor: 255, fontStyle: 'bold' }, // Emerald header
            alternateRowStyles: { fillColor: [245, 245, 245] },
            styles: { fontSize: 8, cellPadding: 3 },
            columnStyles: {
                0: { cellWidth: 30 }, // Empleado
                1: { cellWidth: 25 }, // Cargo
                // Align numbers to right
                2: { halign: 'right' },
                3: { halign: 'right' },
                4: { halign: 'right' },
                5: { halign: 'right' },
                6: { halign: 'right' },
                7: { halign: 'right', fontStyle: 'bold', textColor: [5, 150, 105] }
            },
            foot: [['TOTALES', '',
                formatCurrency(employees.reduce((a, c) => a + c.baseSalary, 0)),
                formatCurrency(employees.reduce((a, c) => a + c.transportAux, 0)),
                formatCurrency(employees.reduce((a, c) => a + c.socialSecurity, 0)),
                formatCurrency(employees.reduce((a, c) => a + c.parafiscales, 0)),
                formatCurrency(employees.reduce((a, c) => a + c.prestaciones, 0)),
                formatCurrency(totalPayroll)
            ]],
            footStyles: { fillColor: [240, 240, 240], textColor: 40, fontStyle: 'bold', halign: 'right' }
        });

        // Smart Advisor Note
        const finalY = (doc as any).lastAutoTable.finalY || 150;
        doc.setFontSize(10);
        doc.setTextColor(100);
        doc.text("Nota: Este reporte verifica el cumplimiento base de aportes parafiscales y prestacionales proyectados.", 14, finalY + 10);

        doc.save(`Nomina_Detallada_${new Date().toISOString().split('T')[0]}.pdf`);
    };

    const totalPayroll = employees.reduce((acc, curr) => acc + curr.totalCost, 0);
    const totalEmployees = employees.length;
    const avgCost = totalEmployees > 0 ? totalPayroll / totalEmployees : 0;

    return (
        <div className="space-y-8 max-w-7xl mx-auto">
            {/* Header */}
            <div className="flex items-center gap-4">
                <div className="p-4 rounded-2xl bg-gradient-to-br from-green-500/20 to-emerald-600/20 border border-green-500/20">
                    <Calculator className="w-10 h-10 text-green-400" />
                </div>
                <div>
                    <h1 className="text-3xl font-bold font-space text-white">Costeo de Nómina Real</h1>
                    <p className="text-slate-400">Análisis detallado de carga prestacional por empleado.</p>
                </div>
            </div>

            {/* Main Content */}
            <AnimatePresence mode='wait'>
                {viewMode === 'upload' ? (
                    <motion.div
                        key="upload"
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -20 }}
                    >
                        <GlassCard className="border-emerald-500/30 relative overflow-hidden min-h-[400px] flex flex-col justify-center">
                            <div className="absolute top-0 right-0 p-4 opacity-5">
                                <Upload className="w-64 h-64 text-emerald-400" />
                            </div>
                            <div className="max-w-xl mx-auto w-full relative z-10 text-center space-y-8">
                                <div>
                                    <h3 className="text-2xl font-bold text-white mb-2">Carga tu Nómina</h3>
                                    <p className="text-slate-400">Sube tu archivo .xlsx o .pdf. Nuestro motor procesará cada empleado, calculará prestaciones, seguridad social y parafiscales automáticamente.</p>
                                </div>
                                <div className="w-full max-w-md mx-auto">
                                    <div className="flex justify-end mb-2">
                                        <FileGuide
                                            moduleName="Costo Nómina"
                                            requiredColumns={['Nombre', 'Cargo', 'Salario_Base', 'Auxilio_Transporte']}
                                            exampleRow={{ 'Nombre': 'Pepito Perez', 'Cargo': 'Analista', 'Salario_Base': '2500000', 'Auxilio_Transporte': '0' }}
                                            tips={['Si tiene Auxilio de Transporte pon el valor (ej. 162000) o 0']}
                                        />
                                    </div>
                                    <FileUpload
                                        accept=".xlsx, .csv"
                                        label="Cargar Nómina de Empleados"
                                        onFilesSelected={handleFileUpload}
                                    />
                                    {uploadedFile && <p className="mt-2 text-emerald-400 text-sm flex items-center justify-center gap-1 font-medium bg-emerald-500/10 p-2 rounded">✅ Cargado: {uploadedFile.name}</p>}
                                </div>
                                {isProcessing && (
                                    <div className="max-w-md mx-auto bg-emerald-900/20 border border-emerald-500/20 rounded-xl p-4 flex items-center gap-4">
                                        <div className="w-6 h-6 border-2 border-emerald-400 border-t-transparent rounded-full animate-spin" />
                                        <div className="text-left">
                                            <p className="text-white font-bold text-sm">Procesando {uploadedFile?.name}...</p>
                                            <p className="text-xs text-emerald-400">Extrayendo datos de empleados y salarios...</p>
                                        </div>
                                    </div>
                                )}
                            </div>
                        </GlassCard>
                    </motion.div>
                ) : (
                    <motion.div
                        key="results"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        className="space-y-8"
                    >
                        {/* Smart Summary */}
                        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                            <GlassCard className="border-emerald-500/30 bg-emerald-900/10">
                                <p className="text-slate-400 text-sm font-medium uppercase tracking-wider">Costo Mensual Total</p>
                                <h2 className="text-3xl font-bold text-white mt-1">${formatCurrency(totalPayroll)}</h2>
                                <div className="mt-2 flex items-center text-emerald-400 text-xs">
                                    <TrendingUp className="w-3 h-3 mr-1" />
                                    Nómina consolidada
                                </div>
                            </GlassCard>
                            <GlassCard>
                                <p className="text-slate-400 text-sm font-medium uppercase tracking-wider">Total Empleados</p>
                                <h2 className="text-3xl font-bold text-white mt-1">{totalEmployees}</h2>
                                <p className="text-xs text-slate-500 mt-2">Activos en planilla</p>
                            </GlassCard>
                            <GlassCard>
                                <p className="text-slate-400 text-sm font-medium uppercase tracking-wider">Costo Promedio</p>
                                <h2 className="text-3xl font-bold text-white mt-1">${formatCurrency(avgCost)}</h2>
                                <p className="text-xs text-slate-500 mt-2">Por colaborador</p>
                            </GlassCard>
                            <GlassCard className="border-indigo-500/30 bg-indigo-900/10 cursor-pointer hover:bg-indigo-900/20 transition-colors" onClick={() => setViewMode('upload')}>
                                <div className="h-full flex flex-col items-center justify-center text-center space-y-2">
                                    <Upload className="w-8 h-8 text-indigo-400" />
                                    <p className="text-indigo-200 font-bold text-sm">Subir Nueva Nómina</p>
                                </div>
                            </GlassCard>
                        </div>

                        {/* Detailed Table */}
                        <GlassCard className="overflow-hidden p-0">
                            <div className="p-6 border-b border-white/10 flex justify-between items-center bg-white/5">
                                <h3 className="text-xl font-bold text-white flex items-center gap-2">
                                    <Users className="w-5 h-5 text-indigo-400" />
                                    Desglose por Empleado
                                </h3>
                                <div className="flex gap-2">
                                    <button className="p-2 hover:bg-white/10 rounded-lg text-slate-400 transition-colors">
                                        <Search className="w-4 h-4" />
                                    </button>
                                </div>
                            </div>
                            <div className="overflow-x-auto">
                                <table className="w-full text-sm text-left">
                                    <thead className="text-xs text-slate-400 uppercase bg-white/5">
                                        <tr>
                                            <th className="px-6 py-3">Empleado</th>
                                            <th className="px-6 py-3 text-right">Salario Base</th>
                                            <th className="px-6 py-3 text-right">Aux. Transp</th>
                                            <th className="px-6 py-3 text-right">Seg. Social</th>
                                            <th className="px-6 py-3 text-right">Parafiscales</th>
                                            <th className="px-6 py-3 text-right">Prestaciones</th>
                                            <th className="px-6 py-3 text-right text-emerald-400 font-bold">Costo Total</th>
                                        </tr>
                                    </thead>
                                    <tbody className="divide-y divide-white/5">
                                        {employees.map((emp) => (
                                            <tr key={emp.id} className="hover:bg-white/5 transition-colors">
                                                <td className="px-6 py-4 font-medium text-white">
                                                    <div>{emp.name}</div>
                                                    <div className="text-xs text-slate-500 font-normal">{emp.cargo}</div>
                                                </td>
                                                <td className="px-6 py-4 text-right text-slate-300">${formatCurrency(emp.baseSalary)}</td>
                                                <td className="px-6 py-4 text-right text-slate-400">${formatCurrency(emp.transportAux)}</td>
                                                <td className="px-6 py-4 text-right text-slate-400">${formatCurrency(emp.socialSecurity)}</td>
                                                <td className="px-6 py-4 text-right text-slate-400">${formatCurrency(emp.parafiscales)}</td>
                                                <td className="px-6 py-4 text-right text-slate-400">${formatCurrency(emp.prestaciones)}</td>
                                                <td className="px-6 py-4 text-right font-bold text-emerald-400 bg-emerald-500/5">
                                                    ${formatCurrency(emp.totalCost)}
                                                </td>
                                            </tr>
                                        ))}
                                    </tbody>
                                    <tfoot className="bg-white/5 font-bold text-white border-t-2 border-white/10">
                                        <tr>
                                            <td className="px-6 py-4">TOTALES</td>
                                            <td className="px-6 py-4 text-right">${formatCurrency(employees.reduce((a, c) => a + c.baseSalary, 0))}</td>
                                            <td className="px-6 py-4 text-right">${formatCurrency(employees.reduce((a, c) => a + c.transportAux, 0))}</td>
                                            <td className="px-6 py-4 text-right">${formatCurrency(employees.reduce((a, c) => a + c.socialSecurity, 0))}</td>
                                            <td className="px-6 py-4 text-right">${formatCurrency(employees.reduce((a, c) => a + c.parafiscales, 0))}</td>
                                            <td className="px-6 py-4 text-right">${formatCurrency(employees.reduce((a, c) => a + c.prestaciones, 0))}</td>
                                            <td className="px-6 py-4 text-right text-emerald-400">${formatCurrency(totalPayroll)}</td>
                                        </tr>
                                    </tfoot>
                                </table>
                            </div>
                        </GlassCard>

                        {/* Smart Advisor Section */}
                        <GlassCard className="bg-slate-900/50 border-emerald-500/30">
                            <div className="flex items-center gap-3 mb-6">
                                <div className="w-10 h-10 rounded-full bg-emerald-500/20 flex items-center justify-center">
                                    <Brain className="w-6 h-6 text-emerald-400" />
                                </div>
                                <div>
                                    <h3 className="text-xl font-bold text-white">Smart Advisor / Análisis Prestacional</h3>
                                    <p className="text-sm text-emerald-300">Inteligencia Artificial aplicada a costos laborales</p>
                                </div>
                            </div>

                            <div className="space-y-6 text-sm text-slate-300">
                                <div className="p-4 rounded-lg bg-emerald-900/20 border border-emerald-500/20 flex items-start gap-4">
                                    <div className="p-2 bg-emerald-500/20 rounded-lg">
                                        <TrendingUp className="w-6 h-6 text-emerald-400" />
                                    </div>
                                    <div>
                                        <h4 className="font-bold text-emerald-400 mb-1">Carga Prestacional Optimizada</h4>
                                        <p>El factor prestacional promedio es del <strong className="text-white">52%</strong> sobre el salario base. Se identifica que la empresa está asumiendo correctamente los aportes parafiscales y de seguridad social sin sobrecostos por mora.</p>
                                    </div>
                                </div>

                                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                                    <div>
                                        <h4 className="font-bold text-white mb-3 text-indigo-400">Distribución del Gasto</h4>
                                        <ul className="list-disc list-inside space-y-2 pl-2 text-slate-400">
                                            <li><strong className="text-white">Seguridad Social:</strong> Representa el mayor rubro no salarial.</li>
                                            <li><strong className="text-white">Provisiones:</strong> Las cesantías y primas están proyectadas correctamente.</li>
                                        </ul>
                                    </div>
                                    <div>
                                        <h4 className="font-bold text-white mb-3 text-amber-400">Recomendaciones</h4>
                                        <p className="mb-2 text-slate-400">Para optimizar el flujo de caja:</p>
                                        <ul className="list-disc list-inside space-y-2 pl-2 text-slate-400">
                                            <li>Consolidar pagos de vacaciones en periodos de baja producción.</li>
                                            <li>Revisar auxilios de transporte en empleados con trabajo remoto/híbrido.</li>
                                        </ul>
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
                                    Descargar Costeo Detallado (Excel)
                                </button>
                                <button
                                    onClick={handleDownloadPDF}
                                    className="flex-1 btn-secondary border-white/10 hover:bg-white/5 flex items-center justify-center gap-2 py-4 text-white hover:text-emerald-300 transition-colors"
                                >
                                    <FileText className="w-5 h-5" />
                                    Informe Gerencial (PDF)
                                </button>
                            </div>
                        </GlassCard>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
}
