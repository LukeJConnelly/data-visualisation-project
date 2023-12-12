from turtle import color
from dash import dash_table
from matplotlib.font_manager import font_family_aliases
from utils.settings import get_colours

from utils import data_filtering
from utils.airport_country_mapping import get_flight_df_with_country

def get_table_data(flight_data, airport_data):
    flight_data_table = data_filtering.get_unique_flight_routes(flight_data)
    flight_data_table = get_flight_df_with_country(flight_data_table, airport_data)

    new_col_names = {
        "from_country": "Departure country",
        "from_airport_code": "Departure airport code",
        "count": "# of flights",
        "dest_country": "Arrival country",
        "dest_airport_code": "Arrival airport code",
    }
    flight_data_table = flight_data_table.rename(columns=new_col_names).sort_values(by="# of flights", ascending=False)[list(new_col_names.values())]
    return flight_data_table

def get_table_header_styling():
    return [{'if': {'column_id': ["Departure country", "Departure airport code"]}, 'backgroundColor': get_colours()[True]},
            {'if': {'column_id': ["Arrival country", "Arrival airport code"]}, 'backgroundColor': get_colours()[False], 'textAlign': 'right'},
            {'if': {'column_id': '# of flights'}, 'textAlign': 'center'}]

def get_table(flight_data, airport_data):
    flight_data_table = get_table_data(flight_data, airport_data)
    return dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} 
                    for i in flight_data_table.columns],
            page_size=10,
            data=flight_data_table.to_dict('records'),
            style_cell=dict(textAlign='left'),
            cell_selectable=False,
            style_header_conditional=get_table_header_styling(),
            style_header=dict(backgroundColor="#7570b3", border='none', color='white', font_family='Segoe UI', fontWeight='bold', padding='0px 10px'),
            style_cell_conditional=[
                {
                    'if': {'column_id': '# of flights'},
                    'width': '8.5%',
                    'textAlign': 'center'
                },
                {
                    'if': {'column_id': ["Departure country", "Departure airport code"]},
                    'width': '22.75%',
                },
                {
                    'if': {'column_id': ["Arrival country", "Arrival airport code"]},
                    'textAlign': 'right'
                }
            ],
            style_data=dict(backgroundColor="white", border='1px solid #eee', color='#444', font_family='Segoe UI', padding='0px 10px')
    ) 