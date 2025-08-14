"""Main application file"""
import os
from dotenv import load_dotenv
from data_sources.steam_source import SteamDataSource
from data_sources.reddit_source import RedditDataSource
from core.data_processor import DataProcessor
from core.reporter import Reporter
from core.visualizer import Visualizer
from config import GAME_NAME, STEAM_APP_ID, DAYS, REDDIT_CONFIG

def load_environment():
    """@brief Load environment variables from .env file
    @details Reads Reddit API credentials from environment variables
    """
    load_dotenv()
    
    # Update Reddit configuration
    REDDIT_CONFIG["client_id"] = os.getenv("REDDIT_CLIENT_ID", "")
    REDDIT_CONFIG["client_secret"] = os.getenv("REDDIT_CLIENT_SECRET", "")
    REDDIT_CONFIG["user_agent"] = os.getenv("REDDIT_USER_AGENT", "SteamAnalyticsBot by User")

def main():
    """@brief Main application entry point
    @details Orchestrates the entire data analysis process:
             1. Loads configuration
             2. Creates data sources
             3. Fetches data
             4. Processes and combines data
             5. Generates reports
             6. Creates visualizations
    """
    print("Starting data analysis...")
    
    # Load environment variables
    load_environment()
    
    # Create data sources
    steam_source = SteamDataSource(name="Steam", days=DAYS, app_id=STEAM_APP_ID)
    reddit_source = RedditDataSource(name="Reddit", days=DAYS, game_name=GAME_NAME)
    
    # Set Reddit credentials
    if REDDIT_CONFIG["client_id"]:
        reddit_source.set_credentials(
            REDDIT_CONFIG["client_id"],
            REDDIT_CONFIG["client_secret"],
            REDDIT_CONFIG["user_agent"]
        )
    
    # Create data processor
    processor = DataProcessor()
    processor.add_data_source(steam_source)
    processor.add_data_source(reddit_source)
    
    # Fetch data (polymorphic interface)
    print("Fetching data from all sources...")
    data = processor.fetch_all_data()
    
    # Get statistics (polymorphic interface)
    print("Getting statistics...")
    stats = processor.get_all_statistics()
    if stats:
        Reporter.print_statistics(stats)
    
    # Combine data
    print("Combining data...")
    try:
        combined_df = processor.combine_data()
        combined_df = processor.add_comments(combined_df)
    except Exception as e:
        print(f"Error combining  {e}")
        return
    
    # Generate reports
    print("Generating reports...")
    Reporter.print_console_table(combined_df, DAYS, GAME_NAME)
    Reporter.save_formatted_csv(combined_df, "output.csv", DAYS, GAME_NAME)
    
    # Visualization
    print("Creating plots...")
    Visualizer.create_plot(combined_df, GAME_NAME, "plot.png")
    
    print("Analysis completed!")

if __name__ == "__main__":
    main()