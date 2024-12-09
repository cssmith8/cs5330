from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from data import Data
from classes import *

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/degree_courses')
def degree_courses():
    return render_template('dcinput.html')

@app.route('/goal_courses')
def goal_courses():
    return render_template('gcinput.html')

@app.route('/degree')
def degree():
    return render_template('degree.html')

@app.route('/goal')
def goal():
    return render_template('goal.html')

@app.route('/course')
def course():
    return render_template('course.html')

@app.route('/instructor')
def instructor():
    return render_template('instructor.html')

@app.route('/section')
def section():
    return render_template('section.html')

@app.route('/selectdegree')
def selectdegree():
    return render_template('selectdegree.html')

@app.route('/selectcourse')
def selectcourse():
    return render_template('selectcourse.html')

@app.route('/selectinstructor')
def selectinstructor():
    return render_template('selectinstructor.html')

@app.route('/selectsemester')
def selectsemester():
    return render_template('selectsemester.html')

@app.route('/evaluation')
def evaluation():
    return render_template('evaluation.html')


################################ Form routes

@app.route('/dcinput/form', methods=['POST'])
def dcinput_form():
    input_degree = json.loads(request.form.get('degree'))
    input_course = json.loads(request.form.get('course'))
    isCore: bool = request.form.get('isCore')

    dc: DegreeCourse = DegreeCourse(input_degree.get('degreeName'), input_degree.get('degreeLevel'), input_course.get("courseID"), isCore)

    Data._instance.db.insert_degree_course(dc)

    return jsonify({"result": str(isCore)})

@app.route('/degree/form', methods=['POST'])
def degree_form():
    degreeName: str = request.form.get('degreeName')
    degreeLevel: str = request.form.get('degreeLevel')

    # input validation here

    degree: Degree = Degree(degreeName, degreeLevel)
    Data._instance.db.insert_degree(degree)

    return jsonify({"result": "success", "invalid1": False, "invalid2": False})

@app.route('/goal/form', methods=['POST'])
def goal_form():
    input_degree = json.loads(request.form.get('degree'))
    goalCode: str = request.form.get('goalCode')
    description: str = request.form.get('goalDesc')

    # input validation here

    # degree: Degree = Degree(degreeName, degreeLevel)
    goal: Goal = Goal(goalCode, input_degree.get('degreeName'), input_degree.get('degreeLevel'), description)
    Data._instance.db.insert_goal(goal)

    return jsonify({"result": goalCode + " " + input_degree.get('degreeName'), "invalid1": False, "invalid2": False})

@app.route('/course/form', methods=['POST'])
def course_form():
    courseID: str = request.form.get('courseID')
    courseName: str = request.form.get('courseName')

    # input validation here

    course: Course = Course(courseID, courseName)
    Data._instance.db.insert_course(course)

    return jsonify({"result": "course success " + courseID, "invalid1": False, "invalid2": False})

@app.route('/gcinput/form', methods=['POST'])
def gcinput_form():
    input_goal = json.loads(request.form.get('goal'))
    input_course = json.loads(request.form.get('course'))

    gc: GoalCourse = GoalCourse(input_goal.get('goalCode'), input_goal.get('degreeName'), input_goal.get('degreeLevel'), input_course.get("courseID"))
    Data._instance.db.insert_goal_course(gc)

    return jsonify({"result": gc.courseID + " - " + gc.goalCode})

@app.route('/instructor/form', methods=['POST'])
def instructor_form():
    instructorName: str = request.form.get('instructorName')
    instructorID: str = request.form.get('instructorID')

    # input validation here

    instructor: Instructor = Instructor(instructorID, instructorName)
    Data._instance.db.insert_instructor(instructor)

    return jsonify({"result": "instructor success " + instructorName, "invalid1": False, "invalid2": False})

@app.route('/section/form', methods=['POST'])
def section_form():
    input_instructor = json.loads(request.form.get('instructor'))
    input_course = json.loads(request.form.get('course'))
    sectionID: str = request.form.get('sectionID')
    numStudents: int = request.form.get('numStudents')
    semester: str = request.form.get('semester')
    year: int = request.form.get('year')

    Data._instance.db.insert_section(Section(sectionID, input_course.get("courseID"), semester, year, numStudents, input_instructor.get('instructorID')))
    
    return jsonify({"result": "added section " + sectionID + " " + input_course.get("courseID") + " " + input_instructor.get('instructorID') + " " + str(numStudents) + " " + semester + " " + str(year)})

