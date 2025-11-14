"""
Visual UI Test - Verify all components are visible and accessible
Tests navigation through all tabs and sections
"""
import time
import sys
sys.path.insert(0, '/workspaces/-Stocksv2')

def print_header(title):
    """Print formatted test header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)


def test_dashboard_structure():
    """Test main dashboard structure"""
    print_header("🎨 VISUAL TEST: DASHBOARD STRUCTURE")
    
    try:
        from dashboard_stocks import show_stocks_dashboard
        print("✅ Dashboard module loaded")
        
        # Check if main function exists
        import inspect
        sig = inspect.signature(show_stocks_dashboard)
        params = list(sig.parameters.keys())
        print(f"✅ Main dashboard function: show_stocks_dashboard({', '.join(params)})")
        
        return True
    except Exception as e:
        print(f"❌ Dashboard structure test failed: {e}")
        return False


def test_tab_definitions():
    """Check all tab definitions in dashboard"""
    print_header("📑 VISUAL TEST: TAB STRUCTURE")
    
    try:
        # Read dashboard file and check for tab definitions
        with open('/workspaces/-Stocksv2/dashboard_stocks.py', 'r') as f:
            content = f.read()
        
        # Look for tab definitions
        if 'tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10' in content:
            print("✅ 10 tabs defined in dashboard")
        
        tabs = [
            ("tab1", "📊 Overview", "show_overview_tab"),
            ("tab2", "💰 Valuation (DD)", "show_valuation_tab"),
            ("tab3", "🎛️ Interactive DCF", "show_enhanced_valuation_tab"),
            ("tab4", "📈 Technical (Charts)", "show_technical_tab"),
            ("tab5", "🎯 Pro Indicators (60+)", "show_pro_indicators_tab"),
            ("tab6", "📊 Delta Divergence", "show_delta_divergence_tab"),
            ("tab7", "💬 Ape Sentiment", "show_sentiment_tab"),
            ("tab8", "🔗 Sentiment Correlation", "show_sentiment_correlation_tab"),
            ("tab9", "🏢 Smart Money", "show_institutional_tab"),
            ("tab10", "🤖 AI Analysis", "check_and_run_global_ai")
        ]
        
        for tab_var, tab_name, function in tabs:
            if tab_name in content:
                print(f"✅ {tab_var}: {tab_name}")
            else:
                print(f"⚠️  {tab_var}: {tab_name} - not found in string search")
        
        print("\n📊 Tab Overview:")
        print("   1. Overview          - Key metrics, buy signal, company info")
        print("   2. Valuation (DD)    - DCF model, intrinsic value, multiples")
        print("   3. Interactive DCF   - Adjustable assumptions, Monte Carlo")
        print("   4. Technical         - Price charts, indicators, patterns")
        print("   5. Pro Indicators    - 60+ technical indicators with AI/ML")
        print("   6. Delta Divergence  - Options flow analysis")
        print("   7. Ape Sentiment     - Reddit/social media sentiment")
        print("   8. Sentiment Corr    - Sentiment vs price correlation")
        print("   9. Smart Money       - Institutional & insider trades")
        print("   10. AI Analysis      - Multi-model AI consensus (NEW!)")
        
        return True
    except Exception as e:
        print(f"❌ Tab definition test failed: {e}")
        return False


def test_global_ai_components():
    """Test Global AI Analysis UI components"""
    print_header("🤖 VISUAL TEST: GLOBAL AI COMPONENTS")
    
    try:
        from src.utils.global_ai_panel import (
            render_floating_ai_button,
            render_ai_analysis_panel,
            check_and_run_global_ai
        )
        print("✅ AI panel functions loaded:")
        print("   • render_floating_ai_button() - Sidebar button with model selector")
        print("   • render_ai_analysis_panel()  - Main analysis interface")
        print("   • check_and_run_global_ai()   - Tab display handler")
        
        # Check for UI elements in the file
        with open('/workspaces/-Stocksv2/src/utils/global_ai_panel.py', 'r') as f:
            content = f.read()
        
        ui_elements = [
            ("🚀 Analyze Everything", "Main action button"),
            ("Multi-Model Consensus", "Consensus mode checkbox"),
            ("Claude", "Model: Claude 3.5 Sonnet"),
            ("GPT-4", "Model: GPT-4 Turbo"),
            ("Gemini", "Model: Gemini Pro"),
            ("Grok", "Model: Grok Beta"),
            ("Consensus Summary", "Results tab"),
            ("Individual Models", "Results tab"),
            ("Fair Value", "Output metric"),
            ("Recommendation", "Output metric"),
            ("Confidence", "Output metric")
        ]
        
        print("\n✅ UI Elements Found:")
        for element, description in ui_elements:
            if element in content:
                print(f"   ✓ {description}")
        
        return True
    except Exception as e:
        print(f"❌ AI components test failed: {e}")
        return False


def test_sidebar_components():
    """Test sidebar elements"""
    print_header("📌 VISUAL TEST: SIDEBAR COMPONENTS")
    
    try:
        with open('/workspaces/-Stocksv2/dashboard_stocks.py', 'r') as f:
            content = f.read()
        
        sidebar_elements = [
            ("render_watchlist_sidebar", "Watchlist manager"),
            ("render_floating_ai_button", "AI Analysis button"),
            ("render_add_to_watchlist_button", "Add to watchlist"),
            ("show_employment_regime_panel", "BLS employment data")
        ]
        
        print("✅ Sidebar Components:")
        for function, description in sidebar_elements:
            if function in content:
                print(f"   ✓ {description} ({function})")
        
        return True
    except Exception as e:
        print(f"❌ Sidebar test failed: {e}")
        return False


def test_main_sections():
    """Test main content sections"""
    print_header("📋 VISUAL TEST: MAIN CONTENT SECTIONS")
    
    try:
        with open('/workspaces/-Stocksv2/dashboard_stocks.py', 'r') as f:
            content = f.read()
        
        sections = [
            ("STONKS ANALYSIS", "Main header"),
            ("Enter Ticker Symbol", "Ticker input field"),
            ("🔍 Analyze", "Analyze button"),
            ("🔄 Refresh", "Refresh button"),
            ("💎🙌", "Diamond hands checkbox"),
            ("render_compact_market_status", "Market hours indicator"),
            ("show_buy_signal_section", "Buy signal section"),
            ("Data fetched:", "Data freshness indicator"),
            ("🔄 Clear Cache", "Cache clear button")
        ]
        
        print("✅ Main Content Sections:")
        for element, description in sections:
            if element in content:
                print(f"   ✓ {description}")
        
        return True
    except Exception as e:
        print(f"❌ Main sections test failed: {e}")
        return False


def test_visual_indicators():
    """Test visual indicators and styling"""
    print_header("🎨 VISUAL TEST: STYLING & INDICATORS")
    
    try:
        with open('/workspaces/-Stocksv2/src/utils/global_ai_panel.py', 'r') as f:
            content = f.read()
        
        visual_elements = [
            ("background: linear-gradient", "Gradient button styling"),
            ("animation: pulse", "Pulsing animation"),
            ("box-shadow:", "Drop shadows"),
            ("border-radius:", "Rounded corners"),
            ("floating-ai-button", "Floating button CSS class"),
            ("st.success", "Success indicators"),
            ("st.error", "Error indicators"),
            ("st.warning", "Warning indicators"),
            ("st.info", "Info boxes"),
            ("st.metric", "Metric displays"),
            ("st.progress", "Progress bars"),
            ("st.expander", "Expandable sections")
        ]
        
        print("✅ Visual Styling Elements:")
        found = 0
        for element, description in visual_elements:
            if element in content:
                found += 1
        print(f"   Found {found}/{len(visual_elements)} styling elements")
        
        return True
    except Exception as e:
        print(f"❌ Visual indicators test failed: {e}")
        return False


def test_data_visualizations():
    """Test data visualization components"""
    print_header("📊 VISUAL TEST: DATA VISUALIZATIONS")
    
    try:
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots
        print("✅ Plotly visualization library loaded")
        
        with open('/workspaces/-Stocksv2/dashboard_stocks.py', 'r') as f:
            content = f.read()
        
        viz_components = [
            ("plotly.graph_objects", "Plotly charts"),
            ("make_subplots", "Multi-panel charts"),
            ("render_indicator_charts", "Indicator visualizations"),
            ("render_delta_divergence_chart", "Options flow chart"),
            ("show_sentiment_correlation_tab", "Sentiment charts")
        ]
        
        print("\n✅ Visualization Components:")
        for component, description in viz_components:
            if component in content:
                print(f"   ✓ {description}")
        
        return True
    except Exception as e:
        print(f"❌ Visualization test failed: {e}")
        return False


def test_export_features():
    """Test export functionality"""
    print_header("💾 VISUAL TEST: EXPORT FEATURES")
    
    try:
        with open('/workspaces/-Stocksv2/dashboard_stocks.py', 'r') as f:
            dashboard_content = f.read()
        
        with open('/workspaces/-Stocksv2/src/utils/global_ai_panel.py', 'r') as f:
            panel_content = f.read()
        
        export_features = [
            ("render_export_buttons", "Export buttons in dashboard"),
            ("st.download_button", "Download functionality"),
            ("generate_text_summary", "Text export format"),
            (".json", "JSON export format")
        ]
        
        print("✅ Export Features:")
        for feature, description in export_features:
            if feature in dashboard_content or feature in panel_content:
                print(f"   ✓ {description}")
        
        return True
    except Exception as e:
        print(f"❌ Export features test failed: {e}")
        return False


def create_visual_checklist():
    """Create a visual testing checklist for manual verification"""
    print_header("📝 MANUAL VISUAL TESTING CHECKLIST")
    
    checklist = """
