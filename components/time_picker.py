from datetime import datetime
from dash import html, dcc
import dash_bootstrap_components as dbc

def get_time_picker(date_options, time_options):
    
    def create_datetime_dropdowns(date_options, time_options, default_value, is_start=False):
        return dbc.CardGroup(
            [
                dbc.Label(f"{'Start' if is_start else 'End'} Date:"),
                dbc.Select(
                    id= "start-date-dropdown" if is_start else "end-date-dropdown",
                    options=date_options,
                    value=default_value,
                    className="mb-2",
                ),
                dbc.Label(f"{'Start' if is_start else 'End'} Time:"),
                dbc.Select(
                    id= "start-time-dropdown" if is_start else "end-time-dropdown",
                    options=time_options,
                    value=default_value,
                    className="mb-2",
                ),
            ],
            className="p-3"
        )

    return html.Div([
        html.Div(id='current-datetime', children="Select a time range"),

        html.Button("Change", id="open-modal-btn", n_clicks=0),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Select Date and Time")),
                dbc.ModalBody([
                    create_datetime_dropdowns(date_options, time_options, "2023-01-01", is_start=True),
                    create_datetime_dropdowns(date_options, time_options, "2023-01-02"),
                ]),
                html.Div(id='warning-message', style={'color': 'red'}),
                dbc.ModalFooter(
                    dbc.Button("Confirm", id="confirm-selection-btn", className="ms-auto", n_clicks=0)
                ),
            ],
            id="datetime-modal",
            is_open=False,
        ),
    ])

def get_default_time_values(date_options, time_options):
    # Determine the earliest start date and time
    earliest_start_date = min(date_options, key=lambda x: x['value'])['value']
    earliest_start_time = min(time_options, key=lambda x: x['value'])['value']

    # Determine the latest end date and time
    latest_end_date = max(date_options, key=lambda x: x['value'])['value']
    latest_end_time = max(time_options, key=lambda x: x['value'])['value']

    return earliest_start_date, earliest_start_time, latest_end_date, latest_end_time