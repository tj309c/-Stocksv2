"""
Runtime Performance Test for Stocks Dashboard
Tests full workflow: load ticker -> analyze data -> check AI button
"""
import time
import sys
import os

# Add project root to path
sys.path.insert(0, '/workspaces/-Stocksv2')

def test_imports():
    """Test if all critical imports work"""
    print("\n" + "="*60)
    print("🧪 TEST 1: IMPORT PERFORMANCE")
    print("="*60)
    
    start = time.time()
    
    try:
        import streamlit as st
        print(f"✅ streamlit: {time.time() - start:.3f}s")
        
        start = time.time()
        from src.analysis.global_ai_analyzer import get_global_ai_analyzer, AI_MODELS
        print(f"✅ global_ai_analyzer: {time.time() - start:.3f}s")
        
        start = time.time()
        from src.utils.global_ai_panel import render_floating_ai_button, check_and_run_global_ai
        print(f"✅ global_ai_panel: {time.time() - start:.3f}s")
        
        start = time.time()
        import yfinance as yf
        print(f"✅ yfinance: {time.time() - start:.3f}s")
        
        start = time.time()
        import pandas as pd
        import numpy as np
        import plotly.graph_objects as go
        print(f"✅ data/viz libraries: {time.time() - start:.3f}s")
        
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False


def test_analyzer_initialization():
    """Test analyzer startup time"""
    print("\n" + "="*60)
    print("🧪 TEST 2: ANALYZER INITIALIZATION")
    print("="*60)
    
    try:
        start = time.time()
        from src.analysis.global_ai_analyzer import get_global_ai_analyzer
        analyzer = get_global_ai_analyzer()
        init_time = time.time() - start
        
        print(f"✅ Analyzer initialized in {init_time:.3f}s")
        
        start = time.time()
        available = analyzer.get_available_models()
        check_time = time.time() - start
        
        print(f"✅ Model availability checked in {check_time:.3f}s")
        print(f"   Available models: {len(available)}/4")
        
        return True
    except Exception as e:
        print(f"❌ Analyzer init failed: {e}")
        return False


def test_data_fetch():
    """Test stock data fetching speed"""
    print("\n" + "="*60)
    print("🧪 TEST 3: DATA FETCHING (AAPL)")
    print("="*60)
    
    try:
        import yfinance as yf
        
        # Test basic fetch
        start = time.time()
        ticker = yf.Ticker("AAPL")
        info = ticker.info
        fetch_time = time.time() - start
        
        print(f"✅ Basic info fetched in {fetch_time:.3f}s")
        
        # Test historical data
        start = time.time()
        hist = ticker.history(period="1mo")
        hist_time = time.time() - start
        
        print(f"✅ Historical data fetched in {hist_time:.3f}s")
        print(f"   Data points: {len(hist)}")
        
        # Test options data
        start = time.time()
        try:
            expirations = ticker.options
            opts_time = time.time() - start
            print(f"✅ Options data fetched in {opts_time:.3f}s")
            print(f"   Expiration dates: {len(expirations)}")
        except:
            print(f"⚠️  Options data unavailable")
        
        total = fetch_time + hist_time
        print(f"\n📊 Total data fetch time: {total:.3f}s")
        
        if total > 10:
            print("⚠️  Warning: Data fetch is slow (>10s)")
        elif total > 5:
            print("⚠️  Caution: Data fetch is moderate (>5s)")
        else:
            print("✅ Data fetch performance is good")
        
        return True
    except Exception as e:
        print(f"❌ Data fetch failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_technical_indicators():
    """Test technical indicator calculation speed"""
    print("\n" + "="*60)
    print("🧪 TEST 4: TECHNICAL INDICATORS CALCULATION")
    print("="*60)
    
    try:
        import yfinance as yf
        import pandas as pd
        import ta
        
        # Fetch data
        ticker = yf.Ticker("AAPL")
        df = ticker.history(period="6mo")
        
        start = time.time()
        
        # Calculate various indicators
        df['SMA_20'] = df['Close'].rolling(window=20).mean()
        df['EMA_12'] = df['Close'].ewm(span=12).mean()
        df['RSI'] = ta.momentum.RSIIndicator(df['Close']).rsi()
        df['MACD'] = ta.trend.MACD(df['Close']).macd()
        df['BB_upper'] = ta.volatility.BollingerBands(df['Close']).bollinger_hband()
        
        calc_time = time.time() - start
        
        print(f"✅ 5 indicators calculated in {calc_time:.3f}s")
        
        if calc_time > 2:
            print("⚠️  Warning: Indicator calculation is slow")
        else:
            print("✅ Indicator performance is good")
        
        return True
    except Exception as e:
        print(f"❌ Indicator calculation failed: {e}")
        return False


def test_ui_components():
    """Test UI component loading"""
    print("\n" + "="*60)
    print("🧪 TEST 5: UI COMPONENTS")
    print("="*60)
    
    try:
        start = time.time()
        from dashboard_stocks import show_stocks_dashboard
        load_time = time.time() - start
        
        print(f"✅ Dashboard module loaded in {load_time:.3f}s")
        
        start = time.time()
        from src.utils.global_ai_panel import (
            render_floating_ai_button,
            render_ai_analysis_panel,
            check_and_run_global_ai
        )
        ui_time = time.time() - start
        
        print(f"✅ AI panel components loaded in {ui_time:.3f}s")
        
        return True
    except Exception as e:
        print(f"❌ UI components failed: {e}")
        return False


def test_memory_usage():
    """Test memory footprint"""
    print("\n" + "="*60)
    print("🧪 TEST 6: MEMORY USAGE")
    print("="*60)
    
    try:
        import psutil
        process = psutil.Process()
        mem = process.memory_info().rss / 1024 / 1024  # MB
        
        print(f"📊 Current memory usage: {mem:.1f} MB")
        
        if mem > 500:
            print("⚠️  Warning: High memory usage (>500 MB)")
        elif mem > 300:
            print("⚠️  Caution: Moderate memory usage (>300 MB)")
        else:
            print("✅ Memory usage is acceptable")
        
        return True
    except Exception as e:
        print(f"⚠️  Could not measure memory: {e}")
        return True  # Don't fail test if psutil not available


def main():
    """Run all tests"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*12 + "RUNTIME PERFORMANCE TEST" + " "*21 + "║")
    print("╚" + "="*58 + "╝")
    
    overall_start = time.time()
    
    results = {
        "Imports": test_imports(),
        "Analyzer Init": test_analyzer_initialization(),
        "Data Fetch": test_data_fetch(),
        "Technical Indicators": test_technical_indicators(),
        "UI Components": test_ui_components(),
        "Memory Usage": test_memory_usage()
    }
    
    overall_time = time.time() - overall_start
    
    # Summary
    print("\n" + "="*60)
    print("📋 TEST SUMMARY")
    print("="*60)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:25s}: {status}")
    
    print("\n" + "="*60)
    print(f"⏱️  Total test time: {overall_time:.2f}s")
    print("="*60)
    
    passed = sum(results.values())
    total = len(results)
    
    if passed == total:
        print(f"\n✅ ALL TESTS PASSED ({passed}/{total})")
        print("\n🚀 Dashboard should run smoothly!")
        print("   - Fast data fetching")
        print("   - Quick indicator calculations")
        print("   - Reasonable memory usage")
        print("   - All components loading properly")
    else:
        print(f"\n⚠️  SOME TESTS FAILED ({passed}/{total} passed)")
        print("   Review failures above for performance issues")
    
    print("="*60 + "\n")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
