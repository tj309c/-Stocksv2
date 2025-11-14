"""
Analysis Engine - Valuation, Technical Analysis, and Buy Signal Detection
"""
import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict, Tuple, List
import ta
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class ValuationEngine:
    """Handles all valuation calculations"""
    
    def __init__(self):
        self.risk_free_rate = 0.045  # 10Y Treasury
        self.market_risk_premium = 0.065
        self.terminal_growth = 0.025
    
    def calculate_dcf(self, financials: Dict, info: Dict) -> Dict:
        """Calculate Discounted Cash Flow valuation"""
        try:
            # Extract key metrics
            beta = info.get("beta", 1.0)
            shares = info.get("sharesOutstanding", 0)
            
            if shares == 0:
                return {"error": "No shares outstanding data"}
            
            # Calculate WACC
            wacc = self.risk_free_rate + beta * self.market_risk_premium
            
            # Get cash flows (simplified - using net income as proxy)
            cash_flows = []
            if "cash_flow" in financials and financials["cash_flow"]:
                cf_data = pd.DataFrame(financials["cash_flow"])
                if "Free Cash Flow" in cf_data.index:
                    cash_flows = cf_data.loc["Free Cash Flow"].values[:4]
                elif "Operating Cash Flow" in cf_data.index:
                    cash_flows = cf_data.loc["Operating Cash Flow"].values[:4]
            
            if len(cash_flows) == 0:
                return {"error": "No cash flow data available"}
            
            # Project future cash flows
            avg_cf = np.mean(cash_flows)
            growth_rate = 0.10  # Assumed growth
            
            # 5-year projection
            projected_cfs = []
            for year in range(1, 6):
                cf = avg_cf * (1 + growth_rate) ** year
                pv = cf / (1 + wacc) ** year
                projected_cfs.append(pv)
            
            # Terminal value
            terminal_cf = avg_cf * (1 + growth_rate) ** 5 * (1 + self.terminal_growth)
            terminal_value = terminal_cf / (wacc - self.terminal_growth)
            pv_terminal = terminal_value / (1 + wacc) ** 5
            
            # Enterprise value and equity value
            enterprise_value = sum(projected_cfs) + pv_terminal
            
            # Add cash, subtract debt
            cash = info.get("totalCash", 0)
            debt = info.get("totalDebt", 0)
            equity_value = enterprise_value + cash - debt
            
            # Fair value per share
            fair_value = equity_value / shares
            current_price = info.get("currentPrice", info.get("regularMarketPrice", 0))
            
            # Calculate scenarios
            scenarios = {
                "bear": fair_value * 0.8,
                "base": fair_value,
                "bull": fair_value * 1.2
            }
            
            return {
                "fair_value": fair_value,
                "current_price": current_price,
                "upside": ((fair_value - current_price) / current_price * 100) if current_price > 0 else 0,
                "scenarios": scenarios,
                "wacc": wacc * 100,
                "enterprise_value": enterprise_value,
                "method": "DCF"
            }
            
        except Exception as e:
            logger.error(f"Error in DCF calculation: {e}")
            return {"error": str(e)}
    
    def calculate_multiples_valuation(self, info: Dict) -> Dict:
        """Calculate valuation based on multiples"""
        try:
            current_price = info.get("currentPrice", info.get("regularMarketPrice", 0))
            
            valuations = {}
            
            # P/E Valuation
            pe_ratio = info.get("trailingPE", 0)
            forward_pe = info.get("forwardPE", 0)
            industry_pe = info.get("industryPE", 20)  # Default industry P/E
            
            if pe_ratio > 0 and forward_pe > 0:
                eps = current_price / pe_ratio
                fair_value_pe = eps * min(industry_pe, 25)  # Cap at 25 P/E
                valuations["P/E"] = {
                    "fair_value": fair_value_pe,
                    "current_ratio": pe_ratio,
                    "target_ratio": industry_pe
                }
            
            # P/B Valuation
            pb_ratio = info.get("priceToBook", 0)
            if pb_ratio > 0:
                book_value = current_price / pb_ratio
                fair_value_pb = book_value * 1.5  # Target 1.5x book
                valuations["P/B"] = {
                    "fair_value": fair_value_pb,
                    "current_ratio": pb_ratio,
                    "target_ratio": 1.5
                }
            
            # PEG Valuation
            peg_ratio = info.get("pegRatio", 0)
            if peg_ratio > 0 and peg_ratio < 2:
                # PEG under 1 is undervalued
                fair_value_peg = current_price * (1 / peg_ratio)
                valuations["PEG"] = {
                    "fair_value": fair_value_peg,
                    "current_ratio": peg_ratio,
                    "target_ratio": 1.0
                }
            
            # Average fair value
            if valuations:
                avg_fair_value = np.mean([v["fair_value"] for v in valuations.values()])
                return {
                    "fair_value": avg_fair_value,
                    "current_price": current_price,
                    "upside": ((avg_fair_value - current_price) / current_price * 100) if current_price > 0 else 0,
                    "valuations": valuations,
                    "method": "Multiples"
                }
            
            return {"error": "Insufficient data for multiples valuation"}
            
        except Exception as e:
            logger.error(f"Error in multiples valuation: {e}")
            return {"error": str(e)}


