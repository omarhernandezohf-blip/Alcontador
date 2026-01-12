'use client';

import { useState, useEffect, useRef } from 'react';
import { motion, useScroll, useTransform, useSpring, useMotionValue, useMotionTemplate } from 'framer-motion';
import { useRouter } from 'next/navigation';
import { StarsBackground } from '@/components/ui/StarsBackground';
import { ArrowRight, ShieldCheck, Brain, FileSpreadsheet, Zap, Lock, Globe } from 'lucide-react';
import Link from 'next/link';
import Image from 'next/image';

export default function LandingPage() {
  const router = useRouter();
  const mouseY = useMotionValue(0);
  const mouseX = useMotionValue(0);

  // Smooth mouse movement for spotlight
  const springX = useSpring(mouseX, { stiffness: 50, damping: 20 });
  const springY = useSpring(mouseY, { stiffness: 50, damping: 20 });

  // Background gradient follows mouse
  const background = useMotionTemplate`radial-gradient(
        650px circle at ${springX}px ${springY}px,
        rgba(79, 70, 229, 0.15),
        transparent 80%
    )`;

  const handleMouseMove = ({ currentTarget, clientX, clientY }: React.MouseEvent) => {
    const { left, top } = currentTarget.getBoundingClientRect();
    mouseX.set(clientX - left);
    mouseY.set(clientY - top);
  };

  return (
    <div
      className="min-h-screen w-full bg-slate-950 relative overflow-x-hidden selection:bg-indigo-500/30 selection:text-indigo-200"
      onMouseMove={handleMouseMove}
    >
      <StarsBackground />

      {/* Mouse Spotlight */}
      <motion.div
        className="pointer-events-none absolute inset-0 z-0 transition-opacity duration-300"
        style={{ background }}
      />

      {/* Navbar */}
      <nav className="fixed top-0 w-full z-50 border-b border-white/5 bg-slate-950/50 backdrop-blur-md">
        <div className="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center shadow-lg shadow-indigo-500/20">
              <Brain className="w-6 h-6 text-white" />
            </div>
            <span className="text-xl font-bold text-white font-space tracking-tight">Alcontador<span className="text-indigo-400">.AI</span></span>
          </div>
          <div className="flex items-center gap-6">
            <Link href="/login" className="text-sm font-medium text-slate-400 hover:text-white transition-colors">Iniciar Sesión</Link>
            <Link
              href="/dashboard"
              className="bg-white text-slate-900 px-5 py-2.5 rounded-full text-sm font-bold hover:bg-indigo-50 transition-all hover:scale-105 active:scale-95 flex items-center gap-2"
            >
              Lanzar App <Zap className="w-4 h-4 fill-slate-900" />
            </Link>
          </div>
        </div>
      </nav>

      <main className="relative z-10 pt-32 pb-20 px-6">
        <div className="max-w-7xl mx-auto">

          {/* Hero Section */}
          <div className="flex flex-col items-center text-center mb-32">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-900/30 border border-indigo-500/30 text-indigo-300 text-xs font-bold uppercase tracking-widest mb-8"
            >
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-indigo-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-indigo-500"></span>
              </span>
              Sistema V2.0 Disponible
            </motion.div>

            <motion.h1
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.1 }}
              className="text-5xl md:text-8xl font-bold text-white mb-8 tracking-tight font-space max-w-5xl"
            >
              <span className="text-transparent bg-clip-text bg-gradient-to-b from-white via-white to-slate-400">Auditoría Financiera</span>
              <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 via-purple-400 to-rose-400">Impulsada por IA</span>
            </motion.h1>

            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.2 }}
              className="text-lg md:text-xl text-slate-400 max-w-2xl mb-12 leading-relaxed"
            >
              Detecta evasión fiscal, concilia bancos y extrae datos de facturas en segundos.
              La plataforma definitiva para contadores modernos y auditores fiscales.
            </motion.p>

            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ type: "spring", duration: 0.5, delay: 0.4 }}
              className="flex flex-col sm:flex-row gap-4"
            >
              <button
                onClick={() => router.push('/dashboard')}
                className="px-8 py-4 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white rounded-2xl font-bold text-lg shadow-xl shadow-indigo-600/20 transition-all hover:scale-105 active:scale-95 flex items-center gap-3 group"
              >
                Iniciar Análisis Gratuito
                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </button>
              <button className="px-8 py-4 bg-slate-900 border border-white/10 hover:bg-slate-800 text-white rounded-2xl font-bold text-lg transition-all hover:scale-105 active:scale-95 flex items-center gap-3">
                <Globe className="w-5 h-5 text-indigo-400" />
                Ver Demo
              </button>
            </motion.div>
          </div>

          {/* Features Grid */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 relative">
            {/* Decorative Line */}
            <div className="absolute top-1/2 left-0 w-full h-px bg-gradient-to-r from-transparent via-indigo-500/20 to-transparent -z-10 hidden md:block" />

            <FeatureCard
              icon={<ShieldCheck className="w-8 h-8 text-rose-400" />}
              title="Auditoría Anti-Sanciones"
              desc="Cruce automático de Exógena vs Contabilidad para prevenir el Art. 651."
              color="rose"
              delay={0.5}
            />
            <FeatureCard
              icon={<Zap className="w-8 h-8 text-emerald-400" />}
              title="Conciliación Neuronal"
              desc="Nuestro motor de IA empareja transferencias bancarias con una precisión del 99%."
              color="emerald"
              delay={0.6}
            />
            <FeatureCard
              icon={<FileSpreadsheet className="w-8 h-8 text-blue-400" />}
              title="Minería de Datos XML"
              desc="Convierte miles de facturas electrónicas en bases de datos accionables al instante."
              color="blue"
              delay={0.7}
            />
          </div>

          {/* Infinite Text Scroll */}
          <div className="mt-32 overflow-hidden opacity-50">
            <div className="flex whitespace-nowrap animate-marquee">
              {[1, 2, 3, 4].map((i) => (
                <span key={i} className="text-[10rem] font-black text-white/5 mx-8 uppercase font-space">
                  Inteligencia • Velocidad • Precisión •
                </span>
              ))}
            </div>
          </div>

        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-white/5 bg-slate-950 py-12 text-center text-slate-600 text-sm relative z-10">
        <p>© 2026 Alcontador AI Suite. Todos los derechos reservados.</p>
      </footer>
    </div>
  );
}

function FeatureCard({ icon, title, desc, color, delay }: { icon: any, title: string, desc: string, color: string, delay: number }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay, duration: 0.5 }}
      className="group relative p-8 rounded-3xl bg-slate-900/40 border border-white/5 hover:border-white/10 transition-all hover:bg-slate-900/60 backdrop-blur-sm"
    >
      <div className={`absolute inset-0 bg-gradient-to-br from-${color}-500/5 to-transparent rounded-3xl opacity-0 group-hover:opacity-100 transition-opacity duration-500`} />

      <div className="relative z-10">
        <div className={`w-14 h-14 rounded-2xl bg-${color}-500/10 border border-${color}-500/20 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300`}>
          {icon}
        </div>
        <h3 className="text-xl font-bold text-white mb-3 group-hover:text-indigo-200 transition-colors">{title}</h3>
        <p className="text-slate-400 leading-relaxed text-sm">
          {desc}
        </p>
        <div className="mt-6 flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-slate-500 group-hover:text-white transition-colors">
          Explorar <ArrowRight className="w-4 h-4" />
        </div>
      </div>
    </motion.div>
  );
}
