import React from "react";
import { useList } from "@refinedev/core";
import { Users, Search, MoreHorizontal } from "lucide-react";

export const CustomerListPage: React.FC = () => {
    const { data, isLoading } = useList({
        resource: "customers",
    });

    return (
        <div className="flex flex-col gap-8">
            <header className="flex flex-col gap-6">
                <div className="flex justify-between items-center">
                    <h1 className="text-4xl font-black">Clientes y Proveedores</h1>
                    <div className="flex gap-2">
                        {["Todos", "VIP", "Corporativo", "Nuevo"].map((tag) => (
                            <button
                                key={tag}
                                className="px-4 py-1.5 rounded-full text-xs font-bold border border-spotify-gray-light hover:border-white transition-all bg-spotify-black text-white hover:bg-spotify-gray-light"
                            >
                                {tag}
                            </button>
                        ))}
                    </div>
                </div>
                <div className="flex items-center gap-4 bg-spotify-gray-light bg-opacity-30 p-2 rounded-md w-full max-w-md border border-transparent focus-within:border-white transition-all">
                    <Search className="text-spotify-gray-text" size={20} />
                    <input
                        type="text"
                        placeholder="Busca por nombre, etiqueta o ciudad..."
                        className="bg-transparent border-none outline-none text-white w-full text-sm placeholder-spotify-gray-text"
                    />
                </div>
            </header>

            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
                {/* Botón para crear nuevo (estilo card) */}
                <div className="bg-spotify-gray hover:bg-spotify-gray-light p-4 rounded-lg flex flex-col items-center justify-center gap-4 cursor-pointer group transition-all h-64 border border-spotify-gray-light border-dashed">
                    <div className="w-24 h-24 bg-spotify-gray-light rounded-full flex items-center justify-center text-spotify-gray-text group-hover:scale-110 transition-transform shadow-xl">
                        <Users size={40} />
                    </div>
                    <span className="font-bold text-center">Añadir nuevo cliente</span>
                </div>

                {isLoading ? (
                    <div className="col-span-full text-center py-20 text-spotify-gray-text">Cargando directorio...</div>
                ) : (
                    data?.data.map((customer: any) => (
                        <div key={customer.id} className="bg-spotify-gray hover:bg-spotify-gray-light p-4 rounded-lg flex flex-col gap-4 cursor-pointer group transition-all h-64 shadow-lg">
                            <div className="relative w-full aspect-square overflow-hidden rounded-md shadow-2xl">
                                <div className="w-full h-full bg-gradient-to-tr from-spotify-gray-light to-spotify-black flex items-center justify-center">
                                    <span className="text-4xl font-black text-spotify-green flex items-center justify-center">
                                        {customer.name.charAt(0)}
                                    </span>
                                </div>
                                <button className="absolute bottom-2 right-2 w-10 h-10 bg-spotify-green rounded-full shadow-xl flex items-center justify-center text-black opacity-0 translate-y-2 group-hover:opacity-100 group-hover:translate-y-0 transition-all duration-300">
                                    <MoreHorizontal size={20} />
                                </button>
                            </div>
                            <div className="flex flex-col">
                                <span className="font-bold truncate text-white">{customer.name}</span>
                                <span className="text-sm text-spotify-gray-text truncate">{customer.email || "Sin email"}</span>
                            </div>
                        </div>
                    ))
                )}

                {/* Dummy data if empty */}
                {!isLoading && (!data?.data || data.data.length === 0) && (
                    ["Inversiones Meraz", "Logística Express", "Ferretería Central"].map((name, i) => (
                        <div key={i} className="bg-spotify-gray hover:bg-spotify-gray-light p-4 rounded-lg flex flex-col gap-4 cursor-pointer group transition-all h-64 shadow-lg opacity-60">
                            <div className="relative w-full aspect-square overflow-hidden rounded-md shadow-2xl">
                                <div className="w-full h-full bg-gradient-to-tr from-blue-900 to-black flex items-center justify-center">
                                    <span className="text-4xl font-black text-white">{name.charAt(0)}</span>
                                </div>
                            </div>
                            <div className="flex flex-col">
                                <span className="font-bold truncate text-white">{name}</span>
                                <span className="text-sm text-spotify-gray-text truncate">cliente@ejemplo.hn</span>
                            </div>
                        </div>
                    ))
                )}
            </div>
        </div>
    );
};
