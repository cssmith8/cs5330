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
                DegreeName VARCHAR(64),
                DegreeLevel VARCHAR(64),
                PRIMARY KEY (DegreeName, DegreeLevel)
            )
            """)

            # Create Course table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS Course (
                CourseID VARCHAR(64) PRIMARY KEY,
                CourseName VARCHAR(64)
            )
            """)

            # Create Degree_Course table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS Degree_Course (
                DegreeName VARCHAR(64),
                DegreeLevel VARCHAR(64),
                CourseID VARCHAR(64),
                IsCore BOOLEAN,
                PRIMARY KEY (DegreeName, DegreeLevel, CourseID),
                FOREIGN KEY (DegreeName, DegreeLevel) REFERENCES Degree(DegreeName, DegreeLevel),
                FOREIGN KEY (CourseID) REFERENCES Course(CourseID)
            )
            """)

            # Create Goal table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS Goal (
                GoalCode VARCHAR(64),
                DegreeName VARCHAR(64),
                DegreeLevel VARCHAR(64),
                Description TEXT,
                PRIMARY KEY (GoalCode, DegreeName, DegreeLevel),
                FOREIGN KEY (DegreeName, DegreeLevel) REFERENCES Degree(DegreeName, DegreeLevel)
            )
            """)

            # Create Goal_Course table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS Goal_Course (
                GoalCode VARCHAR(64),
                DegreeName VARCHAR(64),
                DegreeLevel VARCHAR(64),
                CourseID VARCHAR(64),
                PRIMARY KEY (GoalCode, DegreeName, DegreeLevel, CourseID),
                FOREIGN KEY (GoalCode, DegreeName, DegreeLevel) REFERENCES Goal(GoalCode, DegreeName, DegreeLevel),
                FOREIGN KEY (CourseID) REFERENCES Course(CourseID)
            )
            """)

            # Create Instructor table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS Instructor (
                InstructorID VARCHAR(64) PRIMARY KEY,
                InstructorName VARCHAR(64)
            )
            """)

            # Create Section table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS Section (
                SectionID VARCHAR(64),
                CourseID VARCHAR(64),
                Semester VARCHAR(64),
                Year INT,
                NumStudents INT,
                InstructorID VARCHAR(64),
                PRIMARY KEY (SectionID, CourseID, Semester, Year),
                FOREIGN KEY (CourseID) REFERENCES Course(CourseID),
                FOREIGN KEY (InstructorID) REFERENCES Instructor(InstructorID)
            )
            """)

            # Create Evaluation table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS Evaluation (
                GoalCode VARCHAR(64),
                DegreeName VARCHAR(64),
                DegreeLevel VARCHAR(64),
                SectionID VARCHAR(64),
                CourseID VARCHAR(64),
                Semester VARCHAR(64),
                Year INT,
                EvaluationType VARCHAR(64),
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
            exit()
        finally:
            cursor.close()

    def clear_tables(self) -> None:
        cursor = self.connection.cursor()
        try:
            cursor.execute("DROP TABLE IF EXISTS Evaluation")
            cursor.execute("DROP TABLE IF EXISTS Section")
            cursor.execute("DROP TABLE IF EXISTS Instructor")
            cursor.execute("DROP TABLE IF EXISTS Goal_Course")
            cursor.execute("DROP TABLE IF EXISTS Goal")
            cursor.execute("DROP TABLE IF EXISTS Degree_Course")
            cursor.execute("DROP TABLE IF EXISTS Course")
            cursor.execute("DROP TABLE IF EXISTS Degree")
            self.connection.commit()
            print("Tables cleared successfully.")
        except Error as e:
            print(f"Error clearing tables: {e}")
            self.connection.rollback()
            exit()
        finally:
            cursor.close()
    

    # Inserts a degree into the database
    def insert_degree(self, degree: Degree) -> None:

        cursor = self.connection.cursor()
        try:
            cursor.execute("INSERT INTO Degree (DegreeName, DegreeLevel) VALUES (%s, %s)", (degree.degreeName, degree.degreeLevel))
            self.connection.commit()
            print(f"Degree {degree.degreeName} {degree.degreeLevel} inserted successfully.")
        except Error as e:
            print(f"Error inserting degree: {e}")
            self.connection.rollback()
        finally:
            cursor.close()

    # Inserts a degree course into the database
    def insert_degree_course(self, degreeCourse: DegreeCourse) -> None:
        cursor = self.connection.cursor()
        try:
            cursor.execute("INSERT INTO Degree_Course (DegreeName, DegreeLevel, CourseID, IsCore) VALUES (%s, %s, %s, %s)", (degreeCourse.degreeName, degreeCourse.degreeLevel, degreeCourse.courseID, degreeCourse.isCore))
            self.connection.commit()
            print(f"Degree course {degreeCourse.degreeName} {degreeCourse.degreeLevel} {degreeCourse.courseID} inserted successfully.")
        except Error as e:
            print(f"Error inserting degree course: {e}")
            self.connection.rollback()
        finally:
            cursor.close()

    # Inserts a course into the database
    def insert_course(self, course: Course) -> None:
        cursor = self.connection.cursor()
        try:
            cursor.execute("INSERT INTO Course (CourseID, CourseName) VALUES (%s, %s)", (course.courseID, course.courseName))
            self.connection.commit()
            print(f"Course {course.courseID} inserted successfully.")
        except Error as e:
            print(f"Error inserting course: {e}")
            self.connection.rollback()
        finally:
            cursor.close()


    # Inserts a section into the database
    def insert_section(self, section: Section) -> None:
        cursor = self.connection.cursor()
        try:
            cursor.execute("INSERT INTO Section (SectionID, CourseID, Semester, Year, NumStudents, InstructorID) VALUES (%s, %s, %s, %s, %s, %s)", (section.sectionID, section.courseID, section.semester, section.year, section.numStudents, section.instructorID))
            self.connection.commit()
            print(f"Section {section.sectionID} inserted successfully.")
        except Error as e:
            print(f"Error inserting section: {e}")
            self.connection.rollback()
        finally:
            cursor.close()


    # Inserts an instructor into the database
    def insert_instructor(self, instructor: Instructor) -> None:
        cursor = self.connection.cursor()
        try:
            cursor.execute("INSERT INTO Instructor (InstructorID, InstructorName) VALUES (%s, %s)", (instructor.instructorID, instructor.instructorName))
            self.connection.commit()
            print(f"Instructor {instructor.instructorID} inserted successfully.")
        except Error as e:
            print(f"Error inserting instructor: {e}")
            self.connection.rollback()
        finally:
            cursor.close()


    # Inserts a goal into the database
    def insert_goal(self, goal: Goal) -> None:
        
        cursor = self.connection.cursor()
        try:
            cursor.execute("INSERT INTO Goal (GoalCode, DegreeName, DegreeLevel, Description) VALUES (%s, %s, %s, %s)", (goal.goalCode, goal.degreeName, goal.degreeLevel, goal.description))
            self.connection.commit()
            print(f"Goal {goal.goalCode} {goal.degreeName} {goal.degreeLevel} inserted successfully.")
        except Error as e:
            print(f"Error inserting goal: {e}")
            self.connection.rollback()
        finally:
            cursor.close()


    # Inserts a goal course into the database
    def insert_goal_course(self, goalCourse: GoalCourse) -> None:
        cursor = self.connection.cursor()
        try:
            cursor.execute("INSERT INTO Goal_Course (GoalCode, DegreeName, DegreeLevel, CourseID) VALUES (%s, %s, %s, %s)", (goalCourse.goalCode, goalCourse.degreeName, goalCourse.degreeLevel, goalCourse.courseID))
            self.connection.commit()
            print(f"Goal course {goalCourse.goalCode} {goalCourse.degreeName} {goalCourse.degreeLevel} {goalCourse.courseID} inserted successfully.")
        except Error as e:
            print(f"Error inserting goal course: {e}")
            self.connection.rollback()
        finally:
            cursor.close()


    # Inserts an evaluation into the database
    def insert_evaluation(self, evaluation: Evaluation) -> None:
        cursor = self.connection.cursor()  
        

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
    
    # get all degrees
    def get_all_degrees(self) -> list[Degree]:
        # TODO
        # sample return for now
        return [Degree("Computer Science", "BS"), Degree("Computer Science", "MS"), Degree("Data Science", "PhD")]
    
    # get all courses
    def get_all_courses(self) -> list[Course]:
        # TODO
        # sample return for now
        return [Course("CS101", "Intro to Computer Science"), Course("CS102", "Data Structures"), Course("CS103", "Algorithms")]
    
    # get all degree courses
    def get_all_degree_courses(self) -> list[DegreeCourse]:
        # TODO
        # sample return for now
        return [DegreeCourse("Computer Science", "BS", "CS101", True), DegreeCourse("Computer Science", "BS", "CS102", True), DegreeCourse("Computer Science", "BS", "CS103", False)]
    
    # get all goals
    def get_all_goals(self) -> list[Goal]:
        # TODO
        # sample return for now
        return [Goal("Goal1", "Computer Science", "BS", "Description 1"), Goal("Goal2", "Computer Science", "BS", "Description 2"), Goal("Goal3", "Computer Science", "BS", "Description 3")]
    
    # get all goal courses
    def get_all_goal_courses(self) -> list[GoalCourse]:
        # TODO
        return None
    
    # get all instructors
    def get_all_instructors(self) -> list[Instructor]:
        # TODO
        return None