class TechnicalAnalyzer:
    """Technical analysis and pattern detection"""
    
    def analyze(self, df: pd.DataFrame) -> Dict:
        """Run comprehensive technical analysis"""
        if df.empty or len(df) < 20:
            return {"error": "Insufficient data for technical analysis"}
        
        try:
            analysis = {}
            
            # Price action
            latest_price = df['Close'].iloc[-1]
            sma_20 = df['Close'].rolling(20).mean().iloc[-1]
            sma_50 = df['Close'].rolling(50).mean().iloc[-1] if len(df) >= 50 else sma_20
            sma_200 = df['Close'].rolling(200).mean().iloc[-1] if len(df) >= 200 else sma_50
            
            analysis["price_action"] = {
                "price": latest_price,
                "sma_20": sma_20,
                "sma_50": sma_50,
                "sma_200": sma_200,
                "above_sma_20": latest_price > sma_20,
                "above_sma_50": latest_price > sma_50,
                "above_sma_200": latest_price > sma_200,
            }
            
            # RSI
            rsi = ta.momentum.RSIIndicator(df['Close']).rsi().iloc[-1]
            analysis["rsi"] = {
                "value": rsi,
                "signal": "oversold" if rsi < 30 else "overbought" if rsi > 70 else "neutral"
            }
            
            # MACD
            macd = ta.trend.MACD(df['Close'])
            macd_line = macd.macd().iloc[-1]
            signal_line = macd.macd_signal().iloc[-1]
            analysis["macd"] = {
                "macd": macd_line,
                "signal": signal_line,
                "histogram": macd_line - signal_line,
                "bullish": macd_line > signal_line
            }
            
            # Bollinger Bands
            bb = ta.volatility.BollingerBands(df['Close'])
            analysis["bollinger"] = {
                "upper": bb.bollinger_hband().iloc[-1],
                "middle": bb.bollinger_mavg().iloc[-1],
                "lower": bb.bollinger_lband().iloc[-1],
                "price": latest_price,
                "signal": "oversold" if latest_price < bb.bollinger_lband().iloc[-1] else 
                         "overbought" if latest_price > bb.bollinger_hband().iloc[-1] else "neutral"
            }
            
            # Support and Resistance
            highs = df['High'].rolling(20).max()
            lows = df['Low'].rolling(20).min()
            analysis["support_resistance"] = {
                "resistance": highs.iloc[-1],
                "support": lows.iloc[-1],
                "price": latest_price,
                "near_support": (latest_price - lows.iloc[-1]) / lows.iloc[-1] < 0.02,
                "near_resistance": (highs.iloc[-1] - latest_price) / latest_price < 0.02
            }
            
            # Volume analysis
            avg_volume = df['Volume'].rolling(20).mean().iloc[-1]
            latest_volume = df['Volume'].iloc[-1]
            analysis["volume"] = {
                "current": latest_volume,
                "average": avg_volume,
                "ratio": latest_volume / avg_volume if avg_volume > 0 else 1,
                "increasing": latest_volume > avg_volume * 1.5
            }
            
            # Trend
            analysis["trend"] = self._determine_trend(df)
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error in technical analysis: {e}")
            return {"error": str(e)}
    
    def _determine_trend(self, df: pd.DataFrame) -> str:
        """Determine market trend"""
        if len(df) < 50:
            return "insufficient_data"
        
        sma_20 = df['Close'].rolling(20).mean()
        sma_50 = df['Close'].rolling(50).mean()
        
        if sma_20.iloc[-1] > sma_50.iloc[-1] and sma_20.iloc[-5] < sma_50.iloc[-5]:
            return "bullish_crossover"
        elif sma_20.iloc[-1] < sma_50.iloc[-1] and sma_20.iloc[-5] > sma_50.iloc[-5]:
            return "bearish_crossover"
        elif sma_20.iloc[-1] > sma_50.iloc[-1]:
            return "bullish"
        else:
            return "bearish"
    
    def detect_patterns(self, df: pd.DataFrame) -> List[Dict]:
        """Detect chart patterns"""
        patterns = []
        
        if len(df) < 50:
            return patterns
        
        # Simple pattern detection
        # Head and Shoulders
        if self._detect_head_shoulders(df):
            patterns.append({"pattern": "head_and_shoulders", "signal": "bearish"})
        
        # Double Bottom
        if self._detect_double_bottom(df):
            patterns.append({"pattern": "double_bottom", "signal": "bullish"})
        
        # Cup and Handle (simplified)
        if self._detect_cup_handle(df):
            patterns.append({"pattern": "cup_and_handle", "signal": "bullish"})
        
        return patterns
    
    def _detect_head_shoulders(self, df: pd.DataFrame) -> bool:
        """Simplified head and shoulders detection"""
        if len(df) < 60:
            return False
        
        prices = df['High'].values[-60:]
        # Find peaks
        peaks = []
        for i in range(1, len(prices)-1):
            if prices[i] > prices[i-1] and prices[i] > prices[i+1]:
                peaks.append((i, prices[i]))
        
        if len(peaks) >= 3:
            # Check if middle peak is highest (head)
            peak_values = [p[1] for p in peaks]
            max_idx = peak_values.index(max(peak_values))
            if 0 < max_idx < len(peaks) - 1:
                # Shoulders should be roughly equal
                left_shoulder = peak_values[max_idx - 1]
                right_shoulder = peak_values[max_idx + 1]
                if abs(left_shoulder - right_shoulder) / left_shoulder < 0.05:
                    return True
        
        return False
    
    def _detect_double_bottom(self, df: pd.DataFrame) -> bool:
        """Simplified double bottom detection"""
        if len(df) < 40:
            return False
        
        lows = df['Low'].values[-40:]
        # Find troughs
        troughs = []
        for i in range(1, len(lows)-1):
            if lows[i] < lows[i-1] and lows[i] < lows[i+1]:
                troughs.append((i, lows[i]))
        
        if len(troughs) >= 2:
            # Check if two lows are roughly equal
            for i in range(len(troughs)-1):
                if abs(troughs[i][1] - troughs[i+1][1]) / troughs[i][1] < 0.03:
                    # Check if price went up between them
                    between_high = max(lows[troughs[i][0]:troughs[i+1][0]])
                    if between_high > troughs[i][1] * 1.05:
                        return True
        
        return False
    
    def _detect_cup_handle(self, df: pd.DataFrame) -> bool:
        """Simplified cup and handle detection"""
        if len(df) < 60:
            return False
        
        prices = df['Close'].values[-60:]
        
        # Look for U-shape followed by slight decline
        mid_point = len(prices) // 2
        left_high = max(prices[:mid_point//2])
        bottom = min(prices[mid_point//2:mid_point+mid_point//2])
        right_high = max(prices[mid_point+mid_point//2:-10])
        handle = prices[-10:]
        
        # Cup shape: high-low-high
        if left_high > bottom * 1.1 and right_high > bottom * 1.1:
            # Handle: slight decline from right high
            if max(handle) < right_high and min(handle) > bottom * 1.05:
                return True
        
        return False


class GoodBuyAnalyzer:
    """Determines if a stock is a good buy"""
    
    def __init__(self):
        self.weights = {
            "valuation": 0.30,
            "technical": 0.25,
            "sentiment": 0.15,
            "momentum": 0.15,
            "fundamentals": 0.15
        }
    
    def analyze_buy_opportunity(self, 
                                ticker: str,
                                valuation: Dict,
                                technical: Dict,
                                sentiment: Dict,
                                info: Dict,
                                df: pd.DataFrame) -> Dict:
        """Determine if stock is a good buy and at what price"""
        
        scores = {}
        signals = []
        
        # 1. Valuation Score
        val_score = 0
        if "upside" in valuation and valuation["upside"] > 15:
            val_score = min(100, valuation["upside"] * 2)
            signals.append(f"Undervalued by {valuation['upside']:.1f}%")
        scores["valuation"] = val_score
        
        # 2. Technical Score
        tech_score = 0
        if technical and "error" not in technical:
            # RSI oversold
            if technical.get("rsi", {}).get("value", 50) < 35:
                tech_score += 30
                signals.append(f"RSI oversold at {technical['rsi']['value']:.1f}")
            
            # MACD bullish
            if technical.get("macd", {}).get("bullish", False):
                tech_score += 20
                signals.append("MACD bullish crossover")
            
            # Near support
            if technical.get("support_resistance", {}).get("near_support", False):
                tech_score += 30
                signals.append("Near support level")
            
            # Volume surge
            if technical.get("volume", {}).get("ratio", 1) > 1.5:
                tech_score += 20
                signals.append("Volume surge detected")
        
        scores["technical"] = min(100, tech_score)
        
        # 3. Sentiment Score
        sent_score = 50  # Neutral default
        if sentiment and "sentiment_score" in sentiment:
            if sentiment["sentiment_score"] > 20:
                sent_score = 70
                signals.append("Positive sentiment")
            elif sentiment["sentiment_score"] < -20:
                sent_score = 30
        scores["sentiment"] = sent_score
        
        # 4. Momentum Score
        mom_score = 0
        if not df.empty and len(df) > 20:
            returns_1m = ((df['Close'].iloc[-1] / df['Close'].iloc[-20]) - 1) * 100 if len(df) > 20 else 0
            returns_3m = ((df['Close'].iloc[-1] / df['Close'].iloc[-60]) - 1) * 100 if len(df) > 60 else 0
            
            # Positive but not excessive momentum
            if 0 < returns_1m < 10:
                mom_score += 50
            if -10 < returns_3m < 0:  # Recent pullback
                mom_score += 30
                signals.append("Healthy pullback in uptrend")
        
        scores["momentum"] = min(100, mom_score)
        
        # 5. Fundamentals Score
        fund_score = 50  # Default
        if info:
            pe_ratio = info.get("trailingPE", 0)
            if 0 < pe_ratio < 20:
                fund_score += 25
            
            profit_margin = info.get("profitMargins", 0)
            if profit_margin > 0.15:
                fund_score += 25
        
        scores["fundamentals"] = min(100, fund_score)
        
        # Calculate weighted score
        total_score = sum(scores[k] * self.weights[k] for k in scores)
        
        # Determine buy zones
        current_price = info.get("currentPrice", info.get("regularMarketPrice", 0))
        
        # Calculate good buy price range
        if total_score >= 70:
            # Strong buy
            buy_range_low = current_price * 0.98
            buy_range_high = current_price * 1.02
            confidence = "HIGH"
        elif total_score >= 50:
            # Moderate buy
            buy_range_low = current_price * 0.95
            buy_range_high = current_price
            confidence = "MEDIUM"
        else:
            # Wait for better entry
            buy_range_low = current_price * 0.90
            buy_range_high = current_price * 0.95
            confidence = "LOW"
        
        # Target price
        if "fair_value" in valuation:
            target_price = valuation["fair_value"]
        else:
            # Use technical resistance
            target_price = technical.get("support_resistance", {}).get("resistance", current_price * 1.15)
        
        return {
            "ticker": ticker,
            "current_price": current_price,
            "total_score": total_score,
            "confidence": confidence,
            "buy_range": {
                "low": buy_range_low,
                "high": buy_range_high
            },
            "target_price": target_price,
            "stop_loss": buy_range_low * 0.95,
            "risk_reward_ratio": (target_price - current_price) / (current_price - buy_range_low * 0.95) if current_price > buy_range_low else 0,
            "scores": scores,
            "signals": signals,
            "recommendation": "STRONG BUY" if total_score >= 70 else "BUY" if total_score >= 50 else "HOLD"
        }


class OptionsAnalyzer:
    """Analyze options for opportunities"""
    
    def find_best_opportunities(self, options_data: Dict, current_price: float) -> List[Dict]:
        """Find best options opportunities"""
        opportunities = []
        
        if not options_data or "chains" not in options_data:
            return opportunities
        
        for expiration, chain in options_data["chains"].items():
            if not chain:
                continue
            
            # Analyze calls
            if "calls" in chain and chain["calls"]:
                calls_df = pd.DataFrame(chain["calls"])
                if not calls_df.empty and "strike" in calls_df.columns:
                    # Find high volume/OI ratio
                    if "volume" in calls_df.columns and "openInterest" in calls_df.columns:
                        calls_df["vol_oi_ratio"] = calls_df["volume"] / calls_df["openInterest"].replace(0, 1)
                        unusual = calls_df[calls_df["vol_oi_ratio"] > 2]
                        
                        for _, row in unusual.iterrows():
                            opportunities.append({
                                "type": "CALL",
                                "strike": row.get("strike", 0),
                                "expiration": expiration,
                                "volume": row.get("volume", 0),
                                "oi": row.get("openInterest", 0),
                                "iv": row.get("impliedVolatility", 0),
                                "signal": "Unusual activity"
                            })
        
        return opportunities[:10]  # Top 10 opportunities
