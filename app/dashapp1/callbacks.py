from datetime import datetime as dt
from dash.dependencies import Input
from dash.dependencies import Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly
import plotly.graph_objs as go
import pandas as pd
import mysql.connector as sql


def register_callbacks(dashapp):
    @dashapp.callback(Output('live-graph', 'figure'),
              [Input('graph-update', 'n_intervals')])
    def update_graph_call(n):
        try:
            db_connection = sql.connect(user='root', password='',
                                          host='127.0.0.1',
                                          database='tweets')

            db_cursor = db_connection.cursor()
            df = pd.read_sql('SELECT * FROM sent_trump ORDER BY id DESC LIMIT 1000', con=db_connection, index_col='id')
            #df.sort_values('date_time', inplace=True)
            df["rolling_textblob_ave"] = df["sentiment_textblob"].rolling(int(len(df)/2)).mean()
            df["rolling_vader_ave"] = df["sentiment_vader"].rolling(int(len(df)/2)).mean()

            df['date_time'] = pd.to_datetime(df['date_time'])
            df.set_index('date_time', inplace=True)

            df = df.resample('1S').mean()
            df.dropna(inplace=True)
            X = df.index
            Y1 = df.rolling_textblob_ave
            Y2 = df.rolling_vader_ave
            max_r = max(max(Y1), max(Y2))
            min_r = min(min(Y1), min(Y2))

            data = [go.Scatter(
                    x=X,
                    y=Y1,
                    name='textblob',
                    mode= 'lines+markers'
                    ), go.Scatter(
                            x=X,
                            y=Y2,
                            name='vader',
                            mode= 'lines+markers'
                            )]

            return {'data': data, 'layout' : go.Layout(xaxis=dict(range=[min(X),max(X)]),
                                                    yaxis=dict(range=[min_r,max_r]))}

        except Exception as e:
            with open('errors.txt','a') as f:
                f.write(str(e))
                f.write('\n')
