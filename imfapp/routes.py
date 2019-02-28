from imfapp import app
from imf_api.IMFClient import IMFClient
from flask import render_template
from flask import request
from imf_api.help_functions import parse_imf_api_data, create_go, create_figure, create_layout
import json
import plotly



@app.route('/')
@app.route('/dashboard.html', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'GET':
        client = IMFClient()
        var = client.get_countries('IFS').values
        figures_json = json.dumps([], cls=plotly.utils.PlotlyJSONEncoder)
        return render_template('dashboard.html', figuresJSON=figures_json, var=var)

    elif request.method == 'POST':
        client = IMFClient()
        answer = request.form
        figures = []
        graph_objects = []
        for selected_country in answer:
            data = client.get_data('IFS', 'M', selected_country, 'FILR_PA', '1950', '2016')
            graph_object = create_go(answer[selected_country], data)
            graph_objects.append(graph_object)
        layout = create_layout(title='FILR_PA', x_label='M', y_label='Something I don\'t know')
        figure = create_figure(graph_objects, layout)
        figures.append(figure)
        var = client.get_countries('IFS').values
        figures_json = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)
        return render_template('dashboard.html', figuresJSON=figures_json, var=var)
