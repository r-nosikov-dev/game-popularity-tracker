"""Processing data from various sources"""
import pandas as pd
from typing import List, Dict, Any
from data_sources.base_data_source import BaseDataSource
from models.data_models import DataSourceStats

class DataProcessor:
    """@brief Data processor for combining data from multiple sources
    @details Handles fetching, combining, and processing data from various sources
    """
    
    def __init__(self):
        """@brief Initialize data processor"""
        ## @brief List of data sources to process
        self.data_sources = []
    
    def add_data_source(self, source: BaseDataSource):
        """@brief Add a data source to the processor
        @param source Data source to add
        """
        self.data_sources.append(source)
    
    def fetch_all_data(self, **kwargs) -> Dict[str, Any]:
        """@brief Fetch data from all registered sources
        @param kwargs Additional arguments to pass to data sources
        @return Dictionary mapping source names to their data
        @retval Dict[str, Any] Data from all sources
        """
        results = {}
        for source in self.data_sources:
            print(f"Fetching data from {source.name}...")
            results[source.name] = source.fetch_data(**kwargs)
        return results
    
    def get_all_statistics(self) -> Dict[str, DataSourceStats]:
        """@brief Get statistics from all registered sources
        @details Uses polymorphic interface to get statistics from all sources
        @return Dictionary mapping source names to their statistics
        @retval Dict[str, DataSourceStats] Statistics from all sources
        """
        stats = {}
        for source in self.data_sources:
            source_stats = source.get_statistics()
            if "error" not in source_stats:
                stats[source.name] = DataSourceStats(**source_stats)
        return stats
    
    def combine_data(self) -> pd.DataFrame:
        """@brief Combine data from all registered sources
        @return Combined data as pandas DataFrame
        @retval pd.DataFrame Combined data with all source information
        @exception ValueError If fewer than 2 sources are registered
        """
        if len(self.data_sources) < 2:
            raise ValueError("At least 2 data sources needed for combination")
        
        # Get data from first source (as base)
        base_df = self.data_sources[0].format_data()
        
        # Add data from other sources
        for source in self.data_sources[1:]:
            source_df = source.format_data()
            if not source_df.empty:
                base_df = pd.merge(base_df, source_df, on="Date", how="outer")
        
        # Fill missing values with zeros
        base_df = base_df.fillna(0)
        
        return base_df
    
    def add_comments(self, df: pd.DataFrame) -> pd.DataFrame:
        """@brief Add comments to combined data based on analysis
        @param df Input DataFrame with combined data
        @return DataFrame with added comments column
        @retval pd.DataFrame DataFrame with comments
        """
        if "Reddit Mentions" not in df.columns:
            return df
            
        df_with_comments = df.copy()
        
        max_mentions = df['Reddit Mentions'].max()
        min_mentions = df['Reddit Mentions'].min()
        avg_mentions = df['Reddit Mentions'].mean()
        
        comments = []
        for _, row in df.iterrows():
            reddit_val = row['Reddit Mentions']
            
            if reddit_val == max_mentions and max_mentions > 0:
                comment = "Maximum"
            elif reddit_val >= avg_mentions * 1.5 and reddit_val > 0:
                comment = "High activity"
            elif reddit_val == min_mentions:
                comment = "Minimum"
            elif reddit_val == 0:
                comment = "No mentions"
            else:
                comment = ""
            
            comments.append(comment)
        
        df_with_comments['Comment'] = comments
        return df_with_comments