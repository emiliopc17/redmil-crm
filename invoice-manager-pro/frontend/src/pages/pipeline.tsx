import React from "react";
import { useList, useUpdate } from "@refinedev/core";
import { ChevronRight, Clock, User, DollarSign } from "lucide-react";

const STAGES = [
    { id: "prospecting", title: "Prospección", color: "bg-gray-500" },
    { id: "proposal_sent", title: "Propuesta Enviada", color: "bg-blue-500" },
    { id: "negotiation", title: "Negociación", color: "bg-yellow-500" },
    { id: "won", title: "Ganada 🚀", color: "bg-spotify-green" },
    { id: "lost", title: "Perdida", color: "bg-red-500" },
];

export const PipelineKanbanPage: React.FC = () => {
    const { data, isLoading } = useList({
        resource: "estimates",
    });

    const { mutate: updateEstimate } = useUpdate();

    const handleDragStart = (e: React.DragEvent, id: string) => {
        e.dataTransfer.setData("estimateId", id);
    };

    const handleDrop = (e: React.DragEvent, stageId: string) => {
        const id = e.dataTransfer.getData("estimateId");
        updateEstimate({
            resource: "estimates",
            id,
            values: { pipeline_stage: stageId },
        });
    };

    const getDaysOld = (dateStr: string) => {
        const diff = Date.now() - new Date(dateStr).getTime();
        return Math.floor(diff / (1000 * 60 * 60 * 24));
    };

    return (
        <div className="flex flex-col h-full gap-6">
            <h1 className="text-4xl font-black">Pipeline de Ventas</h1>

            <div className="flex gap-4 overflow-x-auto pb-4 h-[calc(100vh-200px)]">
                {STAGES.map((stage) => (
                    <div
                        key={stage.id}
                        onDragOver={(e) => e.preventDefault()}
                        onDrop={(e) => handleDrop(e, stage.id)}
                        className="flex-shrink-0 w-80 bg-spotify-gray bg-opacity-50 rounded-lg p-4 flex flex-col gap-4 border border-spotify-gray-light"
                    >
                        <div className="flex items-center justify-between border-b border-spotify-gray-light pb-2">
                            <h3 className="font-bold flex items-center gap-2">
                                <span className={`w-2 h-2 rounded-full ${stage.color}`}></span>
                                {stage.title}
                            </h3>
                            <span className="text-xs text-spotify-gray-text bg-spotify-black px-2 py-1 rounded">
                                {data?.data.filter((e: { pipeline_stage?: string }) => (e.pipeline_stage || "prospecting") === stage.id).length || 0}
                            </span>
                        </div>

                        <div className="flex flex-col gap-3 overflow-y-auto">
                            {data?.data
                                .filter((e: { pipeline_stage?: string }) => (e.pipeline_stage || "prospecting") === stage.id)
                                .map((estimate: { id: string; estimate_number: string; estimate_date: string; customer?: { name: string }; last_note?: string; total?: number }) => (
                                    <div
                                        key={estimate.id}
                                        draggable
                                        onDragStart={(e) => handleDragStart(e, estimate.id)}
                                        className="bg-spotify-gray-light bg-opacity-40 p-4 rounded-lg border border-transparent hover:border-spotify-green cursor-grab active:cursor-grabbing transition-all group shadow-md"
                                    >
                                        <div className="flex justify-between items-start mb-2">
                                            <span className="text-xs font-mono text-spotify-green">{estimate.estimate_number}</span>
                                            <div className="flex items-center gap-1 text-[10px] text-spotify-gray-text bg-spotify-black px-1.5 py-0.5 rounded">
                                                <Clock size={10} />
                                                {getDaysOld(estimate.estimate_date)}d
                                            </div>
                                        </div>

                                        <h4 className="font-bold text-sm mb-1 group-hover:text-spotify-green transition-colors">
                                            {estimate.customer?.name || "Cliente Desconocido"}
                                        </h4>
                                        <p className="text-[10px] text-spotify-gray-text italic truncate mb-4">
                                            {estimate.last_note || "Sin actividad reciente..."}
                                        </p>

                                        <div className="flex justify-between items-end mt-4">
                                            <div className="flex flex-col">
                                                <span className="text-[10px] text-spotify-gray-text uppercase">Monto</span>
                                                <span className="text-sm font-bold text-white">Lps. {estimate.total?.toLocaleString() || "0.00"}</span>
                                            </div>
                                            <div className="w-8 h-8 rounded-full bg-spotify-black border border-spotify-gray-light flex items-center justify-center text-xs">
                                                {estimate.customer?.name?.[0] || "?"}
                                            </div>
                                        </div>
                                    </div>
                                ))}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};
