import sys
#sys.path.insert(1, '/mnt/c/Users/aaa/Documents/AU/9/DataVisualization/data-visualisation-project/utils')

from datetime import datetime, timedelta
from dash import Dash, html, dash_table
from dash import dcc, callback_context
from dash.dependencies import Input, Output, State
from components.side_bar import get_sidebar
from components.line_chart import get_line_chart, create_figure
from components.about import get_about_modal
from components.country_airport_dicts import dest_country_airport_dict, from_country_airport_dict
import pytz
from components.map import get_map
from components.table import get_table, get_table_data
from components.time_picker import get_time_picker
from utils.time import get_date_time_options
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

import utils.data_loader as data_loader
from utils import data_filtering

ORIGINAL_FLIGHT_DATA, ORIGINAL_AIRPORT_DATA = data_loader.load_data()
flight_data, airport_data = ORIGINAL_FLIGHT_DATA, ORIGINAL_AIRPORT_DATA
airport_data.index = airport_data['IATA Code']


ORIGINAL_AIRCRAFT_TYPE_COUNT = data_filtering.get_aircraft_type_count(flight_data)
aircraft_type_count = ORIGINAL_AIRCRAFT_TYPE_COUNT
FILTER_AIRCRAFT_TYPE = False

flight_data['departure_time'] = pd.to_datetime(flight_data['departure_time'])
date_options, time_options = get_date_time_options(flight_data['departure_time'])

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dbc.NavbarSimple(brand='FlightVis', brand_href='#', color='dark', dark=True),
    dbc.Row(id='container', children=[
        dbc.Col(id='main', children=[
            html.Div(id='main-contents', children=[
                get_time_picker(date_options, time_options), get_map(flight_data, airport_data), get_about_modal(), get_table(flight_data)
            ])
        ], width=9),
        dbc.Col(id='sidebar', children=[get_sidebar(flight_data, airport_data, from_country_airport_dict, dest_country_airport_dict)], width=3)
    ], className='p-5')
])


@app.callback(
    Output('flight-map', 'figure'),
    [
        Input("flight-map", "selectedData"),
        Input('aircraft-bar-chart', 'clickData'),
        Input("reset-aircraft-button", "n_clicks"),
        Input('from_country', 'value'),
        Input('dest_country', 'value'),
        Input("date-hist", "selectedData"),
        Input('time-bar', "selectedData")
    ],
)
def update_map(selectedData, selected_aircraft, aircraft_reset_button, from_country, dest_country, dates, times):
    global airport_data, flight_data, FILTER_AIRCRAFT_TYPE, ORIGINAL_AIRPORT_DATA, ORIGINAL_FLIGHT_DATA

    iata_codes = []
    ctx = callback_context

    airport_data = ORIGINAL_AIRPORT_DATA

    
    flight_data = flight_data
    if(ctx.triggered_id == "flight-map" and (selectedData is None or len(selectedData["points"]) == 0)):
        flight_data = ORIGINAL_FLIGHT_DATA
    
    # map select
    if selectedData is not None:
        print(selectedData["points"])
        iata_codes = [data_point["text"][:3] for data_point in selectedData["points"] if "text" in data_point and not '(' in data_point["text"]]
        
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

    if from_country != None and from_country != []:
        flight_data = flight_data.loc[flight_data['from_country'].isin(from_country)]
    # if from_airport_code != None and from_airport_code != []:
    #     flight_data = flight_data.loc[flight_data['from_airport_code'].isin(from_airport_code)]
    if dest_country != None and dest_country != []:
        flight_data = flight_data.loc[flight_data['dest_country'].isin(dest_country)]
    # if dest_airport_code != None and dest_airport_code != []:
        # Convert start and end dates to datetime objects

    if dates:
        flight_data = flight_data.loc[flight_data.apply(lambda x: x['departure_time'].strftime('%Y-%m-%d') in [d['x'] for d in dates['points']], axis=1)]
    if times:
        flight_data = flight_data.loc[flight_data.apply(lambda x: x['departure_time'].strftime('%H') in [t['theta'] for t in times['points']], axis=1)]
    
    airport_data = airport_data[(airport_data["IATA Code"].isin(flight_data["from_airport_code"])) | (airport_data["IATA Code"].isin(flight_data["dest_airport_code"]))]

    return get_map(flight_data, airport_data).figure 

######################################################################################
@app.callback(
        Output("table", "data"),
        [Input("flight-map", "figure")
         ]
)
def update_table(_):
    global flight_data
    return get_table_data(flight_data).to_dict("records")

@app.callback(
        Output("airport-bar-chart", "figure"),
        [Input("flight-map", "figure")]
)
def update_iata_bar_chart(_):
    global flight_data, airport_data
    return px.bar(airport_data, x='IATA Code', y='flight_degree', title='Flights from/to airport')

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

# @app.callback(
#     Output('line-chart', 'figure'),
#     [Input('y-axis-dropdown', 'value')]
# )
# def update_chart(selected_y_column):
#     return create_figure(flight_data, selected_y_column)


if __name__ == '__main__':
    app.run(debug=True)
