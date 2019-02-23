from imfapp import app
from imf_api.IMFClient import IMFClient
from flask import render_template
from flask import request
from imf_api.help_functions import parse_imf_api_data
import json
import plotly


@app.route('/')
@app.route('/dashboard.html', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'GET':
        var = [['US', 'United States'], ['GE', 'Germany']]
        figures_json = json.dumps([], cls=plotly.utils.PlotlyJSONEncoder)
        return render_template('dashboard.html', figuresJSON=figures_json, var=var)
    elif request.method == 'POST':
        client = IMFClient()
        answer = request.form
        figures = []
        print(answer)
        for selected_country in answer:
            print(selected_country)
            data = client.get_imf_data(selected_country, 'FILR_PA', '1950', '2016')
            figures.append(parse_imf_api_data(data))
        var = [['US', 'United States'], ['GE', 'Germany']]
        figures_json = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)
        return render_template('dashboard.html', figuresJSON=figures_json, var=var)
