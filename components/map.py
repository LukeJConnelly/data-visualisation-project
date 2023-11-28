from dash import dcc
import plotly.graph_objects as go
from tqdm import tqdm
from components.country_airport_dicts import airport_to_country

def get_map(flight_data, airport_data):

    hover_texts_airports = [f"{airport} - {airport_to_country[airport]}" for airport in airport_data['IATA Code']]
  
    fig = go.Figure()
    
    # FLIGHTS
    prev_errors = set()


    # Option 1: Loop through and plot all together at end

    lats = []
    lons = []
    mid_lats = []
    mid_lons = []
    counts=[]
    grouped_flight_data = flight_data.groupby(['from_airport_code', 'dest_airport_code']).size().reset_index(name='counts')
    hover_texts_flights = []
    
    for _, row in tqdm(grouped_flight_data.iterrows()):
        try:
            lat1, lat2 = airport_data.loc[row['from_airport_code'], 'Latitude Decimal Degrees'], airport_data.loc[row['dest_airport_code'], 'Latitude Decimal Degrees']
            lon1, lon2 = airport_data.loc[row['from_airport_code'], 'Longitude Decimal Degrees'], airport_data.loc[row['dest_airport_code'], 'Longitude Decimal Degrees']
            lats.append(lat1)
            lats.append(lat2)
            lons.append(lon1)
            lons.append(lon2)
            mid_lats.append((lat1+lat2)/2)
            mid_lons.append((lon1+lon2)/2)
            lats.append(None)
            lons.append(None)
            mid_lats.append(None)
            mid_lons.append(None)
            hover_texts_flights.append(f"{row['from_airport_code']} ({airport_to_country[row['from_airport_code']]}) - {row['dest_airport_code']} ({airport_to_country[row['dest_airport_code']]})")
            counts.append(row['counts'])
        except KeyError as e:
            prev_errors.add(e.args[0])

    print(f"There are {len(lats)} flights being plotted")

    fig.add_trace(go.Scattermapbox(
        mode="lines",
        lat=lats,
        lon=lons,
        line=dict(width=1, color="red"),
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