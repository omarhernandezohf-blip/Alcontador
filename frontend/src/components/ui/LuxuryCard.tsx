'use client';

import { motion, useMotionValue, useSpring, useTransform, HTMLMotionProps } from 'framer-motion';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';
import React, { useRef } from 'react';

interface LuxuryCardProps extends HTMLMotionProps<"div"> {
    children: React.ReactNode;
    featured?: boolean;
}

export function LuxuryCard({ children, className, featured, ...props }: LuxuryCardProps) {
    const ref = useRef<HTMLDivElement>(null);

    const x = useMotionValue(0);
    const y = useMotionValue(0);

    const mouseX = useSpring(x, { stiffness: 500, damping: 100 });
    const mouseY = useSpring(y, { stiffness: 500, damping: 100 });

    const rotateX = useTransform(mouseY, [-0.5, 0.5], ["7deg", "-7deg"]);
    const rotateY = useTransform(mouseX, [-0.5, 0.5], ["-7deg", "7deg"]);

    const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
        if (!ref.current) return;

        const rect = ref.current.getBoundingClientRect();

        const width = rect.width;
        const height = rect.height;

        const mouseXFromCenter = e.clientX - rect.left - width / 2;
        const mouseYFromCenter = e.clientY - rect.top - height / 2;

        const xPct = mouseXFromCenter / width;
        const yPct = mouseYFromCenter / height;

        x.set(xPct);
        y.set(yPct);
    };

    const handleMouseLeave = () => {
        x.set(0);
        y.set(0);
    };

    return (
        <motion.div
            ref={ref}
            onMouseMove={handleMouseMove}
            onMouseLeave={handleMouseLeave}
            style={{
                rotateX,
                rotateY,
                transformStyle: "preserve-3d",
            }}
            className={twMerge(
                "relative transition-all duration-200 ease-out",
                featured ? "col-span-1 md:col-span-2 row-span-2" : "",
                className
            )}
            {...props}
        >
            <div className="absolute inset-0 rounded-2xl bg-gradient-to-br from-white/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none"
                style={{ transform: "translateZ(20px)" }}
            />

            <div className={clsx(
                "relative h-full w-full rounded-2xl border border-white/5 bg-slate-900/40 backdrop-blur-xl p-6 shadow-2xl",
                "group hover:shadow-[0_0_30px_rgba(79,70,229,0.15)] transition-shadow duration-300",
                featured ? "bg-gradient-to-br from-slate-900/60 to-indigo-950/20" : ""
            )}>
                {/* Glossy Overlay */}
                <div className="absolute inset-0 rounded-2xl bg-gradient-to-br from-white/5 via-transparent to-transparent opacity-50 pointer-events-none" />

                {/* Content Container with slight Z-lift for depth */}
                <div style={{ transform: "translateZ(30px)" }} className="relative z-10 h-full flex flex-col">
                    {children}
                </div>
            </div>
        </motion.div>
    );
}
