# -*- coding: utf-8 -*-
"""
Created on Fri Jan 13 15:05:46 2023

@author: pdefalco
"""

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

#import dash_bootstrap_components as dbc

'''
data_GVA = pd.read_excel('GVA Data - Delays prediction - Winter 20222023-01-09.xlsx','InnoHUB - TIMINGS')
data_GVA = data_GVA.rename(columns={'Date':'date_dt','Call Sign - IATA': 'callsign','Arrival - Departure Code':'code'})
df = pd.read_csv('predictions_on_2022-12-26_from_2022-12-27-to-2023-03-25.csv', delimiter=';')
df['date_dt'] = df.apply(lambda x: dt.datetime.strptime(x.date, '%Y-%m-%d'), axis =1)

df= df.merge(data_GVA[['date_dt','callsign','code','UTC Schedule Time']], on = ['date_dt','callsign','code'], how='left')
df.to_csv('dataset_dashboard.csv')
'''
df = pd.read_csv('dataset_dashboard.csv', delimiter=',')
df =df[df['code']=='D']
df['diff'] = df['0.75'] - df['0.25']
app = Dash(__name__)
server = app.server
#server = flask.Flask(__name__)
#dbc_css = ("https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.2/dbc.min.css")
#app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc_css])
#app = Dash(__name__, server=server, external_stylesheets=[dbc.themes.ZEPHYR,dbc_css])
#app.title = 'TVInteractions'

colors = {
    'background': '#111111',
    'text': '#7FDBFF'}


app.layout = html.Div(children=[
    html.H1(children='Predicted Departure Delays at Geneve Airport'),
    dcc.Dropdown(id='dates',
                 options=[{'label':i, 'value':i } for i in df['date'].unique()] ),
    html.Div(children='''
        Quantile predictions
    '''+ str('from  ')+ str(df.sort_values(by='date').iloc[0]['date']) + str('  until  ') + str(df.sort_values(by='date').iloc[-1]['date'])),

    dcc.Graph(
        id='Delay'),
    dcc.Graph(
        id='Delay_1'),
    dcc.Graph(
        id='Delay_2'),
    dcc.Graph(
        id='Difference', 
        ),    

]
)

             

             
@app.callback(
    Output(component_id='Delay', component_property ='figure'),
    Output(component_id='Delay_1', component_property ='figure'),
    Output(component_id='Delay_2', component_property ='figure'),
    Output(component_id='Difference', component_property ='figure'),
    Input(component_id='dates', component_property ='value')
)

def update_plot (selected_date):
    filtered_data = df[df['date']==selected_date]
    fig = px.bar(filtered_data.sort_values(by=['0.5']), x="UTC Schedule Time", y=["0.5"], color="callsign", title='Quantile 0.5' , template='plotly_dark') 
    fig_1 = px.bar(filtered_data.sort_values(by=['0.5']), x="UTC Schedule Time", y=["0.75"], color="callsign", title='Quantile 0.75' ) 
    fig_2 = px.bar(filtered_data.sort_values(by=['0.5']), x="UTC Schedule Time", y=["0.25"], color="callsign", title='Quantile 0.25' ) 
    fig_3 = px.bar(filtered_data.sort_values(by=['0.5']), x="UTC Schedule Time", y=["diff"], color="callsign", title='Quantiles difference (0.75 - 0.25)' )
    return fig, fig_1, fig_2,fig_3

if __name__ == '__main__':
    app.run_server(debug=True)
