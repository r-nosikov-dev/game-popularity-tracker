"""Reddit data source"""
import praw
from datetime import datetime, timedelta, timezone
from typing import Dict, Any
import pandas as pd
from data_sources.base_data_source import BaseDataSource

class RedditDataSource(BaseDataSource):
    """@brief Reddit data source implementation
    @details Fetches mention data from Reddit API for a specific game
    """
    
    def __init__(self, name: str = "Reddit", days: int = 30, game_name: str = "Counter-Strike 2"):
        """@brief Initialize Reddit data source
        @param name Name of the data source
        @param days Number of days to analyze
        @param game_name Name of the game to search for
        """
        super().__init__(name, days)
        
        ## @brief Name of the game to search for
        self.game_name = game_name
        
        ## @brief Reddit API client instance
        self.reddit_client = None
        
        ## @brief Reddit API configuration
        self.reddit_config = {
            "client_id": "",
            "client_secret": "",
            "user_agent": "SteamAnalyticsBot by User"
        }
    
    def set_credentials(self, client_id: str, client_secret: str, user_agent: str):
        """@brief Set Reddit API credentials
        @param client_id Reddit API client ID
        @param client_secret Reddit API client secret
        @param user_agent User agent string for API requests
        """
        self.reddit_config = {
            "client_id": client_id,
            "client_secret": client_secret,
            "user_agent": user_agent
        }
    
    def _get_reddit_client(self):
        """@brief Get Reddit API client instance
        @return Reddit API client
        @retval praw.Reddit Reddit client instance
        """
        if not self.reddit_client:
            self.reddit_client = praw.Reddit(
                client_id=self.reddit_config["client_id"],
                client_secret=self.reddit_config["client_secret"],
                user_agent=self.reddit_config["user_agent"]
            )
        return self.reddit_client
    
    def fetch_data(self, game_name: str = None, **kwargs) -> Dict[str, Any]:
        """@brief Fetch mention data from Reddit
        @param game_name Name of the game to search for (optional)
        @param kwargs Additional arguments (not used)
        @return Dictionary containing mention data
        @retval Dict[str, Any] Mention data including mentions count and daily data
        """
        game_name = game_name or self.game_name
        if not game_name:
            raise ValueError("Game name not specified for search")
        
        if not self.reddit_config["client_id"]:
            print("[Reddit] Reddit API credentials not set")
            return {"mentions": {}, "daily_data": {}, "total": 0}
        
        try:
            reddit = self._get_reddit_client()
            end_time = datetime.now(timezone.utc)
            start_time = end_time - timedelta(days=self.days)

            # Initialize all days with 0
            mentions = {}
            current = start_time
            while current <= end_time:
                mentions[current.date()] = 0
                current += timedelta(days=1)

            query = f"title:{game_name}"
            results = reddit.subreddit("all").search(query, sort="new", limit=1000)

            for post in results:
                post_time = datetime.fromtimestamp(post.created_utc, tz=timezone.utc)
                post_date = post_time.date()
                if post_date in mentions:
                    mentions[post_date] += 1

            # Convert dates to strings
            self.data = {
                date.strftime('%Y-%m-%d'): count 
                for date, count in mentions.items()
            }
            
            total_mentions = sum(mentions.values())
            print(f"[Reddit] Found {total_mentions} mentions in {self.days} days")
            
            return {"mentions": mentions, "daily_data": self.data, "total": total_mentions}
            
        except Exception as e:
            print(f"[Reddit] Error fetching data: {e}")
            return {"mentions": {}, "daily_data": {}, "total": 0}
    
    def get_statistics(self) -> Dict[str, Any]:
        """@brief Get statistics for Reddit data
        @return Dictionary containing statistical information
        @retval Dict[str, Any] Statistics including total, average, min, max values
        """
        if not self.data:
            return {"error": "No data for analysis"}
        
        values = list(self.data.values())
        return {
            "total": sum(values),
            "average_daily": sum(values) / len(values) if values else 0,
            "max_daily": max(values) if values else 0,
            "min_daily": min(values) if values else 0,
            "data_source": self.name
        }
    
    def format_data(self) -> pd.DataFrame:
        """@brief Format Reddit data into DataFrame
        @return Formatted data as pandas DataFrame
        @retval pd.DataFrame DataFrame with Date and Reddit Mentions columns
        """
        if not self.data:
            return pd.DataFrame()
        
        dates = self.get_common_dates()
        rows = []
        for date in dates:
            rows.append({
                "Date": date,
                "Reddit Mentions": self.data.get(date, 0)
            })
        
        return pd.DataFrame(rows)