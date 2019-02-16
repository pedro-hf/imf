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
        client = IMFClient()
        data = client.get_imf_data('US', 'FILR_PA', '1950', '2016')
        figures = parse_imf_api_data(data)
        var = [1, 2, 3]
        figures_json = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)
        return render_template('dashboard.html', figuresJSON=figures_json, var=var)
    elif request.method == 'POST':
        client = IMFClient()
        data = client.get_imf_data('GE', 'FILR_PA', '1950', '2016')
        figures = parse_imf_api_data(data)
        var = [1, 2, 3]
        figures_json = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)
        return render_template('dashboard.html', figuresJSON=figures_json, var=var)
