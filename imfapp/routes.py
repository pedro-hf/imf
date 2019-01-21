from imfapp import app

from flask import render_template

@app.route('/')

@app.route('/dashboard.html')
def dashboard():
    return render_template('dashboard.html')