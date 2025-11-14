"""
Smart Investment Dashboard - APE EDITION 🚀
A zero-cost, high-speed investment analysis platform
Now with 3 dashboards: Stocks, Options, and Crypto!
With comprehensive debugging and light/dark mode support!
"""
import streamlit as st
from datetime import datetime

# Import custom modules
from data_fetcher import MarketDataFetcher, SentimentScraper
from analysis_engine import ValuationEngine, TechnicalAnalyzer, GoodBuyAnalyzer, OptionsAnalyzer

# Import dashboards
from dashboard_selector import show_selector, show_dashboard_switcher
from dashboard_stocks import show_stocks_dashboard
from dashboard_options import show_options_dashboard
from dashboard_crypto import show_crypto_dashboard
from dashboard_advanced import show_advanced_dashboard
from dashboard_portfolio import show_portfolio_dashboard

# Import utilities
from theme_manager import apply_theme, show_theme_toggle
from debug_tools import show_debug_panel

# ========== PAGE CONFIGURATION ==========
st.set_page_config(
    page_title="🚀 APE TRADING HQ - WHERE RETARDS BECOME RICH",
    page_icon="🦍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== THEME APPLICATION ==========
# Show theme toggle and apply selected theme (defaults to light)
dark_mode = show_theme_toggle()
apply_theme(dark_mode)

# ========== OLD CSS REMOVED - NOW HANDLED BY THEME MANAGER ==========
# Custom CSS is now generated dynamically by theme_manager.py
# This ensures consistent theming across light and dark modes

# ========== SESSION STATE INITIALIZATION ==========
# Unified session state for ticker management across all dashboards
def init_session_state():
    """Initialize session state with unified ticker management"""
    defaults = {
        "dashboard_selected": False,
        "selected_dashboard": None,
        "current_ticker": "META",           # Main stock dashboard
        "current_options_ticker": "SPY",    # Options dashboard
        "current_crypto": "BTC-USD",        # Crypto dashboard
        "advanced_ticker": "SPY",           # Advanced analytics
        "portfolio_tickers": ["AAPL", "MSFT", "GOOGL"],  # Portfolio
        "ticker_history": [],               # Track ticker changes
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# ========== INITIALIZE COMPONENTS ==========
@st.cache_resource
def init_components():
    """Initialize all components - cached for performance"""
    return {
        "fetcher": MarketDataFetcher(),
        "sentiment": SentimentScraper(),
        "valuation": ValuationEngine(),
        "technical": TechnicalAnalyzer(),
        "goodbuy": GoodBuyAnalyzer(),
        "options": OptionsAnalyzer()
    }

components = init_components()

# ========== DASHBOARD ROUTER ==========
# Check if a dashboard has been selected
if not st.session_state.dashboard_selected or st.session_state.selected_dashboard is None:
    # Show dashboard selector
    show_selector()
    
    # Show debug panel in sidebar even on selector
    show_debug_panel()
else:
    # Show selected dashboard with sidebar switcher
    selected = st.session_state.selected_dashboard
    
    # Display dashboard switcher in sidebar
    show_dashboard_switcher()
    
    # Show debug panel in sidebar
    show_debug_panel()
    
    # Route to correct dashboard
    if selected == "stocks":
        show_stocks_dashboard(components, st.session_state.current_ticker)
    elif selected == "options":
        show_options_dashboard(components, st.session_state.current_options_ticker)
    elif selected == "crypto":
        show_crypto_dashboard(components, ticker=st.session_state.get("current_crypto", "BTC-USD"))
    
    elif selected == "advanced":
        show_advanced_dashboard(components, ticker=st.session_state.get("advanced_ticker", "SPY"))
    
    elif selected == "portfolio":
        show_portfolio_dashboard(components)
    
    elif selected == "debug":
        # Import and show debug dashboard
        from src.dashboards.dashboard_debug import show_debug_dashboard
        show_debug_dashboard()
    else:
        # Fallback
        st.error("Unknown dashboard selected. Returning to menu...")
        st.session_state.dashboard_selected = False
        st.rerun()
