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
    dataflows['general_id'] = dataflows.dataflowID.str.split('_').map(lambda l: l[0])
    dataflows['general_id_description'] = dataflows.description.str.split(',').map(lambda l: l[0])
    df_general = dataflows[['general_id', 'general_id_description']]
    df_general.drop_duplicates(inplace=True, subset=['general_id_description'])
    dataflows = list(zip(df_general['general_id'], df_general['general_id_description']))
    return render_template('dataflow_index.html', dataflows=dataflows)


@app.route('/select.html', methods=['POST'])
def redirect_to_dataflow():
    answer = request.form['dataflow']
    print(answer)
    route = '/dashboard/{}.html'.format(answer)
    return redirect(route)


@app.route('/dashboard/<dataflow>.html', methods=['GET', 'POST'])
def dataflow_dashboard(dataflow):
    client = IMFClient()
    dataflow_description = client.get_dataflows().set_index('dataflowID').loc[dataflow, 'description']
    countries = client.get_countries(dataflow).values
    indicators = client.get_indicators(dataflow).values
    message_board = []

    if request.method == 'GET':
        figures_json = json.dumps([], cls=plotly.utils.PlotlyJSONEncoder)

    elif request.method == 'POST':
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
            data, message = client.get_data(dataflow, 'M', selected_country, plot_ind, '1950', '2016')
            graph_object = create_go(answer['country_' + selected_country], data)
            graph_objects.append(graph_object)
            message_board.append(selected_country + ' ' + message)

        layout = create_layout(title=dataflow, x_label='M', y_label=plot_ind)
        figure = create_figure(graph_objects, layout)
        figures.append(figure)
        figures_json = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('dashboard.html', dataflow=dataflow, messages=message_board, title=dataflow_description,
                           figuresJSON=figures_json, countries=countries, indicators=indicators)
