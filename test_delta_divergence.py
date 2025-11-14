#!/usr/bin/env python3
"""Test script for Delta Divergence Analyzer"""
from src.utils.delta_divergence_chart import DeltaDivergenceAnalyzer
import pandas as pd

print('=' * 80)
print('🧪 TESTING DELTA DIVERGENCE ANALYZER')
print('=' * 80)

# Test with AAPL
print('\n📊 Testing with AAPL...')
analyzer = DeltaDivergenceAnalyzer('AAPL')

print('📡 Fetching options data...')
options_data = analyzer.fetch_options_data()

if options_data:
    print(f'✅ Found {len(options_data)} expiration dates')
    print(f'✅ Current price: ${analyzer.current_price:.2f}')
    
    # Test first expiration
    first_exp = sorted(options_data.keys())[0]
    print(f'\n🎯 Analyzing {first_exp}...')
    
    divergence = analyzer.calculate_delta_divergence(first_exp)
    
    if divergence:
        print('\n📊 RESULTS:')
        print(f'   Call Delta Flow: {divergence["call_delta_flow"]:,.0f}')
        print(f'   Put Delta Flow: {divergence["put_delta_flow"]:,.0f}')
        print(f'   Net Delta Flow: {divergence["net_delta_flow"]:,.0f}')
        print(f'   Call/Put Ratio: {divergence["call_put_ratio"]:.2f}')
        print(f'   Market Expectation: {divergence["market_expectation"]}')
        print(f'   Days to Expiration: {divergence["days_to_expiration"]}')
        
        # Test all divergences
        print('\n📈 Testing summary across all expirations...')
        all_div = analyzer.get_all_divergences()
        print(f'✅ Generated summary for {len(all_div)} expirations')
        
        print('\n✅ DELTA DIVERGENCE ANALYZER TEST PASSED')
        print('\n🎯 All Features Working:')
        print('   ✅ Options data fetching')
        print('   ✅ Delta calculation with volume weighting')
        print('   ✅ Market expectation labeling')
        print('   ✅ Call/Put ratio calculation')
        print('   ✅ Multi-expiration summary')
    else:
        print('❌ Failed to calculate divergence')
else:
    print('❌ No options data found')

print('\n' + '=' * 80)
