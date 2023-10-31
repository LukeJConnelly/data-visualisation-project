#!/usr/bin/python
# -*- coding: utf-8 -*-
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from utils import data_loader
import dash_bootstrap_components as dbc

df = pd.read_csv('data/flights.csv')

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

airport_data = pd.DataFrame({'lat': [0, 50], 'lon': [0, 50]}, index=['ETC', 'DUH'])
flight_data = pd.DataFrame({'src': ['ETC'], 'dest': ['DUH']}, index=['3X4MPL3'])

def get_timepicker():
    return html.Div('Time picker here')

def get_map():
    fig = go.Figure()
    # AIRPORTS
    fig.add_trace(go.Scattermapbox(lat=airport_data['lat'],
                                   lon=airport_data['lon'],
                                   mode='markers',
                                   marker=go.scattermapbox.Marker(size=5, color='black'),
                                   text=airport_data.index))
    # FLIGHTS
    for i in range(len(flight_data)):
        # lookup needs cleaning
        fig.add_trace(
                    go.Scattermapbox(
                        mode='lines',
                        lat=[airport_data.loc[flight_data.iloc[i]['src'], 'lat'], airport_data.loc[flight_data.iloc[i]['dest'], 'lat']],
                        lon=[airport_data.loc[flight_data.iloc[i]['src'], 'lon'], airport_data.loc[flight_data.iloc[i]['dest'], 'lon']],
                        line=go.scattermapbox.Line(
                            width=1,
                            color="red"
                        ),
                        name=str(flight_data.index[i])
                    )
                )
    fig.update_layout(mapbox_style='open-street-map', margin={'r': 0, 't': 0, 'l': 0, 'b': 0,})
    return dcc.Graph(id='map', figure=fig)


def get_sidebar():
    return html.Div(id='sidebar-contents', children=[
        html.H3('Stats & Filter'),
        html.Div(
            id='sidebar-graphs',
            children=[
                html.H6('Example Graph 1'),
                dcc.Graph(id='example-graph-1'),
                html.H6('Example Graph 2'),
                dcc.Graph(id='example-graph-2')
            ]
        ),
    ])


app.layout = html.Div([
    dbc.NavbarSimple(brand='FlightVis', brand_href='#', color='dark', dark=True),
    dbc.Row(id='container', children=[
        dbc.Col(id='main', children=[
            html.Div(id='main-contents', children=[
                get_timepicker(), get_map()
            ])
        ], width=9),
        dbc.Col(id='sidebar', children=[get_sidebar()], width=3)
    ], className='p-5')
])

# callback such as this can be used to update the graph
# @callback(
#     Output('graph-content', 'figure'),
#     Input('dropdown-selection', 'value')
# )
# def update_graph(value):
#     dff = df[df.country==value]
#     return px.line(dff, x='year', y='pop')

if __name__ == '__main__':
    app.run(debug=True)
