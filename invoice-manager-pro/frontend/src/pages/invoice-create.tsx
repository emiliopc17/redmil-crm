import React, { useState } from "react";
import { useCreate, useList } from "@refinedev/core";
import {
    Plus,
    Trash2,
    Save,
    FileText,
    User,
    Search,
    AlertCircle,
    Hash,
    Download
} from "lucide-react";
import { Customer, Item, InvoiceItem } from "../types";

interface ItemRow extends Omit<InvoiceItem, "id"> {
    id: string; // Internal unique ID for React keys
}

export const InvoiceCreatePage: React.FC = () => {
    const [customerId, setCustomerId] = useState("");
    const [items, setItems] = useState<ItemRow[]>([]);
    const [isvRate] = useState(0.15); // 15% ISV Honduras
    const { mutate: createInvoice } = useCreate();

    // Data for selectors
    const { data: customers } = useList<Customer>({ resource: "customers" });
    const { data: products } = useList<Item>({ resource: "items" });

    const addItem = () => {
        const newId = Math.random().toString(36).substring(2, 9);
        setItems([...items, {
            id: newId,
            item_id: "",
            name: "",
            description: "",
            quantity: 1,
            price: 0,
            tax: 0,
            total: 0
        }]);
    };

    const removeItem = (id: string) => {
        setItems((prev) => prev.filter(item => item.id !== id));
    };

    const updateItem = (id: string, field: keyof ItemRow, value: string | number) => {
        setItems((prev) => prev.map(item => {
            if (item.id === id) {
                const updatedItem = { ...item, [field]: value };

                // Autofill if product is selected
                if (field === "item_id") {
                    const prod = products?.data.find((p) => p.id === value);
                    if (prod) {
                        updatedItem.name = prod.name;
                        updatedItem.price = prod.price;
                        updatedItem.description = prod.description || "";
                    }
                }

                // Recalculate totals
                updatedItem.total = Number(updatedItem.quantity) * Number(updatedItem.price);
                updatedItem.tax = updatedItem.total * isvRate;

                return updatedItem;
            }
            return item;
        }));
    };

    const subtotal = items.reduce((acc, item) => acc + item.total, 0);
    const taxTotal = items.reduce((acc, item) => acc + item.tax, 0);
    const grandTotal = subtotal + taxTotal;

    const handleSave = () => {
        if (!customerId) return alert("Selecciona un cliente");
        if (items.length === 0) return alert("Añade al menos un producto");

        createInvoice({
            resource: "invoices",
            values: {
                customer_id: customerId,
                company_id: "00000000-0000-0000-0000-000000000000", // Placeholder until auth is ready
                invoice_number: "INV-" + Date.now().toString().slice(-6),
                invoice_date: new Date().toISOString().split('T')[0],
                due_date: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
                subtotal,
                tax: taxTotal,
                total: grandTotal,
                items: items.map((i) => ({
                    item_id: i.item_id || null,
                    name: i.name,
                    description: i.description,
                    quantity: i.quantity,
                    price: i.price,
                    tax: i.tax,
                    total: i.total
                }))
            }
        });
    };

    return (
        <div className="flex flex-col gap-8 pb-12">
            <header className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                <div className="flex flex-col gap-1">
                    <h1 className="text-4xl font-black">Crear Nueva Factura</h1>
                    <span className="text-spotify-gray-text font-medium">Completa los detalles para generar el documento profesional.</span>
                </div>
                <div className="flex gap-4">
                    <button className="flex items-center gap-2 bg-spotify-gray-light bg-opacity-40 hover:bg-opacity-60 px-6 py-2 rounded-full font-bold transition-all text-sm">
                        <Download size={18} /> Borrador
                    </button>
                    <button
                        onClick={handleSave}
                        className="flex items-center gap-2 bg-spotify-green text-black px-6 py-2 rounded-full font-bold hover:scale-105 transition-all shadow-lg text-sm"
                    >
                        <Save size={18} /> Emitir Factura
                    </button>
                </div>
            </header>

            <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
                {/* Editor Principal */}
                <div className="xl:col-span-2 flex flex-col gap-6">
                    {/* Sección Cliente */}
                    <div className="bg-spotify-gray rounded-xl p-6 border border-spotify-gray-light">
                        <h2 className="text-lg font-bold mb-4 flex items-center gap-2">
                            <User size={20} className="text-spotify-green" />
                            Selección de Cliente
                        </h2>
                        <div className="relative">
                            <select
                                value={customerId}
                                onChange={(e) => setCustomerId(e.target.value)}
                                className="w-full bg-spotify-black border border-spotify-gray-light p-3 rounded-lg text-white appearance-none outline-none focus:border-spotify-green transition-all"
                            >
                                <option value="">Busca o selecciona un cliente...</option>
                                {customers?.data.map((c) => (
                                    <option key={c.id} value={c.id}>{c.name}</option>
                                ))}
                            </select>
                            <Search className="absolute right-4 top-3.5 text-spotify-gray-text pointer-events-none" size={18} />
                        </div>
                    </div>

                    {/* Sección Items */}
                    <div className="bg-spotify-gray rounded-xl p-6 border border-spotify-gray-light">
                        <div className="flex justify-between items-center mb-6">
                            <h2 className="text-lg font-bold flex items-center gap-2">
                                <Plus size={20} className="text-spotify-green" />
                                Detalle de Productos/Servicios
                            </h2>
                            <button
                                onClick={addItem}
                                className="text-xs font-bold text-spotify-green bg-spotify-green bg-opacity-10 px-4 py-2 rounded-full hover:bg-opacity-20 transition-all uppercase tracking-wider"
                            >
                                + Añadir Línea
                            </button>
                        </div>

                        <div className="overflow-x-auto">
                            <table className="w-full border-collapse">
                                <thead>
                                    <tr className="text-left text-xs uppercase tracking-widest text-spotify-gray-text border-b border-spotify-gray-light">
                                        <th className="pb-4 font-bold pl-2">Producto</th>
                                        <th className="pb-4 font-bold w-24">Cant.</th>
                                        <th className="pb-4 font-bold w-32">Precio (Lps)</th>
                                        <th className="pb-4 font-bold w-32 text-right pr-2">Total</th>
                                        <th className="pb-4 font-bold w-12"></th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {items.map((item) => (
                                        <tr key={item.id} className="border-b border-spotify-gray-light border-opacity-30 group hover:bg-spotify-gray-light hover:bg-opacity-20 transition-all">
                                            <td className="py-4 pl-2">
                                                <div className="flex flex-col gap-1">
                                                    <select
                                                        value={item.item_id}
                                                        onChange={(e) => updateItem(item.id, "item_id", e.target.value)}
                                                        className="bg-transparent border-none text-white text-sm font-bold w-full outline-none"
                                                    >
                                                        <option value="">Selecciona Producto...</option>
                                                        {products?.data.map((p) => (
                                                            <option key={p.id} value={p.id}>{p.name}</option>
                                                        ))}
                                                    </select>
                                                    <input
                                                        type="text"
                                                        value={item.description}
                                                        placeholder="Nota adicional..."
                                                        className="bg-transparent border-none text-xs text-spotify-gray-text focus:text-white outline-none w-full"
                                                        onChange={(e) => updateItem(item.id, "description", e.target.value)}
                                                    />
                                                </div>
                                            </td>
                                            <td className="py-4">
                                                <input
                                                    type="number"
                                                    value={item.quantity}
                                                    className="bg-spotify-black border border-transparent focus:border-spotify-gray-light text-center w-16 p-1 rounded rounded-lg text-sm"
                                                    onChange={(e) => updateItem(item.id, "quantity", parseFloat(e.target.value) || 0)}
                                                />
                                            </td>
                                            <td className="py-4">
                                                <input
                                                    type="number"
                                                    value={item.price}
                                                    className="bg-spotify-black border border-transparent focus:border-spotify-gray-light text-center w-24 p-1 rounded rounded-lg text-sm font-mono"
                                                    onChange={(e) => updateItem(item.id, "price", parseFloat(e.target.value) || 0)}
                                                />
                                            </td>
                                            <td className="py-4 text-right pr-2 font-mono text-sm font-bold text-white">
                                                L. {item.total.toFixed(2)}
                                            </td>
                                            <td className="py-4 text-center">
                                                <button
                                                    onClick={() => removeItem(item.id)}
                                                    className="text-spotify-gray-text hover:text-red-500 transition-colors opacity-0 group-hover:opacity-100"
                                                >
                                                    <Trash2 size={16} />
                                                </button>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>

                        {items.length === 0 && (
                            <div className="text-center py-10 flex flex-col items-center gap-3">
                                <FileText className="text-spotify-gray-light" size={48} />
                                <p className="text-spotify-gray-text text-sm">Empieza añadiendo productos a esta factura.</p>
                            </div>
                        )}
                    </div>
                </div>

                {/* Resumen Lateral (Aesthetic Card) */}
                <div className="flex flex-col gap-6">
                    <div className="bg-gradient-to-br from-spotify-green/20 to-spotify-black bg-spotify-gray rounded-xl p-8 border border-white/10 shadow-2xl sticky top-8">
                        <h2 className="text-2xl font-black mb-8 border-b border-white/10 pb-4">Resumen de Pago</h2>

                        <div className="flex flex-col gap-4">
                            <div className="flex justify-between text-sm text-spotify-gray-text font-medium">
                                <span>Subtotal</span>
                                <span className="text-white font-mono">L. {subtotal.toFixed(2)}</span>
                            </div>
                            <div className="flex justify-between text-sm text-spotify-gray-text font-medium">
                                <span>ISV (15.0%)</span>
                                <span className="text-white font-mono">L. {taxTotal.toFixed(2)}</span>
                            </div>
                            <div className="flex justify-between text-sm text-spotify-gray-text font-medium italic">
                                <span>Descuentos</span>
                                <span className="text-red-400 font-mono">- L. 0.00</span>
                            </div>

                            <div className="h-px bg-white/10 my-4 shadow-[0_0_10px_rgba(255,255,255,0.05)]"></div>

                            <div className="flex justify-between items-end">
                                <div className="flex flex-col">
                                    <span className="text-[10px] font-black uppercase tracking-widest text-spotify-green">Total a Pagar</span>
                                    <span className="text-4xl font-black text-white font-sans tracking-tight">L. {grandTotal.toLocaleString(undefined, { minimumFractionDigits: 2 })}</span>
                                </div>
                            </div>
                        </div>

                        <div className="mt-8 p-4 bg-spotify-black rounded-lg border border-spotify-gray-light border-dashed">
                            <div className="flex items-start gap-2 text-[10px] text-spotify-gray-text">
                                <AlertCircle size={14} className="mt-0.5" />
                                <span>Esta factura se generará en moneda local (Lempiras) según la configuración de REDMIL Honduras.</span>
                            </div>
                        </div>

                        {/* Status Label */}
                        <div className="mt-6 flex items-center justify-center gap-2 py-2 bg-spotify-gray-light bg-opacity-20 rounded font-bold text-[10px] uppercase tracking-widest text-spotify-gray-text">
                            <Hash size={12} /> Referencia: Pendiente de Guardar
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};
