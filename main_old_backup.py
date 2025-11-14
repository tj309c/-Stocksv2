"""
Smart Investment Dashboard - APE EDITION 🚀
A zero-cost, high-speed investment analysis platform
Now with 3 dashboards: Stocks, Options, and Crypto!
"""
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path

# Import custom modules
from data_fetcher import MarketDataFetcher, SentimentScraper
from analysis_engine import ValuationEngine, TechnicalAnalyzer, GoodBuyAnalyzer, OptionsAnalyzer

# Import dashboards
from dashboard_selector import show_selector, show_dashboard_switcher
from dashboard_stocks import show_stocks_dashboard
from dashboard_options import show_options_dashboard
from dashboard_crypto import show_crypto_dashboard

# ========== PAGE CONFIGURATION ==========
st.set_page_config(
    page_title="🚀 APE TRADING HQ",
    page_icon="🦍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for all dashboards
st.markdown("""
<style>
    /* Main app background */
    .stApp {
        background: linear-gradient(180deg, #0e1117 0%, #1a1f2e 100%);
    }
    
    /* Metrics styling */
    [data-testid="metric-container"] {
        background: rgba(28, 31, 38, 0.8);
        border: 1px solid #00d4ff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 212, 255, 0.1);
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #00d4ff !important;
        font-weight: 600 !important;
    }
    
    /* Info boxes */
    .stAlert {
        background: rgba(0, 212, 255, 0.1);
        border-left: 4px solid #00d4ff;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(28, 31, 38, 0.5);
        padding: 5px;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(28, 31, 38, 0.8);
        color: #fff;
        border-radius: 5px;
    }
    
    .stTabs [aria-selected="true"] {
        background: #00d4ff;
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ========== SESSION STATE INITIALIZATION ==========
if "dashboard_selected" not in st.session_state:
    st.session_state.dashboard_selected = False
if "selected_dashboard" not in st.session_state:
    st.session_state.selected_dashboard = None
if "current_ticker" not in st.session_state:
    st.session_state.current_ticker = "META"
if "current_options_ticker" not in st.session_state:
    st.session_state.current_options_ticker = "SPY"
if "current_crypto" not in st.session_state:
    st.session_state.current_crypto = "BTC-USD"

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
else:
    # Show selected dashboard with sidebar switcher
    selected = st.session_state.selected_dashboard
    
    # Display dashboard switcher in sidebar
    show_dashboard_switcher()
    
    # Route to correct dashboard
    if selected == "stocks":
        show_stocks_dashboard(components, st.session_state.current_ticker)
    elif selected == "options":
        show_options_dashboard(components, st.session_state.current_options_ticker)
    elif selected == "crypto":
        show_crypto_dashboard(components, st.session_state.current_crypto)
    else:
        # Fallback
        st.error("Unknown dashboard selected. Returning to menu...")
        st.session_state.dashboard_selected = False
        st.rerun()

# ========== ORIGINAL SIDEBAR CODE (DISABLED - Replaced by dashboard switcher) ==========
# with st.sidebar:
    st.markdown("# 🎯 Investment Dashboard")
    st.markdown("---")
    
    # Ticker input
    col1, col2 = st.columns([3, 1])
    with col1:
        ticker_input = st.text_input(
            "Enter Ticker Symbol",
            value=st.session_state.ticker,
            help="Enter a stock ticker (e.g., AAPL, MSFT, META)"
        ).upper()
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("📊 Analyze", type="primary"):
            if ticker_input:
                st.session_state.ticker = ticker_input
                st.session_state.last_update = datetime.now()
    
    # Update timer
    if st.session_state.last_update:
        elapsed = datetime.now() - st.session_state.last_update
        minutes = int(elapsed.total_seconds() / 60)
        seconds = int(elapsed.total_seconds() % 60)
        
        if minutes >= 5:
            st.warning(f"⏰ Data is {minutes}m old. Consider refreshing.")
        else:
            st.info(f"🔄 Last update: {minutes}m {seconds}s ago")
    
    st.markdown("---")
    
    # Quick Stats
    st.markdown("### 📈 Market Status")
    
    # Fetch market indices
    with st.spinner("Loading market data..."):
        try:
            spy = yf.Ticker("SPY").info
            qqq = yf.Ticker("QQQ").info
            
            col1, col2 = st.columns(2)
            with col1:
                spy_change = spy.get("regularMarketChangePercent", 0)
                st.metric(
                    "S&P 500",
                    f"${spy.get('regularMarketPrice', 0):.2f}",
                    f"{spy_change:.2f}%"
                )
            
            with col2:
                qqq_change = qqq.get("regularMarketChangePercent", 0)
                st.metric(
                    "NASDAQ",
                    f"${qqq.get('regularMarketPrice', 0):.2f}",
                    f"{qqq_change:.2f}%"
                )
        except:
            st.info("Market data unavailable")
    
    st.markdown("---")
    
    # Crypto Prices
    st.markdown("### 🪙 Crypto")
    try:
        btc = yf.Ticker("BTC-USD").info
        eth = yf.Ticker("ETH-USD").info
        
        col1, col2 = st.columns(2)
        with col1:
            btc_change = btc.get("regularMarketChangePercent", 0)
            st.metric(
                "BTC",
                f"${btc.get('regularMarketPrice', 0):,.0f}",
                f"{btc_change:.2f}%"
            )
        
        with col2:
            eth_change = eth.get("regularMarketChangePercent", 0)
            st.metric(
                "ETH",
                f"${eth.get('regularMarketPrice', 0):,.0f}",
                f"{eth_change:.2f}%"
            )
    except:
        st.info("Crypto data unavailable")
    
    st.markdown("---")
    st.markdown("### ⚙️ Settings")
    
    # Theme toggle (visual only)
    dark_mode = st.checkbox("🌙 Dark Mode", value=True)
    auto_refresh = st.checkbox("🔄 Auto Refresh (5 min)", value=False)
    
    # About section
    with st.expander("ℹ️ About"):
        st.markdown("""
        **Smart Investment Dashboard v1.0**
        
        A zero-cost, high-accuracy investment analysis platform using:
        - Real-time market data via yfinance
        - Advanced valuation models (DCF, Multiples)
        - Technical analysis & pattern detection
        - Sentiment analysis from social media
        - Options flow analysis
        - Buy signal detection with confidence scoring
        
        Built with ❤️ for retail investors
        """)

# ========== MAIN CONTENT AREA ==========
ticker = st.session_state.ticker

# Header
col1, col2, col3 = st.columns([2, 3, 2])
with col1:
    st.markdown(f"# {ticker}")
with col3:
    if st.button("🔄 Refresh Data", key="refresh_main"):
        st.session_state.last_update = datetime.now()
        st.rerun()

# Fetch all data
@st.cache_data(ttl=300)  # 5 minute cache
def fetch_all_data(ticker):
    """Fetch comprehensive data for ticker"""
    data = {}
    
    # Market data
    data["stock_data"] = components["fetcher"].get_stock_data(ticker)
    data["quote"] = components["fetcher"].get_realtime_quote(ticker)
    data["fundamentals"] = components["fetcher"].get_fundamentals(ticker)
    data["options"] = components["fetcher"].get_options_chain(ticker)
    data["institutional"] = components["fetcher"].get_institutional_data(ticker)
    
    # Sentiment
    data["sentiment"] = {
        "stocktwits": components["sentiment"].get_stocktwits_sentiment(ticker),
        "news": components["sentiment"].get_news_sentiment(ticker)
    }
    
    return data

# Load data
with st.spinner(f"Analyzing {ticker}..."):
    data = fetch_all_data(ticker)

# Process data
if data["stock_data"] and "history" in data["stock_data"]:
    df = pd.DataFrame(data["stock_data"]["history"])
    df.index = pd.to_datetime(df.index) if not isinstance(df.index, pd.DatetimeIndex) else df.index
else:
    df = pd.DataFrame()

info = data["stock_data"].get("info", {}) if data["stock_data"] else {}

# ========== GOOD BUY ANALYSIS (TOP SECTION) ==========
st.markdown("---")

# Run analysis
valuation = components["valuation"].calculate_dcf(data["fundamentals"], info)
if "error" in valuation:
    valuation = components["valuation"].calculate_multiples_valuation(info)

technical = components["technical"].analyze(df) if not df.empty else {}
sentiment = data["sentiment"]["stocktwits"]

buy_analysis = components["goodbuy"].analyze_buy_opportunity(
    ticker, valuation, technical, sentiment, info, df
)

# Display Buy Signal Card
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

current_price = buy_analysis["current_price"]
buy_low = buy_analysis["buy_range"]["low"]
buy_high = buy_analysis["buy_range"]["high"]
target = buy_analysis["target_price"]
confidence = buy_analysis["total_score"]

with col1:
    prev_close = info.get('previousClose', current_price)
    price_change = ((current_price - prev_close) / prev_close * 100) if prev_close > 0 else 0
    st.metric(
        "📍 Current Price",
        f"${current_price:.2f}",
        f"{price_change:.2f}%"
    )

with col2:
    color = "#00FF88" if confidence >= 70 else "#FFB700" if confidence >= 50 else "#FF3860"
    st.markdown(f"""
    <div style="background: {color}20; border: 2px solid {color}; padding: 10px; border-radius: 10px; text-align: center;">
        <h3 style="color: {color}; margin: 0;">🎯 GOOD BUY RANGE</h3>
        <h2 style="color: white; margin: 5px 0;">${buy_low:.2f} - ${buy_high:.2f}</h2>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.metric(
        "🎯 Target Price",
        f"${target:.2f}",
        f"+{((target - current_price) / current_price * 100):.1f}%"
    )

with col4:
    st.metric(
        "🔥 Confidence Score",
        f"{confidence:.0f}/100",
        buy_analysis["confidence"]
    )

# Buy Signals
if buy_analysis["signals"]:
    st.success(f"**Buy Signals:** {' | '.join(buy_analysis['signals'][:3])}")

# Recommendation Badge
rec = buy_analysis["recommendation"]
rec_color = "#00FF88" if rec == "STRONG BUY" else "#FFB700" if rec == "BUY" else "#FF3860"
st.markdown(f"""
<div style="background: {rec_color}20; border: 2px solid {rec_color}; padding: 15px; border-radius: 10px; text-align: center; margin: 20px 0;">
    <h1 style="color: {rec_color}; margin: 0;">{rec}</h1>
    <p style="color: white;">Risk/Reward Ratio: {buy_analysis['risk_reward_ratio']:.2f} | Stop Loss: ${buy_analysis['stop_loss']:.2f}</p>
</div>
""", unsafe_allow_html=True)

# ========== TABS ==========
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "📊 Overview",
    "💰 Valuation",
    "📈 Technical",
    "💬 Sentiment",
    "⚡ Options",
    "📰 News",
    "🏢 Institutional",
    "📉 Charts"
])

