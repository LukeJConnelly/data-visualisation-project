from dash import Dash, html
import dash_bootstrap_components as dbc

def get_help_modal():
    return html.Div([
    dbc.Button("Help", id="open-help-modal", className="mb-3"),
    dbc.Modal(
        [
            dbc.ModalHeader("Help Information"),
            dbc.ModalBody(
    children=[
        html.P([
            html.B("Welcome to the Flight Path Dashboard!"),
            " This tool provides an interactive way to explore and analyze flight data."
        ]),
        html.P([
            html.B("Key Features:"),
            html.Ul([
                html.Li("Interactive Map: "),
                html.Span("Zoom in and out for a detailed view of flight paths."),
                html.Li("Flight Path Visualization: "),
                html.Span("Select airports from the dropdown menu to view corresponding flight paths."),
                html.Li("Detailed Flight Information: "),
                html.Span("Hover over any flight path to see detailed information such as airline, duration, and more."),
                html.Li("Time Filtering: "),
                html.Span("Use the date and time selectors to filter flights based on specific departure and arrival times."),
                html.Li("Data Insights: "),
                html.Span("Gain insights into flight frequencies, popular routes, and airline operations."),
                html.Li("Variable-Based Flight Path Visualization:"),
                html.Span("Select a variable to color code the flight paths based on that variable."),
            ])
        ]),
        html.P([
            html.I("Tip: "),
            "For the best experience, view the dashboard on a desktop or laptop with a stable internet connection."
        ]),
    ]
),
            dbc.ModalFooter(
                dbc.Button("Close", id="close-help-modal", className="ml-auto")
            ),
        ],
        id="help-modal",
    ),
])