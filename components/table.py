from dash import dash_table

from  utils import data_filtering

def get_table_data(flight_data):
    flight_data_table = data_filtering.get_unique_flight_routes(flight_data)
    new_col_names = {
        "from_country": "Departure country",
        "from_airport_code": "Departure airport code",
        "dest_country": "Arrival country",
        "dest_airport_code": "Arrival airport code",
        "count": "Amount of flights"
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
            style_header=dict(backgroundColor="paleturquoise"),
            style_data=dict(backgroundColor="lavender")
    ) 