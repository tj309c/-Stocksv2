"""
Stocks Dashboard - Diamond Hands Edition 💎🙌
For analyzing stonks with ape-approved metrics
Where technical analysis meets autism

Robinhood-inspired aesthetics with expert-level analysis
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import ta
from wsb_quotes import (get_confidence_message, get_sentiment_comment, 
                        get_technical_comment, get_loading_message, 
                        get_error_message, get_dashboard_tagline)
from utils import (format_currency, format_percentage, format_large_number,
                   format_price, get_color_for_value, get_confidence_color,
                   safe_get, safe_divide, sanitize_dict_for_cache)
from enhanced_valuation_ui import show_enhanced_valuation_tab

def show_stocks_dashboard(components, ticker="META"):
    """Display the stocks analysis dashboard"""
    
    tagline = get_dashboard_tagline("stocks")
    
    # Professional header with WSB humor
    st.markdown("""
    <div style="text-align: center; padding: 20px 0 10px 0;">
        <h1 style="font-size: 2.5rem; margin-bottom: 5px; font-weight: 700; letter-spacing: -0.5px;">
            📈 STONKS ANALYSIS
        </h1>
        <p style="font-size: 0.95rem; opacity: 0.8; font-style: italic; margin-top: 0;">
            {tagline}
        </p>
    </div>
    """.replace("{tagline}", tagline), unsafe_allow_html=True)
    
    # Ticker input section
    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
    
    with col1:
        ticker_input = st.text_input(
            "Enter Ticker Symbol",
            value=ticker,
            help="Enter a stock ticker (e.g., AAPL, TSLA, GME, AMC)"
        ).upper()
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔍 Analyze", type="primary", key="analyze_stock"):
            ticker = ticker_input
            st.session_state.active_ticker = ticker
    
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Refresh", key="refresh_stock"):
            st.rerun()
    
    with col4:
        st.markdown("<br>", unsafe_allow_html=True)
        diamond_hands = st.checkbox("💎🙌", value=True, help="Diamond Hands Mode")
    
    # Fetch data
    ticker = st.session_state.get("active_ticker", ticker_input)
    
    loading_msg = get_loading_message()
    with st.spinner(f"{loading_msg} ({ticker})"):
        data = fetch_stock_data(components, ticker)
    
    if not data or "error" in data:
        error_msg = get_error_message()
        st.error(f"{error_msg} Ticker: {ticker}")
        st.info("💡 Try: GME, AMC, TSLA, NVDA, or any ticker that hasn't bankrupted you yet")
        return
    
    # Main metrics and buy signal
    show_buy_signal_section(data, components, diamond_hands)
    
    # Tabs for detailed analysis
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Overview",
        "💰 Valuation (DD)",
        "🎛️ Interactive DCF",
        "📈 Technical (Charts)",
        "💬 Ape Sentiment",
        "🏢 Smart Money"
    ])
    
    with tab1:
        show_overview_tab(data)
    
    with tab2:
        show_valuation_tab(data, components)
    
    with tab3:
        # Enhanced valuation with interactive DCF and Monte Carlo
        show_enhanced_valuation_tab(data, components)
    
    with tab4:
        show_technical_tab(data, components)
    
    with tab5:
        show_sentiment_tab(data, components)
    
    with tab6:
        show_institutional_tab(data)


@st.cache_data(ttl=300)
def fetch_stock_data(_components, ticker):
    """Fetch all stock data with caching"""
    components = _components
    try:
        data = {
            "ticker": ticker,
            "stock_data": components["fetcher"].get_stock_data(ticker),
            "quote": components["fetcher"].get_realtime_quote(ticker),
            "fundamentals": components["fetcher"].get_fundamentals(ticker),
            "institutional": components["fetcher"].get_institutional_data(ticker),
            "sentiment": {
                "stocktwits": components["sentiment"].get_stocktwits_sentiment(ticker),
                "news": components["sentiment"].get_news_sentiment(ticker)
            }
        }
        
        # Process DataFrame
        if data["stock_data"] and "history" in data["stock_data"]:
            df = pd.DataFrame(data["stock_data"]["history"])
            if not df.empty:
                df.index = pd.to_datetime(df.index) if not isinstance(df.index, pd.DatetimeIndex) else df.index
                data["df"] = df
        
        # Sanitize all data for caching (fixes Timestamp errors)
        data = sanitize_dict_for_cache(data)
        
        return data
    except Exception as e:
        return {"error": str(e)}


def show_buy_signal_section(data, components, diamond_hands=True):
    """Display the good buy analysis section"""
    
    df = data.get("df", pd.DataFrame())
    info = data["stock_data"].get("info", {}) if data.get("stock_data") else {}
    
    # Run analysis
    valuation = components["valuation"].calculate_dcf(data["fundamentals"], info)
    if "error" in valuation:
        valuation = components["valuation"].calculate_multiples_valuation(info)
    
    technical = components["technical"].analyze(df) if not df.empty else {}
    sentiment = data["sentiment"]["stocktwits"]
    
    buy_analysis = components["goodbuy"].analyze_buy_opportunity(
        data["ticker"], valuation, technical, sentiment, info, df
    )
    
    # Display buy signal
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
    current_price = buy_analysis["current_price"]
    buy_low = buy_analysis["buy_range"]["low"]
    buy_high = buy_analysis["buy_range"]["high"]
    target = buy_analysis["target_price"]
    confidence = buy_analysis["total_score"]
    
    with col1:
        prev_close = info.get('previousClose', current_price)
        price_change = ((current_price - prev_close) / prev_close * 100) if prev_close > 0 else 0
        price_emoji = "🟢" if price_change > 0 else "🔴" if price_change < 0 else "⚪"
        st.metric(
            f"{price_emoji} Bag Holding At",
            format_currency(current_price),
            format_percentage(price_change) + (" (green is good)" if price_change > 0 else " (ouch)" if price_change < 0 else "")
        )
    
    with col2:
        color = "#00FF88" if confidence >= 70 else "#FFB700" if confidence >= 50 else "#FF3860"
        emoji = "🚀🌕" if confidence >= 70 else "📈💰" if confidence >= 50 else "🤔🎰"
        zone_label = "APE ENTRY ZONE" if confidence >= 70 else "MAYBE BUY?" if confidence >= 50 else "WAIT FOR DIP"
        
        st.markdown(f"""
        <div style="background: {color}20; border: 2px solid {color}; padding: 10px; border-radius: 10px; text-align: center;">
            <h3 style="color: {color}; margin: 0;">{emoji} {zone_label}</h3>
            <h2 style="color: white; margin: 5px 0;">{format_currency(buy_low)} - {format_currency(buy_high)}</h2>
            <p style="color: #999; font-size: 0.8em; margin: 0;">(Not financial advice, obviously)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        upside = ((target - current_price) / current_price * 100) if current_price > 0 else 0
        target_label = "🌕 Moon Price" if upside > 50 else "🎯 Realistic Target" if upside > 20 else "💼 Conservative"
        st.metric(
            target_label,
            format_currency(target),
            f"+{upside:.1f}%" + (" 🚀🚀🚀" if upside > 50 else " 🚀" if upside > 20 else "")
        )
    
    with col4:
        confidence_emoji = "🔥💎" if confidence >= 70 else "👍📊" if confidence >= 50 else "🤷‍♂️🎲"
        confidence_label = "Autism Level"
        st.metric(
            f"{confidence_emoji} {confidence_label}",
            f"{confidence:.0f}/100",
            buy_analysis["confidence"] + " trust"
        )
    
    # Buy signals
    if buy_analysis["signals"]:
        signals_text = " | ".join(buy_analysis["signals"][:3])
        st.success(f"**🦍 Ape Signals:** {signals_text}")
    
    # Recommendation
    rec = buy_analysis["recommendation"]
    rec_color = "#00FF88" if rec == "STRONG BUY" else "#FFB700" if rec == "BUY" else "#FF3860"
    rec_emoji = "💎🙌" if rec == "STRONG BUY" else "👍" if rec == "BUY" else "🧻👎"
    
    # Get WSB-style message based on confidence
    wsb_message = get_confidence_message(confidence)
    
    st.markdown(f"""
    <div style="background: {rec_color}20; border: 2px solid {rec_color}; padding: 15px; border-radius: 10px; text-align: center; margin: 20px 0;">
        <h1 style="color: {rec_color}; margin: 0;">{rec_emoji} {rec}</h1>
        <p style="color: white; font-size: 1.1em; margin: 10px 0;"><i>"{wsb_message}"</i></p>
        <p style="color: white;">Risk/Reward: {buy_analysis['risk_reward_ratio']:.2f} | Stop Loss: {format_currency(buy_analysis['stop_loss'])}</p>
        <p style="color: #aaa; font-size: 0.8em;">{"HODL with diamond hands! 💎🙌" if rec == "STRONG BUY" else "Solid play, ape! 🦍" if rec == "BUY" else "Maybe wait behind the Wendy's dumpster... 🗑️"}</p>
    </div>
    """, unsafe_allow_html=True)


