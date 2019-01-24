from imfapp import app
from imf_api.IMFClient import IMFClient
from flask import render_template
from imf_api.help_functions import parse_imf_api_data
import json
import plotly


@app.route('/')
@app.route('/dashboard.html')
def dashboard():
    client = IMFClient()
    data = client.get_imf_data('US', 'FILR_PA', '1950', '2016')
    figures = parse_imf_api_data(data)
    figuresJSON = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('dashboard.html', figuresJSON=figuresJSON)
