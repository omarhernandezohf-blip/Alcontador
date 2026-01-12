import { Info, X } from 'lucide-react';
import { useState, useRef, useEffect } from 'react';
import { createPortal } from 'react-dom';
import { motion, AnimatePresence } from 'framer-motion';

interface FileGuideProps {
    moduleName: string;
    requiredColumns: string[];
    exampleRow: Record<string, string | number>;
    tips?: string[];
}

export function FileGuide({ moduleName, requiredColumns, exampleRow, tips }: FileGuideProps) {
    const [isOpen, setIsOpen] = useState(false);
    const [position, setPosition] = useState({ top: 0, left: 0 });
    const buttonRef = useRef<HTMLButtonElement>(null);

    // Calculate position when opening
    useEffect(() => {
        if (isOpen && buttonRef.current) {
            const rect = buttonRef.current.getBoundingClientRect();
            // Position: Bottom Left aligned by default, adjust if screen edge is close
            let top = rect.bottom + 8;
            let left = rect.left;

            // Simple bound check (if offscreen to right, align right edge)
            if (left + 320 > window.innerWidth) {
                left = window.innerWidth - 340;
            }

            setPosition({ top, left });
        }
    }, [isOpen]);

    // Close on click outside
    useEffect(() => {
        const handleClickOutside = (e: MouseEvent) => {
            if (buttonRef.current && !buttonRef.current.contains(e.target as Node)) {
                // If clicking inside the portal content (handled by preventing propagation in content)
                // Actually, since portal is in body, we need a ref for the content or check target
                const portalElement = document.getElementById('file-guide-portal');
                if (portalElement && !portalElement.contains(e.target as Node)) {
                    setIsOpen(false);
                }
            }
        };

        if (isOpen) {
            window.addEventListener('click', handleClickOutside);
        }
        return () => window.removeEventListener('click', handleClickOutside);
    }, [isOpen]);

    return (
        <>
            <button
                ref={buttonRef}
                onClick={() => setIsOpen(!isOpen)}
                className="flex items-center gap-2 text-sm text-emerald-400 hover:text-white hover:bg-emerald-600/40 transition-all bg-emerald-950/50 px-3 py-1.5 rounded-lg border border-emerald-500/30 cursor-pointer z-20 relative shadow-lg shadow-emerald-900/10"
            >
                <Info className="w-4 h-4" />
                <span className="font-medium">¿Cómo debe ser el archivo?</span>
            </button>

            {isOpen && typeof document !== 'undefined' && createPortal(
                <AnimatePresence>
                    <motion.div
                        initial={{ opacity: 0, y: -10, scale: 0.95 }}
                        animate={{ opacity: 1, y: 0, scale: 1 }}
                        exit={{ opacity: 0, scale: 0.95 }}
                        className="fixed z-[9999] w-80 p-4 rounded-xl bg-slate-900/95 border border-emerald-500/30 shadow-2xl shadow-black/50 backdrop-blur-md"
                        style={{ top: position.top, left: position.left }}
                        id="file-guide-portal" // ID for click-outside check
                    >
                        <div className="flex justify-between items-start mb-3">
                            <h4 className="font-bold text-white text-sm">Estructura para Importación</h4>
                            <button onClick={() => setIsOpen(false)} className="text-slate-400 hover:text-white">
                                <X className="w-4 h-4" />
                            </button>
                        </div>

                        <div className="bg-slate-950/50 rounded-lg p-3 border border-white/5 overflow-x-auto mb-3">
                            <table className="w-full text-xs text-left">
                                <thead>
                                    <tr className="border-b border-white/10 text-emerald-400">
                                        {requiredColumns.map(col => (
                                            <th key={col} className="pb-2 px-2 whitespace-nowrap">{col}</th>
                                        ))}
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr className="text-slate-300">
                                        {Object.values(exampleRow).map((val, i) => (
                                            <td key={i} className="pt-2 px-2 whitespace-nowrap">{val}</td>
                                        ))}
                                    </tr>
                                </tbody>
                            </table>
                        </div>

                        {tips && (
                            <div className="bg-emerald-500/5 rounded-md p-2 border border-emerald-500/10">
                                <ul className="text-[10px] text-slate-300 space-y-1 list-disc pl-3">
                                    {tips.map((tip, i) => (
                                        <li key={i}>{tip}</li>
                                    ))}
                                </ul>
                            </div>
                        )}
                    </motion.div>
                </AnimatePresence>,
                document.body
            )}
        </>
    );
}
