# 🔥 Analysis Master: One Ring To Rule Them All 🔥

*"One Dashboard to Rule Them All, One Framework to Find Them, One Platform to Bring Them All, and in the Alpha Bind Them."*

A comprehensive, Python-based quantitative analysis framework that democratizes institutional-grade market intelligence. This isn't your grandpa's stock screener - this is a full-spectrum **Digital Landscape Quantitative Modeler** that identifies market inefficiencies, scans for arbitrage opportunities, and generates forward-looking predictions by aggregating a vast array of free public data sources.

**Philosophy:** Blend the irreverent humor of r/wallstreetbets with the sophisticated quantitative tools of professional hedge funds. All models built on **100% free, public data**. No Bloomberg terminals required. 💎🙌

---

## 🎯 Project Goal & Philosophy

This project is a comprehensive framework for:
- **Quantitative Analysis**: Deep fundamental, technical, and risk analysis
- **Arbitrage Scanning**: Real-time detection of market inefficiencies (crypto triangular, statistical pairs trading)
- **Predictive Modeling**: LLM-powered forecasting using "digital landscape" variables (news, sentiment, economic data, congressional trades)
- **Portfolio Optimization**: Modern Portfolio Theory with efficient frontier analysis

The primary objective is to **identify market inefficiencies** and **generate forward-looking price predictions** by leveraging diverse data sources that Wall Street uses but democratized through free APIs.

---

## 🚀 Core Architecture: 5 Specialized Dashboards

### 📈 1. Equity Analysis Dashboard
*Deep-dive tool for comprehensive stock valuation and analysis.*

**Price & Technical Analysis:**
- Interactive Candlestick/OHLC charts with volume
- **Indicators**: RSI, MACD, ADX, On-Balance Volume (OBV), Bollinger Bands, SMA Crossovers
- **AI-Powered Pattern Recognition**: Head & Shoulders, Cup & Handle, Flags, Double Tops/Bottoms
- Real-time price alerts and momentum signals

**Fundamental & Financial Analysis:**
- Deep dive into financial statements (Income Statement, Balance Sheet, Cash Flow)
- **Ratio Analysis**: P/E, P/B, P/S, PEG, ROE, ROA, Profit Margins, Debt-to-Equity, Current Ratio
- Enterprise Value (EV) metrics and EV/EBITDA multiples
- Sector and industry peer comparisons

**Quantitative Valuation Models:**
- **Interactive DCF Calculator**: 🆕 Real-time valuation with adjustable parameters
  - 7 interactive sliders: Growth Rate, WACC, Terminal Growth, Projection Years
  - Live enterprise value and fair value calculations
  - Detailed breakdown of all intermediate steps
  - Visual cash flow projections
- **Monte Carlo Simulation**: 🆕 Statistical valuation with probability distributions
  - 100-10,000 simulation runs with configurable parameters
  - Confidence intervals (50%, 80%, 90%)
  - Probability distribution charts
  - Percentile analysis (5th through 95th percentiles)
- **Sensitivity Analysis**: 🆕 Impact analysis for key variables
  - One-way sensitivity for any parameter
  - Two-way sensitivity matrix (Growth vs WACC)
  - Interactive charts and heatmaps
- **Scenario Comparison**: 🆕 Bear/Base/Bull case analysis
  - Side-by-side scenario comparison
  - Customizable assumptions for each scenario
  - Visual comparison charts
- **Dividend Discount Model (DDM)**: Gordon Growth Model for income-generating equities
- **Net Asset Value (NAV)**: For asset-heavy companies (REITs, BDCs, holding companies)
- **Relative Valuation**: Multiples comparison against sector and industry peers

**Risk & Return Analysis:**
- **Beta** (Market Correlation) and **Rolling Volatility** (30-day window, annualized)
- **Sharpe Ratio** (Risk-Adjusted Return vs. risk-free rate)
- **Sortino Ratio** (Downside Risk-Adjusted Return - only penalizes downside volatility)
- **Maximum Drawdown Analysis** (worst peak-to-trough decline)
- **Value at Risk (VaR)** and **Conditional VaR (CVaR)**

