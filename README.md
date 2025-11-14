# 🎯 Smart Investment Dashboard

A zero-cost, high-speed, high-accuracy investment analysis platform with premium UI/UX that identifies when stocks, options, or crypto are "good buys" with confidence scoring.

## ✨ Features

### 📊 Core Features
- **Real-time Market Data** via yfinance (FREE)
- **Good Buy Detection Engine** with confidence scoring (0-100)
- **Advanced Valuation Models** (DCF with Monte Carlo, Multiples)
- **Technical Analysis** with pattern detection
- **Options Flow Analysis** with unusual activity detection
- **Sentiment Analysis** from StockTwits and news
- **Institutional & Insider Trading Tracking**
- **Premium UI/UX** with dark theme and clean visualizations

### 🎯 Good Buy Engine
The system analyzes multiple factors to determine optimal entry points:
- **Valuation Score**: DCF vs current price
- **Technical Score**: RSI, MACD, Support/Resistance
- **Sentiment Score**: Social media momentum
- **Momentum Score**: Price trends and pullbacks
- **Fundamentals Score**: P/E, margins, growth

Outputs:
- **GOOD BUY RANGE**: $XXX - $YYY
- **TARGET PRICE**: $ZZZ
- **CONFIDENCE SCORE**: ##/100
- **Risk/Reward Ratio**

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Internet connection for data fetching

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd smart-investment-dashboard
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys (optional for enhanced features)
```

4. Run the dashboard:
```bash
streamlit run main.py
```

5. Open browser to `http://localhost:8501`

## 📁 Project Structure

```
smart-investment-dashboard/
├── main.py              # Main Streamlit dashboard
├── data_fetcher.py      # Data fetching using yfinance
├── analysis_engine.py   # Valuation, technical analysis, buy signals
├── requirements.txt     # Python dependencies
├── .env.example        # Environment variables template
├── README.md           # This file
└── data/              # Cache directory (auto-created)
    └── cache/         # SQLite cache files
```

## 🔧 Configuration

### Environment Variables (Optional)
Create a `.env` file with:
```
# Optional - for enhanced sentiment analysis
GEMINI_API_KEY=your_key_here
REDDIT_CLIENT_ID=your_reddit_id
REDDIT_CLIENT_SECRET=your_reddit_secret
```

### Default Settings
- Default ticker: META
- Cache expiry: 5 minutes for real-time data
- Supported cryptos: BTC, ETH, XRP

## 📊 Data Sources

### Free Market Data (yfinance)
- Real-time quotes
- Historical OHLCV
- Options chains with Greeks
- Financial statements
- Institutional holdings
- Insider transactions
- Company info & fundamentals

### Sentiment Sources (Web Scraping)
- StockTwits API (free tier)
- Yahoo Finance news
- Reddit (requires API setup)

## 🎨 UI Features

### Dashboard Tabs
1. **Overview** - Price chart, key metrics, buy signal
2. **Valuation** - DCF analysis, multiples comparison
3. **Technical** - Indicators, patterns, support/resistance
4. **Sentiment** - Social media analysis
5. **Options** - Chain viewer, unusual activity
6. **News** - Latest news feed
7. **Institutional** - Holdings and insider trades
8. **Charts** - Advanced charting with indicators

### Visual Elements
- Dark theme optimized for trading
- Real-time update timer
- Color-coded buy signals (Green/Yellow/Red)
- Interactive Plotly charts
- Responsive layout

## 🚦 Buy Signal Interpretation

### Confidence Levels
- **70-100**: HIGH confidence (Strong Buy)
- **50-69**: MEDIUM confidence (Buy)
- **0-49**: LOW confidence (Hold/Wait)

### Signal Colors
- 🟢 **Green**: Strong buy opportunity
- 🟡 **Yellow**: Moderate opportunity
- 🔴 **Red**: Wait for better entry

## ⚡ Performance

- **Sub-second load times** with caching
- **5-minute cache** for real-time data
- **SQLite database** for persistent storage
- **Lazy loading** for heavy computations

## 🚀 Deployment

### Streamlit Cloud (FREE)
1. Push code to GitHub
2. Connect to [Streamlit Cloud](https://streamlit.io/cloud)
3. Deploy from GitHub repo
4. Set environment variables in Streamlit settings

### Local Deployment
Simply run:
```bash
streamlit run main.py --server.port 8501
```

## ⚠️ Disclaimer

**This dashboard is for educational purposes only. Not financial advice.**

- All data is obtained from free, public sources
- Calculations and signals are algorithmic suggestions
- Always do your own research before investing
- Past performance doesn't guarantee future results

## 🛠️ Troubleshooting

### Common Issues

1. **No data showing**
   - Check internet connection
   - Verify ticker symbol is valid
   - Clear cache and refresh

2. **Slow performance**
   - Data is cached for 5 minutes
   - First load may be slower
   - Check internet speed

3. **Missing indicators**
   - Some require minimum data points (e.g., 200 days for SMA200)
   - Not all tickers have options data

## 📝 Future Enhancements

- [ ] Portfolio tracking
- [ ] Backtesting engine
- [ ] More crypto pairs
- [ ] Email/SMS alerts
- [ ] AI-powered insights (with Gemini API)
- [ ] Custom screeners
- [ ] Risk management tools
- [ ] Multi-timeframe analysis

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Open a Pull Request

## 📜 License

MIT License - feel free to use for any purpose

## 🙏 Credits

- Market data: [yfinance](https://github.com/ranaroussi/yfinance)
- UI framework: [Streamlit](https://streamlit.io)
- Charts: [Plotly](https://plotly.com)
- Technical indicators: [TA-Lib](https://github.com/bukosabino/ta)

---

Built with ❤️ for retail investors | Not financial advice
