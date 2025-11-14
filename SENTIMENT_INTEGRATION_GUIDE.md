# 🚀 Quick Start Guide - Sentiment Integration

## What's New?
Your Stock_Scrapper tool is now integrated into the main dashboard! Real sentiment data from Reddit and news sources now powers the "Ape Sentiment" tab.

## ✅ Completed Integration

### Files Created/Modified:
1. **src/utils/sentiment_scraper.py** (NEW)
   - Wrapper for Stock_Scrapper tools
   - Automatic fallback (enhanced → basic scraper)
   - Streamlit caching (1-hour TTL)
   - Display utilities for sentiment metrics

2. **dashboard_stocks.py** (UPDATED)
   - Real-time sentiment scraping in "Ape Sentiment" tab
   - Live data from Reddit (7 subreddits) + NewsAPI + Yahoo Finance
   - Sentiment breakdown charts
   - Recent posts display
   - 7-day sentiment trends
   - Refresh button for manual updates

3. **src/config/settings.py** (UPDATED)
   - Added Reddit API configuration
   - Added NewsAPI configuration
   - Environment variable support

4. **requirements.txt** (UPDATED)
   - Added textblob>=0.19.0
   - Added nltk>=3.9

5. **README.md** (UPDATED)
   - Complete API setup instructions
   - Reddit API key guide
   - NewsAPI key guide
   - Sentiment scraper documentation

## 📊 Features

### Automatic Scraper Selection
- **Enhanced mode**: Uses PRAW (Reddit API) if keys configured
- **Basic mode**: Falls back to JSON API (no keys needed)
- **Smart caching**: 1-hour TTL to respect rate limits

### Data Sources
✅ Reddit (7 subreddits):
  - r/wallstreetbets
  - r/stocks
  - r/investing
  - r/StockMarket
  - r/options
  - r/Daytrading
  - r/SecurityAnalysis

✅ NewsAPI (optional):
  - Financial news articles
  - Last 30 days of coverage
  - 100 requests/day free tier

✅ Yahoo Finance:
  - RSS feed integration
  - Real-time news updates
  - No API key required

### Sentiment Metrics
- **Total Mentions**: Count of all posts/articles
- **Positive/Negative/Neutral**: Percentage breakdown
- **Polarity Score**: -1 (bearish) to +1 (bullish)
- **Subjectivity Score**: 0 (objective) to 1 (opinionated)
- **Source Distribution**: Bar chart of mention sources
- **7-Day Trends**: Historical sentiment timeline
- **Recent Posts**: Last 10 social media posts with links

## 🔧 Setup (5 Minutes)

### Step 1: Install Dependencies
```bash
pip install textblob nltk
python -c "import nltk; nltk.download('brown'); nltk.download('punkt'); nltk.download('punkt_tab')"
```

### Step 2: Test Basic Mode (No API Keys)
```bash
python test_sentiment_integration.py
```
You should see:
- ✅ BASIC: PASSED (uses Reddit JSON API)
- ✅ ENHANCED: PASSED (initialized)
- ✅ WRAPPER: PASSED (20+ mentions from Yahoo Finance)

### Step 3: Configure Reddit API (Optional but Recommended)

1. **Get Reddit API Keys** (Free, takes 2 minutes):
   - Go to https://www.reddit.com/prefs/apps
   - Click "Create App" or "Create Another App"
   - Fill in:
     - **Name**: StocksV2App
     - **Type**: Script
     - **Redirect URI**: http://localhost:8501
   - Click "Create app"
   - Copy:
     - **Client ID**: string under app name (looks like `abc123xyz`)
     - **Secret**: random string (click to reveal)

2. **Create Streamlit Secrets File**:
   ```bash
   mkdir -p .streamlit
   nano .streamlit/secrets.toml
   ```

3. **Add API Keys**:
   ```toml
   REDDIT_CLIENT_ID = "your_client_id_here"
   REDDIT_CLIENT_SECRET = "your_client_secret_here"
   REDDIT_USER_AGENT = "StocksV2App/1.0"
   
   # Optional - NewsAPI (free 100 requests/day)
   NEWS_API_KEY = "your_newsapi_key_here"
   ```

4. **Save and Test**:
   ```bash
   python test_sentiment_integration.py
   ```
   Now you should see real Reddit data!

### Step 4: Run Dashboard
```bash
streamlit run main.py
```

Navigate to: **Stocks Dashboard → "💬 Ape Sentiment" tab**

## 🎯 Usage

### Without API Keys (Basic Mode):
- ✅ Yahoo Finance news sentiment (20+ articles)
- ✅ Sentiment analysis with TextBlob
- ✅ Basic Reddit data from JSON API
- ⚠️ Limited to 4 subreddits, lower data quality

### With Reddit API Keys (Enhanced Mode):
- ✅ **7 subreddits** instead of 4
- ✅ **Better data quality** (authenticated access)
- ✅ **More posts** per request
- ✅ **Historical data** access
- ✅ **Reddit Premium features** if account has Premium

### With NewsAPI Key (Optional):
- ✅ Financial news from 100+ sources
- ✅ 100 requests/day (enough for 10+ tickers)
- ✅ Last 30 days of news coverage
- ✅ Article snippets and links

## 📈 Dashboard Features

### Sentiment Metrics Display:
```
Total Mentions: 47        Positive: 42.6%
Negative: 10.6%          Avg Polarity: 0.23
```

### Sentiment Breakdown Pie Chart:
- 🟢 Positive: Green
- 🔴 Negative: Red
- ⚪ Neutral: Gray

