from dash import html
import dash_bootstrap_components as dbc

def get_legend(to_colour, from_colour, unselected_input_value):
    return [
        html.H5('Legend', style={'text-align': 'center'}),
        html.Table([
            html.Tr([
                html.Td(html.Div(style={'background-color': from_colour, 'width': '1vw', 'height': '1vw', 'border-radius': '50%'})),
                html.Td('Departures')
            ]),
            html.Tr([
                html.Td(html.Div(style={'background-color': to_colour, 'width': '1vw', 'height': '1vw', 'border-radius': '50%'})),
                html.Td('Arrivals')
            ]),
            html.Tr([
                html.Td([html.Div(style={'background-color': '#ADB1B2', 'width': '0.2vw', 'height': '0.2vw', 'border-radius': '50%'}),
                         html.Div(style={'background-color': '#ADB1B2', 'width': '0.5vw', 'height': '0.5vw', 'border-radius': '50%'}),
                         html.Div(style={'background-color': '#ADB1B2', 'width': '1vw', 'height': '1vw', 'border-radius': '50%'})]),
                html.Td('# Flights')
            ]),
            html.Tr([
                html.Td(html.Div(style={'background-color': to_colour, 'width': '1vw', 'height': '1vw', 'border': '0.35vw solid #ADB1B2', 'border-radius': '50%'})),
                html.Td('% Selected')
            ]),
        ], id='legend-table'),
        html.P(html.Small("Hover on a point for more/exact information"), style={'margin-top': '1vh', 'text-align': 'center'}),
        html.Div([
        html.P('Show all flight paths?', style={'width': '100%', 'text-align': 'center', 'margin-top': '10px'}),
        html.Div(dbc.Checklist(
        options=[{"label": "", "value": 1}],
        value=unselected_input_value, id="show-unselected-input", switch=True
        ))], style={'display': 'flex', 'flex-direction': 'column', 'justify-content': 'center', 'align-items': 'center', 'margin-top': '80px'})

    ]