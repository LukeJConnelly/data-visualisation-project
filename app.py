import sys
#sys.path.insert(1, '/mnt/c/Users/aaa/Documents/AU/9/DataVisualization/data-visualisation-project/utils')

from datetime import datetime, timedelta
from dash import Dash, html, dash_table
from dash import dcc, callback_context
from dash.dependencies import Input, Output, State
from components.side_bar import get_sidebar
from components.help import get_help_modal
import pytz
from components.map import get_map
from components.time_picker import get_default_time_values, get_time_picker
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

import plotly.graph_objects as go

import utils.data_loader as data_loader
from utils import data_filtering

ORIGINAL_FLIGHT_DATA, ORIGINAL_AIRPORT_DATA = data_loader.load_data()
flight_data, airport_data = ORIGINAL_FLIGHT_DATA, ORIGINAL_AIRPORT_DATA
airport_data.index = airport_data['IATA Code']

flight_data_table = data_filtering.get_unique_flight_routes(flight_data)

ORIGINAL_AIRCRAFT_TYPE_COUNT = data_filtering.get_aircraft_type_count(flight_data)
aircraft_type_count = ORIGINAL_AIRCRAFT_TYPE_COUNT
FILTER_AIRCRAFT_TYPE = False

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

time_options = generate_time_options(30)

# flight_data = flight_data.sample(n=300000).reset_index(drop=True)

#The APP!!!!!! (*o*)

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dbc.NavbarSimple(brand='FlightVis', brand_href='#', color='dark', dark=True),
    dbc.Row(id='container', children=[
        dbc.Col(id='main', children=[
            html.Div(id='main-contents', children=[
                get_time_picker(date_options, time_options), get_help_modal(), get_map(flight_data, airport_data),
                dash_table.DataTable(
                        id='table',
                        columns=[{"name": i, "id": i} 
                                for i in flight_data_table.columns],
                        data=flight_data_table.to_dict('records'),
                        # data=[{key: str(value) for key, value in data_point.items()} for data_point in flight_data_table.to_dict('records')],
                        style_cell=dict(textAlign='left'),
                        style_header=dict(backgroundColor="paleturquoise"),
                        style_data=dict(backgroundColor="lavender")
                    ), 
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
        Output("table", "data"),
        [ Input("flight-map", "selectedData")
         ]
)
def update_table(selectedData):
    global flight_data
    iata_codes = []
    
    if selectedData is not None:
        iata_codes = [data_point["text"] for data_point in selectedData["points"]]
        
    if (len(iata_codes) > 0):
        flight_data = flight_data[(flight_data["from_airport_code"].isin(iata_codes)) | (flight_data["dest_airport_code"].isin(iata_codes))]
    
    flight_data_table = data_filtering.get_unique_flight_routes(flight_data)
    
    data = flight_data_table.to_dict('records')
    return data



@app.callback(
    Output('flight-map', 'figure'),
    [Input('confirm-selection-btn', 'n_clicks'),
     Input("flight-map", "selectedData"),
     Input('aircraft-bar-chart', 'clickData'),
     Input("reset-aircraft-button", "n_clicks"),
     ],
    [
     State('start-date-dropdown', 'value'), State('start-time-dropdown', 'value'),
     State('end-date-dropdown', 'value'), State('end-time-dropdown', 'value')]
)
def update_map(n_clicks, selectedData, selected_aircraft, aircraft_reset_button, start_date, start_time, end_date, end_time):
    global flight_data, FILTER_AIRCRAFT_TYPE
    # global flight_data, FILTER_AIRCRAFT_TYPE
    # iata_codes, a = data_filtering.map_selection(flight_data, selectedData)

    iata_codes = []
    ctx = callback_context
    
    # map select
    if selectedData is not None:
        iata_codes = [data_point["text"] for data_point in selectedData["points"]]

    if (ctx.triggered_id != "flight-map" or selectedData is None):
        # if triggered by brushing over map, keep previous brushing
        # but still empty brushing for reset
        flight_data = ORIGINAL_FLIGHT_DATA
        
    if (len(iata_codes) > 0):
        flight_data = flight_data[(flight_data["from_airport_code"].isin(iata_codes)) | (flight_data["dest_airport_code"].isin(iata_codes))]
    
    # make reset permanent until new choice
    if (callback_context.triggered_id == "reset-aircraft-button"):
        FILTER_AIRCRAFT_TYPE = False
    if (callback_context.triggered_id == "aircraft-bar-chart"):
        FILTER_AIRCRAFT_TYPE = True
    if ((selected_aircraft is not None) and (FILTER_AIRCRAFT_TYPE)):
        # dont apply aircraft filter if aircraft selection is reset or nothing is selected
        aircraft_type = selected_aircraft["points"][0]["x"]
        flight_data = data_filtering.get_flights_with_aircraft_type(flight_data, aircraft_type)
    
#    if from_country != None:
#        flight_data = flight_data[flight_data["from_country"] == from_country]
#    if from_town != None:
#        flight_data = flight_data[flight_data["from_airport_code"] == from_town]

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

# Callback to capture clicked data
@app.callback(
    Output('aircraft-bar-chart', 'figure'),
    [Input('aircraft-bar-chart', 'clickData'),
     Input("reset-aircraft-button", "n_clicks"),
     Input("flight-map", "selectedData"),
     ]
)
def display_clicked_data(clickData, n_clicks, map_selection):
    global aircraft_type_count, flight_data

    ctx = callback_context

    if (ctx.triggered_id == "reset-aircraft-button"):
        aircraft_type_count = ORIGINAL_AIRCRAFT_TYPE_COUNT
        flight_data = ORIGINAL_FLIGHT_DATA
    elif clickData is not None:
        aircraft_type = clickData["points"][0]["x"]
        aircraft_type_count = aircraft_type_count.query(f'aircraft_type == "{aircraft_type}"')
        flight_data = data_filtering.get_flights_with_aircraft_type(flight_data, aircraft_type)

    aircraft_type_bar = px.bar(aircraft_type_count, x='aircraft_type', y='count', title='Flights from/to airport')
    return aircraft_type_bar


@app.callback(
    Output("help-modal", "is_open"),
    [Input("open-help-modal", "n_clicks")],
    [State("help-modal", "is_open")],
)
def toggle_modal(n, is_open):
    if n:
        return not is_open
    return is_open



if __name__ == '__main__':
    app.run(debug=True)
