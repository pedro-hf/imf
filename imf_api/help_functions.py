import plotly.graph_objs as go
import pandas as pd
from datetime import datetime


def parse_imf_api_data(df):
    """
    It takes the respond from the IMF API and prepares it for javaScript plotly
    :param df: data as pd.DataFrame from the IMF API
    :return: figure dictionary to pass to the html page.
    """
    df['date'] = df.time.apply(lambda s: datetime.strptime(s, '%Y-%m'))

    graph_one = []
    x_val = df.date.tolist()
    y_val = df.value.tolist()
    graph_one.append(
        go.Scatter(
            x=x_val,
            y=y_val,
            mode='lines',
            name='Name'
        )
    )

    layout_one = {'title': 'Title',
                  'xaxis': {'title': 'Year',
                            'autotick': False,
                            'tick0': 1990,
                            'dtick': 25},
                  'yaxis': {'title': 'Hectares'}}

    figures = dict(data=graph_one, layout=layout_one)
    return figures


def create_go(name, df):
    """Given a name (str) and a dataframe with columns time and value it will create a go.Scatter object"""
    df['date'] = df.time.apply(lambda s: datetime.strptime(s, '%Y-%m'))
    x_val = df.date.tolist()
    y_val = df.value.tolist()
    graph_object = go.Scatter(x=x_val,
                              y=y_val,
                              mode='lines',
                              name=name)
    return graph_object


def create_layout(title='NA', x_label='NA', y_label='NA'):
    """crates a layout dictionary for the figures, given axis labels and title"""
    layout = {'title': title,
              'xaxis': {'title': x_label,
                        'autotick': False,
                        'tick0': 1990,
                        'dtick': 5},
              'yaxis': {'title': y_label}}
    return layout


def create_figure(graph_objects, layout):
    figure = dict(data=graph_objects, layout=layout)
    return figure
