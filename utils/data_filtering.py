import pandas as pd

def get_unique_flight_routes(clean_flight_df):
    flight_routes = clean_flight_df[["from_airport_code", "dest_airport_code"]]
    flight_routes = flight_routes.groupby(["from_airport_code", "dest_airport_code"]).size().reset_index(name='count')

    return flight_routes

def get_airport_country_df(flight_df, airport_df):
    data_dict = {
        "airport": list(flight_df["from_airport_code"]) + list(flight_df["dest_airport_code"]),
        "country": list(flight_df["from_country"]) + list(flight_df["dest_country"])

    }
    new_df = pd.DataFrame(data_dict)
    airport_country_df = new_df.groupby(["airport", "country"]).size().reset_index(name='count')[["airport","country"]]
    return airport_country_df

def get_aircraft_type_count(clean_flight_df):
    aircraft_type_df = clean_flight_df["aircraft_type"]
    aircraft_type_count_df = aircraft_type_df.explode().value_counts().reset_index()
    aircraft_type_count_df.columns = ["aircraft_type", "count"]
    return aircraft_type_count_df

def get_flights_with_aircraft_type(clean_flight_df, aircraft_type):
    filtered_flights = clean_flight_df[clean_flight_df['aircraft_type'].apply(lambda x: aircraft_type in x)]

    return filtered_flights