from __future__ import annotations
import json

class Degree:
    # (key) degreeName: str
    # (key) degreeLevel: str
    def __init__(self, degreeName: str, degreeLevel: str):
        self.degreeName: str = degreeName
        self.degreeLevel: str = degreeLevel
    
    # get all attached degree courses from the database
    def get_degree_courses(self, db) -> list[DegreeCourse]:
        from database import Database
        if not isinstance(db, Database):
            print("Error: Incorrect database type passed into get_degree_courses()")
            return None
        return db.get_degree_courses_from_degree(self.degreeName, self.degreeLevel)
    
    # get all attached goals from the database
    def get_goals(self, db) -> list[Goal]:
        from database import Database
        if not isinstance(db, Database):
            print("Error: Incorrect database type passed into get_goals()")
            return None
        return db.get_goals_from_degree(self.degreeName, self.degreeLevel)
    

class DegreeCourse:
    # (key) degreeName: str
    # (key) degreeLevel: str
    # (key) courseID: str
    # isCore: bool
    def __init__(self, degreeName: str, degreeLevel: str, courseID: str, isCore: bool):
        self.degreeName: str = degreeName
        self.degreeLevel: str = degreeLevel
        self.courseID: str = courseID
        self.isCore: bool = isCore
    
    # get the attached degree from the database
    def get_degree(self, db) -> Degree:
        from database import Database
        if not isinstance(db, Database):
            print("Error: Incorrect database type passed into get_degree()")
            return None
        return db.get_degree(self.degreeName, self.degreeLevel)
    
    # get the attached course from the database
    def get_course(self, db) -> Course:
        from database import Database
        if not isinstance(db, Database):
            print("Error: Incorrect database type passed into get_course()")
            return None
        return db.get_course(self.courseID)


class Course:
    # (key) courseID: str
    # courseName: str
    def __init__(self, courseID: str, courseName: str):
        self.courseID: str = courseID
        self.courseName: str = courseName
    
    # get all attached sections from the database
    def get_sections(self, db) -> list[Section]:
        from database import Database
        if not isinstance(db, Database):
            print("Error: Incorrect database type passed into get_sections()")
            return None
        return db.get_sections_from_course(self.courseID)
    
    # get all attached goal courses from the database
    def get_goal_courses(self, db) -> list[GoalCourse]:
        from database import Database
        if not isinstance(db, Database):
            print("Error: Incorrect database type passed into get_goal_courses()")
            return None
        return db.get_goal_courses_from_course(self.courseID)
    
    # get all attached degree courses from the database
    def get_degree_courses(self, db) -> list[DegreeCourse]:
        from database import Database
        if not isinstance(db, Database):
            print("Error: Incorrect database type passed into get_degree_courses()")
            return None
        return db.get_degree_courses_from_course(self.courseID)


class Section:
    # (key) sectionID: str
    # (key) courseID: str
    # (key) semester: str
    # (key) year: int
    # numStudents: int
    # instructorID: str
    def __init__(self, sectionID: str, courseID: str, semester: str, year: int, numStudents: int, instructorID: str):
        self.sectionID: str = sectionID
        self.courseID: str = courseID
        self.semester: str = semester
        self.year: int = year
        self.numStudents: int = numStudents
        self.instructorID: str = instructorID
    
    # get the attached course from the database
    def get_course(self, db) -> Course:
        from database import Database
        if not isinstance(db, Database):
            print("Error: Incorrect database type passed into get_course()")
            return None
        return db.get_course(self.courseID)
    
    # get the attached instructor from the database
    def get_instructor(self, db) -> Instructor:
        from database import Database
        if not isinstance(db, Database):
            print("Error: Incorrect database type passed into get_instructor()")
            return None
        return db.get_instructor(self.instructorID)
    
    # get all attached evaluations from the database
    def get_evaluations(self, db) -> list[Evaluation]:
        from database import Database
        if not isinstance(db, Database):
            print("Error: Incorrect database type passed into get_evaluations()")
            return None
        return db.get_evaluations_from_section(self.sectionID, self.courseID, self.semester, self.year)
    
    def get_time(self) -> int:
        return Section.get_time_from_semester(self.semester, self.year)
    
    # static function to convert a semester and year to an int
    @staticmethod
    def get_time_from_semester(isemester: str, iyear: int) -> int:
        nSemester: int = 0
        if isemester == "Spring":
            nSemester = 1
        elif isemester == "Summer":
            nSemester = 2
        elif isemester == "Fall":
            nSemester = 3
        else:
            raise ValueError(f"Invalid semester: {isemester}")
        return int(iyear * 10) + int(nSemester)