@app.route('/evaluation/form', methods=['POST'])
def evaluation_form():
    input_instructor = json.loads(request.form.get('instructor'))
    semester: str = request.form.get('semester')
    year: int = request.form.get('year')

    time: int = Section.get_time_from_semester(semester, int(year))

    instructor: Instructor = Instructor(input_instructor.get('instructorID'), input_instructor.get('instructorName'))
    sections: list[Section] = instructor.get_sections(Data._instance.db)
    e = []
    if sections:
        for section in sections:
            if section.get_time() == time:
                goals: list[Goal] = section.all_goals(Data._instance.db)
                if goals:
                    for goal in goals:
                        evaluation: Evaluation = Data._instance.db.get_evaluation(goal.goalCode, goal.degreeName, goal.degreeLevel, section.sectionID, section.courseID, section.semester, section.year)
                        if evaluation:
                            e.append({'goalCode': evaluation.goalCode, 'degreeName': evaluation.degreeName, 'degreeLevel': evaluation.degreeLevel, 'sectionID': evaluation.sectionID, 'courseID': evaluation.courseID, 'semester': evaluation.semester, 'year': evaluation.year, 'evaluationType': evaluation.evaluationType, 'A': evaluation.A, 'B': evaluation.B, 'C': evaluation.C, 'F': evaluation.F, 'improvementSuggestion': evaluation.improvementSuggestion})
                        else:
                            e.append({'goalCode': goal.goalCode, 'degreeName': goal.degreeName, 'degreeLevel': goal.degreeLevel, 'sectionID': section.sectionID, 'courseID': section.courseID, 'semester': section.semester, 'year': section.year, 'evaluationType': "", 'A': -1, 'B': -1, 'C': -1, 'F': -1, 'improvementSuggestion': ""})
    return jsonify({"evaluations": e})
@app.route('/selectdegree/form', methods=['POST'])
def selectdegree_form():
    input_degree = json.loads(request.form.get('degree'))
    degree: Degree = Degree(input_degree.get('degreeName'), input_degree.get('degreeLevel'))

    courses: list[DegreeCourse] = Data._instance.db.get_degree_courses_from_degree(degree.degreeName, degree.degreeLevel)
    c = []
    if courses:
        for degreeCourse in courses:
            c.append({'courseID': degreeCourse.courseID, 'isCore': degreeCourse.isCore})
    goals: list[Goal] = Data._instance.db.get_goals_from_degree(degree.degreeName, degree.degreeLevel)
    g = []
    if goals:
        for goal in goals:
            g.append({'goalCode': goal.goalCode, 'description': goal.description, 'degreeName': goal.degreeName, 'degreeLevel': goal.degreeLevel})
    
    return jsonify({"courses": c, "goals": g})

@app.route('/selectdegree/form2', methods=['POST'])
def selectdegree_form2():
    input_goal = json.loads(request.form.get('goal'))
    goal: Goal = Goal(input_goal.get('goalCode'), input_goal.get('degreeName'), input_goal.get('degreeLevel'), input_goal.get('description'))

    goalCourses: list[GoalCourse] = Data._instance.db.get_goal_courses_from_goal(goal.goalCode, goal.degreeName, goal.degreeLevel)
    c = []
    if goalCourses:
        for goalCourse in goalCourses:
            course: Course = goalCourse.get_course(Data._instance.db)
            if course:
                c.append({'courseID': course.courseID, 'courseName': course.courseName})
            else:
                print("DB Error: course not found from goalCourse")

    return jsonify({"courses": c})

@app.route('/selectdegree/form3', methods=['POST'])
def selectdegree_form3():
    input_degree = json.loads(request.form.get('degree'))
    degree: Degree = Degree(input_degree.get('degreeName'), input_degree.get('degreeLevel'))
    startSemester: str = request.form.get('startSemester')
    startYear: int = request.form.get('startYear')
    endSemester: str = request.form.get('endSemester')
    endYear: int = request.form.get('endYear')

    startTime: int = Section.get_time_from_semester(startSemester, int(startYear))
    endTime: int = Section.get_time_from_semester(endSemester, int(endYear))

    degree_courses: list[DegreeCourse] = degree.get_degree_courses(Data._instance.db)
    sections: list[Section] = []
    if not degree_courses:
        return jsonify({"sections": []})
    for dc in degree_courses:
        course: Course = dc.get_course(Data._instance.db)
        newSections: list[Section] = course.get_sections(Data._instance.db)
        if newSections:
            for section in newSections:
                if section.get_time() >= startTime and section.get_time() <= endTime:
                    sections.append(section)

    sections.sort(key=lambda x: x.get_time())
    s = []
    for section in sections:
        s.append({'sectionID': section.sectionID, 'semester': section.semester, 'year': section.year, 'numStudents': section.numStudents, 'instructorID': section.instructorID, 'courseID': section.courseID})

    return jsonify({"sections": s})

