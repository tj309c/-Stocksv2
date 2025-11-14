# 🎯 Smart Investment Dashboard - StocksV2

A comprehensive, zero-cost investment analysis platform with **5 specialized dashboards** for stocks, options, crypto, advanced analytics, and portfolio optimization. Features professional-grade analysis with WSB-style humor.

## 🚀 5 Specialized Dashboards

### 📈 1. STOCKS Dashboard
**Price & Technical Analysis**
- Interactive price charts with RSI, MACD, ADX, OBV indicators
- Bollinger Bands and SMA crossovers
- AI-powered chart pattern recognition (Head & Shoulders, Cup & Handle, Double Bottom)

**Fundamental Analysis**
- Deep dive into P/E ratios, profit margins, ROE
- Enterprise value metrics and sector comparison

**Valuation Models**
- Discounted Cash Flow (DCF) with Monte Carlo simulation
- Dividend Discount Model (DDM) for dividend stocks
- Net Asset Value (NAV) for asset-heavy companies
- Relative valuation (P/E, P/B, PEG multiples)

**Risk Analysis**
- Beta calculation and volatility metrics
- Sharpe Ratio (risk-adjusted return)
- Sortino Ratio (downside risk focus)
- Rolling volatility charts
- Maximum drawdown analysis

**Good Buy Engine**
- Multi-factor confidence scoring (0-100)
- Optimal entry price ranges
- Target prices and stop losses
- Risk/reward ratio calculation

### ⚡ 2. OPTIONS Dashboard
**Options Flow Analysis**
- Unusual options activity detection
- High volume/OI ratio screening
- Real-time options chain with Greeks

**Greeks Analysis**
- Delta, Gamma, Theta, Vega, Rho
- IV percentile tracking
- Put/Call ratio analysis

**Strategy Builder**
- Pre-built strategies (Iron Condor, Butterfly, Straddle, etc.)
- Risk/reward visualization
- Break-even analysis

### 🚀 3. CRYPTO Dashboard
**Crypto Analysis**
- Real-time crypto price tracking (BTC, ETH, XRP, SOL, DOGE, etc.)
- Technical indicators adapted for crypto
- HODL strength calculator
- Fear & Greed index

**When Lambo Calculator**
- Custom price target projections
- Historical performance analysis

### 🔬 4. ADVANCED ANALYTICS Dashboard
**Model Backtesting**
- Historical DCF accuracy testing
- P/E relative valuation backtesting
- MAPE (Mean Absolute Percentage Error) metrics
- Model performance tracking over time

**Future Forecasting**
- Statistical price predictions
- Prophet-based trend forecasting
- Confidence intervals (80%, 90%, 95%)
- Bull/Bear scenario analysis

**Short Squeeze Detection**
- High short interest identification
- Squeeze momentum indicators
- Days-to-cover calculation
- Short squeeze leaderboard

**Sector Comparison**
- Relative valuation vs sector peers
- Industry benchmarking
- Sector rotation analysis

### 💼 5. PORTFOLIO MANAGER Dashboard
**Portfolio Optimization**
- Modern Portfolio Theory implementation
- Efficient frontier analysis
- Risk-return optimization
- Maximum Sharpe ratio portfolio

**Asset Allocation**
- Multi-asset portfolio builder
- Optimal weight calculations
- Diversification recommendations
- Correlation matrix heatmap

**Rebalancing**
- Automatic rebalancing suggestions
- Threshold-based alerts
- Tax-efficient rebalancing strategies

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Internet connection for data fetching

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd Stocksv2
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download NLTK data (required for sentiment analysis):
```bash
python -c "import nltk; nltk.download('brown'); nltk.download('punkt'); nltk.download('punkt_tab')"
```

4. **(Optional but Recommended)** Configure API keys for real-time sentiment data:

   Create a `.streamlit/secrets.toml` file:
   ```toml
   # Reddit API (Free - https://www.reddit.com/prefs/apps)
   REDDIT_CLIENT_ID = "your_client_id_here"
   REDDIT_CLIENT_SECRET = "your_client_secret_here"
   REDDIT_USER_AGENT = "StocksV2App/1.0"
   
   # NewsAPI (Optional - Free tier: 100 requests/day - https://newsapi.org/)
   NEWS_API_KEY = "your_newsapi_key_here"
   ```
   
   **How to get free API keys:**
   
   **Reddit API** (Highly Recommended):
   - Visit https://www.reddit.com/prefs/apps
   - Click "Create App" or "Create Another App"
   - Select "script" type
   - Name: "StocksV2App"
   - Redirect URI: http://localhost:8501
   - Copy the **client ID** (under app name) and **secret**
   - **Benefits**: Access to wallstreetbets, r/stocks, r/investing sentiment
   
   **NewsAPI** (Optional):
   - Visit https://newsapi.org/register
   - Sign up for free account (100 requests/day)
   - Copy your API key from dashboard
   - **Benefits**: Real financial news sentiment analysis

