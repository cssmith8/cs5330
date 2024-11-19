import mysql.connector
from classes import *
from database import *

def main():
    # Create a connection to the database
    connection: mysql.connector.MySQLConnection = connect_to_database()
