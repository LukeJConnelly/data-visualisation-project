from dash import html, dcc
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.settings import get_colours, default_chart_height, default_bg_color, get_neutral_colour

def get_date_data(flight_data, time_column):
    return flight_data[time_column].apply(lambda x: x.date()).value_counts().reset_index().rename(columns={time_column: "value"})

def get_days_of_week_data(flight_data, time_column):
    return flight_data[time_column].apply(lambda x: x.weekday()).value_counts().reset_index().rename(columns={time_column: "value"})

def get_days_of_week_hist(flight_data, time_column_suffix):
    day_options = get_days_of_week_data(flight_data, 'departure_time' + time_column_suffix)
    return dcc.Graph(id="days-of-week-hist",
                        figure=go.Figure(
                        px.histogram(day_options, x="value", y="count", nbins=7, 
                                     range_x=[-0.5, 6.5], title="Flights by Weekday")
                        .update_xaxes(tickvals=[0, 1, 2, 3, 4, 5, 6], ticktext=['M', 'T', 'W', 'T', 'F', 'S', 'S'])
                        .update_traces(marker_color=get_neutral_colour(), hovertemplate="%{y} flights")
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
                            margin=dict(t=0, b=0, l=0, r=0),)),
                        config={"modeBarButtonsToRemove": ["zoomIn2d", "zoomOut2d", "pan2d", "zoom2d", "autoScale2d", "resetScale2d",],
                                "displaylogo": False,},
                        style={"height": default_chart_height},)

def get_monthly_ticks(start_date, end_date):
    date_range = pd.date_range(start=start_date, end=end_date, freq='MS')
    return [date.timestamp() * 1000 for date in date_range]

def get_monthly_tick_labels(start_date, end_date):
    date_range = pd.date_range(start=start_date, end=end_date, freq='MS')
    return [date.strftime('%m/%d/%y') if date.month == 5 else date.strftime('%m/%d') for date in date_range]

def get_date_hist(flight_data, time_column_suffix, start_date, end_date):
    num_days = (end_date - start_date).days + 1
    date_options = get_date_data(flight_data, 'departure_time' + time_column_suffix)
    return dcc.Graph(id="date-hist",
                     figure=go.Figure(
                     px.histogram(date_options, x="value", y="count", nbins=num_days, range_x=[start_date, end_date], title="Flights by Date")
                     .update_layout(
                         dragmode="select",
                         selectdirection="h",
                         yaxis={"fixedrange": True, "visible": False},
                         yaxis_title=None,
                         xaxis_title=None,
                         xaxis=dict(
                            tickmode='array',
                            fixedrange=True,
                            tickvals=get_monthly_ticks(start_date, end_date),
                            ticktext=get_monthly_tick_labels(start_date, end_date),
                        ),
                         title=dict(font=dict(size=15, color="black"), automargin=True, x=0.5),
                         title_font_family="Segoe UI Semibold",
                         hoverlabel=dict(font_family="Segoe UI"),
                         font_family="Segoe UI",
                         plot_bgcolor=default_bg_color,
                         margin=dict(t=0, b=0, l=0, r=0))
                     .update_traces(marker_color=get_neutral_colour(), hovertemplate="%{x}<br>%{y} flights")
                     ),
                     config={"modeBarButtonsToRemove": ["zoomIn2d", "zoomOut2d", "pan2d", "zoom2d", "autoScale2d", "resetScale2d",],
                             "displaylogo": False,},
                     style={"height": default_chart_height},)

def get_time_data(flight_data, time_column):
    return flight_data[time_column].apply(lambda x: x.strftime('%H')).value_counts().reset_index().rename(columns={time_column: "value"})

def get_time_bar(flight_data, time_column_suffix, is_from=True):
    time_options = get_time_data(flight_data, ('departure_time' if is_from else 'arrival_time') + time_column_suffix)
    return dcc.Graph(id="time-bar" + ("-from" if is_from else "-to"),
                    figure=px.bar_polar(time_options, r="count", theta="value", 
                                        title="Dept. Times" if is_from else "Arrival Times",
                                        hover_data=["value", "count"])
                    .update_layout(
                        margin=dict(t=0, b=0, l=0, r=1),
                        dragmode=False,
                        title=dict(font=dict(size=15, color="black"), automargin=True, x=0.5),
                        title_font_family="Segoe UI Semibold",
                        font_family="Segoe UI",
                        hoverlabel=dict(font_family="Segoe UI"),
                    )
                    .update_traces(
                        marker={"color": get_colours()[is_from]},
                        hovertemplate="%{theta}:00-%{theta}:59<br>%{r} flights"
                    )
                    .update_polars(
                        radialaxis={"visible": False},
                        angularaxis={"ticks": "inside", "visible": False, "categoryorder": "array", "categoryarray": [str(i).zfill(2) for i in range(24)]},
                        hole=0.6,
                        bgcolor=default_bg_color,
                    ).add_annotation(
                        text="00",
                        x=0.5,
                        y=0.76,
                        font=dict(size=12),
                        showarrow=False
                    ).add_annotation(
                        text="12",
                        x=0.5,
                        y=0.24,
                        font=dict(size=12),
                        showarrow=False
                    ).add_annotation(
                        text="06",
                        x=0.76,
                        y=0.5,
                        font=dict(size=12),
                        showarrow=False
                    ).add_annotation(
                        text="18",
                        x=0.24,
                        y=0.5,
                        font=dict(size=12),
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
                    style={"height": default_chart_height},
                )
