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
            <div className="flex min-h-screen">
                <Sidebar />
                <main className="flex-1 ml-[280px] min-h-screen flex flex-col transition-all duration-300 relative z-10">
                    <div className="flex-1 p-8">
                        {children}
                    </div>
                    <LegalFooter />
                </main>
                <SupportChatWidget />
            </div>
        </>
    );
}
