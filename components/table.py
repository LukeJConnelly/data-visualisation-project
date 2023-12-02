from turtle import color
from dash import dash_table
from matplotlib.font_manager import font_family_aliases

from  utils import data_filtering

def get_table_data(flight_data):
    flight_data_table = data_filtering.get_unique_flight_routes(flight_data)
    new_col_names = {
        "from_country": "Departure country",
        "from_airport_code": "Departure airport code",
        "dest_country": "Arrival country",
        "dest_airport_code": "Arrival airport code",
        "count": "Number of flights"
    }
    flight_data_table = flight_data_table.rename(columns=new_col_names)
    return flight_data_table

def get_table(flight_data):
    flight_data_table = get_table_data(flight_data)
    return dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} 
                    for i in flight_data_table.columns],
            data=flight_data_table.to_dict('records'),
            style_cell=dict(textAlign='left'),
            cell_selectable=False,
            style_header=dict(backgroundColor="#9ab6e6", border='none', color='white', font_family='Segoe UI', fontWeight='bold'),
            style_data=dict(backgroundColor="white", border='1px solid #eee', color='#444', font_family='Segoe UI')
    ) 