import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

interface GlassCardProps extends React.HTMLAttributes<HTMLDivElement> {
    children: React.ReactNode;
    gradient?: boolean;
}

export function GlassCard({ children, className, gradient, ...props }: GlassCardProps) {
    return (
        <div
            className={twMerge(
                "glass-card p-6 relative overflow-hidden group",
                gradient && "before:absolute before:inset-0 before:bg-gradient-to-br before:from-indigo-500/10 before:to-purple-500/10 before:opacity-0 hover:before:opacity-100 before:transition-opacity",
                className
            )}
            {...props}
        >
            <div className="relative z-10">
                {children}
            </div>
        </div>
    );
}
