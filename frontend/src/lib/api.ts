const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

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
