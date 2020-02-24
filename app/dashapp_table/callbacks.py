from datetime import datetime as dt
from dash.dependencies import Input
from dash.dependencies import Output
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go
import pandas as pd
import mysql.connector as sql


def register_callbacks_table(dashapp):
    @dashapp.callback(Output('datatable-row-ids', 'data'),
              [Input('datatable-row-ids', "page_current"),Input('datatable-row-ids', 'page_size')])
    def generate_table(page_current,page_size):
        db_connection= sql.connect(user='root', password='', host='127.0.0.1', database='tweets')
        cur = db_connection.cursor()
        df = pd.read_sql('SELECT * FROM sent_trump ORDER BY id DESC LIMIT 15', con=db_connection, index_col='id')

        return df.to_dict('records')
