"""
Theme Manager for Light/Dark Mode Toggle
Handles CSS generation for both themes
"""
import streamlit as st

def get_light_theme_css():
    """Generate CSS for light theme"""
    return """
<style>
    /* Mobile responsive viewport */
    @viewport {
        width: device-width;
        zoom: 1.0;
    }
    
    /* Main app background - Light */
    .stApp {
        background: linear-gradient(180deg, #f5f7fa 0%, #ffffff 100%);
        color: #1a1a1a;
    }
    
    /* Mobile responsive font sizes */
    @media (max-width: 768px) {
        h1 { font-size: 1.5rem !important; }
        h2 { font-size: 1.25rem !important; }
        h3 { font-size: 1.1rem !important; }
        .stMetric { font-size: 0.9rem !important; }
    }
    
    /* Metrics styling - Light mode */
    [data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.9);
        border: 1px solid #00d4ff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s;
        color: #1a1a1a;
    }
    
    [data-testid="metric-container"]:hover {
        transform: scale(1.02);
        border-color: #00ff88;
    }
    
    /* Mobile responsive metrics */
    @media (max-width: 768px) {
        [data-testid="metric-container"] {
            padding: 10px;
            font-size: 0.85rem;
        }
    }
    
    /* Headers - Light mode */
    h1, h2, h3 {
        color: #0088cc !important;
        font-weight: 600 !important;
        text-shadow: 0 0 10px rgba(0, 136, 204, 0.1);
    }
    
    /* Info boxes - Light mode */
    .stAlert {
        background: rgba(0, 212, 255, 0.1);
        border-left: 4px solid #0088cc;
        animation: pulse 2s infinite;
        color: #1a1a1a;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.9; }
    }
    
    /* Mobile responsive alerts */
    @media (max-width: 768px) {
        .stAlert {
            font-size: 0.85rem;
            padding: 8px;
        }
    }
    
    /* Tabs - Light mode */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(240, 240, 240, 0.5);
        padding: 5px;
        border-radius: 10px;
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.8);
        color: #1a1a1a;
        border-radius: 5px;
        transition: all 0.3s;
        white-space: nowrap;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(0, 212, 255, 0.2);
    }
    
    .stTabs [aria-selected="true"] {
        background: #00d4ff;
        color: white;
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.5);
    }
    
    /* Mobile tab adjustments */
    @media (max-width: 768px) {
        .stTabs [data-baseweb="tab"] {
            font-size: 0.85rem;
            padding: 8px 12px;
        }
    }
    
    /* Sidebar - Light mode */
    .css-1d391kg, [data-testid="stSidebar"] {
        background: rgba(245, 247, 250, 0.95);
        color: #1a1a1a;
    }
    
    /* Buttons - Light mode */
    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s;
        background: white;
        color: #1a1a1a;
        border: 2px solid #00d4ff;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 212, 255, 0.4);
        background: #00d4ff;
        color: white;
    }
    
    /* Mobile button adjustments */
    @media (max-width: 768px) {
        .stButton > button {
            width: 100%;
            font-size: 0.9rem;
            padding: 8px 12px;
        }
    }
    
    /* Responsive columns */
    @media (max-width: 768px) {
        [data-testid="column"] {
            min-width: 100% !important;
            flex: 100% !important;
        }
    }
    
    /* Text colors for light mode */
    .stMarkdown, .stText, p, span {
        color: #1a1a1a;
    }
    
    /* Input fields */
    .stTextInput > div > div > input {
        background: white;
        color: #1a1a1a;
        border: 1px solid #ddd;
    }
    
    /* Select boxes */
    .stSelectbox > div > div {
        background: white;
        color: #1a1a1a;
    }
    
    /* Dataframes and tables */
    .stDataFrame, .stTable {
        background: white;
        color: #1a1a1a;
    }
    
    /* Tooltips - Fix black on black issue */
    [data-baseweb="tooltip"] {
        background-color: #1a1a1a !important;
        color: #ffffff !important;
        border: 1px solid #00d4ff !important;
    }
    
    [data-baseweb="tooltip"] div {
        background-color: #1a1a1a !important;
        color: #ffffff !important;
    }
    
    /* Tooltip arrow */
    [data-baseweb="tooltip"] [data-popper-arrow] {
        background-color: #1a1a1a !important;
    }
</style>
"""

