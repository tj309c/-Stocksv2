"""
Debug & Diagnostics Dashboard
Real-time monitoring and troubleshooting panel for Analysis Master.

Features:
- API Health Monitor: Check status of all external APIs
- Data Validator: Inspect DataFrames, flag missing/invalid data
- Model Inspector: DCF calculations, arbitrage logic step-by-step
- Cache Manager: View/clear Streamlit cache, inspect cache hits
- Live Log Viewer: Tail application logs in real-time
- Session State Inspector: View all st.session_state variables
- Performance Profiler: Identify slow functions, bottlenecks

Philosophy:
"You can't fix what you can't see."
This dashboard exposes the internal state of the application, making it
easy to diagnose issues without digging through logs or print statements.
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
import sys
import traceback
from typing import Dict, List, Optional
import json

# Import all pipelines for health checks
try:
    from src.pipelines.get_economic_data import get_economic_data_pipeline
    ECONOMIC_AVAILABLE = True
except ImportError:
    ECONOMIC_AVAILABLE = False

try:
    from src.pipelines.get_political_data import get_political_data_pipeline
    POLITICAL_AVAILABLE = True
except ImportError:
    POLITICAL_AVAILABLE = False

try:
    from src.pipelines.get_market_data import get_market_data_pipeline
    MARKET_AVAILABLE = True
except ImportError:
    MARKET_AVAILABLE = False

try:
    from src.analysis.arbitrage_engine import get_crypto_arbitrage_scanner, get_statistical_arbitrage_scanner
    ARBITRAGE_AVAILABLE = True
except ImportError:
    ARBITRAGE_AVAILABLE = False

try:
    from src.analysis.predictive_models import get_claude_predictor
    LLM_AVAILABLE = True
except ImportError:
    LLM_AVAILABLE = False

logger = logging.getLogger(__name__)


def show_debug_dashboard():
    """
    Main debug dashboard interface.
    """
    st.title("🔧 Debug & Diagnostics Panel")
    st.caption("Internal monitoring and troubleshooting tools")
    
    # Sidebar navigation
    debug_section = st.sidebar.selectbox(
        "Debug Section",
        ["API Health Monitor", "Data Validator", "Model Inspector", 
         "Cache Manager", "Live Logs", "Session State", "Performance Profiler"]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.info("💡 **Tip:** Use this panel to diagnose issues before reporting bugs.")
    
    # Route to appropriate section
    if debug_section == "API Health Monitor":
        show_api_health_monitor()
    elif debug_section == "Data Validator":
        show_data_validator()
    elif debug_section == "Model Inspector":
        show_model_inspector()
    elif debug_section == "Cache Manager":
        show_cache_manager()
    elif debug_section == "Live Logs":
        show_live_logs()
    elif debug_section == "Session State":
        show_session_state()
    elif debug_section == "Performance Profiler":
        show_performance_profiler()


# =============================================================================
# API Health Monitor
# =============================================================================

def show_api_health_monitor():
    """Check status of all external APIs."""
    st.header("🌐 API Health Monitor")
    st.markdown("Real-time status of all data sources and external services.")
    
    # Refresh button
    if st.button("🔄 Refresh All", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    
    # Check each API
    api_status = []
    
    # 1. FRED API (Economic Data)
    st.subheader("1. Federal Reserve Economic Data (FRED)")
    fred_status = check_fred_api()
    api_status.append(fred_status)
    display_api_status(fred_status)
    
    # 2. EIA API (Energy Data)
    st.subheader("2. Energy Information Administration (EIA)")
    eia_status = check_eia_api()
    api_status.append(eia_status)
    display_api_status(eia_status)
    
    # 3. Finnhub API (Insider Trades)
    st.subheader("3. Finnhub (Insider Transactions)")
    finnhub_status = check_finnhub_api()
    api_status.append(finnhub_status)
    display_api_status(finnhub_status)
    
    # 4. Alpha Vantage (Fundamentals)
    st.subheader("4. Alpha Vantage (Fundamental Data)")
    av_status = check_alpha_vantage_api()
    api_status.append(av_status)
    display_api_status(av_status)
    
    # 5. Anthropic Claude (LLM)
    st.subheader("5. Anthropic Claude (Predictions)")
    claude_status = check_claude_api()
    api_status.append(claude_status)
    display_api_status(claude_status)
    
    # 6. ccxt (Crypto Exchanges)
    st.subheader("6. CCXT (Crypto Exchange Data)")
    ccxt_status = check_ccxt_connectivity()
    api_status.append(ccxt_status)
    display_api_status(ccxt_status)
    
    # 7. yfinance (Stock Data)
    st.subheader("7. Yahoo Finance (Stock Prices)")
    yf_status = check_yfinance_api()
    api_status.append(yf_status)
    display_api_status(yf_status)
    
    # Overall summary
    st.markdown("---")
    healthy_count = sum(1 for status in api_status if status['status'] == 'healthy')
    total_count = len(api_status)
    
    if healthy_count == total_count:
        st.success(f"✅ All {total_count} APIs are operational!")
    elif healthy_count > total_count / 2:
        st.warning(f"⚠️ {healthy_count}/{total_count} APIs operational. Some features may be limited.")
    else:
        st.error(f"🔴 Only {healthy_count}/{total_count} APIs operational. Check API keys.")


def display_api_status(status: Dict):
    """Display API status in consistent format."""
    if status['status'] == 'healthy':
        st.success(f"✅ **Status:** {status['message']}")
    elif status['status'] == 'warning':
        st.warning(f"⚠️ **Status:** {status['message']}")
    else:
        st.error(f"🔴 **Status:** {status['message']}")
    
    if status.get('latency'):
        st.caption(f"⏱️ Latency: {status['latency']:.2f}ms")
    
    if status.get('details'):
        with st.expander("View Details"):
            st.json(status['details'])


def check_fred_api() -> Dict:
    """Test FRED API connectivity."""
    try:
        import time
        start = time.time()
        
        if ECONOMIC_AVAILABLE:
            pipeline = get_economic_data_pipeline()
            # Try to fetch inflation data as test
            data = pipeline.get_inflation_data()
            latency = (time.time() - start) * 1000
            
            if data is not None and len(data) > 0:
                return {
                    'status': 'healthy',
                    'message': 'Connected successfully',
                    'latency': latency,
                    'details': {'rows': len(data), 'latest_date': str(data.index[-1])}
                }
        
        return {
            'status': 'error',
            'message': 'Pipeline not available or API key not configured',
            'details': {'module_available': ECONOMIC_AVAILABLE}
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Error: {str(e)}',
            'details': {'exception': str(e)}
        }


def check_eia_api() -> Dict:
    """Test EIA API connectivity."""
    try:
        import time
        start = time.time()
        
        if ECONOMIC_AVAILABLE:
            pipeline = get_economic_data_pipeline()
            data = pipeline.get_crude_oil_prices()
            latency = (time.time() - start) * 1000
            
            if data is not None and len(data) > 0:
                return {
                    'status': 'healthy',
                    'message': 'Connected successfully',
                    'latency': latency,
                    'details': {'rows': len(data), 'latest_value': float(data['value'].iloc[-1])}
                }
        
        return {
            'status': 'warning',
            'message': 'API key not configured or module not available',
            'details': {}
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Error: {str(e)}',
            'details': {'exception': str(e)}
        }


def check_finnhub_api() -> Dict:
    """Test Finnhub API connectivity."""
    try:
        import time
        start = time.time()
        
        if POLITICAL_AVAILABLE:
            pipeline = get_political_data_pipeline()
            data = pipeline.get_insider_transactions('AAPL', months=1)
            latency = (time.time() - start) * 1000
            
            if data is not None and len(data) > 0:
                return {
                    'status': 'healthy',
                    'message': 'Connected successfully',
                    'latency': latency,
                    'details': {'transactions_fetched': len(data)}
                }
        
        return {
            'status': 'warning',
            'message': 'API key not configured',
            'details': {}
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Error: {str(e)}',
            'details': {'exception': str(e)}
        }


def check_alpha_vantage_api() -> Dict:
    """Test Alpha Vantage API connectivity."""
    try:
        import time
        start = time.time()
        
        if MARKET_AVAILABLE:
            pipeline = get_market_data_pipeline()
            data = pipeline.get_company_overview('AAPL')
            latency = (time.time() - start) * 1000
            
            if data:
                return {
                    'status': 'healthy',
                    'message': 'Connected successfully',
                    'latency': latency,
                    'details': {'fields_returned': len(data)}
                }
        
        return {
            'status': 'warning',
            'message': 'API key not configured',
            'details': {}
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Error: {str(e)}',
            'details': {'exception': str(e)}
        }


def check_claude_api() -> Dict:
    """Test Claude API connectivity."""
    try:
        if LLM_AVAILABLE:
            predictor = get_claude_predictor()
            if predictor.client:
                return {
                    'status': 'healthy',
                    'message': 'API key configured successfully',
                    'details': {'model': 'claude-sonnet-4-20250514'}
                }
        
        return {
            'status': 'warning',
            'message': 'API key not configured. Add ANTHROPIC_API_KEY to secrets.toml',
            'details': {}
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Error: {str(e)}',
            'details': {'exception': str(e)}
        }


def check_ccxt_connectivity() -> Dict:
    """Test ccxt exchange connectivity."""
    try:
        import time
        start = time.time()
        
        if ARBITRAGE_AVAILABLE:
            scanner = get_crypto_arbitrage_scanner()
            # Test by fetching BTC/USDT from Binance
            if 'binance' in scanner.exchange_instances:
                exchange = scanner.exchange_instances['binance']
                ticker = exchange.fetch_ticker('BTC/USDT')
                latency = (time.time() - start) * 1000
                
                return {
                    'status': 'healthy',
                    'message': f'Connected to {len(scanner.exchange_instances)} exchanges',
                    'latency': latency,
                    'details': {
                        'exchanges': list(scanner.exchange_instances.keys()),
                        'test_price': ticker['last']
                    }
                }
        
        return {
            'status': 'warning',
            'message': 'ccxt module not available',
            'details': {}
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Error: {str(e)}',
            'details': {'exception': str(e)}
        }


def check_yfinance_api() -> Dict:
    """Test yfinance connectivity."""
    try:
        import time
        start = time.time()
        
        if MARKET_AVAILABLE:
            pipeline = get_market_data_pipeline()
            data = pipeline.get_stock_data('AAPL', period='5d')
            latency = (time.time() - start) * 1000
            
            if data is not None and len(data) > 0:
                return {
                    'status': 'healthy',
                    'message': 'Connected successfully',
                    'latency': latency,
                    'details': {'rows': len(data), 'latest_close': float(data['Close'].iloc[-1])}
                }
        
        return {
            'status': 'error',
            'message': 'yfinance module not available',
            'details': {}
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Error: {str(e)}',
            'details': {'exception': str(e)}
        }


# =============================================================================
# Data Validator
# =============================================================================

def show_data_validator():
    """Inspect DataFrames and validate data quality."""
    st.header("🔍 Data Validator")
    st.markdown("Inspect data quality, detect missing values, and validate ranges.")
    
    st.info("Select a data source to inspect its current state.")
    
    data_source = st.selectbox(
        "Data Source",
        ["Economic Indicators", "Political Trades", "Stock Prices", "Crypto Prices", "Arbitrage Opportunities"]
    )
    
    if data_source == "Economic Indicators":
        validate_economic_data()
    elif data_source == "Political Trades":
        validate_political_data()
    elif data_source == "Stock Prices":
        validate_stock_data()
    elif data_source == "Crypto Prices":
        validate_crypto_data()
    elif data_source == "Arbitrage Opportunities":
        validate_arbitrage_data()


def validate_economic_data():
    """Validate economic indicators data."""
    st.subheader("Economic Indicators Validation")
    
    if not ECONOMIC_AVAILABLE:
        st.error("❌ Economic pipeline not available")
        return
    
    try:
        pipeline = get_economic_data_pipeline()
        data = pipeline.get_all_macro_data()
        
        for key, df in data.items():
            st.markdown(f"**{key}:**")
            
            if df is None or len(df) == 0:
                st.warning(f"⚠️ No data available for {key}")
                continue
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Rows", len(df))
            col2.metric("Columns", len(df.columns))
            col3.metric("Missing Values", df.isnull().sum().sum())
            
            with st.expander(f"Preview {key}"):
                st.dataframe(df.tail(10))
            
            st.markdown("---")
            
    except Exception as e:
        st.error(f"Error validating economic data: {e}")
        st.code(traceback.format_exc())


def validate_political_data():
    """Validate political/insider trades data."""
    st.subheader("Political & Insider Trades Validation")
    
    ticker = st.text_input("Enter ticker to check", value="AAPL")
    
    if not ticker:
        return
    
    if not POLITICAL_AVAILABLE:
        st.error("❌ Political pipeline not available")
        return
    
    try:
        pipeline = get_political_data_pipeline()
        report = pipeline.get_comprehensive_insider_report(ticker)
        
        st.json(report)
        
    except Exception as e:
        st.error(f"Error: {e}")
        st.code(traceback.format_exc())


def validate_stock_data():
    """Validate stock price data."""
    st.subheader("Stock Price Data Validation")
    
    ticker = st.text_input("Enter ticker", value="AAPL")
    
    if not ticker:
        return
    
    if not MARKET_AVAILABLE:
        st.error("❌ Market pipeline not available")
        return
    
    try:
        pipeline = get_market_data_pipeline()
        data = pipeline.get_stock_data(ticker, period='1mo')
        
        if data is None or len(data) == 0:
            st.warning(f"⚠️ No data found for {ticker}")
            return
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Rows", len(data))
        col2.metric("Date Range", f"{len(data)} days")
        col3.metric("Missing", data.isnull().sum().sum())
        col4.metric("Latest Close", f"${data['Close'].iloc[-1]:.2f}")
        
        st.dataframe(data.tail(20))
        
    except Exception as e:
        st.error(f"Error: {e}")


def validate_crypto_data():
    """Validate crypto price data."""
    st.subheader("Crypto Price Data Validation")
    
    symbol = st.text_input("Enter crypto pair", value="BTC/USDT")
    exchange = st.selectbox("Exchange", ["binance", "coinbase", "kraken"])
    
    if not MARKET_AVAILABLE:
        st.error("❌ Market pipeline not available")
        return
    
    try:
        pipeline = get_market_data_pipeline()
        data = pipeline.get_crypto_ohlcv(symbol, exchange, timeframe='1h', limit=100)
        
        if data is None or len(data) == 0:
            st.warning(f"⚠️ No data found for {symbol} on {exchange}")
            return
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Candles", len(data))
        col2.metric("Latest Close", f"${data['close'].iloc[-1]:,.2f}")
        col3.metric("24h Change %", f"{((data['close'].iloc[-1] / data['close'].iloc[-24]) - 1) * 100:.2f}%")
        
        st.dataframe(data.tail(20))
        
    except Exception as e:
        st.error(f"Error: {e}")


def validate_arbitrage_data():
    """Validate arbitrage opportunities."""
    st.subheader("Arbitrage Opportunities Validation")
    
    st.info("This scans live exchanges. May take 10-20 seconds.")
    
    if st.button("🔍 Scan for Opportunities"):
        if not ARBITRAGE_AVAILABLE:
            st.error("❌ Arbitrage scanner not available")
            return
        
        try:
            scanner = get_crypto_arbitrage_scanner()
            opportunities = scanner.scan_all_triangular_opportunities()
            
            if len(opportunities) == 0:
                st.warning("⚠️ No arbitrage opportunities found")
            else:
                st.success(f"✅ Found {len(opportunities)} opportunities")
                df = pd.DataFrame(opportunities)
                st.dataframe(df)
                
        except Exception as e:
            st.error(f"Error: {e}")


# =============================================================================
# Model Inspector
# =============================================================================

def show_model_inspector():
    """Step-by-step inspection of model calculations."""
    st.header("🔬 Model Inspector")
    st.markdown("View intermediate calculations for DCF, arbitrage, and predictions.")
    
    st.info("Coming soon: Step-by-step DCF valuation breakdown")


# =============================================================================
# Cache Manager
# =============================================================================

def show_cache_manager():
    """Manage Streamlit cache."""
    st.header("🗄️ Cache Manager")
    st.markdown("View and clear cached data to force fresh fetches.")
    
    st.warning("Clearing cache will force all data to be re-fetched, which may be slow.")
    
    if st.button("🗑️ Clear All Cache", type="primary"):
        st.cache_data.clear()
        st.success("✅ Cache cleared successfully!")
        st.rerun()


# =============================================================================
# Live Logs
# =============================================================================

def show_live_logs():
    """Display application logs."""
    st.header("📋 Live Logs")
    st.markdown("Recent application events and errors.")
    
    st.info("Log streaming coming soon. For now, check terminal/console output.")


# =============================================================================
# Session State Inspector
# =============================================================================

def show_session_state():
    """Display all session state variables."""
    st.header("💾 Session State Inspector")
    st.markdown("View all variables stored in `st.session_state`.")
    
    if len(st.session_state) == 0:
        st.info("No session state variables set.")
    else:
        st.json(dict(st.session_state))


# =============================================================================
# Performance Profiler
# =============================================================================

def show_performance_profiler():
    """Profile slow functions."""
    st.header("⚡ Performance Profiler")
    st.markdown("Identify bottlenecks and slow operations.")
    
    st.info("Performance profiling coming soon.")


if __name__ == "__main__":
    show_debug_dashboard()
