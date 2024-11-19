import mysql.connector
from classes import *
from database import *

def main():
    # Create a connection to the database
    connection: mysql.connector.MySQLConnection = connect_to_database()

    if (connection is None):
        print("Failed to connect to the database.")
        return
    else:
        print("Connected to the database.")

    db: Database = Database(connection)

    db.create_tables()


if __name__ == "__main__":
    main()