
from dash import html, dcc

def get_sidebar(flight_data, airport_data, from_country_airport_dict, dest_country_airport_dict):
    return html.Div(id='sidebar-contents', children=[
        html.H3('Stats & Filter'),
        html.Div(
            id='sidebar-graphs',
            children=[
                html.H6('Departure Country:'),
                dcc.Dropdown(id='from_country', options=list(from_country_airport_dict.keys()), multi = True),
                html.H6('Arrival Country:'),
                dcc.Dropdown(id='dest_country', options=list(flight_data.dest_country.unique()), multi = True),
                html.H6('Example Graph 1'),
                dcc.Graph(id='example-graph-1'),
                html.H6('Example Graph 2'),
                dcc.Graph(id='example-graph-2')
            ]
        ),
    ])