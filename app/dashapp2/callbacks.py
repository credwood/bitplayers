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


def register_callbacks(dashapp):

    @dashapp.callback(Output('freq-graph', 'figure'),
              [Input('term-freq', 'value')])
    def update_graph_call(input_value):
        try:
            db_connection = sql.connect(user='root', password='',
                                          host='127.0.0.1',
                                          database='tweets')

            db_cursor = db_connection.cursor()
            df = pd.read_sql('SELECT * FROM sent_trump WHERE content LIKE %s ORDER BY id DESC LIMIT 1000', con=db_connection, index_col='id', params=('%' + input_value + '%',))
            #df.sort_values('date_time', inplace=True)
            db_cursor.close()
            db_connection.close()

            df["rolling_vader_ave"] = df["sentiment_vader"].rolling(int(len(df)/2)).mean()
            df['dummy_count'] = [1 for _ in range(len(df))]
            df['date_time'] = pd.to_datetime(df['date_time'])
            df.set_index('date_time', inplace=True)
            dates_group = df.groupby('date_time')
            df["search_freq"] = dates_group['dummy_count'].agg(sum)

            df = df.resample('1s').mean()
            df.dropna(inplace=True)
            X = df.index
            Y1 = df.search_freq
            #Y2 = df.rolling_vader_ave
            min_x = X.min() if not X.empty else 0
            max_x = X.max() if not X.empty else 0
            max_y = Y1.max() if not Y1.empty else 0

            data= [go.Bar(
                    x=X,
                    y=Y1,
                    name='frequency of search term',
                    )]

            return {'data': data, 'layout' : go.Layout(xaxis=dict(range=[min_x,max_x]),
                                                    yaxis=dict(range=[0,max_y+1]))}

        except Exception as e:
            with open('errors.txt','a') as f:
                f.write(str(e))
                f.write('\n')

    @dashapp.callback(Output('datatable-row-ids', 'data'),
              [Input('datatable-row-ids', "page_current"),Input('datatable-row-ids', 'page_size'), Input('term-freq', 'value')])
    def generate_table(page_current,page_size, input_value):
        try:
            db_connection= sql.connect(user='root', password='', host='127.0.0.1', database='tweets')
            cur = db_connection.cursor()
            df = pd.read_sql('SELECT * FROM sent_trump WHERE content LIKE %s ORDER BY id DESC LIMIT 15', con=db_connection,index_col='id', params=('%' + input_value + '%',))
            #df.sort_values('date_time', inplace=True)
            cur.close()
            db_connection.close()
            return df.iloc[page_current*page_size:(page_current+ 1)*page_size].to_dict('records')

        except Exception as e:
            with open('errors.txt','a') as f:
                f.write(str(e))
                f.write('\n')
