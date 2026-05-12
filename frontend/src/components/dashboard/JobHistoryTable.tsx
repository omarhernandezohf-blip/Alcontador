'use client';

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Search, FileText, Download, Clock, CheckCircle2, FileSpreadsheet, FileCode, Trash2, AlertCircle } from 'lucide-react';
import { useAuth } from '@/context/AuthContext';
import { db } from '@/lib/firebase';
import { collection, query, orderBy, onSnapshot, deleteDoc, doc, Timestamp } from 'firebase/firestore';

interface Job {
    id: string;
    name: string;
    type: 'excel' | 'pdf' | 'xml' | 'json';
    completedAt: Timestamp; // Firestore Timestamp
    size: string;
    status: 'completed' | 'expired';
    downloadUrl?: string; // Real download URL
}

export function JobHistoryTable() {
    const { user } = useAuth();
    const [searchTerm, setSearchTerm] = useState('');
    const [jobs, setJobs] = useState<Job[]>([]);
    const [loading, setLoading] = useState(true);

    // Fetch Real Data from Firestore
    useEffect(() => {
        if (!user?.email) {
            setLoading(false);
            return;
        }

        const q = query(
            collection(db, `users/${user.email}/history`),
            orderBy('completedAt', 'desc')
        );

        const unsubscribe = onSnapshot(q, (snapshot) => {
            const realJobs = snapshot.docs.map(doc => ({
                id: doc.id,
                ...doc.data()
            })) as Job[];

            setJobs(realJobs);
            setLoading(false);
        }, (error) => {
            console.error("Error fetching history:", error);
            setLoading(false);
        });

        return () => unsubscribe();
    }, [user]);

    const filteredJobs = jobs.filter(job =>
        job?.name?.toLowerCase().includes(searchTerm.toLowerCase())
    );

    const handleDelete = async (id: string) => {
        if (!user?.email) return;
        try {
            await deleteDoc(doc(db, `users/${user.email}/history`, id));
        } catch (error) {
            console.error("Error deleting job:", error);
        }
    };

    const getIcon = (type: string) => {
        switch (type) {
            case 'excel': return <FileSpreadsheet className="w-5 h-5 text-emerald-400" />;
            case 'pdf': return <FileText className="w-5 h-5 text-rose-400" />;
            case 'xml': return <FileCode className="w-5 h-5 text-amber-400" />;
            default: return <FileText className="w-5 h-5 text-slate-400" />;
        }
    };

    const formatDate = (timestamp: Timestamp) => {
        if (!timestamp) return '';
        // Handle both Firestore Timestamp and regular Date strings if legacy
        const date = timestamp.toDate ? timestamp.toDate() : new Date(timestamp as any);
        return date.toLocaleDateString();
    };

    return (
        <div className="w-full overflow-x-auto custom-scrollbar pb-4">
            <div className="min-w-[800px]"> {/* Ensure min width to force scroll on mobile */}
                {/* Toolbar */}
                <div className="flex items-center justify-between mb-6">
                    <div className="relative group">
                        <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                            <Search className="h-4 w-4 text-slate-500 group-focus-within:text-indigo-400 transition-colors" />
                        </div>
                        <input
                            type="text"
                            placeholder="Buscar archivo real..."
                            className="pl-10 pr-4 py-2.5 bg-slate-900/50 border border-slate-700 rounded-xl focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 text-sm text-white w-64 transition-all"
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                        />
                    </div>
                </div>

                {/* Table Header */}
                <div className="grid grid-cols-12 gap-4 px-6 py-3 text-xs font-bold text-slate-500 uppercase tracking-wider border-b border-white/5">
                    <div className="col-span-5">Nombre del Archivo</div>
                    <div className="col-span-2">Fecha</div>
                    <div className="col-span-2">Tamaño</div>
                    <div className="col-span-2">Estado</div>
                    <div className="col-span-1 text-right">Acciones</div>
                </div>

                {/* List */}
                <div className="space-y-2 mt-2">
                    {loading ? (
                        <div className="text-center py-12 text-slate-500 animate-pulse">
                            Cargando historial en tiempo real...
                        </div>
                    ) : (
                        <AnimatePresence>
                            {filteredJobs.map((job) => (
                                <motion.div
                                    key={job.id}
                                    initial={{ opacity: 0, y: 10 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    exit={{ opacity: 0, height: 0 }}
                                    className="group relative grid grid-cols-12 gap-4 px-6 py-4 items-center bg-slate-800/20 hover:bg-slate-800/40 border border-white/5 hover:border-indigo-500/30 rounded-xl transition-all duration-300"
                                >
                                    {/* File Name & Icon */}
                                    <div className="col-span-5 flex items-center gap-4">
                                        <div className="p-2.5 rounded-lg bg-slate-900 border border-white/5 shadow-sm group-hover:scale-110 transition-transform">
                                            {getIcon(job.type)}
                                        </div>
                                        <div>
                                            <h4 className="text-sm font-medium text-white group-hover:text-indigo-300 transition-colors truncate pr-4">
                                                {job.name}
                                            </h4>
                                            <span className="text-xs text-slate-500 uppercase">{job.type}</span>
                                        </div>
                                    </div>

                                    {/* Date */}
                                    <div className="col-span-2 flex items-center gap-2 text-sm text-slate-400">
                                        <Clock className="w-3.5 h-3.5 opacity-50" />
                                        <span>{formatDate(job.completedAt)}</span>
                                    </div>

                                    {/* Size */}
                                    <div className="col-span-2 text-sm text-slate-400 font-mono">
                                        {job.size}
                                    </div>

                                    {/* Status */}
                                    <div className="col-span-2">
                                        {job.status === 'completed' ? (
                                            <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-xs font-bold text-emerald-400">
                                                <CheckCircle2 className="w-3 h-3" />
                                                Disponible
                                            </span>
                                        ) : (
                                            <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-rose-500/10 border border-rose-500/20 text-xs font-bold text-rose-400">
                                                <Clock className="w-3 h-3" />
                                                Expirado
                                            </span>
                                        )}
                                    </div>

                                    {/* Actions */}
                                    <div className="col-span-1 flex justify-end gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                                        <button
                                            className="p-2 text-slate-400 hover:text-white hover:bg-indigo-600 rounded-lg transition-colors"
                                            title="Descargar"
                                            disabled={job.status === 'expired'}
                                            onClick={() => job.downloadUrl && window.open(job.downloadUrl, '_blank')}
                                        >
                                            <Download className="w-4 h-4" />
                                        </button>
                                        <button
                                            className="p-2 text-slate-400 hover:text-rose-400 hover:bg-rose-500/10 rounded-lg transition-colors"
                                            onClick={() => handleDelete(job.id)}
                                            title="Eliminar"
                                        >
                                            <Trash2 className="w-4 h-4" />
                                        </button>
                                    </div>

                                    {/* Hover Glow Effect */}
                                    <div className="absolute inset-0 rounded-xl bg-gradient-to-r from-indigo-500/0 via-indigo-500/5 to-indigo-500/0 opacity-0 group-hover:opacity-100 pointer-events-none transition-opacity" />
                                </motion.div>
                            ))}
                        </AnimatePresence>
                    )}

                    {!loading && filteredJobs.length === 0 && (
                        <div className="text-center py-16 flex flex-col items-center justify-center">
                            <div className="w-16 h-16 rounded-full bg-slate-900 border border-slate-800 flex items-center justify-center mb-4">
                                <AlertCircle className="w-8 h-8 text-slate-600" />
                            </div>
                            <h3 className="text-slate-300 font-medium mb-1">Sin Actividad Reciente</h3>
                            <p className="text-slate-500 text-sm max-w-xs mx-auto">
                                No se encontraron archivos procesados en tu cuenta. Usa los módulos del sistema para generar nuevos reportes.
                            </p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
