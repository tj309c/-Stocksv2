"""
Quick test script to verify sentiment scraper integration
"""

import sys
from pathlib import Path

# Add Stock_Scrapper to path
STOCK_SCRAPPER_PATH = Path(__file__).parent / "Stock_Scrapper"
sys.path.insert(0, str(STOCK_SCRAPPER_PATH))

# Add src to path
SRC_PATH = Path(__file__).parent / "src"
sys.path.insert(0, str(SRC_PATH))

def test_basic_scraper():
    """Test basic scraper without API keys"""
    print("=" * 60)
    print("Testing Basic Scraper (No API Keys)")
    print("=" * 60)
    
    try:
        from stock_scraper import StockDataScraper
        
        ticker = "AAPL"
        print(f"\nInitializing scraper for ${ticker}...")
        scraper = StockDataScraper(ticker)
        
        print("\nScraping Reddit...")
        reddit_data = scraper.scrape_reddit()
        print(f"✅ Found {len(reddit_data)} Reddit posts")
        
        if reddit_data:
            print("\nSample post:")
            post = reddit_data[0]
            print(f"  Source: {post['source']}")
            print(f"  Title: {post['title'][:60]}...")
            print(f"  Sentiment: {post['sentiment']}")
            print(f"  Date: {post['date']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_enhanced_scraper():
    """Test enhanced scraper with API keys (if available)"""
    print("\n" + "=" * 60)
    print("Testing Enhanced Scraper (With API Keys)")
    print("=" * 60)
    
    try:
        from stock_scraper_enhanced import EnhancedStockDataScraper as StockDataScraper
        
        ticker = "TSLA"
        print(f"\nInitializing enhanced scraper for ${ticker}...")
        
        # Note: This will fail without API keys, which is expected
        config = {
            'reddit_client_id': '',
            'reddit_client_secret': '',
            'reddit_user_agent': 'StocksV2App/1.0'
        }
        
        scraper = StockDataScraper(ticker, config=config)
        print("✅ Enhanced scraper initialized")
        print("⚠️  Note: Reddit API features require valid credentials")
        
        return True
        
    except Exception as e:
        print(f"⚠️  Enhanced scraper not available: {e}")
        return False


def test_sentiment_wrapper():
    """Test the sentiment scraper wrapper"""
    print("\n" + "=" * 60)
    print("Testing Sentiment Scraper Wrapper")
    print("=" * 60)
    
    try:
        from utils.sentiment_scraper import SentimentScraper
        
        print("\nInitializing sentiment scraper wrapper...")
        scraper = SentimentScraper()
        
        ticker = "GME"
        print(f"\nGetting sentiment summary for ${ticker}...")
        summary = scraper.get_sentiment_summary(ticker)
        
        if summary['data_available']:
            print("\n✅ Sentiment Data Retrieved:")
            print(f"  Total Mentions: {summary['total_mentions']}")
            print(f"  Positive: {summary['positive_pct']:.1f}%")
            print(f"  Negative: {summary['negative_pct']:.1f}%")
            print(f"  Neutral: {summary['neutral_pct']:.1f}%")
            print(f"  Avg Polarity: {summary['avg_polarity']:.2f}")
            print(f"  Scraper Type: {summary['scraper_type']}")
            
            if summary['trending_sources']:
                print("\n  Trending Sources:")
                for source, count in list(summary['trending_sources'].items())[:3]:
                    print(f"    - {source}: {count} mentions")
            
            if summary['recent_posts']:
                print(f"\n  Recent Posts: {len(summary['recent_posts'])} found")
            
            return True
        else:
            print("⚠️  No sentiment data available")
            return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "SENTIMENT SCRAPER INTEGRATION TEST" + " " * 13 + "║")
    print("╚" + "=" * 58 + "╝")
    
    results = {}
    
    # Test basic scraper
    results['basic'] = test_basic_scraper()
    
    # Test enhanced scraper
    results['enhanced'] = test_enhanced_scraper()
    
    # Test wrapper
    results['wrapper'] = test_sentiment_wrapper()
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name.upper():<15}: {status}")
    
    total_passed = sum(results.values())
    total_tests = len(results)
    
    print(f"\nTotal: {total_passed}/{total_tests} tests passed")
    
    if all(results.values()):
        print("\n🎉 All tests passed! Sentiment integration is ready.")
    else:
        print("\n⚠️  Some tests failed. Check configuration and dependencies.")
    
    print("\n" + "=" * 60)
    print("NEXT STEPS:")
    print("=" * 60)
    print("1. Add Reddit API credentials to .env or streamlit secrets:")
    print("   - REDDIT_CLIENT_ID=your_client_id")
    print("   - REDDIT_CLIENT_SECRET=your_client_secret")
    print("   - REDDIT_USER_AGENT=StocksV2App/1.0")
    print("\n2. (Optional) Add NewsAPI key for news sentiment:")
    print("   - NEWS_API_KEY=your_api_key")
    print("\n3. Get free API keys:")
    print("   - Reddit: https://www.reddit.com/prefs/apps")
    print("   - NewsAPI: https://newsapi.org/")
    print("\n4. Test dashboard: streamlit run main.py")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
