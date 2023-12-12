import plotly.express as px
from dash import dcc
import pandas as pd

from  utils import data_filtering

def get_matrix(flight_data, airport_data, sort_by="Country"):
    flight_df = data_filtering.get_unique_flight_routes(flight_data)[["from_airport_code", "dest_airport_code", "count"]]
    # flight_df.set_index('from_airport_code', inplace=True)
    flight_df = flight_df.pivot(index='from_airport_code', columns='dest_airport_code', values='count')

    rows = set([i[0] for i in flight_df.reset_index().values.tolist()])
    missing_airports = rows ^ set(list(airport_data["IATA Code"]))

    missing_dict = {"from_airport_code": list(missing_airports),
                    **{airport_code:[0 for _ in range(len(missing_airports))] for airport_code in list(flight_df.columns)}}
    # for airport in missing_airports:
    #     # flight_df[len(flight_df.index)] = [airport] + [0 for _ in range(len(flight_df.columns))]
    #     # airport_data = {airport_code: 0 for airport_code in list(flight_df.columns)}
    #     missing_dict[airport] = [0 for _ in range(len(flight_df.columns))]
        # flight_df = flight_df.append(airport_data, ignore_index=True)
    missing_df = pd.DataFrame(missing_dict)
    missing_df.set_index("from_airport_code", inplace=True)

    # flight_df2 = pd.merge(flight_df, missing_df, how='outer')
    # flight_df2 = pd.merge(flight_df, missing_df, left_index=True, right_index=True, how='outer')
    flight_df = pd.concat([flight_df, missing_df], ignore_index=False)
    flight_df.fillna(0, inplace=True)
    if (sort_by == "IATA Code"):
        flight_df = flight_df.sort_index()
    elif (sort_by == "Country"):
        sorting_order = list(set(airport_data[["IATA Code", "Country"]].sort_values(by="Country")["IATA Code"]))
        flight_df = flight_df[sorting_order]
        flight_df.index = pd.Categorical(flight_df.index, categories=sorting_order, ordered=True)
        flight_df = flight_df.sort_index()

    

    fig = px.imshow(flight_df,
        labels=dict(x="Arrival Airport", y="Departure Airport", color="Number of flights"),
    )
    fig.update_xaxes(side="top")
    return dcc.Graph(id="matrix", figure=fig)
