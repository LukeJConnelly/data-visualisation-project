import pandas as pd
import data_loader

def add_manual_airport_data(airport_df):
    missing_data = {
        "LHR": {
            "Latitude Decimal Degrees": 51.470,
            "Longitude Decimal Degrees": -0.454
        },
        "NBO": {
            "Latitude Decimal Degrees": -1.333,
            "Longitude Decimal Degrees": 36.927
        }
    }

    for airport, missing_data in missing_data.items():
        index = airport_df[airport_df['IATA Code'] == airport].index[0]

        for name, val in missing_data.items():
            airport_df.at[index, name] = val
    return airport_df

def get_unique_flight_routes(clean_flight_df):
    flight_routes = clean_flight_df[["from_airport_code", "dest_airport_code"]]
    flight_routes = flight_routes.groupby(['from_airport_code', 'dest_airport_code']).size().reset_index(name='count')

    return flight_routes

def cleaning_func_flight_df(flight_df, wanted_cols=["from_airport_code","dest_airport_code","aircraft_type","airline_number","airline_name","flight_number","departure_time","arrival_time","duration","stops","price","currency","co2_emissions","avg_co2_emission_for_this_route","co2_percentage"]):
    # Get wanted cols 
    if (len(wanted_cols) > 0):
        flight_df = flight_df[wanted_cols]
    
    return flight_df


def cleaning_func_airport_df(airport_df, flight_df, wanted_cols=["IATA Code", "Latitude Decimal Degrees", "Longitude Decimal Degrees", "flights in", "flights out", "flight_degree"]):
    # Get wanted cols 
    if (len(wanted_cols) > 0):
        airport_df = airport_df[wanted_cols]

    airport_df = add_manual_airport_data(airport_df)

    # Get only relewant airports 
    airport_list = data_loader.all_airports_list(flight_df)
    airport_df = airport_df[airport_df['IATA Code'].isin(airport_list)]
    
    return airport_df


if __name__ == "__main__":
    import os 

    DATAFOLDERPATH = 'data'
    CLEAN_FLIGHT_PATH = f"{DATAFOLDERPATH}/clean_flights.csv"
    CLEAN_AIRPORT_PATH = f"{DATAFOLDERPATH}/clean_airport.csv"

    flight_data = data_loader.load_flight_data()
    airport_data = data_loader.load_airport_data(flight_data=flight_data, with_airport_degree=True)

    # get clean flight data
    if os.path.exists(CLEAN_FLIGHT_PATH):
        clean_flight_df = pd.read_csv(CLEAN_FLIGHT_PATH)
    else:
        clean_flight_df = cleaning_func_flight_df(flight_data)
        clean_flight_df.to_csv(CLEAN_FLIGHT_PATH, index=False)

    # get clean airport data
    if os.path.exists(CLEAN_AIRPORT_PATH):
        clean_airport_df = pd.read_csv(CLEAN_AIRPORT_PATH)
    else:
        clean_airport_df = cleaning_func_airport_df(airport_data, flight_data)
        clean_airport_df.to_csv(CLEAN_AIRPORT_PATH, index=False)
    
    unique_flight_routes = get_unique_flight_routes(clean_flight_df)
    print(unique_flight_routes.head())

    print("airport data:", airport_data.shape)
    print("clean airport data:", clean_airport_df.shape)
    print("flight data:", flight_data.shape)
    print("clean flight data:", clean_flight_df.shape)
