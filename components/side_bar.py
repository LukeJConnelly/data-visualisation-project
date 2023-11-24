
from dash import html, dcc
import plotly.express as px

from utils import data_filtering

def get_sidebar(flight_data, airport_data, from_country_airport_dict, dest_country_airport_dict):
    # ? is this just initial? i.e. will this overwrite callbacks or vise verse? 
    aircraft_type_count = data_filtering.get_aircraft_type_count(flight_data)
    return html.Div(id='sidebar-contents', children=[
        html.H3('Stats & Filter'),
        html.Div(
            id='sidebar-graphs',
            children=[
                html.H6('Departure Country:'),
                dcc.Dropdown(id='from_country', options=list(from_country_airport_dict.keys()), multi = True),
                html.H6('Arrival Country:'),
                dcc.Dropdown(id='dest_country', options=list(flight_data.dest_country.unique()), multi = True),
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