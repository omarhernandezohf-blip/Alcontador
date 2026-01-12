'use client';

import { useState, useRef, useEffect } from 'react';
import { MessageSquare, X, Send, UserCircle2, User, Loader2, Minimize2, Sparkles } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { usePathname } from 'next/navigation';

interface Message {
    id: string;
    role: 'user' | 'assistant';
    content: string;
    timestamp: Date;
}

export function SupportChatWidget() {
    const [isOpen, setIsOpen] = useState(false);
    const [messages, setMessages] = useState<Message[]>([
        {
            id: '1',
            role: 'assistant',
            content: '¡Hola! 👋 Soy Sofía, tu contadora senior de soporte. Veo que estás trabajando en la plataforma. ¿En qué puedo apoyarte para que tu cierre sea exitoso hoy?',
            timestamp: new Date()
        }
    ]);
    const [inputValue, setInputValue] = useState('');
    const [isTyping, setIsTyping] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);
    const pathname = usePathname();

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages, isOpen]);

    const handleSendMessage = async () => {
        if (!inputValue.trim()) return;

        const newUserMessage: Message = {
            id: Date.now().toString(),
            role: 'user',
            content: inputValue,
            timestamp: new Date()
        };

        setMessages(prev => [...prev, newUserMessage]);
        setInputValue('');
        setIsTyping(true);

        try {
            // Context aware prompt
            const context = `Usuario está en la ruta: ${pathname}. Pregunta: ${newUserMessage.content}`;

            const response = await fetch('/api/support-chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: context })
            });

            const data = await response.json();

            const newAiMessage: Message = {
                id: (Date.now() + 1).toString(),
                role: 'assistant',
                content: data.reply || "Lo siento, tuve un problema procesando tu consulta.",
                timestamp: new Date()
            };

            setMessages(prev => [...prev, newAiMessage]);
        } catch (error) {
            console.error('Error sending message:', error);
            const errorMessage: Message = {
                id: (Date.now() + 1).toString(),
                role: 'assistant',
                content: "Lo siento, no pude conectar con el servidor de soporte. Intenta nuevamente.",
                timestamp: new Date()
            };
            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setIsTyping(false);
        }
    };

    const handleKeyPress = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSendMessage();
        }
    };

    return (
        <div className="fixed bottom-6 right-6 z-50 flex flex-col items-end pointer-events-none">
            <AnimatePresence>
                {isOpen && (
                    <motion.div
                        initial={{ opacity: 0, y: 20, scale: 0.95 }}
                        animate={{ opacity: 1, y: 0, scale: 1 }}
                        exit={{ opacity: 0, y: 20, scale: 0.95 }}
                        className="mb-4 w-[380px] max-w-[calc(100vw-48px)] h-[500px] max-h-[calc(100vh-120px)] bg-slate-900/90 backdrop-blur-xl border border-indigo-500/30 rounded-2xl shadow-2xl flex flex-col pointer-events-auto overflow-hidden ring-1 ring-white/10"
                    >
                        <div className="p-4 bg-gradient-to-r from-indigo-600/20 to-purple-600/20 border-b border-white/5 flex items-center justify-between">
                            <div className="flex items-center gap-3">
                                <div className="relative">
                                    <div className="w-10 h-10 rounded-full border-2 border-indigo-500/30 overflow-hidden relative shadow-md shadow-indigo-500/20">
                                        <img 
                                            src="/sofia-avatar.png" 
                                            alt="Sofía Avatar" 
                                            className="w-full h-full object-cover" 
                                        />
                                    </div>
                                    <span className="absolute bottom-0 right-0 w-2.5 h-2.5 bg-emerald-500 border-2 border-slate-900 rounded-full animate-pulse"></span>
                                </div>
                                <div>
                                    <h3 className="font-bold text-white text-sm">Sofía - Soporte Senior</h3>
                                    <p className="text-[10px] text-indigo-300 flex items-center gap-1">
                                        Contadora Pública Certificada
                                    </p>
                                </div>
                            </div>
                            <button
                                onClick={() => setIsOpen(false)}
                                className="p-2 hover:bg-white/5 rounded-lg text-slate-400 hover:text-white transition-colors"
                            >
                                <Minimize2 className="w-4 h-4" />
                            </button>
                        </div>

                        {/* Messages Area */}
                        <div className="flex-1 overflow-y-auto p-4 space-y-4 custom-scrollbar bg-black/20">
                            {messages.map((msg) => (
                                <div
                                    key={msg.id}
                                    className={`flex items-start gap-3 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}
                                >
                                    <div className="flex-shrink-0">
                                        {msg.role === 'user' ? (
                                            <div className="w-8 h-8 rounded-full bg-purple-500/20 border border-purple-500/30 flex items-center justify-center">
                                                <User className="w-4 h-4 text-purple-400" />
                                            </div>
                                        ) : (
                                            <div className="w-8 h-8 rounded-full border border-indigo-500/30 overflow-hidden relative shadow-sm shadow-indigo-500/20">
                                                <img 
                                                    src="/sofia-avatar.png" 
                                                    alt="Sofía" 
                                                    className="w-full h-full object-cover" 
                                                />
                                            </div>
                                        )}
                                    </div>
                                    <div className={`max-w-[85%] p-4 rounded-2xl text-sm shadow-sm ${msg.role === 'user'
                                            ? 'bg-purple-600/20 text-purple-100 rounded-br-sm border border-purple-500/20'
                                            : 'bg-white/10 text-slate-200 rounded-bl-sm border border-white/10'
                                        }`}>
                                        {msg.content}
                                        <div className={`text-[10px] mt-1 opacity-50 ${msg.role === 'user' ? 'text-right' : 'text-left'}`}>
                                            {msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                        </div>
                                    </div>
                                </div>
                            ))}
                            {isTyping && (
                                <div className="flex items-center gap-2 text-slate-400 text-xs ml-12">
                                    <Loader2 className="w-3 h-3 animate-spin" />
                                    Escribiendo...
                                </div>
                            )}
                            <div ref={messagesEndRef} />
                        </div>

                        {/* Input Area */}
                        <div className="p-4 bg-white/5 border-t border-white/10">
                            <div className="relative">
                                <input
                                    type="text"
                                    value={inputValue}
                                    onChange={(e) => setInputValue(e.target.value)}
                                    onKeyDown={handleKeyPress}
                                    placeholder="Pregúntale a Sofía..."
                                    className="w-full bg-slate-900/50 border border-white/10 rounded-xl py-3 pl-4 pr-12 text-sm text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500/50 transition-all font-light"
                                />
                                <button
                                    onClick={handleSendMessage}
                                    disabled={!inputValue.trim()}
                                    className="absolute right-2 top-1/2 -translate-y-1/2 p-1.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg disabled:opacity-50 disabled:hover:bg-indigo-600 transition-colors"
                                >
                                    <Send className="w-4 h-4" />
                                </button>
                            </div>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>

            <button
                onClick={() => setIsOpen(!isOpen)}
                className="group pointer-events-auto relative flex items-center justify-center w-14 h-14 rounded-full bg-gradient-to-r from-indigo-600 to-purple-600 shadow-lg shadow-indigo-600/30 hover:shadow-indigo-600/50 hover:scale-105 transition-all duration-300 ring-2 ring-white/20"
            >
                <div className="absolute inset-0 rounded-full bg-white/20 animate-ping opacity-0 group-hover:opacity-100 duration-1000" />
                <AnimatePresence mode="wait">
                    {isOpen ? (
                        <X className="w-6 h-6 text-white" />
                    ) : (
                        <MessageSquare className="w-6 h-6 text-white" />
                    )}
                </AnimatePresence>

                {!isOpen && (
                    <span className="absolute -top-1 -right-1 w-3 h-3 bg-red-500 rounded-full border-2 border-slate-900" />
                )}
            </button>
        </div>
    );
}
