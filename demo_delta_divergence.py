"""
Demo: Delta Divergence Options Chart
Standalone test of the options delta divergence analyzer
"""
import streamlit as st
from src.utils.delta_divergence_chart import render_delta_divergence_chart

st.set_page_config(page_title="Delta Divergence Demo", page_icon="📊", layout="wide")

st.title("📊 Delta Divergence Options Analyzer - Demo")

st.markdown("""
This demo showcases the Delta Divergence Options Chart that analyzes market expectations
through volume-weighted call vs put delta analysis.
""")

# Ticker input
ticker = st.text_input("Enter ticker symbol:", value="AAPL", max_chars=10).upper()

if ticker:
    render_delta_divergence_chart(ticker)
else:
    st.info("Enter a ticker symbol to begin analysis")

# Show explanation
st.markdown("---")
st.markdown("""
### 🎯 Key Features Implemented

✅ **Diverging Bar Chart**
- Green bars: Call delta flow (bullish positioning)
- Red bars: Put delta flow (bearish positioning)  
- Net flow line: Overall market expectation

✅ **Interactive Expiration Slider**
- Select any available expiration date
- Shows days to expiration for each option
- Real-time calculation for selected date

✅ **Volume × Delta Weighting**
- Each option's delta is multiplied by its volume
- Gives more weight to high-conviction trades
- Uses open interest as backup for low-volume options

✅ **Automatic Market Expectation Label**
- 🟢 BULLISH: Strong call delta dominance
- 🟡 MODERATELY BULLISH: Slight call bias
- 🟡 MODERATELY BEARISH: Slight put bias
- 🔴 BEARISH: Strong put delta dominance

✅ **Additional Features**
- Summary chart across all expirations
- Detailed strike-level breakdown
- Call/Put ratio calculation
- Comprehensive interpretation guide
""")
