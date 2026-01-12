import { initializeApp, getApps, getApp } from "firebase/app";
import { getAnalytics, isSupported } from "firebase/analytics";
import { getFirestore } from "firebase/firestore";
import { getAuth } from "firebase/auth";

const firebaseConfig = {
    apiKey: "AIzaSyAp9XvGI9KumaUj2cPy4Oib0V-Fr_DAvpU",
    authDomain: "asistentecontable-481806.firebaseapp.com",
    projectId: "asistentecontable-481806",
    storageBucket: "asistentecontable-481806.firebasestorage.app",
    messagingSenderId: "247872611020",
    appId: "1:247872611020:web:f6e32844706b996c975869",
    measurementId: "G-TVZ1GLG2KZ"
};

console.log("Firebase Config Debug:", {
    apiKey: firebaseConfig.apiKey ? "********" : "MISSING",
    projectId: firebaseConfig.projectId,
    authDomain: firebaseConfig.authDomain
});

// Initialize Firebase (Singleton pattern)
const app = !getApps().length ? initializeApp(firebaseConfig) : getApp();
const db = getFirestore(app);
const auth = getAuth(app);

// Analytics runs only on client side
let analytics;
if (typeof window !== 'undefined') {
    isSupported().then((supported) => {
        if (supported) {
            analytics = getAnalytics(app);
        }
    });
}

export { app, db, auth, analytics };
