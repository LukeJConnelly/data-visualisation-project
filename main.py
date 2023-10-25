import plotly.graph_objects as go
import plotly
import pandas as pd
from utils import data_loader

if __name__ == "__main__":
    flight_data = data_loader.load_flight_data()
    airport_data = data_loader.load_airport_data(flight_data=flight_data, with_airport_degree=True)
    airport_data = airport_data[airport_data["flight_degree"] >= 1]
    
    # Add source and destination airport data to flight data
    flights_with_source_and_destination_df = pd.merge(flight_data,
                                                        airport_data[["IATA Code", "Latitude Decimal Degrees", "Longitude Decimal Degrees"]],
                                                        left_on="from_airport_code",
                                                        right_on="IATA Code",
                                                        how="left"
                                                        )
    
    flights_with_source_and_destination_df = pd.merge(flights_with_source_and_destination_df,
                                                        airport_data[["IATA Code", "Latitude Decimal Degrees", "Longitude Decimal Degrees"]],
                                                        left_on="dest_airport_code",
                                                        right_on="IATA Code",
                                                        how="left",
                                                        suffixes=(" Source", " Destination")
                                                        )
    
    
    # Create scattermapbox plot
    fig = go.Figure()

    # Add airport markers
    fig.add_trace(go.Scattermapbox(
        lat=airport_data["Latitude Decimal Degrees"],
        lon=airport_data["Longitude Decimal Degrees"],
        mode="markers",
        marker=go.scattermapbox.Marker(
            size=5,
            color="black"
        ),
        text=airport_data["IATA Code"]
    ))

    # Add flight lines
    for i in range(len(flights_with_source_and_destination_df)):
        # sampling as currently takes quite a while to add all lines
        if i % 10000 == 0:
            fig.add_trace(
                go.Scattermapbox(
                    mode='lines',
                    lat=[flights_with_source_and_destination_df["Latitude Decimal Degrees Source"][i], flights_with_source_and_destination_df["Latitude Decimal Degrees Destination"][i]],
                    lon=[flights_with_source_and_destination_df["Longitude Decimal Degrees Source"][i], flights_with_source_and_destination_df[ "Longitude Decimal Degrees Destination"][i]],
                    line=go.scattermapbox.Line(
                        width=1,
                        color="red"
                    ),
                    name=str(flights_with_source_and_destination_df["flight_number"][i])
                )
            )

    # Set layout
    fig.update_layout(
        mapbox_style="open-street-map",
    )

    # Show plot
    plotly.offline.plot(fig)
