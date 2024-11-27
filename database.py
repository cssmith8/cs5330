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

    def is_connected(self) -> bool:
        if self.connection is None:
            return False
        return self.connection.is_connected()
    
    def create_tables(self) -> None:
        cursor = self.connection.cursor()
        try:
            # Create Degree table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS Degree (
                DegreeName VARCHAR(255),
                DegreeLevel VARCHAR(255),
                PRIMARY KEY (DegreeName, DegreeLevel)
            )
            """)

            # Create Course table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS Course (
                CourseID VARCHAR(255) PRIMARY KEY,
                CourseName VARCHAR(255)
            )
            """)

            # Create Degree_Course table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS Degree_Course (
                DegreeName VARCHAR(255),
                DegreeLevel VARCHAR(255),
                CourseID VARCHAR(255),
                IsCore BOOLEAN,
                PRIMARY KEY (DegreeName, DegreeLevel, CourseID),
                FOREIGN KEY (DegreeName, DegreeLevel) REFERENCES Degree(DegreeName, DegreeLevel),
                FOREIGN KEY (CourseID) REFERENCES Course(CourseID)
            )
            """)

            # Create Goal table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS Goal (
                GoalCode VARCHAR(255),
                DegreeName VARCHAR(255),
                DegreeLevel VARCHAR(255),
                Description TEXT,
                PRIMARY KEY (GoalCode, DegreeName, DegreeLevel),
                FOREIGN KEY (DegreeName, DegreeLevel) REFERENCES Degree(DegreeName, DegreeLevel)
            )
            """)

            # Create Goal_Course table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS Goal_Course (
                GoalCode VARCHAR(255),
                DegreeName VARCHAR(255),
                DegreeLevel VARCHAR(255),
                CourseID VARCHAR(255),
                PRIMARY KEY (GoalCode, DegreeName, DegreeLevel, CourseID),
                FOREIGN KEY (GoalCode, DegreeName, DegreeLevel) REFERENCES Goal(GoalCode, DegreeName, DegreeLevel),
                FOREIGN KEY (CourseID) REFERENCES Course(CourseID)
            )
            """)

            # Create Instructor table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS Instructor (
                InstructorID VARCHAR(255) PRIMARY KEY,
                InstructorName VARCHAR(255)
            )
            """)

            # Create Section table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS Section (
                SectionID VARCHAR(255),
                CourseID VARCHAR(255),
                Semester VARCHAR(255),
                Year INT,
                NumStudents INT,
                InstructorID VARCHAR(255),
                PRIMARY KEY (SectionID, CourseID, Semester, Year),
                FOREIGN KEY (CourseID) REFERENCES Course(CourseID),
                FOREIGN KEY (InstructorID) REFERENCES Instructor(InstructorID)
            )
            """)

            # Create Evaluation table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS Evaluation (
                GoalCode VARCHAR(255),
                DegreeName VARCHAR(255),
                DegreeLevel VARCHAR(255),
                SectionID VARCHAR(255),
                CourseID VARCHAR(255),
                Semester VARCHAR(255),
                Year INT,
                EvaluationType VARCHAR(255),
                A INT,
                B INT,
                C INT,
                F INT,
                ImprovementSuggestion TEXT,
                PRIMARY KEY (GoalCode, DegreeName, DegreeLevel, SectionID, CourseID, Semester, Year),
                FOREIGN KEY (GoalCode, DegreeName, DegreeLevel) REFERENCES Goal(GoalCode, DegreeName, DegreeLevel),
                FOREIGN KEY (SectionID, CourseID, Semester, Year) REFERENCES Section(SectionID, CourseID, Semester, Year)
            )
            """)

            self.connection.commit()
            print("Tables created successfully.")
        except Error as e:
            print(f"Error creating tables: {e}")
            self.connection.rollback()
        finally:
            cursor.close()

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
    
    # gets all degree courses from the database given degreeName and degreeLevel
    def get_degree_courses_from_degree(self, degreeName: str, degreeLevel: str) -> list[DegreeCourse]:
        # TODO
        return None
    
    # gets all degree courses from the database given courseID
    def get_degree_courses_from_course(self, courseID: str) -> list[DegreeCourse]:
        # TODO
        return None
    
    # gets all goals from the database given degreeName and degreeLevel
    def get_goals_from_degree(self, degreeName: str, degreeLevel: str) -> list[Goal]:
        # TODO
        return None
    
    # gets all goal courses from the database given goalCode, degreeName, and degreeLevel
    def get_goal_courses_from_goal(self, goalCode: str, degreeName: str, degreeLevel: str) -> list[GoalCourse]:
        # TODO
        return None
    
    # gets all goal courses from the database given courseID
    def get_goal_courses_from_course(self, courseID: str) -> list[GoalCourse]:
        # TODO
        return None
    
    # get all sections from the database given courseID
    def get_sections_from_course(self, courseID: str) -> list[Section]:
        # TODO
        return None
    
    # get all sections from the database given instructorID
    def get_sections_from_instructor(self, instructorID: str) -> list[Section]:
        # TODO
        return None
    
    # get all evaluations from the database given goalCode, DegreeName, and DegreeLevel
    def get_evaluations_from_goal(self, goalCode: str, degreeName: str, degreeLevel: str) -> list[Evaluation]:
        # TODO
        return None
    
    # get all evaluations from the database given SectionID, CourseID, Semester, and Year
    def get_evaluations_from_section(self, sectionID: str, courseID: str, semester: str, year: int) -> list[Evaluation]:
        # TODO
        return None
    