"""
Performance Configuration Module
Manages Fast Mode vs Deep Mode settings globally across the app.

Fast Mode Goals:
- Initial load: < 30 seconds (from 5 min baseline)
- Tab switch: < 1 second (from 30 sec baseline)
- Ticker change: < 30 seconds (from 5 min baseline)

Deep Mode Goals:
- Full data with ETA displayed to user
- Comprehensive analysis with progress indicators
"""
import streamlit as st
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@dataclass
class PerformanceMode:
    """Performance mode configuration"""
    name: str
    historical_period: str  # yfinance period
    cache_ttl_multiplier: float  # Multiply base TTLs by this
    enable_sentiment_scraping: bool
    enable_options_chain: bool
    enable_institutional: bool
    enable_economic_data: bool
    enable_political_data: bool
    max_sentiment_sources: int  # Number of sentiment sources (Reddit, News, etc.)
    parallel_fetch: bool
    show_eta: bool
    description: str


# ============================================================================
# MODE DEFINITIONS
# ============================================================================

FAST_MODE = PerformanceMode(
    name="Fast Mode ⚡",
    historical_period="3mo",  # 3 months instead of 1 year
    cache_ttl_multiplier=3.0,  # Cache 3x longer (e.g., 5min → 15min)
    enable_sentiment_scraping=False,  # Skip sentiment scraping, use cached only
    enable_options_chain=False,  # Skip options analysis per user request
    enable_institutional=False,  # Skip institutional holdings per user request
    enable_economic_data=True,  # Keep economic data (lightweight, cached 24hr)
    enable_political_data=False,  # Skip Congressional trades
    max_sentiment_sources=1,  # Use only cached sentiment if available
    parallel_fetch=True,
    show_eta=False,  # Fast mode doesn't need ETA
    description="Optimized for speed. Uses cached data, reduced historical periods. Target: <30s load."
)

DEEP_MODE = PerformanceMode(
    name="Deep Mode 🔬",
    historical_period="5y",  # 5 years of data
    cache_ttl_multiplier=0.5,  # Cache half as long (fresher data)
    enable_sentiment_scraping=True,  # Full sentiment analysis
    enable_options_chain=True,  # Full options chain with Greeks
    enable_institutional=True,  # Institutional holdings
    enable_economic_data=True,  # All economic indicators
    enable_political_data=True,  # Congressional trades
    max_sentiment_sources=3,  # Reddit, News, StockTwits
    parallel_fetch=True,
    show_eta=True,  # Show estimated time for deep analysis
    description="Comprehensive analysis with all data sources. Real-time scraping enabled. ETA: 2-5 minutes."
)

# Default mode
DEFAULT_MODE = FAST_MODE


# ============================================================================
# API RATE LIMITERS
# ============================================================================

# Rate limits based on free tier documentation
API_RATE_LIMITS = {
    # yfinance: No official limit, but recommended 2000 req/hour (GitHub issues)
    "yfinance": {
        "requests_per_hour": 2000,
        "requests_per_minute": 33,
        "burst_limit": 10  # Max concurrent requests
    },
    
    # Reddit API: 60 requests per minute (free tier)
    "reddit": {
        "requests_per_hour": 3600,
        "requests_per_minute": 60,
        "burst_limit": 5
    },
    
    # NewsAPI: 100 requests per day (free tier)
    "newsapi": {
        "requests_per_day": 100,
        "requests_per_hour": 4,  # Conservative to not hit daily limit
        "requests_per_minute": 1
    },
    
    # FRED: Unlimited (but be respectful)
    "fred": {
        "requests_per_hour": 1000,
        "requests_per_minute": 16,
        "burst_limit": 5
    },
    
    # BLS: 500 series per query, 500 daily requests
    "bls": {
        "requests_per_day": 500,
        "requests_per_hour": 20,
        "requests_per_minute": 2
    },
    
    # EIA: 5000 requests per day
    "eia": {
        "requests_per_day": 5000,
        "requests_per_hour": 200,
        "requests_per_minute": 10
    }
}


# ============================================================================
# ESTIMATED LOAD TIMES (seconds)
# ============================================================================

