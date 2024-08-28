"""
"""
import database
import api_fetch


def main():
    """
    """
    target_subreddits = 'Economics+economy+stocks'

    database.initialize_database()

    api_fetch.save_initial_submissions_to_db(target_subreddits)
    api_fetch.save_streamdata_to_db(target_subreddits)


if __name__ == '__main__':
    main()
