# 🧪 Manual UI Testing Checklist
**User Acceptance Testing for Stock Dashboard Application**

## Pre-Test Setup
- [ ] App is running on http://localhost:8502
- [ ] Have test tickers ready: AAPL, TSLA, META, GME, SPY, BTC-USD, ETH-USD
- [ ] Test on desktop (Chrome/Safari/Firefox)
- [ ] If possible, test on mobile device

---

## 📱 STOCK DASHBOARD

### Tab 1: Overview
- [ ] Enter ticker "AAPL" - loads quickly (<3s)
- [ ] Current price displayed correctly
- [ ] Price chart renders properly
- [ ] Key metrics section shows all data
- [ ] Try invalid ticker "INVALID123" - error message is user-friendly (not technical)
- [ ] Try clearing ticker field - shows helpful prompt

**Expected Issues:**
- ⚠️ Invalid tickers may not show clear error message
- ⚠️ Empty ticker field needs better handling

### Tab 2: Valuation (DD)
- [ ] DCF valuation displays (not $0.00)
- [ ] If DCF is $0.00, error message is clear (not confusing)
- [ ] Graham formula shows value
- [ ] Intrinsic value metrics present
- [ ] All valuation models complete without errors

**Expected Issues:**
- ⚠️ DCF $0.00 needs better error message explaining missing data

### Tab 3: Interactive DCF 🎯 **CRITICAL TEST**
This is a key feature - test thoroughly!

#### Sub-tab: Basic DCF
- [ ] 7 sliders present: Base Cash Flow, Growth Rate, WACC, Terminal Growth, Projection Years, Cash, Debt
- [ ] Moving any slider recalculates fair value instantly (<1s from cache)
- [ ] Fair value updates in real-time
- [ ] Reset button works
- [ ] All labels clear and understandable

**Expected Sliders:**
1. Base Free Cash Flow
2. Revenue Growth Rate
3. WACC (Discount Rate)
4. Terminal Growth Rate
5. Projection Years (5-15)
6. Cash & Equivalents
7. Total Debt

#### Sub-tab: Monte Carlo Simulation
- [ ] Number of simulations slider: 100 to 10,000
- [ ] "Run Simulation" button present
- [ ] Click Run - shows loading indicator or progress bar
- [ ] Results show: Mean, Median, Std Dev, Confidence Intervals
- [ ] Histogram chart displays distribution
- [ ] Chart is readable and well-labeled
- [ ] Can adjust parameters and re-run

**Expected Issues:**
- ⚠️ 10,000 simulations may freeze UI (5-10 seconds)
- ⚠️ No progress bar during calculation

#### Sub-tab: Sensitivity Analysis
- [ ] Two parameters to vary (e.g., Growth Rate vs WACC)
- [ ] Heatmap displays properly
- [ ] Values update when sliders change
- [ ] Color scale is intuitive
- [ ] Axes are labeled clearly

#### Sub-tab: Scenario Comparison
- [ ] Three scenarios: Bull, Base, Bear
- [ ] Can adjust parameters for each
- [ ] Side-by-side comparison chart
- [ ] Values calculate correctly
- [ ] Easy to understand differences

### Tab 4: Technical (Charts)
- [ ] Candlestick chart renders
- [ ] Volume bars display below
- [ ] Technical indicators overlay (SMA 50, SMA 200)
- [ ] RSI indicator present
- [ ] MACD indicator present
- [ ] Bollinger Bands (if implemented)
- [ ] Chart is zoomable/interactive
- [ ] Timeframe selector works (1M, 3M, 6M, 1Y)

**Expected Issues:**
- ⚠️ Missing some standard indicators (Bollinger Bands, SMA 50, SMA 200)

### Tab 5: Ape Sentiment 🦍
- [ ] Sentiment score displays
- [ ] Source breakdown (Reddit, Twitter, News)
- [ ] Sentiment trend chart
- [ ] "Apes together strong" vibe maintained
- [ ] Data refreshes appropriately

### Tab 6: Smart Money
- [ ] Institutional holdings data
- [ ] Recent insider trades
- [ ] Option flow analysis (if applicable)
- [ ] Unusual activity alerts
- [ ] All data formatted clearly

