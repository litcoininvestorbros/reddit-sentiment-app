"""
"""
import database
import api_fetch
import utils


def main():
    """
    """
    utils.load_env_variables()
    database.initialize_database()

    target_subreddits = 'Economics+economy+stocks+StockMarket'
    api_fetch.fetch_paginated_to_db(target_subreddits)
    api_fetch.fetch_stream_to_db(target_subreddits)


if __name__ == '__main__':
    main()
