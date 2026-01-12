'use client';

import { motion } from 'framer-motion';
import { Sparkles, Command, Radio } from 'lucide-react';
import { useAuth } from '@/context/AuthContext';

export function HeroSection() {
    const { user } = useAuth();
    return (
        <div className="relative w-full h-[300px] flex items-center justify-between overflow-hidden rounded-3xl bg-slate-950/50 border border-white/5 p-12 mb-8 group">
            {/* Ambient Background Glow */}
            <div className="absolute inset-0 bg-gradient-to-r from-indigo-500/10 via-purple-500/5 to-transparent blur-3xl" />

            {/* Content Left */}
            <div className="relative z-10 max-w-2xl">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8 }}
                    className="flex items-center gap-3 mb-4"
                >
                    <span className="px-3 py-1 rounded-full bg-amber-500/10 border border-amber-500/20 text-amber-400 text-xs font-bold tracking-wider uppercase flex items-center gap-2">
                        <Sparkles className="w-3 h-3" />
                        Edición Platino
                    </span>
                    <span className="px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-bold tracking-wider uppercase flex items-center gap-2">
                        <Radio className="w-3 h-3 animate-pulse" />
                        Sistema Online
                    </span>
                </motion.div>

                <motion.h1
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8, delay: 0.2 }}
                    className="text-6xl font-bold font-space text-white mb-2 tracking-tight"
                >
                    Hola, <span className="text-transparent bg-clip-text bg-gradient-to-r from-amber-200 via-yellow-100 to-amber-500 filter drop-shadow-[0_0_10px_rgba(251,191,36,0.5)]">
                        {user?.name?.split(' ')[0] || 'Experto'}.
                    </span>
                </motion.h1>

                <motion.p
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ duration: 1, delay: 0.5 }}
                    className="text-lg text-slate-400 font-light"
                >
                    Bienvenido al <span className="text-indigo-400 font-medium">Nexus Financiero</span>. Tu imperio contable está sincronizado y listo para la excelencia.
                </motion.p>
            </div>

            {/* The Core Animation (Right Side) */}
            <div className="relative z-10 hidden lg:block">
                <div className="relative w-48 h-48 flex items-center justify-center">
                    {/* Outer Rings */}
                    <div className="absolute inset-0 border border-indigo-500/20 rounded-full animate-[spin_10s_linear_infinite]" />
                    <div className="absolute inset-2 border border-purple-500/20 rounded-full animate-[spin_15s_linear_infinite_reverse]" />
                    <div className="absolute inset-12 border-2 border-dashed border-white/10 rounded-full animate-[spin_20s_linear_infinite]" />

                    {/* The Core Orb */}
                    <div className="relative w-20 h-20 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-full shadow-[0_0_50px_rgba(99,102,241,0.5)] flex items-center justify-center animate-pulse">
                        <Command className="w-8 h-8 text-white" />
                    </div>

                    {/* Orbital Particles */}
                    <div className="absolute top-0 left-1/2 w-2 h-2 bg-emerald-400 rounded-full shadow-[0_0_10px_rgba(52,211,153,0.8)] animate-bounce" />
                </div>
            </div>

            {/* Interactive Grid overlay */}
            <div className="absolute inset-0 bg-[url('/grid.svg')] bg-center [mask-image:linear-gradient(180deg,white,rgba(255,255,255,0))]" />
        </div>
    );
}
