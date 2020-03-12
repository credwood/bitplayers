from datetime import datetime as dt
from dash.dependencies import Input
from dash.dependencies import Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import mysql.connector as sql

#!!!!!!!!!!!!!!!!TAKE ROOT PASSWORD OUT BEFOR COMMITTING TO GIT!!!!!!!!!!!!!!!!!!!

def register_callbacks(dashapp):

    @dashapp.callback(Output('live-graph', 'figure'),
              [Input(component_id='term_search', component_property='value'),Input('graph-update','n_intervals')])
    def update_graph_call(input_value,n):
        try:
            db_connection = sql.connect(user='root', password='',
                                          host='127.0.0.1',
                                          database='tweets')

            db_cursor = db_connection.cursor()
            df = pd.read_sql('SELECT * FROM sent_trump WHERE content LIKE %s ORDER BY id DESC LIMIT 1500', con=db_connection, index_col='id', params=('%' + input_value + '%',))
            #df.sort_values('date_time', inplace=True)
            db_cursor.close()
            db_connection.close()

            #df['date_time'] = pd.to_datetime(df['date_time'])
            #df.set_index('date_time', inplace=True)

            df.columns = df.columns.str.strip()
            df['location_count'] = [1 for _ in range(len(df))]
            df_freq = df.groupby(['location']).sum()
            df_freq.sort_values(by=['location_count'], ascending=False, inplace=True)
            df_freq = df_freq.head(20)

            #df = df.resample('1S').sum()
            df.dropna(inplace=True)
            #df_freq.columns =
            X = df_freq.index
            Y = df_freq.location_count
            max_y = Y.max() if not Y.empty else 0

            data = [go.Bar(
                    x=X,
                    y=Y,
                    name='location',
                    )]

            return {'data': data, 'layout' : go.Layout(xaxis=dict(automargin=True,title=f"locations"),
                                                    yaxis=dict(range=[0,max_y],title=f"# of tweets"),title=f"locations with the most tweets containing '{input_value}' (up to 20)")}

        except Exception as e:
            with open('errors.txt','a') as f:
                f.write(str(e))
                f.write('\n')

    @dashapp.callback(Output('datatable-row-ids', 'data'),
              [Input('datatable-row-ids', "page_current"),Input('datatable-row-ids', 'page_size'),Input('term_search', 'value')])
    def generate_table(page_current,page_size,input_value):
        try:
            db_connection= sql.connect(user='root', password='', host='127.0.0.1', database='tweets')
            db_cursor = db_connection.cursor()
            df = pd.read_sql('SELECT * FROM sent_trump WHERE content LIKE %s ORDER BY id DESC LIMIT 100', con=db_connection, index_col='id', params=('%' + input_value + '%',))

            #df.sort_values('date_time', inplace=True)
            db_cursor.close()
            db_connection.close()
            return df.iloc[page_current*page_size:(page_current+ 1)*page_size].to_dict('records')

        except Exception as e:
            with open('errors.txt','a') as f:
                f.write(str(e))
                f.write('\n')
