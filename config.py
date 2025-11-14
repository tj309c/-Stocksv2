"""
Investment Dashboard Configuration
"""
import os
from datetime import timedelta
from pathlib import Path

# ==================== PATHS ====================
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
CACHE_DIR = DATA_DIR / "cache"
DB_PATH = DATA_DIR / "market_data.db"

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
CACHE_DIR.mkdir(exist_ok=True)

# ==================== API KEYS ====================
# Set these as environment variables or in .env file
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID", "")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET", "")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "InvestmentDashboard/1.0")

# ==================== CACHE SETTINGS ====================
CACHE_EXPIRY = {
    "realtime": timedelta(minutes=5),      # Prices, quotes
    "options": timedelta(minutes=5),       # Option chains
    "hourly": timedelta(hours=1),          # Sentiment, trends
    "daily": timedelta(days=1),            # Fundamentals, financials
    "weekly": timedelta(days=7),           # Company info, sectors
}

# ==================== DATA SOURCES ====================
DATA_SOURCES = {
    "prices": ["yahoo", "marketwatch"],
    "options": ["yahoo", "barchart"],
    "fundamentals": ["yahoo", "marketwatch"],
    "sentiment": ["reddit", "stocktwits", "google_trends"],
    "crypto": ["yahoo", "coinmarketcap"],
    "news": ["yahoo", "finviz"],
}

# ==================== DEFAULT SETTINGS ====================
DEFAULT_TICKER = "META"
DEFAULT_CRYPTOS = ["BTC-USD", "ETH-USD", "XRP-USD"]
DEFAULT_LOOKBACK_DAYS = 365
DEFAULT_FORECAST_DAYS = 30

# ==================== VALUATION PARAMETERS ====================
VALUATION_PARAMS = {
    "risk_free_rate": 0.045,  # Current 10Y Treasury
    "market_risk_premium": 0.065,
    "terminal_growth_rate": 0.025,
    "wacc_iterations": 1000,  # Monte Carlo iterations
    "dcf_scenarios": ["bear", "base", "bull"],
    "confidence_weights": {
        "dcf": 0.30,
        "technical": 0.20,
        "sentiment": 0.15,
        "options_flow": 0.15,
        "multiples": 0.10,
        "momentum": 0.10,
    }
}

# ==================== TECHNICAL INDICATORS ====================
TECHNICAL_INDICATORS = {
    "momentum": ["RSI", "MACD", "Stochastic", "Williams %R"],
    "trend": ["SMA", "EMA", "Bollinger Bands", "Ichimoku"],
    "volume": ["OBV", "Volume Profile", "Money Flow"],
    "volatility": ["ATR", "Bollinger Width", "Keltner Channel"],
}

# ==================== OPTIONS SETTINGS ====================
OPTIONS_CONFIG = {
    "min_volume": 100,
    "min_oi": 500,
    "unusual_volume_threshold": 2.0,  # 2x average
    "iv_percentile_period": 252,  # Trading days
    "greeks_to_calculate": ["delta", "gamma", "theta", "vega", "rho"],
    "strategies": [
        "covered_call", "cash_secured_put", "iron_condor",
        "butterfly", "straddle", "strangle", "calendar_spread"
    ],
}

# ==================== PATTERN DETECTION ====================
CHART_PATTERNS = [
    "head_shoulders", "inverse_head_shoulders",
    "cup_handle", "double_top", "double_bottom",
    "triangle_ascending", "triangle_descending",
    "wedge_rising", "wedge_falling",
    "flag", "pennant", "channel",
]

# ==================== UI CONFIGURATION ====================
UI_CONFIG = {
    "theme": "dark",
    "chart_height": 500,
    "page_title": "🎯 Smart Investment Dashboard",
    "page_icon": "📈",
    "layout": "wide",
    "sidebar_state": "expanded",
}

# ==================== COLOR SCHEME ====================
COLORS = {
    "primary": "#00D4FF",      # Cyan
    "success": "#00FF88",      # Green
    "danger": "#FF3860",       # Red
    "warning": "#FFB700",      # Orange
    "info": "#3273DC",         # Blue
    "dark": "#1A1A1A",         # Dark background
    "light": "#F5F5F5",        # Light text
    "chart_bg": "#0E1117",     # Chart background
    "bullish": "#00FF88",
    "bearish": "#FF3860",
    "neutral": "#FFB700",
}

# ==================== GOOD BUY THRESHOLDS ====================
GOOD_BUY_CRITERIA = {
    "min_confidence_score": 70,  # Minimum score to flag as "good buy"
    "dcf_discount_required": 0.15,  # 15% below intrinsic value
    "rsi_oversold": 30,
    "iv_percentile_low": 20,  # Options are cheap
    "sentiment_divergence": 0.3,  # Sentiment improving vs price
    "volume_surge": 1.5,  # 50% above average
    "support_proximity": 0.02,  # Within 2% of support
}

# ==================== BACKTESTING ====================
BACKTEST_CONFIG = {
    "initial_capital": 100000,
    "position_size": 0.1,  # 10% per position
    "max_positions": 10,
    "stop_loss": 0.05,  # 5% stop loss
    "take_profit": 0.15,  # 15% take profit
    "commission": 0.001,  # 0.1% per trade
    "slippage": 0.001,  # 0.1% slippage
}

# ==================== ERROR MESSAGES ====================
ERROR_MESSAGES = {
    "no_data": "⚠️ Unable to fetch data. Please check your internet connection.",
    "invalid_ticker": "❌ Invalid ticker symbol. Please enter a valid symbol.",
    "cache_error": "⚠️ Cache error. Fetching fresh data...",
    "api_limit": "⚠️ API rate limit reached. Using cached data.",
    "calculation_error": "❌ Calculation error. Please try again.",
}

# ==================== LOGGING ====================
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": "dashboard.log",
}
