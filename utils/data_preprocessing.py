import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tqdm import tqdm
import pytz

from utils.timezone import get_timezone_from_IATA
from utils.continent import get_continent_from_coordinates

#######################################################
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


def clean_co2(data):
    '''
    Cleans the co2 columns
    - normalises the co2_emissions collumn
    - re-calculates the avg_co2_emissions_for_this_route column
    - re-calculates the co2_percentage column
    (necessary because documentation for the data was lacking)
    '''
    # scaling the co2_emissions column
    scaler = MinMaxScaler()
    data.loc[:, 'co2_emissions'] = scaler.fit_transform(data[['co2_emissions']])

    # calculating and inserting avg c02 emissions for each route
    groups = data.groupby(["from_airport_code", "dest_airport_code"])["co2_emissions"].mean()
    data.loc[:, 'avg_co2_route'] = data.apply(lambda x: groups[(x['from_airport_code'], x['dest_airport_code'])], axis=1)

    # calculating and inserting difference between a flight and its' average co2 emissons
    data.loc[:, 'co2_percentage'] = ((data['avg_co2_route'] - data['co2_emissions'])/data['avg_co2_route'])
    return data

#######################################################
def convert_flight_df(flight_df):
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

    for column, dtype in dtype_dict.items():
        flight_df[column] = flight_df[column].astype(dtype)
    
    flight_df['departure_time'] = pd.to_datetime(flight_df['departure_time'], format='%Y-%m-%d %H:%M:%S')
    flight_df['arrival_time'] = pd.to_datetime(flight_df['arrival_time'], format='%Y-%m-%d %H:%M:%S')
    flight_df['scan_date'] = pd.to_datetime(flight_df['scan_date'], format='%Y-%m-%d %H:%M:%S')
    flight_df['duration'] = pd.to_timedelta(flight_df['duration'], unit='m')
    
    # Miscellaneous mapping ({} represents mapping dict)
    flight_df = map_column(split_and_clean_column(flight_df, 'aircraft_type'), 'aircraft_type', {}, is_list=True)
    flight_df = map_column(split_and_clean_column(flight_df, 'airline_name', remove_head=1, remove_tail=1), 'airline_name', {}, is_list=True)
    flight_df = split_and_clean_column(flight_df, 'flight_number')
    
    return flight_df

def convert_airport_df(airport_df):

    airport_dtype_dict = {"ICAO Code": str,
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
    airport_df.columns = airport_dtype_dict.keys()
    airport_df.fillna('N/A', inplace=True)

    return airport_df

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

def add_airport_continent(airport_df):
    airport_df['Continent'] = airport_df.apply(lambda row: get_continent_from_coordinates(row["Latitude Decimal Degrees"], row["Longitude Decimal Degrees"]), axis=1)
    return airport_df

#######################################################
def add_manual_airport_data(airport_df):
    missing_data = {
        "NBO": {
            "Latitude Decimal Degrees": -1.333,
            "Longitude Decimal Degrees": 36.927,
            "Country": "KENYA"
        },
        "ICN": {
            "Latitude Decimal Degrees": 37.469,
            "Longitude Decimal Degrees": 126.450,
            "Country": "SOUTH KOREA"
        },
        "ATH": {
            "Latitude Decimal Degrees": 37.936401,
            "Longitude Decimal Degrees": 23.9445,
            "Country": "GREECE"
        },
        "PVG": {
            "Latitude Decimal Degrees": 31.143,
            "Longitude Decimal Degrees": 121.805,
            "Country": "CHINA"
        },
        "SAW": {
            "Latitude Decimal Degrees": 40.898,
            "Longitude Decimal Degrees": 29.309,
            "Country": "TURKEY"
        },
        "DME": {
            "Latitude Decimal Degrees": 55.408,
            "Longitude Decimal Degrees": 37.906,
            "Country": "RUSSIA"
        },
        "LHR": {
            "Latitude Decimal Degrees": 51.470,
            "Longitude Decimal Degrees": -0.454,
            "Country": "UNITED KINGDOM"
        },
        "MNL": {
            "Latitude Decimal Degrees": 14.509,
            "Longitude Decimal Degrees": 121.019,
            "Country": "PHILIPPINES"
        }
    }
    
    for airport, missing_data in missing_data.items():
        if not (airport in airport_df['IATA Code'].values):
            new_row = pd.DataFrame([{"IATA Code": airport, **missing_data}])
            airport_df = pd.concat([airport_df, new_row], ignore_index=True)
        index = airport_df[airport_df['IATA Code'] == airport].index[0]

        for name, val in missing_data.items():
            airport_df.at[index, name] = val
    return airport_df

def remove_duplicate_airport(airport_df):
    """
    Duplicate airports are removed and the correct is added manually 
    """
    airport_df = airport_df[airport_df["IATA Code"] != "MNL"]
    airport_df = airport_df[airport_df["IATA Code"] != "LHR"]
    return airport_df

# def cleaning_func_flight_df(flight_df, wanted_cols=["from_airport_code","from_country","dest_airport_code","dest_country","aircraft_type","airline_number","airline_name","flight_number","departure_time","arrival_time","duration","stops","price","currency","co2_emissions","avg_co2_emission_for_this_route","co2_percentage"]):
def cleaning_func_flight_df(flight_df, wanted_cols=["from_airport_code","dest_airport_code","aircraft_type","airline_number","airline_name","flight_number","departure_time","arrival_time","duration","stops","price","currency","co2_emissions","avg_co2_emission_for_this_route","co2_percentage"]):
    # Get wanted cols 
    if (len(wanted_cols) > 0):
        flight_df = flight_df[wanted_cols]
    
    flight_df = clean_co2(flight_df)
    return flight_df


def cleaning_func_airport_df(airport_df, flight_df, wanted_cols=["IATA Code", "Country", "Latitude Decimal Degrees", "Longitude Decimal Degrees"]):
# def cleaning_func_airport_df(airport_df, flight_df, wanted_cols=["IATA Code", "Latitude Decimal Degrees", "Longitude Decimal Degrees", "flights in", "flights out", "flight_degree"]):
    # Get wanted cols 
    if (len(wanted_cols) > 0):
        airport_df = airport_df[wanted_cols]

    airport_df = remove_duplicate_airport(airport_df)
    airport_df = add_manual_airport_data(airport_df)

    # Get only relevant airports 
    airport_list = all_airports_list(flight_df)
    airport_df = airport_df[airport_df['IATA Code'].isin(airport_list)]
    
    return airport_df

def get_gmt_time(times, codes, airport_df):
    timezones = [get_timezone_from_IATA(airport_df, c) for c in tqdm(airport_df['IATA Code'], desc="Calculating timezones")]
    timezone_lookup = dict(zip(airport_df['IATA Code'], timezones))

    gmt_tz = pytz.timezone('GMT')
    
    return [timezone_lookup[c].localize(t).astimezone(gmt_tz) for t, c in tqdm(zip(times, codes), desc="Adding GMT times to df")]