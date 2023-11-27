def get_unique_flight_routes(clean_flight_df):
    flight_routes = clean_flight_df[["from_airport_code", "from_country", "dest_airport_code", "dest_country"]]
    flight_routes = flight_routes.groupby(["from_airport_code", "from_country", "dest_airport_code", "dest_country"]).size().reset_index(name='count')

    return flight_routes

def get_aircraft_type_count(clean_flight_df):
    aircraft_type_df = clean_flight_df["aircraft_type"]
    aircraft_type_count_df = aircraft_type_df.explode().value_counts().reset_index()
    return aircraft_type_count_df

def get_flights_with_aircraft_type(clean_flight_df, aircraft_type):
    filtered_flights = clean_flight_df[clean_flight_df['aircraft_type'].apply(lambda x: aircraft_type in x)]

    return filtered_flights

def map_selection(ctx, clean_flight_df, selectedData, ORIGINAL_FLIGHT_DATA):
    """
    Returns a list of iata codes and a filtered df 
    """
    if selectedData is None:
        return [], clean_flight_df
    
    if (ctx.triggered_id == "flight-map" and selectedData is None):
        flight_data = ORIGINAL_FLIGHT_DATA
    elif (ctx.triggered_id != "flight-map"):
        flight_data = ORIGINAL_FLIGHT_DATA

    iata_codes = [data_point["text"][:3] for data_point in selectedData["points"]]
    if (len(iata_codes) > 0):
        clean_flight_df = clean_flight_df[(clean_flight_df["from_airport_code"].isin(iata_codes)) | (flight_data["dest_airport_code"].isin(iata_codes))]
    
    return clean_flight_df