**Ape Intelligence Engine:**
- Multi-factor confidence scoring (0-100 "Ape Score")
- Optimal entry price ranges with technical + fundamental confluence
- Target prices, stop losses, and risk/reward ratios
- Real-time sentiment from Reddit (7 subreddits), Twitter, and financial news

---

### ⚡ 2. Derivatives & Options Dashboard
*Identify opportunity and risk in the options market like an institutional flow desk.*

**Options Flow Analysis:**
- **Unusual Volume & Open Interest (OI) Scanner**: Flags abnormal activity
- **High Volume/OI Ratio Screening**: Detects new large positions being opened
- **Put/Call Ratio Analysis**: Overall market sentiment and specific underlying bias
- Dark pool and block trade detection (where free data available)

**Chain Analysis & The Greeks:**
- Real-time options chain visualization with bid/ask spreads
- **Greeks Tracking**: Delta, Gamma, Theta, Vega, Rho (calculated via py_vollib)
- **Implied Volatility (IV) Percentile**: Historical IV rank tracking
- **IV Skew Analysis**: Put skew vs. call skew (fear gauge)

**Strategy Builder & Visualization:**
- Payoff-diagram modeler for pre-built strategies:
  - **Spreads**: Bull/Bear Call/Put Spreads, Iron Condor, Iron Butterfly
  - **Volatility Plays**: Long/Short Straddle, Strangle
  - **Income**: Covered Call, Cash-Secured Put, Wheel Strategy
- Risk/Reward and Break-Even price analysis
- Probability of Profit (PoP) calculator

---

### 🚀 3. Crypto & Digital Assets Dashboard
*Analysis tools tailored for 24/7, high-volatility crypto markets.*

**Market & Technical Analysis:**
- Real-time price tracking for curated basket: BTC, ETH, XRP, SOL, DOGE, ADA, DOT, LINK, etc.
- Technical indicators adapted for 24/7 markets (no market-close gaps)
- Volume profile and order book depth analysis

**On-Chain & Sentiment Metrics:**
- **Fear & Greed Index** integration (alternative.me API)
- **HODL Wave & Strength Analysis**: Age distribution of UTXO set (where available via free APIs)
- **Transaction Volume** and **Active Address** monitoring (on-chain activity as demand proxy)
- Whale wallet tracking (large holder movements)

**Performance & Target Modeling:**
- **Price Target Projection Models**: Fibonacci extensions, Elliott Wave counts
- Historical volatility and performance analysis (1D, 7D, 30D, 90D, 1Y)
- **"When Lambo" Calculator**: Custom price target projections with timeline estimates 🏎️💨

---

### 🔬 4. Predictive Modeling & Arbitrage Dashboard
*The core alpha-generation engine. Scans for inefficiencies and predicts future moves.*

**Arbitrage Scanning Engine:**

**A. Crypto Triangular Arbitrage:**
- Scans for price discrepancies between three-pair assets across exchanges (via ccxt library)
- Example: BTC/USDT → ETH/BTC → ETH/USDT → back to BTC/USDT
- Real-time opportunity detection with expected profit % (after fees)
- Exchange latency and fee modeling

**B. Statistical Arbitrage (Pairs Trading):**
- Identifies highly correlated/cointegrated asset pairs (e.g., KO vs. PEP, XLE vs. crude oil)
- Models mean reversion using Ornstein-Uhlenbeck process
- Z-score deviation alerts (trade signal when |z| > 2)
- Cointegration testing (Engle-Granger, Johansen tests via statsmodels)

**LLM-Based Predictive Modeler (Powered by Claude):**
- **Ingests ALL "Digital Landscape" Variables:**
  - News sentiment (NewsAPI, Reddit, Twitter/X, StockTwits)
  - Economic data (CPI, unemployment, interest rates, GDP, oil inventories)
  - Political signals (congressional trades, insider transactions)
  - Technical and fundamental metrics from all dashboards