@app.route('/selectcourse/form', methods=['POST'])
def selectcourse_form():
    input_course = json.loads(request.form.get('course'))
    course: Course = Course(input_course.get('courseID'), input_course.get('courseName'))
    startSemester: str = request.form.get('startSemester')
    startYear: int = request.form.get('startYear')
    endSemester: str = request.form.get('endSemester')
    endYear: int = request.form.get('endYear')

    startTime: int = Section.get_time_from_semester(startSemester, int(startYear))
    endTime: int = Section.get_time_from_semester(endSemester, int(endYear))

    sections: list[Section] = course.get_sections(Data._instance.db)
    sections.sort(key=lambda x: x.get_time())
    s = []
    if sections:
        for section in sections:
            if section.get_time() >= startTime and section.get_time() <= endTime:
                s.append({'sectionID': section.sectionID, 'semester': section.semester, 'year': section.year, 'numStudents': section.numStudents, 'instructorID': section.instructorID, 'courseID': section.courseID})

    return jsonify({"sections": s})

@app.route('/selectinstructor/form', methods=['POST'])
def selectinstructor_form():
    input_instructor = json.loads(request.form.get('instructor'))
    instructor: Instructor = Instructor(input_instructor.get('instructorID'), input_instructor.get('instructorName'))
    startSemester: str = request.form.get('startSemester')
    startYear: int = request.form.get('startYear')
    endSemester: str = request.form.get('endSemester')
    endYear: int = request.form.get('endYear')

    startTime: int = Section.get_time_from_semester(startSemester, int(startYear))
    endTime: int = Section.get_time_from_semester(endSemester, int(endYear))

    sections: list[Section] = instructor.get_sections(Data._instance.db)
    sections.sort(key=lambda x: x.get_time())
    s = []
    if sections:
        for section in sections:
            if section.get_time() >= startTime and section.get_time() <= endTime:
                s.append({'sectionID': section.sectionID, 'semester': section.semester, 'year': section.year, 'numStudents': section.numStudents, 'instructorID': section.instructorID, 'courseID': section.courseID})


    return jsonify({"sections": s})

@app.route('/selectsemester/form', methods=['POST'])
def selectsemester_form():
    semester: str = request.form.get('semester')
    year: int = request.form.get('year')

    time: int = Section.get_time_from_semester(semester, int(year))
    sections: list[Section] = Data._instance.db.get_all_sections()

    s = []
    if sections:
        for section in sections:
            if section.get_time() == time:
                evalinfo: str = "0"
                real: list[Evaluation] = section.get_evaluations(Data._instance.db)
                if real:
                    evalinfo = "1"
                    e: Evaluation = real[0]
                    if (e.A is None or e.A == -1) or (e.B is None or e.B == -1) or (e.C is None or e.C == -1) or (e.F is None or e.F == -1) or (e.evaluationType is None or e.evaluationType == ""):
                        if (e.improvementSuggestion is None or e.improvementSuggestion == ""):
                            evalinfo = "4"
                        else:
                            evalinfo = "3"
                    else:
                        if (e.improvementSuggestion is None or e.improvementSuggestion == ""):
                            evalinfo = "2"
                s.append({'sectionID': section.sectionID, 'semester': section.semester, 'year': section.year, 'numStudents': section.numStudents, 'instructorID': section.instructorID, 'courseID': section.courseID, 'status': evalinfo})
                      
    return jsonify({"sections": s})

@app.route('/selectsemester/form2', methods=['POST'])
def selectsemester_form2():
    semester: str = request.form.get('semester2')
    year: int = request.form.get('year2')
    percent: int = request.form.get('percentage')

    time: int = Section.get_time_from_semester(semester, int(year))
    sections: list[Section] = Data._instance.db.get_all_sections()

    s = []
    if sections:
        for section in sections:
            if section.get_time() == time:
                evalinfo: str = "0"
                real: list[Evaluation] = section.get_evaluations(Data._instance.db)
                if real:
                    for e in real:
                        percentage: float = e.get_passing_percentage(Data._instance.db)
                        if percentage >= float(percent) / 100.0:
                            s.append({'sectionID': section.sectionID, 'semester': section.semester, 'year': section.year, 'numStudents': section.numStudents, 'instructorID': section.instructorID, 'courseID': section.courseID, 'percentage': percentage * 100})
    return jsonify({"sections": s})

