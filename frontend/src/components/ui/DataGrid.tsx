'use client';

import { GlassCard } from './GlassCard';
import { clsx } from 'clsx';

interface DataGridProps {
    data: any[];
    className?: string;
    title?: string;
}

export function DataGrid({ data, className, title }: DataGridProps) {
    if (!data || data.length === 0) return null;

    const columns = Object.keys(data[0]);

    return (
        <GlassCard className={clsx("overflow-hidden p-0", className)}>
            {title && (
                <div className="px-6 py-4 border-b border-white/10 bg-white/5">
                    <h3 className="font-bold text-white">{title}</h3>
                </div>
            )}
            <div className="overflow-x-auto custom-scrollbar">
                <table className="w-full text-sm text-left">
                    <thead className="text-xs text-slate-300 uppercase bg-black/20 font-space tracking-wider">
                        <tr>
                            {columns.map((col) => (
                                <th key={col} className="px-6 py-4 font-semibold whitespace-nowrap">
                                    {col}
                                </th>
                            ))}
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-white/5">
                        {data.map((row, idx) => (
                            <tr
                                key={idx}
                                className="bg-transparent hover:bg-white/5 transition-colors duration-150"
                            >
                                {columns.map((col) => (
                                    <td key={`${idx}-${col}`} className="px-6 py-4 font-medium text-slate-200 truncate max-w-[300px]">
                                        {typeof row[col] === 'object' ? JSON.stringify(row[col]) : row[col]}
                                    </td>
                                ))}
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </GlassCard>
    );
}
