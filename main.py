import mysql.connector
from classes import *
from database import *
from pages import *
from tests import tests

from flask import Flask, render_template, request, flash, redirect, url_for, jsonify

class FlaskGlobal:
    db: Database = None

data = FlaskGlobal()

@app.route('/home/process', methods=['POST'])
def process():
    input_data = request.form.get('inputData')
    input_data_2 = request.form.get('inputData2')
    input_data_3 = request.form.get('dropdown')
    print (input_data_3)
    # Process the data
    result = some_processing_function(input_data)
    result2 = some_processing_function(input_data_2)
    return jsonify({'result': result + " " + result2, 'invalid1': 0})

def some_processing_function(input_data) -> str:
    # Example processing function
    print(f"Processing data: {input_data}")
    return f"Processed data: {data.db.is_connected()}"

def main():
    # Create a connection to the database
    connection: mysql.connector.MySQLConnection = connect_to_database()
    if (connection is None):
        print("Failed to connect to the database.")
        return
    else:
        print("Connected to the database.")
    data.db = Database(connection)
    data.db.create_tables()
    data.db.clear_tables()
    app.run(debug=False)

def runTests():
    connection: mysql.connector.MySQLConnection = connect_to_database()
    if (connection is None):
        print("Failed to connect to the database.")
        return
    else:
        print("Connected to the database.")
    data.db = Database(connection)
    tests(data.db)

if __name__ == "__main__":
    testing: bool = True # Change to True to run tests
    if testing:
        runTests()
    else:
        main()
