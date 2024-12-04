from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from data import Data
from classes import *

app = Flask(__name__)

options: list = ['option1', 'option7', 'option3']

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/degree_courses')
def degree_courses():
    return render_template('dcinput.html')

@app.route('/degree')
def degree():
    return render_template('degree.html')

@app.route('/goal')
def goal():
    return render_template('goal.html')

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



################################ Backend routes

@app.route('/get_all_degrees')
def get_all_degrees():
    degrees: list[Degree] = Data._instance.db.get_all_degrees()
    r = []
    for degree in degrees:
        r.append({'degreeName': degree.degreeName, 'degreeLevel': degree.degreeLevel})
    return jsonify({'degrees': r})

@app.route('/get_all_courses')
def get_all_courses():
    courses: list[Course] = Data._instance.db.get_all_courses()
    r = []
    for course in courses:
        r.append({'courseID': course.courseID, 'courseName': course.courseName})
    return jsonify({'courses': r})

@app.route('/get_all_degree_courses')
def get_all_degree_courses():
    degreeCourses: list[DegreeCourse] = Data._instance.db.get_all_degree_courses()
    r = []
    for dc in degreeCourses:
        r.append({'courseID': dc.courseID, 'degreeName': dc.degreeName, 'degreeLevel': dc.degreeLevel, 'isCore': dc.isCore})
    return jsonify({'courses': r})

@app.route('/get_all_goals')
def get_all_goals():
    goals: list[Goal] = Data._instance.db.get_all_goals()
    r = []
    for goal in goals:
        r.append({'degreeName': goal.degreeName, 'degreeLevel': goal.degreeLevel, 'goalCode': goal.goalCode, 'description': goal.description})
    return jsonify({'goals': r})

@app.route('/get_options')
def get_options():
    print("real " + str(Data._instance.db.is_connected()))
    return jsonify({'options': options})



################################ misc routes

# @app.route('/get_degree/<degree_id>')
# def get_degree(degree_id):
#     degree: Degree = Data._instance.db.get_degree(degree_id)
#     if degree:
#         return jsonify(degree)
#     else:
#         return jsonify({'error': 'Degree not found'}), 404