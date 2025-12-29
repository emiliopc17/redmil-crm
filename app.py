import streamlit as st
import auth
import database
import time
from views import dashboard, inventory, clients, quotes, admin, quote_generator
from utils import styles

# Initialize Database
database.init_db()

# Set page config
st.set_page_config(
    page_title="REDMIL Quoter Pro",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- SESSION & TIMEOUT LOGIC (JS INJECTION) ---
# This script handles cookies for persistence across refreshes
# and monitors inactivity for the 10-minute timeout.

# Initialize Session State FIRST
if 'user' not in st.session_state:
    st.session_state.user = None
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Dashboard"

# Cookie-based session restoration
session_restore_js = """
<script>
    // Helper functions for cookies
    function setCookie(name, value, days) {
        const expires = new Date();
        expires.setTime(expires.getTime() + (days * 24 * 60 * 60 * 1000));
        document.cookie = name + '=' + encodeURIComponent(value) + ';expires=' + expires.toUTCString() + ';path=/';
    }
    
    function getCookie(name) {
        const nameEQ = name + "=";
        const ca = document.cookie.split(';');
        for(let i = 0; i < ca.length; i++) {
            let c = ca[i];
            while (c.charAt(0) == ' ') c = c.substring(1, c.length);
            if (c.indexOf(nameEQ) == 0) return decodeURIComponent(c.substring(nameEQ.length, c.length));
        }
        return null;
    }
    
    function deleteCookie(name) {
        document.cookie = name + '=; expires=Thu, 01 Jan 1970 00:00:01 GMT; path=/;';
    }
    
    // Timeout logic
    const TIMEOUT_MS = 10 * 60 * 1000; // 10 minutes
    const WARN_MS = 9 * 60 * 1000;   // Warn at 9 minutes
    let timeoutHandle;
    let warnHandle;

    function resetTimers() {
        clearTimeout(timeoutHandle);
        clearTimeout(warnHandle);
        
        warnHandle = setTimeout(() => {
            if (confirm("Tu sesión expirará en 1 minuto por inactividad. ¿Deseas continuar?")) {
                resetTimers();
            }
        }, WARN_MS);

        timeoutHandle = setTimeout(() => {
            alert("Sesión cerrada por inactividad.");
            deleteCookie("redmil_user");
            window.location.reload();
        }, TIMEOUT_MS);
    }

    // Listen for messages from Streamlit
    window.addEventListener('message', (event) => {
        if (event.data.type === 'persist_user') {
            setCookie("redmil_user", JSON.stringify(event.data.user), 1); // 1 day
            resetTimers();
        }
        if (event.data.type === 'logout_user') {
            deleteCookie("redmil_user");
        }
    });

    // Activity Listeners
    ['mousedown', 'mousemove', 'keydown', 'scroll', 'touchstart'].forEach(name => {
        document.addEventListener(name, resetTimers);
    });
    
    // Start timers if user is logged in
    const savedUser = getCookie("redmil_user");
    if (savedUser) {
        resetTimers();
    }
</script>
"""

# Inject the session JS
from streamlit.components.v1 import html
html(session_restore_js, height=0)

# Check if we need to restore session from cookies
restore_session_js = """
<script>
    function getCookie(name) {
        const nameEQ = name + "=";
        const ca = document.cookie.split(';');
        for(let i = 0; i < ca.length; i++) {
            let c = ca[i];
            while (c.charAt(0) == ' ') c = c.substring(1, c.length);
            if (c.indexOf(nameEQ) == 0) return decodeURIComponent(c.substring(nameEQ.length, c.length));
        }
        return null;
    }
    
    const savedUser = getCookie("redmil_user");
    if (savedUser) {
        // Return the user data
        window.parent.postMessage({
            type: 'streamlit:setComponentValue',
            value: savedUser
        }, '*');
    }
</script>
"""

from streamlit.components.v1 import components
restored_user_json = html(restore_session_js, height=0)

# Try to restore from cookie if not logged in
if not st.session_state.user:
    # Use a simpler approach - check via JS and set a flag
    check_cookie_js = """
    <script>
        function getCookie(name) {
            const nameEQ = name + "=";
            const ca = document.cookie.split(';');
            for(let i = 0; i < ca.length; i++) {
                let c = ca[i];
                while (c.charAt(0) == ' ') c = c.substring(1, c.length);
                if (c.indexOf(nameEQ) == 0) return decodeURIComponent(c.substring(nameEQ.length, c.length));
            }
            return null;
        }
        
        const savedUser = getCookie("redmil_user");
        if (savedUser && savedUser !== "null") {
            // Redirect with query param to restore session
            const url = new URL(window.location.href);
            if (!url.searchParams.has('restore_session')) {
                url.searchParams.set('restore_session', savedUser);
                window.location.href = url.toString();
            }
        }
    </script>
    """
    html(check_cookie_js, height=0)
    
    # Check query params for session restoration
    query_params = st.query_params
    if "restore_session" in query_params:
        try:
            import json
            user_data = json.loads(query_params["restore_session"])
            st.session_state.user = user_data
            # Clean up URL
            st.query_params.clear()
            st.rerun()
        except Exception as e:
            pass


def login():
    # Spotify Dark Mode Login
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
            
            /* Spotify Dark Background */
            .stApp {
                background: #121212 !important;
            }
            
            /* Hide Streamlit default elements */
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            
            /* Remove default padding */
            .main .block-container {
                padding-top: 4rem !important;
                padding-bottom: 2rem !important;
                max-width: 100% !important;
            }
            
            /* Login wrapper - Spotify Card Style */
            .login-wrapper {
                width: 450px;
                padding: 48px;
                border: none;
                border-radius: 12px;
                text-align: center;
                background: #181818;
                box-shadow: 0 16px 48px rgba(0, 0, 0, 0.7);
                margin: 0 auto;
            }
            
            .login-title {
                font-size: 3rem;
                color: #1DB954;
                font-weight: 900;
                margin-bottom: 8px;
                font-family: 'Inter', sans-serif;
                letter-spacing: -0.02em;
            }
            
            .login-subtitle {
                font-size: 1rem;
                color: #B3B3B3;
                margin-bottom: 40px;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.1em;
            }
            
            /* Hide default streamlit form styling */
            .stForm {
                border: none !important;
                padding: 0 !important;
            }
            
            /* Input styling - Spotify Style */
            .stTextInput > div > div > input {
                background: #121212 !important;
                border: 2px solid #535353 !important;
                border-radius: 4px !important;
                color: #FFFFFF !important;
                font-size: 1rem !important;
                padding: 14px !important;
                transition: all 0.2s ease !important;
                font-family: 'Inter', sans-serif !important;
            }
            
            .stTextInput > div > div > input::placeholder {
                color: #727272 !important;
            }
            
            .stTextInput > div > div > input:focus {
                border-color: #1DB954 !important;
                background: #181818 !important;
                box-shadow: 0 0 0 3px rgba(29, 185, 84, 0.1) !important;
            }
            
            .stTextInput > label {
                color: #FFFFFF !important;
                font-weight: 700 !important;
                font-size: 0.875rem !important;
                margin-bottom: 8px !important;
                font-family: 'Inter', sans-serif !important;
                text-transform: uppercase !important;
                letter-spacing: 0.05em !important;
            }
            
            /* Button styling - Spotify Green Pill */
            .stButton > button {
                background: linear-gradient(135deg, #1ED760 0%, #1DB954 100%) !important;
                color: #000000 !important;
                font-size: 1rem !important;
                font-weight: 800 !important;
                padding: 16px 32px !important;
                border-radius: 500px !important;
                border: none !important;
                width: 100% !important;
                margin-top: 24px !important;
                text-transform: uppercase !important;
                letter-spacing: 2px !important;
                font-family: 'Inter', sans-serif !important;
                transition: all 0.3s cubic-bezier(0.3, 0, 0.5, 1) !important;
                box-shadow: 0 8px 24px rgba(29, 185, 84, 0.4) !important;
            }
            
            .stButton > button:hover {
                background: linear-gradient(135deg, #1FDF64 0%, #1ED760 100%) !important;
                transform: scale(1.05) !important;
                box-shadow: 0 12px 32px rgba(29, 185, 84, 0.5) !important;
            }
            
            .stButton > button:active {
                transform: scale(0.98) !important;
            }
            
            /* Error message styling - Spotify Style */
            .stAlert {
                background: rgba(226, 33, 52, 0.1) !important;
                color: #FFFFFF !important;
                border: 1px solid #E22134 !important;
                border-radius: 8px !important;
            }
            
            /* Animation */
            @keyframes fadeInUp {
                from {
                    opacity: 0;
                    transform: translateY(40px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            .login-wrapper {
                animation: fadeInUp 0.8s cubic-bezier(0.4, 0, 0.2, 1);
            }
        </style>
    """, unsafe_allow_html=True)
    
    # Add spacing to center vertically
    st.markdown("<br>" * 2, unsafe_allow_html=True)
    
    # Create centered login form
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("""
            <div class="login-wrapper">
                <div class="login-title">REDMIL</div>
                <div class="login-subtitle">Quoter Pro</div>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("Usuario", placeholder="Ingrese su usuario")
            password = st.text_input("Contraseña", type="password", placeholder="Ingrese su contraseña")
            submit = st.form_submit_button("Iniciar Sesión", use_container_width=True)
            
            if submit:
                user = auth.authenticate_user(username, password)
                if user:
                    user_dict = dict(user)
                    st.session_state.user = user_dict
                    # Tell JS to save this user
                    import json
                    st.components.v1.html(f"""
                        <script>
                            window.parent.postMessage({{type: 'persist_user', user: {json.dumps(user_dict)}}}, '*');
                        </script>
                    """, height=0)
                    st.rerun()
                else:
                    st.error("❌ Usuario o contraseña incorrectos")


def logout():
    st.session_state.user = None
    st.session_state.current_page = "Dashboard"
    # Tell JS to clear localStorage
    st.components.v1.html("""
        <script>
            window.parent.postMessage({type: 'logout_user'}, '*');
        </script>
    """, height=0)
    st.rerun()

def main():
    styles.load_css()
    
    if 'rates_updated' not in st.session_state:
        from utils import forex
        success, rate = forex.update_rates_from_api()
        if success:
            st.toast(f"💱 Tasa actualizada: L. {rate}", icon="✅")
        st.session_state.rates_updated = True
    
    if not st.session_state.user:
        login()
        return

    # Sidebar Navigation
    with st.sidebar:
        st.markdown(f"## 👋 Hola, {st.session_state.user['full_name']}")
        st.markdown(f"**Rol:** {st.session_state.user['role'].upper()}")
        st.markdown("---")
        
        menu_options = ["Dashboard", "Inventario", "Generar Cotización (React)", "Clientes", "Cotizaciones"]
        
        if st.session_state.user['role'] == 'admin':
            menu_options.append("Configuración")
            
        selection = st.radio("Navegación", menu_options, index=menu_options.index(st.session_state.current_page) if st.session_state.current_page in menu_options else 0)
        
        if selection != st.session_state.current_page:
            if selection == "Generar Cotización (React)":
                st.session_state.quote_items = []
                st.session_state.temp_client = None
            st.session_state.current_page = selection
            st.rerun()

        st.markdown("---")
        if st.button("🚪 Cerrar Sesión", use_container_width=True):
            logout()

    # Routing
    st.markdown("<div class='animate-enter'>", unsafe_allow_html=True)
    if st.session_state.current_page == "Dashboard":
        dashboard.show()
    elif st.session_state.current_page == "Inventario":
        inventory.show()
    elif st.session_state.current_page == "Generar Cotización (React)":
        quote_generator.show()
    elif st.session_state.current_page == "Clientes":
        clients.show()
    elif st.session_state.current_page == "Cotizaciones":
        quotes.show()
    elif st.session_state.current_page == "Configuración":
        admin.show()
    else:
        dashboard.show()
    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
