"""
Dashboard Selector - Choose your trading adventure! 🚀
With WSB-style fun animations and terminology
Maximum autism, maximum gains (or losses, probably losses)
"""
import streamlit as st
import time
from wsb_quotes import get_dashboard_tagline, get_loading_message

def show_selector():
    """Display the fun dashboard selector with animations"""
    
    # Custom CSS for animations and styling
    st.markdown("""
    <style>
        @keyframes rocket {
            0%, 100% { transform: translateY(0px) rotate(45deg); }
            50% { transform: translateY(-20px) rotate(45deg); }
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }
        
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            25% { transform: translateX(-5px); }
            75% { transform: translateX(5px); }
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }
        
        .main-title {
            text-align: center;
            font-size: 4em;
            font-weight: bold;
            background: linear-gradient(45deg, #00FF88, #00D4FF, #FFB700);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: pulse 2s infinite;
            margin-bottom: 20px;
        }
        
        .subtitle {
            text-align: center;
            font-size: 1.5em;
            color: #00D4FF;
            margin-bottom: 50px;
        }
        
        .dashboard-card {
            background: linear-gradient(135deg, rgba(28, 31, 38, 0.9), rgba(28, 31, 38, 0.6));
            border: 3px solid;
            border-radius: 20px;
            padding: 40px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            margin: 10px;
            height: 100%;
        }
        
        .dashboard-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 20px 40px rgba(0, 212, 255, 0.3);
        }
        
        .stocks-card {
            border-color: #00FF88;
        }
        
        .stocks-card:hover {
            background: linear-gradient(135deg, rgba(0, 255, 136, 0.2), rgba(28, 31, 38, 0.8));
        }
        
        .options-card {
            border-color: #FFB700;
        }
        
        .options-card:hover {
            background: linear-gradient(135deg, rgba(255, 183, 0, 0.2), rgba(28, 31, 38, 0.8));
        }
        
        .crypto-card {
            border-color: #00D4FF;
        }
        
        .crypto-card:hover {
            background: linear-gradient(135deg, rgba(0, 212, 255, 0.2), rgba(28, 31, 38, 0.8));
        }
        
        .card-icon {
            font-size: 5em;
            margin-bottom: 20px;
        }
        
        .stocks-icon {
            animation: float 3s ease-in-out infinite;
        }
        
        .options-icon {
            animation: shake 2s ease-in-out infinite;
        }
        
        .crypto-icon {
            animation: rocket 2s ease-in-out infinite;
        }
        
        .card-title {
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 15px;
        }
        
        .card-subtitle {
            font-size: 1.2em;
            color: #ccc;
            margin-bottom: 20px;
        }
        
        .card-features {
            text-align: left;
            font-size: 1em;
            color: #aaa;
            margin-top: 20px;
        }
        
        .ape-mode {
            text-align: center;
            font-size: 0.8em;
            color: #666;
            margin-top: 50px;
            font-style: italic;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Main title with animation
    st.markdown('<h1 class="main-title">🚀 APE TRADING HQ 🚀</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Choose Your Path to Tendies (or Wendy\'s)... 💰</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle" style="font-size: 1em; color: #666;">*Not financial advice. We\'re all regarded here.*</p>', unsafe_allow_html=True)
    
    # Dashboard selection cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="dashboard-card stocks-card">
            <div class="card-icon stocks-icon">📈</div>
            <div class="card-title" style="color: #00FF88;">STONKS</div>
            <div class="card-subtitle">💎🙌 Diamond Hands Only 🦍</div>
            <div class="card-features">
                ✅ Real-time copium tracking<br>
                ✅ "DD" (crayon analysis)<br>
                ✅ Bag holder valuation<br>
                ✅ Ape sentiment heatmap<br>
                ✅ Lambo price calculator<br>
                🚨 Includes loss porn generator
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🦍 **STONKS ONLY GO UP!**", key="stocks", width='stretch', type="primary"):
            st.session_state.selected_dashboard = "stocks"
            st.session_state.dashboard_selected = True
            show_rocket_animation()
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="dashboard-card options-card">
            <div class="card-icon options-icon">⚡</div>
            <div class="card-title" style="color: #FFB700;">OPTIONS</div>
            <div class="card-subtitle">🎰 Maximum Autism 🤡</div>
            <div class="card-features">
                ✅ 0DTE FD scanner<br>
                ✅ Theta gang HQ<br>
                ✅ Nancy Pelosi tracker<br>
                ✅ IV crush calculator<br>
                ✅ Margin call predictor<br>
                🚨 Bankruptcy speedrun mode
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("⚡ **YOLO THE RENT MONEY!**", key="options", width='stretch', type="primary"):
            st.session_state.selected_dashboard = "options"
            st.session_state.dashboard_selected = True
            show_rocket_animation()
            st.rerun()
    
    with col3:
        st.markdown("""
        <div class="dashboard-card crypto-card">
            <div class="card-icon crypto-icon">🚀</div>
            <div class="card-title" style="color: #00D4FF;">CRYPTO</div>
            <div class="card-subtitle">🌙 Have Fun Staying Poor 💎</div>
            <div class="card-features">
                ✅ Shitcoin tracker<br>
                ✅ HODL strength meter<br>
                ✅ Rugpull detector 2.0<br>
                ✅ Dip buyer's remorse<br>
                ✅ $69,420 countdown<br>
                🚨 Accepts Monopoly money
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🌙 **WEN LAMBO?! (spoiler: never)**", key="crypto", width='stretch', type="primary"):
            st.session_state.selected_dashboard = "crypto"
            st.session_state.dashboard_selected = True
            show_rocket_animation()
            st.rerun()
    
    # Fun footer
    st.markdown("""
    <div class="ape-mode">
        <p>⚠️ Not financial advice. We're all regarded here. ⚠️</p>
        <p>💎🙌 Diamond hands only. Paper hands exit left. 🧻👎</p>
        <p>🦍 Ape together strong. Ape alone... also strong? (probably not)</p>
        <p>📉 Your losses = Our gain porn 📈</p>
    </div>
    """, unsafe_allow_html=True)


def show_rocket_animation():
    """Show a fun loading animation when dashboard is selected"""
    loading_msg = get_loading_message()
    
    st.markdown("""
    <style>
        @keyframes launch {
            0% { transform: translateY(0) rotate(45deg); opacity: 1; }
            100% { transform: translateY(-500px) rotate(45deg); opacity: 0; }
        }
        
        .rocket-launch {
            font-size: 5em;
            text-align: center;
            animation: launch 1s ease-out;
        }
        
        .loading-text {
            text-align: center;
            font-size: 1.5em;
            color: #00FF88;
            margin-top: 20px;
            font-style: italic;
        }
    </style>
    <div style="height: 300px;">
        <div class="rocket-launch">🚀</div>
        <div class="loading-text">""" + loading_msg + """</div>
    </div>
    """, unsafe_allow_html=True)
    time.sleep(0.8)


def show_dashboard_switcher():
    """Show dashboard switcher in sidebar"""
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔄 Switch Dashboard")
    
    current = st.session_state.get("selected_dashboard", "stocks")
    
    # Display current dashboard
    dashboard_emojis = {
        "stocks": "📈 STONKS",
        "options": "⚡ OPTIONS",
        "crypto": "🚀 CRYPTO"
    }
    
    st.sidebar.info(f"**Current:** {dashboard_emojis.get(current, 'Unknown')}")
    
    # Switch buttons
    col1, col2, col3 = st.sidebar.columns(3)
    
    with col1:
        if st.button("📈", key="switch_stocks", help="Stocks Dashboard", width='stretch'):
            if current != "stocks":
                st.session_state.selected_dashboard = "stocks"
                st.rerun()
    
    with col2:
        if st.button("⚡", key="switch_options", help="Options Dashboard", width='stretch'):
            if current != "options":
                st.session_state.selected_dashboard = "options"
                st.rerun()
    
    with col3:
        if st.button("🚀", key="switch_crypto", help="Crypto Dashboard", width='stretch'):
            if current != "crypto":
                st.session_state.selected_dashboard = "crypto"
                st.rerun()
    
    # Reset button
    if st.sidebar.button("🏠 Back to Menu", width='stretch'):
        st.session_state.dashboard_selected = False
        st.session_state.selected_dashboard = None
        st.rerun()
