"""Report generation"""
from typing import Dict
import pandas as pd
from models.data_models import DataSourceStats
from config import GAME_NAME

class Reporter:
    """@brief Report generator for data analysis results
    @details Handles generating console output and saving data to files
    """
    
    @staticmethod
    def print_console_table(df: pd.DataFrame, days: int = 30, game_name: str = None):
        """@brief Print data table to console
        @param df DataFrame containing data to display
        @param days Number of days analyzed
        @param game_name Name of the game being analyzed
        """
        if game_name is None:
            game_name = GAME_NAME
            
        print("\n" + "="*80)
        print(f"DYNAMICS OF {game_name.upper()} MENTIONS IN REDDIT (Last {days} days)")
        print("="*80)
        
        # Table header
        print(f"{'Date':<12} {'Steam':<15} {'Reddit':<10} {'Comment'}")
        print("-"*80)
        
        # Data
        if "Reddit Mentions" in df.columns:
            max_mentions = df['Reddit Mentions'].max()
            min_mentions = df['Reddit Mentions'].min()
            avg_mentions = df['Reddit Mentions'].mean()
        else:
            max_mentions = min_mentions = avg_mentions = 0
        
        for _, row in df.iterrows():
            date = row['Date']
            steam = f"{int(row['Steam Subscribers']):,}" if 'Steam Subscribers' in row else "0"
            reddit = int(row['Reddit Mentions']) if 'Reddit Mentions' in row else 0
            
            # Add comments for peaks
            if reddit == max_mentions and max_mentions > 0:
                comment = "Maximum"
            elif reddit >= avg_mentions * 1.5 and reddit > 0:
                comment = "High activity"
            elif reddit == min_mentions:
                comment = "Minimum"
            elif reddit == 0:
                comment = "No mentions"
            else:
                comment = ""
            
            print(f"{date:<12} {steam:<15} {reddit:<10} {comment}")
        
        print("-"*80)
        if "Reddit Mentions" in df.columns:
            print("Statistics:")
            print(f"   Average: {avg_mentions:.1f} mentions/day")
            print(f"   Maximum: {max_mentions} mentions")
            print(f"   Minimum: {min_mentions} mentions")
            print(f"   Total mentions: {df['Reddit Mentions'].sum()}")
        print("="*80)
    
    @staticmethod
    def print_statistics(stats: Dict[str, DataSourceStats]):
        """@brief Print statistics from all data sources
        @param stats Dictionary mapping source names to statistics
        """
        print("\n" + "="*50)
        print("GENERAL STATISTICS")
        print("="*50)
        
        for source_name, stat in stats.items():
            print(f"\n{source_name.upper()}:")
            print(f"   Total count: {stat.total:,}")
            print(f"   Daily average: {stat.average_daily:.1f}")
            print(f"   Daily maximum: {stat.max_daily}")
            print(f"   Daily minimum: {stat.min_daily}")
        
        print("="*50)
    
    @staticmethod
    def save_formatted_csv(df: pd.DataFrame, filename: str = "output.csv", days: int = 30, game_name: str = None):
        """@brief Save data to formatted CSV file
        @param df DataFrame containing data to save
        @param filename Output filename
        @param days Number of days analyzed
        @param game_name Name of the game being analyzed
        """
        if game_name is None:
            game_name = GAME_NAME
            
        # Output settings
        OUTPUT_SETTINGS = {
            "date_width": 12,
            "steam_width": 15,
            "reddit_width": 10,
            "comment_width": 20
        }
        
        # Define column widths
        date_width = OUTPUT_SETTINGS["date_width"]
        steam_width = OUTPUT_SETTINGS["steam_width"]
        reddit_width = OUTPUT_SETTINGS["reddit_width"]
        comment_width = OUTPUT_SETTINGS["comment_width"]
        
        # Create file header
        header_line = (
            f"{'Date':<{date_width}} "
            f"{'Steam':<{steam_width}} "
            f"{'Reddit':<{reddit_width}} "
            f"{'Comment':<{comment_width}}"
        )
        
        separator = "-" * len(header_line)
        
        # Create data rows
        data_lines = []
        for _, row in df.iterrows():
            date = row['Date']
            steam = f"{int(row['Steam Subscribers']):,}" if 'Steam Subscribers' in row else "0"
            reddit = int(row['Reddit Mentions']) if 'Reddit Mentions' in row else 0
            comment = row.get('Comment', '')
            
            line = (
                f"{date:<{date_width}} "
                f"{steam:<{steam_width}} "
                f"{reddit:<{reddit_width}} "
                f"{comment:<{comment_width}}"
            )
            data_lines.append(line)
        
        # Create statistics
        if "Reddit Mentions" in df.columns:
            stats = {
                "avg": df['Reddit Mentions'].mean(),
                "max": df['Reddit Mentions'].max(),
                "min": df['Reddit Mentions'].min(),
                "total": df['Reddit Mentions'].sum()
            }
            
            stats_lines = [
                "",
                "Statistics:",
                f"   Average: {stats['avg']:.1f} mentions/day",
                f"   Maximum: {stats['max']} mentions",
                f"   Minimum: {stats['min']} mentions",
                f"   Total mentions: {stats['total']}",
                f"   Period: Last {days} days"
            ]
        else:
            stats_lines = ["", "Data saved successfully"]
        
        # Save to CSV
        with open(filename, 'w', encoding='utf-8-sig') as f:
            f.write(f"{game_name.upper()} POPULARITY ANALYSIS\n")
            f.write("=" * 60 + "\n")
            f.write(header_line + "\n")
            f.write(separator + "\n")
            for line in data_lines:
                f.write(line + "\n")
            f.write(separator + "\n")
            for line in stats_lines:
                f.write(line + "\n")
            f.write("=" * 60 + "\n")
        
        print(f"\nFormatted table saved to {filename}")
        
        # Also save standard CSV for compatibility
        df.to_csv("data.csv", index=False, encoding='utf-8-sig')
        print("Standard data saved to data.csv")