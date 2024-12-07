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
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
            cursor.execute("TRUNCATE TABLE Evaluation")
            cursor.execute("TRUNCATE TABLE Section")
            cursor.execute("TRUNCATE TABLE Instructor")
            cursor.execute("TRUNCATE TABLE Goal_Course")
            cursor.execute("TRUNCATE TABLE Goal")
            cursor.execute("TRUNCATE TABLE Degree_Course")
            cursor.execute("TRUNCATE TABLE Course")
            cursor.execute("TRUNCATE TABLE Degree")
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
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
           
        #TODO

    # gets a degree from the database given all the key attributes
    def get_degree(self, degreeName: str, degreeLevel: str) -> Degree:

        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT * FROM Degree WHERE DegreeName = %s AND DegreeLevel = %s", (degreeName, degreeLevel))
            result = cursor.fetchone()
            if result is not None:
                return Degree(result[0], result[1])
            else:
                return None
        except Error as e:
            print(f"Error getting degree: {e}")
            return None
        finally:
            cursor.close()
    

    # gets a degree course from the database given all the key attributes
    def get_degree_course(self, degreeName: str, degreeLevel: str, courseID: int) -> DegreeCourse:
        
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT * FROM Degree_Course WHERE DegreeName = %s AND DegreeLevel = %s AND CourseID = %s", (degreeName, degreeLevel, courseID))
            result = cursor.fetchone()
            if result is not None:
                return DegreeCourse(result[0], result[1], result[2], result[3])
            else:
                return None
        except Error as e:
            print(f"Error getting degree course: {e}")
            return None
        finally:
            cursor.close()


    # gets a course from the database given all the key attributes
    def get_course(self, courseID: str) -> Course:

        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT * FROM Course WHERE CourseID = %s", (courseID,))
            result = cursor.fetchone()
            if result is not None:
                return Course(result[0], result[1])
            else:
                return None
        except Error as e:
            print(f"Error getting course: {e}")
            return None
        finally:
            cursor.close()

    # gets a section from the database given all the key attributes
    def get_section(self, sectionID: str, courseID: str, semester: str, year: int) -> Section:
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT * FROM Section WHERE SectionID = %s AND CourseID = %s AND Semester = %s AND Year = %s", (sectionID, courseID, semester, year))
            result = cursor.fetchone()
            if result is not None:
                return Section(result[0], result[1], result[2], result[3], result[4], result[5])
            else:
                return None
        except Error as e:
            print(f"Error getting section: {e}")
            return None
        finally:
            cursor.close()

    # gets an instructor from the database given all the key attributes
    def get_instructor(self, instructorID: str) -> Instructor:
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT * FROM Instructor WHERE InstructorID = %s", (instructorID,))
            result = cursor.fetchone()
            if result is not None:
                return Instructor(result[0], result[1])
            else:
                return None
        except Error as e:
            print(f"Error getting instructor: {e}")
            return None
        finally:
            cursor.close()

    # gets a goal from the database given all the key attributes
    def get_goal(self, goalCode: str, degreeName: str, degreeLevel: str) -> Goal:
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT * FROM Goal WHERE GoalCode = %s AND DegreeName = %s AND DegreeLevel = %s", (goalCode, degreeName, degreeLevel))
            result = cursor.fetchone()
            if result is not None:
                return Goal(result[0], result[1], result[2], result[3])
            else:
                return None
        except Error as e:
            print(f"Error getting goal: {e}")
            return None
        finally:
            cursor.close()

    # gets a goal course from the database given all the key attributes
    def get_goal_course(self, goalCode: str, degreeName: str, degreeLevel: str, courseID: str) -> GoalCourse:

        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT * FROM Goal_Course WHERE GoalCode = %s AND DegreeName = %s AND DegreeLevel = %s AND CourseID = %s", (goalCode, degreeName, degreeLevel, courseID))
            result = cursor.fetchone()
            if result is not None:
                return GoalCourse(result[0], result[1], result[2], result[3])
            else:
                return None
        except Error as e:
            print(f"Error getting goal course: {e}")
            return None
        finally:
            cursor.close()

    # gets an evaluation from the database given all the key attributes
    def get_evaluation(self, goalCode: str, degreeName: str, degreeLevel: str, sectionID: str, courseID: str, semester: str, year: int) -> Evaluation:
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT * FROM Evaluation WHERE GoalCode = %s AND DegreeName = %s AND DegreeLevel = %s AND SectionID = %s AND CourseID = %s AND Semester = %s AND Year = %s", (goalCode, degreeName, degreeLevel, sectionID, courseID, semester, year))
            result = cursor.fetchone()
            if result is not None:
                return Evaluation(result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7], result[8], result[9], result[10], result[11])
            else:
                return None
        except Error as e:
            print(f"Error getting evaluation: {e}")
            return None
        finally:
            cursor.close()
    
    # gets all degree courses from the database given degreeName and degreeLevel
    def get_degree_courses_from_degree(self, degreeName: str, degreeLevel: str) -> list[DegreeCourse]:

        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT * FROM Degree_Course WHERE DegreeName = %s AND DegreeLevel = %s", (degreeName, degreeLevel))
            result = cursor.fetchall()
            if result is not None:
                degreeCourses = []
                for row in result:
                    degreeCourses.append(DegreeCourse(row[0], row[1], row[2], row[3]))
                return degreeCourses
            else:
                return None
        except Error as e:
            print(f"Error getting degree courses: {e}")
            return None
        finally:
            cursor.close()
    
    # gets all degree courses from the database given courseID
    def get_degree_courses_from_course(self, courseID: str) -> list[DegreeCourse]:
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT * FROM Degree_Course WHERE CourseID = %s", (courseID,))
            result = cursor.fetchall()
            if result is not None:
                degreeCourses = []
                for row in result:
                    degreeCourses.append(DegreeCourse(row[0], row[1], row[2], row[3]))
                return degreeCourses
            else:
                return None
        except Error as e:
            print(f"Error getting degree courses: {e}")
            return None
        finally:
            cursor.close()
    
    # gets all goals from the database given degreeName and degreeLevel
    def get_goals_from_degree(self, degreeName: str, degreeLevel: str) -> list[Goal]:

        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT * FROM Goal WHERE DegreeName = %s AND DegreeLevel = %s", (degreeName, degreeLevel))
            result = cursor.fetchall()
            if result is not None:
                goals = []
                for row in result:
                    goals.append(Goal(row[0], row[1], row[2], row[3]))
                return goals
            else:
                return None
        except Error as e:
            print(f"Error getting goals: {e}")
            return None
        finally:
            cursor.close()
    
    # gets all goal courses from the database given goalCode, degreeName, and degreeLevel
    def get_goal_courses_from_goal(self, goalCode: str, degreeName: str, degreeLevel: str) -> list[GoalCourse]:
            
            cursor = self.connection.cursor()
            try:
                cursor.execute("SELECT * FROM Goal_Course WHERE GoalCode = %s AND DegreeName = %s AND DegreeLevel = %s", (goalCode, degreeName, degreeLevel))
                result = cursor.fetchall()
                if result is not None:
                    goalCourses = []
                    for row in result:
                        goalCourses.append(GoalCourse(row[0], row[1], row[2], row[3]))
                    return goalCourses
                else:
                    return None
            except Error as e:
                print(f"Error getting goal courses: {e}")
                return None
            finally:
                cursor.close()
    
    # gets all goal courses from the database given courseID
    def get_goal_courses_from_course(self, courseID: str) -> list[GoalCourse]:
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT * FROM Goal_Course WHERE CourseID = %s", (courseID,))
            result = cursor.fetchall()
            if result is not None:
                goalCourses = []
                for row in result:
                    goalCourses.append(GoalCourse(row[0], row[1], row[2], row[3]))
                return goalCourses
            else:
                return None
        except Error as e:
            print(f"Error getting goal courses: {e}")
            return None
        finally:
            cursor.close()
    
    # get all sections from the database given courseID
    def get_sections_from_course(self, courseID: str) -> list[Section]:
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT * FROM Section WHERE CourseID = %s", (courseID,))
            result = cursor.fetchall()
            if result is not None:
                sections = []
                for row in result:
                    sections.append(Section(row[0], row[1], row[2], row[3], row[4], row[5]))
                return sections
            else:
                return None
        except Error as e:
            print(f"Error getting sections: {e}")
            return None
        finally:
            cursor.close()
    
    # get all sections from the database given instructorID
    def get_sections_from_instructor(self, instructorID: str) -> list[Section]:
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT * FROM Section WHERE InstructorID = %s", (instructorID,))
            result = cursor.fetchall()
            if result is not None:
                sections = []
                for row in result:
                    sections.append(Section(row[0], row[1], row[2], row[3], row[4], row[5]))
                return sections
            else:
                return None
        except Error as e:
            print(f"Error getting sections: {e}")
            return None
        finally:
            cursor.close()
    
    # get all evaluations from the database given goalCode, DegreeName, and DegreeLevel
    def get_evaluations_from_goal(self, goalCode: str, degreeName: str, degreeLevel: str) -> list[Evaluation]:
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT * FROM Evaluation WHERE GoalCode = %s AND DegreeName = %s AND DegreeLevel = %s", (goalCode, degreeName, degreeLevel))
            result = cursor.fetchall()
            if result is not None:
                evaluations = []
                for row in result:
                    evaluations.append(Evaluation(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11]))
                return evaluations
            else:
                return None
        except Error as e:
            print(f"Error getting evaluations: {e}")
            return None
        finally:
            cursor.close()
    
    # get all evaluations from the database given SectionID, CourseID, Semester, and Year
    def get_evaluations_from_section(self, sectionID: str, courseID: str, semester: str, year: int) -> list[Evaluation]:
        
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT * FROM Evaluation WHERE SectionID = %s AND CourseID = %s AND Semester = %s AND Year = %s", (sectionID, courseID, semester, year))
            result = cursor.fetchall()
            if result is not None:
                evaluations = []
                for row in result:
                    evaluations.append(Evaluation(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11]))
                return evaluations
            else:
                return None
        except Error as e:
            print(f"Error getting evaluations: {e}")
            return None
        finally:
            cursor.close()
    
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
        #sample return for now
        return [Instructor("1", "John Doe"), Instructor("2", "Jane Doe"), Instructor("3", "Alice Smith")]