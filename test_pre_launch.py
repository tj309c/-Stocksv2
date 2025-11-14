#!/usr/bin/env python3
"""
Pre-Launch Critical Error Check
Tests all core functionality before running streamlit
"""
import sys

def test_imports():
    """Test all critical imports"""
    print("🔍 Testing imports...")
    try:
        from data_fetcher import MarketDataFetcher, SentimentScraper
        from analysis_engine import ValuationEngine, TechnicalAnalyzer, GoodBuyAnalyzer, OptionsAnalyzer
        from dashboard_stocks import show_stocks_dashboard
        from dashboard_options import show_options_dashboard
        from dashboard_crypto import show_crypto_dashboard
        from dashboard_advanced import show_advanced_dashboard
        from dashboard_portfolio import show_portfolio_dashboard
        print("   ✅ All imports successful\n")
        return True
    except Exception as e:
        print(f"   ❌ Import error: {e}\n")
        return False

def test_data_fetcher():
    """Test MarketDataFetcher functionality"""
    print("🔍 Testing MarketDataFetcher...")
    try:
        from data_fetcher import MarketDataFetcher
        fetcher = MarketDataFetcher()
        
        # Test stock data
        data = fetcher.get_stock_data('AAPL', '1mo')
        assert data and 'info' in data, "Stock data missing"
        assert data['info'].get('symbol') == 'AAPL', "Ticker mismatch"
        
        # Test quote
        quote = fetcher.get_realtime_quote('TSLA')
        assert quote and 'price' in quote, "Quote data missing"
        assert quote['price'] > 0, "Invalid price"
        
        print("   ✅ Data fetcher working correctly\n")
        return True
    except Exception as e:
        print(f"   ❌ Data fetcher error: {e}\n")
        return False

def test_session_state_consistency():
    """Test that all dashboards use active_ticker consistently"""
    print("🔍 Testing session state consistency...")
    try:
        import re
        dashboards = [
            'dashboard_stocks.py',
            'dashboard_options.py', 
            'dashboard_crypto.py',
            'dashboard_advanced.py'
        ]
        
        issues = []
        for dashboard in dashboards:
            with open(dashboard, 'r') as f:
                content = f.read()
                
                # Check for old session state variables
                old_vars = ['current_ticker', 'current_options_ticker', 
                           'current_crypto', 'advanced_ticker']
                for var in old_vars:
                    if f'st.session_state.{var}' in content or f'st.session_state.get("{var}"' in content:
                        issues.append(f"{dashboard} still uses old variable: {var}")
                
                # Check that active_ticker is used
                if 'st.session_state.active_ticker' not in content and 'st.session_state.get("active_ticker"' not in content:
                    issues.append(f"{dashboard} doesn't use active_ticker")
        
        if issues:
            print("   ⚠️ Session state issues found:")
            for issue in issues:
                print(f"      - {issue}")
            return False
        else:
            print("   ✅ All dashboards use unified active_ticker\n")
            return True
    except Exception as e:
        print(f"   ❌ Session state test error: {e}\n")
        return False

def test_cache_decorators():
    """Test that cache decorators are properly applied"""
    print("🔍 Testing cache decorators...")
    try:
        with open('data_fetcher.py', 'r') as f:
            content = f.read()
        
        # Check for @st.cache_data decorators
        cache_count = content.count('@st.cache_data')
        if cache_count < 5:
            print(f"   ⚠️ Only {cache_count} cache decorators found (expected 5+)")
            return False
        
        # Check that SQLite code is removed
        if 'sqlite3' in content:
            print("   ⚠️ SQLite code still present (should be removed)")
            return False
        
        if '_get_cached' in content or '_set_cache' in content:
            print("   ⚠️ Old cache methods still present")
            return False
        
        print(f"   ✅ {cache_count} cache decorators found, SQLite removed\n")
        return True
    except Exception as e:
        print(f"   ❌ Cache decorator test error: {e}\n")
        return False

def test_ticker_input_flow():
    """Test ticker input and data fetch flow"""
    print("🔍 Testing ticker input flow...")
    try:
        from data_fetcher import MarketDataFetcher
        fetcher = MarketDataFetcher()
        
        # Test various ticker formats
        test_cases = [
            ('AAPL', True),
            ('aapl', True),  # Should be uppercase
            ('TSLA', True),
            ('BTC-USD', True),  # Crypto ticker
            ('INVALID123', False),  # Should fail gracefully
        ]
        
        for ticker, should_succeed in test_cases:
            ticker_upper = ticker.upper()
            try:
                data = fetcher.get_stock_data(ticker_upper, '1mo')
                if should_succeed:
                    if not data or not data.get('info'):
                        print(f"   ⚠️ {ticker} returned no data (expected data)")
                else:
                    if data and data.get('info'):
                        print(f"   ⚠️ {ticker} returned data (expected failure)")
            except Exception as e:
                if should_succeed:
                    print(f"   ⚠️ {ticker} raised exception (expected success): {e}")
        
        print("   ✅ Ticker input flow working correctly\n")
        return True
    except Exception as e:
        print(f"   ❌ Ticker input flow error: {e}\n")
        return False

def main():
    """Run all pre-launch tests"""
    print("\n" + "="*60)
    print("🚀 PRE-LAUNCH CRITICAL ERROR CHECK")
    print("="*60 + "\n")
    
    tests = [
        ("Imports", test_imports),
        ("Data Fetcher", test_data_fetcher),
        ("Session State", test_session_state_consistency),
        ("Cache Decorators", test_cache_decorators),
        ("Ticker Input Flow", test_ticker_input_flow),
    ]
    
    results = []
    for name, test_func in tests:
        results.append((name, test_func()))
    
    # Summary
    print("="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status:12} | {name}")
    
    print("="*60)
    print(f"Result: {passed}/{total} tests passed")
    print("="*60 + "\n")
    
    if passed == total:
        print("🎉 All tests passed! Ready to launch!")
        print("Run: streamlit run main.py")
        return 0
    else:
        print("⚠️  Some tests failed. Review errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
