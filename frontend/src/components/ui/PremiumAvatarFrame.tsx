import { motion } from 'framer-motion';
import { User, Camera, Sparkles, Crown, Zap } from 'lucide-react';
import { clsx } from 'clsx';

interface PremiumAvatarFrameProps {
    avatarUrl?: string;
    userName?: string;
    plan: string;
    isProcessing?: boolean;
    onCameraClick?: () => void;
    size?: 'sm' | 'md' | 'lg' | 'xl';
}

export const PremiumAvatarFrame = ({
    avatarUrl,
    userName,
    plan = 'free',
    isProcessing = false,
    onCameraClick,
    size = 'xl'
}: PremiumAvatarFrameProps) => {

    const isPremium = plan === 'premium' || plan === 'platinum';
    const isPro = plan === 'pro';

    // Size mapping
    const sizeClasses = {
        sm: 'w-10 h-10',
        md: 'w-16 h-16',
        lg: 'w-24 h-24',
        xl: 'w-36 h-36'
    };

    const containerSize = sizeClasses[size];

    // --- FREE PLAN (Basic) ---
    if (!isPremium && !isPro) {
        return (
            <div className={`relative group/avatar ${containerSize}`}>
                <div className="w-full h-full rounded-full bg-slate-800 border-2 border-slate-700 overflow-hidden shadow-lg relative">
                    {isProcessing ? (
                        <div className="w-full h-full flex items-center justify-center bg-slate-900/80">
                            <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-slate-400"></div>
                        </div>
                    ) : avatarUrl ? (
                        <img src={avatarUrl} alt={userName} className="w-full h-full object-cover" />
                    ) : (
                        <div className="w-full h-full flex items-center justify-center bg-slate-700/50 text-slate-400">
                            <User className="w-1/2 h-1/2" />
                        </div>
                    )}
                </div>
                {onCameraClick && (
                    <button
                        onClick={onCameraClick}
                        className="absolute bottom-0 right-0 p-2 rounded-full bg-slate-700 text-white shadow-md hover:bg-slate-600 transition-colors border border-slate-900 z-20"
                        disabled={isProcessing}
                    >
                        <Camera className="w-3 h-3" />
                    </button>
                )}
            </div>
        );
    }

    // --- PRO PLAN (Professional Blue/Cyan) ---
    if (isPro) {
        return (
            <div className={`relative group/avatar ${containerSize} flex items-center justify-center my-6`}>

                {/* Pro Glow */}
                <div className="absolute inset-[-10%] rounded-full bg-blue-500/10 blur-xl" />

                {/* Single Tech Ring */}
                <motion.div
                    animate={{ rotate: 360 }}
                    transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
                    className="absolute inset-[-5%] rounded-full border-[1px] border-blue-500/30 border-t-cyan-400/50 border-transparent shadow-[0_0_10px_rgba(56,189,248,0.2)]"
                />

                {/* Main Avatar Container */}
                <div className="w-full h-full rounded-full p-[2px] bg-gradient-to-br from-blue-500 to-cyan-400 shadow-xl relative z-10">
                    <div className="w-full h-full rounded-full bg-slate-950 border-[2px] border-slate-900 overflow-hidden relative">
                        {isProcessing ? (
                            <div className="w-full h-full flex items-center justify-center bg-slate-950/90 backdrop-blur-sm">
                                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-cyan-400"></div>
                            </div>
                        ) : avatarUrl ? (
                            <img src={avatarUrl} alt={userName} className="w-full h-full object-cover transition-transform duration-500 group-hover/avatar:scale-105" />
                        ) : (
                            <div className="w-full h-full flex items-center justify-center bg-gradient-to-br from-slate-900 to-slate-800 text-blue-300/50">
                                <User className="w-1/2 h-1/2" />
                            </div>
                        )}
                    </div>
                </div>

                {/* Camera Button PRO */}
                {onCameraClick && (
                    <button
                        onClick={onCameraClick}
                        className="absolute bottom-1 right-1 p-2 rounded-full bg-slate-800 text-cyan-400 shadow-lg border border-cyan-500/30 hover:bg-slate-700 transition-all z-20"
                        disabled={isProcessing}
                    >
                        <Camera className="w-3.5 h-3.5" />
                    </button>
                )}

                {/* PRO Badge */}
                <div className="absolute -bottom-6 cursor-default z-30">
                    <span className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-slate-900/90 border border-blue-500/30 text-[10px] font-bold text-cyan-400 shadow-lg backdrop-blur-md uppercase tracking-wider">
                        <Zap className="w-3 h-3 text-cyan-400" />
                        Edición Pro
                    </span>
                </div>
            </div>
        );
    }

    // --- PREMIUM PLAN (Luxury Gold/Amber) ---
    return (
        <div className={`relative group/avatar ${containerSize} flex items-center justify-center my-6`}>

            {/* 1. Ambient God-Ray Glow */}
            <div className="absolute inset-[-30%] rounded-full bg-gradient-to-tr from-indigo-500/20 via-purple-500/10 to-amber-500/5 blur-2xl animate-pulse" />

            {/* 2. Slow Rotating Elegant Ring */}
            <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 30, repeat: Infinity, ease: "linear" }}
                className="absolute inset-[-12%] rounded-full border-[1px] border-indigo-500/30 border-t-indigo-300/60 border-b-transparent border-l-transparent shadow-[0_0_15px_rgba(99,102,241,0.2)]"
            />

            {/* 3. Fast Counter-Rotating Detail Ring */}
            <motion.div
                animate={{ rotate: -360 }}
                transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
                className="absolute inset-[-6%] rounded-full border-[1px] border-purple-500/20 border-b-purple-300/60 border-t-transparent border-r-transparent dashed-border"
            />

            {/* 4. Luxury Particles */}
            <motion.div
                className="absolute w-[140%] h-[140%]"
                animate={{ rotate: 360 }}
                transition={{ duration: 15, repeat: Infinity, ease: "linear" }}
            >
                <div className="absolute top-0 left-1/2 -translate-x-1/2 w-1.5 h-1.5 bg-cyan-200 rounded-full shadow-[0_0_8px_2px_rgba(165,243,252,0.8)]" />
                <div className="absolute bottom-[20%] right-[20%] w-1 h-1 bg-amber-300 rounded-full shadow-[0_0_8px_1px_rgba(252,211,77,0.6)]" />
            </motion.div>

            {/* 5. Main Image Container with Glass Border */}
            <div className="w-full h-full rounded-full p-[3px] bg-gradient-to-br from-indigo-400 via-purple-400 to-amber-400 shadow-2xl relative z-10">
                <div className="w-full h-full rounded-full bg-slate-950 border-[2px] border-slate-900 overflow-hidden relative">
                    {isProcessing ? (
                        <div className="w-full h-full flex items-center justify-center bg-slate-950/90 backdrop-blur-sm">
                            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-400 shadow-[0_0_15px_rgba(99,102,241,0.5)]"></div>
                        </div>
                    ) : avatarUrl ? (
                        <img src={avatarUrl} alt={userName} className="w-full h-full object-cover transition-transform duration-700 group-hover/avatar:scale-105" />
                    ) : (
                        <div className="w-full h-full flex items-center justify-center bg-gradient-to-br from-slate-900 to-slate-950 text-indigo-300/50">
                            <User className="w-1/2 h-1/2" />
                        </div>
                    )}

                    {/* Inner Shine Effect */}
                    <div className="absolute inset-0 rounded-full ring-1 ring-inset ring-white/10" />
                    <div className="absolute -top-[50%] -left-[50%] w-[200%] h-[200%] bg-gradient-to-br from-white/5 to-transparent rotate-45 pointer-events-none" />
                </div>
            </div>

            {/* 6. Gold-Plated Camera Button */}
            {onCameraClick && (
                <button
                    onClick={onCameraClick}
                    className="absolute bottom-1 right-1 p-2.5 rounded-full bg-gradient-to-r from-slate-900 to-slate-800 text-amber-300 shadow-lg border border-amber-500/30 hover:border-amber-400 hover:text-amber-200 transition-all z-20 group-hover/avatar:scale-110 group-hover/avatar:shadow-[0_0_15px_rgba(251,191,36,0.3)]"
                    disabled={isProcessing}
                >
                    <Camera className="w-4 h-4" />
                </button>
            )}

            {/* 7. The Ultimate Luxury Badge (PREMIUM) */}
            <motion.div
                initial={{ y: 0, opacity: 0.9 }}
                animate={{ y: [0, -3, 0] }}
                transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" }}
                className="absolute -bottom-8 cursor-default z-30"
            >
                <div className="relative">
                    {/* Glow behind badge */}
                    <div className="absolute inset-0 bg-amber-500/20 blur-md rounded-full" />

                    <span className="relative flex items-center gap-2 px-4 py-1.5 rounded-full bg-gradient-to-b from-slate-900/90 to-black/90 border border-amber-500/30 text-[10px] tracking-widest font-black text-transparent bg-clip-text bg-gradient-to-r from-amber-200 via-yellow-100 to-amber-300 shadow-xl backdrop-blur-xl uppercase">
                        <Crown className="w-3 h-3 text-amber-400 fill-amber-400/20" />
                        Edición Premium
                    </span>
                </div>
            </motion.div>
        </div>
    );
};
