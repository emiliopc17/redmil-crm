import streamlit as st
import pandas as pd
import database
import hashlib

def show():
    st.title("⚙️ Configuración del Sistema")
    
    tab1, tab2, tab3 = st.tabs(["👥 Usuarios", "💱 Tasas de Cambio", "📄 Cotizaciones"])
    
    # --- USERS TAB ---
    with tab1:
        st.subheader("Gestión de Usuarios")
        
        # List Users
        users = database.get_all_users()
        if users:
            df_users = pd.DataFrame(users)
            st.dataframe(df_users[["id", "full_name", "username", "role", "created_at"]], hide_index=True, use_container_width=True)
            
            # Delete User Action
            with st.expander("🗑️ Eliminar Usuario"):
                user_to_delete = st.selectbox("Seleccionar usuario a eliminar", 
                                            options=users, 
                                            format_func=lambda x: f"{x['username']} ({x['full_name']})")
                
                if st.button("Eliminar Usuario"):
                    if user_to_delete['username'] == 'admin':
                        st.error("No puedes eliminar al usuario admin principal.")
                    elif user_to_delete['username'] == st.session_state.get('username'):
                        st.error("No puedes eliminar tu propio usuario.")
                    else:
                        database.delete_user(user_to_delete['id'])
                        st.success("Usuario eliminado.")
                        st.rerun()

        st.divider()
        
        # Create User
        st.subheader("Crear Nuevo Usuario")
        with st.form("create_user_form"):
            col1, col2 = st.columns(2)
            with col1:
                new_user_name = st.text_input("Nombre Completo")
                new_username = st.text_input("Usuario (Login)")
            with col2:
                new_password = st.text_input("Contraseña", type="password")
                new_role = st.selectbox("Rol", ["vendedor", "admin"])
            
            submitted = st.form_submit_button("Crear Usuario")
            if submitted:
                if new_username and new_password and new_user_name:
                    if database.create_user(new_username, new_password, new_user_name, new_role):
                        st.success(f"Usuario {new_username} creado exitosamente.")
                        st.rerun()
                    else:
                        st.error("Error: El usuario ya existe.")
                else:
                    st.warning("Todos los campos son obligatorios.")

    # --- RATES TAB ---
    with tab2:
        st.subheader("Historial de Tasas de Cambio")
        
        # 1. Add Rate
        with st.expander("➕ Registrar Nueva Tasa"):
            c1, c2 = st.columns(2)
            with c1:
                manual_rate = st.number_input("Tasa de Venta (Lps)", min_value=1.0, step=0.0001, format="%.4f")
            with c2:
                st.write("")
                st.write("")
                if st.button("Guardar Tasa"):
                    if database.update_exchange_rate(manual_rate):
                        st.success("Tasa registrada.")
                        st.rerun()
        
        # 2. View History
        rates = database.get_exchange_rate_history()
        if rates:
            df_rates = pd.DataFrame(rates)
            
            # Simple Chart
            st.line_chart(df_rates.set_index("rate_date")["rate_value"])
            
            # Table
            st.dataframe(df_rates, use_container_width=True, hide_index=True)
        else:
            st.info("No hay historial de tasas.")

    # --- QUOTE CONFIG TAB ---
    with tab3:
        st.subheader("Personalización de Cotizaciones")
        st.info("Esta información aparecerá fija en todas las cotizaciones generadas.")
        
        current_header = database.get_config('quote_header')
        current_footer = database.get_config('quote_footer')
        
        with st.form("quote_config_form"):
            new_header = st.text_area("Encabezado (Nombre, RTN, Dirección, etc.)", value=current_header, height=150)
            new_footer = st.text_area("Pie de Página (Términos, Agradecimiento, etc.)", value=current_footer, height=100)
            
            if st.form_submit_button("Guardar Configuración", type="primary"):
                database.set_config('quote_header', new_header)
                database.set_config('quote_footer', new_footer)
                st.success("Configuración guardada exitosamente.")
                st.rerun()

