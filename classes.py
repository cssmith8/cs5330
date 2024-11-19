
class Degree:
    # (key) degreeName: str
    # (key) degreeLevel: str
    def __init__(self, degreeName: str, degreeLevel: str):
        self.degreeName: str = degreeName
        self.degreeLevel: str = degreeLevel

class DegreeCourse:
    # (key) degreeName: str
    # (key) degreeLevel: str
    # (key) courseID: int
    # isCore: bool
    def __init__(self, degreeName: str, degreeLevel: str, courseID: int, isCore: bool):
        self.degreeName: str = degreeName
        self.degreeLevel: str = degreeLevel
        self.courseID: int = courseID
        self.isCore: bool = isCore
    
    # get the attached degree from the database
    def get_degree(self, db) -> None:
        from database import Database
        if not isinstance(db, Database):
            return None
        return db.get_degree(self.degreeName, self.degreeLevel)
    
    # get the attached course from the database
    def get_course(self, db) -> None:
        from database import Database
        if not isinstance(db, Database):
            return None
        return db.get_course(self.courseID)

class Course:
    # (key) courseID: str
    # courseName: str
    def __init__(self, courseID: str, courseName: str):
        self.courseID: str = courseID
        self.courseName: str = courseName

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
    def get_course(self, db) -> None:
        from database import Database
        if not isinstance(db, Database):
            return None
        return db.get_course(self.courseID)

class Instructor:
    # (key) instructorID: str
    # instructorName: str
    def __init__(self, instructorID: str, instructorName: str):
        self.instructorID: str = instructorID
        self.instructorName: str = instructorName

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
