""" Data model definitions """
from dataclasses import dataclass
from typing import Dict, Any
from datetime import datetime

@dataclass
class DataSourceStats:
    """@brief Statistics for a data source
    @details Contains statistical information about data from a specific source
    """
    
    ## @brief Total count of items
    total: int
    
    ## @brief Average daily count
    average_daily: float
    
    ## @brief Maximum daily count
    max_daily: int
    
    ## @brief Minimum daily count
    min_daily: int
    
    ## @brief Name of the data source
    data_source: str
    
    ## @brief Timestamp of when statistics were calculated
    timestamp: datetime = None
    
    def __post_init__(self):
        """@brief Post-initialization method
        @details Sets timestamp if not provided
        """
        if self.timestamp is None:
            self.timestamp = datetime.now()

@dataclass
class CombinedData:
    """@brief Combined data from multiple sources
    @details Represents data points that combine information from different sources
    """
    
    ## @brief Date of the data point
    date: str
    
    ## @brief Number of Steam subscribers
    steam_subscribers: int
    
    ## @brief Number of Reddit mentions
    reddit_mentions: int
    
    ## @brief Optional comment about the data point
    comment: str = ""