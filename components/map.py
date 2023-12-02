from dash import dcc
import plotly.graph_objects as go
from components.country_airport_dicts import airport_to_country
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
from utils.settings import to_and_from_colour

def get_map(original_grouped_flight_data, flight_data, airport_data, is_from=True):
    fig = go.Figure()

    # Join airport data to flight data
    grouped_flight_data_counts = flight_data.groupby(['from_airport_code', 'dest_airport_code']).size().reset_index(name='count')
    grouped_flight_data_from = pd.merge(grouped_flight_data_counts, airport_data, left_on='from_airport_code', right_on='IATA Code')
    grouped_flight_data_to = pd.merge(grouped_flight_data_counts, airport_data, left_on='dest_airport_code', right_on='IATA Code')
    grouped_flight_data = pd.merge(grouped_flight_data_from, grouped_flight_data_to, on=['from_airport_code', 'dest_airport_code', 'count'], suffixes=('_from', '_to')).drop(['IATA Code_from', 'IATA Code_to'], axis=1)

    # FLIGHTS
    fig.add_trace(go.Scattermapbox(
        mode="lines",
        lat=np.array(grouped_flight_data[['Latitude Decimal Degrees_from', 'Latitude Decimal Degrees_to']]).flatten(),
        lon=np.array(grouped_flight_data[['Longitude Decimal Degrees_from', 'Longitude Decimal Degrees_to']]).flatten(),
        line=dict(width=1, color=to_and_from_colour[is_from]),
        name="Flights",
        opacity=0.1,
    ))

    # AIRPORTS
    total_flights = [original_grouped_flight_data[original_grouped_flight_data['from_airport_code' if is_from else 'dest_airport_code'] == code]['count'].sum() for code in airport_data['IATA Code']]
    selected_totals = [grouped_flight_data[grouped_flight_data['from_airport_code' if is_from else 'dest_airport_code'] == code]['count'].sum() for code in airport_data['IATA Code']]
    is_filtered_data = not all([total_flights[i] == selected_totals[i] for i in range(len(total_flights))])
    exponent = 0.5
    exp_max_total_flights = np.power(max(total_flights), exponent)
    exp_min_total_flights = np.power(1, exponent)

    for i, airport in airport_data.iterrows():
        # Black circle - total flights in/out
        fig.add_trace(go.Scattermapbox(lat=[airport['Latitude Decimal Degrees']],
                                       lon=[airport['Longitude Decimal Degrees']],
                                       mode='markers',
                                       marker=go.scattermapbox.Marker(size=round((np.power(total_flights[i], exponent) - exp_min_total_flights) * 20 / exp_max_total_flights) + 1, color='black'),
                                       text=f"{airport['IATA Code']} - {airport_to_country[airport['IATA Code']]} - {total_flights[i]} flights",
                                       hoverinfo='text',
                                       customdata=[airport['IATA Code']],
                                       opacity=0.2 if is_filtered_data else 1,))

    for i, airport in airport_data.iterrows():
        # Coloured circle - flights in/out to/from selected airport (plotted in seperate loop to ensure they are on top)
        if selected_totals[i] :
            fig.add_trace(go.Scattermapbox(
                mode="markers",
                lat=[airport['Latitude Decimal Degrees']],
                lon=[airport['Longitude Decimal Degrees']],
                marker=dict(size=round((np.power(selected_totals[i], exponent) - exp_min_total_flights) * 20 / exp_max_total_flights), color=to_and_from_colour[is_from]),
                name=airport['IATA Code'],
                text=f"{airport['IATA Code']} - {airport_to_country[airport['IATA Code']]} - {selected_totals[i]} flights" + (f" of {total_flights[i]} selected" if is_filtered_data else ""),
                hoverinfo='text'
            ))

    fig.update_layout(mapbox_style='open-street-map',  margin={"r":0,"t":0,"l":0,"b":0}, showlegend=False, mapbox_bounds={"west": -180, "east": 180, "south": -90, "north": 90})
    return dcc.Graph(id=f'flight-map-{"from" if is_from else "to"}', figure=fig)
