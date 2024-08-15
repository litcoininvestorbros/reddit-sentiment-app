import psycopg2
from psycopg2 import sql
from dotenv import dotenv_values


# Load environment variables
env = dotenv_values('./.env')

# Replace these values with your actual database credentials
host = env['DB_SERVER']
port = 5432
user = env['DB_USER']
password = env['DB_PASS']


def conection():
    config = {'user':{user},
            'password':f'{password}',
            'host':'127.0.0.1',
            'port':'5432',
            'dbname':'reddit',
            'autocommit':True} #this resolve the problem "InternalError: CREATE DATABASE cannot run inside a transaction block"
    try:
        cnx = psycopg2.connect(**config)
    except psycopg2.Error as err:
        print(err)
        exit(1)
    else:
        return cnx

conection()