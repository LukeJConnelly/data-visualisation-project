import pandas as pd
import os

from utils import data_preprocessing
# import data_preprocessing

def load_data(raw_flights_file_path= "data/flights.csv", raw_airport_file_path="data/GlobalAirportDatabase/GlobalAirportDatabase.txt"):
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
    clean_flight_df_exist = os.path.exists("data/clean_flights.csv")
    clean_airport_df_exist = os.path.exists("data/clean_airport.csv")
    
    # get clean flight data
    if clean_flight_df_exist:
        clean_flight_df = pd.read_csv("data/clean_flights.csv")

    # get clean airport data
    if clean_airport_df_exist:
        clean_airport_df = pd.read_csv("data/clean_airport.csv")

    if (clean_flight_df_exist and clean_airport_df_exist):
        return clean_flight_df, clean_airport_df
    
    ### IF CLEAN DATA IS NOT FOUND 
    assert os.path.exists(raw_flights_file_path), f"{raw_flights_file_path} not found! Make sure to run from root folder!"
    assert os.path.exists(raw_airport_file_path), f"{raw_airport_file_path} not found! Make sure to run from root folder!"

    flight_df = pd.read_csv(raw_flights_file_path)
    airport_df = pd.read_csv(raw_airport_file_path, sep=":", header=None)
    
    # Convert data to correct data types 
    flight_df = data_preprocessing.convert_flight_df(flight_df)
    airport_df = data_preprocessing.convert_airport_df(airport_df)

    # clean data 
    clean_flight_df = data_preprocessing.cleaning_func_flight_df(flight_df)
    clean_airport_df = data_preprocessing.cleaning_func_airport_df(airport_df, flight_df)

    # add degree to airport
    airport_df = data_preprocessing.add_airport_degree(airport_df, flight_df)

    # save clean data types
    clean_flight_df.to_csv("data/clean_flights.csv", index=False)
    clean_airport_df.to_csv("data/clean_airport.csv", index=False)

    return clean_flight_df, clean_airport_df

if __name__ == "__main__":
    flight_df, airport_df = load_data()

    print("flight_df shape", flight_df.shape)
    print("airport_df shape", airport_df.shape)