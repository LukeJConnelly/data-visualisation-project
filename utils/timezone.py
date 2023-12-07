import pytz
from timezonefinder import TimezoneFinder
from utils import data_loader
import pandas as pd
from datetime import datetime
import os

def get_timezone_from_IATA(airport_data, IATA):
    if IATA not in airport_data["IATA Code"].to_list():
        return None

    lat, lon = tuple(airport_data[airport_data["IATA Code"] == IATA][["Latitude Decimal Degrees","Longitude Decimal Degrees"]].iloc[0])
    return get_timezone_from_coordinates(lat, lon)

def get_timezone_from_saved_IATA(IATA):
    from utils.data_loader import AIRPORT_DATA
    return AIRPORT_DATA[AIRPORT_DATA["IATA Code"] == IATA][["Timezone"]].iloc[0]

def get_timezone_from_coordinates(latitude, longitude):
    """ Yanked from ChatGPT
    Get the timezone for a given latitude and longitude.

    Args:
        latitude (float): The latitude coordinate.
        longitude (float): The longitude coordinate.

    Returns:
        str: The timezone name, or None if not found.
    """
    # Create a TimezoneFinder instance
    tf = TimezoneFinder()

    # Get the timezone at the specified coordinates
    timezone_str = tf.timezone_at(lng=longitude, lat=latitude)
    if timezone_str:
        # Get the timezone object
        return pytz.timezone(timezone_str)
    
    raise Exception("!Timezones are so much fun")

def get_time_diff_on_date(date_to_compare, timezone1, timezone2):
    """
    returns time difference as datetime.timedelta 
    """
    if None in [date_to_compare, timezone1, timezone2]:
        return None

    # some pandas wierd stuff
    # if (type(timezone1) == "<class 'pandas.core.series.Series'>")
    timezone1 = timezone1.values[0]
    timezone2 = timezone2.values[0]
    
    localized_time1 = timezone1.localize(date_to_compare)
    localized_time2 = timezone2.localize(date_to_compare)

    # Calculate the time difference
    time_difference = localized_time1 - localized_time2
    return time_difference

def get_time_diff_from_IATA(date_to_compare, IATA1, IATA2):
    tz1 = get_timezone_from_saved_IATA(IATA1)
    tz2 = get_timezone_from_saved_IATA(IATA2)
    return get_time_diff_on_date(date_to_compare, tz1, tz2)

def get_airport_timezone_dict(airport_IATA_list, airport_data, local_datetime=datetime(2022, 4, 30, 14, 0, 0), timezone_str="GMT"):
    timezones = {IATA: get_timezone_from_IATA(airport_data, IATA) for IATA in airport_IATA_list}

    # Define a datetime in your local timezone

    # Define the target timezone (GMT)
    target_timezone = pytz.timezone(timezone_str)

    # Convert the local datetime to GMT
    return {airport: local_datetime.astimezone(timezone) for airport, timezone in timezones.items()}

def get_airport_time_diffs(airport_IATA_list, airport_data, local_datetime=datetime(2022, 4, 30, 14, 0, 0), timezone_str="GMT"):

    localized_timeszones = get_airport_timezone_dict(airport_IATA_list, airport_data, local_datetime, timezone_str)

    amount_of_airports = len(airport_IATA_list)

    from_airport = []
    dest_airport = []
    timezone_diff = []
    
    for from_air in airport_IATA_list:
        from_airport += [from_air] * amount_of_airports
        from_tz = localized_timeszones[from_air]
        from_tz = from_tz.replace(hour=local_datetime.hour, minute=local_datetime.minute, second=local_datetime.second)

        for dest_air in airport_IATA_list:
            dest_airport.append(dest_air)
            dest_tz = localized_timeszones[dest_air]
            dest_tz = dest_tz.replace(hour=local_datetime.hour, minute=local_datetime.minute, second=local_datetime.second)
            try:
                time_diff = dest_tz - from_tz
                timezone_diff.append(time_diff)
            except Exception:
                timezone_diff.append(None)
    df = pd.DataFrame({"from_airport_code": from_airport, "dest_airport_code": dest_airport, "timezone_diff": timezone_diff})
    return df 

def add_tz_diff_to_flight_df(flight_df, airport_time_diff_df):
    new_df = flight_df.copy()
    merged_df = new_df.merge(airport_time_diff_df, on=['from_airport_code', 'dest_airport_code'], how='left')
    return merged_df


if __name__ == "__main__":
    TZ_FILEPATH = 'data/timezone_differences.csv'

    flight_data = data_loader.load_flight_data()
    airport_data = data_loader.load_airport_data(flight_data=flight_data, with_airport_degree=True)
    
    airports = data_loader.all_airports_list(flight_data)

    tz_dict = get_airport_timezone_dict(airports, airport_data)
    print(tz_dict)

    tz_diff = None
    if os.path.exists(TZ_FILEPATH):
        tz_diff = pd.read_csv(TZ_FILEPATH)
    
    else:
        tz_diff = get_airport_time_diffs(airports, airport_data)
        tz_diff.to_csv(TZ_FILEPATH, index=False)

    flight_data_with_timediff = add_tz_diff_to_flight_df(flight_data, tz_diff)
    print(flight_data_with_timediff)
        
    print(tz_diff.head())
    print(tz_diff.tail())

    # timezones = [get_timezone_from_IATA(IATA) for IATA in airports]
    # test_time_to_compare = datetime(2022, 4, 30, 14, 30, 0)

    # print(timezones)
    # print(get_time_diff_on_date(test_time_to_compare, timezones[0], timezones[1]))