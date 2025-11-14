"""
StocksV2 Dashboard - Main Entry Point (Refactored)
Professional stock, options, and crypto analysis platform

New Features:
- Organized project structure (src/ directory)
- Centralized configuration and constants
- Comprehensive logging system
- Performance tracking
- Better error handling
- Type hints throughout
"""
import sys
from pathlib import Path

# Setup project paths
PROJECT_ROOT = Path(__file__).parent
SRC_DIR = PROJECT_ROOT / "src"
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(SRC_DIR))

import streamlit as st
from typing import Dict, Any

# Core imports
try:
    from src.core.logging import app_logger, log_app_start, perf_tracker
    from src.config import get_config
    HAS_NEW_STRUCTURE = True
except ImportError:
    # Fallback to old structure
    import logging
    app_logger = logging.getLogger(__name__)
    HAS_NEW_STRUCTURE = False
    def log_app_start(): pass
    class perf_tracker:
        @staticmethod
        def start(x): pass
        @staticmethod
        def end(x): pass

# Import existing modules (backward compatible)
from theme_manager import apply_theme, show_theme_toggle
from dashboard_selector import show_selector, show_dashboard_switcher
from dashboard_stocks import show_stocks_dashboard
from dashboard_options import show_options_dashboard
from dashboard_crypto import show_crypto_dashboard
from dashboard_advanced import show_advanced_dashboard
from dashboard_portfolio import show_portfolio_dashboard
from debug_tools import show_debug_panel

# Import analysis engines
from analysis_engine import (
    ValuationEngine,
    TechnicalAnalyzer,
    GoodBuyAnalyzer,
    OptionsAnalyzer
)
from data_fetcher import MarketDataFetcher

# Import sentiment analyzer
try:
    from sentiment_analyzer import SentimentAnalyzer
except ImportError:
    # Create a dummy sentiment analyzer if not available
    class SentimentAnalyzer:
        def get_stocktwits_sentiment(self, ticker):
            return {"error": "Sentiment analysis not available"}
        def get_news_sentiment(self, ticker):
            return []

# Page config
st.set_page_config(
    page_title="StocksV2 Dashboard - Professional Analysis",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

def init_components() -> Dict[str, Any]:
    """
    Initialize all analysis components
    
    Returns:
        Dictionary of initialized components
    """
    perf_tracker.start("component_init")
    
    try:
        components = {
            "fetcher": MarketDataFetcher(),
            "valuation": ValuationEngine(),
            "technical": TechnicalAnalyzer(),
            "goodbuy": GoodBuyAnalyzer(),
            "sentiment": SentimentAnalyzer(),
            "options": OptionsAnalyzer(),
        }
        
        app_logger.info("All components initialized successfully")
        perf_tracker.end("component_init")
        return components
        
    except Exception as e:
        app_logger.error(f"Component initialization failed: {e}")
        st.error(f"⚠️ Error initializing components: {e}")
        perf_tracker.end("component_init")
        return {}

def main():
    """Main application entry point"""
    # Log application start
    log_app_start()
    perf_tracker.start("app_render")
    
    # Show new structure notification in sidebar
    if HAS_NEW_STRUCTURE:
        with st.sidebar:
            st.success("✅ Using optimized structure")
    
    # Theme toggle in sidebar
    with st.sidebar:
        dark_mode = show_theme_toggle()
    
    # Apply theme
    apply_theme(dark_mode)
    
    # Initialize components
    if "components" not in st.session_state:
        with st.spinner("🚀 Initializing analysis engines..."):
            st.session_state.components = init_components()
    
    components = st.session_state.components
    
    # Debug panel in sidebar (if enabled)
    if HAS_NEW_STRUCTURE:
        config = get_config()
        if config.get("features.debug_panel", False):
            with st.sidebar:
                show_debug_panel()
    else:
        # Show debug panel for old structure
        with st.sidebar:
            with st.expander("🔧 Debug Tools"):
                show_debug_panel()
    
    # Show dashboard switcher in sidebar if on a dashboard
    if "current_page" in st.session_state and st.session_state.current_page != "home":
        with st.sidebar:
            show_dashboard_switcher()
    
    # Route to appropriate page
    current_page = st.session_state.get("current_page", "home")
    
    try:
        if current_page == "home":
            show_selector()
        elif current_page == "stocks":
            show_stocks_dashboard(components)
        elif current_page == "options":
            show_options_dashboard(components)
        elif current_page == "crypto":
            show_crypto_dashboard(components, ticker=st.session_state.get("current_crypto", "BTC-USD"))
        elif current_page == "advanced":
            show_advanced_dashboard(components, ticker=st.session_state.get("advanced_ticker", "SPY"))
        elif current_page == "portfolio":
            show_portfolio_dashboard(components)
        else:
            st.error(f"Unknown page: {current_page}")
            show_selector()
            
    except Exception as e:
        app_logger.error(f"Error rendering page {current_page}: {e}", exc_info=True)
        st.error(f"⚠️ Error loading dashboard: {e}")
        st.info("Click below to return to home")
        if st.button("🏠 Return to Home"):
            st.session_state.current_page = "home"
            st.rerun()
    
    perf_tracker.end("app_render")
    
    # Show performance metrics in sidebar (debug mode only)
    if HAS_NEW_STRUCTURE:
        config = get_config()
        if config.is_debug:
            with st.sidebar:
                with st.expander("⚡ Performance"):
                    metrics = perf_tracker.get_metrics()
                    for operation, data in metrics.items():
                        if data.get("duration"):
                            st.metric(operation, f"{data['duration']:.3f}s")

if __name__ == "__main__":
    main()
