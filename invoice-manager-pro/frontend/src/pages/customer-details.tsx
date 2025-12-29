import React, { useState } from "react";
import { useShow, useList, useCreate } from "@refinedev/core";
import {
    User,
    Mail,
    Phone,
    MapPin,
    Plus,
    StickyNote,
    Calendar,
    CheckCircle2,
    Clock,
    MoreVertical,
    Send
} from "lucide-react";

export const CustomerDetailsPage: React.FC = () => {
    const { queryResult } = useShow();
    const { data: customer, isLoading: isCustomerLoading } = queryResult;
    const [noteContent, setNoteContent] = useState("");

    const { data: notes, isLoading: isNotesLoading } = useList({
        resource: "crm/customers/" + customer?.data?.id + "/notes",
        queryOptions: { enabled: !!customer?.data?.id }
    });

    const { data: tasks, isLoading: isTasksLoading } = useList({
        resource: "crm/customers/" + customer?.data?.id + "/tasks",
        queryOptions: { enabled: !!customer?.data?.id }
    });

    const { mutate: addNote } = useCreate();

    const handleAddNote = () => {
        if (!noteContent.trim()) return;
        addNote({
            resource: "crm/customers/" + customer?.data?.id + "/notes",
            values: { content: noteContent },
            successNotification: () => ({
                message: "Nota agregada",
                type: "success"
            })
        });
        setNoteContent("");
    };

    if (isCustomerLoading) return <div className="p-8 text-spotify-gray-text">Cargando perfil...</div>;

    const client = customer?.data;

    return (
        <div className="flex flex-col gap-8 pb-12">
            {/* Header / Profile Hero */}
            <div className="relative bg-gradient-to-b from-spotify-gray-light to-spotify-black p-8 rounded-2xl flex items-end gap-6 h-64 shadow-2xl overflow-hidden">
                <div className="absolute top-0 right-0 p-8 opacity-10">
                    <User size={160} />
                </div>

                <div className="w-40 h-40 bg-spotify-black rounded-lg shadow-2xl flex items-center justify-center border border-spotify-gray-light overflow-hidden">
                    <span className="text-7xl font-black text-spotify-green">
                        {client?.name?.[0]}
                    </span>
                </div>

                <div className="flex flex-col gap-2">
                    <span className="text-xs font-bold uppercase tracking-widest text-spotify-gray-text">Perfil del Cliente</span>
                    <h1 className="text-6xl font-black text-white">{client?.name}</h1>
                    <div className="flex items-center gap-4 text-sm text-spotify-gray-text mt-2 font-medium">
                        <span className="flex items-center gap-1"><Mail size={14} /> {client?.email}</span>
                        <span className="flex items-center gap-1"><Phone size={14} /> {client?.phone || "Sin teléfono"}</span>
                        <span className="flex items-center gap-1"><MapPin size={14} /> {client?.billing_city || "Honduras"}</span>
                    </div>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Lado Izquierdo: Seguimiento (Notas) */}
                <div className="lg:col-span-2 flex flex-col gap-6">
                    <div className="bg-spotify-gray rounded-xl p-6 border border-spotify-gray-light shadow-lg">
                        <h3 className="text-xl font-bold mb-6 flex items-center gap-2">
                            <StickyNote size={20} className="text-spotify-green" />
                            Seguimiento de Ventas
                        </h3>

                        {/* Input de nueva nota */}
                        <div className="bg-spotify-black p-4 rounded-lg mb-8 border border-spotify-gray-light focus-within:border-spotify-green transition-all shadow-inner">
                            <textarea
                                placeholder="Escribe un resumen de la última llamada o visita..."
                                className="w-full bg-transparent border-none outline-none text-white text-sm resize-none h-24"
                                value={noteContent}
                                onChange={(e) => setNoteContent(e.target.value)}
                            />
                            <div className="flex justify-end mt-2 pt-2 border-t border-spotify-gray-light border-opacity-20">
                                <button
                                    onClick={handleAddNote}
                                    className="bg-spotify-green text-black px-4 py-1.5 rounded-full font-bold text-xs hover:scale-105 transition-transform flex items-center gap-2"
                                >
                                    <Send size={14} /> Guardar Nota
                                </button>
                            </div>
                        </div>

                        {/* Timeline de notas */}
                        <div className="flex flex-col gap-4">
                            {notes?.data.length === 0 ? (
                                <div className="text-center py-12 text-spotify-gray-text italic text-sm">
                                    No hay interacciones registradas aún.
                                </div>
                            ) : (
                                notes?.data.map((note: { id: string; created_at: string; content: string }) => (
                                    <div key={note.id} className="group relative bg-spotify-black bg-opacity-40 p-4 rounded-lg border border-spotify-gray-light hover:bg-opacity-60 transition-all">
                                        <div className="flex justify-between items-start mb-2">
                                            <span className="text-[10px] text-spotify-gray-text font-bold uppercase tracking-wider">
                                                {new Date(note.created_at).toLocaleString()}
                                            </span>
                                            <button className="text-spotify-gray-text hover:text-white opacity-0 group-hover:opacity-100 transition-opacity">
                                                <MoreVertical size={14} />
                                            </button>
                                        </div>
                                        <p className="text-sm text-spotify-gray-text leading-relaxed whitespace-pre-wrap">
                                            {note.content}
                                        </p>
                                    </div>
                                ))
                            )}
                        </div>
                    </div>
                </div>

                {/* Lado Derecho: Recordatorios y Tareas */}
                <div className="flex flex-col gap-6">
                    <div className="bg-spotify-gray rounded-xl p-6 border border-spotify-gray-light shadow-lg h-full">
                        <div className="flex justify-between items-center mb-6">
                            <h3 className="text-xl font-bold flex items-center gap-2">
                                <Calendar size={20} className="text-spotify-green" />
                                Recordatorios
                            </h3>
                            <button className="w-8 h-8 bg-spotify-green rounded-full flex items-center justify-center text-black hover:scale-110 transition-transform shadow-lg">
                                <Plus size={20} />
                            </button>
                        </div>

                        <div className="flex flex-col gap-3">
                            {tasks?.data.length === 0 ? (
                                <div className="text-center py-12 text-spotify-gray-text italic text-sm">
                                    No hay tareas pendientes.
                                </div>
                            ) : (
                                tasks?.data.map((task: { id: string; title: string; due_date: string }) => (
                                    <div key={task.id} className="bg-spotify-black bg-opacity-60 p-4 rounded-lg flex gap-3 items-start border border-spotify-gray-light hover:border-spotify-green transition-all group">
                                        <button className="mt-1 text-spotify-gray-light group-hover:text-spotify-green transition-colors">
                                            <CheckCircle2 size={18} />
                                        </button>
                                        <div className="flex flex-col gap-1">
                                            <span className="text-sm font-bold text-white leading-tight">{task.title}</span>
                                            <div className="flex items-center gap-1.5">
                                                <Clock size={12} className="text-spotify-gray-text" />
                                                <span className="text-[10px] font-bold text-spotify-gray-text uppercase">
                                                    {new Date(task.due_date).toLocaleDateString()}
                                                </span>
                                            </div>
                                        </div>
                                    </div>
                                ))
                            )}

                            {/* Dummy Task for demo */}
                            <div className="bg-spotify-black bg-opacity-30 p-4 rounded-lg flex gap-3 items-start border border-spotify-gray-light opacity-60">
                                <div className="mt-1 text-spotify-gray-light"><CheckCircle2 size={18} /></div>
                                <div className="flex flex-col gap-1">
                                    <span className="text-sm font-bold text-white leading-tight">Llamar para cierre de cotización</span>
                                    <div className="flex items-center gap-1.5">
                                        <Clock size={12} className="text-spotify-gray-text" />
                                        <span className="text-[10px] font-bold text-spotify-gray-text uppercase">24 Dic 2025</span>
                                    </div>
                                </div>
                            </div>
                        </div>

                        {/* Botón de historial (estilo Spotify "See all") */}
                        <div className="mt-8 flex justify-center">
                            <button className="text-xs font-bold text-spotify-gray-text hover:text-white uppercase tracking-widest hover:underline">
                                Ver tareas completadas
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};
