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
    @dashapp.callback(Output('datatable-row-ids', 'data'))
    def generate_table(max_rows=10):
        pass