COMPONENT_ETA = {
    "fast_mode": {
        "stock_data": 2,  # Basic stock data (cached)
        "quote": 1,  # Real-time quote
        "fundamentals": 2,  # Fundamentals
        "sentiment_cached": 1,  # Cached sentiment only
        "economic_data": 1,  # Cached economic data
        "technical_analysis": 1,  # Chart analysis
        "total": 8  # Total estimate
    },
    "deep_mode": {
        "stock_data": 5,  # 5 years of data
        "quote": 1,
        "fundamentals": 3,
        "options_chain": 15,  # Greeks calculation for 6 expirations
        "institutional": 8,  # Institutional holdings
        "sentiment_scraping": 30,  # Reddit + News + StockTwits scraping
        "economic_data": 5,  # Fresh economic data
        "political_data": 10,  # Congressional trades
        "technical_analysis": 2,
        "total": 79  # Total estimate (~1.3 minutes)
    }
}


# ============================================================================
# SESSION STATE MANAGEMENT
# ============================================================================

def initialize_performance_mode():
    """Initialize performance mode in session state"""
    if "performance_mode" not in st.session_state:
        st.session_state.performance_mode = DEFAULT_MODE
        logger.info(f"Initialized performance mode: {DEFAULT_MODE.name}")


def get_current_mode() -> PerformanceMode:
    """Get the current performance mode"""
    initialize_performance_mode()
    return st.session_state.performance_mode


def set_performance_mode(mode: PerformanceMode):
    """Set the performance mode globally"""
    st.session_state.performance_mode = mode
    logger.info(f"Performance mode changed to: {mode.name}")


def toggle_performance_mode():
    """Toggle between Fast and Deep mode"""
    current = get_current_mode()
    if current.name == FAST_MODE.name:
        set_performance_mode(DEEP_MODE)
    else:
        set_performance_mode(FAST_MODE)


def is_fast_mode() -> bool:
    """Check if currently in fast mode"""
    return get_current_mode().name == FAST_MODE.name


def is_deep_mode() -> bool:
    """Check if currently in deep mode"""
    return get_current_mode().name == DEEP_MODE.name


# ============================================================================
# CACHE TTL CALCULATOR
# ============================================================================

def get_adjusted_ttl(base_ttl: int) -> int:
    """
    Get cache TTL adjusted for current performance mode.
    
    Args:
        base_ttl: Base TTL in seconds
        
    Returns:
        Adjusted TTL in seconds
    """
    mode = get_current_mode()
    adjusted = int(base_ttl * mode.cache_ttl_multiplier)
    return adjusted


# ============================================================================
# ETA CALCULATOR
# ============================================================================

def calculate_eta(components: List[str]) -> Dict:
    """
    Calculate estimated time to load based on current mode and components.
    
    Args:
        components: List of components to load (e.g., ['stock_data', 'sentiment_scraping'])
        
    Returns:
        Dict with eta_seconds, eta_formatted, breakdown
    """
    mode = get_current_mode()
    mode_key = "fast_mode" if is_fast_mode() else "deep_mode"
    
    eta_seconds = 0
    breakdown = {}
    
    for component in components:
        if component in COMPONENT_ETA[mode_key]:
            time = COMPONENT_ETA[mode_key][component]
            eta_seconds += time
            breakdown[component] = time
    
    # Format ETA
    if eta_seconds < 60:
        eta_formatted = f"{eta_seconds}s"
    else:
        minutes = eta_seconds // 60
        seconds = eta_seconds % 60
        eta_formatted = f"{minutes}m {seconds}s"
    
    return {
        "eta_seconds": eta_seconds,
        "eta_formatted": eta_formatted,
        "breakdown": breakdown,
        "mode": mode.name
    }


def get_dashboard_eta(dashboard_name: str) -> str:
    """Get estimated load time for a specific dashboard"""
    mode = get_current_mode()
    
    if dashboard_name == "stocks":
        if is_fast_mode():
            components = ["stock_data", "quote", "fundamentals", "sentiment_cached", "technical_analysis"]
        else:
            components = ["stock_data", "quote", "fundamentals", "options_chain", 
                         "institutional", "sentiment_scraping", "technical_analysis"]
    
    elif dashboard_name == "options":
        if is_fast_mode():
            return "Not available in Fast Mode"
        else:
            components = ["stock_data", "options_chain", "technical_analysis"]
    
    elif dashboard_name == "crypto":
        if is_fast_mode():
            components = ["stock_data", "quote", "technical_analysis"]
        else:
            components = ["stock_data", "quote", "sentiment_scraping", "technical_analysis"]
    
    elif dashboard_name == "advanced":
        if is_fast_mode():
            components = ["stock_data", "fundamentals", "economic_data", "technical_analysis"]
        else:
            components = ["stock_data", "fundamentals", "economic_data", 
                         "political_data", "sentiment_scraping", "technical_analysis"]
    
    else:
        return "N/A"
    
    eta = calculate_eta(components)
    return eta["eta_formatted"]


