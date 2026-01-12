'use client';

import React, { createContext, useContext, useState, useEffect } from 'react';
import { useRouter, usePathname } from 'next/navigation';

export type PlanType = 'inicial' | 'pro' | 'premium';

interface User {
    email: string;
    name: string;
    plan: PlanType;
    avatar?: string;
    multiSession?: boolean;
}

interface AuthContextType {
    user: User | null;
    isAuthenticated: boolean;
    login: (email: string, pass: string) => Promise<boolean>;
    loginWithGoogle: () => Promise<void>;
    logout: () => void;
    checkPermission: (feature: string) => boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
    const [user, setUser] = useState<User | null>(null);
    const router = useRouter();
    const pathname = usePathname();

    // Check for existing session on mount
    useEffect(() => {
        const storedUser = localStorage.getItem('ac_user');
        if (storedUser) {
            setUser(JSON.parse(storedUser));
        } else if (!pathname.includes('/login')) {
            router.push('/login');
        }
    }, []);

    const login = async (email: string, pass: string): Promise<boolean> => {
        try {
            const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
            console.log("Attempting login to:", API_URL); // Debug

            const res = await fetch(`${API_URL}/api/auth/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password: pass })
            });

            if (!res.ok) {
                const errorData = await res.json().catch(() => ({}));
                console.error("Login failed:", res.status, errorData);
                return false;
            }

            const userData = await res.json();

            const user: User = {
                ...userData,
                plan: userData.plan.toLowerCase() as PlanType
            };

            setUser(user);
            localStorage.setItem('ac_user', JSON.stringify(user));
            router.push('/dashboard');
            return true;
        } catch (error) {
            console.error("Login Network Error:", error);
            return false;
        }
    };

    const loginWithGoogle = async () => {
        try {
            // Import dynamically to avoid SSR issues if needed, or rely on top-level imports
            const { GoogleAuthProvider, signInWithPopup } = await import("firebase/auth");
            const { auth } = await import("@/lib/firebase");

            const provider = new GoogleAuthProvider();
            const result = await signInWithPopup(auth, provider);
            const firebaseUser = result.user;

            // Map Firebase user to App User
            // In a real app, you would verify this with your backend here
            const user: User = {
                email: firebaseUser.email || "",
                name: firebaseUser.displayName || "Usuario Google",
                plan: 'inicial', // Default plan for new Google users
                avatar: firebaseUser.photoURL || undefined,
                multiSession: true
            };

            setUser(user);
            localStorage.setItem('ac_user', JSON.stringify(user));
            router.push('/dashboard');
        } catch (error) {
            console.error("Google Login Error:", error);
            // Optional: Notify user of error
        }
    };

    const logout = () => {
        setUser(null);
        localStorage.removeItem('ac_user');
        router.push('/login');
    };

    const checkPermission = (feature: string): boolean => {
        if (!user) return false;

        switch (feature) {
            case 'ai_unlimited':
                return user.plan === 'premium';
            case 'advanced_audit':
                return user.plan === 'pro' || user.plan === 'premium';
            case 'financial_planning':
                return true; // All plans
            default:
                return true;
        }
    };

    return (
        <AuthContext.Provider value={{ user, isAuthenticated: !!user, login, loginWithGoogle, logout, checkPermission }}>
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
}
