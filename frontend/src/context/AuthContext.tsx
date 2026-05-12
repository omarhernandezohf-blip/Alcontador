'use client';

import React, { createContext, useContext, useState, useEffect } from 'react';
import { useRouter, usePathname } from 'next/navigation';
import { API_URL } from '@/lib/api';
import { db } from '@/lib/firebase';
import { doc, getDoc, setDoc, onSnapshot } from 'firebase/firestore';

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
            setUser(parsedUser);

            // Immediately sync with Firestore if we have an email
            if (parsedUser.email) {
                syncWithFirestore(parsedUser.email);
            }
        } else if (!pathname.includes('/login')) {
            router.push('/login');
        }
    }, []);

    // Listen to Firestore changes for specific user data (Avatar, Name, Plan)
    const syncWithFirestore = (email: string) => {
        const userRef = doc(db, 'users', email);

        // Real-time listener for profile updates (cross-device sync)
        const unsubscribe = onSnapshot(userRef, (docSnap) => {
            if (docSnap.exists()) {
                const cloudData = docSnap.data();

                setUser(prev => {
                    if (!prev) return null;

                    // Only update if data actually changed to avoid loop
                    const newAvatar = cloudData.avatar;
                    const newName = cloudData.name;

                    if (prev.avatar !== newAvatar || prev.name !== newName) {
                        const updated = {
                            ...prev,
                            avatar: newAvatar || prev.avatar,
                            name: newName || prev.name
                        };

                        // Update local storage too so it persists offline/refresh
                        localStorage.setItem('ac_user', JSON.stringify(updated));
                        return updated;
                    }
                    return prev;
                });
            }
        }, (error) => {
            console.error("Error syncing with Firestore:", error);
        });

        return unsubscribe;
    };

    const updateUser = async (data: Partial<User>) => {
        if (!user) return;

        // 1. Optimistic Update (Local)
        const updatedUser = { ...user, ...data };
        setUser(updatedUser);
        localStorage.setItem('ac_user', JSON.stringify(updatedUser));

        // 2. Persist to Cloud (Firestore)
        try {
            const userRef = doc(db, 'users', user.email);
            // We only persist specific fields to avoid overwriting auth/credits logic which might be handled by backend
            const persistentData: any = {};
            if (data.avatar !== undefined) persistentData.avatar = data.avatar;
            if (data.name !== undefined) persistentData.name = data.name;

            if (Object.keys(persistentData).length > 0) {
                await setDoc(userRef, persistentData, { merge: true });
                // Also legacy save to local DB just in case
                saveToLocalDB(user.email, persistentData);
            }
        } catch (e) {
            console.error("Error saving to Firestore", e);
        }
    };

    const login = async (email: string, pass: string): Promise<boolean> => {
        try {
            // Robust API URL selection: Centralized
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

            // Start cloud sync
            syncWithFirestore(email);

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

            // Start cloud sync
            syncWithFirestore(email);

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
