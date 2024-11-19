import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
from classes import *


def connect_to_database() -> mysql.connector.MySQLConnection:
    try:
        if (not load_dotenv()):
            print("Could not load .env file.")
            return None
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

class Database:
    # connection: mysql.connector.MySQLConnection
    def __init__(self, connection: mysql.connector.MySQLConnection):
        self.connection: mysql.connector.MySQLConnection = connection
    
    def create_tables(self) -> None:
        # TODO
        return 

    def clear_tables(self) -> None:
        # TODO
        return

    # Inserts a degree into the database
    def insert_degree(self, degree: Degree) -> None:
        # TODO
        return

    # Inserts a degree course into the database
    def insert_degree_course(self, degreeCourse: DegreeCourse) -> None:
        # TODO
        return

    # Inserts a course into the database
    def insert_course(self, course: Course) -> None:
        # TODO
        return

    # Inserts a section into the database
    def insert_section(self, section: Section) -> None:
        # TODO
        return

    # Inserts an instructor into the database
    def insert_instructor(self, instructor: Instructor) -> None:
        # TODO
        return

    # Inserts a goal into the database
    def insert_goal(self, goal: Goal) -> None:
        # TODO
        return

    # Inserts a goal course into the database
    def insert_goal_course(self, goalCourse: GoalCourse) -> None:
        # TODO
        return

    # Inserts an evaluation into the database
    def insert_evaluation(self, evaluation: Evaluation) -> None:
        # TODO
        return

    # gets a degree from the database given all the key attributes
    def get_degree(self, degreeName: str, degreeLevel: str) -> Degree:
        # TODO
        return None

    # gets a degree course from the database given all the key attributes
    def get_degree_course(self, degreeName: str, degreeLevel: str, courseID: int) -> DegreeCourse:
        # TODO
        return None

    # gets a course from the database given all the key attributes
    def get_course(self, courseID: str) -> Course:
        # TODO
        return None

    # gets a section from the database given all the key attributes
    def get_section(self, sectionID: str, courseID: str, semester: str, year: int) -> Section:
        # TODO
        return None

    # gets an instructor from the database given all the key attributes
    def get_instructor(self, instructorID: str) -> Instructor:
        # TODO
        return None

    # gets a goal from the database given all the key attributes
    def get_goal(self, goalCode: str, degreeName: str, degreeLevel: str) -> Goal:
        # TODO
        return None

    # gets a goal course from the database given all the key attributes
    def get_goal_course(self, goalCode: str, degreeName: str, degreeLevel: str, courseID: str) -> GoalCourse:
        # TODO
        return None

    # gets an evaluation from the database given all the key attributes
    def get_evaluation(self, goalCode: str, degreeName: str, degreeLevel: str, sectionID: str, courseID: str, semester: str, year: int) -> Evaluation:
        # TODO
        return None