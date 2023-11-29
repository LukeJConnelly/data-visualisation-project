from dash import dcc
import plotly.graph_objects as go
from tqdm import tqdm
from components.country_airport_dicts import airport_to_country
import pandas as pd

def get_map(flight_data, airport_data, chosen_for_colouring, quantiles):

    hover_texts_airports = [f"{airport} - {airport_to_country[airport]}" for airport in airport_data['IATA Code']]
  
    fig = go.Figure()
    
    # FLIGHTS
    prev_errors = set()

    colours=['#27b300','#b3b000','#b35f00','#b30000']

    # Option 1: Loop through and plot all together at end
    if chosen_for_colouring != 'none':
        lats = [[] for _ in range(len(colours))]
        lons = [[] for _ in range(len(colours))]
        counts=[[] for _ in range(len(colours))] 
        mid_lats = []
        mid_lons = []
        hover_texts_flights = []
        grouped_data_by_airports = flight_data.groupby(['from_airport_code', 'dest_airport_code'])
        airports_and_colour = grouped_data_by_airports[chosen_for_colouring].mean().reset_index(name=chosen_for_colouring)
        airports_and_counts = grouped_data_by_airports.size().reset_index(name='count')
        grouped_flight_data = airports_and_colour.merge(airports_and_counts, on=['from_airport_code', 'dest_airport_code'])
        for _, row in tqdm(grouped_flight_data.iterrows()):
            try:
                curr_quantile = 0 if row[chosen_for_colouring] < quantiles[0] else 1 if row[chosen_for_colouring] < quantiles[1] else 2 if row[chosen_for_colouring] < quantiles[2] else 3
                lat1, lat2 = airport_data.loc[row['from_airport_code'], 'Latitude Decimal Degrees'], airport_data.loc[row['dest_airport_code'], 'Latitude Decimal Degrees']
                lon1, lon2 = airport_data.loc[row['from_airport_code'], 'Longitude Decimal Degrees'], airport_data.loc[row['dest_airport_code'], 'Longitude Decimal Degrees']
                lats[curr_quantile].append(lat1)
                lats[curr_quantile].append(lat2)
                lons[curr_quantile].append(lon1)
                lons[curr_quantile].append(lon2)  
                mid_lats.append((lat1+lat2)/2)
                mid_lons.append((lon1+lon2)/2)
                lats[curr_quantile].append(None)
                lons[curr_quantile].append(None)
                mid_lats.append(None)
                mid_lons.append(None)
                hover_texts_flights.append(f"{row['from_airport_code']} ({airport_to_country[row['from_airport_code']]}) - {row['dest_airport_code']} ({airport_to_country[row['dest_airport_code']]})")
                counts[curr_quantile].append(row['counts'])
            except KeyError as e:
                prev_errors.add(e.args[0])

        # hover_texts = [f"{name} - Lat: {lat}, Lon: {lon}" for name, lat, lon in zip(airport_data.index, airport_data['Latitude Decimal Degrees'], airport_data['Longitude Decimal Degrees'])]

        for i in range(len(colours)):
            fig.add_trace(go.Scattermapbox(
                mode="lines",
                lat=lats[i],
                lon=lons[i],
                line=dict(width=1, color=colours[i]),
                name="Flights w/ " + chosen_for_colouring + " in " + str(i+1) + ["st", "nd", "rd", "th"][i] + " quantile",
                # text=hover_texts,
                hoverinfo='none',
                opacity=0.1,
            ))

        middle_node_trace = go.Scattermapbox(
            lat=mid_lats,
            lon=mid_lons,
            mode='markers',
            marker=go.Marker(
                opacity=0
            ),
            hoverinfo='text',
            text=hover_texts_flights,
        )

        fig.add_trace(middle_node_trace)
    else:
        lats = []
        lons = []
        counts=[] 
        mid_lats = []
        mid_lons = []
        hover_texts_flights = []
        grouped_flight_data = flight_data.groupby(['from_airport_code', 'dest_airport_code']).size().reset_index(name='count')
        for _, row in tqdm(grouped_flight_data.iterrows()):
            try:
                lat1, lat2 = airport_data.loc[row['from_airport_code'], 'Latitude Decimal Degrees'], airport_data.loc[row['dest_airport_code'], 'Latitude Decimal Degrees']
                lon1, lon2 = airport_data.loc[row['from_airport_code'], 'Longitude Decimal Degrees'], airport_data.loc[row['dest_airport_code'], 'Longitude Decimal Degrees']
                lats.append(lat1)
                lats.append(lat2)
                lons.append(lon1)
                lons.append(lon2)
                lats.append(None)
                mid_lats.append((lat1+lat2)/2)
                mid_lons.append((lon1+lon2)/2)
                lons.append(None)
                hover_texts_flights.append(f"{row['from_airport_code']} ({airport_to_country[row['from_airport_code']]}) - {row['dest_airport_code']} ({airport_to_country[row['dest_airport_code']]})")
                counts.append(row['counts'])
            except KeyError as e:
                prev_errors.add(e.args[0])

        fig.add_trace(go.Scattermapbox(
            mode="lines",
            lat=lats,
            lon=lons,
            line=dict(width=1, color=colours[-1]),
            name="Flights",
            hoverinfo='none',
            opacity=0.1,
        ))
        
        middle_node_trace = go.Scattermapbox(
            lat=mid_lats,
            lon=mid_lons,
            mode='markers',
            marker=go.Marker(
                opacity=0
            ),
            hoverinfo='text',
            text=hover_texts_flights,
        )

        fig.add_trace(middle_node_trace)



    fig.add_trace(go.Scattermapbox(lat=airport_data['Latitude Decimal Degrees'],
                                lon=airport_data['Longitude Decimal Degrees'],
                                mode='markers',
                                marker=go.scattermapbox.Marker(size=5, color='black'),
                                name='Airports',
                                text=hover_texts_airports,
                                hoverinfo='text'))


    # Option 2: Loop through and plot each flight individually
    
    # for i in tqdm(range(len(flight_data))):
    #     try:
    #         fig.add_trace(
    #                     go.Scattermapbox(
    #                         mode='lines',
    #                         lat=[airport_data.loc[flight_data.iloc[i]['from_airport_code'], 'Latitude Decimal Degrees'], airport_data.loc[flight_data.iloc[i]['dest_airport_code'], 'Latitude Decimal Degrees']],
    #                         lon=[airport_data.loc[flight_data.iloc[i]['from_airport_code'], 'Longitude Decimal Degrees'], airport_data.loc[flight_data.iloc[i]['dest_airport_code'], 'Longitude Decimal Degrees']],
    #                         line=go.scattermapbox.Line(
    #                             width=1,
    #                             color="red"
    #                         ),
    #                         name=str(flight_data['flight_number'][i])
    #                     )
    #                 )
    #     except KeyError as e:
    #         prev_errors.add(e.args[0])

    
    print("Following lookup errors occurred:", prev_errors)
    fig.update_layout(mapbox_style='open-street-map',  margin={'r': 20, 't': 20, 'l': 0, 'b': 20})
    return dcc.Graph(id='flight-map', figure=fig)