def show_overview_tab(data):
    """Show overview with price chart and key metrics"""
    
    col1, col2 = st.columns([2, 1])
    
    df = data.get("df", pd.DataFrame())
    info = data["stock_data"].get("info", {}) if data.get("stock_data") else {}
    
    with col1:
        st.subheader("📈 Price Chart")
        
        if not df.empty:
            fig = make_subplots(
                rows=2, cols=1,
                shared_xaxes=True,
                row_heights=[0.7, 0.3],
                vertical_spacing=0.03
            )
            
            # Candlestick
            has_ohlc = all(col in df.columns for col in ['Open', 'High', 'Low', 'Close'])
            fig.add_trace(
                go.Candlestick(
                    x=df.index,
                    open=df['Open'] if has_ohlc else df['Close'],
                    high=df['High'] if has_ohlc else df['Close'],
                    low=df['Low'] if has_ohlc else df['Close'],
                    close=df['Close'],
                    name="Price"
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
                title=f"{data['ticker']} - To The Moon! 🚀",
                yaxis_title="Price ($)",
                yaxis2_title="Volume",
                template="plotly_dark",
                height=500,
                showlegend=True,
                hovermode='x unified'
            )
            
            fig.update_xaxes(rangeslider_visible=False)
            st.plotly_chart(fig, width='stretch')
        else:
            st.warning("No price data available")
    
    with col2:
        st.subheader("📊 Key Metrics")
        
        if info:
            # Market cap with emoji scale
            market_cap = info.get('marketCap', 0)
            if market_cap > 200e9:
                cap_emoji = "🐋"  # Whale
            elif market_cap > 10e9:
                cap_emoji = "🦍"  # Gorilla
            else:
                cap_emoji = "🐒"  # Monkey
            
            st.markdown(f"**{cap_emoji} Market Cap:** {format_large_number(market_cap)}" if market_cap > 0 else "**Market Cap:** N/A")
            st.markdown(f"**P/E Ratio:** {info.get('trailingPE', 0):.2f}" if info.get('trailingPE', 0) > 0 else "**P/E Ratio:** N/A")
            st.markdown(f"**EPS:** {format_currency(info.get('trailingEps', 0))}" if info.get('trailingEps', 0) > 0 else "**EPS:** N/A")
            
            # Dividend with fun text
            div_yield = info.get('dividendYield', 0)
            if div_yield > 0:
                st.markdown(f"**💰 Dividend:** {format_percentage(div_yield*100)} (Free tendies!)")
            else:
                st.markdown("**Dividend:** None (Growth mode 🚀)")
            
            st.markdown(f"**Beta:** {info.get('beta', 1):.2f} {'🎢' if info.get('beta', 1) > 1.5 else '📊'}")
            st.markdown(f"**52W High:** {format_currency(info.get('fiftyTwoWeekHigh', 0))}")
            st.markdown(f"**52W Low:** {format_currency(info.get('fiftyTwoWeekLow', 0))}")
            
            # Volume analysis
            avg_vol = info.get('averageVolume', 0)
            if avg_vol > 0:
                st.markdown(f"**Avg Volume:** {format_large_number(avg_vol)}")


def show_valuation_tab(data, components):
    """Show valuation analysis (Due Diligence)"""
    st.subheader("💰 Valuation DD (Due Diligence)")
    
    try:
        info = data["stock_data"].get("info", {}) if data.get("stock_data") else {}
        
        if not info:
            st.warning("⚠️ No stock info available for valuation analysis")
            return
        
        # Calculate valuation
        valuation = components["valuation"].calculate_dcf(data.get("fundamentals", {}), info)
        if "error" in valuation:
            valuation = components["valuation"].calculate_multiples_valuation(info)
    except Exception as e:
        st.error(f"❌ Error loading valuation data: {str(e)}")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        if "error" not in valuation:
            st.markdown("### 🧮 Fair Value Calc")
            
            fair_value = valuation.get('fair_value', 0)
            current_price = valuation.get('current_price', 0)
            upside = valuation.get('upside', 0)
            
            st.markdown(f"**Fair Value:** {format_currency(fair_value)}")
            st.markdown(f"**Current Price:** {format_currency(current_price)}")
            
            if upside > 20:
                st.success(f"**Upside:** {format_percentage(upside)} 🚀 (UNDERVALUED!)")
            elif upside > 0:
                st.info(f"**Upside:** {format_percentage(upside)} 📈")
            else:
                st.warning(f"**Downside:** {format_percentage(upside)} 📉")
            
            st.markdown(f"**Method:** {valuation.get('method', 'Unknown')}")
            
            # Scenarios
            if "scenarios" in valuation:
                st.markdown("### 📊 Price Scenarios")
                try:
                    scenarios_df = pd.DataFrame({
                        'Scenario': ['🐻 Bear', '📊 Base', '🚀 Bull'],
                        'Price': [
                            valuation['scenarios']['bear'],
                            valuation['scenarios']['base'],
                            valuation['scenarios']['bull']
                        ]
                    })
                    
                    fig = go.Figure(data=[
                        go.Bar(
                            x=scenarios_df['Scenario'],
                            y=scenarios_df['Price'],
                            marker_color=['#FF3860', '#FFB700', '#00FF88']
                        )
                    ])
                    
                    if current_price and current_price > 0:
                        fig.add_hline(y=current_price, line_dash="dash", line_color="white",
                                    annotation_text="Current Price")
                    
                    fig.update_layout(
                        yaxis_title="Price ($)",
                        template="plotly_dark",
                        height=400
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.error(f"Error creating scenarios chart: {str(e)}")
        else:
            st.warning(f"⚠️ Valuation unavailable: {valuation.get('error', 'Unknown error')}")
    
    with col2:
        st.markdown("### 📐 Multiples")
        
        multiples = {
            "P/E": info.get('trailingPE', 0),
            "Forward P/E": info.get('forwardPE', 0),
            "P/B": info.get('priceToBook', 0),
            "P/S": info.get('priceToSalesTrailing12Months', 0),
            "PEG": info.get('pegRatio', 0),
        }
        
        multiples = {k: v for k, v in multiples.items() if v > 0}
        
        if multiples:
            for metric, value in multiples.items():
                if metric == "PEG" and value < 1:
                    st.success(f"**{metric}:** {value:.2f} (CHEAP! 🤑)")
                elif metric == "P/E" and value < 15:
                    st.success(f"**{metric}:** {value:.2f} (Value play! 💰)")
                else:
                    st.markdown(f"**{metric}:** {value:.2f}")
        else:
            st.info("No multiples data available")


def show_technical_tab(data, components):
    """Show technical analysis"""
    st.subheader("📈 Technical Analysis (TA)")
    
    df = data.get("df", pd.DataFrame())
    
    if df.empty:
        st.warning("Insufficient data for TA")
        return
    
    technical = components["technical"].analyze(df)
    
    if "error" in technical:
        st.error(f"TA Error: {technical['error']}")
        return
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # RSI
        rsi_val = technical.get("rsi", {}).get("value", 50)
        rsi_signal = technical.get("rsi", {}).get("signal", "neutral")
        
        st.markdown("### 🔥 RSI")
        
        if rsi_signal == "oversold":
            st.success(f"**{rsi_val:.1f}** - OVERSOLD! Time to buy the dip! 🦍")
        elif rsi_signal == "overbought":
            st.warning(f"**{rsi_val:.1f}** - OVERBOUGHT! Moon soon? 🚀")
        else:
            st.info(f"**{rsi_val:.1f}** - Neutral 📊")
    
    with col2:
        # MACD
        st.markdown("### 📊 MACD")
        macd_bull = technical.get("macd", {}).get("bullish", False)
        
        if macd_bull:
            st.success("**BULLISH** Crossover! 🚀")
        else:
            st.warning("**BEARISH** Watch out! 📉")
    
    with col3:
        # Support/Resistance
        st.markdown("### 🎯 Levels")
        support = technical.get("support_resistance", {}).get("support", 0)
        resistance = technical.get("support_resistance", {}).get("resistance", 0)
        
        st.markdown(f"**Resistance:** {format_currency(resistance)}")
        st.markdown(f"**Support:** {format_currency(support)}")
        
        if technical.get("support_resistance", {}).get("near_support", False):
            st.success("📍 Near support! Buy opportunity!")
    
    # Patterns
    st.markdown("---")
    st.markdown("### 🔍 Chart Patterns")
    
    patterns = components["technical"].detect_patterns(df)
    if patterns:
        for pattern in patterns:
            signal_color = "#00FF88" if pattern['signal'] == "bullish" else "#FF3860"
            signal_emoji = "🚀" if pattern['signal'] == "bullish" else "📉"
            st.markdown(
                f"<span style='color: {signal_color}'>{signal_emoji} {pattern['pattern'].replace('_', ' ').title()} - {pattern['signal'].upper()}</span>",
                unsafe_allow_html=True
            )
    else:
        st.info("No major patterns detected. Sideways trading 📊")


def show_sentiment_tab(data, components):
    """Show sentiment analysis using real scraper data"""
    from src.utils.sentiment_scraper import get_scraper, display_sentiment_metrics, display_recent_posts
    from src.config.settings import Config
    
    st.subheader("💬 Ape Sentiment Tracker")
    
    # Get configuration for API keys
    config_obj = Config()
    api_config = {
        'reddit_client_id': config_obj.get('api.reddit.client_id', ''),
        'reddit_client_secret': config_obj.get('api.reddit.client_secret', ''),
        'reddit_user_agent': config_obj.get('api.reddit.user_agent', 'StocksV2App/1.0'),
        'news_api_key': config_obj.get('api.news.api_key', '')
    }
    
    # Initialize scraper
    scraper = get_scraper(api_config)
    
    # Add refresh button
    col_refresh, col_info = st.columns([1, 3])
    with col_refresh:
        if st.button("🔄 Refresh Data", key="refresh_sentiment"):
            scraper.get_sentiment_data.clear()
            st.rerun()
    
    with col_info:
        st.caption("Real-time sentiment from Reddit (wallstreetbets, stocks, investing) and news sources")
    
    # Get sentiment data
    ticker = data["ticker"]
    with st.spinner(f"Scraping sentiment data for ${ticker}..."):
        summary = scraper.get_sentiment_summary(ticker)
    
    if summary['data_available']:
        # Display metrics
        display_sentiment_metrics(summary)
        
        st.divider()
        
        # Create two columns for visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Sentiment Breakdown")
            
            # Sentiment pie chart
            sentiment_data = {
                "🟢 Positive": summary['positive_pct'],
                "🔴 Negative": summary['negative_pct'],
                "⚪ Neutral": summary['neutral_pct']
            }
            
            fig = go.Figure(data=[go.Pie(
                labels=list(sentiment_data.keys()),
                values=list(sentiment_data.values()),
                hole=.3,
                marker_colors=["#00FF88", "#FF3860", "#FFB700"]
            )])
            
            fig.update_layout(
                title=f"Sentiment Distribution ({summary['total_mentions']} mentions)",
                template="plotly_dark",
                height=350
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Sentiment score interpretation
            avg_polarity = summary['avg_polarity']
            if avg_polarity > 0.3:
                st.success(f"**Polarity: {avg_polarity:.2f}** - Apes are BULLISH! 🦍🚀")
            elif avg_polarity > 0:
                st.info(f"**Polarity: {avg_polarity:.2f}** - Slightly bullish 📈")
            elif avg_polarity > -0.3:
                st.warning(f"**Polarity: {avg_polarity:.2f}** - Slightly bearish 📉")
            else:
                st.error(f"**Polarity: {avg_polarity:.2f}** - Bears winning 🐻")
        
        with col2:
            st.markdown("### 📈 Trending Sources")
            
            # Source distribution bar chart
            sources = summary['trending_sources']
            if sources:
                fig_sources = go.Figure(data=[go.Bar(
                    x=list(sources.values()),
                    y=list(sources.keys()),
                    orientation='h',
                    marker_color='#00D9FF'
                )])
                
                fig_sources.update_layout(
                    title="Mentions by Source",
                    template="plotly_dark",
                    height=350,
                    xaxis_title="Number of Mentions",
                    yaxis_title="Source"
                )
                
                st.plotly_chart(fig_sources, use_container_width=True)
            else:
                st.info("No source data available")
            
            # Subjectivity meter
            subjectivity = summary['avg_subjectivity']
            st.metric(
                "Avg Subjectivity",
                f"{subjectivity:.2f}",
                help="0 = Objective, 1 = Highly Subjective/Opinionated"
            )
        
        st.divider()
        
        # Display recent posts
        st.markdown("### 🔥 Recent Social Activity")
        display_recent_posts(summary['recent_posts'], max_posts=10)
        
        # Sentiment over time (if we have enough data)
        sentiment_over_time = scraper.get_sentiment_over_time(ticker, days=7)
        if not sentiment_over_time.empty:
            st.markdown("### 📅 Sentiment Trend (Last 7 Days)")
            
            fig_trend = go.Figure()
            
            if 'positive' in sentiment_over_time.columns:
                fig_trend.add_trace(go.Scatter(
                    x=sentiment_over_time['date_only'],
                    y=sentiment_over_time['positive'],
                    mode='lines+markers',
                    name='Positive',
                    line=dict(color='#00FF88', width=2)
                ))
            
            if 'negative' in sentiment_over_time.columns:
                fig_trend.add_trace(go.Scatter(
                    x=sentiment_over_time['date_only'],
                    y=sentiment_over_time['negative'],
                    mode='lines+markers',
                    name='Negative',
                    line=dict(color='#FF3860', width=2)
                ))
            
            if 'neutral' in sentiment_over_time.columns:
                fig_trend.add_trace(go.Scatter(
                    x=sentiment_over_time['date_only'],
                    y=sentiment_over_time['neutral'],
                    mode='lines+markers',
                    name='Neutral',
                    line=dict(color='#FFB700', width=2)
                ))
            
            fig_trend.update_layout(
                title="Daily Sentiment Mentions",
                template="plotly_dark",
                height=400,
                xaxis_title="Date",
                yaxis_title="Number of Mentions",
                hovermode='x unified'
            )
            
            st.plotly_chart(fig_trend, use_container_width=True)
    
    else:
        # Fallback to old sentiment display if no scraper data
        st.warning("⚠️ Real-time sentiment scraping unavailable. Configure API keys for live data.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🦍 StockTwits Vibes")
            sentiment = data["sentiment"]["stocktwits"]
            
            if "error" not in sentiment:
                sentiment_data = {
                    "🚀 Bullish": sentiment.get("bullish", 0),
                    "📉 Bearish": sentiment.get("bearish", 0),
                    "🤷 Neutral": sentiment.get("neutral", 0)
                }
                
                fig = go.Figure(data=[go.Pie(
                    labels=list(sentiment_data.keys()),
                    values=list(sentiment_data.values()),
                    hole=.3,
                    marker_colors=["#00FF88", "#FF3860", "#FFB700"]
                )])
                
                fig.update_layout(
                    title="Community Sentiment",
                    template="plotly_dark",
                    height=300
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                score = sentiment.get('sentiment_score', 0)
                if score > 30:
                    st.success(f"**Score: {score:,.1f}** - Apes are BULLISH! 🦍🚀")
                elif score > 0:
                    st.info(f"**Score: {score:,.1f}** - Slightly bullish 📈")
                elif score > -30:
                    st.warning(f"**Score: {score:,.1f}** - Slightly bearish 📉")
                else:
                    st.error(f"**Score: {score:,.1f}** - Bears winning 🐻")
            else:
                st.info("No sentiment data available")
        
        with col2:
            st.markdown("### 📰 Latest News")
            news = data["sentiment"]["news"]
            if news:
                for article in news[:5]:
                    with st.expander(f"📰 {article['title'][:60]}..."):
                        st.markdown(f"**Publisher:** {article['publisher']}")
                        st.markdown(f"**Time:** {article['timestamp']}")
                        st.markdown(f"[Read More]({article['link']})")
            else:
                st.info("No recent news")


def show_institutional_tab(data):
    """Show institutional holdings"""
    st.subheader("🏢 Smart Money Tracker")
    
    inst_data = data["institutional"]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🐋 Major Holders")
        if "major_holders" in inst_data and inst_data["major_holders"]:
            holders_df = pd.DataFrame(inst_data["major_holders"])
            st.dataframe(holders_df, width='stretch')
        else:
            st.info("No major holders data")
    
    with col2:
        st.markdown("### 🏦 Institutional")
        if "institutional_holders" in inst_data and inst_data["institutional_holders"]:
            inst_df = pd.DataFrame(inst_data["institutional_holders"])
            if not inst_df.empty:
                st.dataframe(inst_df.head(5), width='stretch')
        else:
            st.info("No institutional data")
    
    st.markdown("### 👔 Insider Moves")
    if "insider_transactions" in inst_data and inst_data["insider_transactions"]:
        insider_df = pd.DataFrame(inst_data["insider_transactions"])
        if not insider_df.empty:
            st.dataframe(insider_df.head(10), width='stretch')
            
            # Check for insider buying
            if 'Shares' in insider_df.columns:
                recent_buys = insider_df[insider_df['Shares'] > 0]
                if not recent_buys.empty:
                    st.success("🚨 Insiders are buying! Bullish signal! 🚀")
    else:
        st.info("No insider transaction data")
