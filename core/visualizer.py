"""Data visualization"""
import matplotlib.pyplot as plt
import pandas as pd

class Visualizer:
    """@brief Data visualizer for creating plots and charts
    @details Handles creation of visual representations of the analyzed data
    """
    
    @staticmethod
    def create_plot(df: pd.DataFrame, game_name: str = "Counter-Strike 2", filename: str = "plot.png"):
        """@brief Create plot with dual axes showing Steam subscribers and Reddit mentions
        @param df DataFrame containing data to plot
        @param game_name Name of the game being analyzed
        @param filename Output filename for the plot
        """
        if 'Date' not in df.columns:
            print("No data for plotting")
            return
            
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Create figure and axes
        fig, ax1 = plt.subplots(figsize=(14, 7))
        
        # Main line - Steam subscribers
        if 'Steam Subscribers' in df.columns:
            ax1.plot(df['Date'], df['Steam Subscribers'], 
                     label="Steam Subscribers", color="blue", linewidth=2)
            ax1.set_ylabel("Steam Subscribers", color="blue")
            ax1.tick_params(axis='y', labelcolor="blue")
            
            # Format Y axis for subscribers
            ax1.yaxis.set_major_formatter(lambda x, pos: f"{int(x):,}")
            
            # Set fixed range for Y axis of subscribers
            steam_values = df['Steam Subscribers']
            min_val = steam_values.min()
            max_val = steam_values.max()
            margin = (max_val - min_val) * 0.1 if max_val != min_val else 1000000
            ax1.set_ylim(min_val - margin, max_val + margin)
        
        # Second axis - Reddit mentions
        ax2 = ax1.twinx()
        if 'Reddit Mentions' in df.columns:
            scatter = ax2.scatter(df['Date'], df['Reddit Mentions'], 
                                 label="Reddit Mentions", color="red", s=60, alpha=0.7)
            
            # Add annotations for Reddit mentions
            for _, row in df.iterrows():
                if row['Reddit Mentions'] > 0:  # Only for non-zero values
                    ax2.annotate(str(row['Reddit Mentions']), 
                                (row['Date'], row['Reddit Mentions']),
                                xytext=(5, 5), textcoords='offset points',
                                fontsize=8, alpha=0.7)
            
            ax2.set_ylabel("Reddit Mentions", color="red")
            ax2.tick_params(axis='y', labelcolor="red")
        
        # Plot settings
        plt.title(f"Data dynamics of subscribers and mentions for game {game_name}", fontsize=16)
        fig.legend(loc="upper right", bbox_to_anchor=(0.85, 0.85), fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45, fontsize=10)
        plt.tight_layout()
        plt.savefig(filename, dpi=300)
        print(f"Plot saved to {filename}")