- **Correlation Discovery**: Models relationships between disparate data points
  - Example: "Does a surprise BLS unemployment report affect tech stock volatility 48 hours later?"
  - Example: "When senators buy defense stocks, does the defense sector outperform 30 days later?"
- **Price Direction Forecasts**: Generates bullish/bearish/neutral outlook with confidence scores
- **Natural Language Insights**: Explains predictions in plain English (or ape speak 🦍)

**Future Forecasting & Backtesting:**
- **Statistical Forecasting**: Prophet-based trend analysis with confidence intervals (80%, 90%, 95%)
- **Model Backtesting Engine**: 
  - Tests historical accuracy of all valuation models (DCF, P/E strategies)
  - Calculates MAPE (Mean Absolute Percentage Error) and win rate
  - Displays equity curves and drawdowns for each strategy
- **Monte Carlo Simulation**: 10,000 price path simulations for scenario analysis

**Short Squeeze Detection:**
- **High Short Interest Screening**: Filters for stocks with >20% short interest
- **Days-to-Cover Calculation**: Short interest / average daily volume
- **Squeeze Momentum Indicators**: Price + volume surge + short interest data
- **Cost-to-Borrow Tracking**: Where available via free APIs (Fintel, Ortex alternatives)

---

### 💼 5. Portfolio & Risk Management Dashboard
*Top-down portfolio construction and monitoring with institutional risk controls.*

**Portfolio Optimization:**
- **Modern Portfolio Theory (MPT)**: Efficient Frontier analysis to find optimal risk/return allocations
- **Maximum Sharpe Ratio Portfolio**: Highest risk-adjusted return combination
- **Minimum Volatility Portfolio**: Lowest volatility for risk-averse strategies
- **Risk Parity**: Equal risk contribution from each asset

**Asset Allocation & Risk:**
- **Multi-Asset Portfolio Builder**: Stocks, crypto, commodities, bonds (via ETFs)
- **Correlation Matrix Heatmap**: Visualizes diversification and hedging relationships
- **Beta-Neutral Portfolios**: Long/short combinations for market-neutral strategies
- **Tail Risk Hedging**: Allocation to defensive assets (VIX calls, gold, TLT)

**Rebalancing & Monitoring:**
- **Automatic Rebalancing Suggestions**: Threshold-based alerts (e.g., drift >5% from target)
- **Tax-Loss Harvesting Alerts**: Identifies losing positions for tax optimization
- **Performance Attribution**: Which holdings contributed to gains/losses
- **Scenario Analysis**: How does portfolio perform in recession, inflation, or crash scenarios?

---

## 📊 Data Sources & Predictive Strategy

This platform's strength is its aggregation of **diverse, free data sources**. All models built on public APIs or web scraping.

| **Data Category** | **Specific Sources (Free APIs/Libraries)** | **Predictive Value & Use Case** |
|-------------------|---------------------------------------------|----------------------------------|
| **Market Data** | `yfinance`, `ccxt`, `CoinGecko` (Free Tier) | Core OHLCV, volume, options chain. Foundation for all technical analysis and backtesting. |
| **Fundamental Data** | `yfinance`, `Alpha Vantage` (Free), `Financial Modeling Prep` (Free) | Financial statements, earnings, ratios. Inputs for DCF, DDM, relative valuation models. |
| **Economic Data (Macro)** | `fredapi` (Federal Reserve), `bls` (Bureau of Labor), `eia` (Energy Info Admin) | Macro trend analysis. Model correlations between CPI, interest rates, unemployment, oil inventories vs. asset class performance. |
| **Political & Insider** | Senate/House Public Disclosures (BeautifulSoup scraping), `Finnhub` (Free Tier) | Event-driven signals. Track congressional trades as leading indicator for sector policy. Monitor corporate insider buy/sell ratios. |
| **Alternative & Sentiment** | `praw` (Reddit), `snscrape` (Twitter/X), `StockTwits` API, `NewsAPI.org` (Dev Plan) | Real-time psychology. Feed sentiment velocity/scores into LLM to detect market psychology shifts before price reflects them. |
| **Crypto On-Chain** | `CoinGecko`, `Blockchain.com` API, `Glassnode` (limited free) | On-chain metrics (active addresses, transaction volume) as demand proxies for crypto assets. |

