"""
Stock Ticker Data Scraper
Retrieves news articles, Reddit posts, and search results for a given stock ticker
with sentiment analysis and structured output.
"""

import requests
from datetime import datetime, timedelta
import pandas as pd
from typing import List, Dict
import time
from urllib.parse import quote
import re

# For sentiment analysis
try:
    from textblob import TextBlob
except ImportError:
    print("TextBlob not installed. Install with: pip install textblob")


class StockDataScraper:
    """Scraper for collecting stock-related data from multiple sources."""
    
    def __init__(self, ticker: str):
        """
        Initialize the scraper with a stock ticker.
        
        Args:
            ticker: Stock ticker symbol (e.g., 'AAPL', 'TSLA')
        """
        self.ticker = ticker.upper()
        self.data = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
    def analyze_sentiment(self, text: str) -> str:
        """
        Analyze sentiment of text using TextBlob.
        
        Args:
            text: Text to analyze
            
        Returns:
            Sentiment classification: 'positive', 'negative', or 'neutral'
        """
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            
            if polarity > 0.1:
                return 'positive'
            elif polarity < -0.1:
                return 'negative'
            else:
                return 'neutral'
        except Exception as e:
            print(f"Sentiment analysis error: {e}")
            return 'neutral'
    
    def scrape_reddit(self, limit: int = 50) -> List[Dict]:
        """
        Scrape Reddit posts about the ticker from the past month.
        Uses Reddit's JSON API (no authentication required for public posts).
        
        Args:
            limit: Maximum number of posts to retrieve
            
        Returns:
            List of dictionaries containing post data
        """
        results = []
        subreddits = ['wallstreetbets', 'stocks', 'investing', 'StockMarket']
        
        print(f"Scraping Reddit for ${self.ticker}...")
        
        for subreddit in subreddits:
            try:
                # Search Reddit using JSON API
                url = f"https://www.reddit.com/r/{subreddit}/search.json"
                params = {
                    'q': self.ticker,
                    'restrict_sr': 'on',
                    'sort': 'new',
                    'limit': limit // len(subreddits)
                }
                
                response = requests.get(url, headers=self.headers, params=params, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    posts = data.get('data', {}).get('children', [])
                    
                    for post in posts:
                        post_data = post.get('data', {})
                        created_utc = post_data.get('created_utc', 0)
                        created_date = datetime.fromtimestamp(created_utc)
                        
                        # Only include posts from the past month
                        if created_date > datetime.now() - timedelta(days=30):
                            title = post_data.get('title', '')
                            selftext = post_data.get('selftext', '')
                            text = f"{title}. {selftext}"
                            
                            results.append({
                                'source': 'Reddit',
                                'subreddit': subreddit,
                                'title': title,
                                'text': text[:500],  # Limit text length
                                'url': f"https://reddit.com{post_data.get('permalink', '')}",
                                'date': created_date,
                                'sentiment': self.analyze_sentiment(text),
                                'score': post_data.get('score', 0)
                            })
                
                time.sleep(2)  # Rate limiting
                
            except Exception as e:
                print(f"Error scraping r/{subreddit}: {e}")
                continue
        
        print(f"Found {len(results)} Reddit posts")
        return results
    
    def scrape_news_api(self, api_key: str = None) -> List[Dict]:
        """
        Scrape news articles using NewsAPI (requires free API key).
        Get your key at: https://newsapi.org/
        
        Args:
            api_key: NewsAPI key (optional)
            
        Returns:
            List of dictionaries containing article data
        """
        results = []
        
        if not api_key:
            print("No NewsAPI key provided. Skipping news scraping.")
            print("Get a free key at: https://newsapi.org/")
            return results
        
        print(f"Scraping news for ${self.ticker}...")
        
        try:
            url = "https://newsapi.org/v2/everything"
            params = {
                'q': f"{self.ticker} stock OR {self.ticker} shares",
                'from': (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
                'sortBy': 'publishedAt',
                'language': 'en',
                'apiKey': api_key,
                'pageSize': 100
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                articles = data.get('articles', [])
                
                for article in articles:
                    published_at = article.get('publishedAt', '')
                    try:
                        date = datetime.strptime(published_at, '%Y-%m-%dT%H:%M:%SZ')
                    except (ValueError, TypeError) as e:
                        print(f"NewsAPI date parsing error: {e}")
                        date = datetime.now()
                    
                    title = article.get('title', '')
                    description = article.get('description', '')
                    text = f"{title}. {description}"
                    
                    results.append({
                        'source': 'News',
                        'outlet': article.get('source', {}).get('name', 'Unknown'),
                        'title': title,
                        'text': text,
                        'url': article.get('url', ''),
                        'date': date,
                        'sentiment': self.analyze_sentiment(text)
                    })
            else:
                print(f"NewsAPI error: {response.status_code}")
                
        except Exception as e:
            print(f"Error scraping news: {e}")
        
        print(f"Found {len(results)} news articles")
        return results
    
    def scrape_google_finance(self) -> List[Dict]:
        """
        Scrape Google search results for the ticker.
        Note: This is a simplified version. For production, consider using
        Google Custom Search API or other search APIs.
        
        Returns:
            List of dictionaries containing search result data
        """
        results = []
        
        print(f"Scraping Google search results for ${self.ticker}...")
        
        try:
            # Note: Direct Google scraping may be blocked. This is a placeholder.
            # Consider using SerpAPI or Google Custom Search API for production.
            search_query = f"{self.ticker} stock news"
            
            # Placeholder - in production, use an API
            print("Note: Google scraping requires an API for reliable results.")
            print("Consider using SerpAPI or Google Custom Search API.")
            
        except Exception as e:
            print(f"Error scraping Google: {e}")
        
        return results
    
    def scrape_yahoo_finance(self) -> List[Dict]:
        """
        Scrape Yahoo Finance news for the ticker.
        
        Returns:
            List of dictionaries containing Yahoo Finance news
        """
        results = []
        
        print(f"Scraping Yahoo Finance for ${self.ticker}...")
        
        try:
            # Yahoo Finance RSS feed
            url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={self.ticker}&region=US&lang=en-US"
            
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                # Parse RSS feed (basic parsing)
                import xml.etree.ElementTree as ET
                root = ET.fromstring(response.content)
                
                for item in root.findall('.//item'):
                    title_elem = item.find('title')
                    link_elem = item.find('link')
                    pubdate_elem = item.find('pubDate')
                    description_elem = item.find('description')
                    
                    if title_elem is not None:
                        title = title_elem.text or ''
                        description = description_elem.text if description_elem is not None else ''
                        text = f"{title}. {description}"
                        
                        # Parse date
                        try:
                            date_str = pubdate_elem.text if pubdate_elem is not None else ''
                            date = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %z')
                            date = date.replace(tzinfo=None)
                        except (ValueError, TypeError, AttributeError) as e:
                            print(f"RSS feed date parsing error: {e}")
                            date = datetime.now()
                        
                        # Only include items from past month
                        if date > datetime.now() - timedelta(days=30):
                            results.append({
                                'source': 'Yahoo Finance',
                                'title': title,
                                'text': text,
                                'url': link_elem.text if link_elem is not None else '',
                                'date': date,
                                'sentiment': self.analyze_sentiment(text)
                            })
                            
        except Exception as e:
            print(f"Error scraping Yahoo Finance: {e}")
        
        print(f"Found {len(results)} Yahoo Finance articles")
        return results
    
    def scrape_all(self, news_api_key: str = None) -> pd.DataFrame:
        """
        Scrape all sources and return a pandas DataFrame.
        
        Args:
            news_api_key: Optional NewsAPI key for news articles
            
        Returns:
            Pandas DataFrame with all scraped data
        """
        print(f"\n=== Starting scrape for ${self.ticker} ===\n")
        
        all_data = []
        
        # Scrape Reddit
        reddit_data = self.scrape_reddit()
        all_data.extend(reddit_data)
        
        # Scrape Yahoo Finance
        yahoo_data = self.scrape_yahoo_finance()
        all_data.extend(yahoo_data)
        
        # Scrape News (if API key provided)
        if news_api_key:
            news_data = self.scrape_news_api(news_api_key)
            all_data.extend(news_data)
        
        # Create DataFrame
        if all_data:
            df = pd.DataFrame(all_data)
            
            # Sort by date (newest first)
            df = df.sort_values('date', ascending=False)
            
            # Reset index
            df = df.reset_index(drop=True)
            
            print(f"\n=== Scrape complete ===")
            print(f"Total items collected: {len(df)}")
            print(f"\nSentiment breakdown:")
            print(df['sentiment'].value_counts())
            
            return df
        else:
            print("No data collected")
            return pd.DataFrame()


def main():
    """Example usage of the StockDataScraper."""
    
    # Example ticker
    ticker = input("Enter stock ticker (e.g., AAPL, TSLA): ").strip()
    
    if not ticker:
        ticker = "AAPL"
        print(f"Using default ticker: {ticker}")
    
    # Initialize scraper
    scraper = StockDataScraper(ticker)
    
    # Optional: Add your NewsAPI key here
    news_api_key = None  # Get free key at https://newsapi.org/
    
    # Scrape all sources
    df = scraper.scrape_all(news_api_key=news_api_key)
    
    # Display results
    if not df.empty:
        print("\n=== Sample Results ===")
        print(df[['source', 'title', 'date', 'sentiment']].head(10))
        
        # Save to CSV
        output_file = f"{ticker}_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df.to_csv(output_file, index=False)
        print(f"\nData saved to: {output_file}")
        
        # Additional statistics
        print(f"\n=== Statistics ===")
        print(f"Date range: {df['date'].min()} to {df['date'].max()}")
        print(f"\nSources:")
        print(df['source'].value_counts())


if __name__ == "__main__":
    main()
