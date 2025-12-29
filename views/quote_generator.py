import streamlit as st
import pandas as pd
import json
import datetime
import streamlit.components.v1 as components
import database

def show():
    st.title("📄 Generador de Cotizaciones")

    # Initialize Session State
    if 'quote_items' not in st.session_state:
        st.session_state.quote_items = []
    if 'client_mode' not in st.session_state:
        st.session_state.client_mode = "Buscar"
    if 'selected_client_data' not in st.session_state:
        st.session_state.selected_client_data = None
    
    col_left, col_right = st.columns([1.3, 2.7], gap="medium")

    # --- LEFT PANEL: COMPACT EDITOR ---
    with col_left:
        # Client Info
        with st.container():
            st.markdown("### 👤 Cliente")
            client_mode = st.radio("Acción", ["Buscar", "Nuevo"], horizontal=True, key="client_mode_radio")
            
            selected_client_id = None
            c_name, c_rtn, c_phone, c_addr = "", "", "", ""
            
            if client_mode == "Buscar":
                clients = database.get_all_clients()
                client_map = {f"{c['full_name']}": c for c in clients}
                search_client = st.selectbox("Buscar por nombre", ["-- Seleccionar --"] + list(client_map.keys()))
                if search_client != "-- Seleccionar --":
                    c_data = client_map[search_client]
                    selected_client_id = c_data['id']
                    c_name = c_data['full_name']
                    c_rtn = c_data.get('rtn_id', '') or c_data.get('email', '')
                    c_phone = c_data.get('phone', '')
                    c_addr = c_data.get('address', '')
                    # Store in session for consistency
                    st.session_state.selected_client_data = {
                        "name": c_name, "rtn": c_rtn, "phone": c_phone, "address": c_addr
                    }
                elif st.session_state.selected_client_data:
                    # Use previously selected/created client
                    c_name = st.session_state.selected_client_data.get("name", "")
                    c_rtn = st.session_state.selected_client_data.get("rtn", "")
                    c_phone = st.session_state.selected_client_data.get("phone", "")
                    c_addr = st.session_state.selected_client_data.get("address", "")
            else:
                c_name = st.text_input("Nombre Completo")
                c_rtn = st.text_input("RTN / ID")
                c_phone = st.text_input("Teléfono")
                c_addr = st.text_area("Dirección", height=60)
                if st.button("✨ Guardar y Usar Cliente", use_container_width=True):
                    if c_name:
                        # FIX 1: Save new client to database
                        client_data = {
                            "full_name": c_name,
                            "rtn_id": c_rtn,
                            "phone": c_phone,
                            "email": "",  # Can be added if needed
                            "address": c_addr
                        }
                        if database.create_client(client_data):
                            st.success(f"✅ Cliente '{c_name}' guardado en la base de datos.")
                        else:
                            st.warning("⚠️ El cliente ya existe o hubo un error. Usando datos temporalmente.")
                        
                        # Store in session for use in quote
                        st.session_state.selected_client_data = {
                            "name": c_name, "rtn": c_rtn, "phone": c_phone, "address": c_addr
                        }

        st.markdown("---")
        
        # FIX 2: Dual Product Search (Code and Description/Brand)
        with st.container():
            st.markdown("### 🛒 Buscar Productos")
            
            # Two separate search fields
            search_code = st.text_input("🔢 Buscar por Código", placeholder="Ej: PROD-001")
            search_desc = st.text_input("📝 Buscar por Descripción/Marca", placeholder="Ej: Laptop HP")
            
            # Get all products
            products = database.get_all_products()
            
            # Filter products based on search
            filtered_products = products
            if search_code.strip():
                filtered_products = [
                    p for p in filtered_products 
                    if search_code.lower() in p['product_code'].lower()
                ]
            if search_desc.strip():
                filtered_products = [
                    p for p in filtered_products 
                    if search_desc.lower() in p['description'].lower() or 
                       search_desc.lower() in (p.get('brand', '') or '').lower()
                ]
            
            # Show results count
            if search_code.strip() or search_desc.strip():
                st.caption(f"📊 {len(filtered_products)} productos encontrados")
            
            # Product selector with filtered results
            prod_options = {f"{p['product_code']} - {p['description']}": p for p in filtered_products}
            selected_prod_label = st.selectbox(
                "Seleccionar Producto", 
                ["-- Seleccionar --"] + list(prod_options.keys()),
                key="product_selector"
            )
            
            row1_c1, row1_c2 = st.columns([1, 1])
            with row1_c1:
                qty_input = st.number_input("Cant.", min_value=1, value=1)
            
            current_rate = database.get_current_exchange_rate()
            base_price = 0.0
            if selected_prod_label != "-- Seleccionar --":
                prod = prod_options[selected_prod_label]
                base_price = float(prod.get('cost_usd', 0)) * float(current_rate)
                
            with row1_c2:
                markup_pct = st.number_input("% Ganancia", min_value=0, value=0, max_value=500, step=5)
            
            final_unit_price = base_price * (1 + (markup_pct / 100))
            
            st.info(f"P. Inicial: L. {base_price:,.2f} → Final: **L. {final_unit_price:,.2f}**")
            
            if st.button("➕ Agregar a la Lista", type="primary", use_container_width=True):
                if selected_prod_label != "-- Seleccionar --":
                    prod = prod_options[selected_prod_label]
                    st.session_state.quote_items.append({
                        "product_id": prod.get('id'),
                        "code": prod['product_code'],
                        "description": prod['description'],
                        "quantity": qty_input,
                        "price": final_unit_price,
                        "markup": markup_pct,
                        "base_lps": base_price
                    })
                    st.success(f"✅ Agregado: {prod['description']}")
                    st.rerun()

        st.markdown("---")
        
        # FIX 3: Items Table with Delete Option
        if st.session_state.quote_items:
            st.markdown("### 📋 Productos en Cotización")
            st.caption(f"Total de productos: {len(st.session_state.quote_items)}")
            
            # Display each item with delete button
            for idx, item in enumerate(st.session_state.quote_items):
                with st.container():
                    col_item, col_qty, col_price, col_delete = st.columns([3, 1, 1.5, 0.8])
                    
                    with col_item:
                        st.markdown(f"**{item['description']}**")
                        st.caption(f"Código: {item['code']}")
                    
                    with col_qty:
                        # Allow editing quantity
                        new_qty = st.number_input(
                            "Q",
                            min_value=1,
                            value=int(item['quantity']),
                            key=f"qty_{idx}",
                            label_visibility="collapsed"
                        )
                        if new_qty != item['quantity']:
                            st.session_state.quote_items[idx]['quantity'] = new_qty
                            st.rerun()
                    
                    with col_price:
                        subtotal = item['quantity'] * item['price']
                        st.markdown(f"**L. {subtotal:,.2f}**")
                        st.caption(f"@L. {item['price']:,.2f}")
                    
                    with col_delete:
                        # Delete button
                        if st.button("🗑️", key=f"del_{idx}", help="Eliminar producto"):
                            st.session_state.quote_items.pop(idx)
                            st.success("Producto eliminado")
                            st.rerun()
                    
                    st.markdown("---")
            
            # Total calculation
            total_subtotal = sum(i['quantity'] * i['price'] for i in st.session_state.quote_items)
            isv = total_subtotal * 0.15
            total = total_subtotal + isv
            
            st.markdown(f"""
                <div style='background: #f0f2f6; padding: 1rem; border-radius: 8px;'>
                    <p style='margin:0;'><b>Subtotal:</b> L. {total_subtotal:,.2f}</p>
                    <p style='margin:0;'><b>ISV (15%):</b> L. {isv:,.2f}</p>
                    <p style='margin:0; font-size:1.2rem; color:#667eea;'><b>TOTAL:</b> L. {total:,.2f}</p>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("")
            
            # Save button
            if st.button("💾 Guardar Cotización", type="primary", use_container_width=True):
                # Get client data from session or form
                if st.session_state.selected_client_data:
                    c_name = st.session_state.selected_client_data["name"]
                    c_rtn = st.session_state.selected_client_data["rtn"]
                    c_phone = st.session_state.selected_client_data["phone"]
                    c_addr = st.session_state.selected_client_data["address"]
                
                if not c_name:
                    st.error("⚠️ Debes seleccionar o crear un cliente primero.")
                else:
                    client_details = json.dumps({"rtn": c_rtn, "phone": c_phone, "address": c_addr})
                    products_json = json.dumps(st.session_state.quote_items)
                    
                    if database.save_quote_history(c_name, client_details, products_json, total):
                        st.success("✅ ¡Cotización Guardada Exitosamente!")
                        st.balloons()
                        
                        # Store that quote was saved
                        st.session_state.quote_saved = True
                        st.rerun()
        
        # Show options after saving
        if st.session_state.get('quote_saved', False):
            st.markdown("---")
            st.markdown("### ✅ Cotización Guardada")
            st.markdown("#### ¿Qué deseas hacer ahora?")
            
            col_opt1, col_opt2 = st.columns(2)
            
            with col_opt1:
                if st.button("🆕 Nueva Cotización", use_container_width=True, type="primary"):
                    # FIX 4: Clear everything for new quote
                    st.session_state.quote_items = []
                    st.session_state.selected_client_data = None
                    st.session_state.quote_saved = False
                    st.success("📝 Documento en blanco listo")
                    st.rerun()
            
            with col_opt2:
                if st.button("📋 Ver Historial", use_container_width=True):
                    st.session_state.current_page = "Cotizaciones"
                    st.session_state.quote_saved = False
                    st.rerun()

    # --- RIGHT PANEL: ZOOMABLE PREVIEW ---
    with col_right:
        from utils import renderer
        
        # Get client data for preview
        if st.session_state.selected_client_data:
            c_name = st.session_state.selected_client_data.get("name", "")
            c_rtn = st.session_state.selected_client_data.get("rtn", "")
            c_phone = st.session_state.selected_client_data.get("phone", "")
            c_addr = st.session_state.selected_client_data.get("address", "")
        
        # Load Global Configs
        header_info = database.get_config('quote_header')
        footer_info = database.get_config('quote_footer')
        
        preview_data = {
            "client": {"name": c_name, "rtn": c_rtn, "phone": c_phone, "address": c_addr},
            "items": st.session_state.quote_items,
            "meta": {
                "date": datetime.date.today().strftime("%d/%m/%Y"),
                "valid_until": (datetime.date.today() + datetime.timedelta(days=15)).strftime("%d/%m/%Y"),
                "quote_number": f"RD-{datetime.date.today().strftime('%y%m%d')}-NEW"
            },
            "config": {
                "header": header_info,
                "footer": footer_info
            }
        }
        
        html_code = renderer.get_quote_html(preview_data)
        components.html(html_code, height=1200, scrolling=True)
