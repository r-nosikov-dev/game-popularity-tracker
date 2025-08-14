# game-popularity-tracker
Steam and Reddit game popularity analytics tool. Tracks subscriber counts and social mentions for gaming trend analysis.

📊 Description 

Tool for analyzing computer game popularity by tracking: 

    Steam subscriber counts
    Reddit mentions
    Dynamics of changes over a specified period
     

The project collects data from two platforms, combines them by date, and provides analytical information in a convenient format. 

🚀 Features 

    Steam Analysis: Get data on game owner counts
    Reddit Analysis: Search for game mentions in post titles
    Visualization: Dual-axis charts for data comparison
    Reports: Detailed statistics and result tables
    Flexible Configuration: Easily change game and analysis period
     

📦 Requirements 

    Python 3.7 or higher
    Reddit account with API keys

🛠️ Installation 

    Clone the repository: 
    git clone https://github.com/yourusername/game-popularity-tracker.git
    cd game-popularity-tracker

    Install dependencies:
    pip install -r requirements.txt

    Open the .env file and insert your Reddit API keys: 
    REDDIT_CLIENT_ID=your_client_id_here
    REDDIT_CLIENT_SECRET=your_client_secret_here
    REDDIT_USER_AGENT=GamePopularityTracker by YourUsername

▶️ Running

    python main.py

📁 Analysis Results 

After execution, the program creates several files: 
📊 data.csv - Standard format for import 

File with data in standard CSV format, convenient for: 

    Importing to Excel/Google Sheets
    Automatic processing by other programs
    Integration with BI tools
     

📋 output.csv - Formatted report for reading 

File with a beautifully formatted table, convenient for: 

    Direct viewing of results
    Quick analysis of peak values
    Presenting results to colleagues
     

📈 plot.png - Data visualization 

Chart with dual axes: 

    Blue line: Steam subscriber counts
    Red dots: Reddit mentions

🎛️ Configuration Parameters 

Parameters can be changed in the config.py file: 

    GAME_NAME = "Counter-Strike 2"  # Game name for analysis
    STEAM_APP_ID = "730"            # Steam App ID of the game
    DAYS = 30                       # Analysis period in days

📁 Project Structure

game-popularity-tracker/
├── data_sources/     # Data sources (Steam, Reddit)
├── core/            # Core logic (processing, reports, visualization)
├── models/          # Data models
├── config.py        # Project settings
├── main.py          # Entry point
├── requirements.txt # Dependencies
├── .env.example     # Template for API keys
└── README.md        # Documentation

🤝 Architecture 

The project uses an object-oriented approach: 

    Polymorphism: Unified interface for all data sources
    Inheritance: Specific sources inherit from the base class
    Modularity: Clear separation of responsibilities between components
    Extensibility: Easy to add new data sources

📈 Example Output

DYNAMICS OF COUNTER-STRIKE 2 MENTIONS IN REDDIT (Last 30 days)
================================================================================
Date         Steam           Reddit     Comment        
--------------------------------------------------------------------------------
2025-07-15   100,000,000     14         High activity  
2025-07-16   100,000,000     15         High activity  
2025-07-17   100,000,000     6                           
2025-07-30   100,000,000     18         Maximum        
--------------------------------------------------------------------------------
Statistics:
   Average: 6.9 mentions/day
   Maximum: 18 mentions
   Total mentions: 208
================================================================================


     
    
