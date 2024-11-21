from flask import Flask, render_template, request, flash, redirect, url_for, jsonify

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')