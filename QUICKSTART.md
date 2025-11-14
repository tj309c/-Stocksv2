# 🚀 StocksV2 Dashboard - Quick Start Guide

## 🎯 What Is This?

A **Robinhood-inspired** stock analysis dashboard that combines:
- 💎 **Professional Financial Analysis** (DCF valuation, technical indicators, institutional tracking)
- 🦍 **WSB Dark Humor** (Diamond hands, ape signals, moon price targets)
- ⚡ **Options Trading Tools** (unusual activity, Greeks, strategy builder)
- 🚀 **Crypto Analysis** (HODL calculator, "When Lambo?", fear & greed index)

**100% FREE** - No API keys required! Uses yfinance for all market data.

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the App
```bash
streamlit run main.py
```

### 3. Open in Browser
```
http://localhost:8501
```

---

## 📊 Dashboard Guide

### **STOCKS Dashboard** 📈
**Best for:** Long-term investors, swing traders, value investors

**Features:**
- **Buy Signal Analysis**: See if a stock is a good buy with confidence scoring
- **Valuation (DD)**: DCF fair value, multiples analysis, price scenarios
- **Technical Analysis**: RSI, MACD, chart patterns, support/resistance
- **Sentiment Tracking**: Community vibes from StockTwits + news
- **Smart Money**: Institutional holdings and insider transactions

**Try These Tickers:**
- `AAPL` - Apple (blue chip)
- `TSLA` - Tesla (high volatility)
- `GME` - GameStop (meme stock)
- `NVDA` - NVIDIA (growth)
- `SPY` - S&P 500 ETF

---

### **OPTIONS Dashboard** ⚡
**Best for:** Options traders, risk-takers, advanced strategies

**Features:**
- **Unusual Activity**: Detect whale bets (high volume/OI ratio)
- **Options Chain**: View calls/puts with ITM highlighting
- **Greeks Guide**: Learn Delta, Gamma, Theta, Vega, Rho
- **Strategy Builder**: Pre-built strategies with examples
  - Long Call (YOLO plays)
  - Covered Call (income generation)
  - Iron Condor (theta gang)
  - Straddle (earnings plays)

**Try These Tickers:**
- `SPY` - Most liquid options
- `QQQ` - NASDAQ ETF
- `AAPL` - High volume, tight spreads
- `TSLA` - High IV, exciting moves

**Warning:** Options can expire worthless! Don't YOLO rent money! 🏠

---

### **CRYPTO Dashboard** 🚀
**Best for:** HODLers, degens, moon chasers

**Features:**
- **Price Action**: Multi-timeframe candlestick charts
- **Technical Analysis**: RSI, MACD, trend detection
- **Fear & Greed Index**: Market sentiment gauge
- **HODL Calculator**: Calculate "When Lambo?" 🏎️
- **DCA Strategy**: Plan your dollar-cost-averaging

**Try These Cryptos:**
- `BTC-USD` - Bitcoin (king)
- `ETH-USD` - Ethereum (smart contracts)
- `SOL-USD` - Solana (fast)
- `DOGE-USD` - Dogecoin (meme)

---

## 🎨 Features

### Theme Toggle 🌗
- **Light Mode** (default): Clean, Robinhood-inspired
- **Dark Mode**: WSB dark theme for late-night trading
- Toggle in sidebar

### Debug Tools 🔧
- Available in sidebar
- Check dependencies, file integrity, API connectivity
- Auto-diagnosis of common issues

### Mobile Responsive 📱
- Works on phones, tablets, desktops
- Swipe-friendly navigation
- Optimized charts for small screens

---

## 💡 Pro Tips

### For Stocks
1. **Check multiple timeframes**: Compare 1M, 3M, 1Y charts
2. **Cross-reference**: Use technical + fundamental + sentiment together
3. **Watch smart money**: Insider buying is a bullish signal
4. **Don't chase**: If confidence is low, wait for a better entry

### For Options
1. **Start with liquid tickers**: SPY, QQQ, AAPL have tight spreads
2. **Check IV**: High IV = expensive options
3. **Use defined risk**: Spreads limit max loss
4. **Time decay hurts**: Don't hold options too close to expiration

### For Crypto
1. **HODL philosophy**: Buy and hold through dips
2. **DCA is smart**: Average down your cost basis
3. **Don't FOMO**: Fear of missing out leads to bad trades
4. **Take profits**: Nothing wrong with securing gains