class Instructor:
    # (key) instructorID: str
    # instructorName: str
    def __init__(self, instructorID: str, instructorName: str):
        self.instructorID: str = instructorID
        self.instructorName: str = instructorName

    # get all attached sections from the database
    def get_sections(self, db) -> list[Section]:
        from database import Database
        if not isinstance(db, Database):
            print("Error: Incorrect database type passed into get_sections()")
            return None
        return db.get_sections_from_instructor(self.instructorID)


class Goal:
    # (key) goalCode: str
    # (key) degreeName: str
    # (key) degreeLevel: str
    # description: str
    def __init__(self, goalCode: str, degreeName: str, degreeLevel: str, description: str):
        self.goalCode: str = goalCode
        self.degreeName: str = degreeName
        self.degreeLevel: str = degreeLevel
        self.description: str = description
    
    # get the attached degree from the database
    def get_degree(self, db) -> Degree:
        from database import Database
        if not isinstance(db, Database):
            print("Error: Incorrect database type passed into get_degree()")
            return None
        return db.get_degree(self.degreeName, self.degreeLevel)
    
    # get all attached goal courses from the database
    def get_goal_courses(self, db) -> list[GoalCourse]:
        from database import Database
        if not isinstance(db, Database):
            print("Error: Incorrect database type passed into get_goal_courses()")
            return None
        return db.get_goal_courses_from_goal(self.goalCode, self.degreeName, self.degreeLevel)
    
    # get all attached evaluations from the database
    def get_evaluations(self, db) -> list[Evaluation]:
        from database import Database
        if not isinstance(db, Database):
            print("Error: Incorrect database type passed into get_evaluations()")
            return None
        return db.get_evaluations_from_goal(self.goalCode, self.degreeName, self.degreeLevel)


class GoalCourse:
    # (key) goalCode: str
    # (key) degreeName: str
    # (key) degreeLevel: str
    # (key) courseID: str
    def __init__(self, goalCode: str, degreeName: str, degreeLevel: str, courseID: str):
        self.goalCode: str = goalCode
        self.degreeName: str = degreeName
        self.degreeLevel: str = degreeLevel
        self.courseID: str = courseID
    
    # get the attached goal from the database
    def get_goal(self, db) -> Goal:
        from database import Database
        if not isinstance(db, Database):
            print("Error: Incorrect database type passed into get_goal()")
            return None
        return db.get_goal(self.goalCode, self.degreeName, self.degreeLevel)
    
    # get the attached course from the database
    def get_course(self, db) -> Course:
        from database import Database
        if not isinstance(db, Database):
            print("Error: Incorrect database type passed into get_course()")
            return None
        return db.get_course(self.courseID)


class Evaluation:
    # (key) goalCode: str
    # (key) degreeName: str
    # (key) degreeLevel: str
    # (key) sectionID: str
    # (key) courseID: str
    # (key) semester: str
    # (key) year: int
    # evaluationType: str
    # A: int
    # B: int
    # C: int
    # F: int
    # improvementSuggestion: str
    def __init__(self, goalCode: str, degreeName: str, degreeLevel: str, sectionID: str, courseID: str, semester: str, year: int, evaluationType: str, A: int, B: int, C: int, F: int, improvementSuggestion: str):
        self.goalCode: str = goalCode
        self.degreeName: str = degreeName
        self.degreeLevel: str = degreeLevel
        self.sectionID: str = sectionID
        self.courseID: str = courseID
        self.semester: str = semester
        self.year: int = year
        self.evaluationType: str = evaluationType
        self.A: int = A
        self.B: int = B
        self.C: int = C
        self.F: int = F
        self.improvementSuggestion: str = improvementSuggestion
    
    # get the attached section from the database
    def get_section(self, db) -> Section:
        from database import Database
        if not isinstance(db, Database):
            print("Error: Incorrect database type passed into get_section()")
            return None
        return db.get_section(self.sectionID, self.courseID, self.semester, self.year)
    
    # get the attached goal from the database
    def get_goal(self, db) -> Goal:
        from database import Database
        if not isinstance(db, Database):
            print("Error: Incorrect database type passed into get_goal()")
            return None
        return db.get_goal(self.goalCode, self.degreeName, self.degreeLevel)
    
    # get the percentage of passing students
    def get_passing_percentage(self, db) -> float:
        from database import Database
        if not isinstance(db, Database):
            print("Error: Incorrect database type passed into get_section()")
            return None
        if self.F is None or self.get_section(db).numStudents is None:
            return 0
        return 1 - (self.F / self.get_section(db).numStudents)