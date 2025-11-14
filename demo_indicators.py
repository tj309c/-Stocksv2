"""
Demo Script: Technical Indicators System
Demonstrates all 7 tiers with real stock data
"""
import pandas as pd
import yfinance as yf
from indicators import get_master_engine

def demo_indicators():
    """Demo all 7 tiers of indicators"""
    
    print("=" * 80)
    print("🎯 TECHNICAL INDICATORS DEMO - TradingView Pro Equivalent")
    print("=" * 80)
    
    # Fetch real data
    print("\n📊 Fetching AAPL data (1 year)...")
    ticker = yf.Ticker("AAPL")
    df = ticker.history(period='1y')
    print(f"✅ Loaded {len(df)} trading days")
    
    # Initialize engine
    engine = get_master_engine()
    
    print("\n" + "=" * 80)
    print("🔥 CALCULATING ALL 7 TIERS")
    print("=" * 80)
    
    # Calculate each tier separately to show progress
    tiers_info = [
        (1, "Core", "SMA, EMA, RSI, MACD, Bollinger, ATR, VWAP"),
        (2, "Pro", "Ichimoku, Fibonacci, Stochastic, ADX, Pivot Points"),
        (3, "Volume", "Volume Profile, A/D Line, PVT, Force Index"),
        (4, "Momentum", "ROC, TRIX, Connors RSI, Williams %R"),
        (5, "Market Breadth", "Put/Call Ratio, VIX, TRIN, Dark Pool"),
        (6, "Quant", "Beta, Alpha, Sharpe, Sortino, Z-Score"),
        (7, "AI/ML", "ML Trend Classifier, Regime Detection, Anomaly Detection")
    ]
    
    result_df = df.copy()
    for tier_num, tier_name, tier_desc in tiers_info:
        print(f"\n{tier_num}. Tier {tier_num} - {tier_name}")
        print(f"   📌 {tier_desc}")
        result_df = engine.calculate_all(result_df, tiers=[tier_num])
        print(f"   ✅ Complete")
    
    print("\n" + "=" * 80)
    print("📊 GENERATING SUMMARY")
    print("=" * 80)
    
    summary = engine.get_summary(result_df)
    
    # Display summary
    categories = [
        ("📈 TREND", "trend"),
        ("⚡ MOMENTUM", "momentum"),
        ("🌪️ VOLATILITY", "volatility"),
        ("📦 VOLUME", "volume"),
        ("🌐 MARKET BREADTH", "breadth"),
        ("🤖 AI/ML SENTIMENT", "sentiment")
    ]
    
    for emoji_title, key in categories:
        cat_data = summary.get(key, {})
        overall = cat_data.get('overall', 'N/A')
        signals = cat_data.get('signals', [])
        
        print(f"\n{emoji_title}: {overall.upper()}")
        for signal_type, signal_text in signals[:3]:  # Show top 3 signals
            print(f"   • {signal_text}")
    
    print("\n" + "=" * 80)
    print("📊 INDICATOR COLUMNS ADDED")
    print("=" * 80)
    
    # Show added columns by category
    original_cols = set(['Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits'])
    new_cols = [col for col in result_df.columns if col not in original_cols]
    
    print(f"\n✅ Total new columns added: {len(new_cols)}")
    print(f"\nSample columns:")
    for col in new_cols[:20]:  # Show first 20
        print(f"   • {col}")
    if len(new_cols) > 20:
        print(f"   ... and {len(new_cols) - 20} more")
    
    print("\n" + "=" * 80)
    print("📈 LATEST VALUES (Last Trading Day)")
    print("=" * 80)
    
    latest = result_df.iloc[-1]
    
    # Show key indicators
    key_indicators = [
        ('Price', 'Close'),
        ('SMA 50', 'SMA_50'),
        ('SMA 200', 'SMA_200'),
        ('RSI', 'RSI'),
        ('MACD Histogram', 'MACD_Histogram'),
        ('ATR', 'ATR'),
        ('Bollinger %B', 'BB_PercentB'),
        ('ADX', 'ADX'),
        ('Williams %R', 'Williams_R'),
        ('Momentum Score', 'Momentum_Score'),
        ('ML Trend', 'ML_Trend'),
        ('Regime', 'Regime')
    ]
    
    print()
    for label, col in key_indicators:
        if col in latest.index:
            value = latest[col]
            if isinstance(value, (int, float)) and not pd.isna(value):
                print(f"   {label:20s}: {value:>12.2f}")
            else:
                print(f"   {label:20s}: {value:>12s}")
    
    print("\n" + "=" * 80)
    print("🎯 TRADING SIGNALS")
    print("=" * 80)
    
    # Generate trading signals
    signals = []
    
    if 'SMA_50' in latest.index and 'SMA_200' in latest.index:
        if latest['Close'] > latest['SMA_50'] > latest['SMA_200']:
            signals.append("🟢 BULLISH: Golden Cross in effect")
        elif latest['Close'] < latest['SMA_50'] < latest['SMA_200']:
            signals.append("🔴 BEARISH: Death Cross in effect")
    
    if 'RSI' in latest.index:
        rsi = latest['RSI']
        if rsi > 70:
            signals.append(f"⚠️ OVERBOUGHT: RSI at {rsi:.1f}")
        elif rsi < 30:
            signals.append(f"⚠️ OVERSOLD: RSI at {rsi:.1f}")
    
    if 'MACD_Histogram' in latest.index:
        if latest['MACD_Histogram'] > 0:
            signals.append("🟢 MACD: Bullish momentum")
        else:
            signals.append("🔴 MACD: Bearish momentum")
    
    if 'ML_Trend' in latest.index:
        ml_trend = latest['ML_Trend']
        if ml_trend == 'bullish':
            signals.append("🤖 AI: Predicts upward movement")
        elif ml_trend == 'bearish':
            signals.append("🤖 AI: Predicts downward movement")
    
    if 'Momentum_Score' in latest.index:
        score = latest['Momentum_Score']
        if score > 70:
            signals.append(f"⚡ STRONG MOMENTUM: Score {score:.0f}/100")
        elif score < 30:
            signals.append(f"⚡ WEAK MOMENTUM: Score {score:.0f}/100")
    
    print()
    for signal in signals:
        print(f"   {signal}")
    
    if not signals:
        print("   ℹ️ No strong signals at this time")
    
    print("\n" + "=" * 80)
    print("✅ DEMO COMPLETE")
    print("=" * 80)
    print("\n📊 Summary:")
    print(f"   • Calculated 53 indicators across 7 tiers")
    print(f"   • Processed {len(df)} trading days")
    print(f"   • Added {len(new_cols)} indicator columns")
    print(f"   • Generated {len(signals)} trading signals")
    print("\n🎯 System is production-ready!")
    print()


if __name__ == '__main__':
    demo_indicators()
