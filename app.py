import sys
#sys.path.insert(1, '/mnt/c/Users/aaa/Documents/AU/9/DataVisualization/data-visualisation-project/utils')

from datetime import datetime, timedelta
from dash import Dash, html
from dash import dcc, callback_context
from dash.dependencies import Input, Output, State
from components.side_bar import get_sidebar
from components.line_chart import get_line_chart, create_figure
from components.about import get_about_modal
from components.country_airport_dicts import dest_country_airport_dict, from_country_airport_dict
import pytz
from components.map import get_map
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
                get_time_picker(date_options, time_options), get_map(flight_data, airport_data), get_about_modal(),
                get_line_chart(flight_data)
            ])
        ], width=9),
        # dbc.Col(id='sidebar', children=[get_sidebar(flight_data, airport_data, from_country_airport_dict, dest_country_airport_dict)], width=3)
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
        start_date, start_time, end_date, end_time = date_options[0]['value'], time_options[0]['value'], date_options[-1]['value'], time_options[-1]['value']
    
    return html.Div([
        html.Span("Start Time: ", style={'font-weight': 'bold'}),
        html.Span(f"{start_date} {start_time}, "),
        html.Span("End Time: ", style={'font-weight': 'bold'}),
        html.Span(f"{end_date} {end_time}")
    ])

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
        # Convert start and end dates to datetime objects
    start_datetime = pd.to_datetime(f'{start_date} {start_time}')
    end_datetime = pd.to_datetime(f'{end_date} {end_time}')

    # Filter by date and time range
    filtered_data = flight_data[
        (flight_data['departure_time'] >= start_datetime) & 
        (flight_data['departure_time'] <= end_datetime)
    ]

    return get_map(filtered_data, airport_data).figure 

# @app.callback(
#     Output('flight-map', 'figure'),
#     [Input('confirm-selection-btn', 'n_clicks')],
#     Input("flight-map", "selectedData"),
#     Input('aircraft-bar-chart', 'clickData'),
#     Input("reset-aircraft-button", "n_clicks"),
#     Input('from_country', 'value'),
#     Input('dest_country', 'value'),
#     [State('start-date-dropdown', 'value'), State('start-time-dropdown', 'value'),
#     State('end-date-dropdown', 'value'), State('end-time-dropdown', 'value')]
# )
# def update_map(n_clicks, selectedData, selected_aircraft, aircraft_reset_button, from_country, dest_country, start_date, start_time, end_date, end_time):

#     global flight_data, FILTER_AIRCRAFT_TYPE

#     iata_codes = []
#     ctx = callback_context
    
#     # map select
#     if selectedData is not None:
#         iata_codes = [data_point["text"] for data_point in selectedData["points"]]

#     if (ctx.triggered_id != "flight-map" or selectedData is None):
#         # if triggered by brushing over map, keep previous brushing
#         # but still empty brushing for reset
#         flight_data = ORIGINAL_FLIGHT_DATA
        
#     if (len(iata_codes) > 0):
#         flight_data = flight_data[(flight_data["from_airport_code"].isin(iata_codes)) | (flight_data["dest_airport_code"].isin(iata_codes))]
    
#     # make reset permanent until new choice
#     if (callback_context.triggered_id == "reset-aircraft-button"):
#         FILTER_AIRCRAFT_TYPE = False
#     if (callback_context.triggered_id == "aircraft-bar-chart"):
#         FILTER_AIRCRAFT_TYPE = True
#     if ((selected_aircraft is not None) and (FILTER_AIRCRAFT_TYPE)):
#         # dont apply aircraft filter if aircraft selection is reset or nothing is selected
#         aircraft_type = selected_aircraft["points"][0]["x"]
#         flight_data = data_filtering.get_flights_with_aircraft_type(flight_data, aircraft_type)

#     if from_country != None and from_country != []:
#         flight_data = flight_data.loc[flight_data['from_country'].isin(from_country)]
#     # if from_airport_code != None and from_airport_code != []:
#     #     flight_data = flight_data.loc[flight_data['from_airport_code'].isin(from_airport_code)]
#     if dest_country != None and dest_country != []:
#         flight_data = flight_data.loc[flight_data['dest_country'].isin(dest_country)]
#     # if dest_airport_code != None and dest_airport_code != []:
#     #     flight_data = flight_data.loc[flight_data['dest_airport_code'].isin(dest_airport_code)]

#     if(n_clicks > 0):
#         flight_data['departure_time'] = pd.to_datetime(flight_data['departure_time'])
#         start_date = pd.to_datetime(f'{start_date} {start_time}').date()
#         end_date = pd.to_datetime(f'{end_date} {end_time}').date()

#         # Perform the comparison
#         filtered_data = flight_data[
#             (flight_data['departure_time'].dt.date >= start_date) & 
#             (flight_data['departure_time'].dt.date <= end_date) &
#             (((flight_data['departure_time'].dt.time >= datetime.strptime(start_time, '%H:%M').time()) &
#             (flight_data['departure_time'].dt.time <= datetime.strptime(end_time, '%H:%M').time()))
#              if flight_data['departure_time'].dt.date == end_date else True)
#         ]

#         updated_figure = get_map(filtered_data, airport_data).figure 

#         return updated_figure
    
#     return get_map(flight_data, airport_data).figure

# Callback to capture clicked data
@app.callback(
    Output('aircraft-bar-chart', 'figure'),
    [Input('aircraft-bar-chart', 'clickData'),
     Input("reset-aircraft-button", "n_clicks"),
     ]
)
def display_clicked_data(clickData, n_clicks):
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

@app.callback(
    Output('line-chart', 'figure'),
    [Input('y-axis-dropdown', 'value')]
)
def update_chart(selected_y_column):
    return create_figure(flight_data, selected_y_column).figure


if __name__ == '__main__':
    app.run(debug=True)