# ========== TAB 1: OVERVIEW ==========
with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Price Chart
        st.subheader("📈 Price Chart")
        
        if not df.empty:
            fig = make_subplots(
                rows=2, cols=1,
                shared_xaxes=True,
                row_heights=[0.7, 0.3],
                vertical_spacing=0.03
            )
            
            # Candlestick chart
            has_ohlc = all(col in df.columns for col in ['Open', 'High', 'Low', 'Close'])
            fig.add_trace(
                go.Candlestick(
                    x=df.index,
                    open=df['Open'] if has_ohlc else df['Close'],
                    high=df['High'] if has_ohlc else df['Close'],
                    low=df['Low'] if has_ohlc else df['Close'],
                    close=df['Close'],
                    name="OHLC"
                ),
                row=1, col=1
            )
            
            # Moving averages
            if len(df) >= 20:
                sma20 = df['Close'].rolling(20).mean()
                fig.add_trace(
                    go.Scatter(x=df.index, y=sma20, name="SMA20", line=dict(color="#00d4ff", width=1)),
                    row=1, col=1
                )
            
            if len(df) >= 50:
                sma50 = df['Close'].rolling(50).mean()
                fig.add_trace(
                    go.Scatter(x=df.index, y=sma50, name="SMA50", line=dict(color="#ff9500", width=1)),
                    row=1, col=1
                )
            
            # Volume
            if 'Open' in df.columns:
                colors = ['red' if row['Close'] < row['Open'] else 'green' for idx, row in df.iterrows()]
            else:
                colors = ['blue'] * len(df)
            
            fig.add_trace(
                go.Bar(x=df.index, y=df.get('Volume', 0), name="Volume", marker_color=colors),
                row=2, col=1
            )
            
            fig.update_layout(
                title=f"{ticker} Price & Volume",
                yaxis_title="Price ($)",
                yaxis2_title="Volume",
                template="plotly_dark",
                height=500,
                showlegend=True,
                hovermode='x unified'
            )
            
            fig.update_xaxes(rangeslider_visible=False)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No price data available")
    
    with col2:
        # Key Metrics
        st.subheader("📊 Key Metrics")
        
        if info:
            metrics_data = {
                "Market Cap": f"${info.get('marketCap', 0)/1e9:.2f}B" if info.get('marketCap', 0) > 0 else "N/A",
                "P/E Ratio": f"{info.get('trailingPE', 0):.2f}" if info.get('trailingPE', 0) > 0 else "N/A",
                "EPS": f"${info.get('trailingEps', 0):.2f}" if info.get('trailingEps', 0) > 0 else "N/A",
                "Dividend Yield": f"{info.get('dividendYield', 0)*100:.2f}%" if info.get('dividendYield', 0) > 0 else "N/A",
                "Beta": f"{info.get('beta', 1):.2f}",
                "52W High": f"${info.get('fiftyTwoWeekHigh', 0):.2f}",
                "52W Low": f"${info.get('fiftyTwoWeekLow', 0):.2f}",
                "Avg Volume": f"{info.get('averageVolume', 0)/1e6:.2f}M" if info.get('averageVolume', 0) > 0 else "N/A"
            }
            
            for metric, value in metrics_data.items():
                st.markdown(f"**{metric}:** {value}")
        
        # Score Breakdown
        st.subheader("🎯 Score Breakdown")
        
        scores_df = pd.DataFrame({
            'Factor': list(buy_analysis['scores'].keys()),
            'Score': list(buy_analysis['scores'].values())
        })
        
        fig = go.Figure(data=[
            go.Bar(
                x=scores_df['Score'],
                y=scores_df['Factor'],
                orientation='h',
                marker_color=['#00FF88' if s >= 70 else '#FFB700' if s >= 50 else '#FF3860' 
                             for s in scores_df['Score']]
            )
        ])
        
        fig.update_layout(
            title="Buy Signal Components",
            xaxis_title="Score",
            template="plotly_dark",
            height=300,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)

