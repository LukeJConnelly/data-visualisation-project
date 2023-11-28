from dash import Dash, html
import dash_bootstrap_components as dbc

def get_about_modal():
    return html.Div([
    dbc.Button("About", id="open-help-modal", className="mb-3 btn-secondary"),
    dbc.Modal(
        [
            dbc.ModalHeader(html.H3("Help Information")),
            dbc.ModalBody(
    children=[
        html.P([
            " This tool provides an interactive way to explore and analyze flight data."
        ]),
        html.P([
            html.B("Key Features:"),
            html.Ul([
                html.Li(html.B("Interactive Map: ")),
                html.Span("Zoom in and out for a detailed view of flight paths."),
                html.Li(html.B("Flight Path Visualization: ")),
                html.Span("Select airports from the dropdown menu to view corresponding flight paths."),
                html.Li(html.B("Detailed Flight Information: ")),
                html.Span("Hover over any flight path to see detailed information such as airline, duration, and more."),
                html.Li(html.B("Time Filtering: ")),
                html.Span("Use the date and time selectors to filter flights based on specific departure and arrival times."),
                html.Li(html.B("Data Insights: ")),
                html.Span("Gain insights into flight frequencies, popular routes, and airline operations."),
                html.Li(html.B("Variable-Based Flight Path Visualization:")),
                html.Span("Select a variable to color code the flight paths based on that variable."),
            ])
        ]),
        html.P([
            html.I("Tip: "),
            "For the best experience, view the dashboard on a desktop or laptop with a stable internet connection."
        ]),
    ]
),
        ],
        id="help-modal",
    ),
])