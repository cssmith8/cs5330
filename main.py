import mysql.connector
from classes import *
from database import *
from pages import *

from flask import Flask, render_template, request, flash, redirect, url_for, jsonify

class FlaskGlobal:
    db: Database = None

data = FlaskGlobal()

@app.route('/home/process', methods=['POST'])
def process():
    input_data = request.form.get('inputData')
    input_data_2 = request.form.get('inputData2')
    print (data.db.is_connected())
    # Process the data
    result = some_processing_function(input_data)
    result2 = some_processing_function(input_data_2)
    return jsonify({'result': result + result2, 'invalid1': 0})

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
    app.run(debug=True)

if __name__ == "__main__":
    main()