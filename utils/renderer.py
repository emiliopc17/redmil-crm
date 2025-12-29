import json
import datetime

def get_quote_html(data):
    """
    Generates the React-based HTML for a quote preview/document.
    Expects data to have: client (dict), items (list), meta (dict), config (dict)
    """
    props_json = json.dumps(data)
    
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://cdn.tailwindcss.com"></script>
        <script src="https://unpkg.com/react@18/umd/react.production.min.js" crossorigin></script>
        <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js" crossorigin></script>
        <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
        <script src="https://unpkg.com/lucide@latest"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
            body {{ font-family: 'Inter', sans-serif; background-color: #f3f4f6; overflow-x: hidden; }}
            
            @media print {{
                @page {{
                    margin: 0;
                    size: auto;
                }}
                html, body {{
                    height: auto !important;
                    margin: 0 !important;
                    padding: 0 !important;
                    background: white !important;
                }}
                .no-print {{ display: none !important; }}
                .preview-wrapper {{
                    padding: 0 !important;
                    margin: 0 !important;
                    display: block !important;
                }}
                .page-container {{ 
                    box-shadow: none !important; 
                    margin: 0 !important; 
                    width: 100% !important;
                    max-width: 100% !important;
                    transform: scale(1) !important;
                    height: auto !important;
                    min-height: 0 !important;
                    padding: 40px !important;
                    border: none !important;
                }}
                * {{
                    -webkit-print-color-adjust: exact !important;
                    print-color-adjust: exact !important;
                }}
            }}
            
            .page-container {{
                width: 210mm;
                min-height: 297mm;
                background: white;
                margin: 20px auto;
                padding: 40px;
                box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
                transform-origin: top center;
                transition: transform 0.2s ease;
                border: 1px solid #e5e7eb;
            }}

            .preview-wrapper {{
                display: flex;
                flex-direction: column;
                align-items: center;
                width: 100%;
                overflow: visible;
            }}
        </style>
    </head>
    <body class="p-4">
        <div id="root"></div>

        <script type="text/babel">
            const {{ useState, useEffect }} = React;

            const INITIAL_DATA = {props_json};

            const formatCurrency = (num) => {{
                return new Intl.NumberFormat('en-US', {{
                    style: 'decimal',
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2
                }}).format(num);
            }};

            const QuotePreview = () => {{
                const data = INITIAL_DATA;
                const {{ client, items, meta, config }} = data;
                const [zoom, setZoom] = useState(0.85);

                useEffect(() => {{
                    lucide.createIcons();
                }}, []);

                const handlePrint = () => {{
                    window.print();
                }};

                const subtotal = items.reduce((acc, item) => acc + (item.quantity * item.price), 0);
                const isv = subtotal * 0.15; 
                const total = subtotal + isv;

                return (
                    <div className="preview-wrapper">
                        {{/* Toolbar */}}
                        <div className="w-full max-w-[210mm] flex justify-between items-center mb-6 no-print bg-white p-3 rounded-lg shadow-sm border border-slate-200">
                             <div className="flex items-center gap-4">
                                <span className="text-xs font-bold text-slate-400 uppercase">Zoom</span>
                                <div className="flex items-center bg-slate-100 rounded-lg p-1">
                                    <button onClick={{() => setZoom(Math.max(0.4, zoom - 0.1))}} className="p-1.5 hover:bg-white rounded shadow-sm transition-all">
                                        <i data-lucide="minus" className="w-4 h-4 text-slate-600"></i>
                                    </button>
                                    <span className="px-4 text-sm font-semibold text-slate-700 w-16 text-center">{{Math.round(zoom * 100)}}%</span>
                                    <button onClick={{() => setZoom(Math.min(1.5, zoom + 0.1))}} className="p-1.5 hover:bg-white rounded shadow-sm transition-all">
                                        <i data-lucide="plus" className="w-4 h-4 text-slate-600"></i>
                                    </button>
                                </div>
                             </div>
                             <div className="flex gap-2">
                                 <button 
                                    onClick={{handlePrint}}
                                    className="flex items-center gap-2 bg-[#0066FF] text-white px-5 py-2 rounded-lg font-semibold hover:opacity-90 transition shadow-lg shadow-blue-200"
                                >
                                    <i data-lucide="printer" className="w-4 h-4"></i> Descargar PDF / Imprimir
                                </button>
                             </div>
                        </div>

                        {{/* Paper Sheet */}}
                        <div className="page-container relative text-slate-800" style={{{{ transform: `scale(${{zoom}})` }}}}>
                            {{/* Header */}}
                            <div className="flex justify-between items-start border-b-2 border-slate-900 pb-8 mb-8">
                                <div className="max-w-[60%]">
                                    <h1 className="text-4xl font-extrabold text-slate-900 tracking-tighter mb-4">REDMIL</h1>
                                    <div className="text-xs text-slate-600 leading-relaxed whitespace-pre-wrap font-medium uppercase tracking-wider">
                                        {{config.header || 'Configura el encabezado en Admin'}}
                                    </div>
                                </div>
                                <div className="text-right">
                                    <div className="inline-block bg-slate-900 text-white px-4 py-1 text-sm font-bold tracking-widest uppercase mb-4">
                                        COTIZACIÓN
                                    </div>
                                    <div className="space-y-1">
                                        <p className="text-[10px] text-slate-400 font-bold uppercase tracking-widest">Número</p>
                                        <p className="text-lg font-bold text-slate-900 tracking-tight">#{{meta.quote_number}}</p>
                                    </div>
                                </div>
                            </div>

                            {{/* Info Grid */}}
                            <div className="grid grid-cols-2 mb-10 gap-12">
                                <div>
                                    <h3 className="text-[10px] font-black text-slate-400 uppercase tracking-[0.2em] mb-3 border-b pb-1">Para:</h3>
                                    <div className="text-sm space-y-0.5">
                                        <p className="text-base font-bold text-slate-900 uppercase underline decoration-2 decoration-[#0066FF] underline-offset-4 mb-2">{{client.name || 'CLIENTE FINAL'}}</p>
                                        <p className="font-medium text-slate-600">{{client.rtn || 'RTN: N/A'}}</p>
                                        <p className="text-slate-500">{{client.address || ''}}</p>
                                        <p className="text-slate-500 font-bold">{{client.phone || ''}}</p>
                                    </div>
                                </div>
                                <div className="text-right">
                                     <h3 className="text-[10px] font-black text-slate-400 uppercase tracking-[0.2em] mb-3 border-b pb-1">Detalles:</h3>
                                     <div className="text-sm space-y-2">
                                        <div className="flex justify-between ml-auto w-48">
                                            <span className="text-slate-400 font-bold tracking-tighter uppercase text-[10px] mt-1">Fecha Emisión</span>
                                            <span className="font-bold text-slate-900">{{meta.date}}</span>
                                        </div>
                                        <div className="flex justify-between ml-auto w-48">
                                            <span className="text-slate-400 font-bold tracking-tighter uppercase text-[10px] mt-1">Validez</span>
                                            <span className="font-bold text-slate-900">{{meta.valid_until}}</span>
                                        </div>
                                     </div>
                                </div>
                            </div>

                            {{/* Items Table */}}
                            <table className="w-full text-sm mb-12">
                                <thead className="bg-[#0066FF] text-white">
                                    <tr>
                                        <th className="py-2.5 px-4 text-left font-black uppercase tracking-widest text-[10px]">Descripción / Código</th>
                                        <th className="py-2.5 px-4 text-center font-black uppercase tracking-widest text-[10px] w-24">Cant.</th>
                                        <th className="py-2.5 px-4 text-right font-black uppercase tracking-widest text-[10px] w-32">P. Unitario</th>
                                        <th className="py-2.5 px-4 text-right font-black uppercase tracking-widest text-[10px] w-32">Total</th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y divide-slate-200 border-b-2 border-slate-900">
                                    {{items.length > 0 ? items.map((item, idx) => (
                                        <tr key={{idx}} className="hover:bg-slate-50">
                                            <td className="py-4 px-4">
                                                <p className="font-bold text-slate-900 tracking-tight">{{item.description}}</p>
                                                <p className="text-[10px] font-bold text-[#0066FF] uppercase tracking-tighter">{{item.code}}</p>
                                            </td>
                                            <td className="py-4 px-4 text-center text-slate-900 font-medium font-mono text-base border-x border-slate-100 italic">{{item.quantity}}</td>
                                            <td className="py-4 px-4 text-right text-slate-900 font-mono">L. {{formatCurrency(item.price)}}</td>
                                            <td className="py-4 px-4 text-right font-black text-slate-900 font-mono border-l border-slate-100">L. {{formatCurrency(item.price * item.quantity)}}</td>
                                        </tr>
                                    )) : (
                                        <tr>
                                            <td colSpan="4" className="py-12 text-center text-slate-300 italic uppercase font-black tracking-widest">
                                                Sin ítems registrados
                                            </td>
                                        </tr>
                                    )}}
                                </tbody>
                            </table>

                            {{/* Totals */}}
                            <div className="flex justify-end pt-2">
                                <div className="w-80 space-y-1">
                                    <div className="flex justify-between text-sm px-4">
                                        <span className="text-slate-400 font-black uppercase text-[10px] tracking-widest">Subtotal</span>
                                        <span className="font-bold font-mono text-slate-600 underline underline-offset-4 decoration-slate-200">L. {{formatCurrency(subtotal)}}</span>
                                    </div>
                                    <div className="flex justify-between text-sm px-4">
                                        <span className="text-slate-400 font-black uppercase text-[10px] tracking-widest">Impuesto ISV 15%</span>
                                        <span className="font-bold font-mono text-slate-600">L. {{formatCurrency(isv)}}</span>
                                    </div>
                                    <div className="flex justify-between items-center bg-slate-900 text-white px-5 py-4 mt-4 shadow-xl">
                                        <span className="font-black uppercase text-[12px] tracking-[0.3em]">Total Neto</span>
                                        <span className="text-2xl font-black font-mono tracking-tighter">L. {{formatCurrency(total)}}</span>
                                    </div>
                                </div>
                            </div>

                            {{/* Footer */}}
                            <div className="mt-20 border-t-2 border-slate-900 pt-6">
                                <div className="flex justify-between items-end">
                                    <div className="max-w-[70%]">
                                        <h4 className="text-[10px] font-black text-slate-900 uppercase tracking-widest mb-2 border-b-2 border-[#0066FF] inline-block">Condiciones y Notas:</h4>
                                        <p className="text-[11px] text-slate-600 font-medium whitespace-pre-wrap leading-relaxed">
                                            {{config.footer || 'Válida por 15 días.'}}
                                        </p>
                                    </div>
                                    <div className="text-right">
                                         <p className="text-[10px] font-black text-slate-900 uppercase tracking-widest border-t-2 border-slate-900 pt-1">Autorizado por REDMIL</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                );
            }};

            const root = ReactDOM.createRoot(document.getElementById('root'));
            root.render(<QuotePreview />);
        </script>
    </body>
    </html>
    """
