import streamlit as st
import database
import pandas as pd

def show():
    st.title("👥 Gestión de Clientes")
    
    tab1, tab2 = st.tabs(["📂 Directorio", "➕ Nuevo Cliente"])
    
    with tab1:
        st.markdown("### Directorio de Clientes")
        search_client = st.text_input("Buscar Cliente", placeholder="Nombre, RTN o Teléfono")
        
        clients = database.get_all_clients()
        
        if clients:
            df = pd.DataFrame(clients)
            # Filter
            if search_client:
                mask = df.apply(lambda row: search_client.lower() in str(row).lower(), axis=1)
                df = df[mask]
                
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No hay clientes registrados.")
        
    with tab2:
        st.markdown("### Registrar Nuevo Cliente")
        with st.form("new_client_form"):
            c1, c2 = st.columns(2)
            with c1:
                name = st.text_input("Nombre Completo / Razón Social")
                rtn = st.text_input("RTN")
            with c2:
                phone = st.text_input("Teléfono")
                email = st.text_input("Correo Electrónico")
            
            address = st.text_area("Dirección")
            
            submitted = st.form_submit_button("Guardar Cliente")
            if submitted:
                if not name:
                    st.error("El nombre es obligatorio.")
                else:
                    data = {
                        "full_name": name,
                        "rtn_id": rtn,
                        "phone": phone,
                        "email": email,
                        "address": address
                    }
                    if database.create_client(data):
                        st.success("Cliente guardado exitosamente.")
                        st.rerun()
                    else:
                        st.error("Error al guardar cliente. Verifique si el RTN ya existe.")