# ============================================================================
# MODE DISPLAY HELPERS
# ============================================================================

def show_performance_mode_indicator():
    """Display current performance mode in sidebar"""
    mode = get_current_mode()
    
    # Color-coded indicator
    if is_fast_mode():
        icon = "⚡"
        color = "green"
    else:
        icon = "🔬"
        color = "blue"
    
    st.sidebar.markdown(f"### {icon} {mode.name}")
    st.sidebar.caption(mode.description)
    
    # Mode toggle button
    toggle_label = "Switch to Deep Mode 🔬" if is_fast_mode() else "Switch to Fast Mode ⚡"
    if st.sidebar.button(toggle_label, key="performance_mode_toggle", use_container_width=True):
        toggle_performance_mode()
        st.rerun()
    
    st.sidebar.markdown("---")


def show_eta_indicator(dashboard_name: str):
    """Show estimated load time for current dashboard"""
    mode = get_current_mode()
    
    if mode.show_eta:
        eta = get_dashboard_eta(dashboard_name)
        st.info(f"⏱️ Estimated load time: **{eta}** ({mode.name})")


# ============================================================================
# FEATURE FLAGS
# ============================================================================

def should_fetch_sentiment() -> bool:
    """Check if sentiment scraping should be enabled"""
    return get_current_mode().enable_sentiment_scraping


def should_fetch_options() -> bool:
    """Check if options chain should be fetched"""
    return get_current_mode().enable_options_chain


def should_fetch_institutional() -> bool:
    """Check if institutional data should be fetched"""
    return get_current_mode().enable_institutional


def should_fetch_economic() -> bool:
    """Check if economic data should be fetched"""
    return get_current_mode().enable_economic_data


def should_fetch_political() -> bool:
    """Check if political data should be fetched"""
    return get_current_mode().enable_political_data


def get_historical_period() -> str:
    """Get the historical period for data fetching"""
    return get_current_mode().historical_period


def get_max_sentiment_sources() -> int:
    """Get max number of sentiment sources to query"""
    return get_current_mode().max_sentiment_sources


# ============================================================================
# USAGE TRACKING
# ============================================================================

class APIUsageTracker:
    """Track API usage to prevent hitting rate limits"""
    
    def __init__(self):
        if "api_usage" not in st.session_state:
            st.session_state.api_usage = {}
    
    def record_request(self, api_name: str):
        """Record an API request"""
        if api_name not in st.session_state.api_usage:
            st.session_state.api_usage[api_name] = {
                "count": 0,
                "last_reset": datetime.now()
            }
        
        st.session_state.api_usage[api_name]["count"] += 1
    
    def check_limit(self, api_name: str) -> bool:
        """Check if we can make another request without hitting limits"""
        if api_name not in API_RATE_LIMITS:
            return True  # No limit defined
        
        usage = st.session_state.api_usage.get(api_name, {"count": 0})
        limit = API_RATE_LIMITS[api_name].get("requests_per_minute", float('inf'))
        
        return usage["count"] < limit
    
    def get_usage_stats(self) -> Dict:
        """Get current API usage statistics"""
        return st.session_state.api_usage.copy()


# ============================================================================
# EXPORT
# ============================================================================

__all__ = [
    "PerformanceMode",
    "FAST_MODE",
    "DEEP_MODE",
    "initialize_performance_mode",
    "get_current_mode",
    "set_performance_mode",
    "toggle_performance_mode",
    "is_fast_mode",
    "is_deep_mode",
    "get_adjusted_ttl",
    "calculate_eta",
    "get_dashboard_eta",
    "show_performance_mode_indicator",
    "show_eta_indicator",
    "should_fetch_sentiment",
    "should_fetch_options",
    "should_fetch_institutional",
    "should_fetch_economic",
    "should_fetch_political",
    "get_historical_period",
    "get_max_sentiment_sources",
    "APIUsageTracker",
    "API_RATE_LIMITS"
]
