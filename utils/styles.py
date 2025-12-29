import streamlit as st

def load_css():
    """
    Spotify-inspired Dark Mode Theme for REDMIL Quoter Pro
    Features: Dark backgrounds, Spotify green accents, smooth animations, pill-shaped buttons
    """
    st.markdown("""
        <style>
            /* ========================================
               SPOTIFY DARK MODE - GLOBAL THEME
            ======================================== */
            
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
            
            /* Global Styles */
            html, body, [class*="css"], .stApp {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
                background-color: #121212 !important;
                color: #FFFFFF !important;
            }
            
            /* Main Container */
            .main .block-container {
                padding-top: 2rem !important;
                padding-bottom: 3rem !important;
                max-width: 100% !important;
            }
            
            /* ========================================
               SIDEBAR - SPOTIFY STYLE (NON-FIXED)
            ======================================== */
            
            [data-testid="stSidebar"] {
                background-color: #000000 !important;
                border-right: 1px solid #282828 !important;
            }
            
            [data-testid="stSidebar"] > div:first-child {
                background-color: #000000 !important;
            }
            
            /* Sidebar Text - Better Legibility */
            [data-testid="stSidebar"] * {
                color: #B3B3B3 !important;
            }
            
            [data-testid="stSidebar"] h2,
            [data-testid="stSidebar"] h3,
            [data-testid="stSidebar"] .stMarkdown strong {
                color: #FFFFFF !important;
                font-weight: 700 !important;
            }
            
            /* Sidebar Menu Items - Readable Style */
            [data-testid="stSidebar"] .stRadio > div {
                gap: 0.5rem;
            }
            
            [data-testid="stSidebar"] .stRadio label {
                background-color: transparent !important;
                padding: 0.75rem 1rem !important;
                border-radius: 6px !important;
                transition: all 0.2s ease !important;
                cursor: pointer !important;
                color: #B3B3B3 !important;
                font-weight: 500 !important;
            }
            
            [data-testid="stSidebar"] .stRadio label:hover {
                background-color: #282828 !important;
                color: #FFFFFF !important;
            }
            
            /* Selected Menu Item */
            [data-testid="stSidebar"] .stRadio label[data-checked="true"] {
                background-color: #282828 !important;
                color: #1DB954 !important;
                font-weight: 700 !important;
            }
            
            /* Radio button circle */
            [data-testid="stSidebar"] .stRadio input[type="radio"] {
                accent-color: #1DB954 !important;
            }
            
            /* ========================================
               SPOTIFY GREEN BUTTONS (PILL STYLE)
            ======================================== */
            
            /* Primary Buttons (Guardar, Imprimir) */
            .stButton > button[kind="primary"],
            .stButton > button[type="primary"],
            button[kind="primary"] {
                background: linear-gradient(135deg, #1ED760 0%, #1DB954 100%) !important;
                color: #000000 !important;
                font-weight: 700 !important;
                font-size: 0.95rem !important;
                padding: 0.75rem 2rem !important;
                border-radius: 500px !important; /* Pill shape */
                border: none !important;
                text-transform: none !important;
                letter-spacing: 0.5px !important;
                transition: all 0.3s cubic-bezier(0.3, 0, 0.5, 1) !important;
                box-shadow: 0 4px 12px rgba(29, 185, 84, 0.3) !important;
            }
            
            .stButton > button[kind="primary"]:hover {
                background: linear-gradient(135deg, #1FDF64 0%, #1ED760 100%) !important;
                transform: scale(1.04) !important;
                box-shadow: 0 6px 20px rgba(29, 185, 84, 0.4) !important;
            }
            
            .stButton > button[kind="primary"]:active {
                transform: scale(0.98) !important;
            }
            
            /* Secondary Buttons */
            .stButton > button {
                background-color: transparent !important;
                color: #FFFFFF !important;
                font-weight: 600 !important;
                padding: 0.65rem 1.5rem !important;
                border-radius: 500px !important;
                border: 1px solid #535353 !important;
                transition: all 0.2s ease !important;
            }
            
            .stButton > button:hover {
                background-color: #282828 !important;
                border-color: #FFFFFF !important;
                transform: scale(1.02) !important;
            }
            
            /* ========================================
               CARDS - SPOTIFY STYLE
            ======================================== */
            
            .bento-card {
                background: #181818 !important;
                border-radius: 12px !important;
                padding: 24px !important;
                border: 1px solid #282828 !important;
                box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5) !important;
                height: 100%;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            }
            
            .bento-card:hover {
                background: #202020 !important;
                transform: translateY(-4px) !important;
                box-shadow: 0 12px 32px rgba(0, 0, 0, 0.6) !important;
                border-color: #1DB954 !important;
            }
            
            /* Metrics */
            .metric-value {
                font-size: 2.5rem !important;
                font-weight: 800 !important;
                color: #FFFFFF !important;
                letter-spacing: -0.02em !important;
                margin-top: 8px !important;
            }
            
            .metric-label {
                font-size: 0.85rem !important;
                font-weight: 600 !important;
                color: #B3B3B3 !important;
                text-transform: uppercase !important;
                letter-spacing: 0.1em !important;
            }
            
            .metric-delta {
                font-size: 0.875rem !important;
                font-weight: 500 !important;
                margin-top: 6px !important;
            }
            
            .delta-pos { color: #1DB954 !important; }
            .delta-neg { color: #E22134 !important; }
            
            /* ========================================
               TABLES - HOVER EFFECTS
            ======================================== */
            
            /* DataFrame Styling */
            [data-testid="stDataFrame"] {
                background-color: #181818 !important;
                border: 1px solid #282828 !important;
                border-radius: 8px !important;
                overflow: hidden !important;
            }
            
            /* Table Headers */
            [data-testid="stDataFrame"] thead tr th {
                background-color: #000000 !important;
                color: #B3B3B3 !important;
                font-weight: 700 !important;
                text-transform: uppercase !important;
                font-size: 0.75rem !important;
                letter-spacing: 0.1em !important;
                padding: 1rem !important;
                border-bottom: 1px solid #282828 !important;
            }
            
            /* Table Rows */
            [data-testid="stDataFrame"] tbody tr {
                background-color: #181818 !important;
                transition: all 0.2s ease !important;
            }
            
            [data-testid="stDataFrame"] tbody tr:hover {
                background-color: #282828 !important;
                transform: scale(1.01) !important;
                box-shadow: 0 2px 8px rgba(29, 185, 84, 0.2) !important;
            }
            
            [data-testid="stDataFrame"] tbody tr td {
                color: #FFFFFF !important;
                padding: 1rem !important;
                border-bottom: 1px solid #282828 !important;
            }
            
            /* ========================================
               INPUTS & FORMS
            ======================================== */
            
            /* Text Inputs */
            .stTextInput input,
            .stNumberInput input,
            .stTextArea textarea,
            .stSelectbox select {
                background-color: #121212 !important;
                border: 1px solid #535353 !important;
                border-radius: 4px !important;
                color: #FFFFFF !important;
                padding: 0.75rem !important;
                transition: all 0.2s ease !important;
            }
            
            .stTextInput input:focus,
            .stNumberInput input:focus,
            .stTextArea textarea:focus {
                border-color: #1DB954 !important;
                box-shadow: 0 0 0 1px #1DB954 !important;
            }
            
            .stTextInput label,
            .stNumberInput label,
            .stTextArea label,
            .stSelectbox label {
                color: #B3B3B3 !important;
                font-weight: 600 !important;
                font-size: 0.875rem !important;
            }
            
            /* Selectbox */
            .stSelectbox > div > div {
                background-color: #121212 !important;
                border: 1px solid #535353 !important;
                border-radius: 4px !important;
            }
            
            /* ========================================
               ANIMATIONS
            ======================================== */
            
            /* Fade In Animation */
            @keyframes fadeIn {
                from { 
                    opacity: 0; 
                    transform: translateY(20px); 
                }
                to { 
                    opacity: 1; 
                    transform: translateY(0); 
                }
            }
            
            /* Slide From Right (Framer Motion style) */
            @keyframes slideInRight {
                from {
                    opacity: 0;
                    transform: translateX(100px);
                }
                to {
                    opacity: 1;
                    transform: translateX(0);
                }
            }
            
            /* Slide From Left */
            @keyframes slideInLeft {
                from {
                    opacity: 0;
                    transform: translateX(-100px);
                }
                to {
                    opacity: 1;
                    transform: translateX(0);
                }
            }
            
            /* Scale In */
            @keyframes scaleIn {
                from {
                    opacity: 0;
                    transform: scale(0.9);
                }
                to {
                    opacity: 1;
                    transform: scale(1);
                }
            }
            
            /* Animation Classes */
            .animate-enter {
                animation: fadeIn 0.6s cubic-bezier(0.4, 0, 0.2, 1) forwards;
            }
            
            .animate-slide-right {
                animation: slideInRight 0.7s cubic-bezier(0.4, 0, 0.2, 1) forwards;
            }
            
            .animate-slide-left {
                animation: slideInLeft 0.7s cubic-bezier(0.4, 0, 0.2, 1) forwards;
            }
            
            .animate-scale {
                animation: scaleIn 0.5s cubic-bezier(0.4, 0, 0.2, 1) forwards;
            }
            
            /* ========================================
               CUSTOM SCROLLBAR - SPOTIFY STYLE
            ======================================== */
            
            ::-webkit-scrollbar {
                width: 12px;
                height: 12px;
            }
            
            ::-webkit-scrollbar-track {
                background: #121212;
            }
            
            ::-webkit-scrollbar-thumb {
                background: #535353;
                border-radius: 6px;
                border: 3px solid #121212;
            }
            
            ::-webkit-scrollbar-thumb:hover {
                background: #B3B3B3;
            }
            
            /* ========================================
               TITLES & HEADINGS
            ======================================== */
            
            h1, h2, h3, h4, h5, h6 {
                color: #FFFFFF !important;
                font-weight: 800 !important;
                letter-spacing: -0.02em !important;
            }
            
            h1 {
                font-size: 3rem !important;
                margin-bottom: 1rem !important;
            }
            
            h2 {
                font-size: 2rem !important;
                margin-bottom: 0.75rem !important;
            }
            
            h3 {
                font-size: 1.5rem !important;
                margin-bottom: 0.5rem !important;
            }
            
            /* ========================================
               ALERTS & MESSAGES
            ======================================== */
            
            .stAlert {
                background-color: #181818 !important;
                border: 1px solid #282828 !important;
                border-radius: 8px !important;
                color: #FFFFFF !important;
            }
            
            .stSuccess {
                background-color: rgba(29, 185, 84, 0.1) !important;
                border-color: #1DB954 !important;
            }
            
            .stError {
                background-color: rgba(226, 33, 52, 0.1) !important;
                border-color: #E22134 !important;
            }
            
            .stWarning {
                background-color: rgba(255, 184, 0, 0.1) !important;
                border-color: #FFB800 !important;
            }
            
            .stInfo {
                background-color: rgba(29, 185, 84, 0.05) !important;
                border-color: #535353 !important;
            }
            
            /* ========================================
               EXPANDERS
            ======================================== */
            
            .streamlit-expanderHeader {
                background-color: #181818 !important;
                border: 1px solid #282828 !important;
                border-radius: 8px !important;
                color: #FFFFFF !important;
                font-weight: 600 !important;
            }
            
            .streamlit-expanderHeader:hover {
                background-color: #202020 !important;
                border-color: #1DB954 !important;
            }
            
            /* ========================================
               TOOLTIPS
            ======================================== */
            
            [data-baseweb="tooltip"] {
                background-color: #282828 !important;
                color: #FFFFFF !important;
                border-radius: 4px !important;
                font-size: 0.875rem !important;
            }
            
            /* ========================================
               MISC
            ======================================== */
            
            /* Divider */
            hr {
                border-color: #282828 !important;
            }
            
            /* Links */
            a {
                color: #1DB954 !important;
                text-decoration: none !important;
                transition: color 0.2s ease !important;
            }
            
            a:hover {
                color: #1ED760 !important;
                text-decoration: underline !important;
            }
            
            /* Code Blocks */
            code {
                background-color: #181818 !important;
                color: #1DB954 !important;
                padding: 0.2rem 0.4rem !important;
                border-radius: 4px !important;
                font-family: 'Monaco', 'Menlo', monospace !important;
            }
            
            /* Smooth Scroll */
            html {
                scroll-behavior: smooth;
            }
            
        </style>
    """, unsafe_allow_html=True)

def card(content):
    """Renders a Spotify-style dark card with content"""
    st.markdown(f"<div class='bento-card'>{content}</div>", unsafe_allow_html=True)