---

## 📈 OPTIONS DASHBOARD

### Tab: Chain Analysis
- [ ] Enter ticker "SPY"
- [ ] Options chain loads (<5s)
- [ ] Call/Put sections clear
- [ ] Strike prices aligned
- [ ] Expiration date selector works
- [ ] Bid/Ask/Volume/OI columns present
- [ ] Can filter by moneyness (ITM/OTM)

### Tab: Greeks
- [ ] Delta, Gamma, Theta, Vega displayed
- [ ] Greeks explain tooltip (helpful for beginners)
- [ ] Greeks update when changing expiry
- [ ] Color coding for positive/negative

### Tab: Strategy Builder
- [ ] Can select strategies: Covered Call, Protective Put, Iron Condor, etc.
- [ ] Visual payoff diagram renders
- [ ] Max profit/loss calculations
- [ ] Break-even points marked
- [ ] Can adjust strikes interactively

**Expected Issues:**
- ⚠️ No options chain for stocks without options - needs friendly error

---

## ₿ CRYPTO DASHBOARD

### Tab: Overview
- [ ] Enter "BTC-USD"
- [ ] Current price in USD
- [ ] 24h price change percentage
- [ ] Volume data present
- [ ] Real-time updates (or shows data timestamp)

### Tab: Technical
- [ ] Crypto-specific indicators (if any)
- [ ] Same chart quality as stock dashboard
- [ ] Timeframes work correctly

### Tab: Fear & Greed Index
- [ ] Index gauge displays (0-100)
- [ ] Historical trend chart
- [ ] Interpretation text ("Extreme Fear" etc.)
- [ ] Sources cited

### Tab: HODL Calculator 💎🙌
- [ ] "When Lambo?" calculator present
- [ ] Input: Initial investment amount
- [ ] Input: Purchase date
- [ ] Output: Current value
- [ ] Output: ROI percentage
- [ ] Fun/engaging presentation

---

## 🔬 ADVANCED DASHBOARD

### Tab: Backtesting
- [ ] Can select strategy parameters
- [ ] Historical data range selector
- [ ] "Run Backtest" button
- [ ] Results show: Total Return, Sharpe Ratio, Max Drawdown
- [ ] Equity curve chart
- [ ] Trade log (optional)

### Tab: Forecasting
- [ ] LLM prediction section (if implemented)
- [ ] Monte Carlo price paths
- [ ] Confidence bands on chart
- [ ] Forecast horizon selector
- [ ] Disclaimer about predictions

### Tab: Squeeze Detection
- [ ] Short interest percentage
- [ ] Days to cover
- [ ] Borrow fee rate
- [ ] Squeeze probability score
- [ ] GME/AMC example data works

### Tab: Sector Comparison
- [ ] Can compare multiple tickers
- [ ] Performance chart (YTD, 1Y, etc.)
- [ ] Sector averages shown
- [ ] Relative strength metrics

---

## 💼 PORTFOLIO DASHBOARD

### Tab: Optimal Allocation
- [ ] Can input portfolio tickers
- [ ] Weight sliders for each ticker
- [ ] Optimization algorithm runs
- [ ] Recommended allocation displayed
- [ ] Expected return & risk shown

### Tab: Efficient Frontier
- [ ] Chart plots risk vs return
- [ ] Optimal portfolio marked
- [ ] Can see different portfolio points
- [ ] Sharpe ratio indicated

### Tab: Risk/Return
- [ ] Portfolio metrics summary
- [ ] Volatility calculation
- [ ] Correlation matrix heatmap
- [ ] Diversification score

### Tab: Rebalancing
- [ ] Current vs target allocation
- [ ] Trades needed to rebalance
- [ ] Cost basis considerations (if applicable)
- [ ] Export rebalancing instructions

---

## 🔧 DEBUG DASHBOARD

### Health Check
- [ ] Run comprehensive health check
- [ ] Shows pass/fail for all modules
- [ ] Detailed error logs (if any)
- [ ] Export health report button

### Performance Metrics
- [ ] Cache hit rate
- [ ] API call count
- [ ] Load times by dashboard
- [ ] Memory usage (if tracked)

