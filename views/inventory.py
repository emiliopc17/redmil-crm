import streamlit as st
import pandas as pd
from utils import parsers
import database

def show():
    st.title("📦 Inventario de Productos")
    
    # --- FILTERS SECTION ---
    with st.expander("🔍 Busqueda y Filtros", expanded=True):
        col1, col2, col3 = st.columns([2, 1, 1])
        
        products = database.get_all_products()
        df_products = pd.DataFrame(products) if products else pd.DataFrame(columns=["product_code", "description", "brand", "cost_usd", "cost_lps", "category", "stock_quantity", "id"])
        
        # Brand list for filter
        all_brands = sorted(list(set(df_products['brand'].dropna().unique()))) if not df_products.empty else []
        
        with col1:
            search = st.text_input("Buscar (Código, Nombre)", placeholder="Escribe para buscar...")
        with col2:
            selected_brands = st.multiselect("Filtrar por Marca", options=all_brands)
        with col3:
            # Price range
            min_price = 0.0
            max_price = 2000.0 # Default max
            if not df_products.empty:
               max_val = df_products['cost_usd'].max()
               if max_val > 0: max_price = float(max_val)
            
            price_range = st.slider("Rango de Precio (USD)", 0.0, max_price + 100, (0.0, max_price + 100))

    # Apply Filters
    if not df_products.empty:
        # Text Search
        if search:
            mask = df_products.apply(lambda row: search.lower() in str(row).lower(), axis=1)
            df_products = df_products[mask]
        
        # Brand Filter
        if selected_brands:
            df_products = df_products[df_products['brand'].isin(selected_brands)]
            
        # Price Filter
        df_products = df_products[
            (df_products['cost_usd'] >= price_range[0]) & 
            (df_products['cost_usd'] <= price_range[1])
        ]

    st.markdown("---")
    
    # --- MAIN ACTIONS & GRID ---
    
    # Actions
    ac1, ac2 = st.columns([1, 4])
    with ac1:
        if st.button("🔄 Actualizar", use_container_width=True):
            st.rerun()
            
    with ac2:
        with st.expander("📥 Importar Inventario (Excel/PDF)"):
            st.markdown("""
            **Guía para Carga:**
            Sube tu archivo PDF o Excel. El sistema identificará automáticamente los productos y precios.
            """)
            
            uploaded_file = st.file_uploader("Subir archivo", type=['xlsx', 'pdf'])
            
            if uploaded_file:
                if uploaded_file.name.endswith('.pdf'):
                    extracted_data = parsers.parse_pdf_inventory(uploaded_file)
                elif uploaded_file.name.endswith('.xlsx'):
                    extracted_data = parsers.parse_excel_inventory(uploaded_file)
                else:
                    extracted_data = []

                if extracted_data:
                    current_rate = database.get_current_exchange_rate()
                    st.info(f"Usando tasa: L. {current_rate:.2f}. Se encontraron {len(extracted_data)} productos.")
                    
                    # Convert to LPS
                    for item in extracted_data:
                        item['cost_lps'] = float(item.get('cost_usd', 0)) * float(current_rate)

                    st.dataframe(extracted_data, height=200)

                    # Brand Logic
                    existing_brands = database.get_all_brands()
                    brand_options = ["-- Identificar desde el archivo (No sobrescribir) --"] + existing_brands + ["🆕 Crear Nueva Marca..."]
                    
                    selected_brand_option = st.selectbox("Marca a asignar:", brand_options, index=0)
                    
                    final_brand_name = None
                    force_brand = False

                    if selected_brand_option == "🆕 Crear Nueva Marca...":
                        new_brand_name = st.text_input("Nombre nueva marca:")
                        if new_brand_name.strip():
                            final_brand_name = new_brand_name.strip()
                            force_brand = True
                    elif selected_brand_option != "-- Identificar desde el archivo (No sobrescribir) --":
                        final_brand_name = selected_brand_option
                        force_brand = True
                    
                    if st.button("💾 Guardar en Base de Datos"):
                        count = 0
                        progress_bar = st.progress(0)
                        
                        for i, item in enumerate(extracted_data):
                            if force_brand and final_brand_name:
                                item['brand'] = final_brand_name
                            # If not forcing, it uses item['brand'] which comes from parser (default Unknown if missing)
                            
                            if database.upsert_product(item, user_name="Importador"):
                                count += 1
                            progress_bar.progress((i + 1) / len(extracted_data))
                        
                        st.success(f"¡Procesado! {count} productos actualizados.")
                        st.rerun()
                else:
                    st.warning("No se encontraron datos válidos.")

    # Main Grid
    st.markdown(f"### Lista de Productos ({len(df_products)})")
    
    if not df_products.empty:
        # Only show relevant columns
        # Columns: product_code, description, brand, cost_usd, cost_lps
        # Hide: id, category, stock_quantity, image_url, ...
        
        edited_df = st.data_editor(
            df_products,
            column_config={
                "product_code": "Código",
                "description": st.column_config.TextColumn("Descripción", width="large"),
                "brand": "Marca",
                "cost_usd": st.column_config.NumberColumn("Costo USD", format="$%.2f"),
                "cost_lps": st.column_config.NumberColumn("Costo LPS", format="L %.2f"),
            },
            column_order=["product_code", "description", "brand", "cost_usd", "cost_lps"],
            hide_index=True,
            use_container_width=True,
            num_rows="dynamic",
            key="inventory_editor",
            disabled=["id", "cost_lps"] # Disable LPS editing directly to enforce consistency? Or allow both? Let's allow USD edit.
        )
        
        if st.button("💾 Guardar Cambios en Grid"):
            current_rate = database.get_current_exchange_rate()
            updates = 0
            for idx, row in edited_df.iterrows():
                # Re-calc LPS
                row['cost_lps'] = float(row['cost_usd']) * float(current_rate)
                item = row.to_dict()
                if database.upsert_product(item, user_name="GridEdit"):
                    updates += 1
            st.success(f"{updates} registros actualizados.")
            st.rerun()
            
    else:
        st.info("No hay productos que coincidan con los filtros.")
        
    # --- PRODUCT DETAILS & HISTORY ---
    st.markdown("---")
    st.markdown("### 📋 Detalles del Producto (Historial y Cotizaciones)")
    
    # Product Selector
    if not df_products.empty:
        display_options = df_products.apply(lambda x: f"{x['product_code']} - {x['description']}", axis=1).tolist()
        selected_prod_str = st.selectbox("Selecciona un producto para ver detalles:", ["-- Seleccionar --"] + display_options)
        
        if selected_prod_str != "-- Seleccionar --":
            # Extract code
            code = selected_prod_str.split(" - ")[0]
            prod_row = df_products[df_products['product_code'] == code].iloc[0]
            prod_id = int(prod_row['id']) # Ensure int
            
            c1, c2 = st.columns(2)
            
            with c1:
                st.markdown("#### 📉 Historial de Precios")
                history = database.get_product_history(prod_id)
                if history:
                    st.dataframe(
                        pd.DataFrame(history)[['change_date', 'old_cost_usd', 'new_cost_usd', 'changed_by']],
                        column_config={
                            "change_date": "Fecha Cambio",
                            "old_cost_usd": st.column_config.NumberColumn("Antes", format="$%.2f"),
                            "new_cost_usd": st.column_config.NumberColumn("Nuevo", format="$%.2f"),
                            "changed_by": "Usuario"
                        },
                        hide_index=True,
                        use_container_width=True
                    )
                else:
                    st.info("No hay historial de cambios.")
                    
            with c2:
                st.markdown("#### 📑 Cotizaciones Relacionadas")
                quotes = database.get_product_quotes(prod_id)
                if quotes:
                    st.dataframe(
                        pd.DataFrame(quotes),
                        column_config={
                            "quote_date": "Fecha",
                            "client_name": "Cliente",
                            "quantity": "Cant.",
                            "unit_price_lps": st.column_config.NumberColumn("Precio Unit. (L)", format="L %.2f")
                        },
                        hide_index=True,
                        use_container_width=True
                    )
                else:
                    st.info("Este producto no ha sido cotizado aún.")