@app.route('/evaluation/edit', methods=['POST'])
def evaluation_edit():
    sectionID: str = request.form.get('sectionID')
    courseID: str = request.form.get('courseID')
    semester: str = request.form.get('semester')
    year: int = request.form.get('year')
    goalCode: str = request.form.get('goalCode')
    degreeName: str = request.form.get('degreeName')
    degreeLevel: str = request.form.get('degreeLevel')
    evaluationType: str = request.form.get('evaluationType')
    A: int = request.form.get('A')
    B: int = request.form.get('B')
    C: int = request.form.get('C')
    F: int = request.form.get('F')
    improvementSuggestion: str = request.form.get('improvementSuggestion')

    if A == "": A = -1
    if B == "": B = -1
    if C == "": C = -1
    if F == "": F = -1

    e: Evaluation = Evaluation(goalCode, degreeName, degreeLevel, sectionID, courseID, semester, year, evaluationType, A, B, C, F, improvementSuggestion)

    Data._instance.db.insert_or_update_evaluation(e)

    return jsonify({"success": 1})

@app.route('/evaluation/duplicate', methods=['POST'])
def evaluation_duplicate():
    eval_from = json.loads(request.form.get('evalFrom'))
    eval_to = json.loads(request.form.get('evalTo'))

    eNew: Evaluation = Evaluation(eval_to.get('goalCode'), eval_to.get('degreeName'), eval_to.get('degreeLevel'), eval_to.get('sectionID'), eval_to.get('courseID'), eval_to.get('semester'), eval_to.get('year'), eval_from.get('evaluationType'), eval_from.get('A'), eval_from.get('B'), eval_from.get('C'), eval_from.get('F'), eval_from.get('improvementSuggestion'))

    Data._instance.db.insert_or_update_evaluation(eNew)

    return jsonify({"success": 1})

################################ Backend routes

@app.route('/get_all_degrees')
def get_all_degrees():
    degrees: list[Degree] = Data._instance.db.get_all_degrees()
    if not degrees:
        return jsonify({'content': []})
    r = []
    for degree in degrees:
        r.append({'degreeName': degree.degreeName, 'degreeLevel': degree.degreeLevel})
    return jsonify({'content': r})

@app.route('/get_all_courses')
def get_all_courses():
    courses: list[Course] = Data._instance.db.get_all_courses()
    if not courses:
        return jsonify({'content': []})
    r = []
    for course in courses:
        r.append({'courseID': course.courseID, 'courseName': course.courseName})
    return jsonify({'content': r})

@app.route('/get_all_degree_courses')
def get_all_degree_courses():
    degreeCourses: list[DegreeCourse] = Data._instance.db.get_all_degree_courses()
    if not degreeCourses:
        return jsonify({'content': []})
    r = []
    for dc in degreeCourses:
        r.append({'courseID': dc.courseID, 'degreeName': dc.degreeName, 'degreeLevel': dc.degreeLevel, 'isCore': dc.isCore})
    return jsonify({'content': r})

@app.route('/get_all_goals')
def get_all_goals():
    goals: list[Goal] = Data._instance.db.get_all_goals()
    if not goals:
        return jsonify({'content': []})
    r = []
    for goal in goals:
        r.append({'degreeName': goal.degreeName, 'degreeLevel': goal.degreeLevel, 'goalCode': goal.goalCode, 'description': goal.description})
    return jsonify({'content': r})

@app.route('/get_all_goal_courses')
def get_all_goal_courses():
    goalCourses: list[GoalCourse] = Data._instance.db.get_all_goal_courses()
    if not goalCourses:
        return jsonify({'content': []})
    r = []
    for gc in goalCourses:
        r.append({'courseID': gc.courseID, 'goalCode': gc.goalCode, 'degreeName': gc.degreeName, 'degreeLevel': gc.degreeLevel})
    return jsonify({'content': r})

@app.route('/get_all_instructors')
def get_all_instructors():
    instructors: list[Instructor] = Data._instance.db.get_all_instructors()
    if not instructors:
        return jsonify({'content': []})
    r = []
    for instructor in instructors:
        r.append({'instructorID': instructor.instructorID, 'instructorName': instructor.instructorName})
    return jsonify({'content': r})

@app.route('/get_all_sections')
def get_all_sections():
    sections: list[Section] = Data._instance.db.get_all_sections()
    if not sections:
        return jsonify({'content': []})
    r = []
    for section in sections:
        r.append({'sectionID': section.sectionID, 'courseID': section.courseID, 'semester': section.semester, 'year': section.year, 'numStudents': section.numStudents, 'instructorID': section.instructorID})
    return jsonify({'content': r})