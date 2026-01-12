'use client';

import { useState } from 'react';
import Link from 'next/link';
import { LegalModal } from '@/components/ui/LegalModal';

export function LegalFooter() {
    const [modalOpen, setModalOpen] = useState(false);
    const [currentPolicy, setCurrentPolicy] = useState<{ title: string; content: React.ReactNode } | null>(null);

    const legalContent = {
        terminos: {
            title: "Términos de Uso",
            content: (
                <div className="space-y-4">
                    <p>Bienvenido al Asistente Contable Pro. Al utilizar nuestro software, aceptas cumplir con los siguientes términos y condiciones de uso.</p>

                    <h3 className="font-bold text-white">1. Propósito de la Herramienta</h3>
                    <p>Este software es una herramienta de <strong>apoyo tecnológico</strong> diseñada para facilitar cálculos, proyecciones y auditorías preliminares. NO constituye asesoramiento legal, contable ni fiscal vinculante.</p>

                    <h3 className="font-bold text-white">2. Responsabilidad del Usuario</h3>
                    <p>El usuario (profesional contable o empresa) es el <strong>único responsable</strong> de la validación final de los datos y del cumplimiento de las obligaciones tributarias ante entidades como la DIAN, UGPP u otras autoridades.</p>

                    <h3 className="font-bold text-white">3. Limitación de Responsabilidad</h3>
                    <p>Asistente Contable Pro S.A.S. no se hace responsable por multas, sanciones, errores en declaraciones o pérdidas financieras derivadas del uso de esta herramienta. El software se proporciona "tal cual", sin garantías expresas sobre la exactitud absoluta de las proyecciones futuras.</p>

                    <h3 className="font-bold text-white">4. Propiedad Intelectual</h3>
                    <p>El código fuente, algoritmos, diseño "Legendary" y la marca son propiedad exclusiva de la empresa. Queda prohibida la ingeniería inversa o redistribución no autorizada.</p>
                </div>
            )
        },
        privacidad: {
            title: "Política de Privacidad",
            content: (
                <div className="space-y-4">
                    <p>Valoramos su privacidad y nos comprometemos a proteger sus datos financieros y personales.</p>

                    <h3 className="font-bold text-white">1. Recolección de Datos</h3>
                    <p>Recopilamos únicamente la información necesaria para la operación del servicio: datos de facturación, NITs para validación y archivos cargados temporalmente para su procesamiento.</p>

                    <h3 className="font-bold text-white">2. Uso de la Información</h3>
                    <p>Los archivos cargados (XML, Excel) se procesan en memoria y <strong>no se almacenan permanentemente</strong> en nuestros servidores salvo solicitud expresa de "Backup en la Nube". Se utilizan exclusivamente para generar los reportes solicitados.</p>

                    <h3 className="font-bold text-white">3. Seguridad</h3>
                    <p>Utilizamos encriptación de grado bancario (AES-256) en tránsito y en reposo para proteger su información corporativa.</p>
                </div>
            )
        },
        tratamiento: {
            title: "Tratamiento de Datos Personales",
            content: (
                <div className="space-y-4">
                    <p>En cumplimiento de la <strong>Ley 1581 de 2012</strong> (Ley de Habeas Data) y decretos reglamentarios de Colombia:</p>

                    <h3 className="font-bold text-white">1. Autorización</h3>
                    <p>Al registrarse, usted autoriza el tratamiento de sus datos para fines administrativos, comerciales y de soporte técnico relacionados con el servicio.</p>

                    <h3 className="font-bold text-white">2. Derechos del Titular</h3>
                    <p>Usted tiene derecho a conocer, actualizar, rectificar y suprimir sus datos personales de nuestras bases de datos en cualquier momento.</p>

                    <h3 className="font-bold text-white">3. Oficial de Privacidad</h3>
                    <p>Para ejercer sus derechos, puede contactar a nuestro oficial de privacidad a través del chat de soporte o al correo legal@asistentecontable.pro.</p>
                </div>
            )
        }
    };

    const openLegal = (type: keyof typeof legalContent) => {
        setCurrentPolicy(legalContent[type]);
        setModalOpen(true);
    };

    return (
        <>
            <footer className="w-full py-8 px-8 border-t border-white/5 bg-slate-950/50 mt-12 relative z-30">
                <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-6">

                    <div className="text-center md:text-left">
                        <p className="text-sm text-slate-500">
                            &copy; 2026 Asistente Contable Pro S.A.S. Todos los derechos reservados.
                        </p>
                        <p className="text-xs text-slate-600 mt-2 max-w-md">
                            * Advertencia Legal: Este software actúa como una herramienta de asistencia y cálculo. La validación final y cumplimiento de obligaciones tributarias es responsabilidad exclusiva del profesional contable. No, reemplaza el criterio experto.
                        </p>
                    </div>

                    <div className="flex gap-6 text-sm text-slate-400">
                        <button onClick={() => openLegal('terminos')} className="hover:text-indigo-400 transition-colors">Términos de Uso</button>
                        <button onClick={() => openLegal('privacidad')} className="hover:text-indigo-400 transition-colors">Política de Privacidad</button>
                        <button onClick={() => openLegal('tratamiento')} className="hover:text-indigo-400 transition-colors">Tratamiento de Datos</button>
                    </div>

                </div>
            </footer>

            {currentPolicy && (
                <LegalModal
                    isOpen={modalOpen}
                    onClose={() => setModalOpen(false)}
                    title={currentPolicy.title}
                    content={currentPolicy.content}
                />
            )}
        </>
    );
}