def get_dark_theme_css():
    """Generate CSS for dark theme"""
    return """
<style>
    /* Mobile responsive viewport */
    @viewport {
        width: device-width;
        zoom: 1.0;
    }
    
    /* Main app background - Dark as my portfolio */
    .stApp {
        background: linear-gradient(180deg, #0e1117 0%, #1a1f2e 100%);
        color: #ffffff;
    }
    
    /* Mobile responsive font sizes */
    @media (max-width: 768px) {
        h1 { font-size: 1.5rem !important; }
        h2 { font-size: 1.25rem !important; }
        h3 { font-size: 1.1rem !important; }
        .stMetric { font-size: 0.9rem !important; }
    }
    
    /* Metrics styling - Gains are green, losses are... character building */
    [data-testid="metric-container"] {
        background: rgba(28, 31, 38, 0.8);
        border: 1px solid #00d4ff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 212, 255, 0.1);
        transition: transform 0.2s;
    }
    
    [data-testid="metric-container"]:hover {
        transform: scale(1.02);
        border-color: #00ff88;
    }
    
    /* Mobile responsive metrics */
    @media (max-width: 768px) {
        [data-testid="metric-container"] {
            padding: 10px;
            font-size: 0.85rem;
        }
    }
    
    /* Headers - Autism speaks in cyan */
    h1, h2, h3 {
        color: #00d4ff !important;
        font-weight: 600 !important;
        text-shadow: 0 0 10px rgba(0, 212, 255, 0.3);
    }
    
    /* Info boxes - For when you need copium */
    .stAlert {
        background: rgba(0, 212, 255, 0.1);
        border-left: 4px solid #00d4ff;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }
    
    /* Mobile responsive alerts */
    @media (max-width: 768px) {
        .stAlert {
            font-size: 0.85rem;
            padding: 8px;
        }
    }
    
    /* Tabs - Switch between your bad decisions */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(28, 31, 38, 0.5);
        padding: 5px;
        border-radius: 10px;
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(28, 31, 38, 0.8);
        color: #fff;
        border-radius: 5px;
        transition: all 0.3s;
        white-space: nowrap;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(0, 212, 255, 0.2);
    }
    
    .stTabs [aria-selected="true"] {
        background: #00d4ff;
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.5);
    }
    
    /* Mobile tab adjustments */
    @media (max-width: 768px) {
        .stTabs [data-baseweb="tab"] {
            font-size: 0.85rem;
            padding: 8px 12px;
        }
    }
    
    /* Sidebar - Your autism dashboard */
    .css-1d391kg, [data-testid="stSidebar"] {
        background: rgba(14, 17, 23, 0.95);
    }
    
    /* Buttons - For degenerate moves */
    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 212, 255, 0.4);
    }
    
    /* Mobile button adjustments */
    @media (max-width: 768px) {
        .stButton > button {
            width: 100%;
            font-size: 0.9rem;
            padding: 8px 12px;
        }
    }
    
    /* Responsive columns */
    @media (max-width: 768px) {
        [data-testid="column"] {
            min-width: 100% !important;
            flex: 100% !important;
        }
    }
    
    /* Tooltips - Fix readability (white text on dark background) */
    [data-baseweb="tooltip"] {
        background-color: #1a1f2e !important;
        color: #ffffff !important;
        border: 1px solid #00ff88 !important;
    }
    
    [data-baseweb="tooltip"] div {
        background-color: #1a1f2e !important;
        color: #ffffff !important;
    }
    
    /* Tooltip arrow */
    [data-baseweb="tooltip"] [data-popper-arrow] {
        background-color: #1a1f2e !important;
    }
</style>
"""

def apply_theme(dark_mode=False):
    """Apply the selected theme"""
    if dark_mode:
        st.markdown(get_dark_theme_css(), unsafe_allow_html=True)
    else:
        st.markdown(get_light_theme_css(), unsafe_allow_html=True)
    
    # Additional global CSS to fix all tooltip readability issues
    st.markdown("""
    <style>
        /* Fix Streamlit's help icon tooltips */
        [data-testid="stTooltipHoverTarget"] + div {
            background-color: rgba(26, 31, 46, 0.95) !important;
            color: white !important;
            border: 1px solid #00ff88 !important;
            padding: 8px 12px !important;
            border-radius: 6px !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
        }
        
        /* Fix tooltip content text */
        [data-testid="stTooltipHoverTarget"] + div * {
            color: white !important;
        }
        
        /* Ensure all help tooltips are readable */
        .stTooltip, [role="tooltip"] {
            background-color: rgba(26, 31, 46, 0.95) !important;
            color: white !important;
            border: 1px solid #00ff88 !important;
        }
    </style>
    """, unsafe_allow_html=True)

def show_theme_toggle():
    """Show theme toggle in sidebar"""
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🎨 Theme")
    
    # Initialize theme in session state
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = False  # Default to light mode
    
    # Toggle switch
    dark_mode = st.sidebar.toggle(
        "🌙 Dark Mode",
        value=st.session_state.dark_mode,
        help="Switch between light and dark themes"
    )
    
    # Update session state if changed
    if dark_mode != st.session_state.dark_mode:
        st.session_state.dark_mode = dark_mode
        st.rerun()
    
    return st.session_state.dark_mode