# ========== TAB 2: VALUATION ==========
with tab2:
    st.subheader("💰 Valuation Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if "error" not in valuation:
            st.markdown("### DCF Valuation")
            
            val_metrics = {
                "Fair Value": f"${valuation.get('fair_value', 0):.2f}",
                "Current Price": f"${valuation.get('current_price', 0):.2f}",
                "Upside/Downside": f"{valuation.get('upside', 0):.1f}%",
                "WACC": f"{valuation.get('wacc', 0):.2f}%",
                "Method": valuation.get('method', 'DCF')
            }
            
            for metric, value in val_metrics.items():
                st.markdown(f"**{metric}:** {value}")
            
            # Scenarios
            if "scenarios" in valuation:
                st.markdown("### Price Scenarios")
                scenarios_df = pd.DataFrame({
                    'Scenario': ['Bear', 'Base', 'Bull'],
                    'Price': [valuation['scenarios']['bear'], 
                             valuation['scenarios']['base'],
                             valuation['scenarios']['bull']]
                })
                
                fig = go.Figure(data=[
                    go.Bar(
                        x=scenarios_df['Scenario'],
                        y=scenarios_df['Price'],
                        marker_color=['#FF3860', '#FFB700', '#00FF88']
                    )
                ])
                
                fig.add_hline(y=current_price, line_dash="dash", line_color="white", 
                            annotation_text="Current Price")
                
                fig.update_layout(
                    title="Valuation Scenarios",
                    yaxis_title="Price ($)",
                    template="plotly_dark",
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning(f"Valuation error: {valuation.get('error', 'Unknown error')}")
    
    with col2:
        st.markdown("### Multiples Analysis")
        
        multiples = {
            "P/E": info.get('trailingPE', 0),
            "Forward P/E": info.get('forwardPE', 0),
            "P/B": info.get('priceToBook', 0),
            "P/S": info.get('priceToSalesTrailing12Months', 0),
            "PEG": info.get('pegRatio', 0),
            "EV/EBITDA": info.get('enterpriseToEbitda', 0)
        }
        
        # Filter out zeros
        multiples = {k: v for k, v in multiples.items() if v > 0}
        
        if multiples:
            multiples_df = pd.DataFrame({
                'Multiple': list(multiples.keys()),
                'Value': list(multiples.values())
            })
            
            fig = go.Figure(data=[
                go.Bar(
                    x=multiples_df['Multiple'],
                    y=multiples_df['Value'],
                    marker_color='#00d4ff'
                )
            ])
            
            fig.update_layout(
                title="Valuation Multiples",
                yaxis_title="Value",
                template="plotly_dark",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No multiples data available")

# ========== TAB 3: TECHNICAL ==========
with tab3:
    st.subheader("📈 Technical Analysis")
    
    if technical and "error" not in technical:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # RSI
            rsi_val = technical.get("rsi", {}).get("value", 50)
            rsi_signal = technical.get("rsi", {}).get("signal", "neutral")
            
            st.markdown("### RSI Indicator")
            st.metric("RSI", f"{rsi_val:.1f}", rsi_signal.upper())
            
            # RSI Gauge
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=rsi_val,
                domain={'x': [0, 1], 'y': [0, 1]},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "#00d4ff"},
                    'steps': [
                        {'range': [0, 30], 'color': "#00FF88"},
                        {'range': [30, 70], 'color': "#FFB700"},
                        {'range': [70, 100], 'color': "#FF3860"}
                    ],
                    'threshold': {
                        'line': {'color': "white", 'width': 4},
                        'thickness': 0.75,
                        'value': rsi_val
                    }
                }
            ))
            
            fig.update_layout(height=200, template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # MACD
            st.markdown("### MACD")
            macd_bull = technical.get("macd", {}).get("bullish", False)
            st.metric(
                "Signal",
                "BULLISH" if macd_bull else "BEARISH",
                "↑" if macd_bull else "↓"
            )
            
            macd_val = technical.get("macd", {}).get("macd", 0)
            signal_val = technical.get("macd", {}).get("signal", 0)
            st.markdown(f"**MACD:** {macd_val:.4f}")
            st.markdown(f"**Signal:** {signal_val:.4f}")
            st.markdown(f"**Histogram:** {macd_val - signal_val:.4f}")
        
        with col3:
            # Support/Resistance
            st.markdown("### Support & Resistance")
            support = technical.get("support_resistance", {}).get("support", 0)
            resistance = technical.get("support_resistance", {}).get("resistance", 0)
            
            st.metric("Support", f"${support:.2f}")
            st.metric("Resistance", f"${resistance:.2f}")
            
            near_support = technical.get("support_resistance", {}).get("near_support", False)
            near_resistance = technical.get("support_resistance", {}).get("near_resistance", False)
            
            if near_support:
                st.success("📍 Near Support Level")
            if near_resistance:
                st.warning("📍 Near Resistance Level")
        
        # Pattern Detection
        st.markdown("---")
        st.markdown("### 🔍 Pattern Detection")
        
        patterns = components["technical"].detect_patterns(df)
        if patterns:
            for pattern in patterns:
                signal_color = "#00FF88" if pattern['signal'] == "bullish" else "#FF3860"
                st.markdown(f"<span style='color: {signal_color}'>● {pattern['pattern'].replace('_', ' ').title()} - {pattern['signal'].upper()}</span>", unsafe_allow_html=True)
        else:
            st.info("No significant patterns detected")
    else:
        st.warning("Insufficient data for technical analysis")

# ========== TAB 4: SENTIMENT ==========
with tab4:
    st.subheader("💬 Sentiment Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### StockTwits Sentiment")
        
        st_sentiment = data["sentiment"]["stocktwits"]
        if "error" not in st_sentiment:
            # Sentiment pie chart
            sentiment_data = {
                "Bullish": st_sentiment.get("bullish", 0),
                "Bearish": st_sentiment.get("bearish", 0),
                "Neutral": st_sentiment.get("neutral", 0)
            }
            
            fig = go.Figure(data=[go.Pie(
                labels=list(sentiment_data.keys()),
                values=list(sentiment_data.values()),
                hole=.3,
                marker_colors=["#00FF88", "#FF3860", "#FFB700"]
            )])
            
            fig.update_layout(
                title="Sentiment Distribution",
                template="plotly_dark",
                height=300
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.metric(
                "Sentiment Score",
                f"{st_sentiment.get('sentiment_score', 0):.1f}",
                "BULLISH" if st_sentiment.get('sentiment_score', 0) > 20 else "BEARISH" if st_sentiment.get('sentiment_score', 0) < -20 else "NEUTRAL"
            )
        else:
            st.info("No sentiment data available")
    
    with col2:
        st.markdown("### Social Media Trends")
        st.info("Reddit sentiment analysis requires API setup")
        
        # Placeholder for trend chart
        dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
        trend_data = pd.DataFrame({
            'Date': dates,
            'Mentions': np.random.poisson(50, 30),
            'Sentiment': np.random.uniform(-50, 50, 30)
        })
        
        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            row_heights=[0.5, 0.5]
        )
        
        fig.add_trace(
            go.Scatter(x=trend_data['Date'], y=trend_data['Mentions'], 
                      name="Mentions", line=dict(color="#00d4ff")),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(x=trend_data['Date'], y=trend_data['Sentiment'],
                      name="Sentiment", line=dict(color="#FFB700")),
            row=2, col=1
        )
        
        fig.update_layout(
            title="30-Day Trend",
            template="plotly_dark",
            height=400,
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)

# ========== TAB 5: OPTIONS ==========
with tab5:
    st.subheader("⚡ Options Analysis")
    
    if data["options"] and "chains" in data["options"]:
        # Options summary
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Expirations Available", len(data["options"].get("expirations", [])))
        
        # Find unusual activity
        opportunities = components["options"].find_best_opportunities(
            data["options"],
            current_price
        )
        
        if opportunities:
            st.markdown("### 🔥 Unusual Options Activity")
            
            opp_df = pd.DataFrame(opportunities)
            st.dataframe(
                opp_df[['type', 'strike', 'expiration', 'volume', 'oi', 'signal']],
                use_container_width=True
            )
        else:
            st.info("No unusual options activity detected")
        
        # Options chain viewer
        st.markdown("### Options Chain")
        
        if data["options"]["expirations"]:
            selected_exp = st.selectbox(
                "Select Expiration",
                data["options"]["expirations"][:6]
            )
            
            if selected_exp and selected_exp in data["options"]["chains"]:
                chain = data["options"]["chains"][selected_exp]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### Calls")
                    if "calls" in chain and chain["calls"]:
                        calls_df = pd.DataFrame(chain["calls"])
                        display_cols = ['strike', 'lastPrice', 'volume', 'openInterest', 'impliedVolatility']
                        available_cols = [col for col in display_cols if col in calls_df.columns]
                        if available_cols:
                            st.dataframe(
                                calls_df[available_cols].head(10),
                                use_container_width=True
                            )
                    else:
                        st.info("No calls data")
                
                with col2:
                    st.markdown("#### Puts")
                    if "puts" in chain and chain["puts"]:
                        puts_df = pd.DataFrame(chain["puts"])
                        display_cols = ['strike', 'lastPrice', 'volume', 'openInterest', 'impliedVolatility']
                        available_cols = [col for col in display_cols if col in puts_df.columns]
                        if available_cols:
                            st.dataframe(
                                puts_df[available_cols].head(10),
                                use_container_width=True
                            )
                    else:
                        st.info("No puts data")
    else:
        st.warning("Options data not available for this ticker")

# ========== TAB 6: NEWS ==========
with tab6:
    st.subheader("📰 Latest News")
    
    news = data["sentiment"]["news"]
    if news:
        for article in news[:10]:
            with st.expander(f"📰 {article['title'][:100]}..."):
                st.markdown(f"**Publisher:** {article['publisher']}")
                st.markdown(f"**Published:** {article['timestamp']}")
                st.markdown(f"[Read Full Article]({article['link']})")
    else:
        st.info("No recent news available")

# ========== TAB 7: INSTITUTIONAL ==========
with tab7:
    st.subheader("🏢 Institutional Activity")
    
    inst_data = data["institutional"]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Major Holders")
        if "major_holders" in inst_data and inst_data["major_holders"]:
            holders_df = pd.DataFrame(inst_data["major_holders"])
            st.dataframe(holders_df, use_container_width=True)
        else:
            st.info("No major holders data available")
    
    with col2:
        st.markdown("### Institutional Holders")
        if "institutional_holders" in inst_data and inst_data["institutional_holders"]:
            inst_df = pd.DataFrame(inst_data["institutional_holders"])
            if not inst_df.empty:
                st.dataframe(inst_df.head(10), use_container_width=True)
        else:
            st.info("No institutional holders data available")
    
    st.markdown("### Insider Transactions")
    if "insider_transactions" in inst_data and inst_data["insider_transactions"]:
        insider_df = pd.DataFrame(inst_data["insider_transactions"])
        if not insider_df.empty:
            st.dataframe(insider_df.head(10), use_container_width=True)
    else:
        st.info("No insider transactions data available")

# ========== TAB 8: ADVANCED CHARTS ==========
with tab8:
    st.subheader("📉 Advanced Charts")
    
    if not df.empty:
        chart_type = st.selectbox(
            "Select Chart Type",
            ["Candlestick", "Line", "Area", "Heikin Ashi", "Renko"]
        )
        
        indicators = st.multiselect(
            "Add Indicators",
            ["SMA20", "SMA50", "SMA200", "EMA12", "EMA26", "Bollinger Bands", "RSI", "MACD", "Volume"]
        )
        
        # Create chart based on selection
        if chart_type == "Candlestick":
            fig = go.Figure(data=[go.Candlestick(
                x=df.index,
                open=df.get('Open', df['Close']),
                high=df.get('High', df['Close']),
                low=df.get('Low', df['Close']),
                close=df['Close']
            )])
        elif chart_type == "Line":
            fig = go.Figure(data=[go.Scatter(
                x=df.index,
                y=df['Close'],
                mode='lines',
                name='Close',
                line=dict(color='#00d4ff', width=2)
            )])
        elif chart_type == "Area":
            fig = go.Figure(data=[go.Scatter(
                x=df.index,
                y=df['Close'],
                fill='tozeroy',
                mode='lines',
                name='Close',
                line=dict(color='#00d4ff', width=2)
            )])
        else:
            # Heikin Ashi
            ha_close = (df['Open'] + df['High'] + df['Low'] + df['Close']) / 4
            ha_open = ha_close.shift(1)
            ha_high = df[['High', 'Open', 'Close']].max(axis=1)
            ha_low = df[['Low', 'Open', 'Close']].min(axis=1)
            
            fig = go.Figure(data=[go.Candlestick(
                x=df.index,
                open=ha_open,
                high=ha_high,
                low=ha_low,
                close=ha_close,
                name="Heikin Ashi"
            )])
        
        # Add selected indicators
        if "SMA20" in indicators and len(df) >= 20:
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df['Close'].rolling(20).mean(),
                name='SMA20',
                line=dict(color='#FFB700', width=1)
            ))
        
        if "SMA50" in indicators and len(df) >= 50:
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df['Close'].rolling(50).mean(),
                name='SMA50',
                line=dict(color='#FF3860', width=1)
            ))
        
        if "Bollinger Bands" in indicators and len(df) >= 20:
            bb = ta.volatility.BollingerBands(df['Close'])
            fig.add_trace(go.Scatter(
                x=df.index,
                y=bb.bollinger_hband(),
                name='BB Upper',
                line=dict(color='rgba(250, 128, 114, 0.5)', width=1)
            ))
            fig.add_trace(go.Scatter(
                x=df.index,
                y=bb.bollinger_lband(),
                name='BB Lower',
                line=dict(color='rgba(250, 128, 114, 0.5)', width=1),
                fill='tonexty',
                fillcolor='rgba(250, 128, 114, 0.1)'
            ))
        
        fig.update_layout(
            title=f"{ticker} - {chart_type} Chart",
            yaxis_title="Price ($)",
            template="plotly_dark",
            height=600,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No data available for charting")

# ========== FOOTER ==========
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>Smart Investment Dashboard v1.0 | Data provided by yfinance | Not financial advice</p>
    <p>Built with ❤️ using Streamlit and Python</p>
</div>
""", unsafe_allow_html=True)
