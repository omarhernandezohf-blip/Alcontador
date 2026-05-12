'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { LuxuryCard } from '@/components/ui/LuxuryCard';
import { StarsBackground } from '@/components/ui/StarsBackground';
import { useAuth } from '@/context/AuthContext';
import { Lock, Mail, ChevronRight, AlertCircle, Command } from 'lucide-react';
import Image from 'next/image';


export default function LoginPage() {
    const { login, loginWithGoogle } = useAuth();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState('');

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsLoading(true);
        setError('');

        try {
            const success = await login(email, password);
            if (!success) {
                setError('Credenciales inválidas. Prueba con: admin@premium.com');
            }
        } catch (err) {
            setError('Error al conectar con el servidor.');
        } finally {
            setIsLoading(false);
        }
    };

    const handleGoogleLogin = async () => {
        setIsLoading(true);
        await loginWithGoogle();
        setIsLoading(false);
    };

    return (
        <div className="min-h-screen w-full flex items-center justify-center bg-slate-950 relative overflow-hidden font-sans">
            <StarsBackground />

            {/* Ambient Glow */}
            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] bg-indigo-500/10 rounded-full blur-[100px]" />

            <div className="relative z-10 w-full max-w-md px-4">
                <motion.div
                    initial={{ opacity: 0, y: 30 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8 }}
                >
                    <div className="text-center mb-8">
                        <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-br from-indigo-500 to-purple-600 shadow-xl shadow-indigo-500/30 mb-6">
                            <Command className="w-8 h-8 text-white" />
                        </div>
                        <h1 className="text-3xl font-bold text-white mb-2 font-space tracking-tight">Bienvenido de Nuevo <span className="text-xs align-top bg-indigo-500/20 text-indigo-300 px-2 py-0.5 rounded-full border border-indigo-500/30">v1.0</span></h1>
                        <p className="text-slate-400">Accede a tu Suite Financiera Premium</p>
                    </div>

                    <LuxuryCard className="bg-slate-900/60 backdrop-blur-xl border-white/10">
                        <form onSubmit={handleSubmit} className="space-y-6">

                            <div className="space-y-2">
                                <label className="text-xs font-bold text-slate-500 uppercase tracking-wider">Correo Corporativo</label>
                                <div className="relative group">
                                    <Mail className="absolute left-4 top-3.5 w-5 h-5 text-slate-500 group-focus-within:text-indigo-400 transition-colors" />
                                    <input
                                        type="email"
                                        value={email}
                                        onChange={(e) => setEmail(e.target.value)}
                                        className="w-full bg-slate-950/50 border border-white/10 rounded-xl py-3 pl-12 pr-4 text-white placeholder-slate-600 focus:outline-none focus:border-indigo-500/50 focus:ring-1 focus:ring-indigo-500/50 transition-all"
                                        placeholder="nombre@empresa.com"
                                        required
                                    />
                                </div>
                            </div>

                            <div className="space-y-2">
                                <label className="text-xs font-bold text-slate-500 uppercase tracking-wider">Contraseña</label>
                                <div className="relative group">
                                    <Lock className="absolute left-4 top-3.5 w-5 h-5 text-slate-500 group-focus-within:text-indigo-400 transition-colors" />
                                    <input
                                        type="password"
                                        value={password}
                                        onChange={(e) => setPassword(e.target.value)}
                                        className="w-full bg-slate-950/50 border border-white/10 rounded-xl py-3 pl-12 pr-4 text-white placeholder-slate-600 focus:outline-none focus:border-indigo-500/50 focus:ring-1 focus:ring-indigo-500/50 transition-all"
                                        placeholder="••••••••"
                                        required
                                    />
                                </div>
                            </div>

                            {error && (
                                <motion.div
                                    initial={{ opacity: 0, height: 0 }}
                                    animate={{ opacity: 1, height: 'auto' }}
                                    className="p-3 rounded-lg bg-rose-500/10 border border-rose-500/20 flex items-center gap-3"
                                >
                                    <AlertCircle className="w-5 h-5 text-rose-400" />
                                    <span className="text-sm text-rose-300">{error}</span>
                                </motion.div>
                            )}

                            <button
                                type="submit"
                                disabled={isLoading}
                                className="w-full py-3.5 rounded-xl bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-bold shadow-lg shadow-indigo-500/25 transition-all active:scale-[0.98] disabled:opacity-70 flex items-center justify-center gap-2"
                            >
                                {isLoading ? (
                                    <span className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                                ) : (
                                    <>Acceder al Sistema <ChevronRight className="w-4 h-4" /></>
                                )}
                            </button>

                            <div className="relative py-4">
                                <div className="absolute inset-0 flex items-center">
                                    <div className="w-full border-t border-white/10"></div>
                                </div>
                                <div className="relative flex justify-center text-xs">
                                    <span className="px-2 bg-slate-900/60 text-slate-500">O continúa con</span>
                                </div>
                            </div>

                            <button
                                type="button"
                                onClick={handleGoogleLogin}
                                disabled={isLoading}
                                className="w-full py-3.5 rounded-xl bg-white hover:bg-slate-50 text-slate-900 font-bold border border-slate-200 transition-all flex items-center justify-center gap-3 disabled:opacity-70"
                            >
                                {/* Google SVG Icon */}
                                <svg className="w-5 h-5" viewBox="0 0 24 24">
                                    <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4" />
                                    <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853" />
                                    <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.26.81-.58z" fill="#FBBC05" />
                                    <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335" />
                                </svg>
                                Google
                            </button>

                        </form>
                    </LuxuryCard>

                    <div className="mt-8 text-center space-y-2">
                        <p className="text-xs text-slate-500">Credenciales Demo:</p>
                        <div className="flex justify-center gap-4 text-xs font-mono text-slate-400">
                            <span className="cursor-pointer hover:text-white" onClick={() => setEmail('usuario@inicial.com')}>usuario@inicial.com</span>
                            <span className="cursor-pointer hover:text-white" onClick={() => setEmail('admin@premium.com')}>admin@premium.com</span>
                        </div>
                    </div>


                </motion.div>
            </div>
        </div>
    );
}
