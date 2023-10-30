import pandas as pd
import numpy as np
import os

def load_airport_data(data_filepath="data/GlobalAirportDatabase/GlobalAirportDatabase.txt", flight_data=None, with_airport_degree=False):
    """
    Load airport data based on the GlobalAirportDatabase dataset
    """
    assert os.path.exists(data_filepath), f"{data_filepath} not found! Make sure to run from root folder!"
    assert not (with_airport_degree and flight_data is None), "With_airport_degree requires flight_data as input"


    dtype_dict = {"ICAO Code": str,
                    "IATA Code": str,
                    "Airport Name": str,
                    "City/Town": str,
                    "Country": str,
                    "Latitude Degrees": int,
                    "Latitude Minutes": int,
                    "Latitude Seconds": int,
                    "Latitude Direction": str,
                    "Longitude Degrees": int,
                    "Longitude Minutes": int,
                    "Longitude Seconds": int,
                    "Longitude Direction": str,
                    "Altitude": int,
                    "Latitude Decimal Degrees": float,
                    "Longitude Decimal Degrees": float
                    }

    airport_data = pd.read_csv(data_filepath,
                                sep=":",
                                names=dtype_dict.keys(),
                                dtype=dtype_dict,
                                skiprows=[0]
                                )
    airport_data.fillna('N/A', inplace=True)

    if with_airport_degree:
        airport_data = add_airport_degree(airport_data=airport_data, flight_data=flight_data)

    return airport_data

def split_and_clean_column(df, column_name, seperator='|', remove_head=0, remove_tail=None):
    """splits and cleans a string column of a dataframe

    Args:
        df (pandas.DataFrame): dataframe to be modified
        column_name (str): column to be modified
        seperator (str, optional): what to split the column by. Defaults to '|'.
        remove_head (int, optional): how many characters to remove from the start of the string. Defaults to 0.
        remove_tail (int, optional): how many characters to remove from the end of the string. Defaults to None.

    Returns:
        pandas.DataFrame: modified dataframe
    """
    df[column_name] = [[y.strip() for y in 
                        x[remove_head:-remove_tail if remove_tail else None].split(seperator)]
                       if type(x) == str else [] for x in df[column_name]]
    return df    
    
def map_column(df, column_name, mapping_dict, is_list=False):
    """Map a column in a dataframe to a new column using a mapping dictionary

    Args:
        df (pandas.DataFrame): dataframe to be modified
        column_name (str): column to be mapped
        mapping_dict (dict): dict for mapping strings
        is_list (bool, optional): whether the column is a list. Defaults to False.

    Returns:
       pandas.DataFrame: modified dataframe
    """
    if is_list:
        df[column_name] = [[mapping_dict[y] if y in mapping_dict else y for y in x] for x in df[column_name]]
    else:
        df[column_name] = df[column_name].map(mapping_dict)
    return df

def min_max_scaling(column):
    '''
    Min-Max scales a column
    (used in clean_co2 function)
    '''
    return (column - column.min()) / (column.max() - column.min())

def clean_co2(data):
    '''
    Cleans the co2 columns
    - normalises the co2_emissions collumn
    - re-calculates the avg_co2_emissions_for_this_route column
    - re-calculates the co2_percentage column
    (necessary because documentation for the data was lacking)
    '''
    # scaling the co2_emissions collumn
    data["co2_emissions"] = min_max_scaling(data["co2_emissions"])

    # calculating and inserting avg c02 emissions for each route
    groups = data.groupby(["from_airport_code", "dest_airport_code"])["co2_emissions"].mean()
    for index, row in data.iterrows():
        data.at[index, "avg_co2_emission_for_this_route"] = groups[row["from_airport_code"]][row["dest_airport_code"]]
    
    # calculating and incerting difference between a flight and its' average co2 emissons
    for index, row in data.iterrows():
        data.at[index, "co2_percentage"] = ((row["avg_co2_emission_for_this_route"] - row["co2_emissions"])/row["avg_co2_emission_for_this_route"])
    
    return data

def load_flight_data(data_filepath="data/flights.csv"):
    assert os.path.exists(data_filepath), f"{data_filepath} not found! Make sure to run from root folder!"
    data = pd.read_csv( data_filepath)

    dtype_dict = {
        "from_airport_code": str,
        "from_country": str,
        "dest_airport_code": str,
        "dest_country": str,
        "aircraft_type": str,
        "airline_number": str,
        "airline_name": str,
        "flight_number": str,
        "departure_time": str,
        "arrival_time": str,
        "duration": int,
        "stops": 'Int64',
        "price": float,
        "currency": str,
        "co2_emissions": 'Int64',
        "avg_co2_emission_for_this_route": 'Int64',
        "co2_percentage": str,
        "scan_date": str
    }
    
    data['departure_time'] = pd.to_datetime(data['departure_time'], format='%Y-%m-%d %H:%M:%S')
    data['arrival_time'] = pd.to_datetime(data['arrival_time'], format='%Y-%m-%d %H:%M:%S')
    data['scan_date'] = pd.to_datetime(data['scan_date'], format='%Y-%m-%d %H:%M:%S')
    data['duration'] = pd.to_timedelta(data['duration'], unit='m')
    
    # Miscellaneous mapping
    data = map_column(split_and_clean_column(data, 'aircraft_type'), 'aircraft_type', {'Airbus A318': 'Example Mapping'}, is_list=True)
    data = map_column(split_and_clean_column(data, 'airline_name', remove_head=1, remove_tail=1), 'airline_name', {}, is_list=True)
    data = split_and_clean_column(data, 'flight_number')
    data = clean_co2(data)

    return data


##################################################################


def all_airports_list(flight_data, from_col="from_airport_code", dest_col="dest_airport_code"):
    """
    List all unique airports in the flight dataset based on specified columns
    """
    depature_airports = set(flight_data[from_col])
    arrival_airports = set(flight_data[dest_col])
    return list(set.union(depature_airports, arrival_airports))


def add_airport_degree(airport_data, flight_data):
    """
    adds degree in/out to airport
    Returns:
        Dataframe: airport_data with added degrees for "flights in", "flights out" and "flight_degree"
    """
    
    deg_in = np.zeros(airport_data.shape[0], dtype=int)
    deg_out = np.zeros(airport_data.shape[0], dtype=int)

    all_airports = all_airports_list(flight_data)
    for airport in all_airports:
        if not (airport) in airport_data["IATA Code"].tolist():
            continue
        
        index = airport_data["IATA Code"].tolist().index(airport)
        deg_in[index] = flight_data["dest_airport_code"].to_list().count(airport)
        deg_out[index] = flight_data["from_airport_code"].to_list().count(airport)
    
    airport_data["flights in"] = deg_in
    airport_data["flights out"] = deg_out
    airport_data["flight_degree"] = [max(0,deg_in+deg_out) for deg_in, deg_out in zip(deg_in, deg_out)]
    return airport_data