from flask import Flask, render_template, request, flash, redirect, url_for, jsonify

app = Flask(__name__)

# list of options
options: list = ['option1', 'option7', 'option3']

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/get_options')
def get_options():
    return jsonify({'options': options})