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
from components.time_picker import get_time_picker
from utils.time import get_date_time_options
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

# ORIGINAL_AIRCRAFT_TYPE_COUNT = 
aircraft_type_count = data_filtering.get_aircraft_type_count(flight_data)
FILTER_AIRCRAFT_TYPE = False

flight_data['departure_time'] = pd.to_datetime(flight_data['departure_time'])
date_options, time_options = get_date_time_options(flight_data['departure_time'])

COLOURING_CHOICES = ['price', 'co2_emissions'] # duration, stops, none
choice = 0

QUANTILES = {
    k: [flight_data.groupby(['from_airport_code', 'dest_airport_code'])[k]
         .mean().reset_index(name=k)[k].quantile(i) 
         for i in [0.25, 0.5, 0.75]
    ]
    for k in COLOURING_CHOICES
}

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dbc.NavbarSimple(brand='FlightVis', brand_href='#', color='dark', dark=True),
    dbc.Row(id='container', children=[
        dbc.Col(id='main', children=[
            html.Div(id='main-contents', children=[
                get_time_picker(date_options, time_options), get_map(flight_data, airport_data, COLOURING_CHOICES[choice], QUANTILES[COLOURING_CHOICES[choice]]), get_about_modal(),
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
                # get_time_picker(date_options, time_options), get_map(flight_data, airport_data), 
            # ])
        ], width=9),
        dbc.Col(id='sidebar', children=[get_sidebar(flight_data, airport_data, from_country_airport_dict, dest_country_airport_dict)], width=3)
    ], className='p-5')
])


@app.callback(
        Output("airport-bar-chart", "figure"),
        [Input("flight-map", "figure")
        # [Input("flight-map", "selectedData")
         ]
)
def update_aita_bar_chart(flight_map_fig):
    global flight_data, airport_data, ORIGINAL_AIRPORT_DATA

    airport_data = airport_data[(ORIGINAL_AIRPORT_DATA["IATA Code"].isin(flight_data["from_airport_code"])) | (ORIGINAL_AIRPORT_DATA["IATA Code"].isin(flight_data["dest_airport_code"]))]
    return px.bar(airport_data, x='IATA Code', y='flight_degree', title='Flights from/to airport')

@app.callback(
        Output("table", "data"),
        [Input("flight-map", "figure")
        # [Input("flight-map", "selectedData")
         ]
)
def update_table(selectedData):
    global flight_data
    
    flight_data_table = data_filtering.get_unique_flight_routes(flight_data)
    
    data = flight_data_table.to_dict('records')
    return data


# @app.callback(
#     Output('flight-map', 'figure'),
#     [Input('confirm-selection-btn', 'n_clicks'), Input('flight-map', "selectedData"), Input()],
#     [State('start-date-dropdown', 'value'), State('start-time-dropdown', 'value'),
#     State('end-date-dropdown', 'value'), State('end-time-dropdown', 'value')]
# )
# def update_map(n_clicks, selectedData, selected_aircraft, aircraft_reset_button, start_date, start_time, end_date, end_time):
#     global flight_data, FILTER_AIRCRAFT_TYPE
    # global flight_data, FILTER_AIRCRAFT_TYPE
    # iata_codes, a = data_filtering.map_selection(flight_data, selectedData)
# def update_map(n_clicks, start_date, start_time, end_date, end_time):

@app.callback(
    Output('flight-map', 'figure'),
    [Input("flight-map", "selectedData"),
    Input('aircraft-bar-chart', 'clickData'),
    Input("reset-aircraft-button", "n_clicks"),
    Input('from_country', 'value'),
    Input('dest_country', 'value'),
    Input("date-hist", "selectedData"),
    Input('time-bar', "selectedData")
    ],
)
def update_map(selectedData, selected_aircraft, aircraft_reset_button, from_country, dest_country, dates, times):

    global flight_data, FILTER_AIRCRAFT_TYPE, ORIGINAL_AIRPORT_DATA

    # print("Selected data:", selectedData)

    iata_codes = []
    ctx = callback_context

    # flight_data = ORIGINAL_FLIGHT_DATA
    airport_data = ORIGINAL_AIRPORT_DATA

    # flight_data = data_filtering.map_selection(ctx, flight_data, selectedData, ORIGINAL_FLIGHT_DATA)
    # map select
    if selectedData is not None:
        iata_codes = [data_point["text"][:3] for data_point in selectedData["points"]]

    # if (ctx.triggered_id != "flight-map" or selectedData is None):
        # if triggered by brushing over map, keep previous brushing
        # but still empty brushing for reset
    if (ctx.triggered_id == "flight-map" and selectedData is None):
        flight_data = ORIGINAL_FLIGHT_DATA
    elif (ctx.triggered_id != "flight-map"):
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

    if from_country != None and from_country != []:
        flight_data = flight_data.loc[flight_data['from_country'].isin(from_country)]
    # if from_airport_code != None and from_airport_code != []:
    #     flight_data = flight_data.loc[flight_data['from_airport_code'].isin(from_airport_code)]
    if dest_country != None and dest_country != []:
        flight_data = flight_data.loc[flight_data['dest_country'].isin(dest_country)]
    # if dest_airport_code != None and dest_airport_code != []:
        # Convert start and end dates to datetime objects

    filtered_data = flight_data

    if dates:
        filtered_data = filtered_data.loc[filtered_data.apply(lambda x: x['departure_time'].strftime('%Y-%m-%d') in [d['x'] for d in dates['points']], axis=1)]
    if times:
        filtered_data = filtered_data.loc[filtered_data.apply(lambda x: x['departure_time'].strftime('%H') in [t['theta'] for t in times['points']], axis=1)]
    
    return get_map(filtered_data, airport_data, COLOURING_CHOICES[choice], QUANTILES[COLOURING_CHOICES[choice]]).figure 
    #     flight_data = flight_data.loc[flight_data['dest_airport_code'].isin(dest_airport_code)]

    # return get_map(flight_data, airport_data).figure

# Callback to capture clicked data
@app.callback(
    Output('aircraft-bar-chart', 'figure'),
    [Input('aircraft-bar-chart', 'clickData'),
     Input("reset-aircraft-button", "n_clicks"),
     Input("flight-map", "figure"),
     ]
)
def display_clicked_data(clickData, n_clicks, map_figure):
    global aircraft_type_count, flight_data

    ctx = callback_context

    # if (ctx.triggered_id == "reset-aircraft-button"):
    #     aircraft_type_count = ORIGINAL_AIRCRAFT_TYPE_COUNT
    #     flight_data = ORIGINAL_FLIGHT_DATA
    if clickData is not None:
        aircraft_type = clickData["points"][0]["x"]
        aircraft_type_count = aircraft_type_count.query(f'aircraft_type == "{aircraft_type}"')
        flight_data = data_filtering.get_flights_with_aircraft_type(flight_data, aircraft_type)
    
    aircraft_type_count = data_filtering.get_aircraft_type_count(flight_data)

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
