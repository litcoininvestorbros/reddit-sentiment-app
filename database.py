"""
"""
import psycopg2
from psycopg2 import sql
from dotenv import dotenv_values


# Load environment variables
env = dotenv_values('.env')

DB_SERVER = env['DB_SERVER']
DB_PORT = env['DB_PORT']
DB_USER = env['DB_USER']
DB_PASS = env['DB_PASS']
DB_NAME = env['DB_NAME']


def connect_to_database():
    """
    """
    conn = psycopg2.connect(
        host = DB_SERVER,
        port = DB_PORT,
        user = DB_USER,
        password = DB_PASS,
        dbname = DB_NAME
    )
    return conn


def create_database() -> None:
    """
    """
    def connect_to_db_server():
        conn = psycopg2.connect(
            host = DB_SERVER,
            port = DB_PORT,
            user = DB_USER,
            password = DB_PASS
        )
        return conn

    conn = connect_to_db_server()

    # Create a cursor object
    cursor = conn.cursor()

    # Check if the database already exists
    cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_NAME,))
    exists = cursor.fetchone()

    if not exists:
        # Close and reconnect before creating the database
        cursor.close()
        conn.close()

        conn = connect_to_db_server()
        conn.autocommit = True
        cursor = conn.cursor()

        # Create the new database
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DB_NAME)))
        print(f"Database '{DB_NAME}' created OK")


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


def insert_row(table_name: str, data: dict) -> None:
    """
    """
    conn = connect_to_database()
    cursor = conn.cursor()

    # Insert data into the table
    for _, row in data.items():
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

    conn.commit()
    cursor.close()
    conn.close()


def initialize_db_and_tables():
    """Create database and tables in local environment,
    if they don't exist.
    """
    create_database()

    # Define tables and columns' data types
    tables = {
        'submissions': {
            "id": "VARCHAR(8) PRIMARY KEY",
            'created_utc': "INTEGER",
            'num_comments': "INTEGER",
            'score': "INTEGER",
            'upvote_ratio': "FLOAT",
            'sentiment': "FLOAT"
        }#,
        #comments': {
        #    "id": "VARCHAR(8) PRIMARY KEY",
        #    'submission_id:
    }
    for table_name, columns in tables.items():
        create_table(table_name, columns)
