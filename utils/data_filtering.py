def get_unique_flight_routes(clean_flight_df):
    flight_routes = clean_flight_df[["from_airport_code", "dest_airport_code"]]
    flight_routes = flight_routes.groupby(['from_airport_code', 'dest_airport_code']).size().reset_index(name='count')

    return flight_routes

def get_aircraft_type_count(clean_flight_df):
    aircraft_type_df = clean_flight_df["aircraft_type"]
    aircraft_type_count_df = aircraft_type_df.explode().value_counts().reset_index()
    return aircraft_type_count_df

def get_flights_with_aircraft_type(clean_flight_df, aircraft_type):
    filtered_flights = clean_flight_df[clean_flight_df['aircraft_type'].apply(lambda x: aircraft_type in x)]

    return filtered_flights