### Trending Sources Bar Chart:
Shows which sources have most mentions (Reddit, Yahoo Finance, NewsAPI)

### Recent Posts Feed:
- Last 10 posts with sentiment emoji
- Source, timestamp, and direct link
- Expandable for details

### 7-Day Sentiment Trend:
Line chart showing daily sentiment evolution

### Refresh Button:
Manual refresh to get latest data (clears 1-hour cache)

## 🧪 Testing

### Test Script Output:
```bash
$ python test_sentiment_integration.py

╔==========================================================╗
║          SENTIMENT SCRAPER INTEGRATION TEST             ║
╚==========================================================╝

✅ BASIC: PASSED
✅ ENHANCED: PASSED
✅ WRAPPER: PASSED

🎉 All tests passed! Sentiment integration is ready.
```

### What Gets Tested:
1. **Basic Scraper**: Reddit JSON API + Yahoo Finance
2. **Enhanced Scraper**: PRAW initialization + config
3. **Wrapper**: Full integration with caching and metrics

## 🔍 Troubleshooting

### "No sentiment data available"
- Check internet connection
- Verify Stock_Scrapper folder exists
- Run: `python test_sentiment_integration.py`

### "TextBlob not installed"
```bash
pip install textblob
python -c "import nltk; nltk.download('brown'); nltk.download('punkt')"
```

### "PRAW not available"
```bash
pip install praw
```

### Reddit API not working
- Verify credentials in `.streamlit/secrets.toml`
- Check client ID format (no quotes in actual ID)
- Ensure redirect URI matches: `http://localhost:8501`
- Test with: `python -c "import praw; print('PRAW OK')"`

### No Reddit data (0 posts)
- Reddit JSON API has rate limits (fallback to Yahoo Finance)
- Try with Reddit API keys for better access
- Check if ticker is actually discussed on Reddit (GME, TSLA work well)

### Cache not clearing
- Click "🔄 Refresh Data" button in dashboard
- Or restart Streamlit: `Ctrl+C` then `streamlit run main.py`

## 📚 Code References

### Get Sentiment in Code:
```python
from src.utils.sentiment_scraper import get_scraper

# Initialize scraper
scraper = get_scraper()

# Get sentiment summary
summary = scraper.get_sentiment_summary('AAPL')

# Access metrics
print(f"Total: {summary['total_mentions']}")
print(f"Positive: {summary['positive_pct']:.1f}%")
print(f"Polarity: {summary['avg_polarity']:.2f}")
```

### Display in Dashboard:
```python
from src.utils.sentiment_scraper import display_sentiment_metrics, display_recent_posts

# Show metrics
display_sentiment_metrics(summary)

# Show recent posts
display_recent_posts(summary['recent_posts'])
```

### Get Trend Data:
```python
# 7-day sentiment trend
trend_df = scraper.get_sentiment_over_time('TSLA', days=7)
print(trend_df.columns)  # ['date_only', 'positive', 'negative', 'neutral', 'avg_polarity', 'total_mentions']
```

## 🎉 What Changed?

### Before Integration:
- Simulated/placeholder sentiment data
- StockTwits API (often rate limited)
- No real Reddit scraping
- Limited news sources

### After Integration:
- ✅ Real Reddit data from 7 subreddits
- ✅ Yahoo Finance RSS feeds
- ✅ Optional NewsAPI integration
- ✅ TextBlob sentiment analysis
- ✅ 1-hour caching (respects rate limits)
- ✅ Automatic fallback (enhanced → basic)
- ✅ Live sentiment trends over time
- ✅ Recent posts with direct links
- ✅ Source distribution metrics

## 📊 Example Output

### Ticker: GME
```
Total Mentions: 47
Positive: 42.6% (20 posts)
Negative: 10.6% (5 posts)
Neutral: 46.8% (22 posts)
Avg Polarity: 0.23 (Slightly bullish 📈)
Avg Subjectivity: 0.45

Trending Sources:
  - Reddit (wallstreetbets): 15 mentions
  - Yahoo Finance: 20 mentions
  - Reddit (stocks): 8 mentions
  - NewsAPI: 4 mentions
```

### Recent Posts:
1. 🟢 "GME to the moon! Diamond hands!" (wallstreetbets, 2h ago)
2. ⚪ "GameStop reports Q3 earnings" (Yahoo Finance, 4h ago)
3. 🔴 "GameStop faces challenges" (NewsAPI, 6h ago)

## 🚀 Next Steps

1. **Test with popular tickers**:
   - GME, TSLA, AAPL (high Reddit activity)
   - META, NVDA, AMD (tech stocks)
   - SPY, QQQ (index tracking)

2. **Monitor sentiment shifts**:
   - Watch 7-day trend charts
   - Compare polarity changes
   - Track volume spikes

3. **Correlate with price**:
   - Compare sentiment to price movements
   - Identify sentiment-driven rallies
   - Spot potential reversals

4. **Optimize API usage**:
   - 1-hour cache reduces API calls
   - Manual refresh only when needed
   - Free tier limits respected

## 📧 Support

If you encounter issues:
1. Check test output: `python test_sentiment_integration.py`
2. Verify API keys in `.streamlit/secrets.toml`
3. Check logs in `logs/` directory
4. Reddit API help: https://www.reddit.com/prefs/apps
5. NewsAPI help: https://newsapi.org/docs

---

**🎉 Congratulations!** Your Stock_Scrapper tool is now fully integrated with accurate, real-time sentiment tracking across all dashboards!