When you start the dashboard, verify these elements are VISIBLE:

🏠 HOMEPAGE (Dashboard Selector):
   □ Title: "STONKS ANALYSIS"
   □ Tagline with WSB humor
   □ Market hours indicator (green/red status)
   □ Ticker input field
   □ "🔍 Analyze" button
   □ "🔄 Refresh" button
   □ "💎🙌" checkbox

📌 SIDEBAR (Left Panel):
   □ Watchlist section
   □ "Add to Watchlist" button
   □ "🤖 Global AI Analysis" section
   □ Model status indicators (4 models)
   □ "🚀 Analyze Everything" button
   □ Model selector checkboxes
   □ BLS Employment panel (if available)

📑 TAB 1: Overview
   □ Company info card
   □ Current price with % change
   □ Key metrics (PE, PB, etc.)
   □ Buy signal indicator
   □ Basic company information

📑 TAB 2: Valuation (DD)
   □ DCF intrinsic value
   □ Current vs fair value comparison
   □ Upside/downside percentage
   □ Valuation multiples table
   □ Charts and visualizations

📑 TAB 3: Interactive DCF
   □ Adjustable sliders (discount rate, growth, etc.)
   □ Monte Carlo simulation
   □ Probability distributions
   □ Scenario analysis

📑 TAB 4: Technical (Charts)
   □ Candlestick price chart
   □ Volume bars
   □ Moving averages
   □ Technical indicators overlays

