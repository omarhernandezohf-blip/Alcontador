'use client';

import { motion } from 'framer-motion';
import { Check, X, Zap, Crown, ShieldCheck, Diamond } from 'lucide-react';
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
        buttonVariant: 'current',
        highlight: false
    },
    {
        name: 'PLAN PRO',
        price: '$70.000',
        originalPrice: '$100.000',
        period: 'COP/mes',
        features: [
            { text: '500 Créditos Mensuales', included: true },
            { text: 'Modelo Gemini 1.5 Flash', included: true },
            { text: 'Archivos hasta 10 MB', included: true },
            { text: 'Soporte Prioritario', included: true },
        ],
        buttonText: '⚡ MEJORAR A PRO',
        buttonVariant: 'primary',
        highlight: false
    },
    {
        name: 'PLAN PREMIUM',
        price: '$120.000',
        originalPrice: '$180.000',
        period: 'COP/mes',
        features: [
            { text: 'Ilimitado + Agentic IA', included: true },
            { text: 'Modelo Gemini 1.5 PRO', included: true },
            { text: 'Archivos hasta 50 MB (Massive)', included: true },
            { text: 'Auditoría NIIF Avanzada', included: true },
        ],
        buttonText: '🚀 OBTENER BLINDAJE TOTAL',
        buttonVariant: 'premium',
        highlight: true
    }
];

export function PricingSection() {
    return (
        <section className="py-12 mt-12 border-t border-white/5 relative">
            {/* Section Header */}
            <div className="flex items-center gap-3 mb-8">
                <Diamond className="w-6 h-6 text-indigo-400" />
                <h2 className="text-2xl font-bold text-white font-space tracking-wide">
                    MEJORAR NIVEL DE ACCESO
                </h2>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                {plans.map((plan, index) => (
                    <LuxuryCard
                        key={plan.name}
                        className={clsx(
                            "relative flex flex-col h-full",
                            plan.highlight ? "border-indigo-500/50 shadow-[0_0_40px_rgba(79,70,229,0.15)]" : ""
                        )}
                    >
                        {plan.highlight && (
                            <div className="absolute -top-4 right-4 px-3 py-1 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full text-[10px] font-bold text-white shadow-lg flex items-center gap-1 z-20">
                                <Crown className="w-3 h-3" />
                                RECOMENDADO
                            </div>
                        )}

                        <div className="mb-6">
                            <h3 className={clsx("text-sm font-bold tracking-wider mb-4", plan.highlight ? "text-indigo-300" : "text-slate-400")}>
                                {plan.name}
                            </h3>

                            {plan.originalPrice && (
                                <p className="text-sm text-slate-500 line-through mb-1 font-mono">
                                    {plan.originalPrice}
                                </p>
                            )}

                            <div className="flex items-end gap-1">
                                <span className={clsx("text-4xl font-bold text-white", plan.highlight && "text-transparent bg-clip-text bg-gradient-to-r from-white to-indigo-200")}>
                                    {plan.price}
                                </span>
                                <span className="text-xs text-slate-400 mb-1">{plan.period}</span>
                            </div>
                        </div>

                        <ul className="space-y-4 mb-8 flex-1">
                            {plan.features.map((feature, idx) => (
                                <li key={idx} className="flex items-start gap-3 text-sm">
                                    {feature.included ? (
                                        <Check className="w-4 h-4 text-emerald-400 mt-0.5 shrink-0" />
                                    ) : (
                                        <X className="w-4 h-4 text-rose-500/50 mt-0.5 shrink-0" />
                                    )}
                                    <span className={feature.included ? "text-slate-300" : "text-slate-600"}>
                                        {feature.text}
                                    </span>
                                </li>
                            ))}
                        </ul>

                        <button
                            className={clsx(
                                "w-full py-3 rounded-xl text-sm font-bold transition-all duration-300 flex items-center justify-center gap-2",
                                plan.buttonVariant === 'current' && "bg-slate-700/50 text-slate-400 hover:bg-slate-700/70 border border-white/5",
                                plan.buttonVariant === 'primary' && "bg-gradient-to-r from-blue-600 to-blue-500 text-white hover:shadow-lg hover:shadow-blue-500/25",
                                plan.buttonVariant === 'premium' && "bg-gradient-to-r from-indigo-600 to-purple-600 text-white hover:shadow-lg hover:shadow-indigo-500/30 group-hover:scale-[1.02]"
                            )}
                        >
                            {plan.buttonText}
                        </button>
                    </LuxuryCard>
                ))}
            </div>
        </section>
    );
}
