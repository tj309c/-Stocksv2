# API Keys and Configuration Guide

## Required vs Optional API Keys

### ✅ **NO API KEYS REQUIRED FOR BASIC FUNCTIONALITY**

The dashboard works completely **FREE** without any API keys using:
- **yfinance** - Market data (stocks, options, crypto)
- **StockTwits** - Public sentiment data  
- **Yahoo Finance** - News and company info

---

## Optional API Keys (Enhanced Features)

### 🤖 **1. Google Gemini API (Optional)**
**Purpose:** AI-powered insights and enhanced analysis

**Get Your Key:**
1. Visit: https://makersuite.google.com/app/apikey
2. Click "Get API Key"
3. Copy your key

**Setup:**
```bash
# Add to .env file
GEMINI_API_KEY=your_gemini_api_key_here
```

**Features Enabled:**
- AI-generated buy/sell recommendations
- Natural language analysis
- Enhanced sentiment scoring

**Cost:** FREE tier available (60 requests/minute)

---

### 🗨️ **2. Reddit API (Optional)**
**Purpose:** Enhanced sentiment analysis from r/wallstreetbets and other subs

**Get Your Keys:**
1. Visit: https://www.reddit.com/prefs/apps
2. Click "Create App" or "Create Another App"
3. Select "script" type
4. Note your `client_id` and `client_secret`

**Setup:**
```bash
# Add to .env file
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_secret
REDDIT_USER_AGENT=YourAppName/1.0
```

**Features Enabled:**
- Reddit mention tracking
- WSB sentiment analysis
- Trending tickers detection

**Cost:** FREE

---

## Configuration File (.env)

Create a `.env` file in the project root:

```bash
# Optional - Gemini AI
GEMINI_API_KEY=

# Optional - Reddit
REDDIT_CLIENT_ID=
REDDIT_CLIENT_SECRET=
REDDIT_USER_AGENT=InvestmentDashboard/1.0

# Database (Auto-created, no setup needed)
DB_PATH=data/market_data.db
```

---

## Current Feature Status

### ✅ **Working WITHOUT API Keys:**
- ✓ Real-time stock quotes (yfinance)
- ✓ Historical price data
- ✓ Technical indicators (RSI, MACD, Bollinger Bands)
- ✓ Options chains with Greeks
- ✓ Fundamental data (P/E, EPS, market cap)
- ✓ StockTwits sentiment
- ✓ Yahoo Finance news
- ✓ Institutional holdings
- ✓ Insider transactions
- ✓ Crypto prices (BTC, ETH, altcoins)
- ✓ DCF valuation models
- ✓ Buy signal detection

### 🔒 **Requires API Keys:**
- Reddit sentiment (REDDIT_* keys)
- AI-powered insights (GEMINI_API_KEY)

---

## Troubleshooting

### Issue: "No data returned"
**Solution:** 
- Check internet connection
- yfinance may be rate-limited (wait 60 seconds)
- Try a different ticker symbol

### Issue: "Module not found"
**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: "Cannot create data directory"
**Solution:**
```bash
mkdir -p data/cache
chmod 755 data
```

### Issue: "Reddit/Gemini features not working"
**Solution:**
- These are OPTIONAL
- App works without them
- Add API keys only if you want enhanced features

---

## Testing Your Setup

Run the built-in diagnostic tool:
1. Start the app: `streamlit run main.py`
2. Check the sidebar for "System Status"
3. Click "Run Full Diagnostics"
4. Review any issues and follow recommendations

---

## Cost Breakdown

| Service | Cost | Required |
|---------|------|----------|
| yfinance | **FREE** | ✅ Yes |
| StockTwits | **FREE** | ✅ Yes |
| Yahoo Finance | **FREE** | ✅ Yes |
| Google Gemini | FREE tier available | ❌ Optional |
| Reddit API | **FREE** | ❌ Optional |

**Total Required Cost: $0.00** 🚀

---

## Security Best Practices

1. **Never commit `.env` file to git**
   ```bash
   # Add to .gitignore
   .env
   .env.local
   ```

2. **Use environment variables in production**
   ```bash
   export GEMINI_API_KEY="your_key"
   export REDDIT_CLIENT_ID="your_id"
   ```

3. **Rotate keys periodically**
   - Regenerate API keys every 90 days
   - Remove unused keys immediately

---

## Need Help?

1. **Run diagnostics** - Use the built-in tool in the sidebar
2. **Check logs** - Look at `streamlit.log` for errors
3. **Verify dependencies** - Ensure all packages are installed
4. **Test individually** - Try each dashboard separately

---

**Remember:** The dashboard is fully functional without any API keys! 🎉
