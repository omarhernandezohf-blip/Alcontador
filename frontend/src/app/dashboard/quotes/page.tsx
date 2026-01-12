'use client';

import { useState, useEffect } from 'react';
import { FileText, Plus, Trash, Download, Printer } from 'lucide-react';
import { GlassCard } from '@/components/ui/GlassCard';
import { motion } from 'framer-motion';

export default function QuotesPage() {
    const [items, setItems] = useState([{ desc: '', qty: 1, price: 0 }]);
    const [client, setClient] = useState({ name: '', nit: '', address: '' });
    const [invoiceId, setInvoiceId] = useState('0000');

    useEffect(() => {
        setInvoiceId(Math.floor(Math.random() * 10000).toString().padStart(4, '0'));
    }, []);

    const addItem = () => setItems([...items, { desc: '', qty: 1, price: 0 }]);
    const removeItem = (idx: number) => setItems(items.filter((_, i) => i !== idx));

    const updateItem = (idx: number, field: string, value: any) => {
        const newItems = [...items];
        // @ts-ignore
        newItems[idx][field] = value;
        setItems(newItems);
    };

    const total = items.reduce((acc, item) => acc + (item.qty * item.price), 0);
    const iva = total * 0.19;
    const formatCurrency = (val: number) => val.toLocaleString('es-CO');

    return (
        <div className="space-y-8 max-w-7xl mx-auto">
            <div className="flex items-center gap-4">
                <div className="p-4 rounded-2xl bg-gradient-to-br from-pink-500/20 to-rose-500/20 border border-pink-500/20">
                    <FileText className="w-10 h-10 text-pink-400" />
                </div>
                <div>
                    <h1 className="text-3xl font-bold font-space text-white">Generador de Cotizaciones</h1>
                    <p className="text-slate-400">Crea propuestas comerciales profesionales en segundos.</p>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* Editor Form */}
                <div className="space-y-6">
                    <GlassCard>
                        <h3 className="text-lg font-bold text-white mb-4">Datos del Cliente</h3>
                        <div className="space-y-4">
                            <input
                                className="input-field w-full"
                                placeholder="Nombre / Razón Social"
                                value={client.name}
                                onChange={e => setClient({ ...client, name: e.target.value })}
                            />
                            <div className="grid grid-cols-2 gap-4">
                                <input
                                    className="input-field w-full"
                                    placeholder="NIT / CC"
                                    value={client.nit}
                                    onChange={e => setClient({ ...client, nit: e.target.value })}
                                />
                                <input
                                    className="input-field w-full"
                                    placeholder="Dirección"
                                    value={client.address}
                                    onChange={e => setClient({ ...client, address: e.target.value })}
                                />
                            </div>
                        </div>
                    </GlassCard>

                    <GlassCard>
                        <div className="flex justify-between items-center mb-4">
                            <h3 className="text-lg font-bold text-white">Items</h3>
                            <button onClick={addItem} className="p-2 bg-indigo-500/20 hover:bg-indigo-500/40 rounded-lg text-indigo-400 transition-colors">
                                <Plus className="w-4 h-4" />
                            </button>
                        </div>

                        <div className="space-y-3">
                            {items.map((item, i) => (
                                <motion.div
                                    key={i}
                                    initial={{ opacity: 0, x: -10 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    className="flex gap-2 items-center"
                                >
                                    <input
                                        className="input-field flex-1"
                                        placeholder="Descripción"
                                        value={item.desc}
                                        onChange={e => updateItem(i, 'desc', e.target.value)}
                                    />
                                    <input
                                        type="number"
                                        className="input-field w-20"
                                        placeholder="Cant."
                                        value={item.qty}
                                        onChange={e => updateItem(i, 'qty', Number(e.target.value))}
                                    />
                                    <input
                                        type="number"
                                        className="input-field w-32"
                                        placeholder="Precio"
                                        value={item.price}
                                        onChange={e => updateItem(i, 'price', Number(e.target.value))}
                                    />
                                    <button onClick={() => removeItem(i)} className="p-2 text-rose-400 hover:bg-rose-500/10 rounded-lg">
                                        <Trash className="w-4 h-4" />
                                    </button>
                                </motion.div>
                            ))}
                        </div>
                    </GlassCard>
                </div>

                {/* Live Preview */}
                <div className="sticky top-8">
                    <div className="bg-white text-slate-900 rounded-xl shadow-2xl p-8 min-h-[600px] flex flex-col relative overflow-hidden">
                        <div className="absolute top-0 left-0 w-full h-2 bg-gradient-to-r from-indigo-500 to-purple-500" />

                        <div className="flex justify-between items-start mb-12">
                            <div>
                                <h2 className="text-2xl font-bold text-indigo-900">COTIZACIÓN</h2>
                                <p className="text-sm text-slate-500">#{invoiceId}</p>
                            </div>
                            <div className="text-right">
                                <h3 className="font-bold text-slate-800">Tu Empresa S.A.S</h3>
                                <p className="text-sm text-slate-500">NIT 900.000.000-1</p>
                                <p className="text-sm text-slate-500">Bogotá D.C, Colombia</p>
                            </div>
                        </div>

                        <div className="mb-8 p-4 bg-slate-50 rounded-lg border border-slate-100">
                            <p className="text-xs text-slate-400 uppercase font-bold mb-1">Cliente</p>
                            <p className="font-bold text-slate-800">{client.name || 'Nombre del Cliente'}</p>
                            <p className="text-sm text-slate-600">{client.nit && `NIT: ${client.nit}`}</p>
                            <p className="text-sm text-slate-600">{client.address}</p>
                        </div>

                        <table className="w-full text-sm mb-auto">
                            <thead className="border-b border-slate-200 text-slate-500">
                                <tr>
                                    <th className="py-2 text-left">Item</th>
                                    <th className="py-2 text-center">Cant</th>
                                    <th className="py-2 text-right">Precio</th>
                                    <th className="py-2 text-right">Total</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-slate-100">
                                {items.map((item, i) => (
                                    <tr key={i}>
                                        <td className="py-3 text-slate-700">{item.desc || 'Item ' + (i + 1)}</td>
                                        <td className="py-3 text-center text-slate-600">{item.qty}</td>
                                        <td className="py-3 text-right text-slate-600">${formatCurrency(item.price)}</td>
                                        <td className="py-3 text-right font-medium text-slate-800">
                                            ${formatCurrency(item.qty * item.price)}
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>

                        <div className="border-t-2 border-slate-100 pt-4 space-y-2">
                            <div className="flex justify-between text-slate-600">
                                <span>Subtotal</span>
                                <span>${formatCurrency(total)}</span>
                            </div>
                            <div className="flex justify-between text-slate-600">
                                <span>IVA (19%)</span>
                                <span>${formatCurrency(iva)}</span>
                            </div>
                            <div className="flex justify-between text-xl font-bold text-indigo-900 pt-2">
                                <span>Total</span>
                                <span>${formatCurrency(total + iva)}</span>
                            </div>
                        </div>
                    </div>

                    <div className="flex gap-4 mt-6">
                        <button
                            onClick={() => alert("Función de descarga PDF simulada. En prod usaría 'jspdf'.")}
                            className="flex-1 btn-primary flex justify-center items-center gap-2"
                        >
                            <Download className="w-5 h-5" /> Descargar PDF
                        </button>
                        <button className="px-6 py-2 rounded-lg border border-white/20 hover:bg-white/10 text-white transition-colors">
                            <Printer className="w-5 h-5" />
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}
