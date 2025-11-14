"""
Data Fetcher Module - Using yfinance for all market data
Only scrapes for sentiment/news
"""
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import requests
from bs4 import BeautifulSoup
import json
import sqlite3
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class MarketDataFetcher:
    """Fetches all market data using yfinance API"""
    
    def __init__(self, cache_dir: Path = Path("data/cache")):
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = self.cache_dir / "market_data.db"
        self._init_db()
        
    def _init_db(self):
        """Initialize SQLite database for caching"""
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS cache (
                key TEXT PRIMARY KEY,
                data TEXT,
                timestamp DATETIME
            )
        """)
        conn.commit()
        conn.close()
    
    def _get_cached(self, key: str, max_age_minutes: int = 5) -> Optional[Dict]:
        """Get cached data if not expired"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT data, timestamp FROM cache WHERE key = ?", (key,)
        )
        result = cursor.fetchone()
        conn.close()
        
        if result:
            data, timestamp = result
            cached_time = datetime.fromisoformat(timestamp)
            if datetime.now() - cached_time < timedelta(minutes=max_age_minutes):
                return json.loads(data)
        return None
    
    def _set_cache(self, key: str, data: Dict):
        """Store data in cache"""
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            "INSERT OR REPLACE INTO cache (key, data, timestamp) VALUES (?, ?, ?)",
            (key, json.dumps(data, default=str), datetime.now().isoformat())
        )
        conn.commit()
        conn.close()
    
    # ========== PRICE DATA ==========
    def get_stock_data(self, ticker: str, period: str = "1y") -> Dict:
        """Get comprehensive stock data from yfinance"""
        cache_key = f"stock_{ticker}_{period}"
        cached = self._get_cached(cache_key)
        if cached:
            return cached
        
        try:
            stock = yf.Ticker(ticker)
            
            # Get all data in one go
            data = {
                "info": stock.info,
                "history": stock.history(period=period).to_dict(),
                "actions": stock.actions.to_dict() if not stock.actions.empty else {},
                "dividends": stock.dividends.to_dict() if not stock.dividends.empty else {},
                "splits": stock.splits.to_dict() if not stock.splits.empty else {},
            }
            
            self._set_cache(cache_key, data)
            return data
            
        except Exception as e:
            logger.error(f"Error fetching stock data for {ticker}: {e}")
            return {}
    
    def get_realtime_quote(self, ticker: str) -> Dict:
        """Get real-time quote"""
        cache_key = f"quote_{ticker}"
        cached = self._get_cached(cache_key, max_age_minutes=1)
        if cached:
            return cached
        
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            quote = {
                "price": info.get("currentPrice", info.get("regularMarketPrice", 0)),
                "change": info.get("regularMarketChange", 0),
                "change_pct": info.get("regularMarketChangePercent", 0),
                "volume": info.get("volume", 0),
                "bid": info.get("bid", 0),
                "ask": info.get("ask", 0),
                "bid_size": info.get("bidSize", 0),
                "ask_size": info.get("askSize", 0),
                "high": info.get("dayHigh", 0),
                "low": info.get("dayLow", 0),
                "open": info.get("open", 0),
                "prev_close": info.get("previousClose", 0),
                "timestamp": datetime.now().isoformat()
            }
            
            self._set_cache(cache_key, quote)
            return quote
            
        except Exception as e:
            logger.error(f"Error fetching quote for {ticker}: {e}")
            return {}
    
    # ========== OPTIONS DATA ==========
    def get_options_chain(self, ticker: str) -> Dict:
        """Get options chain with Greeks"""
        cache_key = f"options_{ticker}"
        cached = self._get_cached(cache_key, max_age_minutes=5)
        if cached:
            return cached
        
        try:
            stock = yf.Ticker(ticker)
            expirations = stock.options[:6]  # Get first 6 expirations
            
            options_data = {
                "expirations": expirations,
                "chains": {}
            }
            
            for exp in expirations:
                chain = stock.option_chain(exp)
                options_data["chains"][exp] = {
                    "calls": chain.calls.to_dict() if not chain.calls.empty else {},
                    "puts": chain.puts.to_dict() if not chain.puts.empty else {}
                }
            
            self._set_cache(cache_key, options_data)
            return options_data
            
        except Exception as e:
            logger.error(f"Error fetching options for {ticker}: {e}")
            return {}
    
    # ========== FUNDAMENTALS ==========
    def get_fundamentals(self, ticker: str) -> Dict:
        """Get fundamental data"""
        cache_key = f"fundamentals_{ticker}"
        cached = self._get_cached(cache_key, max_age_minutes=60)
        if cached:
            return cached
        
        try:
            stock = yf.Ticker(ticker)
            
            fundamentals = {
                "financials": stock.financials.to_dict() if hasattr(stock, 'financials') and stock.financials is not None else {},
                "balance_sheet": stock.balance_sheet.to_dict() if hasattr(stock, 'balance_sheet') and stock.balance_sheet is not None else {},
                "cash_flow": stock.cashflow.to_dict() if hasattr(stock, 'cashflow') and stock.cashflow is not None else {},
                "earnings": stock.earnings.to_dict() if hasattr(stock, 'earnings') and stock.earnings is not None else {},
                "recommendations": stock.recommendations.to_dict() if hasattr(stock, 'recommendations') and stock.recommendations is not None else {},
            }
            
            self._set_cache(cache_key, fundamentals)
            return fundamentals
            
        except Exception as e:
            logger.error(f"Error fetching fundamentals for {ticker}: {e}")
            return {}
    
    # ========== INSTITUTIONAL ==========
    def get_institutional_data(self, ticker: str) -> Dict:
        """Get institutional and insider data"""
        try:
            stock = yf.Ticker(ticker)
            
            return {
                "major_holders": stock.major_holders.to_dict() if hasattr(stock, 'major_holders') and stock.major_holders is not None else {},
                "institutional_holders": stock.institutional_holders.to_dict() if hasattr(stock, 'institutional_holders') and stock.institutional_holders is not None else {},
                "insider_transactions": stock.insider_transactions.to_dict() if hasattr(stock, 'insider_transactions') and stock.insider_transactions is not None else {},
                "insider_purchases": stock.insider_purchases.to_dict() if hasattr(stock, 'insider_purchases') and stock.insider_purchases is not None else {},
            }
            
        except Exception as e:
            logger.error(f"Error fetching institutional data for {ticker}: {e}")
            return {}


