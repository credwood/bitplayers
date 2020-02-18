import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly
import pandas as pd
import plotly.graph_objs as go
import pandas as pd
import mysql.connector as sql



layout = html.Div(
    [
        html.H2('Live Twitter Sentiment'),
        html.A("Home", id='Home', href="http://127.0.0.1:5000/"),
        dcc.Graph(id='live-graph', animate=True),
        dcc.Interval(id='graph-update', interval=1*10000),

        html.Div(id='page-content')
    ])
