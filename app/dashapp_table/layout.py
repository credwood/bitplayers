import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly
import plotly.graph_objs as go
import pandas as pd
import mysql.connector as sql

import pandas as pd

db_connection = sql.connect(user='root', password='',
                              host='127.0.0.1',
                              database='tweets')

db_cursor = db_connection.cursor()

df = pd.read_sql('SELECT * FROM sent_trump', con=db_connection, index_col='id')
df=df.tail(15)
df = pd.DataFrame(df)

layout = html.Div([
    dash_table.DataTable(
        style_data={
        'whiteSpace': 'normal',
        'height': 'auto'
        },
        id='datatable-row-ids',
        columns=[
            {'name': i, 'id': i, 'deletable': True} for i in df.columns
            # omit the id column
            if i != 'id'
        ],
        data=df.to_dict('records'),
        editable=True,
        filter_action="native",
        sort_action="native",
        sort_mode='multi',
        row_selectable='multi',
        row_deletable=True,
        selected_rows=[],
        page_action='native',
        page_current= 0,
        page_size= 10,
    ),
    html.Div(id='datatable-row-ids-container')
])

"""
layout = html.Div([
    dash_table.DataTable(
        id='tweet-table',
    )])
"""
