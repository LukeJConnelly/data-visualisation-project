from dash import html, dcc
import plotly.express as px

from utils import data_filtering

def get_sidebar(flight_data, airport_data):
    # ? is this just initial? i.e. will this overwrite callbacks or vise verse? 
    aircraft_type_count = data_filtering.get_aircraft_type_count(flight_data)

    return html.Div(id='sidebar-contents', children=[
        html.H3('Stats & Filter'),
        html.Div(
            id='sidebar-graphs',
            children=[
                html.H6('From country'),
                dcc.Dropdown(id='slct-from-country', options=[]),
                #dcc.Checklist(id='slct-all-from-country', options=[{'label': 'Select All', 'value': 1}], values=[]),
                html.H6('To country'),
                dcc.Dropdown(id='to_country'),
                #dcc.Checklist(id='slct-all-to-country', options=[{'label': 'Select All', 'value': 1}], values=[]),
                html.H6('From city'),
                dcc.Dropdown(id='from_town',
                            options = flight_data['from_airport_code'].unique()),
                dcc.Checklist(id='slct-all-from-town',
                            options=[{'label': 'Select All', 'value': 1}]),
                html.H6('To city'),
                dcc.Dropdown(id='to_town',
                            options = flight_data['dest_airport_code'].unique()),
                dcc.Checklist(id='slct-all-to-town',
                            options=[{'label': 'Select All', 'value': 1}]),
                dcc.Graph(id='airport-bar-chart',
                          figure=px.bar(airport_data, x='IATA Code', y='flight_degree', title='Flights from/to airport')),
                dcc.Graph(id='aircraft-bar-chart',
                          figure=px.bar(aircraft_type_count, x='aircraft_type', y='count', title='Flights from/to airport')),
                html.Button('Reset Aircraft Selection', id='reset-aircraft-button'),
                html.H6('Example Graph 1'),
                dcc.Graph(id='example-graph-1'),
                html.H6('Example Graph 2'),
                dcc.Graph(id='example-graph-2')
            ]
        ),
    ])