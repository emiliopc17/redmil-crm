import React from "react";
import { useList } from "@refinedev/core";
import { Plus, MoreHorizontal, FileText } from "lucide-react";
import { Invoice } from "../types";

export const InvoiceListPage: React.FC = () => {
    const { data, isLoading } = useList<Invoice>({
        resource: "invoices",
    });

    return (
        <div className="flex flex-col gap-6">
            <header className="flex items-end gap-6 mb-8">
                <div className="w-56 h-56 bg-gradient-to-br from-spotify-green to-spotify-black shadow-2xl rounded-lg flex items-center justify-center text-white">
                    <FileText size={100} strokeWidth={1} />
                </div>
                <div className="flex flex-col gap-2">
                    <span className="text-sm font-bold uppercase">Lista</span>
                    <h1 className="text-8xl font-black">Facturas</h1>
                    <div className="flex items-center gap-2 text-sm font-semibold mt-4">
                        <span className="text-spotify-green">REDMIL Pro</span>
                        <span className="text-spotify-gray-text">•</span>
                        <span>{data?.total || 0} facturas emitidas</span>
                    </div>
                </div>
            </header>

            <div className="flex items-center gap-6 p-4">
                <button className="w-14 h-14 bg-spotify-green rounded-full flex items-center justify-center text-black hover:scale-105 transition-transform shadow-lg">
                    <Plus size={30} fill="black" />
                </button>
                <MoreHorizontal className="text-spotify-gray-text hover:text-white cursor-pointer" size={32} />
            </div>

            <div className="bg-transparent overflow-x-auto">
                <table className="w-full text-left text-spotify-gray-text text-sm border-separate border-spacing-y-2 min-w-[800px]">
                    <thead>
                        <tr className="border-b border-spotify-gray-light uppercase text-xs tracking-widest">
                            <th className="px-4 py-2 w-10">#</th>
                            <th className="px-4 py-2">Número</th>
                            <th className="px-4 py-2">Cliente</th>
                            <th className="px-4 py-2">Fecha</th>
                            <th className="px-4 py-2">Estado</th>
                            <th className="px-4 py-2 text-right">Monto Total</th>
                        </tr>
                    </thead>
                    <tbody>
                        {isLoading ? (
                            <tr><td colSpan={6} className="text-center py-10">Cargando facturas...</td></tr>
                        ) : (
                            data?.data.map((invoice, index) => (
                                <tr key={invoice.id} className="group hover:bg-spotify-gray-light transition-colors rounded-md overflow-hidden cursor-pointer">
                                    <td className="px-4 py-3 rounded-l-md font-medium">{index + 1}</td>
                                    <td className="px-4 py-3 text-white font-bold">{invoice.invoice_number}</td>
                                    <td className="px-4 py-3">{invoice.customer?.name || "N/A"}</td>
                                    <td className="px-4 py-3">{invoice.invoice_date}</td>
                                    <td className="px-4 py-3">
                                        <span className={`px-2 py-1 rounded text-xs font-bold uppercase ${invoice.status === 'paid' ? 'bg-spotify-green text-black' : 'bg-spotify-gray-light text-white'
                                            }`}>
                                            {invoice.status}
                                        </span>
                                    </td>
                                    <td className="px-4 py-3 text-right text-white font-mono rounded-r-md">
                                        {invoice.currency} {(invoice.total || 0).toLocaleString()}
                                    </td>
                                </tr>
                            ))
                        )}
                        {/* Sample data if empty */}
                        {!isLoading && (!data?.data || data.data.length === 0) && (
                            [1, 2, 3].map((i) => (
                                <tr key={i} className="group hover:bg-spotify-gray-light transition-colors rounded-md overflow-hidden cursor-pointer opacity-50">
                                    <td className="px-4 py-3 rounded-l-md font-medium">{i}</td>
                                    <td className="px-4 py-3 text-white font-bold">INV-2025-00{i}</td>
                                    <td className="px-4 py-3">Cliente de Prueba {i}</td>
                                    <td className="px-4 py-3">2025-12-23</td>
                                    <td className="px-4 py-3">
                                        <span className="px-2 py-1 rounded text-xs font-bold uppercase bg-spotify-gray-light text-white">
                                            Borrador
                                        </span>
                                    </td>
                                    <td className="px-4 py-3 text-right text-white font-mono rounded-r-md">
                                        USD 1,250.00
                                    </td>
                                </tr>
                            ))
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
};
