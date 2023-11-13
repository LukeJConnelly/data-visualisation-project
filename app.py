import sys
#sys.path.insert(1, '/mnt/c/Users/aaa/Documents/AU/9/DataVisualization/data-visualisation-project/utils')

from datetime import datetime, timedelta
from dash import Dash, html
from dash import dcc
from dash.dependencies import Input, Output, State
from components.help import get_help_modal
import pytz
from components.map import get_map
from components.time_picker import get_default_time_values, get_time_picker
import utils.data_loader as data_loader
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

flight_data, airport_data = data_loader.load_data()
airport_data.index = airport_data['IATA Code']

unique_dates = pd.to_datetime(flight_data['departure_time']).dt.date.dropna().unique()
unique_dates = sorted(unique_dates)  # Convert to set for uniqueness, then sort

date_options = [{'label': pd.to_datetime(date).strftime('%Y-%m-%d'), 'value': date} for date in unique_dates]

def generate_time_options(interval_minutes=30):
    start_time = datetime(2000, 1, 1, 0, 0)
    end_time = datetime(2000, 1, 2, 0, 0)

    time_options = []
    current_time = start_time
    while current_time < end_time:
        time_str = current_time.strftime('%H:%M')
        time_options.append({'label': time_str, 'value': time_str})
        current_time += timedelta(minutes=interval_minutes)

    return time_options

# Generate time options
time_options = generate_time_options(30)

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
                get_time_picker(date_options, time_options), get_help_modal(), get_map(flight_data, airport_data)
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

@app.callback(
    [Output('warning-message', 'children'), 
     Output('confirm-selection-btn', 'disabled')],
    [Input('start-date-dropdown', 'value'), Input('start-time-dropdown', 'value'),
     Input('end-date-dropdown', 'value'), Input('end-time-dropdown', 'value')]
)
def validate_datetime(start_date, start_time, end_date, end_time):
    start_datetime = pd.to_datetime(f'{start_date} {start_time}')
    end_datetime = pd.to_datetime(f'{end_date} {end_time}')

    if end_datetime < start_datetime:
        return "End date-time cannot be before start date-time.", True
    return "", False

@app.callback(
    Output('flight-map', 'figure'),
    [Input('confirm-selection-btn', 'n_clicks')],
    [State('start-date-dropdown', 'value'), State('start-time-dropdown', 'value'),
     State('end-date-dropdown', 'value'), State('end-time-dropdown', 'value')]
)
def update_map(n_clicks, start_date, start_time, end_date, end_time):
    if(n_clicks > 0):
        flight_data['departure_time'] = pd.to_datetime(flight_data['departure_time'])
        start_date = pd.to_datetime(f'{start_date} {start_time}').date()
        end_date = pd.to_datetime(f'{end_date} {end_time}').date()


        # Perform the comparison
        filtered_data = flight_data[
            (flight_data['departure_time'].dt.date >= start_date) & 
            (flight_data['departure_time'].dt.date <= end_date)
        ]

        updated_figure = get_map(filtered_data, airport_data).figure 

        return updated_figure
    
    return get_map(flight_data, airport_data).figure

@app.callback(
    Output("help-modal", "is_open"),
    [Input("open-help-modal", "n_clicks"), Input("close-help-modal", "n_clicks")],
    [State("help-modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open



if __name__ == '__main__':
    app.run(debug=True)
