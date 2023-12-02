from dash import Dash, html
from dash import callback_context
from dash.dependencies import Input, Output
from components.col_chart import get_histogram_price, get_histogram_country
from components.map import get_map
from components.table import get_table, get_table_data
from components.time_picker import get_time_bar, get_date_hist
import dash_bootstrap_components as dbc
import pandas as pd

import utils.data_loader as data_loader

SAMPLE_MODE = False

print("Loading data...")
ORIGINAL_FLIGHT_DATA, ORIGINAL_AIRPORT_DATA = data_loader.load_data(SAMPLE_MODE)
flight_data, airport_data = ORIGINAL_FLIGHT_DATA, ORIGINAL_AIRPORT_DATA
grouped_flight_data_counts = flight_data.groupby(['from_airport_code', 'dest_airport_code']).size().reset_index(name='count')
grouped_flight_data_from = pd.merge(grouped_flight_data_counts, airport_data, left_on='from_airport_code', right_on='IATA Code')
grouped_flight_data_to = pd.merge(grouped_flight_data_counts, airport_data, left_on='dest_airport_code', right_on='IATA Code')
ORIGINAL_FLIGHT_DATA_GROUPED = pd.merge(grouped_flight_data_from, grouped_flight_data_to, on=['from_airport_code', 'dest_airport_code', 'count'], suffixes=('_from', '_to')).drop(['IATA Code_from', 'IATA Code_to'], axis=1)
MIN_DAY = ORIGINAL_FLIGHT_DATA['departure_time'].min().date()
MAX_DAY = ORIGINAL_FLIGHT_DATA['departure_time'].max().date()
print("Finished!")

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dbc.NavbarSimple(brand='FlightVis', brand_href='#', color='dark', dark=True),
    dbc.Row(id='graph-container', 
            children=[
                dbc.Col(get_time_bar(flight_data, is_from=True), width=1),
                dbc.Col(get_date_hist(flight_data, MIN_DAY, MAX_DAY), width=6),
                dbc.Col(get_time_bar(flight_data, is_from=False), width=1),
                dbc.Col(get_histogram_price(flight_data), width=3),
                dbc.Col(get_histogram_country(flight_data, is_from=True), width=3),
                dbc.Col(get_histogram_country(flight_data, is_from=False), width=3),
            ],
            className='m-2 p-1'),
    dbc.Row(id='map-container',
            children=[dbc.Col(id='flight-map-from-container', 
                              children=[get_map(ORIGINAL_FLIGHT_DATA_GROUPED, flight_data, airport_data, is_from=True)]), 
                      dbc.Col(id='flight-map-to-container',
                              children=[get_map(ORIGINAL_FLIGHT_DATA_GROUPED, flight_data, airport_data, is_from=False)])],
            className='m-2'),
    dbc.Row(id='table-container', 
            children=[get_table(flight_data)], 
            className='m-2')
])

# If you are going to filter flight_data in any way, use this function here
@app.callback([
    Output('flight-map-from', 'figure'),
    Output('flight-map-to', 'figure'),
    Output('date-hist', 'figure'),
    Output('time-bar-from', 'figure'),
    Output('time-bar-to', 'figure'),
    Output('table', 'data'),
],[
    Input('flight-map-from', 'selectedData'),
    Input('flight-map-to', 'selectedData'),
    Input('date-hist', 'selectedData'),
    Input('time-bar-from', 'selectedData'),
    Input('time-bar-to', 'selectedData'),
])
def update_everything_on_selects(selectedDataFrom, selectedDataTo, dates, timesFrom, timesTo):
    global flight_data, airport_data, ORIGINAL_FLIGHT_DATA_GROUPED, ORIGINAL_FLIGHT_DATA, ORIGINAL_AIRPORT_DATA

    flight_data = ORIGINAL_FLIGHT_DATA

    if selectedDataFrom and selectedDataFrom["points"]:
        flight_data = flight_data[flight_data["from_airport_code"].isin([d["customdata"] for d in selectedDataFrom["points"] if "customdata" in d])]

    if selectedDataTo and selectedDataTo["points"]:
        flight_data = flight_data[flight_data["dest_airport_code"].isin([d["customdata"] for d in selectedDataTo["points"] if "customdata" in d])]

    if dates and dates['points']:
        flight_data = flight_data.loc[flight_data.apply(lambda x: x['departure_time'].strftime('%Y-%m-%d') in [d['x'] for d in dates['points']], axis=1)]
    
    if timesFrom and timesFrom['points']:
        flight_data = flight_data.loc[flight_data.apply(lambda x: x['departure_time'].strftime('%H') in [t['theta'] for t in timesFrom['points']], axis=1)]

    if timesTo and timesTo['points']:
        flight_data = flight_data.loc[flight_data.apply(lambda x: x['arrival_time'].strftime('%H') in [t['theta'] for t in timesTo['points']], axis=1)]

    output_graphs = [
        get_map(ORIGINAL_FLIGHT_DATA_GROUPED, flight_data, airport_data, is_from=True).figure,
        get_map(ORIGINAL_FLIGHT_DATA_GROUPED, flight_data, airport_data, is_from=False).figure,
        get_date_hist(flight_data, MIN_DAY, MAX_DAY).figure,
        get_time_bar(flight_data, is_from=True).figure,
        get_time_bar(flight_data, is_from=False).figure,
        get_table_data(flight_data).to_dict("records")
    ]
    
    return output_graphs

if __name__ == '__main__':
    app.run(debug=True)
