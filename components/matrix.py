import plotly.express as px
from dash import dcc

from  utils import data_filtering

def get_matrix(flight_data, airport_data):
    flight_df = data_filtering.get_unique_flight_routes(flight_data)[["from_airport_code", "dest_airport_code", "count"]]
    # flight_df.set_index('from_airport_code', inplace=True)
    flight_df = flight_df.pivot(index='from_airport_code', columns='dest_airport_code', values='count')
    flight_df.fillna(0, inplace=True)

    fig = px.imshow(flight_df,
        labels=dict(x="Arrival Airport", y="Departure Airport", color="Number of flights"),
    )
    fig.update_xaxes(side="top")
    return dcc.Graph(id="matrix", figure=fig)