**Key Insight**: The magic happens when you **cross-correlate** these data silos. Example: A spike in defense stock purchases by senators + rising oil prices + hawkish Fed minutes = bullish signal for defense contractors (LMT, RTX, NOC).

---

## 🛠️ Technology Stack & Requirements

See `requirements.txt` for full dependencies.

### Core Dependencies
```plaintext
# Core Data Handling
pandas>=2.0.0
numpy>=1.24.0

# Web App & UI
streamlit>=1.28.0
plotly>=5.17.0

# Financial Data APIs
yfinance>=0.2.28
ccxt>=4.0.0              # Crypto exchange data & arbitrage
alpha-vantage            # Fundamental data
fredapi                  # Federal Reserve economic data
eia-python               # Energy Information Administration
finnhub-python           # Insider trades, news

# Social Media & News
praw>=7.7.0              # Reddit
newsapi-python           # News sentiment
textblob>=0.19.0         # Sentiment analysis
nltk>=3.9                # NLP
vaderSentiment>=3.3.2    # Financial sentiment

# Machine Learning & Forecasting
scikit-learn>=1.3.0      # ML, metrics, backtesting
scipy>=1.11.0            # Statistical tests
statsmodels              # Cointegration, time series
transformers             # Advanced NLP (HuggingFace)
torch                    # PyTorch backend
prophet                  # Time-series forecasting
anthropic                # Claude LLM integration

# Financial & Risk Analysis
ta>=0.11.0               # Technical Analysis
py_vollib>=1.0.1         # Options Greeks
pyfolio                  # Portfolio performance
quantstats               # Backtest metrics

# Storage & Caching
sqlalchemy>=2.0.0        # Database
pyarrow>=14.0.0          # Parquet storage

# Utils
python-dotenv>=1.0.0     # .env config
streamlit-option-menu>=0.3.6  # Navigation
beautifulsoup4>=4.12.0   # Web scraping
requests>=2.31.0         # HTTP requests
```

---

## 🚀 Quick Start

### 1. Clone the repository:
```bash
git clone https://github.com/tj309c/-Stocksv2.git
cd -Stocksv2
```

### 2. Install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Download NLTK data (required for sentiment analysis):
```bash
python -c "import nltk; nltk.download('brown'); nltk.download('punkt'); nltk.download('punkt_tab')"
```

### 4. Set up environment variables:
Create `.streamlit/secrets.toml` or `.env` file:

```toml
# === REQUIRED: LLM for Predictive Modeling ===
ANTHROPIC_API_KEY = "your_claude_api_key_here"

# === RECOMMENDED: Sentiment Analysis ===
REDDIT_CLIENT_ID = "your_reddit_client_id"
REDDIT_CLIENT_SECRET = "your_reddit_client_secret"
REDDIT_USER_AGENT = "AnalysisMaster/1.0"

# === OPTIONAL: Enhanced Features ===
NEWS_API_KEY = "your_newsapi_key"           # NewsAPI (100 req/day free)
ALPHA_VANTAGE_KEY = "your_av_key"           # Alpha Vantage (500 req/day free)
FINNHUB_API_KEY = "your_finnhub_key"        # Finnhub (60 req/min free)
FRED_API_KEY = "your_fred_key"              # Federal Reserve (unlimited free)
EIA_API_KEY = "your_eia_key"                # Energy Info Admin (free)
```

