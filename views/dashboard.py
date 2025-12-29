import streamlit as st
import database
from datetime import datetime, date

def show():
    # Header
    st.markdown("""
        <div style="margin-bottom: 2rem;">
            <h1 style="font-size: 2.5rem; font-weight: 800; letter-spacing: -0.03em;">Dashboard</h1>
            <p style="color: #6b7280;">Vista general del sistema y métricas clave.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # --- METRICS SECTION (BENTO GRID) ---
    
    # Get Data
    rate_info = database.get_current_exchange_rate_full()
    products = database.get_all_products()
    quotes = database.get_all_quotes() 
    
    # Calculations
    current_rate = rate_info['rate_value']
    rate_date_str = rate_info['rate_date']
    
    inventory_count = len(products)
    quotes_count = len(quotes)
    
    # Calculate total sum in Lempiras
    total_lps = 0
    if quotes:
        for quote in quotes:
            if 'total_amount_lps' in quote and quote['total_amount_lps']:
                total_lps += float(quote['total_amount_lps'])
    
    # Rate Freshness
    try:
        last_date = datetime.strptime(rate_date_str, '%Y-%m-%d').date()
    except:
        last_date = date.today()
    is_outdated = last_date < date.today()
    rate_color = "#ef4444" if is_outdated else "#10b981"
    rate_icon = "⚠️" if is_outdated else "✅"

    # CSS Grid Layout (using Streamlit Cols for structure, HTML for cards)
    c1, c2, c3 = st.columns(3)
    
    # Card 1: Exchange Rate
    with c1:
        st.markdown(f"""
        <div class="bento-card">
            <div class="metric-label">Tasa de Cambio (Venta)</div>
            <div class="metric-value">L. {current_rate:.4f}</div>
            <div class="metric-delta" style="color: {rate_color}">
                {rate_icon} Actualizado: {rate_date_str}
            </div>
            <div style="margin-top: 1rem; font-size: 0.75rem; color: #9ca3af;">
                Fuente: Manual
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    # Card 2: Inventory
    with c2:
        st.markdown(f"""
        <div class="bento-card">
            <div class="metric-label">Productos en Inventario</div>
            <div class="metric-value">{inventory_count}</div>
            <div class="metric-delta delta-pos">
                🛒 Items Activos
            </div>
            <div style="margin-top: 1rem; font-size: 0.75rem; color: #9ca3af;">
                Disponibles para cotizar
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Card 3: Total in Lempiras
    with c3:
        st.markdown(f"""
        <div class="bento-card">
            <div class="metric-label">Total Cotizaciones</div>
            <div class="metric-value">L. {total_lps:,.2f}</div>
            <div class="metric-delta delta-pos">
                📄 {quotes_count} Cotizaciones
            </div>
            <div style="margin-top: 1rem; font-size: 0.75rem; color: #9ca3af;">
                Suma total en Lempiras
            </div>
        </div>
        """, unsafe_allow_html=True)

    # --- ACTIONS & UTILS ---
    st.markdown("### ⚡ Acciones Rápidas")
    
    ac1, ac2, ac3 = st.columns([2, 1, 1])
    
    with ac1:
        # Rate Updater Inline
        with st.expander("🔄 Actualizar Tasa de Cambio", expanded=is_outdated):
            new_rate = st.number_input("Nueva Tasa de Venta (Lps)", value=float(current_rate), format="%.4f", step=0.0001)
            if st.button("Guardar Nueva Tasa", type="primary"):
                if database.update_exchange_rate(new_rate):
                    st.success("Tasa actualizada correctamente.")
                    st.rerun()

    with ac2:
        st.markdown("<div style='height: 10px'></div>", unsafe_allow_html=True) # Spacer
        if st.button("📝 Crear Cotización", use_container_width=True):
             st.session_state.current_page = "Generar Cotización (React)"
             st.rerun()

    with ac3:
        st.markdown("<div style='height: 10px'></div>", unsafe_allow_html=True) # Spacer
        if st.button("📦 Ver Inventario", use_container_width=True):
             st.session_state.current_page = "Inventario"
             st.rerun()

    # --- TWO COLUMN LAYOUT FOR RECENT ACTIVITY ---
    st.markdown("---")
    
    col_left, col_right = st.columns([1.5, 1])
    
    # LEFT COLUMN: Recent Quotes
    with col_left:
        st.markdown("### 📋 Últimas 5 Cotizaciones")
        if quotes:
            # Get last 5 quotes sorted by date (descending)
            sorted_quotes = sorted(quotes, key=lambda x: x.get('quote_date', ''), reverse=True)
            recent_quotes = sorted_quotes[:5]
            
            # Display as interactive table
            for idx, quote in enumerate(recent_quotes):
                quote_id = quote.get('id', idx)
                client_name = quote.get('client_name', 'N/A')
                quote_date = quote.get('quote_date', 'N/A')
                total = quote.get('total_amount_lps', 0)
                
                # Create clickable card for each quote
                col_a, col_b, col_c = st.columns([2, 2, 1])
                
                with col_a:
                    st.markdown(f"**{client_name}**")
                with col_b:
                    st.markdown(f"📅 {quote_date}")
                with col_c:
                    st.markdown(f"**L. {float(total):,.2f}**")
                
                # View button
                if st.button(f"Ver 👁️", key=f"view_quote_{quote_id}", use_container_width=True):
                    st.session_state.current_page = "Cotizaciones"
                    st.session_state.selected_quote_id = quote_id
                    st.rerun()
                
                st.markdown("---")
        else:
            st.info("No hay cotizaciones recientes para mostrar.")
    
    # RIGHT COLUMN: Top 10 Brands
    with col_right:
        st.markdown("### 🏆 Top 10 Marcas Más Cotizadas")
        
        # Calculate brand counts from quotes
        if quotes:
            brand_counts = {}
            
            # Get all quote items
            conn = database.get_connection()
            cursor = conn.cursor()
            
            for quote in quotes:
                quote_id = quote.get('id')
                if quote_id:
                    cursor.execute("""
                        SELECT qi.product_id, p.brand 
                        FROM quote_items qi
                        JOIN products p ON qi.product_id = p.id
                        WHERE qi.quote_id = ?
                    """, (quote_id,))
                    
                    items = cursor.fetchall()
                    for item in items:
                        brand = item['brand'] or 'Sin Marca'
                        brand_counts[brand] = brand_counts.get(brand, 0) + 1
            
            conn.close()
            
            # Sort by count and get top 10
            if brand_counts:
                sorted_brands = sorted(brand_counts.items(), key=lambda x: x[1], reverse=True)[:10]
                
                # Display as a beautiful list
                for idx, (brand, count) in enumerate(sorted_brands):
                    # Create a progress bar effect
                    max_count = sorted_brands[0][1]
                    percentage = (count / max_count) * 100
                    
                    st.markdown(f"""
                    <div style="margin-bottom: 1rem;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 0.25rem;">
                            <span style="font-weight: 600; font-size: 0.9rem;">{idx + 1}. {brand}</span>
                            <span style="color: #6b7280; font-size: 0.85rem;">{count} veces</span>
                        </div>
                        <div style="background: #e5e7eb; border-radius: 4px; height: 6px; overflow: hidden;">
                            <div style="background: linear-gradient(90deg, #667eea, #764ba2); width: {percentage}%; height: 100%;"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No hay datos de marcas aún.")
        else:
            st.info("No hay cotizaciones para analizar.")
