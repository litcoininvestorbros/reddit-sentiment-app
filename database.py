"""
"""
import psycopg2
from psycopg2 import sql
import utils


def connect_to_database():
    """
    """
    env = utils.load_env_variables()

    conn = psycopg2.connect(
        host = env['DB_SERVER'],
        port = env['DB_PORT'],
        user = env['DB_USER'],
        password = env['DB_PASS'],
        dbname = env['DB_NAME']
    )
    return conn


def create_database() -> None:
    """
    """
    env = utils.load_env_variables()

    def connect_to_db_server():
        conn = psycopg2.connect(
            host = env['DB_SERVER'],
            port = env['DB_PORT'],
            user = env['DB_USER'],
            password = env['DB_PASS']
        )
        return conn

    conn = connect_to_db_server()
    cursor = conn.cursor()

    # Check if the database already exists
    cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (env['DB_NAME'],))
    exists = cursor.fetchone()

    if not exists:
        # Close and reconnect before creating the database
        cursor.close()
        conn.close()

        conn = connect_to_db_server()
        conn.autocommit = True
        cursor = conn.cursor()

        # Create the new database
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(env['DB_NAME'])))
        print(f"Database '{env['DB_NAME']}' created OK")


def create_table(table_name, columns) -> None:
    """
    """
    conn = connect_to_database()
    cursor = conn.cursor()

    # Create the table
    create_table_query = sql.SQL(
        "CREATE TABLE IF NOT EXISTS {} ({})"
    ).format(
        sql.Identifier(table_name),
        sql.SQL(", ").join(
            sql.SQL("{} {}").format(sql.Identifier(col), sql.SQL(col_type))
            for col, col_type in columns.items()
        )
    )
    cursor.execute(create_table_query)
    conn.commit()


def insert_rows(table_name: str, rows_data: list[dict]) -> None:
    """
    """
    # Ensure input `rows_data` is of type list[dict]
    if isinstance(rows_data, dict):
        rows_data = [rows_data]

    conn = connect_to_database()
    cursor = conn.cursor()

    # Insert data into the table
    for row in rows_data:
        columns = row.keys()
        values = [row[col] for col in columns]
        insert_query = sql.SQL(
            "INSERT INTO {} ({}) VALUES ({}) ON CONFLICT (id) DO NOTHING;"
        ).format(
            sql.Identifier(table_name),
            sql.SQL(", ").join(map(sql.Identifier, columns)),
            sql.SQL(", ").join(sql.Placeholder() * len(values))
        )
        cursor.execute(insert_query, values)
        print(row, '\n\n')
    conn.commit()

    cursor.close()
    conn.close()


def initialize_database():
    """Create database and tables in the environment's database
     server instance, if they don't exist.
    """
    # Define tables and data types
    tables = {
        'submissions': {
            'id': 'TEXT PRIMARY KEY',
            'created_utc': 'INTEGER',
            'subreddit': 'TEXT',
            'author_name': 'TEXT',
            'title': 'TEXT',
            'selftext': 'TEXT',
            'url': 'TEXT',
            'num_comments': 'INTEGER',
            'score': 'INTEGER',
            'upvote_ratio': 'FLOAT',
            'sentiment_title_vader': 'FLOAT',
            'sentiment_selftext_vader': 'FLOAT',
            'sentiment_distilroberta': 'FLOAT'
        }
    }

    # Create the new database and its tables
    create_database()
    for table_name, columns in tables.items():
        create_table(table_name, columns)
