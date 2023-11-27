from dash import html, dcc
import dash_bootstrap_components as dbc

def get_time_picker(date_options, time_options):
    
    def create_datetime_dropdowns(date_options, time_options, is_start=False):
        return dbc.CardGroup(
            [
                dbc.Label(f"{'Start' if is_start else 'End'} Date:", className="primary-label"),
                dbc.Select(
                    id= "start-date-dropdown" if is_start else "end-date-dropdown",
                    options=date_options,
                    value=date_options[0]['value'] if is_start else date_options[-1]['value'],
                    className="mb-2",
                ),
                dbc.Label(f"{'Start' if is_start else 'End'} Time:", className="primary-label"),
                dbc.Select(
                    id= "start-time-dropdown" if is_start else "end-time-dropdown",
                    options=time_options,
                    value=time_options[0]['value'] if is_start else time_options[-1]['value'],
                    className="mb-2",
                ),
            ],
            className="p-3"
        )

    return html.Div([
        dbc.Row([
            dbc.Col(html.Div(id='current-datetime', children="Select a time range"), width=9),
            dbc.Col(dbc.Button("Change Time", id="open-modal-btn", n_clicks=0, className="mb-3"), width=3),
        ], justify="center"),

        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Select Date and Time")),
                dbc.ModalBody([
                    create_datetime_dropdowns(date_options, time_options, is_start=True),
                    create_datetime_dropdowns(date_options, time_options, is_start=False),
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

