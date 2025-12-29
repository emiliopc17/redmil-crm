import React, { useState } from "react";
import { useCreate } from "@refinedev/core";
import { Upload, FileText, CheckCircle, AlertCircle, Loader2 } from "lucide-react";

export const PDFUploadPage: React.FC = () => {
    const [file, setFile] = useState<File | null>(null);
    const [uploading, setUploading] = useState(false);
    const { mutate } = useCreate();

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files) {
            setFile(e.target.files[0]);
        }
    };

    const handleUpload = async () => {
        if (!file) return;
        setUploading(true);

        const formData = new FormData();
        formData.append("file", file);
        formData.append("upload_type", "price_list");

        // Enviar a la API de FastAPI que usa Docling
        mutate({
            resource: "pdf-uploads",
            values: formData as any,
            successNotification: {
                message: "Archivo subido con éxito",
                description: "Docling está procesando los datos en segundo plano.",
                type: "success",
            },
        }, {
            onSettled: () => setUploading(false)
        });
    };

    return (
        <div className="max-w-4xl mx-auto">
            <h1 className="text-4xl font-black mb-2 text-white">Extraer datos de PDF</h1>
            <p className="text-spotify-gray-text mb-8">Utiliza la potencia de Docling para convertir listas de precios y facturas de proveedores a datos estructurados.</p>

            <div className="bg-spotify-gray rounded-xl p-10 border-2 border-dashed border-spotify-gray-light hover:border-spotify-green transition-all flex flex-col items-center justify-center gap-6 group">
                <div className="w-20 h-20 bg-spotify-gray-light rounded-full flex items-center justify-center text-spotify-green group-hover:scale-110 transition-transform">
                    <Upload size={40} />
                </div>

                <div className="text-center">
                    <label className="cursor-pointer">
                        <span className="bg-white text-black px-8 py-3 rounded-full font-bold hover:scale-105 active:scale-95 transition-all inline-block">
                            ELEGIR ARCHIVO
                        </span>
                        <input type="file" className="hidden" onChange={handleFileChange} accept=".pdf" />
                    </label>
                    <p className="mt-4 text-sm text-spotify-gray-text">
                        {file ? `Seleccionado: ${file.name}` : "Arrastra tus archivos aquí o haz clic para buscar"}
                    </p>
                </div>
            </div>

            {file && (
                <div className="mt-8 bg-spotify-gray p-4 rounded-lg flex items-center justify-between animate-in fade-in slide-in-from-bottom-4">
                    <div className="flex items-center gap-4">
                        <FileText className="text-spotify-green" />
                        <div>
                            <p className="font-bold">{file.name}</p>
                            <p className="text-xs text-spotify-gray-text">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
                        </div>
                    </div>
                    <button
                        onClick={handleUpload}
                        disabled={uploading}
                        className="bg-spotify-green text-black px-6 py-2 rounded-full font-bold hover:scale-105 disabled:opacity-50 disabled:scale-100 flex items-center gap-2"
                    >
                        {uploading ? <Loader2 className="animate-spin" size={18} /> : "PROCESAR CON DOCLING"}
                    </button>
                </div>
            )}

            <div className="mt-12">
                <h2 className="text-xl font-bold mb-4">Procesamientos recientes</h2>
                <div className="grid grid-cols-1 gap-2">
                    {[1, 2].map((i) => (
                        <div key={i} className="bg-spotify-gray hover:bg-spotify-gray-light p-3 rounded-md flex items-center justify-between group transition-colors">
                            <div className="flex items-center gap-4">
                                <CheckCircle className="text-spotify-green" size={20} />
                                <div>
                                    <p className="font-semibold text-sm">Lista_Precios_Proveedor_{i}.pdf</p>
                                    <p className="text-xs text-spotify-gray-text">Completado por Docling • Hace 2 horas</p>
                                </div>
                            </div>
                            <button className="text-spotify-gray-text hover:text-white opacity-0 group-hover:opacity-100 transition-opacity">
                                Ver resultados
                            </button>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};
