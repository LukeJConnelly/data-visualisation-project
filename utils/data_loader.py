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

    return data


##################################################################

def all_airports_list(flight_data):
    """
    List all unique airports in the flight dataset
    """
    depature_airports = set(flight_data["from_airport_code"])
    arrival_airports = set(flight_data["dest_airport_code"])
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