'use client';

import { useState, useRef } from 'react';
import { Upload, File as FileIcon, X, CheckCircle } from 'lucide-react';
import { GlassCard } from '@/components/ui/GlassCard';
import { clsx } from 'clsx';
import { motion, AnimatePresence } from 'framer-motion';

interface FileUploadProps {
    onFilesSelected: (files: File[]) => void;
    accept?: string;
    multiple?: boolean;
    label?: string;
}

export function FileUpload({ onFilesSelected, accept, multiple = false, label = "Arrastra archivos aquí" }: FileUploadProps) {
    const [dragActive, setDragActive] = useState(false);
    const [files, setFiles] = useState<File[]>([]);
    const inputRef = useRef<HTMLInputElement>(null);

    const handleDrag = (e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === "dragenter" || e.type === "dragover") {
            setDragActive(true);
        } else if (e.type === "dragleave") {
            setDragActive(false);
        }
    };

    const handleDrop = (e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            const newFiles = Array.from(e.dataTransfer.files);
            setFiles(newFiles);
            onFilesSelected(newFiles);
        }
    };

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        e.preventDefault();
        if (e.target.files && e.target.files[0]) {
            const newFiles = Array.from(e.target.files);
            setFiles(newFiles);
            onFilesSelected(newFiles);
        }
    };

    const removeFile = (index: number) => {
        const newFiles = files.filter((_, i) => i !== index);
        setFiles(newFiles);
        onFilesSelected(newFiles);
    };

    return (
        <div className="w-full">
            <div
                className={clsx(
                    "relative border-2 border-dashed rounded-xl p-8 transition-all duration-300 ease-in-out text-center cursor-pointer overflow-hidden group",
                    dragActive
                        ? "border-indigo-500 bg-indigo-500/10 scale-[1.02]"
                        : "border-white/10 bg-white/5 hover:bg-white/10 hover:border-white/20"
                )}
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
                onClick={() => inputRef.current?.click()}
            >
                <input
                    ref={inputRef}
                    type="file"
                    className="hidden"
                    multiple={multiple}
                    accept={accept}
                    onChange={handleChange}
                />

                <div className="flex flex-col items-center gap-4 relative z-10">
                    <div className={clsx(
                        "p-4 rounded-full transition-all duration-300",
                        dragActive ? "bg-indigo-500 text-white" : "bg-white/60 text-indigo-900 group-hover:scale-110"
                    )}>
                        <Upload className="w-6 h-6" />
                    </div>
                    <div>
                        <p className="text-lg font-medium text-white">{label}</p>
                        <p className="text-sm text-slate-400 mt-1">o haz click para explorar</p>
                    </div>
                </div>

                {/* Glow effect */}
                <div className="absolute inset-0 bg-gradient-to-tr from-indigo-500/0 via-indigo-500/0 to-indigo-500/0 group-hover:from-indigo-500/5 group-hover:to-purple-500/5 transition-all duration-500" />
            </div>

            <AnimatePresence>
                {files.length > 0 && (
                    <motion.div
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: 'auto' }}
                        exit={{ opacity: 0, height: 0 }}
                        className="mt-4 space-y-2"
                    >
                        {files.map((file, idx) => (
                            <motion.div
                                key={`${file.name}-${idx}`}
                                initial={{ x: -20, opacity: 0 }}
                                animate={{ x: 0, opacity: 1 }}
                                exit={{ x: 20, opacity: 0 }}
                                className="flex items-center justify-between p-3 bg-white/5 border border-white/5 rounded-lg"
                            >
                                <div className="flex items-center gap-3 overflow-hidden">
                                    <FileIcon className="w-4 h-4 text-indigo-400 shrink-0" />
                                    <span className="text-sm text-slate-200 truncate max-w-[200px]">{file.name}</span>
                                    <span className="text-xs text-slate-500">({(file.size / 1024).toFixed(1)} KB)</span>
                                </div>
                                <button
                                    onClick={(e) => { e.stopPropagation(); removeFile(idx); }}
                                    className="p-1 hover:bg-white/10 rounded-full text-slate-400 hover:text-rose-400 transition-colors"
                                >
                                    <X className="w-4 h-4" />
                                </button>
                            </motion.div>
                        ))}
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
}
