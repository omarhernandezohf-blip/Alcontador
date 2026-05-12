'use client';

import { motion } from 'framer-motion';
import { Check, X, Zap, Crown, ShieldCheck, Diamond, Sparkles, Star } from 'lucide-react';
import { LuxuryCard } from '@/components/ui/LuxuryCard';
import { clsx } from 'clsx';

const plans = [
    {
        name: 'NIVEL INICIAL',
        price: '$0',
        period: 'COP/mes',
        features: [
            { text: 'Acceso al Dashboard', included: true },
            { text: '5 Consultas IA/día', included: true },
            { text: 'Archivos hasta 2 MB', included: true },
            { text: 'Agente Tributario', included: false },
            { text: 'Conexión Bancaria', included: false },
        ],
        buttonText: 'PLAN ACTUAL',
        variant: 'free',
    },
    {
        name: 'PLAN PRO',
        price: '$70.000',
        originalPrice: '$100.000',
        period: 'COP/mes',
        description: 'Para contadores que buscan velocidad.',
        features: [
            { text: '400 Créditos Mensuales', included: true },
            { text: 'Modelo Gemini 1.5 Flash', included: true },
            { text: 'Archivos hasta 10 MB', included: true },
            { text: 'Soporte Prioritario', included: true },
        ],
        buttonText: 'MEJORAR A PRO',
        variant: 'pro',
    },
    {
        name: 'PLAN PREMIUM',
        price: '$120.000',
        originalPrice: '$180.000',
        period: 'COP/mes',
        description: 'La suite definitiva para líderes.',
        features: [
            { text: '2000 Créditos + Agentic IA', included: true },
            { text: 'Modelo Gemini 1.5 PRO', included: true },
            { text: 'Archivos hasta 50 MB (Massive)', included: true },
            { text: 'Auditoría NIIF Avanzada', included: true },
            { text: 'Acceso Anticipado a Funciones', included: true },
        ],
        buttonText: 'OBTENER BLINDAJE TOTAL',
        variant: 'premium',
    }
];