---

## ⚠️ Disclaimers

### Not Financial Advice
This dashboard is for **educational and entertainment purposes only**. We are not financial advisors. Do your own research (DD).

### Risk Warning
- **Stocks**: Can lose value
- **Options**: Can expire worthless (100% loss)
- **Crypto**: Extremely volatile

### Data Source
- Uses **yfinance** (free, public data)
- Data may have delays or inaccuracies
- Not suitable for high-frequency trading

### Humor Warning
Contains WSB-style humor and terminology:
- "Stonks" = Stocks
- "Tendies" = Profits
- "Diamond Hands" = Hold through dips
- "Paper Hands" = Sell too early
- "Moon" = Large price increase
- "Ape" = Retail investor

If this offends you, this dashboard might not be for you! 🦍

---

## 🔧 Troubleshooting

### App Won't Start
```bash
# Check dependencies
pip install -r requirements.txt

# Check Python version (needs 3.9+)
python --version

# Try clearing cache
rm -rf data/cache/market_data.db
```

### Data Not Loading
- **Check internet connection** (needs to reach Yahoo Finance)
- **Try a different ticker** (some tickers may have issues)
- **Wait a minute** (yfinance has rate limits)

### Charts Not Displaying
- **Refresh the page** (F5 or Cmd+R)
- **Clear browser cache**
- **Try a different browser**

### Slow Performance
- **Clear cache**: Delete `data/cache/market_data.db`
- **Restart app**: Ctrl+C and `streamlit run main.py`
- **Reduce timeframe**: Use shorter periods (1M instead of 1Y)

---

## 🤝 Contributing

Want to add features? Found a bug?

1. Fork the repo
2. Create a feature branch
3. Make your changes
4. Submit a pull request

**Ideas Welcome:**
- New technical indicators
- Additional options strategies
- More crypto metrics
- UI/UX improvements
- Bug fixes

---

## 📚 Resources

### Learn More
- [WSB Reddit](https://reddit.com/r/wallstreetbets) - For the memes
- [Investopedia](https://investopedia.com) - For serious learning
- [Options Profit Calculator](https://optionsprofitcalculator.com) - Model strategies
- [TradingView](https://tradingview.com) - Advanced charting

### Tools Used
- [Streamlit](https://streamlit.io) - Web framework
- [yfinance](https://github.com/ranaroussi/yfinance) - Market data
- [Plotly](https://plotly.com/python/) - Interactive charts
- [TA-Lib](https://ta-lib.org/) - Technical analysis

---

## 🎓 Understanding the Metrics

### Buy Signal Confidence (0-100)
- **70+**: Strong buy (diamond hands territory)
- **50-70**: Moderate buy (decent opportunity)
- **<50**: Wait (maybe not the best time)

### RSI (Relative Strength Index)
- **<30**: Oversold (potential buy)
- **30-70**: Neutral
- **>70**: Overbought (potential sell)

### MACD (Moving Average Convergence Divergence)
- **Bullish Crossover**: MACD crosses above signal line (buy signal)
- **Bearish Crossover**: MACD crosses below signal line (sell signal)

### P/E Ratio (Price-to-Earnings)
- **<15**: Potentially undervalued
- **15-25**: Fair value
- **>25**: Potentially overvalued (or growth stock)

### Volume/OI Ratio (Options)
- **>2**: Unusual activity (whales entering new positions)
- **<1**: Normal activity

---

## 🏆 Success Stories

Use this dashboard to:
- ✅ Identify undervalued stocks before rallies
- ✅ Spot unusual options activity (whale bets)
- ✅ Time crypto entries during fear (buy the dip)
- ✅ Learn options strategies risk-free (paper trading)
- ✅ Track institutional smart money moves

---

## 🌟 Final Thoughts

**This dashboard combines:**
- 🎯 Professional analysis tools
- 😂 WSB humor and culture
- 🎨 Beautiful, clean design
- ⚡ Fast, optimized performance
- 💎 100% free, no API keys

**Remember:**
- Do your own research
- Only invest what you can afford to lose
- HODL with diamond hands 💎🙌
- Stonks only go up! 📈 (just kidding, they don't)

---

**Made with 💎 by degens, for degens**

*"We may stay retarded longer than the market can stay irrational"* - WSB Proverb

🚀🌙 To the moon! 🌙🚀

---

*Last Updated: November 14, 2025*  
*Version: 2.0*
