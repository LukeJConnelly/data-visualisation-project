import sys
#sys.path.insert(1, '/mnt/c/Users/aaa/Documents/AU/9/DataVisualization/data-visualisation-project/utils')

from dash import Dash, html
from dash.dependencies import Input, Output, State
from components.map import get_map
from components.time_picker import get_default_time_values, get_time_picker
import utils.data_loader as data_loader
import dash_bootstrap_components as dbc
import plotly.express as px

flight_data, airport_data = data_loader.load_data()
airport_data.index = airport_data['IATA Code']

date_options = [{'label': 'Date 1', 'value': '2023-01-01'},
        {'label': 'Date 2', 'value': '2023-01-02'}]
time_options = [{'label': 'Time 1', 'value': '00:00'},
        {'label': 'Time 2', 'value': '01:00'}]

# flight_data = flight_data.sample(n=300000).reset_index(drop=True)

# Sidebar function
def get_sidebar(flight_data, airport_data):
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
                html.H6('Example Graph 1'),
                dcc.Graph(id='example-graph-1'),
                html.H6('Example Graph 2'),
                dcc.Graph(id='example-graph-2')
            ]
        ),
    ])

#The APP!!!!!! (*o*)

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


app.layout = html.Div([
    dbc.NavbarSimple(brand='FlightVis', brand_href='#', color='dark', dark=True),
    dbc.Row(id='container', children=[
        dbc.Col(id='main', children=[
            html.Div(id='main-contents', children=[
                get_time_picker(date_options, time_options), get_map(flight_data, airport_data)
            ])
        ], width=9),
        dbc.Col(id='sidebar', children=[get_sidebar(flight_data, airport_data)], width=3)
    ], className='p-5')
])


@app.callback(
    Output("datetime-modal", "is_open"),
    [Input("open-modal-btn", "n_clicks"), Input("confirm-selection-btn", "n_clicks")],
    [State("datetime-modal", "is_open")],
)
def toggle_time_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    Output('current-datetime', 'children'),
    [Input('confirm-selection-btn', 'n_clicks')],
    [State('start-date-dropdown', 'value'), State('start-time-dropdown', 'value'),
     State('end-date-dropdown', 'value'), State('end-time-dropdown', 'value')]
)
def update_datetime(n_clicks, start_date, start_time, end_date, end_time):
    if not n_clicks:
        start_date, start_time, end_date, end_time = get_default_time_values(date_options, time_options)
    
    return f"Start Time: {start_date} {start_time}, End Time: {end_date} {end_time}"

if __name__ == '__main__':
    app.run(debug=True)
