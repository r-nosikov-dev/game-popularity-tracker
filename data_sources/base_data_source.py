"""Base class for data sources"""
from abc import ABC, abstractmethod
from datetime import datetime, timedelta, timezone
from typing import Dict, Any
import pandas as pd

class BaseDataSource(ABC):
    """@brief Abstract base class for data sources
    @details Defines the interface that all data sources must implement.
             Provides common functionality for date handling.
    """
    
    def __init__(self, name: str, days: int = 30):
        """@brief Initialize the data source
        @param name Name of the data source
        @param days Number of days to analyze
        """
        ## @brief Name of the data source
        self.name = name
        
        ## @brief Number of days to analyze
        self.days = days
        
        ## @brief Data storage dictionary
        self.data = {}
    
    @abstractmethod
    def fetch_data(self, **kwargs) -> Dict[str, Any]:
        """@brief Abstract method for fetching data
        @param kwargs Additional arguments for data fetching
        @return Dictionary containing fetched data
        @retval Dict[str, Any] Data from the source
        """
        pass
    
    @abstractmethod
    def get_statistics(self) -> Dict[str, Any]:
        """@brief Abstract method for getting statistics
        @return Dictionary containing statistical information
        @retval Dict[str, Any] Statistical data
        """
        pass
    
    @abstractmethod
    def format_data(self) -> pd.DataFrame:
        """@brief Abstract method for formatting data
        @return Formatted data as pandas DataFrame
        @retval pd.DataFrame Formatted data
        """
        pass
    
    def get_common_dates(self) -> list:
        """@brief Get list of dates for analysis period
        @return List of date strings in YYYY-MM-DD format
        @retval list[str] Dates for analysis
        """
        end_time = datetime.now(timezone.utc).date()
        dates = [(end_time - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(self.days)]
        return sorted(dates)
    
    def __str__(self):
        """@brief String representation of the object
        @return Class name with source name
        @retval str String representation
        """
        return f"{self.__class__.__name__}(name='{self.name}')"