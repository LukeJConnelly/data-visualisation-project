import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from utils import data_loader

if __name__ == "__main__":
    flight_data = data_loader.load_flight_data()
    airport_data = data_loader.load_airport_data(flight_data=flight_data, with_airport_degree=True)

    layout = go.Layout(
    showlegend=False,
    hovermode='closest',)

    fig1 = px.scatter_mapbox(airport_data,
                            lat=airport_data["Latitude Decimal Degrees"],
                            lon=airport_data["Longitude Decimal Degrees"],
                            size=airport_data["flight_degree"],
                            text='IATA Code',
                            zoom=3,
                            width=1200,
                            height=900,
                            title="Airports"
                            )
    fig1.update_layout(mapbox_style="open-street-map")
    fig1.show()