5. Run the dashboard:
```bash
streamlit run main.py
# or use the optimized version:
streamlit run main_refactored.py
```

6. Open browser to `http://localhost:8501`

**Note**: The app works without API keys but will show simulated sentiment data. Configure Reddit API for real social media sentiment tracking!

## 📁 Project Structure

```
StocksV2/
├── main.py                      # Main entry point (original)
├── main_refactored.py           # Optimized entry point with new features
├── analysis_engine.py           # Valuation & technical analysis engines
├── data_fetcher.py              # Market data fetching (yfinance)
├── dashboard_stocks.py          # Stocks dashboard
├── dashboard_options.py         # Options dashboard
├── dashboard_crypto.py          # Crypto dashboard
├── dashboard_advanced.py        # 🆕 Advanced analytics dashboard
├── dashboard_portfolio.py       # 🆕 Portfolio optimization dashboard
├── dashboard_selector.py        # Dashboard navigation
├── theme_manager.py             # UI theming (light/dark mode)
├── utils.py                     # Utility functions
├── wsb_quotes.py                # WSB-style humor
├── debug_tools.py               # Debug panel
├── requirements.txt             # Dependencies
├── src/                         # 🆕 Organized code structure
│   ├── config/                  # Configuration management
│   │   ├── constants.py         # All magic numbers
│   │   └── settings.py          # Runtime settings
│   ├── core/                    # Core functionality
│   │   └── logging.py           # Comprehensive logging
│   ├── components/              # Reusable components (future)
│   ├── dashboards/              # Dashboard modules (future)
│   └── utils/                   # Utilities (future)
├── tests/                       # Unit tests
│   ├── test_config.py
│   └── test_utils.py
├── logs/                        # Application logs
│   ├── app.log
│   ├── data.log
│   ├── analysis.log
│   ├── cache.log
│   └── error.log
└── data/                        # Cache directory
    └── cache/                   # SQLite cache files
```

## 🔧 Configuration

### Sentiment Scraper Setup
The dashboard includes a **Stock_Scrapper** tool that provides real-time sentiment analysis from Reddit and news sources.

**Features:**
- Reddit scraping from 7 subreddits (wallstreetbets, stocks, investing, StockMarket, options, Daytrading, SecurityAnalysis)
- News scraping from NewsAPI
- Yahoo Finance RSS feed integration
- TextBlob sentiment analysis (polarity + subjectivity scores)
- Automatic caching (1-hour TTL to avoid rate limits)

**Two Modes:**
1. **Basic Scraper** (no API keys required):
   - Uses Reddit JSON API (no authentication)
   - Limited to 4 subreddits
   - Yahoo Finance news only
   
2. **Enhanced Scraper** (recommended):
   - Full Reddit API access via PRAW
   - 7 subreddits + better data quality
   - NewsAPI integration for financial news
   - Requires free API keys (see Installation section)

### Environment Variables (Optional)
Configure via `.streamlit/secrets.toml`:
```toml
# Reddit API (Free - highly recommended)
REDDIT_CLIENT_ID = "your_client_id"
REDDIT_CLIENT_SECRET = "your_client_secret"
REDDIT_USER_AGENT = "StocksV2App/1.0"

# NewsAPI (Optional - free tier available)
NEWS_API_KEY = "your_api_key"
```

### Default Settings
- Default ticker: META
- Cache expiry: 5 minutes for market data, 1 hour for sentiment
- Supported cryptos: BTC, ETH, XRP, SOL, DOGE
- Sentiment sources: Reddit (7 subreddits), NewsAPI, Yahoo Finance

## 🎯 Complete Feature List

### Price & Technical Analysis
✅ Interactive price charts  
✅ RSI, MACD, ADX, OBV indicators  
✅ Bollinger Bands, SMA crossovers  
✅ AI-powered pattern recognition  

### Fundamental Analysis
✅ P/E ratios, margins, returns  
✅ Enterprise value metrics  
✅ Sector comparison & benchmarking  

### Valuation Models
✅ Discounted Cash Flow (DCF)  
✅ Dividend Discount Model (DDM)  
✅ Net Asset Value (NAV)  
✅ Relative valuation (P/E, P/B, PEG)  

### Risk Analysis
✅ Beta calculation  
✅ Sharpe & Sortino ratios  
✅ Rolling volatility charts  
✅ Maximum drawdown  

### Model Backtesting
✅ Historical DCF accuracy  
✅ P/E relative valuation backtesting  
✅ MAPE (Mean Absolute Percentage Error) metrics  

### Future Forecasting
✅ Statistical price predictions  
✅ Confidence intervals (80%, 90%, 95%)  
✅ Trend analysis  

### Short Squeeze Detection
✅ High short interest identification  
✅ Squeeze momentum indicators  
✅ Short squeeze leaderboard  

### Portfolio Optimization
✅ Efficient frontier analysis  
✅ Modern Portfolio Theory  
✅ Risk-return optimization  
✅ Correlation matrix  
✅ Auto-rebalancing suggestions  

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
