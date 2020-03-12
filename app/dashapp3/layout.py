import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly
import plotly.graph_objs as go

layout = html.Div([
    html.H2('Top Locations of Search Terms'),
    html.P('Term searches may take several seconds. Please be patient.''),
    html.P('Twitter users are not required to list a location in their profile; search results only reflect those who do.''),
    html.A("Home", id='Home', href="http://127.0.0.1:5000/"),
    html.Br(),
    html.Br(),
    dcc.Input(id='term_search', value='enter search term', type='text'),
    html.Br(),
    html.Br(),
    dcc.Graph(id='live-graph',animate=False),
    dcc.Interval(id='graph-update', interval=1*10000),
    html.Br(),
    html.Br(),
    html.P('Partial records for up to 100 of the most recent tweets containing search term'),
    dash_table.DataTable(
        id='datatable-row-ids',
        style_data={
        'whiteSpace': 'normal',
        'height': 'auto'
        },
        columns=[
            {'name': i, 'id': i, 'deletable': True} for i in ['date_time', 'content', 'verified', 'lang',
       'location',
       'user', 'is_rt', 'textblob_sentiment',
       'vader_sentiment']
            # omit the id column
            if i != 'id'
        ],
        page_action='custom',
        page_current= 0,
        page_size= 10
    ),

    html.Div(id='datatable-row-ids-container')
])

"""
layout = html.Div([
    dash_table.DataTable(
        id='tweet-table',
    )])
"""
