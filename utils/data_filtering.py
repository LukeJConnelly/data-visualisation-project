
def get_unique_flight_routes(clean_flight_df):
    flight_routes = clean_flight_df[["from_airport_code", "dest_airport_code"]]
    flight_routes = flight_routes.groupby(['from_airport_code', 'dest_airport_code']).size().reset_index(name='count')

    return flight_routes
