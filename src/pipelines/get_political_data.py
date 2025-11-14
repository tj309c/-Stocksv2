"""
Political & Insider Data Scraper
Tracks congressional stock trades and corporate insider transactions.

Data Sources:
- Senate Financial Disclosures: https://efdsearch.senate.gov/search/
- House Financial Disclosures: https://disclosures-clerk.house.gov/
- Finnhub Insider Transactions API: https://finnhub.io/ (Free tier: 60 req/min)

Use Cases:
- Detect early sector rotation signals (e.g., senators buying defense stocks before policy announcement)
- Insider buy/sell ratio as bullish/bearish signal for specific stocks
- Monitor "smart money" positioning
"""

import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging
import requests
from bs4 import BeautifulSoup
import time

try:
    import finnhub
    FINNHUB_AVAILABLE = True
except ImportError:
    FINNHUB_AVAILABLE = False

logger = logging.getLogger(__name__)


class PoliticalDataPipeline:
    """
    Scrapes and aggregates political and insider trading data.
    
    WARNING: Congressional disclosure scraping may be rate-limited or blocked.
    Use responsibly and cache aggressively.
    """
    
    def __init__(self):
        """Initialize with API keys from Streamlit secrets or environment."""
        self.finnhub_client = None
        
        try:
            if hasattr(st, 'secrets'):
                finnhub_key = st.secrets.get('FINNHUB_API_KEY')
            else:
                import os
                finnhub_key = os.getenv('FINNHUB_API_KEY')
            
            if finnhub_key and FINNHUB_AVAILABLE:
                self.finnhub_client = finnhub.Client(api_key=finnhub_key)
                logger.info("Finnhub API initialized successfully")
            else:
                logger.warning("Finnhub API key not found or finnhub-python not installed")
                
        except Exception as e:
            logger.error(f"Error initializing Finnhub API: {e}")
    
    # =========================================================================
    # Congressional Trades (Senate)
    # =========================================================================
    
    @st.cache_data(ttl=43200, show_spinner=False)  # Cache for 12 hours
    def scrape_senate_trades(_self, max_results: int = 100) -> Optional[pd.DataFrame]:
        """
        Scrape recent Senate financial disclosures.
        
        NOTE: This is a simplified scraper. The actual Senate disclosure site
        (https://efdsearch.senate.gov/) uses JavaScript and may require Selenium
        or API access. For now, this returns a placeholder structure.
        
        Args:
            max_results: Maximum number of trades to fetch
            
        Returns:
            DataFrame with columns: date, senator, ticker, transaction_type, amount_range
        """
        st.warning("⚠️ Senate trade scraping requires advanced setup (Selenium/API). Placeholder data shown.")
        
        # Placeholder - In production, implement Selenium scraper or use paid API
        return pd.DataFrame({
            'date': [datetime.now() - timedelta(days=i) for i in range(10)],
            'senator': ['Sen. Smith', 'Sen. Johnson', 'Sen. Williams'] * 3 + ['Sen. Brown'],
            'ticker': ['AAPL', 'MSFT', 'TSLA', 'NVDA', 'META', 'GOOGL', 'AMZN', 'SPY', 'QQQ', 'LMT'],
            'transaction_type': ['Buy', 'Sell', 'Buy', 'Buy', 'Sell', 'Buy', 'Sell', 'Buy', 'Buy', 'Buy'],
            'amount_range': ['$15,001 - $50,000'] * 10,
            'disclosure_date': [datetime.now()] * 10
        })
    
    @st.cache_data(ttl=43200, show_spinner=False)
    def analyze_senate_sentiment(_self, ticker: Optional[str] = None) -> Dict:
        """
        Analyze congressional trading sentiment for a specific ticker or overall market.
        
        Args:
            ticker: Optional ticker to filter by
            
        Returns:
            Dictionary with buy/sell counts, net sentiment score
        """
        trades_df = _self.scrape_senate_trades()
        
        if trades_df is None or len(trades_df) == 0:
            return {'error': 'No data available'}
        
        if ticker:
            trades_df = trades_df[trades_df['ticker'] == ticker.upper()]
        
        buy_count = len(trades_df[trades_df['transaction_type'] == 'Buy'])
        sell_count = len(trades_df[trades_df['transaction_type'] == 'Sell'])
        
        # Net sentiment: positive = more buying, negative = more selling
        net_sentiment = (buy_count - sell_count) / (buy_count + sell_count) if (buy_count + sell_count) > 0 else 0
        
        return {
            'buy_count': buy_count,
            'sell_count': sell_count,
            'net_sentiment': net_sentiment,
            'total_trades': buy_count + sell_count,
            'bullish': net_sentiment > 0.2,
            'bearish': net_sentiment < -0.2
        }
    
    # =========================================================================
    # Corporate Insider Transactions (Finnhub)
    # =========================================================================
    
    @st.cache_data(ttl=3600, show_spinner=False)  # Cache for 1 hour
    def get_insider_transactions(_self, ticker: str, months: int = 3) -> Optional[pd.DataFrame]:
        """
        Fetch corporate insider transactions from Finnhub.
        
        Args:
            ticker: Stock ticker symbol
            months: Number of months of historical data
            
        Returns:
            DataFrame with columns: date, name, transaction, shares, price
        """
        if not _self.finnhub_client:
            st.warning("⚠️ Finnhub API not configured. Get free key at: https://finnhub.io/register")
            return None
        
        try:
            from_date = (datetime.now() - timedelta(days=months*30)).strftime('%Y-%m-%d')
            to_date = datetime.now().strftime('%Y-%m-%d')
            
            data = _self.finnhub_client.stock_insider_transactions(
                ticker.upper(),
                from_date,
                to_date
            )
            
            if not data or 'data' not in data:
                return None
            
            df = pd.DataFrame(data['data'])
            
            if len(df) == 0:
                return None
            
            # Clean and format
            df['filing_date'] = pd.to_datetime(df['filingDate'])
            df['transaction_date'] = pd.to_datetime(df['transactionDate'])
            df['name'] = df['name']
            df['transaction_type'] = df['transactionCode'].map({
                'P': 'Purchase',
                'S': 'Sale',
                'A': 'Award',
                'M': 'Option Exercise'
            }).fillna(df['transactionCode'])
            df['shares'] = df['share']
            df['price'] = df['transactionPrice']
            
            # Calculate transaction value
            df['value'] = df['shares'] * df['price']
            
            return df[['transaction_date', 'filing_date', 'name', 'transaction_type', 'shares', 'price', 'value']].sort_values('transaction_date', ascending=False)
            
        except Exception as e:
            logger.error(f"Error fetching insider transactions for {ticker}: {e}")
            return None
    
    @st.cache_data(ttl=3600, show_spinner=False)
    def analyze_insider_sentiment(_self, ticker: str, months: int = 3) -> Dict:
        """
        Analyze insider trading sentiment for a ticker.
        High insider buying = bullish signal.
        High insider selling = neutral (could be personal reasons, not necessarily bearish).
        
        Args:
            ticker: Stock ticker symbol
            months: Number of months to analyze
            
        Returns:
            Dictionary with buy/sell metrics and sentiment score
        """
        df = _self.get_insider_transactions(ticker, months)
        
        if df is None or len(df) == 0:
            return {'error': 'No insider data available'}
        
        # Filter to actual purchases and sales
        buys = df[df['transaction_type'] == 'Purchase']
        sells = df[df['transaction_type'] == 'Sale']
        
        buy_value = buys['value'].sum()
        sell_value = sells['value'].sum()
        buy_count = len(buys)
        sell_count = len(sells)
        
        # Calculate buy/sell ratio (value-weighted)
        if buy_value + sell_value > 0:
            buy_ratio = buy_value / (buy_value + sell_value)
        else:
            buy_ratio = 0.5
        
        # Sentiment interpretation
        if buy_ratio > 0.7:
            sentiment = 'Strongly Bullish'
        elif buy_ratio > 0.55:
            sentiment = 'Bullish'
        elif buy_ratio > 0.45:
            sentiment = 'Neutral'
        else:
            sentiment = 'Cautious'  # Note: Insider selling is not necessarily bearish
        
        return {
            'buy_count': buy_count,
            'sell_count': sell_count,
            'buy_value': buy_value,
            'sell_value': sell_value,
            'buy_ratio': buy_ratio,
            'sentiment': sentiment,
            'total_transactions': buy_count + sell_count
        }
    
    # =========================================================================
    # Aggregation Methods
    # =========================================================================
    
    def get_comprehensive_insider_report(self, ticker: str) -> Dict:
        """
        Generate a comprehensive report combining corporate insiders and congressional trades.
        
        Args:
            ticker: Stock ticker symbol
            
        Returns:
            Dictionary with all insider and political data
        """
        report = {}
        
        # Corporate insiders
        insider_df = self.get_insider_transactions(ticker, months=6)
        insider_sentiment = self.analyze_insider_sentiment(ticker, months=6)
        
        report['corporate_insider_transactions'] = insider_df
        report['corporate_insider_sentiment'] = insider_sentiment
        
        # Congressional trades
        senate_sentiment = self.analyze_senate_sentiment(ticker)
        
        report['congressional_sentiment'] = senate_sentiment
        
        # Combined score
        # Weight: 70% corporate insiders, 30% congressional (corporate insiders more reliable)
        insider_score = insider_sentiment.get('buy_ratio', 0.5) if 'buy_ratio' in insider_sentiment else 0.5
        congress_score = (senate_sentiment.get('net_sentiment', 0) + 1) / 2  # Convert -1 to 1 range to 0 to 1
        
        combined_score = (insider_score * 0.7) + (congress_score * 0.3)
        
        report['combined_insider_score'] = combined_score
        report['combined_sentiment'] = 'Bullish' if combined_score > 0.6 else 'Neutral' if combined_score > 0.4 else 'Bearish'
        
        return report


# Convenience function
def get_political_data_pipeline() -> PoliticalDataPipeline:
    """Factory function to get configured pipeline instance."""
    return PoliticalDataPipeline()
