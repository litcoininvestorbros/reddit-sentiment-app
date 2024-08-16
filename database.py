import psycopg2
from psycopg2 import sql
from dotenv import dotenv_values


# Load environment variables
env = dotenv_values('./.env')

# Replace these values with your actual database credentials
DB_SERVER = env['DB_SERVER']
DB_PORT = 5432
DB_USER = env['DB_USER']
DB_PASS = env['DB_PASS']


def create_database():
    # Connect to the PostgreSQL server
    conn = psycopg2.connect(
        host=DB_SERVER,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASS
    )

    # Create a cursor object
    cursor = conn.cursor()

    # Define the new database name
    new_db_name = "reddit_3"

    # Check if the database already exists
    cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (new_db_name,))
    exists = cursor.fetchone()

    if not exists:
        # Close the cursor and connection before creating the database
        cursor.close()
        conn.close()

        # Reconnect to the server without a transaction block
        conn = psycopg2.connect(
            host=DB_SERVER,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASS
        )
        conn.autocommit = True  # Enable autocommit mode
        cursor = conn.cursor()

        # Create the new database
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(new_db_name)))
        print(f"Database '{new_db_name}' created successfully.")


def create_table():
    # Reconnect to the new database to create the table and insert data
    conn = psycopg2.connect(
        host=DB_SERVER,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASS,
        dbname='reddit_3'
    )
    cursor = conn.cursor()

    # Define the table name and columns
    table_name = "sentiment"
    columns = {
        "id": "VARCHAR(255)",
        'created_utc': "FLOAT",
        'num_comments': "INTEGER",
        'score': "INTEGER",
        'upvote_ratio': "FLOAT",
        'sentiment': "FLOAT"
    }

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


def insert_data(table_name, data: dict):
    # Reconnect to the new database to create the table and insert data
    conn = psycopg2.connect(
        host=DB_SERVER,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASS,
        dbname='reddit_3'
    )
    cursor = conn.cursor()
    
    # Insert data into the table
    for _, row in data.items():
        columns = row.keys()
        values = [row[col] for col in columns]
        insert_query = sql.SQL(
            "INSERT INTO {} ({}) VALUES ({})"
        ).format(
            sql.Identifier(table_name),
            sql.SQL(", ").join(map(sql.Identifier, columns)),
            sql.SQL(", ").join(sql.Placeholder() * len(values))
        )
        cursor.execute(insert_query, values)

    # Commit the changes
    conn.commit()

    # Close the cursor and connection
    cursor.close()
    conn.close()

    ##  DEBUG print("Data inserted successfully.")