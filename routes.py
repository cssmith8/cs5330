from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from data import Data
from classes import *

app = Flask(__name__)

options: list = ['option1', 'option7', 'option3']

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

@app.route('/instructor')
def instructor():
    return render_template('instructor.html')

@app.route('/section')
def section():
    return render_template('section.html')

@app.route('/selectdegree')
def selectdegree():
    return render_template('selectdegree.html')



################################ Form routes

@app.route('/home/process', methods=['POST'])
def process():
    input_data = request.form.get('inputData')
    input_data_2 = request.form.get('inputData2')
    input_data_3 = request.form.get('dropdown')
    print (input_data_3)
    # Process the data
    result = some_processing_function(input_data)
    result2 = some_processing_function(input_data_2)
    return jsonify({'result': result + " " + result2, 'invalid1': 0})

def some_processing_function(input_data) -> str:
    # Example processing function
    print(f"Processing data: {input_data}")
    return f"Processed data: {Data._instance.db.is_connected()}"

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

@app.route('/get_options')
def get_options():
    return jsonify({'content': options})



################################ misc routes

# @app.route('/get_degree/<degree_id>')
# def get_degree(degree_id):
#     degree: Degree = Data._instance.db.get_degree(degree_id)
#     if degree:
#         return jsonify(degree)
#     else:
#         return jsonify({'error': 'Degree not found'}), 404