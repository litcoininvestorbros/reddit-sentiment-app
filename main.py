"""
"""
import database
import api_fetch


def main():
    """
    """
    database.initialize_database()
    api_fetch.save_streamdata_to_db('Economics+economy+stocks')


if __name__ == '__main__':
    main()