**How to Get Free API Keys:**
- **Anthropic Claude**: https://console.anthropic.com/ (Required - $5 credit for new users)
- **Reddit API**: https://www.reddit.com/prefs/apps (Highly recommended - 2 min setup)
- **FRED API**: https://fred.stlouisfed.org/docs/api/api_key.html (Free, instant)
- **NewsAPI**: https://newsapi.org/register (100 requests/day free)
- **Alpha Vantage**: https://www.alphavantage.co/support/#api-key (500 requests/day free)
- **Finnhub**: https://finnhub.io/register (60 requests/min free)
- **EIA**: https://www.eia.gov/opendata/register.php (Free, instant)

### 5. Run the dashboard:
```bash
streamlit run main.py
```

### 6. Open browser to `http://localhost:8501`

**🎉 You're ready to find alpha!**

---

## 📁 Project Structure

```
-Stocksv2/  (Analysis Master)
├── main.py                          # Main Streamlit app entry point
├── main_refactored.py               # Optimized entry with logging
├── requirements.txt                 # Python dependencies
├── .env                             # Environment variables (API keys) - NOT in git
├── .gitignore
│
├── src/
│   ├── dashboards/                  # Dashboard modules
│   │   ├── dashboard_equity.py          # (renamed from dashboard_stocks.py)
│   │   ├── dashboard_options.py         # Derivatives & Options
│   │   ├── dashboard_crypto.py          # Crypto & Digital Assets
│   │   ├── dashboard_predictive.py      # Predictive & Arbitrage (renamed from dashboard_advanced.py)
│   │   ├── dashboard_portfolio.py       # Portfolio & Risk Management
│   │   ├── dashboard_debug.py           # 🆕 Debug & Diagnostics Panel
│   │   └── dashboard_selector.py        # Navigation
│   │
│   ├── pipelines/                   # 🆕 Data ingestion modules
│   │   ├── get_market_data.py           # Market data (yfinance, ccxt)
│   │   ├── get_economic_data.py         # 🆕 FRED, BLS, EIA integration
│   │   ├── get_sentiment.py             # Sentiment (Reddit, Twitter, News)
│   │   └── get_political_data.py        # 🆕 Congressional trades, insider data
│   │
│   ├── analysis/                    # Core quantitative engines
│   │   ├── valuation_models.py          # DCF, DDM, NAV, Multiples
│   │   ├── technical_analysis.py        # RSI, MACD, pattern recognition
│   │   ├── risk_management.py           # Sharpe, Sortino, VaR, drawdowns
│   │   ├── predictive_models.py         # 🆕 LLM predictor, ML models
│   │   └── arbitrage_engine.py          # 🆕 Triangular, pairs trading
│   │
│   ├── core/                        # App configuration & utilities
│   │   ├── config.py                    # Settings, constants
│   │   ├── settings.py                  # Runtime configuration
│   │   ├── logging.py                   # Comprehensive logging
│   │   └── cache_manager.py             # 🆕 Cache control
│   │
│   └── utils/                       # Helper functions
│       ├── helpers.py                   # Formatters, validators
│       ├── sentiment_scraper.py         # Sentiment wrapper
│       └── api_monitor.py               # 🆕 API health checks
│
├── Stock_Scrapper/                  # Sentiment scraping tool
├── tests/                           # Unit tests
│   ├── test_valuation.py
│   ├── test_arbitrage.py
│   └── test_pipelines.py
│
├── data/                            # Cached data, logs
│   ├── cache/                       # SQLite cache files
│   └── logs/                        # Application logs
│
├── analysis_engine.py               # (Legacy - will migrate to src/analysis/)
├── data_fetcher.py                  # (Legacy - will migrate to src/pipelines/)
├── wsb_quotes.py                    # WSB humor generator
├── theme_manager.py                 # UI theming
└── debug_tools.py                   # (Will enhance & move to dashboard_debug.py)
```

---

## 🧪 Debugging & Diagnostics Panel

A robust **Debug Dashboard** is essential for managing dozens of live data feeds. Access via sidebar toggle.

