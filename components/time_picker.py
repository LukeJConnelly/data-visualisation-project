from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go


def get_time_picker(date_options, time_options):
    min_day = min(date_options["value"])
    max_day = max(date_options["value"])
    num_days = (max_day - min_day).days + 1

    print(num_days)

    return html.Div(
        [
            dbc.Row(
                [
                    dcc.Graph(
                        id="date-hist",
                        figure=go.Figure(
                            px.histogram(
                                date_options, x="label", y="count", nbins=num_days
                            ).update_layout(
                                dragmode="select",
                                selectdirection="h",
                                xaxis={"fixedrange": True},
                                yaxis={"fixedrange": True, "visible": False},
                                yaxis_title=None,
                                xaxis_title=None,
                                margin=dict(t=0, b=0, l=0, r=0),
                            )
                        ),
                        config={
                            "modeBarButtonsToRemove": [
                                "zoomIn2d",
                                "zoomOut2d",
                                "pan2d",
                                "zoom2d",
                                "autoScale2d",
                                "resetScale2d",
                            ],
                            "displaylogo": False,
                        },
                        style={"width": "50vw"},
                    ),
                    dcc.Graph(
                        id="time-bar",
                        figure=px.bar_polar(time_options, r="count", theta="value")
                        .update_layout(
                            margin=dict(t=0, b=0, l=0, r=0),
                            dragmode=False,
                        )
                        .update_polars(
                            radialaxis={"visible": False},
                            angularaxis={"ticks": "inside", "visible": False},
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
                        style={"width": "10vw", "height": "15vh"},
                    ),
                ],
                justify="center",
                style={"height": "20vh"},
            ),
        ]
    )
