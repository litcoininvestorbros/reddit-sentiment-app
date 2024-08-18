import database
import reddit_api


if __name__ == '__main__':
    
    # Create database and table, if it they don't exists
    database.create_database()
    database.create_table('sentiment')

    # Run Reddit API data collection
    reddit_api.run_data_collection('WallStreetBets')

