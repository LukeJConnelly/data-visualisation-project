from dash import Dash, html, callback_context, no_update
from dash.dependencies import Input, Output
from components.col_chart import get_histogram_price, get_histogram_country, get_histogram_duration, get_histogram_co2, get_histogram_airline
from components.map import get_map
from components.matrix import get_matrix
from components.table import get_table, get_table_data, get_table_header_styling
from components.time_picker import get_time_bar, get_date_hist, get_days_of_week_hist
from components.legend import get_legend
import dash_bootstrap_components as dbc
import pandas as pd
from functools import reduce
from utils.settings import get_colours, set_colour_blind_mode
from utils.airport_country_mapping import get_flight_df_with_country

from utils import data_loader

SAMPLE_MODE = False

print("Loading data...")
ORIGINAL_FLIGHT_DATA, ORIGINAL_AIRPORT_DATA = data_loader.load_data(SAMPLE_MODE)
flight_data, airport_data = get_flight_df_with_country(ORIGINAL_FLIGHT_DATA, ORIGINAL_AIRPORT_DATA), ORIGINAL_AIRPORT_DATA
grouped_flight_data_counts = flight_data.groupby(['from_airport_code', 'dest_airport_code']).size().reset_index(name='count')
grouped_flight_data_from = pd.merge(grouped_flight_data_counts, airport_data, left_on='from_airport_code', right_on='IATA Code')
grouped_flight_data_to = pd.merge(grouped_flight_data_counts, airport_data, left_on='dest_airport_code', right_on='IATA Code')
ORIGINAL_FLIGHT_DATA_GROUPED = pd.merge(grouped_flight_data_from, grouped_flight_data_to, on=['from_airport_code', 'dest_airport_code', 'count'], suffixes=('_from', '_to')).drop(['IATA Code_from', 'IATA Code_to'], axis=1)
MIN_DAY = ORIGINAL_FLIGHT_DATA['departure_time'].min().date()-pd.Timedelta(days=1)
MAX_DAY = ORIGINAL_FLIGHT_DATA['departure_time'].max().date()+pd.Timedelta(days=1)
time_column_suffix = ''
print("Finished!")

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dbc.NavbarSimple(brand='FlightVis', brand_href='#', color='dark', dark=True, 
                     children=[dbc.NavItem(dbc.Label("Use Local times")), 
                               dbc.NavItem(html.Div(dbc.Checklist(options=[{"label": "", "value": 1}],
                                                value=[0],id="timezone-input",switch=True))),
                               dbc.NavItem(dbc.Label("Use GMT times")),
                               dbc.NavItem(dbc.Label("Colourblind mode", class_name="colourblind-label")), 
                               dbc.NavItem(dbc.Checklist(options=[{"label": "", "value": 1}],
                                                         value=[0],id="colorblind-mode-input",switch=True))]),
    dbc.Row(id='graph-container', 
            children=[
                dbc.Col(get_time_bar(flight_data, time_column_suffix, is_from=True), width=1),
                dbc.Col(get_time_bar(flight_data, time_column_suffix, is_from=False), width=1),
                dbc.Col(get_date_hist(flight_data, time_column_suffix, MIN_DAY, MAX_DAY), width=6),
                dbc.Col(get_days_of_week_hist(flight_data, time_column_suffix), width=2),
                dbc.Col(get_histogram_price(flight_data), width=3),
                dbc.Col(get_histogram_country(flight_data, airport_data, get_colours(), is_from=True), width=4),
                dbc.Col(get_histogram_country(flight_data, airport_data, get_colours(), is_from=False), width=4),
                dbc.Col(get_histogram_duration(flight_data), width=3),
                dbc.Col(get_histogram_co2(flight_data), width=3),
                dbc.Col(get_histogram_airline(flight_data), width=4),
            ],
            className='m-2 p-1'),
    dbc.Row(id='map-container',
            children=[dbc.Col(id='flight-map-from-container',
                              children=[get_map(ORIGINAL_FLIGHT_DATA_GROUPED, flight_data, airport_data, is_from=True)]),
                      dbc.Col(id='legend', children=get_legend(*get_colours()), width=1),
                      dbc.Col(id='flight-map-to-container',
                              children=[get_map(ORIGINAL_FLIGHT_DATA_GROUPED, flight_data, airport_data, is_from=False)])],
            className='m-2'),
    dbc.Row(id='table-container', 
            children=[
                #get_histogram_price(flight_data),
                        get_matrix(flight_data, airport_data) if not SAMPLE_MODE else None,
                        get_table(flight_data, airport_data),
            ], 
            className='m-2'),
])

