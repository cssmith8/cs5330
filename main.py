class Degree:
    # degreeName: str
    # degreeLevel: str
    def __init__(self, degreeName: str, degreeLevel: str):
        self.degreeName: str = degreeName
        self.degreeLevel: str = degreeLevel

class DegreeCourse:
    # degreeName: str
    # degreeLevel: str
    # courseID: int
    # isCore: bool
    def __init__(self, degreeName: str, degreeLevel: str, courseID: int, isCore: bool):
        self.degreeName: str = degreeName
        self.degreeLevel: str = degreeLevel
        self.courseID: int = courseID
        self.isCore: bool = isCore

class Course:
    # courseID: str
    # courseName: str
    def __init__(self, courseID: str, courseName: str):
        self.courseID: str = courseID
        self.courseName: str = courseName

class Section:
    # sectionID: str
    # courseID: str
    # semester: str
    # year: int
    # numStudents: int
    # instructorID: str
    def __init__(self, sectionID: str, courseID: str, semester: str, year: int, numStudents: int, instructorID: str):
        self.sectionID: str = sectionID
        self.courseID: str = courseID
        self.semester: str = semester
        self.year: int = year
        self.numStudents: int = numStudents
        self.instructorID: str = instructorID

class Instructor:
    # instructorID: str
    # instructorName: str
    def __init__(self, instructorID: str, instructorName: str):
        self.instructorID: str = instructorID
        self.instructorName: str = instructorName

class Goal:
    # goalCode: str
    # degreeName: str
    # degreeLevel: str
    # description: str
    def __init__(self, goalCode: str, degreeName: str, degreeLevel: str, description: str):
        self.goalCode: str = goalCode
        self.degreeName: str = degreeName
        self.degreeLevel: str = degreeLevel
        self.description: str = description

    def real() -> list[int]:
        return [1, 2, 3]


class GoalCourse:
    # goalCode: str
    # degreeName: str
    # degreeLevel: str
    # courseID: str
    def __init__(self, goalCode: str, degreeName: str, degreeLevel: str, courseID: str):
        self.goalCode: str = goalCode
        self.degreeName: str = degreeName
        self.degreeLevel: str = degreeLevel
        self.courseID: str = courseID

class Evaluation:
    # goalCode: str
    # degreeName: str
    # degreeLevel: str
    # sectionID: str
    # courseID: str
    # semester: str
    # year: int
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
