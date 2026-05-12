// Centralized API URL configuration
// This ensures that production builds (Vercel) automatically point to Render
// while local development continues to work with localhost.

const getApiUrl = () => {
    // 1. Priority: Environment Variable (set in Vercel or .env.local)
    if (process.env.NEXT_PUBLIC_API_URL) {
        return process.env.NEXT_PUBLIC_API_URL;
    }

    // 2. Production Fallback (When deployed on Vercel but env var missing)
    if (process.env.NODE_ENV === 'production') {
        return 'https://alcontador.onrender.com';
    }

    // 3. Local Development Fallback
    return 'http://localhost:8000';
};

export const API_URL = getApiUrl();

export async function consultAI(prompt: string, userPlan: string = 'FREE', email?: string) {
    try {
        const response = await fetch(`${API_URL}/api/ai/consult`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                prompt,
                user_plan: userPlan,
                email,
            }),
        });

        if (!response.ok) {
            throw new Error(`API Error: ${response.statusText}`);
        }

        const data = await response.json();
        return data.response;
    } catch (error) {
        console.error("AI Service Error:", error);
        return "Lo siento, hubo un error de conexión con el servidor.";
    }
}
