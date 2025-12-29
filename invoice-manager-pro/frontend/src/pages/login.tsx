import React, { useState } from "react";
import { useLogin } from "@refinedev/core";
import { LogIn, Lock, Mail, Music } from "lucide-react";

export const LoginPage: React.FC = () => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const { mutate: login, isLoading } = useLogin();

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        login({ email, password });
    };

    return (
        <div className="min-h-screen bg-spotify-black flex items-center justify-center p-4 font-sans text-white">
            <div className="max-w-md w-full flex flex-col items-center">
                {/* Logo Section */}
                <div className="mb-10 flex items-center gap-3 animate-pulse">
                    <div className="w-12 h-12 bg-spotify-green rounded-full flex items-center justify-center shadow-[0_0_20px_rgba(29,185,84,0.4)]">
                        <Music className="text-black" size={28} />
                    </div>
                    <h1 className="text-3xl font-black tracking-tighter">REDMIL PRO</h1>
                </div>

                {/* Login Card */}
                <div className="w-full bg-gradient-to-b from-[#1f1f1f] to-[#121212] p-10 rounded-2xl shadow-2xl border border-white/5">
                    <h2 className="text-2xl font-bold mb-8 text-center uppercase tracking-widest text-spotify-gray-text text-sm">
                        Iniciar Sesión
                    </h2>

                    <form onSubmit={handleSubmit} className="space-y-6">
                        <div className="space-y-2">
                            <label className="text-xs font-bold uppercase tracking-wider text-spotify-gray-text ml-1">
                                Correo Electrónico
                            </label>
                            <div className="relative group">
                                <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none text-spotify-gray-text group-focus-within:text-spotify-green transition-colors">
                                    <Mail size={18} />
                                </div>
                                <input
                                    type="email"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    className="w-full bg-[#3e3e3e] border-none rounded-md py-3 pl-12 pr-4 text-white placeholder-spotify-gray-text focus:ring-2 focus:ring-spotify-green transition-all outline-none"
                                    placeholder="ejemplo@redmil.hn"
                                    required
                                />
                            </div>
                        </div>

                        <div className="space-y-2">
                            <label className="text-xs font-bold uppercase tracking-wider text-spotify-gray-text ml-1">
                                Contraseña
                            </label>
                            <div className="relative group">
                                <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none text-spotify-gray-text group-focus-within:text-spotify-green transition-colors">
                                    <Lock size={18} />
                                </div>
                                <input
                                    type="password"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    className="w-full bg-[#3e3e3e] border-none rounded-md py-3 pl-12 pr-4 text-white placeholder-spotify-gray-text focus:ring-2 focus:ring-spotify-green transition-all outline-none"
                                    placeholder="••••••••"
                                    required
                                />
                            </div>
                        </div>

                        <button
                            type="submit"
                            disabled={isLoading}
                            className="w-full bg-spotify-green text-black font-black py-4 rounded-full hover:scale-105 active:scale-95 transition-all shadow-lg hover:shadow-spotify-green/20 disabled:opacity-50 disabled:hover:scale-100 mt-2 flex items-center justify-center gap-2"
                        >
                            {isLoading ? (
                                <div className="w-5 h-5 border-2 border-black border-t-transparent rounded-full animate-spin"></div>
                            ) : (
                                <>
                                    <span>ENCONTRAR ACCESO</span>
                                    <LogIn size={20} />
                                </>
                            )}
                        </button>
                    </form>

                    <div className="mt-8 pt-8 border-t border-white/5 text-center">
                        <p className="text-sm text-spotify-gray-text">
                            ¿Olvidaste tu contraseña?{" "}
                            <a href="#" className="text-white hover:text-spotify-green transition-colors font-semibold">
                                Obtener ayuda
                            </a>
                        </p>
                    </div>
                </div>

                <div className="mt-8 text-spotify-gray-text text-xs uppercase tracking-[0.2em] font-medium opacity-50">
                    © 2025 REDMIL PRO • HONDURAS
                </div>
            </div>
        </div>
    );
};
