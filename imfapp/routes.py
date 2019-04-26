from imfapp import app
from imf_api.IMFClient import IMFClient
from flask import render_template, redirect
from flask import request
from imf_api.help_functions import parse_imf_api_data, create_go, create_figure, create_layout
import json
import plotly



@app.route('/')
@app.route('/dashboard.html')
def dashboard():
    client = IMFClient()
    dataflows = client.get_dataflows()
    dataflows = dataflows['dataflowID'].values
    return render_template('dataflow_index.html', dataflows=dataflows)


@app.route('/select.html', methods=['POST'])
def redirect_to_dataflow():
    answer = request.form['dataflow']
    print(answer)
    route = '/dashboard/{}.html'.format(answer)
    return redirect(route)


@app.route('/dashboard/<dataflow>.html', methods=['GET', 'POST'])
def dataflow_dashboard(dataflow):
    if request.method == 'GET':
        client = IMFClient()
        countries = client.get_countries(dataflow).values
        indicators = client.get_indicators(dataflow).values
        figures_json = json.dumps([], cls=plotly.utils.PlotlyJSONEncoder)
        return render_template('dashboard.html', dataflow=dataflow,
                               figuresJSON=figures_json, countries=countries, indicators=indicators)

    elif request.method == 'POST':
        client = IMFClient()
        answer = request.form
        figures = []
        graph_objects = []

        plot_countries = []
        for item in answer:
            [type, value] = item.split('_', 1)
            if type == 'country':
                plot_countries.append(value)
            elif type == 'ind':
                plot_ind = value

        for selected_country in plot_countries:
            print('country = ' + selected_country)
            print('Indicator = ' + plot_ind)
            data = client.get_data(dataflow, 'M', selected_country, plot_ind, '1950', '2016')  # 'FILR_PA'
            graph_object = create_go(answer['country_' + selected_country], data)
            graph_objects.append(graph_object)

        layout = create_layout(title='FILR_PA', x_label='M', y_label='Something I don\'t know')
        figure = create_figure(graph_objects, layout)
        figures.append(figure)

        countries = client.get_countries(dataflow).values
        indicators = client.get_indicators(dataflow).values
        figures_json = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)
        return render_template('dashboard.html', dataflow=dataflow, figuresJSON=figures_json,
                               countries=countries, indicators=indicators)