export function PricingSection() {
    return (
        <section className="py-16 mt-12 border-t border-white/5 relative overflow-hidden">
            {/* Background Effects */}
            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[400px] bg-indigo-500/10 blur-[120px] rounded-full pointer-events-none" />

            {/* Section Header */}
            <div className="flex flex-col items-center gap-4 mb-16 text-center relative z-10">
                <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-xs font-bold tracking-wider uppercase">
                    <Diamond className="w-3 h-3" />
                    Propuestas de Valor
                </div>
                <h2 className="text-4xl md:text-5xl font-bold text-white font-space tracking-tight">
                    Eleva tu <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-purple-400">Potencial Contable</span>
                </h2>
                <p className="text-slate-400 max-w-lg">
                    Herramientas diseñadas para cada etapa de tu crecimiento profesional.
                </p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 align-stretch max-w-7xl mx-auto px-4">
                {plans.map((plan, index) => (
                    <div key={plan.name} className={clsx("relative", plan.variant === 'premium' ? "lg:-mt-8 lg:mb-4 z-20" : "z-10")}>
                        {/* PREMIUM GLOW */}
                        {plan.variant === 'premium' && (
                            <div className="absolute inset-0 bg-gradient-to-b from-amber-500/20 to-purple-600/20 blur-3xl -z-10" />
                        )}

                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            viewport={{ once: true }}
                            transition={{ delay: index * 0.1 }}
                            className={clsx(
                                "flex flex-col h-full rounded-3xl p-8 border transition-all duration-500 relative overflow-hidden group hover:-translate-y-2",
                                plan.variant === 'free' && "bg-slate-900/40 border-slate-800 hover:border-slate-700 grayscale hover:grayscale-0",
                                plan.variant === 'pro' && "bg-slate-900/60 border-blue-500/30 hover:border-cyan-400/50 hover:shadow-[0_0_30px_rgba(34,211,238,0.1)]",
                                plan.variant === 'premium' && "bg-slate-900/80 border-amber-500/50 shadow-2xl shadow-indigo-500/20 ring-1 ring-white/10 scale-105"
                            )}
                        >
                            {/* Recommended Badge */}
                            {plan.variant === 'premium' && (
                                <div className="absolute top-0 inset-x-0 flex justify-center -mt-px">
                                    <div className="bg-gradient-to-r from-amber-500 via-yellow-500 to-amber-600 text-white text-[10px] font-bold tracking-widest uppercase px-4 py-1 rounded-b-xl shadow-lg flex items-center gap-1.5">
                                        <Crown className="w-3 h-3 fill-white/50" />
                                        Recomendado por Expertos
                                    </div>
                                </div>
                            )}

                            {/* Plan Header */}
                            <div className="mb-8">
                                <h3 className={clsx(
                                    "text-sm font-bold tracking-wider mb-2 uppercase",
                                    plan.variant === 'free' && "text-slate-500",
                                    plan.variant === 'pro' && "text-cyan-400",
                                    plan.variant === 'premium' && "text-transparent bg-clip-text bg-gradient-to-r from-amber-200 to-yellow-500"
                                )}>
                                    {plan.name}
                                </h3>

                                <div className="flex items-baseline gap-1 mb-2">
                                    <span className={clsx(
                                        "text-4xl md:text-5xl font-bold tracking-tighter",
                                        plan.variant === 'free' && "text-slate-300",
                                        plan.variant === 'pro' && "text-white",
                                        plan.variant === 'premium' && "text-white drop-shadow-[0_0_10px_rgba(251,191,36,0.3)]"
                                    )}>
                                        {plan.price}
                                    </span>
                                    <span className="text-sm text-slate-500 font-medium">{plan.period}</span>
                                </div>

                                {plan.originalPrice && (
                                    <div className="inline-flex items-center px-2 py-0.5 rounded-md bg-rose-500/10 border border-rose-500/20">
                                        <span className="text-xs text-rose-400 line-through font-mono">
                                            {plan.originalPrice}
                                        </span>
                                        <span className="ml-2 text-[10px] font-bold text-rose-500">
                                            AHORRAS 35%
                                        </span>
                                    </div>
                                )}
                            </div>

                            {/* Divider */}
                            <div className={clsx("h-px w-full mb-8",
                                plan.variant === 'free' ? "bg-slate-800" :
                                    plan.variant === 'pro' ? "bg-gradient-to-r from-transparent via-cyan-500/30 to-transparent" :
                                        "bg-gradient-to-r from-transparent via-amber-500/50 to-transparent"
                            )} />

                            {/* Features */}
                            <ul className="space-y-4 mb-8 flex-1">
                                {plan.features.map((feature, idx) => (
                                    <li key={idx} className={clsx("flex items-start gap-3 text-sm group/item",
                                        !feature.included && "opacity-50"
                                    )}>
                                        {feature.included ? (
                                            <div className={clsx(
                                                "mt-0.5 rounded-full p-0.5",
                                                plan.variant === 'premium' ? "bg-amber-500/20 text-amber-300" :
                                                    plan.variant === 'pro' ? "bg-cyan-500/20 text-cyan-400" : "bg-slate-700 text-slate-400"
                                            )}>
                                                <Check className="w-3 h-3" />
                                            </div>
                                        ) : (
                                            <X className="w-4 h-4 text-slate-700 mt-0.5" />
                                        )}
                                        <span className={clsx(
                                            feature.included ? "text-slate-300" : "text-slate-600 decoration-slate-700",
                                            plan.variant === 'premium' && feature.included && "font-medium text-slate-200"
                                        )}>
                                            {feature.text}
                                        </span>
                                    </li>
                                ))}
                            </ul>

                            {/* CTA Button */}
                            <button
                                className={clsx(
                                    "w-full py-4 rounded-xl text-sm font-bold tracking-wide transition-all duration-300 relative overflow-hidden group/btn",
                                    plan.variant === 'free' && "bg-slate-800 text-slate-400 border border-slate-700 hover:bg-slate-700",
                                    plan.variant === 'pro' && "bg-slate-800 text-white border border-cyan-500/50 hover:bg-cyan-950/30 hover:shadow-[0_0_20px_rgba(34,211,238,0.2)] hover:border-cyan-400",
                                    plan.variant === 'premium' && "bg-gradient-to-r from-indigo-600 via-purple-600 to-indigo-600 bg-[length:200%_auto] animate-gradient text-white shadow-lg shadow-indigo-500/40 hover:shadow-indigo-500/60 scale-105"
                                )}
                            >
                                <span className="relative z-10 flex items-center justify-center gap-2">
                                    {plan.variant === 'pro' && <Zap className="w-4 h-4 fill-current animate-pulse" />}
                                    {plan.variant === 'premium' && <Sparkles className="w-4 h-4 animate-pulse" />}
                                    {plan.buttonText}
                                </span>

                                {/* Shine Effect for Premium */}
                                {plan.variant === 'premium' && (
                                    <div className="absolute inset-0 -translate-x-[100%] group-hover/btn:translate-x-[100%] transition-transform duration-1000 bg-gradient-to-r from-transparent via-white/20 to-transparent" />
                                )}
                            </button>

                        </motion.div>
                    </div>
                ))}
            </div>
        </section>
    );
}
