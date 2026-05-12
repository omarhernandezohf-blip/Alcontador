'use client';

import { useAuth } from "@/context/AuthContext";
import { Sidebar } from "./Sidebar";
import { SupportChatWidget } from "@/components/tools/SupportChatWidget";
import { LegalFooter } from "@/components/layout/LegalFooter";
import { StarsBackground } from "@/components/ui/StarsBackground";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";

export function AuthGuard({ children }: { children: React.ReactNode }) {
    const { isAuthenticated, user } = useAuth();
    const pathname = usePathname();
    const [mounted, setMounted] = useState(false);
    const [isMobileOpen, setIsMobileOpen] = useState(false);

    useEffect(() => {
        setMounted(true);
    }, []);

    // PRIORITY: Always show login page immediately
    // Accepting hydration mismatch risk to ensure UI visibility
    if (pathname?.includes('/login')) {
        return <>{children}</>;
    }

    // Prevent hydration mismatch for protected routes
    if (!mounted) {
        return (
            <div className="min-h-screen bg-slate-950 flex flex-col items-center justify-center gap-4">
                <div className="w-8 h-8 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin"></div>
                <p className="text-sm text-slate-500 font-medium">Verificando Credenciales...</p>
            </div>
        );
    }

    if (!isAuthenticated) {
        return null; // AuthContext handles redirect
    }

    return (
        <>
            <StarsBackground />
            <div className="flex min-h-screen relative">

                {/* Mobile Header / Hamburger */}
                <div className="md:hidden fixed top-0 left-0 right-0 h-16 bg-slate-900/80 backdrop-blur-md border-b border-white/10 z-30 flex items-center px-4 justify-between">
                    <button
                        onClick={() => setIsMobileOpen(true)}
                        className="p-2 -ml-2 text-white hover:bg-white/5 rounded-lg"
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="4" x2="20" y1="12" y2="12" /><line x1="4" x2="20" y1="6" y2="6" /><line x1="4" x2="20" y1="18" y2="18" /></svg>
                    </button>
                    <span className="font-bold text-white">Asistente Pro</span>
                    <div className="w-8" /> {/* Spacer for centering */}
                </div>

                <Sidebar isMobileOpen={isMobileOpen} onCloseMobile={() => setIsMobileOpen(false)} />

                {/* Main Content: ml-0 on mobile, ml-280 on desktop. Added pt-16 for mobile header space */}
                <main className="flex-1 w-full ml-0 md:ml-[280px] min-h-screen flex flex-col transition-all duration-300 relative z-10 pt-16 md:pt-0">
                    <div className="flex-1 p-4 md:p-8 overflow-x-hidden">
                        {children}
                    </div>
                    <LegalFooter />
                </main>
                <SupportChatWidget />
            </div>
        </>
    );
}
