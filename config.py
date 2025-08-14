"""Project configuration settings"""
import os

## @brief Game name for analysis
GAME_NAME = "Counter-Strike 2"

## @brief Steam App ID for the game
STEAM_APP_ID = "730"

## @brief Number of days to analyze
DAYS = 30

## @brief Reddit API configuration dictionary
## @details Will be populated from environment variables
REDDIT_CONFIG = {
    "client_id": "",
    "client_secret": "",
    "user_agent": "SteamAnalyticsBot by User"
}