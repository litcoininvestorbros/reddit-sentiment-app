"""
"""
import database
import reddit_api


def main():
    """
    """
    database.initialize_db_and_tables()
    reddit_api.run_data_collection('Economics+economy')


if __name__ == '__main__':
    main()