# If you are going to filter flight_data in any way, use this function here
@app.callback([
    Output('flight-map-from', 'figure'),
    Output('flight-map-to', 'figure'),
    Output('date-hist', 'figure'),
    Output('time-bar-from', 'figure'),
    Output('time-bar-to', 'figure'),
    Output('days-of-week-hist', 'figure'),
    Output('price-hist', 'figure'),
    Output('duration-hist', 'figure'),
    Output('co2-hist', 'figure'),
    Output('country-hist-from', 'figure'),
    Output('country-hist-to', 'figure'),
    Output('airline-hist', 'figure'),
    Output('table', 'data'),
    Output('table', 'style_header_conditional'),
    Output('legend', 'children'),
],[
    Input('flight-map-from', 'selectedData'),
    Input('flight-map-to', 'selectedData'),
    Input('date-hist', 'selectedData'),
    Input('time-bar-from', 'selectedData'),
    Input('time-bar-to', 'selectedData'),
    Input('days-of-week-hist', 'selectedData'),
    Input('price-hist', 'selectedData'),
    Input('duration-hist', 'selectedData'),
    Input('co2-hist', 'selectedData'),
    Input('airline-hist', 'clickData'),
    Input('country-hist-from', 'clickData'),
    Input('country-hist-to', 'clickData'),
    Input("timezone-input", "value"),
    Input("colorblind-mode-input", "value"),
])
def update_everything_on_selects(selectedDataFrom, selectedDataTo, dates, timesFrom, timesTo, days, prices, durations, co2s, airline, country_from, country_to, timezone_mode, colourblind_mode):

    # hacky fix for double histogram callbacking
    if (callback_context.triggered[0]['prop_id'] == 'days-of-week-hist.selectedData' and days and not days['points']):
        return no_update
    elif (callback_context.triggered[0]['prop_id'] == 'date-hist.selectedData' and dates and not dates['points']):
        return no_update
    elif (callback_context.triggered[0]['prop_id'] == 'price-hist.selectedData' and prices and not prices['points']):
        return no_update
    elif (callback_context.triggered[0]['prop_id'] == 'duration-hist.selectedData' and durations and not durations['points']):
        return no_update
    elif (callback_context.triggered[0]['prop_id'] == 'co2-hist.selectedData' and co2s and not co2s['points']):
        return no_update
    
    set_colour_blind_mode(colourblind_mode[-1] == 1)
    
    global flight_data, airport_data, ORIGINAL_FLIGHT_DATA_GROUPED, ORIGINAL_FLIGHT_DATA, ORIGINAL_AIRPORT_DATA, time_column_suffix

    time_column_suffix = '_gmt' if timezone_mode[-1] == 1 else ''

    flight_data = ORIGINAL_FLIGHT_DATA

    if selectedDataFrom and selectedDataFrom["points"]:
        flight_data = flight_data[flight_data["from_airport_code"].isin([d["customdata"] for d in selectedDataFrom["points"] if "customdata" in d])]

    if selectedDataTo and selectedDataTo["points"]:
        flight_data = flight_data[flight_data["dest_airport_code"].isin([d["customdata"] for d in selectedDataTo["points"] if "customdata" in d])]

    if dates and dates['points']:
        flight_data = flight_data.loc[flight_data.apply(lambda x: x['departure_time'+time_column_suffix].strftime('%Y-%m-%d') in [d['x'] for d in dates['points']], axis=1)]
    
    if timesFrom and timesFrom['points']:
        flight_data = flight_data.loc[flight_data.apply(lambda x: x['departure_time'+time_column_suffix].strftime('%H') in [t['theta'] for t in timesFrom['points']], axis=1)]

    if timesTo and timesTo['points']:
        flight_data = flight_data.loc[flight_data.apply(lambda x: x['arrival_time'+time_column_suffix].strftime('%H') in [t['theta'] for t in timesTo['points']], axis=1)]

    if days and days['points']:
        flight_data = flight_data.loc[flight_data.apply(lambda x: x['departure_time'+time_column_suffix].weekday() in [d['x'] for d in days['points']], axis=1)]

    if prices and prices['points']:
        flight_data = flight_data.loc[flight_data.apply(lambda x: prices['range']['x'][0] < x['price'] and x['price'] < prices['range']['x'][1], axis=1)]

    if durations and durations['points']:
        flight_data = flight_data.loc[flight_data.apply(lambda x: durations['range']['x'][0] < x['duration_minutes'] and x['duration_minutes'] < durations['range']['x'][1], axis=1)]

    if co2s and co2s['points']:
        flight_data = flight_data.loc[flight_data.apply(lambda x: co2s['range']['x'][0] < x['co2_emissions'] and x['co2_emissions'] < co2s['range']['x'][1], axis=1)]

    if airline and airline['points']:
        flight_data = flight_data.loc[flight_data.apply(lambda x: airline['points'][0]['x'] in x['airline_name'], axis=1)]

    flight_data = get_flight_df_with_country(flight_data, airport_data)

    if country_from and country_from['points']:
        flight_data = flight_data.loc[flight_data.apply(lambda x: country_from['points'][0]['x'] == x['from_country'], axis=1)]

    if country_to and country_to['points']:
        flight_data = flight_data.loc[flight_data.apply(lambda x: country_to['points'][0]['x'] == x['dest_country'], axis=1)]

    output_graphs = [
        get_map(ORIGINAL_FLIGHT_DATA_GROUPED, flight_data, airport_data, is_from=True).figure,
        get_map(ORIGINAL_FLIGHT_DATA_GROUPED, flight_data, airport_data, is_from=False).figure,
        get_date_hist(flight_data, time_column_suffix, MIN_DAY, MAX_DAY).figure,
        get_time_bar(flight_data, time_column_suffix, is_from=True).figure,
        get_time_bar(flight_data, time_column_suffix, is_from=False).figure,
        get_days_of_week_hist(flight_data, time_column_suffix).figure,
        get_histogram_price(flight_data).figure,
        get_histogram_duration(flight_data).figure,
        get_histogram_co2(flight_data).figure,
        get_histogram_country(flight_data, airport_data, get_colours(), is_from=True).figure,
        get_histogram_country(flight_data, airport_data, get_colours(), is_from=False).figure,
        get_histogram_airline(flight_data).figure,
        get_table_data(flight_data, airport_data).to_dict("records"),
        get_table_header_styling(),
        get_legend(*get_colours())
    ]
    
    return output_graphs

if __name__ == '__main__':
    app.run(debug=True)
