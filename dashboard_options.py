"""
Options Dashboard - YOLO Edition ⚡
For degens who love 0DTE plays and gamma squeezes
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
from utils import (format_currency, format_percentage, format_large_number,
                   format_price, get_color_for_value, get_confidence_color,
                   safe_get, safe_divide)

def show_options_dashboard(components, ticker="SPY"):
    """Display the options analysis dashboard"""
    
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h1 style="margin: 0; font-size: 3em;">⚡ OPTIONS Dashboard</h1>
        <p style="color: #888; font-size: 1.2em; margin: 10px 0;"><i>YOLO plays and gamma squeezes</i> 🎰</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Ticker input
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        ticker_input = st.text_input(
            "Enter Ticker Symbol",
            value=ticker,
            help="Works best with liquid stocks (SPY, AAPL, TSLA, etc.)"
        ).upper()
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("⚡ Analyze", type="primary", key="analyze_options"):
            ticker = ticker_input
            st.session_state.active_ticker = ticker
    
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Refresh", key="refresh_options"):
            st.rerun()
    
    ticker = st.session_state.get("active_ticker", ticker_input)
    
    # Fetch data
    with st.spinner(f"Loading options chain for {ticker}... ⚡"):
        data = fetch_options_data(components, ticker)
    
    if not data or "error" in data:
        st.error(f"❌ No options data for {ticker}. Try a more liquid ticker!")
        return
    
    # Show current price and key metrics
    show_options_overview(data, components)
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔥 Unusual Activity",
        "📊 Options Chain",
        "📈 Greeks Analysis",
        "🎯 Strategy Builder"
    ])
    
    with tab1:
        show_unusual_activity_tab(data, components)
    
    with tab2:
        show_options_chain_tab(data)
    
    with tab3:
        show_greeks_tab(data)
    
    with tab4:
        show_strategy_tab(data)


@st.cache_data(ttl=300)
def fetch_options_data(_components, ticker):
    """Fetch options data with caching"""
    components = _components
    try:
        data = {
            "ticker": ticker,
            "stock_data": components["fetcher"].get_stock_data(ticker, period="3mo"),
            "quote": components["fetcher"].get_realtime_quote(ticker),
            "options": components["fetcher"].get_options_chain(ticker),
        }
        
        # Get current price
        info = data["stock_data"].get("info", {}) if data["stock_data"] else {}
        data["current_price"] = info.get("currentPrice", info.get("regularMarketPrice", 0))
        
        # Sanitize all data for caching (fixes Timestamp errors)
        from utils import sanitize_dict_for_cache
        data = sanitize_dict_for_cache(data)
        
        return data
    except Exception as e:
        return {"error": str(e)}


def show_options_overview(data, components):
    """Show current price and quick stats"""
    
    st.markdown("---")
    
    current_price = data["current_price"]
    info = data["stock_data"].get("info", {}) if data.get("stock_data") else {}
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        prev_close = info.get('previousClose', current_price)
        price_change = ((current_price - prev_close) / prev_close * 100) if prev_close > 0 else 0
        st.metric(
            "💰 Stock Price",
            format_currency(current_price),
            format_percentage(price_change)
        )
    
    with col2:
        # Count available expirations
        expirations = data["options"].get("expirations", [])
        st.metric(
            "📅 Expirations",
            len(expirations),
            "Available dates"
        )
    
    with col3:
        # IV if available
        iv = info.get("impliedVolatility", 0)
        if iv > 0:
            st.metric(
                "📊 IV",
                format_percentage(iv*100),
                "Implied Vol"
            )
        else:
            st.metric("📊 IV", "N/A", "Check options")
    
    with col4:
        # Volume indicator
        volume = info.get("volume", 0)
        avg_volume = info.get("averageVolume", 1)
        vol_ratio = volume / avg_volume if avg_volume > 0 else 1
        
        st.metric(
            "📈 Volume",
            f"{vol_ratio:,.2f}x",
            "vs Average"
        )


def show_unusual_activity_tab(data, components):
    """Show unusual options activity"""
    st.subheader("🔥 Unusual Options Activity (Whales Buying)")
    
    current_price = data["current_price"]
    opportunities = components["options"].find_best_opportunities(
        data["options"],
        current_price
    )
    
    if opportunities:
        st.success(f"🚨 Found {len(opportunities)} unusual options flows!")
        
        # Convert to DataFrame for display
        opp_df = pd.DataFrame(opportunities)
        
        # Color code by type
        def color_type(val):
            if val == "CALL":
                return 'background-color: rgba(0, 255, 136, 0.2)'
            else:
                return 'background-color: rgba(255, 56, 96, 0.2)'
        
        if 'type' in opp_df.columns:
            styled_df = opp_df.style.applymap(color_type, subset=['type'])
            st.dataframe(styled_df, width='stretch')
        else:
            st.dataframe(opp_df, width='stretch')
        
        st.markdown("### 🦍 What This Means:")
        st.info("""
        **High Volume/OI Ratio** = Smart money is entering new positions!
        - **Unusual Call Activity** 🚀 = Bullish whale bets
        - **Unusual Put Activity** 📉 = Bearish hedge or directional play
        - **Near-the-money** = Most likely to move stock price
        """)
    else:
        st.warning("No unusual activity detected. Market is quiet... 😴")
        st.info("💡 Try a more liquid ticker like SPY, QQQ, AAPL, or TSLA")


def show_options_chain_tab(data):
    """Show full options chain"""
    st.subheader("📊 Options Chain Explorer")
    
    options_data = data["options"]
    current_price = data["current_price"]
    
    if not options_data or "expirations" not in options_data:
        st.warning("No options chain available")
        return
    
    expirations = options_data["expirations"]
    
    # Expiration selector
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_exp = st.selectbox(
            "Select Expiration Date",
            expirations[:10],  # Show first 10
            help="Choose an expiration to view the options chain"
        )
    
    with col2:
        # Calculate DTE
        try:
            exp_date = datetime.strptime(selected_exp, '%Y-%m-%d')
            dte = (exp_date - datetime.now()).days
            st.metric("Days to Expiry", dte, "DTE" if dte > 1 else "⚠️ 0DTE!" if dte == 0 else "EXPIRED")
        except:
            dte = 0
    
    if selected_exp and selected_exp in options_data["chains"]:
        chain = options_data["chains"][selected_exp]
        
        # Show calls and puts side by side
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🚀 CALLS (Bullish)")
            if "calls" in chain and chain["calls"]:
                calls_df = pd.DataFrame(chain["calls"])
                
                # Filter to show strikes around current price
                if 'strike' in calls_df.columns and len(calls_df) > 0:
                    calls_df = calls_df[
                        (calls_df['strike'] >= current_price * 0.9) &
                        (calls_df['strike'] <= current_price * 1.2)
                    ]
                
                display_cols = ['strike', 'lastPrice', 'volume', 'openInterest', 'impliedVolatility']
                available_cols = [col for col in display_cols if col in calls_df.columns]
                
                if available_cols and not calls_df.empty:
                    # Highlight ITM options
                    def highlight_itm(row):
                        if row['strike'] < current_price:
                            return ['background-color: rgba(0, 255, 136, 0.1)'] * len(row)
                        return [''] * len(row)
                    
                    styled_calls = calls_df[available_cols].head(20).style.apply(highlight_itm, axis=1)
                    st.dataframe(styled_calls, width='stretch', height=400)
                else:
                    st.info("No calls data")
            else:
                st.info("No calls available")
        
        with col2:
            st.markdown("#### 📉 PUTS (Bearish)")
            if "puts" in chain and chain["puts"]:
                puts_df = pd.DataFrame(chain["puts"])
                
                # Filter to show strikes around current price
                if 'strike' in puts_df.columns and len(puts_df) > 0:
                    puts_df = puts_df[
                        (puts_df['strike'] >= current_price * 0.8) &
                        (puts_df['strike'] <= current_price * 1.1)
                    ]
                
                display_cols = ['strike', 'lastPrice', 'volume', 'openInterest', 'impliedVolatility']
                available_cols = [col for col in display_cols if col in puts_df.columns]
                
                if available_cols and not puts_df.empty:
                    # Highlight ITM options
                    def highlight_itm(row):
                        if row['strike'] > current_price:
                            return ['background-color: rgba(255, 56, 96, 0.1)'] * len(row)
                        return [''] * len(row)
                    
                    styled_puts = puts_df[available_cols].head(20).style.apply(highlight_itm, axis=1)
                    st.dataframe(styled_puts, width='stretch', height=400)
                else:
                    st.info("No puts data")
            else:
                st.info("No puts available")
        
        # Legend
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.info("💡 **ITM (In The Money)** = Highlighted options have intrinsic value")
        with col2:
            st.info("📊 **Volume > OI** = New positions being opened (bullish signal)")


def show_greeks_tab(data):
    """Show Greeks analysis"""
    st.subheader("📈 Greeks Analysis")
    
    st.info("🔨 Greeks calculator coming soon!")
    st.markdown("""
    ### What are Greeks? 🤔
    
    - **Delta (Δ)**: How much option price changes per $1 stock move
        - Calls: 0 to 1 | Puts: -1 to 0
        - 0.50 Delta = $0.50 option move per $1 stock move
    
    - **Gamma (Γ)**: Rate of change of Delta
        - High gamma = Delta changes fast (risky but profitable!)
        - Highest at-the-money
    
    - **Theta (Θ)**: Time decay per day
        - How much option loses value each day
        - Sellers love theta! Buyers hate it! ⏰
    
    - **Vega (V)**: Sensitivity to IV changes
        - High vega = Big moves when IV spikes
        - Great for earnings plays
    
    - **Rho (ρ)**: Sensitivity to interest rates
        - Usually least important for retail
    """)
    
    st.warning("⚠️ **Remember**: Options can expire worthless! Don't YOLO your rent money! 🏠")


def show_strategy_tab(data):
    """Show options strategy ideas"""
    st.subheader("🎯 Options Strategy Builder")
    
    current_price = data["current_price"]
    ticker = data["ticker"]
    
    st.markdown(f"### Current {ticker} Price: {format_currency(current_price)}")
    
    # Strategy selector
    strategy = st.selectbox(
        "Choose a Strategy",
        [
            "🚀 Long Call (Bullish YOLO)",
            "📉 Long Put (Bearish)",
            "💰 Covered Call (Income)",
            "🛡️ Cash-Secured Put (Wheel)",
            "🦋 Iron Condor (Theta Gang)",
            "⚡ Straddle (Earnings Play)",
            "🎯 Bull Call Spread (Moderate Bullish)"
        ]
    )
    
    st.markdown("---")
    
    if "Long Call" in strategy:
        st.markdown("### 🚀 Long Call Strategy")
        st.success("**When to use**: You think stock will moon! 🌙")
        st.markdown(f"""
        **Setup:**
        - Buy 1 call option at strike {format_currency(current_price * 1.05)} (5% OTM)
        - Choose expiration 30-60 days out
        - Max loss: Premium paid
        - Max gain: Unlimited! 🚀
        
        **Example:**
        - Stock at {format_currency(current_price)}
        - Buy {format_currency(current_price * 1.05)} call for $2.00
        - If stock hits {format_currency(current_price * 1.20)}, profit = {format_currency(current_price * 0.15 - 2)} per share!
        - Breakeven: {format_currency(current_price * 1.05 + 2)}
        """)
        
    elif "Long Put" in strategy:
        st.markdown("### 📉 Long Put Strategy")
        st.warning("**When to use**: You think stock will tank! 📉")
        st.markdown(f"""
        **Setup:**
        - Buy 1 put option at strike {format_currency(current_price * 0.95)} (5% OTM)
        - Max loss: Premium paid
        - Max gain: Strike - premium (if stock goes to $0)
        
        **Risk**: Puts can lose value fast if stock rallies!
        """)
        
    elif "Covered Call" in strategy:
        st.markdown("### 💰 Covered Call (Theta Gang)")
        st.success("**When to use**: You own 100 shares, want income! 💵")
        st.markdown(f"""
        **Setup:**
        - Own 100 shares of {ticker}
        - Sell 1 call at {format_currency(current_price * 1.10)} strike
        - Collect premium immediately!
        - If called away: Profit on shares + premium
        
        **Risk**: Limited upside if stock moons past strike
        **Reward**: Consistent income, reduces cost basis
        """)
        
    elif "Iron Condor" in strategy:
        st.markdown("### 🦋 Iron Condor (Theta Gang)")
        st.info("**When to use**: Stock will stay flat 📊")
        st.markdown(f"""
        **Setup** (Complex but profitable!):
        - Sell call at {format_currency(current_price * 1.05)}
        - Buy call at {format_currency(current_price * 1.10)}
        - Sell put at {format_currency(current_price * 0.95)}
        - Buy put at {format_currency(current_price * 0.90)}
        
        **Max Profit**: Premium collected (if stock stays between sold strikes)
        **Max Loss**: Width of spread - premium
        
        **Best for**: High IV, rangebound stocks
        """)
        
    elif "Straddle" in strategy:
        st.markdown("### ⚡ Long Straddle (Earnings Play)")
        st.warning("**When to use**: Big move expected, unsure direction! 📊")
        st.markdown(f"""
        **Setup:**
        - Buy ATM call at {format_currency(current_price)}
        - Buy ATM put at {format_currency(current_price)}
        
        **Wins if**: Stock moves big in EITHER direction!
        **Loses if**: Stock doesn't move (theta decay)
        
        **Perfect for**: Earnings announcements 📣
        """)
    
    st.markdown("---")
    st.error("⚠️ **DISCLAIMER**: Options are risky! Can lose 100% of premium. Not financial advice! 🚨")
