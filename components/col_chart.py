import re
import datetime
from dash import dcc
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from utils.settings import get_colours, default_chart_height, get_neutral_colour, default_bg_color

from utils.airport_country_mapping import get_flight_df_with_country

def get_bar_chart(flight_data):
    return dcc.Graph(
            id='bar-chart',
            figure=px.bar(flight_data, x="from_airport_code", color="dest_airport_code", barmode="group")
        )

def get_histogram_price(flight_data):
    return dcc.Graph(
            id='price-hist',
            figure=px.histogram(flight_data['price'], x="price", title="Ticket Price (USD)", range_x=[-0.5, max(flight_data['price'])+0.5])
                     .update_layout(
                         dragmode="select",
                         selectdirection="h",
                         xaxis={"fixedrange": True},
                         yaxis={"fixedrange": True, "visible": False},
                         yaxis_title=None,
                         xaxis_title=None,
                         title=dict(font=dict(size=15, color="black"), automargin=True, x=0.5),
                         title_font_family="Segoe UI Semibold",
                         hoverlabel=dict(font_family="Segoe UI"),
                         font_family="Segoe UI",
                         plot_bgcolor=default_bg_color,
                         margin=dict(t=0, b=0, l=0, r=0))
                     .update_traces(marker_color=get_neutral_colour(), hovertemplate="%{y} flights"),
            config={"modeBarButtonsToRemove": ["zoomIn2d", "zoomOut2d", "pan2d", "zoom2d", "autoScale2d", "resetScale2d",],
                                "displaylogo": False,},
            style={"height": default_chart_height}
        )


def get_histogram_co2(flight_data):
    return dcc.Graph(
            id='co2-hist',
            figure=px.histogram(flight_data, x="co2_percentage")
                     .update_layout(
                         dragmode="select",
                         selectdirection="h",
                         xaxis={"fixedrange": True},
                         yaxis={"fixedrange": True, "visible": False},
                         yaxis_title=None,
                         xaxis_title=None,
                         margin=dict(t=0, b=0, l=0, r=0))
                     .update_traces(marker_color=get_neutral_colour()),
            style={"height": default_chart_height}
        )

def convert_duration_to_hours(duration_str):
    # Regular expression to extract days, and optionally hours, minutes, and seconds
    regex_pattern = r"(\d+)\s*days(?:\s*(\d+):(\d+):(\d+))?"

    match = re.search(regex_pattern, duration_str)
    if match:
        days = match.group(1)
        hours = match.group(2) if match.group(2) else 0
        minutes = match.group(3) if match.group(3) else 0
        seconds = match.group(4) if match.group(4) else 0
    else:
        print("Pattern not found in the string.")

    return int(days) * 24 * 60 + int(hours) * 60 + int(minutes)

def get_histogram_duration(flight_data):
    flight_data["duration_minutes"] = flight_data["duration"].apply(convert_duration_to_hours)
        
    
    return dcc.Graph(
            id='duration-hist',
            figure=px.histogram(flight_data, x="duration_minutes", title="Flight Duration (minutes)", range_x=[-0.5, max(flight_data['duration_minutes'])+0.5])
                     .update_layout(
                         dragmode="select",
                         selectdirection="h",
                         xaxis={"fixedrange": True},
                         yaxis={"fixedrange": True, "visible": False},
                         yaxis_title=None,
                         xaxis_title=None,
                         title=dict(font=dict(size=15, color="black"), automargin=True, x=0.5),
                         title_font_family="Segoe UI Semibold",
                         hoverlabel=dict(font_family="Segoe UI"),
                         font_family="Segoe UI",
                         plot_bgcolor=default_bg_color,
                         margin=dict(t=0, b=0, l=0, r=0))
                     .update_traces(marker_color=get_neutral_colour(), hovertemplate="%{y} flights"),
            style={"height": default_chart_height}
        )
        

def get_histogram_country(flight_data, airport_data, colour_tuple, is_from=True):
    """
    colour_tuple is (to_colour, from_colour)
    """
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
                         marker={"color": colour_tuple[is_from]},
                     ),
            style={"height": default_chart_height}
        )