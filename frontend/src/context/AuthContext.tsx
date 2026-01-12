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
    credits?: number;
    subscriptionEnd?: string; // ISO Date string
}

interface AuthContextType {
    user: User | null;
    isAuthenticated: boolean;
    login: (email: string, pass: string) => Promise<boolean>;
    loginWithGoogle: () => Promise<void>;
    logout: () => void;
    checkPermission: (feature: string) => boolean;
    updateUser: (data: Partial<User>) => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
    const [user, setUser] = useState<User | null>(null);
    const router = useRouter();
    const pathname = usePathname();

    // Helper to get mock subscription date
    const getMockSubscriptionEnd = () => {
        const date = new Date();
        date.setDate(date.getDate() + 30);
        return date.toISOString();
    };

    // Helper to load persistent user data from "local database"
    const loadFromLocalDB = (email: string) => {
        try {
            const db = localStorage.getItem('ac_users_db');
            if (db) {
                const parsedDB = JSON.parse(db);
                return parsedDB[email] || {};
            }
        } catch (e) {
            console.error("Error reading local DB", e);
        }
        return {};
    };

    // Helper to save persistent user data to "local database"
    const saveToLocalDB = (email: string, data: Partial<User>) => {
        try {
            const dbStr = localStorage.getItem('ac_users_db');
            const db = dbStr ? JSON.parse(dbStr) : {};

            // Merge existing data for this user with new data
            db[email] = { ...(db[email] || {}), ...data };

            localStorage.setItem('ac_users_db', JSON.stringify(db));
        } catch (e) {
            console.error("Error saving to local DB", e);
        }
    };

    // Check for existing session on mount
    useEffect(() => {
        const storedUser = localStorage.getItem('ac_user');
        if (storedUser) {
            const parsedUser = JSON.parse(storedUser);
            // Ensure we have the latest persisted data
            const persistedData = loadFromLocalDB(parsedUser.email);
            setUser({ ...parsedUser, ...persistedData });
        } else if (!pathname.includes('/login')) {
            router.push('/login');
        }
    }, []);

    const updateUser = (data: Partial<User>) => {
        if (!user) return;
        const updatedUser = { ...user, ...data };
        setUser(updatedUser);

        try {
            // 1. Update active session
            localStorage.setItem('ac_user', JSON.stringify(updatedUser));

            // 2. Update persistent storage (Avatar, Name, etc)
            // We only persist fields that are meant to be editable by user
            const persistentFields: Partial<User> = {};
            if (data.name) persistentFields.name = data.name;
            if (data.avatar) persistentFields.avatar = data.avatar;

            if (Object.keys(persistentFields).length > 0) {
                saveToLocalDB(user.email, persistentFields);
            }
        } catch (error) {
            console.error("Error saving to localStorage:", error);
        }
    };

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

            // Load any persistent edits for this user
            const persistedData = loadFromLocalDB(email);

            const user: User = {
                ...userData,
                plan: userData.plan.toLowerCase() as PlanType,
                subscriptionEnd: getMockSubscriptionEnd(),
                ...persistedData // Overwrite mock data with saved user edits
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
        console.log("GOOGLE AUTH STARTING..."); // Force Deploy Check
        try {
            // Import dynamically to avoid SSR issues if needed, or rely on top-level imports
            const { GoogleAuthProvider, signInWithPopup } = await import("firebase/auth");
            const { auth } = await import("@/lib/firebase");

            const provider = new GoogleAuthProvider();
            const result = await signInWithPopup(auth, provider);
            const firebaseUser = result.user;
            const email = firebaseUser.email || "";

            // Load any persistent edits for this user
            const persistedData = loadFromLocalDB(email);

            // Map Firebase user to App User
            const user: User = {
                email: email,
                name: firebaseUser.displayName || "Usuario Google",
                plan: 'inicial', // Default plan for new Google users
                avatar: firebaseUser.photoURL || undefined,
                multiSession: true,
                credits: 5, // Default credits for free plan
                subscriptionEnd: getMockSubscriptionEnd(),
                ...persistedData // Overwrite mock data with saved user edits (e.g. if they changed avatar locally)
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
        // We only clear the SESSION, not the persistent DB
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
        <AuthContext.Provider value={{ user, isAuthenticated: !!user, login, loginWithGoogle, logout, checkPermission, updateUser }}>
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
