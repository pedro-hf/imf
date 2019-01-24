import plotly.graph_objs as go
import pandas as pd
from datetime import datetime



def parse_imf_api_data(json_data):
    """
    It takes the respond from the IMF API and prepares it for javaScript plotly
    :param json_data: data in jason format from the IMF API
    :return: figure dictionary to pass to the html page.
    """
    df = pd.DataFrame().from_dict(json_data)
    df.rename(columns={'@OBS_VALUE': 'value', '@TIME_PERIOD': 'time_period'}, inplace=True)
    df['date'] = df.time_period.apply(lambda s: datetime.strptime(s, '%Y-%m'))

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

    figures = [dict(data=graph_one, layout=layout_one)]
    return figures
