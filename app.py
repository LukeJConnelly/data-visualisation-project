from dash import Dash, html
from dash.dependencies import Input, Output, State
from components.map import get_map
from components.side_bar import get_sidebar
from components.time_picker import get_default_time_values, get_time_picker
from utils import data_loader
import dash_bootstrap_components as dbc

flight_data, airport_data = data_loader.load_data()
airport_data.index = airport_data['IATA Code']

date_options = [{'label': 'Date 1', 'value': '2023-01-01'},
        {'label': 'Date 2', 'value': '2023-01-02'}]
time_options = [{'label': 'Time 1', 'value': '00:00'},
        {'label': 'Time 2', 'value': '01:00'}]

# flight_data = flight_data.sample(n=300000).reset_index(drop=True)

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


app.layout = html.Div([
    dbc.NavbarSimple(brand='FlightVis', brand_href='#', color='dark', dark=True),
    dbc.Row(id='container', children=[
        dbc.Col(id='main', children=[
            html.Div(id='main-contents', children=[
                get_time_picker(date_options, time_options), get_map(flight_data, airport_data)
            ])
        ], width=9),
        dbc.Col(id='sidebar', children=[get_sidebar()], width=3)
    ], className='p-5')
])


@app.callback(
    Output("datetime-modal", "is_open"),
    [Input("open-modal-btn", "n_clicks"), Input("confirm-selection-btn", "n_clicks")],
    [State("datetime-modal", "is_open")],
)
def toggle_time_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    Output('current-datetime', 'children'),
    [Input('confirm-selection-btn', 'n_clicks')],
    [State('start-date-dropdown', 'value'), State('start-time-dropdown', 'value'),
     State('end-date-dropdown', 'value'), State('end-time-dropdown', 'value')]
)
def update_datetime(n_clicks, start_date, start_time, end_date, end_time):
    if not n_clicks:
        start_date, start_time, end_date, end_time = get_default_time_values(date_options, time_options)
    
    return f"Start Time: {start_date} {start_time}, End Time: {end_date} {end_time}"

if __name__ == '__main__':
    app.run(debug=True)
