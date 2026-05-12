'use client';

import { useState, useRef } from 'react';
import { motion } from 'framer-motion';
import { useAuth } from '@/context/AuthContext';
import { User, CreditCard, Calendar, Shield, Save, Camera, Sparkles } from 'lucide-react';
import { clsx } from 'clsx';
import { PremiumAvatarFrame } from '@/components/ui/PremiumAvatarFrame';

export default function ProfilePage() {
    const { user, updateUser } = useAuth();
    const [isEditing, setIsEditing] = useState(false);
    const [name, setName] = useState(user?.name || '');
    const [isProcessing, setIsProcessing] = useState(false);
    const fileInputRef = useRef<HTMLInputElement>(null);

    // Calculate days remaining
    const daysRemaining = user?.subscriptionEnd
        ? Math.ceil((new Date(user.subscriptionEnd).getTime() - new Date().getTime()) / (1000 * 60 * 60 * 24))
        : 0;

    const handleSave = () => {
        if (name !== user?.name) {
            updateUser({ name });
        }
        setIsEditing(false);
    };

    const handleCameraClick = () => {
        if (isProcessing) return;
        // Programmatically trigger the file input
        fileInputRef.current?.click();
    };

    const compressImage = (file: File): Promise<string> => {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload = (event) => {
                const img = new Image();
                img.src = event.target?.result as string;
                img.onload = () => {
                    const canvas = document.createElement('canvas');
                    const MAX_WIDTH = 300;
                    const MAX_HEIGHT = 300;
                    let width = img.width;
                    let height = img.height;

                    if (width > height) {
                        if (width > MAX_WIDTH) {
                            height *= MAX_WIDTH / width;
                            width = MAX_WIDTH;
                        }
                    } else {
                        if (height > MAX_HEIGHT) {
                            width *= MAX_HEIGHT / height;
                            height = MAX_HEIGHT;
                        }
                    }

                    canvas.width = width;
                    canvas.height = height;
                    const ctx = canvas.getContext('2d');
                    if (!ctx) {
                        reject(new Error("No 2d context"));
                        return;
                    }
                    ctx.drawImage(img, 0, 0, width, height);
                    resolve(canvas.toDataURL('image/jpeg', 0.7));
                };
                img.onerror = (e) => reject(e);
            };
            reader.onerror = (e) => reject(e);
        });
    };

    const handleAvatarChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (file) {
            setIsProcessing(true);
            try {
                const compressedBase64 = await compressImage(file);
                updateUser({ avatar: compressedBase64 });
            } catch (error) {
                console.error("Error processing image:", error);
                alert("Error al procesar la imagen.");
            } finally {
                setIsProcessing(false);
                if (fileInputRef.current) {
                    fileInputRef.current.value = '';
                }
            }
        }
    };

    if (!user) return null;

    return (
        <div className="p-6 max-w-5xl mx-auto space-y-8">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-white mb-2">Mi Perfil <span className="text-xs bg-rose-500/20 text-rose-300 px-2 py-1 rounded-full border border-rose-500/30 align-middle">v1.0</span></h1>
                <p className="text-slate-400">Gestiona tu información personal y membresía</p>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Left Column: Personal Info */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="lg:col-span-2 space-y-6"
                >
                    {/* Identity Card */}
                    <div className="glass-panel p-8 rounded-2xl border border-white/5 relative overflow-hidden group">
                        <div className="absolute top-0 right-0 p-32 bg-indigo-500/10 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2" />

                        <div className="flex flex-col sm:flex-row items-center sm:items-start gap-6 relative z-10">
                            <div className="relative pb-8"> {/* Added padding bottom for the badge */}
                                <PremiumAvatarFrame
                                    avatarUrl={user.avatar}
                                    userName={user.name}
                                    plan={user.plan || 'free'}
                                    isProcessing={isProcessing}
                                    onCameraClick={handleCameraClick}
                                    size="xl"
                                />

                                {/* Hidden Input remains outside component logic but controlled by ref */}
                                <input
                                    type="file"
                                    ref={fileInputRef}
                                    accept="image/*"
                                    className="hidden"
                                    onChange={handleAvatarChange}
                                    style={{ display: 'none' }}
                                />
                            </div>

                            <div className="flex-1 text-center sm:text-left space-y-4 w-full">
                                <div>
                                    <label className="text-xs text-slate-500 uppercase tracking-wider font-bold mb-1 block">Nombre Visible</label>
                                    {isEditing ? (
                                        <input
                                            type="text"
                                            value={name}
                                            onChange={(e) => setName(e.target.value)}
                                            className="bg-slate-900/50 border border-white/10 rounded-lg px-4 py-2 text-white w-full focus:outline-none focus:border-indigo-500 transition-colors"
                                        />
                                    ) : (
                                        <h2 className="text-2xl font-bold text-white">{user.name}</h2>
                                    )}
                                </div>

                                <div>
                                    <label className="text-xs text-slate-500 uppercase tracking-wider font-bold mb-1 block">Correo Electrónico</label>
                                    <p className="text-slate-300 font-mono">{user.email}</p>
                                </div>

                                <div className="pt-2">
                                    {isEditing ? (
                                        <div className="flex gap-3 justify-center sm:justify-start">
                                            <button
                                                onClick={handleSave}
                                                className="px-4 py-2 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded-lg hover:bg-emerald-500/20 transition-all text-sm font-bold flex items-center gap-2"
                                            >
                                                <Save className="w-4 h-4" /> Guardar Cambios
                                            </button>
                                            <button
                                                onClick={() => setIsEditing(false)}
                                                className="px-4 py-2 bg-slate-800 text-slate-400 rounded-lg hover:bg-slate-700 transition-all text-sm font-bold"
                                            >
                                                Cancelar
                                            </button>
                                        </div>
                                    ) : (
                                        <button
                                            onClick={() => setIsEditing(true)}
                                            className="text-sm text-indigo-400 hover:text-indigo-300 font-medium underline-offset-4 hover:underline"
                                        >
                                            Editar Información
                                        </button>
                                    )}
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Security & Access */}
                    <div className="glass-panel p-6 rounded-2xl border border-white/5">
                        <h3 className="text-lg font-bold text-white mb-6 flex items-center gap-2">
                            <Shield className="w-5 h-5 text-emerald-400" />
                            Seguridad y Acceso
                        </h3>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div className="p-4 rounded-xl bg-slate-900/30 border border-white/5 hover:border-indigo-500/30 transition-colors group cursor-pointer">
                                <div className="flex items-center justify-between mb-2">
                                    <span className="text-slate-300 font-medium group-hover:text-indigo-300 transition-colors">Contraseña</span>
                                    <span className="text-xs text-slate-500">********</span>
                                </div>
                                <p className="text-xs text-slate-500">Último cambio hace 3 meses</p>
                            </div>
                            <div className="p-4 rounded-xl bg-slate-900/30 border border-white/5 hover:border-indigo-500/30 transition-colors group cursor-pointer">
                                <div className="flex items-center justify-between mb-2">
                                    <span className="text-slate-300 font-medium group-hover:text-indigo-300 transition-colors">Autenticación 2FA</span>
                                    <span className="px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 text-[10px] font-bold">ACTIVO</span>
                                </div>
                                <p className="text-xs text-slate-500">Protección Google Auth</p>
                            </div>
                        </div>
                    </div>
                </motion.div>

                {/* Right Column: Subscription Stats */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.1 }}
                    className="space-y-6"
                >
                    {/* Subscription Card */}
                    <div className="glass-panel p-6 rounded-2xl border border-white/5 relative overflow-hidden">
                        <div className="absolute top-0 right-0 p-24 bg-purple-500/10 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2" />

                        <h3 className="text-lg font-bold text-white mb-6 flex items-center gap-2 relative z-10">
                            <CreditCard className="w-5 h-5 text-purple-400" />
                            Tu Membresía
                        </h3>

                        <div className="space-y-6 relative z-10">
                            <div className="flex items-center justify-between">
                                <span className="text-slate-400">Plan Actual</span>
                                <span className={clsx(
                                    "px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wide",
                                    user.plan === 'premium' ? "bg-indigo-500/20 text-indigo-300 border border-indigo-500/30" :
                                        user.plan === 'pro' ? "bg-blue-500/20 text-blue-300 border border-blue-500/30" :
                                            "bg-slate-700 text-slate-300"
                                )}>
                                    {user.plan}
                                </span>
                            </div>

                            <div className="space-y-2">
                                <div className="flex items-center justify-between text-sm">
                                    <span className="text-slate-400">Créditos IA</span>
                                    <span className="text-white font-bold">{user.credits} / {user.plan === 'premium' ? 2000 : user.plan === 'pro' ? 400 : 5}</span>
                                </div>
                                <div className="h-2 bg-slate-800 rounded-full overflow-hidden">
                                    <motion.div
                                        initial={{ width: 0 }}
                                        animate={{ width: `${Math.min(100, (user.credits || 0) / (user.plan === 'premium' ? 2000 : user.plan === 'pro' ? 400 : 5) * 100)}%` }}
                                        className="h-full bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full"
                                    />
                                </div>
                                <p className="text-[10px] text-slate-500 flex items-center gap-1">
                                    <Sparkles className="w-3 h-3 text-amber-400" />
                                    Cada consulta consume 1 crédito
                                </p>
                            </div>

                            <div className="pt-4 border-t border-white/5">
                                <div className="flex items-start gap-4">
                                    <div className="p-3 rounded-lg bg-slate-900 border border-white/10 text-center flex-1">
                                        <span className="block text-2xl font-bold text-white mb-1">
                                            {daysRemaining}
                                        </span>
                                        <span className="text-[10px] text-slate-500 uppercase font-bold">Días Restantes</span>
                                    </div>
                                    <div className="p-3 rounded-lg bg-slate-900 border border-white/10 text-center flex-1">
                                        <Calendar className="w-6 h-6 text-slate-400 mx-auto mb-1" />
                                        <span className="text-[10px] text-slate-500 uppercase font-bold">Renovación Auto</span>
                                    </div>
                                </div>
                                <p className="text-xs text-center text-slate-500 mt-4">
                                    Tu suscripción vence el {user.subscriptionEnd ? new Date(user.subscriptionEnd).toLocaleDateString() : 'N/A'}
                                </p>
                            </div>

                            <button className="w-full py-3 rounded-xl bg-white/5 hover:bg-white/10 text-white font-bold text-sm transition-all border border-white/10">
                                Gestionar Suscripción
                            </button>
                        </div>
                    </div>
                </motion.div>
            </div>
        </div>
    );
}
