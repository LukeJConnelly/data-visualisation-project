import plotly.express as px
import plotly.graph_objects as go
from dash import dcc
import pandas as pd
import numpy as np

from utils import data_filtering
from utils.settings import default_bg_color

def get_matrix(flight_data, airport_data,sort_by="Country"):
    flight_df = data_filtering.get_unique_flight_routes(flight_data)[["from_airport_code", "dest_airport_code", "count"]]
    flight_df = flight_df.pivot(index='from_airport_code', columns='dest_airport_code', values='count')

    rows = set([i[0] for i in flight_df.reset_index().values.tolist()])
    missing_airports = rows ^ set(list(airport_data["IATA Code"]))

    missing_dict = {"from_airport_code": list(missing_airports),
                    **{airport_code:[0 for _ in range(len(missing_airports))] for airport_code in list(flight_df.columns)}}

    missing_df = pd.DataFrame(missing_dict)
    missing_df.set_index("from_airport_code", inplace=True)

    flight_df = pd.concat([flight_df, missing_df], ignore_index=False)
    # flight_df.fillna(0, inplace=True)
    flight_df.replace(0, np.nan, inplace=True)
    if (sort_by == "IATA Code"):
        flight_df = flight_df.sort_index(ascending=True)
        sorting = None
    elif (sort_by == "Country"):
        sorting = airport_data[["IATA Code", "Country"]].sort_values(by=["Country", "IATA Code"])
        sorting_order = list(sorting["IATA Code"])
        flight_df = flight_df[sorting_order]
        flight_df.index = pd.Categorical(flight_df.index, categories=sorting_order, ordered=True)
        flight_df = flight_df.sort_index()
    elif (sort_by == "Continent"):
        sorting = airport_data[["IATA Code", "Country", "Continent"]].sort_values(by=["Continent", "Country", "IATA Code"])
        sorting_order = list(sorting["IATA Code"])
        flight_df = flight_df[sorting_order]
        flight_df.index = pd.Categorical(flight_df.index, categories=sorting_order, ordered=True)
        flight_df = flight_df.sort_index()
        

    heatmap = go.Heatmap(x=flight_df.columns, y=flight_df.index, z=flight_df.values.T)
    fig = go.Figure(data=[heatmap])


    fig = px.imshow(flight_df,
        labels=dict(x="Arrival Airport", y="Departure Airport", color="Number of flights")
    )

    fig.update_layout(
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        plot_bgcolor=default_bg_color
    ).update_traces(
        hovertemplate="%{y} -> %{x} : %{z:.1d} flights",
    )

    fig.update_xaxes(side="top")

    return dcc.Graph(id="matrix", figure=fig)
