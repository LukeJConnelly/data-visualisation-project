# Flight Data Visualisation
Project made as part of the Data Visualisation course on Aarhus University by group 26.<br>
Jakob Bjørn Hyldgaard, Luke John Connelly, Sarah Elna Valentin & Mariam Shamsali

The repository contains a webserver visualisation of flights with the purpose of providing an overview of the flight network, and allowing users to explore the data in an interactive way making the user efficiently engage with the data.

## Tools
The visualisation is made in Python with [Plotly](https://plotly.com/) running in a webserver created with [Dash](https://plotly.com/dash/)

## setting up the project 
Before running the project, its dependecies must be installed. This is done by the following command:
```python
pip install -r requirements.txt
```
### Data
The project assumes a folder named ```data``` with a [flights.csv](https://www.kaggle.com/datasets/polartech/flight-data-with-1-million-or-more-records) and a folder named [GlobalAirportDatanase](https://www.partow.net/miscellaneous/airportdatabase/index.html). <br> This will be used in the preprocessing step, which will create the files ```data/clean_flight.csv``` and ```data/clean_airports.csv``` used for the visualisation.

The [Clean Data files](https://drive.google.com/file/d/1z7dSvFJK9tAEoux3Sm_aPuR0wApZ6pSb/view?usp=drive_link) can also be downloaded directly. 
