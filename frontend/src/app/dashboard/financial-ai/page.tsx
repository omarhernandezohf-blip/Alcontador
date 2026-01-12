import { AIChat } from '@/components/modules/AIChat';
import { Cpu } from 'lucide-react';

export default function FinancialAI() {
    return (
        <div className="max-w-4xl mx-auto space-y-6">
            <div className="flex items-center gap-4 mb-8">
                <div className="p-4 rounded-2xl bg-gradient-to-br from-emerald-500/20 to-teal-500/20 border border-emerald-500/20">
                    <Cpu className="w-10 h-10 text-emerald-400" />
                </div>
                <div>
                    <h1 className="text-3xl font-bold font-space text-white">Inteligencia Financiera</h1>
                    <p className="text-slate-400">Consultor experto disponible 24/7 para auditoría y análisis.</p>
                </div>
            </div>

            <AIChat />
        </div>
    );
}
