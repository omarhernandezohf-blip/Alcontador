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
        // Mock Authentication Logic
        await new Promise(resolve => setTimeout(resolve, 1000)); // Simulate API
        try {
            const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
            const res = await fetch(`${API_URL}/api/auth/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password: pass })
            });

            if (!res.ok) {
                console.error("Login failed: Invalid credentials or server error");
                return false;
            }

            const userData = await res.json();
            // Map backend response 'plan' (uppercase) to frontend type (lowercase) if needed
            const user: User = {
                ...userData,
                plan: userData.plan.toLowerCase() as PlanType
            };

            setUser(user);
            localStorage.setItem('ac_user', JSON.stringify(user));
            router.push('/dashboard');
            return true;
        } catch (error) {
            console.error("Login Connection Error:", error);
            return false;
        }
    };

    const loginWithGoogle = async () => {
        // Mock Google Login -> Defaults to Initial Plan for demo
        await new Promise(resolve => setTimeout(resolve, 1500));
        const mockUser: User = {
            email: 'google.user@gmail.com',
            name: 'Google User',
            plan: 'inicial',
            avatar: 'https://lh3.googleusercontent.com/a/default-user=s96-c'
        };
        setUser(mockUser);
        localStorage.setItem('ac_user', JSON.stringify(mockUser));
        router.push('/dashboard');
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
