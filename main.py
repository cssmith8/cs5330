import mysql.connector
from classes import *
from database import *
from routes import *
from tests import tests
from data import Data

def main():
    Data._instance.db.create_tables()
    Data._instance.db.clear_tables()
    app.run(debug=False)

if __name__ == "__main__":
    testing: bool = True # Change to True to run tests
    data: Data = Data()
    connection: mysql.connector.MySQLConnection = connect_to_database()
    if (connection is None):
        print("Failed to connect to the database.")
        exit()
    else:
        print("Connected to the database.")
    Data._instance.db = Database(connection)
    if testing:
        tests(Data._instance.db)
    else:
        main()
