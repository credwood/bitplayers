import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly
import plotly.graph_objs as go

layout = html.Div([
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
        editable=True,
        filter_action="native",
        sort_action="native",
        sort_mode='multi',
        row_selectable='multi',
        row_deletable=True,
        selected_rows=[],
        page_action='native',
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
