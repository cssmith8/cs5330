import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

def connect_to_database() -> mysql.connector.MySQLConnection:
    try:
        load_dotenv()
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None

def create_tables(connection: mysql.connector.MySQLConnection) -> None:
    # TODO
    return

def clear_tables(connection: mysql.connector.MySQLConnection) -> None:
    # TODO
    return