### Diagnostics
- [ ] System info (Python version, packages)
- [ ] Configuration viewer
- [ ] Log viewer
- [ ] Clear cache button

---

## 🎨 THEME & SETTINGS

### Theme Toggle
- [ ] Light mode renders correctly
- [ ] Dark mode renders correctly
- [ ] All text readable in both themes
- [ ] Charts adapt to theme
- [ ] No contrast issues

### Settings (if present)
- [ ] Can adjust cache TTL
- [ ] Can toggle features on/off
- [ ] Settings persist across sessions

---

## 🚨 CRITICAL USER FLOWS

### First-Time User Experience
1. [ ] Open app - homepage is welcoming
2. [ ] Select "Stock Dashboard"
3. [ ] Don't know what ticker to enter - is there placeholder/example?
4. [ ] Enter "AAPL" - everything loads smoothly
5. [ ] Navigate through all tabs - no errors
6. [ ] Try Interactive DCF - understand what sliders do
7. [ ] Run Monte Carlo - not confused by loading time

### Power User Experience
1. [ ] Quickly enter ticker (no lag)
2. [ ] Jump between dashboards using sidebar
3. [ ] Adjust DCF parameters rapidly
4. [ ] Export data or charts (if available)
5. [ ] Switch to another ticker seamlessly

### Error Recovery
1. [ ] Enter invalid ticker - error is clear, not technical
2. [ ] Try ticker with no data - friendly message
3. [ ] Internet drops mid-load - app doesn't crash
4. [ ] Go back button works
5. [ ] Can recover from any error without refresh

---

## 📊 USABILITY SCORING

Rate each dashboard 1-5 stars:
- **Stock Dashboard**: ⭐⭐⭐⭐⭐ _____
- **Options Dashboard**: ⭐⭐⭐⭐⭐ _____
- **Crypto Dashboard**: ⭐⭐⭐⭐⭐ _____
- **Advanced Dashboard**: ⭐⭐⭐⭐⭐ _____
- **Portfolio Dashboard**: ⭐⭐⭐⭐⭐ _____

**Overall App Experience**: ⭐⭐⭐⭐⭐ _____

---

## 🐛 BUG TRACKER

| Bug # | Dashboard | Description | Severity | Reproduced? |
|-------|-----------|-------------|----------|-------------|
| 1 | Stock | Invalid ticker not caught | Medium | [ ] |
| 2 | All | Stale data not flagged | Medium | [ ] |
| 3 | Stock | DCF $0.00 confusing | Medium | [ ] |
| 4 | Technical | Missing indicators | Medium | [ ] |
| 5 | All | No market hours indicator | Low | [ ] |

---

## ✅ ACCEPTANCE CRITERIA

**App is ready for launch if:**
- [x] Zero critical bugs
- [ ] < 3 high priority bugs
- [ ] All core features work (Stock Dashboard tabs 1-6)
- [ ] Interactive DCF fully functional
- [ ] Monte Carlo simulation works
- [ ] No data fetch crashes
- [ ] Error messages are user-friendly
- [ ] Performance acceptable (<3s load times)

**Current Status:** 🟢 **READY** | 🟡 **NEEDS WORK** | 🔴 **NOT READY**

---

## 💡 ENHANCEMENT PRIORITIES

Based on automated testing, prioritize these enhancements:

**High Priority (Improves Core UX):**
1. Add watchlist/favorites feature
2. Add data freshness indicator
3. Add loading progress bars
4. Improve error messages (user-friendly)
5. Add missing technical indicators

**Medium Priority (Nice to Have):**
6. Export to CSV/PDF
7. Keyboard shortcuts
8. Mobile optimization
9. Lazy loading for large tables

**Low Priority (Polish):**
10. Alt text for accessibility
11. Market hours indicator
12. Theme consistency improvements

---

## 📝 TESTER NOTES

**Date:** _____________
**Tester:** _____________
**Browser/Device:** _____________

**Overall Impression:**
```
(Write overall thoughts here)
```

**Best Features:**
- 
- 
- 

**Most Confusing Parts:**
- 
- 
- 

**Would You Use This App?** YES / NO

**Recommendation:** LAUNCH / DELAY / MAJOR REWORK
