import { NextResponse } from 'next/server';

export async function POST(req: Request) {
    try {
        const body = await req.json();
        const { message } = body;

        // Aquí se conectaría con lógica real o backend en el futuro.
        // Por ahora simulamos una respuesta inteligente básica o "mock" 
        // para dar feedback inmediato al usuario.

        let reply = "¡Entendido! Me parece un punto importante. ¿Podrías darme un poco más de contexto para orientarte con la precisión que necesitas?";

        const lowerMsg = message.toLowerCase();

        if (lowerMsg.includes('ugpp')) {
            reply = "Claro, la UGPP es un tema delicado. Te cuento: aquí analizamos específicamente la regla 60/40 de la Ley 1393. Si notas que el riesgo sale 'Alto', suele ser porque los bonos o auxilios están superando el 40% del total devengado. ¿Quieres que revisemos algún empleado en específico?";
        } else if (lowerMsg.includes('nomina') || lowerMsg.includes('nómina')) {
            reply = "Con gusto. En el módulo de Nómina me encargo de validar que las prestaciones y la seguridad social cuadren al centavo. Si tienes dudas con algún cálculo, recuerda que siempre validamos contra los porcentajes de ley vigentes. ¿Estás intentando cargar un plano o es una liquidación individual?";
        } else if (lowerMsg.includes('dian') || lowerMsg.includes('exogena')) {
            reply = "Entiendo perfectamente. Los cruces de la DIAN a veces nos dan dolores de cabeza por diferencias mínimas. Aquí cruzamos tu contabilidad contra la 'Información Reportada por Terceros'. Normalmente, las diferencias son por NITs mal digitados o pagos que quedaron en un periodo diferente. ¿Te ayudo a interpretar algún hallazgo?";
        } else if (lowerMsg.includes('fiscal') || lowerMsg.includes('bancarizacion')) {
            reply = "Muy buen punto. En Auditoría Fiscal mi prioridad es blindarte contra el Art. 771-5 (Bancarización). Ojo con los pagos en efectivo grandes, porque la DIAN los desconoce de una. Si ves alertas rojas en el reporte, te sugiero priorizar esos soportes. ¿Necesitas el formato de certificación?";
        } else if (lowerMsg.includes('hola') || lowerMsg.includes('buenos dias')) {
            reply = "¡Hola! Qué gusto saludarte. Aquí estoy pendiente para echarte una mano en lo que necesites. ¿Cómo va esa contabilidad hoy?";
        } else if (lowerMsg.includes('gracias')) {
            reply = "¡Con todo el gusto! Para eso estamos, colega. Cualquier otra cosa, aquí sigo pendiente. 👍";
        }

        // Simular delay de red
        await new Promise(resolve => setTimeout(resolve, 1000));

        return NextResponse.json({ reply });
    } catch (error) {
        return NextResponse.json(
            { error: 'Error processing request' },
            { status: 500 }
        );
    }
}
