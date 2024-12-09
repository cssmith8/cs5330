import mysql.connector
from classes import *
from database import *
from routes import *
from tests import tests
from data import Data

def main():
    Data._instance.db.create_tables()
    Data._instance.db.clear_tables()
    add_sample_data: bool = False
    if add_sample_data:
        Data._instance.db.insert_degree(Degree("Computer Science", "BS"))
        Data._instance.db.insert_course(Course("CS5330", "Databases"))
        Data._instance.db.insert_degree_course(DegreeCourse("Computer Science", "BS", "CS5330", True))
        Data._instance.db.insert_goal(Goal("G123", "Computer Science", "BS", "Goal_Desc"))
        Data._instance.db.insert_goal_course(GoalCourse("G123", "Computer Science", "BS", "CS5330"))
        Data._instance.db.insert_instructor(Instructor("I2345678", "Abc Def"))
        Data._instance.db.insert_section(Section("801", "CS5330", "Fall", 2024, 10, "I2345678"))
    app.run(debug=False)

if __name__ == "__main__":
    testing: bool = False # Change to True to run tests
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
