from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from utils.settings import get_colours

def get_date_data(flight_data):
    return flight_data['departure_time'].apply(lambda x: x.date()).value_counts().reset_index().rename(columns={"departure_time": "value"})

def get_date_hist(flight_data, start_date, end_date):
    num_days = (end_date - start_date).days + 1
    date_options = get_date_data(flight_data)
    return dcc.Graph(id="date-hist",
                     figure=go.Figure(
                     px.histogram(date_options, x="value", y="count", nbins=num_days, range_x=[start_date, end_date])
                     .update_layout(
                         dragmode="select",
                         selectdirection="h",
                         xaxis={"fixedrange": True},
                         yaxis={"fixedrange": True, "visible": False},
                         yaxis_title=None,
                         xaxis_title=None,
                         margin=dict(t=0, b=0, l=0, r=0),)),
                     config={"modeBarButtonsToRemove": ["zoomIn2d", "zoomOut2d", "pan2d", "zoom2d", "autoScale2d", "resetScale2d",],
                             "displaylogo": False,},
                     style={"height": "15vh"},)

def get_time_data(flight_data, is_from=True):
    return flight_data['departure_time' if is_from else 'arrival_time'].apply(lambda x: x.strftime('%H')).value_counts().reset_index().rename(columns={"departure_time": "value", "arrival_time": "value"})

def get_time_bar(flight_data, is_from=True):
    time_options = get_time_data(flight_data, is_from)
    return dcc.Graph(id="time-bar" + ("-from" if is_from else "-to"),
                    figure=px.bar_polar(time_options, r="count", theta="value")
                    .update_layout(
                        margin=dict(t=0, b=0, l=0, r=0),
                        dragmode=False,
                    )
                    .update_traces(
                        marker={"color": get_colours()[is_from]},
                    )
                    .update_polars(
                        radialaxis={"visible": False},
                        angularaxis={"ticks": "inside", "visible": False, "categoryorder": "array", "categoryarray": [str(i).zfill(2) for i in range(24)]},
                        hole=0.6,
                    ).add_annotation(
                        text="24h<br>clock",
                        x=0.5,
                        y=0.5,
                        showarrow=False
                    ),
                    config={
                        "modeBarButtonsToRemove": [
                            "zoomIn2d",
                            "zoomOut2d",
                            "pan2d",
                            "zoom2d",
                            "autoScale2d",
                            "resetScale2d",
                            "select2d",
                        ],
                        "displaylogo": False,
                    },
                    style={"height": "15vh"},
                )
