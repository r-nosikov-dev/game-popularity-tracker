"""Steam data source"""
import requests
from datetime import datetime, timedelta, timezone
from typing import Dict, Any
import pandas as pd
from data_sources.base_data_source import BaseDataSource

class SteamDataSource(BaseDataSource):
    """@brief Steam data source implementation
    @details Fetches subscriber data from SteamSpy API for a specific game
    """
    
    def __init__(self, name: str = "Steam", days: int = 30, app_id: str = "730"):
        """@brief Initialize Steam data source
        @param name Name of the data source
        @param days Number of days to analyze
        @param app_id Steam App ID for the game
        """
        super().__init__(name, days)
        
        ## @brief Steam App ID for the game
        self.app_id = app_id
        
        ## @brief Number of subscribers
        self.subscribers = 0
    
    def fetch_data(self, **kwargs) -> Dict[str, Any]:
        """@brief Fetch subscriber data from SteamSpy
        @param kwargs Additional arguments (not used)
        @return Dictionary containing subscriber data
        @retval Dict[str, Any] Subscriber data including total count and daily data
        """
        url = f"https://steamspy.com/api.php?request=appdetails&appid={self.app_id}"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Get concrete number instead of range
            owners = data.get("owners", 0)
            if " .. " in str(owners):
                self.subscribers = int(owners.replace(",", "").split(" .. ")[0])
            else:
                self.subscribers = int(owners)
            
            print(f"[Steam] Approximate number of owners: {self.subscribers:,}")
            
            # Create dictionary with same value for all dates
            dates = self.get_common_dates()
            self.data = {date: self.subscribers for date in dates}
            
            return {"subscribers": self.subscribers, "daily_data": self.data}
            
        except Exception as e:
            print(f"[Steam] Error fetching data: {e}")
            return {"subscribers": 0, "daily_data": {}}
    
    def get_statistics(self) -> Dict[str, Any]:
        """@brief Get statistics for Steam data
        @return Dictionary containing statistical information
        @retval Dict[str, Any] Statistics including total, average, min, max values
        """
        if not self.data:
            return {"error": "No data for analysis"}
        
        return {
            "total": self.subscribers,
            "average_daily": self.subscribers,
            "min_daily": self.subscribers,
            "max_daily": self.subscribers,
            "data_source": self.name
        }
    
    def format_data(self) -> pd.DataFrame:
        """@brief Format Steam data into DataFrame
        @return Formatted data as pandas DataFrame
        @retval pd.DataFrame DataFrame with Date and Steam Subscribers columns
        """
        if not self.data:
            return pd.DataFrame()
        
        dates = self.get_common_dates()
        rows = []
        for date in dates:
            rows.append({
                "Date": date,
                "Steam Subscribers": self.data.get(date, 0)
            })
        
        return pd.DataFrame(rows)