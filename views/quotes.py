import streamlit as st
import pandas as pd
import json
import database
from utils import renderer
import streamlit.components.v1 as components

def show():
    # Initialize Session State
    if "selected_quote" not in st.session_state:
        st.session_state.selected_quote = None

    st.title("📝 Cotizaciones")
    
    # --- DETAILED VIEW ---
    if st.session_state.selected_quote:
        q = st.session_state.selected_quote
        
        if st.button("🔙 Volver al Listado", use_container_width=True):
            st.session_state.selected_quote = None
            st.rerun()
            
        st.divider()
        
        # Display Quote Details
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown(f"### Cotización #{q['id']}")
            st.markdown(f"**Cliente:** {q['client_name']}")
            st.markdown(f"**Fecha:** {q['created_at']}")
            st.markdown(f"### Total: L. {q['total_lps']:,.2f}")
            
        with col2:
            st.info("💡 Puedes volver a descargar o imprimir el documento usando el botón en la vista previa a la derecha.")

        # Reconstruct data for renderer
        try:
            client_details = json.loads(q['client_details'])
            items = json.loads(q['products_json'])
            
            # Get current config (might have changed, but usually we want snapshot or current?)
            # Usually history wants snapshot, but we didn't save config in history.
            # Let's fetch current config.
            header_info = database.get_config('quote_header')
            footer_info = database.get_config('quote_footer')
            
            preview_data = {
                "client": {
                    "name": q['client_name'],
                    "rtn": client_details.get('rtn', ''),
                    "phone": client_details.get('phone', ''),
                    "address": client_details.get('address', '')
                },
                "items": items,
                "meta": {
                    "date": q['created_at'].split()[0], # Just date
                    "valid_until": "Válida por 15 días", # Hardcoded or calc
                    "quote_number": f"RD-{q['id']:04d}"
                },
                "config": {
                    "header": header_info,
                    "footer": footer_info
                }
            }
            
            html_code = renderer.get_quote_html(preview_data)
            components.html(html_code, height=1000, scrolling=True)
            
        except Exception as e:
            st.error(f"Error al cargar los detalles: {e}")
            
        return

    # --- LIST VIEW ---
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader("Historial de Cotizaciones")
    with col2:
        if st.button("➕ Nueva Cotización", type="primary", use_container_width=True):
            st.session_state.current_page = "Generar Cotización (React)"
            st.rerun()
            
    # Fetch Real Quotes from History
    quotes_history = database.get_all_quotes_history()
    
    if quotes_history:
        df_quotes = pd.DataFrame(quotes_history)
        
        # Format display dataframe
        display_df = df_quotes[["id", "created_at", "client_name", "total_lps"]].copy()
        display_df.columns = ["ID", "Fecha", "Cliente", "Total (L)"]
        
        st.dataframe(
            display_df,
            column_config={
                "Total (L)": st.column_config.NumberColumn(format="L %.2f")
            },
            use_container_width=True, 
            hide_index=True
        )
        
        st.markdown("---")
        # Action to view detail
        selected_id = st.selectbox("Seleccionar Cotización para ver detalle", 
                                  options=[q['id'] for q in quotes_history],
                                  format_func=lambda x: f"Cotización #{x} - {next(q['client_name'] for q in quotes_history if q['id'] == x)}")
        
        if st.button("🔎 Ver Detalle Completo", use_container_width=True):
            st.session_state.selected_quote = next(q for q in quotes_history if q['id'] == selected_id)
            st.rerun()
            
    else:
        st.info("No hay cotizaciones registradas en el historial.")
