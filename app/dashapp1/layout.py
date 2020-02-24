import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly
import pandas as pd
import plotly.graph_objs as go
import pandas as pd
import mysql.connector as sql



layout = html.Div([
        html.H2('Live Twitter Sentiment'),
        html.A("Home", id='Home', href="http://127.0.0.1:5000/"),
        dcc.Graph(id='live-graph', animate=True),
        dcc.Interval(id='graph-update', interval=1*10000),
        dash_table.DataTable(
            id='datatable-row-ids',
            style_data={
            'whiteSpace': 'normal',
            'height': 'auto'
            },
            columns=[
                {'name': i, 'id': i, 'deletable': True} for i in ['date_time', 'content', 'verified', 'lang', 'place',
           'location', 'hashtags', 'user_mentions', 'in_reply_to_screen_name',
           'user', 'retweet', 'sentiment', 'sentiment_textblob',
           'sentiment_vader']
                # omit the id column
                if i != 'id'
            ],
            page_action='custom',
            page_current= 0,
            page_size= 10
            ),
        html.Div(id='page-content')
    ])
