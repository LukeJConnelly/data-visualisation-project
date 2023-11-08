from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from torch import layout
from utils import data_loader
import dash_bootstrap_components as dbc
from tqdm import tqdm

flight_data, airport_data = data_loader.load_data()
airport_data.index = airport_data['IATA Code']

# flight_data = flight_data.sample(n=300000).reset_index(drop=True)

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

def get_timepicker():
    return html.Div('Time picker here')

def get_map():
    fig = go.Figure()
    # AIRPORTS
    fig.add_trace(go.Scattermapbox(lat=airport_data['Latitude Decimal Degrees'],
                                   lon=airport_data['Longitude Decimal Degrees'],
                                   mode='markers',
                                   marker=go.scattermapbox.Marker(size=5, color='black'),
                                   name='Airports',
                                   text=airport_data.index))
    # FLIGHTS
    prev_errors = set()


    # Option 1: Loop through and plot all together at end

    lats = []
    lons = []
    counts=[]
    grouped_flight_data = flight_data.groupby(['from_airport_code', 'dest_airport_code']).size().reset_index(name='counts')
    for _, row in tqdm(grouped_flight_data.iterrows()):
        try:
            lat1, lat2 = airport_data.loc[row['from_airport_code'], 'Latitude Decimal Degrees'], airport_data.loc[row['dest_airport_code'], 'Latitude Decimal Degrees']
            lon1, lon2 = airport_data.loc[row['from_airport_code'], 'Longitude Decimal Degrees'], airport_data.loc[row['dest_airport_code'], 'Longitude Decimal Degrees']
            lats.append(lat1)
            lats.append(lat2)
            lons.append(lon1)
            lons.append(lon2)
            lats.append(None)
            lons.append(None)
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
        # Needs debugging, and/or width
        text=["Count: " +str(count) for count in counts],
        opacity=0.1
    ))

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
    fig.update_layout(mapbox_style='open-street-map', margin={'r': 0, 't': 0, 'l': 0, 'b': 0,})
    return dcc.Graph(id='map', figure=fig)


def get_sidebar():
    return html.Div(id='sidebar-contents', children=[
        html.H3('Stats & Filter'),
        html.Div(
            id='sidebar-graphs',
            children=[
                html.H6('Example Graph 1'),
                dcc.Graph(id='example-graph-1'),
                html.H6('Example Graph 2'),
                dcc.Graph(id='example-graph-2')
            ]
        ),
    ])


app.layout = html.Div([
    dbc.NavbarSimple(brand='FlightVis', brand_href='#', color='dark', dark=True),
    dbc.Row(id='container', children=[
        dbc.Col(id='main', children=[
            html.Div(id='main-contents', children=[
                get_timepicker(), get_map()
            ])
        ], width=9),
        dbc.Col(id='sidebar', children=[get_sidebar()], width=3)
    ], className='p-5')
])

# callback such as this can be used to update the graph
# @callback(
#     Output('graph-content', 'figure'),
#     Input('dropdown-selection', 'value')
# )
# def update_graph(value):
#     dff = df[df.country==value]
#     return px.line(dff, x='year', y='pop')

if __name__ == '__main__':
    app.run(debug=True)