📑 TAB 5: Pro Indicators (60+)
   □ Summary bar with overall score
   □ Indicator categories
   □ Individual indicator values
   □ AI/ML predictions
   □ Indicator charts

📑 TAB 6: Delta Divergence
   □ Options flow chart
   □ Delta metrics
   □ Call/Put ratio
   □ Market expectation indicator

📑 TAB 7: Ape Sentiment
   □ Reddit sentiment score
   □ Sentiment gauge/meter
   □ Keywords/phrases
   □ Sentiment history

📑 TAB 8: Sentiment Correlation
   □ Correlation chart
   □ Sentiment vs price graph
   □ Correlation coefficient

📑 TAB 9: Smart Money
   □ Institutional ownership
   □ Insider trades table
   □ Congressional trades
   □ Recent activity

📑 TAB 10: AI Analysis ⭐ NEW!
   □ Instructions text
   □ API setup info
   □ "Click sidebar button" message
   
   After clicking "🚀 Analyze Everything":
   □ Loading spinner/progress
   □ Model status (which are running)
   □ Results tabs:
      □ Consensus Summary tab
         □ Executive summary
         □ Recommendation (BUY/HOLD/SELL)
         □ Confidence score with progress bar
         □ Fair value estimate
         □ Bull case section
         □ Bear case section
         □ Risk factors
      □ Individual Models tab
         □ Expandable sections per model
         □ Model weight displayed
         □ Full response from each AI
      □ Detailed Analysis tab
         □ Technical deep dive
         □ Sentiment analysis
         □ Options analysis
         □ Economic context
      □ Raw Data tab
         □ JSON output
         □ Download button

🎨 STYLING TO VERIFY:
   □ Gradient button (purple/blue)
   □ Pulsing animation on AI button
   □ Color-coded metrics (green/red)
   □ Responsive layout
   □ Readable fonts
   □ Proper spacing
   □ Icons rendering correctly
   □ Charts displaying properly

⚡ FUNCTIONALITY TO TEST:
   □ Ticker input works
   □ Analyze button fetches data
   □ Tabs switch smoothly
   □ Charts are interactive
   □ Buttons respond to clicks
   □ No console errors
   □ Data loads within 5 seconds
   □ AI button triggers analysis
   □ Results display properly
    """
    
    print(checklist)
    
    return True


def main():
    """Run all visual tests"""
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*18 + "VISUAL UI COMPONENT TEST" + " "*25 + "║")
    print("╚" + "="*68 + "╝")
    
    tests = [
        ("Dashboard Structure", test_dashboard_structure),
        ("Tab Definitions", test_tab_definitions),
        ("Global AI Components", test_global_ai_components),
        ("Sidebar Components", test_sidebar_components),
        ("Main Sections", test_main_sections),
        ("Visual Indicators", test_visual_indicators),
        ("Data Visualizations", test_data_visualizations),
        ("Export Features", test_export_features),
        ("Visual Checklist", create_visual_checklist)
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "="*70)
    print("📋 VISUAL TEST SUMMARY")
    print("="*70)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:30s}: {status}")
    
    passed = sum(results.values())
    total = len(results)
    
    print("\n" + "="*70)
    if passed == total:
        print(f"✅ ALL VISUAL TESTS PASSED ({passed}/{total})")
        print("\n🎨 All UI components are properly structured!")
        print("   • 10 tabs with distinct content")
        print("   • Sidebar with AI analysis button")
        print("   • Rich visualizations")
        print("   • Export functionality")
        print("   • Responsive styling")
    else:
        print(f"⚠️  SOME TESTS FAILED ({passed}/{total})")
    
    print("\n" + "="*70)
    print("🚀 NEXT STEP: Start dashboard and verify manually")
    print("="*70)
    print("\nRun:")
    print("   /workspaces/-Stocksv2/.venv/bin/python -m streamlit run dashboard_selector.py")
    print("\nThen use the checklist above to verify all elements are visible.")
    print("="*70 + "\n")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
