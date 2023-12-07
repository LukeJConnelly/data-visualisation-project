import pandas as pd

def get_flight_df_with_country(flight_data, airport_data):
    airport_country_mapping = airport_data[["IATA Code", "Country"]].copy()

    airport_country_mapping.rename(columns={"IATA Code": "from_airport_code", "Country": "from_country"}, inplace=True)
    flight_df = pd.merge(flight_data, airport_country_mapping)

    airport_country_mapping.rename(columns={"from_airport_code": "dest_airport_code", "from_country": "dest_country"}, inplace=True)
    flight_df = pd.merge(flight_df, airport_country_mapping)

    return flight_df