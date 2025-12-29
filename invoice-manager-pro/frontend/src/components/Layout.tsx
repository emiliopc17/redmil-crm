import React, { useState } from "react";
import { LayoutProps } from "@refinedev/core";
import {
    Home,
    FileText,
    Users,
    Package,
    Upload,
    Sun,
    Moon,
    Menu,
    ChevronLeft
} from "lucide-react";
import { Link, useLocation } from "react-router-dom";

export const SpotifyLayout: React.FC<LayoutProps> = ({ children }) => {
    const [darkMode, setDarkMode] = useState(true);
    const [collapsed, setCollapsed] = useState(false);
    const location = useLocation();

    const menuItems = [
        { label: "Dashboard", icon: <Home size={22} />, path: "/" },
        { label: "Facturas", icon: <FileText size={22} />, path: "/invoices" },
        { label: "Clientes", icon: <Users size={22} />, path: "/customers" },
        { label: "Productos", icon: <Package size={22} />, path: "/items" },
        { label: "Cargar PDF", icon: <Upload size={22} />, path: "/pdf-uploads" },
    ];

    return (
        <div className={`min-h-screen ${darkMode ? "dark bg-spotify-black text-white" : "bg-gray-100 text-black"} font-sans`}>
            <div className="flex h-screen overflow-hidden p-2 gap-2">
                {/* Sidebar */}
                <aside className={`${collapsed ? "w-20" : "w-64"} flex flex-col gap-2 transition-all duration-300`}>
                    <div className="bg-spotify-gray rounded-lg p-4 flex flex-col gap-4">
                        <div className="flex items-center justify-between">
                            {!collapsed && <span className="text-xl font-bold text-spotify-green">REDMIL Pro</span>}
                            <button
                                onClick={() => setCollapsed(!collapsed)}
                                className="p-1 hover:bg-spotify-gray-light rounded-full"
                            >
                                <ChevronLeft className={`transition-transform ${collapsed ? "rotate-180" : ""}`} />
                            </button>
                        </div>

                        <nav className="flex flex-col gap-2">
                            {menuItems.map((item) => (
                                <Link
                                    key={item.path}
                                    to={item.path}
                                    className={`flex items-center gap-4 p-2 rounded-md transition-all ${location.pathname === item.path
                                            ? "text-white bg-spotify-gray-light"
                                            : "text-spotify-gray-text hover:text-white"
                                        }`}
                                >
                                    {item.icon}
                                    {!collapsed && <span className="font-semibold">{item.label}</span>}
                                </Link>
                            ))}
                        </nav>
                    </div>

                    <div className="bg-spotify-gray rounded-lg p-4 flex-1 flex flex-col">
                        <Link to="/playlists" className="flex items-center gap-4 text-spotify-gray-text hover:text-white p-2">
                            <FileText size={22} />
                            {!collapsed && <span className="font-semibold">Mis Listas</span>}
                        </Link>
                    </div>

                    {/* Theme Toggle Button */}
                    <div className="bg-spotify-gray rounded-lg p-4">
                        <button
                            onClick={() => setDarkMode(!darkMode)}
                            className="flex items-center gap-4 w-full p-2 text-spotify-gray-text hover:text-white transition-all"
                        >
                            {darkMode ? <Sun size={22} /> : <Moon size={22} />}
                            {!collapsed && <span className="font-semibold">{darkMode ? "Modo Claro" : "Modo Oscuro"}</span>}
                        </button>
                    </div>
                </aside>

                {/* Main Content Area */}
                <main className="flex-1 bg-gradient-to-b from-spotify-gray-light to-spotify-black rounded-lg overflow-y-auto overflow-x-hidden relative">
                    <header className="sticky top-0 z-10 p-4 bg-transparent bg-opacity-80 backdrop-blur-md flex justify-end">
                        <div className="w-10 h-10 bg-spotify-black rounded-full border border-spotify-gray-light flex items-center justify-center cursor-pointer hover:scale-110 transition-transform">
                            R
                        </div>
                    </header>
                    <div className="p-6">
                        {children}
                    </div>
                </main>
            </div>
        </div>
    );
};
