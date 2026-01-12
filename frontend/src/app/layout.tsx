import type { Metadata } from "next";
import { Inter, Space_Grotesk } from "next/font/google";
import "./globals.css";
import { Sidebar } from "@/components/layout/Sidebar";
import { StarsBackground } from "@/components/ui/StarsBackground";
import { clsx } from "clsx";

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });
const spaceGrotesk = Space_Grotesk({ subsets: ["latin"], variable: "--font-space" });

export const metadata: Metadata = {
  title: "Asistente Contable Pro",
  description: "Suite Empresarial de Inteligencia Financiera",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es">
      <body className={clsx(inter.variable, spaceGrotesk.variable, "antialiased bg-slate-950 text-slate-100")}>
        <StarsBackground />
        <div className="flex min-h-screen">
          <Sidebar />
          <main className="flex-1 ml-[280px] p-8 transition-all duration-300 relative z-10">
            {children}
          </main>
        </div>
      </body>
    </html>
  );
}
