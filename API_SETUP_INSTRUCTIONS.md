# 🔑 API Keys Setup Instructions

**Date:** November 14, 2025  
**Status:** In Progress

---

## ✅ ALREADY CONFIGURED

- **FRED API** ✅ (Key already in secrets.toml)

---

## 🚀 STEP-BY-STEP API KEY SETUP

### 1. Reddit API (5 minutes) - HIGHEST PRIORITY

**Why:** Real sentiment analysis from r/wallstreetbets and other investing subreddits

**Steps:**
1. Go to https://www.reddit.com/prefs/apps
2. Log in to Reddit (or create account)
3. Scroll to bottom and click **"create another app..."**
4. Fill in:
   - **Name:** StocksV2 Analyzer
   - **App type:** Select "script"
   - **Description:** Stock sentiment analysis tool
   - **About URL:** (leave blank)
   - **Redirect URI:** http://localhost:8501
5. Click **"create app"**
6. You'll see:
   - **Client ID** (under the app name, looks like: `dQw4w9WgXcQ`)
   - **Secret** (labeled "secret", longer string)

**Add to secrets.toml:**
```toml
REDDIT_CLIENT_ID = "your_client_id_here"
REDDIT_CLIENT_SECRET = "your_secret_here"
REDDIT_USER_AGENT = "StocksAnalyzer/1.0"
```

---

### 2. News API (2 minutes) - HIGH PRIORITY

**Why:** Financial news headlines and sentiment

**Steps:**
1. Go to https://newsapi.org/register
2. Enter email and password
3. Check email for verification
4. Log in and copy your API key from dashboard

**Limits:** 100 requests/day (free tier)

**Add to secrets.toml:**
```toml
NEWSAPI_KEY = "your_newsapi_key_here"
```

---

### 3. Finnhub API (2 minutes) - RECOMMENDED

**Why:** Insider trading data, congressional trades, institutional ownership

**Steps:**
1. Go to https://finnhub.io/register
2. Sign up with email
3. Verify email
4. Dashboard will show your API key

**Limits:** 60 requests/minute (free tier)

**Add to secrets.toml:**
```toml
FINNHUB_API_KEY = "your_finnhub_key_here"
```

---

### 4. Alpha Vantage API (2 minutes) - BACKUP DATA SOURCE

**Why:** Alternative fundamental data, backup for yfinance

**Steps:**
1. Go to https://www.alphavantage.co/support/#api-key
2. Enter email and click "GET FREE API KEY"
3. API key shown immediately (no verification needed)

**Limits:** 5 requests/minute, 500 requests/day (free tier)

**Add to secrets.toml:**
```toml
ALPHA_VANTAGE_API_KEY = "your_alpha_vantage_key"
```

---

### 5. EIA API (2 minutes) - OPTIONAL (Energy Sector)

**Why:** Oil prices, natural gas data, energy sector analysis

**Steps:**
1. Go to https://www.eia.gov/opendata/register.php
2. Fill in registration form
3. Check email for API key

**Add to secrets.toml:**
```toml
EIA_API_KEY = "your_eia_key_here"
```

---

### 6. Anthropic Claude API (5 minutes + credit card) - SKIP FOR NOW

**Why:** LLM predictions feature (not yet implemented)

**Cost:** ~$0.50-2.00 per day of usage (very cheap but requires payment)

**Steps:**
1. Go to https://console.anthropic.com/
2. Sign up
3. Add payment method
4. Get API key from dashboard

**Add to secrets.toml:**
```toml
ANTHROPIC_API_KEY = "sk-ant-api03-your_key_here"
```

**Recommendation:** Skip until LLM feature is implemented

---

## 📝 AFTER ADDING KEYS

### Test the APIs:

```bash
# Restart Streamlit to load new secrets
pkill -f streamlit
streamlit run main.py
```

### Verify APIs are working:
1. Go to Stock Dashboard
2. Enter a ticker (e.g., AAPL)
3. Check "Sentiment" tab - should show Reddit/News data (not simulated)
4. Check "Smart Money" tab - should show Finnhub insider trades

---

## 🔧 TROUBLESHOOTING

### API Key Not Working?
- Make sure there are no extra spaces in secrets.toml
- Wrap keys in quotes: `FRED_API_KEY = "abc123"`
- Restart Streamlit after adding keys
- Check API provider dashboard for usage limits

### File Format:
```toml
# Correct ✅
REDDIT_CLIENT_ID = "dQw4w9WgXcQ"

# Wrong ❌
REDDIT_CLIENT_ID = dQw4w9WgXcQ  # Missing quotes
REDDIT_CLIENT_ID = 'dQw4w9WgXcQ'  # Wrong quote type
```

---

## 📊 PRIORITY ORDER

**Do First (15 minutes total):**
1. ✅ FRED (already done)
2. Reddit API (5 min)
3. News API (2 min)
4. Finnhub (2 min)

**Result:** 90% of features unlocked

**Do Later (5 minutes):**
5. Alpha Vantage (2 min)
6. EIA (2 min)

**Result:** 95% of features unlocked

**Skip for Now:**
7. Anthropic Claude (feature not built yet)

---

## ✅ CHECKLIST

Track your progress:

- [x] FRED API ✅ (Already configured)
- [ ] Reddit API (5 min) - Core sentiment feature
- [ ] News API (2 min) - News sentiment
- [ ] Finnhub API (2 min) - Insider trades
- [ ] Alpha Vantage (2 min) - Backup data
- [ ] EIA API (2 min) - Energy data
- [ ] Test app with new keys

**Total Time:** ~15 minutes for core features

---

## 🎯 NEXT STEPS AFTER API SETUP

Once APIs are configured, we'll implement:

1. **Watchlist Feature** (3 hours)
2. **Export Functionality** (2 hours)
3. **Technical Indicators** (1 hour)
4. **Market Hours Indicator** (1 hour)
5. **Lazy Loading** (2 hours)
6. **Mobile Optimization** (3 hours)
7. **Accessibility** (4 hours)

---

**Ready? Let's start with Reddit API!** 🚀

Open https://www.reddit.com/prefs/apps in your browser and follow Step 1 above.
