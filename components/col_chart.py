from dash import dcc
import plotly.graph_objects as go
import plotly.express as px
from utils.settings import get_colours

from utils.airport_country_mapping import get_flight_df_with_country

def get_bar_chart(flight_data):
    return dcc.Graph(
            id='bar-chart',
            figure=px.bar(flight_data, x="from_airport_code", color="dest_airport_code", barmode="group")
        )

def get_histogram_price(flight_data):
    return dcc.Graph(
            id='price-hist',
            figure=px.histogram(flight_data, x="price")
                     .update_layout(
                         dragmode="select",
                         selectdirection="h",
                         xaxis={"fixedrange": True},
                         yaxis={"fixedrange": True, "visible": False},
                         yaxis_title=None,
                         xaxis_title=None,
                         margin=dict(t=0, b=0, l=0, r=0)),
            style={"height": "15vh"}
        )

def get_histogram_country(flight_data, airport_data, is_from=True):
    flight_df = get_flight_df_with_country(flight_data, airport_data)

    return dcc.Graph(
            id='country-hist'+ ("-from" if is_from else "-to"),
            figure=px.histogram(flight_df, x="from_country" if is_from else "dest_country")
                     .update_layout(
                         dragmode="select",
                         selectdirection="h",
                         xaxis={"fixedrange": True},
                         yaxis={"fixedrange": True, "visible": False},
                         yaxis_title=None,
                         xaxis_title=None,
                         margin=dict(t=0, b=0, l=0, r=0))
                     .update_traces(
                         marker={"color": get_colours()[is_from]},
                     ),
            style={"height": "15vh"}
        )