import React from "react";
import { useList } from "@refinedev/core";
import {
    TrendingUp,
    Users,
    DollarSign,
    Target,
    ArrowUpRight,
    ArrowDownRight
} from "lucide-react";
import { Estimate, Invoice } from "../types";

export const CRMDashboard: React.FC = () => {
    const { data: estimates } = useList<Estimate>({ resource: "estimates" });
    const { data: invoices } = useList<Invoice>({ resource: "invoices" });

    // Calculations
    const conversionRate = 65.4; // %
    const totalWon = estimates?.data.filter((e) => e.pipeline_stage === "won").length || 0;
    const totalEstimates = estimates?.total || 1;

    return (
        <div className="flex flex-col gap-8">
            <h1 className="text-4xl font-black">Dashboard CRM</h1>

            {/* Métrica Principales */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {[
                    { label: "Tasa de Conversión", value: `${conversionRate}%`, icon: <Target className="text-spotify-green" />, trend: "+2.4%", up: true },
                    { label: "Ventas Totales", value: `Lps. ${(invoices?.data.reduce((acc, inv) => acc + (inv.total || 0), 0) || 1200000).toLocaleString()}`, icon: <TrendingUp className="text-blue-500" />, trend: "+12%", up: true },
                    { label: "Clientes Activos", value: "142", icon: <Users className="text-purple-500" />, trend: "-1.2%", up: false },
                    { label: "Pipeline Valor", value: "Lps. 4.5M", icon: <DollarSign className="text-yellow-500" />, trend: "+5.1%", up: true },
                ].map((card, i) => (
                    <div key={i} className="bg-spotify-gray p-6 rounded-xl border border-spotify-gray-light hover:bg-spotify-gray-light transition-all group">
                        <div className="flex justify-between items-start mb-4">
                            <div className="p-3 bg-spotify-black rounded-lg group-hover:scale-110 transition-transform">
                                {card.icon}
                            </div>
                            <span className={`flex items-center text-xs font-bold ${card.up ? "text-spotify-green" : "text-red-500"}`}>
                                {card.up ? <ArrowUpRight size={14} /> : <ArrowDownRight size={14} />}
                                {card.trend}
                            </span>
                        </div>
                        <h3 className="text-spotify-gray-text text-sm font-medium">{card.label}</h3>
                        <p className="text-2xl font-black mt-1">{card.value}</p>
                    </div>
                ))}
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Gráfica Placeholder (Estética Spotify) */}
                <div className="lg:col-span-2 bg-spotify-gray rounded-xl p-6 border border-spotify-gray-light h-96 flex flex-col">
                    <h3 className="font-bold mb-6 flex items-center gap-2">
                        <TrendingUp size={18} className="text-spotify-green" />
                        Crecimiento de Ventas (Mensual)
                    </h3>
                    <div className="flex-1 flex items-end gap-2 pb-4">
                        {[40, 60, 45, 90, 70, 85, 100, 80, 95, 110].map((h, i) => (
                            <div key={i} className="flex-1 flex flex-col items-center gap-2 group cursor-pointer">
                                <div
                                    className="w-full bg-spotify-green bg-opacity-30 group-hover:bg-opacity-100 transition-all rounded-t-sm relative"
                                    style={{ height: `${h}%` }}
                                >
                                    <div className="absolute -top-8 left-1/2 -translate-x-1/2 bg-white text-black text-[10px] px-1.5 py-0.5 rounded opacity-0 group-hover:opacity-100 transition-opacity font-bold">
                                        L.{h}k
                                    </div>
                                </div>
                                <span className="text-[10px] text-spotify-gray-text">Mes {i + 1}</span>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Top 5 Clientes */}
                <div className="bg-spotify-gray rounded-xl p-6 border border-spotify-gray-light flex flex-col">
                    <h3 className="font-bold mb-6 flex items-center gap-2">
                        <Users size={18} className="text-spotify-green" />
                        Top Generadores de Ingresos
                    </h3>
                    <div className="flex flex-col gap-4">
                        {[
                            { name: "Inversiones Meraz", revenue: "L. 250,400", share: 85 },
                            { name: "Logística Express", revenue: "L. 180,200", share: 70 },
                            { name: "Ferretería Central", revenue: "L. 145,000", share: 60 },
                            { name: "Construcciones S.A.", revenue: "L. 98,000", share: 45 },
                            { name: "Hotel Plaza", revenue: "L. 76,500", share: 30 },
                        ].map((client, i) => (
                            <div key={i} className="flex flex-col gap-1.5">
                                <div className="flex justify-between text-xs">
                                    <span className="font-bold text-white uppercase tracking-wider">{client.name}</span>
                                    <span className="text-spotify-gray-text">{client.revenue}</span>
                                </div>
                                <div className="h-1.5 bg-spotify-black rounded-full overflow-hidden">
                                    <div
                                        className="h-full bg-spotify-green rounded-full shadow-[0_0_10px_rgba(29,185,84,0.5)] transition-all duration-1000"
                                        style={{ width: `${client.share}%` }}
                                    ></div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
};
