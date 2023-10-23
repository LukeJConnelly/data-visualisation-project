import networkx as nx

def get_flight_graph(airport_data, flight_data):

    graph = nx.Graph()

    nodes = {airport: (lat, lng) for airport,lat,lng in zip(airport_data["IATA Code"], airport_data["Latitude Decimal Degrees"], airport_data["Longitude Decimal Degrees"])}
    edges = [(departure, arrival) for departure, arrival in zip(flight_data["from_airport_code"], flight_data["dest_airport_code"])]
    graph.add_nodes_from(nodes)
    graph.add_edges_from(edges)
    return graph

if __name__ == "__main__":
    from utils.data_loader import load_airport_data, load_flight_data
    import os 


    AIRPORT_DATA_PATH = "data/GlobalAirportDatabase/GlobalAirportDatabase.txt"
    FLIGHT_DATA_PATH = "data/flights.csv"


    FLIGHT_DATA = load_flight_data(FLIGHT_DATA_PATH)
    AIRPORT_DATA = load_airport_data(AIRPORT_DATA_PATH, flight_data=FLIGHT_DATA)

    get_flight_graph(AIRPORT_DATA, FLIGHT_DATA)