class SentimentScraper:
    """Scrapes sentiment data from web sources"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_stocktwits_sentiment(self, ticker: str) -> Dict:
        """Get StockTwits sentiment"""
        try:
            url = f"https://api.stocktwits.com/api/2/streams/symbol/{ticker}.json"
            response = self.session.get(url)
            
            if response.status_code != 200:
                return {"error": "Unable to fetch StockTwits data"}
            
            data = response.json()
            messages = data.get("messages", [])
            
            if not messages:
                return {"error": "No messages found"}
            
            # Analyze sentiment
            bullish = bearish = neutral = 0
            for msg in messages:
                sentiment = msg.get("entities", {}).get("sentiment", {}).get("basic")
                if sentiment == "Bullish":
                    bullish += 1
                elif sentiment == "Bearish":
                    bearish += 1
                else:
                    neutral += 1
            
            total = len(messages)
            return {
                "total_messages": total,
                "bullish": bullish,
                "bearish": bearish,
                "neutral": neutral,
                "bullish_pct": (bullish/total)*100 if total > 0 else 0,
                "bearish_pct": (bearish/total)*100 if total > 0 else 0,
                "sentiment_score": ((bullish-bearish)/total)*100 if total > 0 else 0,
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error fetching StockTwits sentiment: {e}")
            return {"error": str(e)}
    

    def get_news_sentiment(self, ticker: str) -> List[Dict]:
        """Get news from yfinance"""
        try:
            stock = yf.Ticker(ticker)
            news = stock.news
            
            if not news:
                return []
            
            # Format news items
            formatted = []
            for item in news[:10]:  # Limit to 10 items
                formatted.append({
                    "title": item.get("title", ""),
                    "publisher": item.get("publisher", ""),
                    "link": item.get("link", ""),
                    "timestamp": datetime.fromtimestamp(item.get("providerPublishTime", 0)).isoformat(),
                })
            
            return formatted
            
        except Exception as e:
            logger.error(f"Error fetching news: {e}")
            return []
