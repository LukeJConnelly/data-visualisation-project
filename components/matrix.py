import plotly.express as px
import plotly.graph_objects as go
from dash import dcc
import pandas as pd
import numpy as np
from tqdm import tqdm


from utils import data_filtering
from utils.settings import get_neutral_colour, default_bg_color

def map_continent(continent):
    if continent == "North America":
        return "N. America"
    if continent == "South America":
        return "S. America"
    return continent

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
        

    # if sorting:
    #     line_placement = []
    #     last_row = None
    #     for row in sorting[["IATA Code", sort_by]].iterrows():
    #         if last_row = None:
    #             last_row = row
    #             continue
    #         if last_row[sort_by] != 

    lines = []


    # Add horizontal lines
    # for i in range(1, len(flight_df)):
    # lines.append(go.Scatter(x=["AEP","DUB"], y=["AEP", "DUB"], mode='lines', line=dict(color='black')))

    # Add vertical lines
    # for i in range(1, len(flight_df.columns)):
    # lines.append(go.Scatter(x=[len(flight_df.columns), 0], y=[0,len(flight_df.index)], mode='lines', line=dict(color='black')))

    heatmap = go.Heatmap(x=flight_df.columns, y=flight_df.index, z=flight_df.values.T)
    fig = go.Figure(data=[heatmap, *lines])


    # fig = px.imshow(flight_df,
    #     labels=dict(x="Arrival Airport", y="Departure Airport", color="Number of flights")
    # )
    if sort_by == "Continent":
        sorting.reset_index(inplace=True)
        continent_changes = sorting.index[sorting[sort_by] != sorting[sort_by].shift(1)].tolist() + [len(sorting.index)]
        prev = 0
        for i in continent_changes:
            if i == 0:
                continue
            fig.add_annotation(
                x=(i + prev) / 2,
                y=len(flight_df.index) + 2,
                text=map_continent(sorting.iloc[prev][sort_by]),
                textangle=20,
                showarrow=False,
                font=dict(size=10, color="black", family="Segoe UI Semibold"),
            )
            fig.add_annotation(
                x=len(flight_df.index) + 2,
                y=(i + prev) / 2,
                text=map_continent(sorting.iloc[prev][sort_by]),
                textangle=20,
                showarrow=False,
                font=dict(size=10, color="black", family="Segoe UI Semibold"),
            )
            prev = i
            if i == len(sorting.index):
                continue
            fig.add_shape(
                type="line",
                x0=i - 0.5,
                x1=i - 0.5,
                y0=-0.5,
                y1=len(flight_df.index)-0.5,
                line=dict(color="#212529", width=2),
            )
            fig.add_shape(
                type="line",
                x0=-0.5,
                x1=len(flight_df.index)-0.5,
                y0=i - 0.5,
                y1=i - 0.5,
                line=dict(color="#212529", width=2),
            )

    country_lookup = {airport_data.iloc[i]["IATA Code"]: airport_data.iloc[i]["Country"].title() if len(airport_data.iloc[i]["Country"]) >= 4 else airport_data.iloc[i]["Country"] for i in range(len(airport_data))}

    fig.update_layout(
        xaxis=dict(showgrid=False, tickfont=dict(size=10), ticktext=[x for x in flight_df.columns], tickvals=[i for i in range(len(flight_df.columns))], side="top"),
        yaxis=dict(showgrid=False, autorange="reversed", scaleanchor="x", side="left", tickfont=dict(size=10), ticktext=[x for x in flight_df.index], tickvals=[i for i in range(len(flight_df.index))]),
        plot_bgcolor=default_bg_color,
        title=dict(font=dict(size=15, color="black"), automargin=True, x=0.5),
        title_font_family="Segoe UI Semibold",
        hoverlabel=dict(font_family="Segoe UI"),
        font_family="Segoe UI",
        margin=dict(t=0, b=5, l=0, r=5),
    ).update_traces(
        hoverongaps=False,
        customdata=np.stack(([[country_lookup[c] for c in flight_df.columns.to_list()]] * len(flight_df), [[country_lookup[c]] * len(flight_df) for c in flight_df.columns]), axis=-1),
        # customdata=[f"({country_lookup[flight_df.columns[j]]})" for i in range(len(flight_df.index)) for j in range(len(flight_df.columns))],
        # text=[f"{flight_df.columns[j]} ({country_lookup[flight_df.columns[j]]})-> {flight_df.index[i]} ({country_lookup[flight_df.index[i]]}): {flight_df.iloc[i,j]} flights" for i in range(len(flight_df.index)) for j in range(len(flight_df.columns))]
        hovertemplate="%{y} (%{customdata[1]}) -> %{x} (%{customdata[0]}): %{z:.1d} flights",
    )


    # for i, row in tqdm(enumerate(flight_df.index)):
    #     for j, col in enumerate(flight_df.columns):
            
    #         fig.add_annotation(
    #                     x=i,
    #                     y=j,
    #                     hovertext=f"{row}{col} :",# {flight_df.iloc[row,col]}",
    #                     text="",
    #                     showarrow=False,
    #                     xref='x',
    #                     yref='y',
    #                     font=dict(size=10)
    #                 )

    return dcc.Graph(id="matrix", figure=fig)
