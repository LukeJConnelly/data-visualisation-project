from geopy.geocoders import Nominatim
import pycountry_convert as pc

def country_to_continent(country_code):
    country_continent_code = pc.country_alpha2_to_continent_code(country_code.upper())
    country_continent_name = pc.convert_continent_code_to_continent_name(country_continent_code)
    return country_continent_name

def get_continent_from_coordinates(latitude, longitude):
    geolocator = Nominatim(user_agent="Datavis")
    location = geolocator.reverse((latitude, longitude), language='en')
    
    if location and "country_code" in location.raw["address"]:
        return country_to_continent(location.raw["address"]["country_code"])
    else:
        return 'Unknown'
