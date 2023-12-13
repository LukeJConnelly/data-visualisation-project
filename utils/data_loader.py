from bleach import clean
import pandas as pd
import os
import json
import ast

from utils import data_preprocessing
from utils import data_filtering
# import data_preprocessing

def load_data(sample_mode=False, raw_flights_file_path= "data/flights.csv", raw_airport_file_path="data/GlobalAirportDatabase/GlobalAirportDatabase.txt"):
    """
    Loads the data as pd dataframes Assumes a data folder named "data" in project folder.
    If no clean data is found the raw data will be preprocessed and saved as csv.
    If clean data is found (raw_flights_file_path and raw_airport_file_path) will NOT be used!
    Clean data is assumed to be found as: 
        * data/clean_flights.csv
        * data/clean_airport.csv
    
    Returns:
        Tuple[pd.DataFrame, pd.DataFrame]: flight data, airport data 
    """
    LATEST_VERSION = 4.0
    version_stored = None
        
    clean_flight_df_exist = os.path.exists("data/clean_flights.csv")
    clean_airport_df_exist = os.path.exists("data/clean_airport.csv")

    if (os.path.exists("data/metadata.json")):
        with open("data/metadata.json", "r") as file:
            data = json.loads(file.read())
            version_stored = data["version"]
    
    if LATEST_VERSION != version_stored:
        try:
            os.remove("data/clean_flights.csv")
            os.remove("data/clean_airport.csv")
        except OSError:
            pass
        clean_flight_df_exist = os.path.exists("data/clean_flights.csv")
        clean_airport_df_exist = os.path.exists("data/clean_airport.csv")
    
    # get clean flight data
    if clean_flight_df_exist:
        clean_flight_df = pd.read_csv("data/clean_flights.csv") if not sample_mode else pd.read_csv("data/clean_flights.csv", nrows=500)
        # convert lists to list after load as string
        for col_with_list in ["aircraft_type", "airline_name", "flight_number"]:
            # clean_flight_df[col_with_list] = clean_flight_df[col_with_list].apply(json.loads)
            clean_flight_df[col_with_list] = clean_flight_df[col_with_list].apply(ast.literal_eval)
        clean_flight_df["departure_time"] = pd.to_datetime(clean_flight_df["departure_time"])
        clean_flight_df["arrival_time"] = pd.to_datetime(clean_flight_df["arrival_time"])
        clean_flight_df["departure_time_gmt"] = pd.to_datetime(clean_flight_df["departure_time_gmt"])
        clean_flight_df["arrival_time_gmt"] = pd.to_datetime(clean_flight_df["arrival_time_gmt"])

    # get clean airport data
    if clean_airport_df_exist:
        clean_airport_df = pd.read_csv("data/clean_airport.csv")

    if clean_flight_df_exist and clean_airport_df_exist:
        return clean_flight_df, clean_airport_df
    
    ### IF CLEAN DATA IS NOT FOUND 
    
    assert os.path.exists(raw_flights_file_path), f"{raw_flights_file_path} not found! Make sure to run from root folder!"
    assert os.path.exists(raw_airport_file_path), f"{raw_airport_file_path} not found! Make sure to run from root folder!"

    flight_df = pd.read_csv(raw_flights_file_path)
    airport_df = pd.read_csv(raw_airport_file_path, sep=":", header=None)

    
    # Convert data to correct data types 
    flight_df = data_preprocessing.convert_flight_df(flight_df)
    airport_df = data_preprocessing.convert_airport_df(airport_df)

    airport_country_df = data_filtering.get_airport_country_df(flight_df, airport_df)
    # airport_df = pd.merge(airport_df, airport_country_df, left_on='IATA Code', right_on='airport')

    # clean data 
    clean_flight_df = data_preprocessing.cleaning_func_flight_df(flight_df)
    clean_airport_df = data_preprocessing.cleaning_func_airport_df(airport_df, flight_df)

    # add degree to airport
    clean_airport_df = data_preprocessing.add_airport_degree(clean_airport_df, clean_flight_df)
    clean_airport_df = data_preprocessing.add_airport_continent(clean_airport_df)
    clean_flight_df['departure_time_gmt'] = data_preprocessing.get_gmt_time(clean_flight_df['departure_time'], clean_flight_df['from_airport_code'], clean_airport_df)
    clean_flight_df['arrival_time_gmt'] = data_preprocessing.get_gmt_time(clean_flight_df['arrival_time'], clean_flight_df['dest_airport_code'], clean_airport_df)

    # save clean data types
    clean_flight_df.to_csv("data/clean_flights.csv", index=False)
    clean_airport_df.to_csv("data/clean_airport.csv", index=False)
    with open("data/metadata.json", "w") as file:
        file.write(json.dumps({"version": LATEST_VERSION}))

    # return clean_flight_df, clean_airport_df
    # Yay recursion! <3 
    return load_data(sample_mode, raw_flights_file_path, raw_airport_file_path)

if __name__ == "__main__":
    flight_df, airport_df = load_data()

    print("flight_df shape", flight_df.shape)
    print("airport_df shape", airport_df.shape)