**Features:**

### 1. API Status Monitor
- Real-time health checks for all external APIs (yfinance, FRED, NewsAPI, Claude, etc.)
- Displays HTTP status codes (✅ 200 OK or ❌ 404/503 ERROR)
- Ping latency tracking
- Remaining API quota/rate limit status (e.g., "NewsAPI: 87/100 requests remaining today")

### 2. Data Validation Viewer
- Select any raw data pipeline (e.g., "Get Fundamentals") and view the raw DataFrame/JSON
- Highlights `NaN`, `None`, or unexpected data types
- Schema validation with alerts for failures

### 3. Model Inspector ("Black Box" Debugger)
- Select a model (e.g., "DCF Valuation") and see **all intermediate calculations**
- Example for DCF: Shows FCF growth rate, terminal value, WACC, discount factors, final intrinsic value
- Catches division-by-zero, NaN propagation, assumption failures

### 4. Cache Management Console
- "Force Clear All Cache" button (wipes all `@st.cache_data` decorators)
- "Inspect Cache" viewer showing cached objects, sizes, expiration times

### 5. Live Log Stream
- Scrolling text box displaying real-time INFO, WARNING, ERROR logs
- No need to check terminal - debug directly in UI

### 6. Session State Viewer
- Displays entire `st.session_state` as collapsible JSON
- Critical for debugging button states, multi-page logic

---

## ⚠️ Disclaimer

**For Educational & Research Purposes Only. Not Financial Advice.**

- All data obtained from free, public sources and may contain inaccuracies or delays.
- All calculations, models, and signals are **algorithmic suggestions**, not investment recommendations.
- Trading and investing carry significant financial risk. **Always Do Your Own Research (DYOR)** before making decisions.
- Past performance is not indicative of future results.
- The developers assume no liability for any financial losses incurred using this platform.

**This app is built by apes, for apes. We eat crayons for breakfast. 🖍️🦍**

---

## 🎯 Roadmap

**Phase 1: Economic Data Integration** ✅ (In Progress)
- [ ] FRED API integration (macro data)
- [ ] BLS integration (employment data)
- [ ] EIA integration (energy data)

**Phase 2: Arbitrage Engine** 🚧 (Next)
- [ ] Crypto triangular arbitrage scanner
- [ ] Statistical arbitrage (pairs trading)
- [ ] Cointegration testing

**Phase 3: LLM Predictive Model** 🔮 (Next)
- [ ] Claude API integration
- [ ] Multi-source data aggregation
- [ ] Correlation discovery engine
- [ ] Natural language insights

**Phase 4: Debug & Diagnostics** 🛠️ (Next)
- [ ] API health monitor
- [ ] Model inspector
- [ ] Cache management UI
- [ ] Live log streaming

**Phase 5: Enhanced Sentiment** 📢 (Future)
- [ ] Twitter/X integration (snscrape)
- [ ] StockTwits API
- [ ] FinBERT for financial sentiment

**Phase 6: Advanced Portfolio** 💼 (Future)
- [ ] Risk parity optimization
- [ ] Tax-loss harvesting
- [ ] Monte Carlo portfolio simulation

---

## 🤝 Contributing

Contributions welcome! This is a community-driven, open-source project. If you want to add features, fix bugs, or improve documentation:

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📜 License

MIT License - Feel free to use, modify, and distribute. Just don't blame us when you YOLO into 0DTE options. 😅

---

## 💎 Built With WSB Energy

*This app was built with the spirit of r/wallstreetbets: high-IQ analysis meets maximum autism. We're here to find alpha, print tendies, and have fun doing it. Diamond hands only. 💎🙌*

**"The market can stay irrational longer than you can stay solvent. But with enough data, you can predict the irrationality." - Probably not Keynes**

---

**🚀 TO THE MOON! 🌙**

*Last Updated: November 14, 2025*  
*Version: 2.0.0 - "One Ring Edition"*
