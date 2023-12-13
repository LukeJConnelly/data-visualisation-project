from turtle import bgcolor
from dash import dcc
import plotly.express as px
from utils.settings import get_colours, default_chart_height, get_neutral_colour, default_bg_color, neutral_colour_hover, get_colours_hover

from utils.airport_country_mapping import get_flight_df_with_country
from utils.time import convert_duration_to_hours
import plotly.express as px

def get_bar_chart(flight_data):
    return dcc.Graph(
            id='bar-chart',
            figure=px.bar(flight_data, x="from_airport_code", color="dest_airport_code", barmode="group")
        )

def get_histogram_price(flight_data):
    margin = 0 * (flight_data['price'].max() - flight_data['price'].min())
    return dcc.Graph(
            id='price-hist',
            figure=px.histogram(flight_data['price'], x="price", title="Ticket Price (USD)", nbins=20)
                     .update_layout(
                         dragmode="select",
                         selectdirection="h",
                         xaxis={"fixedrange": True},
                         yaxis={"fixedrange": True,},
                         yaxis_title=None,
                         xaxis_title=None,
                         title=dict(font=dict(size=15, color="black"), automargin=True, x=0.5),
                         title_font_family="Segoe UI Semibold",
                         hoverlabel=dict(font_family="Segoe UI", bgcolor=neutral_colour_hover),
                         font_family="Segoe UI",
                         plot_bgcolor=default_bg_color,
                         bargap=0,
                         hovermode="x",
                         margin=dict(t=0, b=0, l=0, r=0))
                     .update_traces(marker_color=get_neutral_colour(), hovertemplate="$%{x}<br>%{y} flights")
                     .update_xaxes(range=[flight_data['price'].min() - margin, flight_data['price'].max() + margin]),
            config={"modeBarButtonsToRemove": ["zoomIn2d", "zoomOut2d", "pan2d", "zoom2d", "autoScale2d", "resetScale2d","lasso2d"],
                                "displaylogo": False,},
            style={"height": default_chart_height}
        )


def get_histogram_co2(flight_data):
    margin = 0 * (flight_data['co2_emissions'].max() - flight_data['co2_emissions'].min())
    return dcc.Graph(
            id='co2-hist',
            figure=px.histogram(flight_data, x="co2_emissions", title="CO2 Emissions", nbins=12)
                     .update_layout(
                         dragmode="select",
                         selectdirection="h",
                         xaxis={"fixedrange": True},
                         yaxis={"fixedrange": True, },
                         yaxis_title=None,
                         xaxis_title=None,
                         title=dict(font=dict(size=15, color="black"), automargin=True, x=0.5),
                         title_font_family="Segoe UI Semibold",
                         hoverlabel=dict(font_family="Segoe UI", bgcolor=neutral_colour_hover),
                         font_family="Segoe UI",
                         plot_bgcolor=default_bg_color,
                         bargap=0,
                         hovermode="x",
                         margin=dict(t=0, b=0, l=0, r=0))
                     .update_traces(marker_color=get_neutral_colour(), hovertemplate="%{x}<br>%{y} flights")
                     .update_xaxes(range=[flight_data['co2_emissions'].min() - margin, flight_data['co2_emissions'].max() + margin]),
            config={"modeBarButtonsToRemove": ["zoomIn2d", "zoomOut2d", "pan2d", "zoom2d", "autoScale2d", "resetScale2d","lasso2d"],
                                "displaylogo": False,},
            style={"height": default_chart_height}
    )

def get_histogram_duration(flight_data):
    flight_data["duration_minutes"] = flight_data["duration"].apply(convert_duration_to_hours)
    margin = 0 * (flight_data['duration_minutes'].max() - flight_data['duration_minutes'].min())
    
    return dcc.Graph(
            id='duration-hist',
            figure=px.histogram(flight_data, x="duration_minutes", title="Flight Duration (minutes)", nbins=20)
                     .update_layout(
                         dragmode="select",
                         selectdirection="h",
                         xaxis={"fixedrange": True},
                         yaxis={"fixedrange": True,},
                         yaxis_title=None,
                         xaxis_title=None,
                         title=dict(font=dict(size=15, color="black"), automargin=True, x=0.5),
                         title_font_family="Segoe UI Semibold",
                         hoverlabel=dict(font_family="Segoe UI", bgcolor=neutral_colour_hover),
                         font_family="Segoe UI",
                         plot_bgcolor=default_bg_color,
                         bargap=0,
                         hovermode="x",
                         margin=dict(t=0, b=0, l=0, r=0))
                     .update_traces(marker_color=get_neutral_colour(), hovertemplate="%{x}m<br>%{y} flights")
                     .update_xaxes(range=[flight_data['duration_minutes'].min() - margin, flight_data['duration_minutes'].max() + margin]),
            config={"modeBarButtonsToRemove": ["zoomIn2d", "zoomOut2d", "pan2d", "zoom2d", "autoScale2d", "resetScale2d","lasso2d"],
                                "displaylogo": False,},
            style={"height": default_chart_height}
        )
        

def get_histogram_country(flight_df, airport_data, colour_tuple, is_from=True):
    """
    colour_tuple is (to_colour, from_colour)
    """
    vals = flight_df["from_country" if is_from else "dest_country"].value_counts().index.tolist()
    return dcc.Graph(
            id='country-hist'+ ("-from" if is_from else "-to"),
            figure=px.histogram(flight_df, x="from_country" if is_from else "dest_country", title=f'{"Arrival" if not is_from else "Departure"} Countries')
                     .update_layout(
                        dragmode="pan",
                        xaxis={'categoryorder': 'total descending', 'range': [-0.5, 10.5 if len(vals) >= 10 else len(vals) - 0.5], 
                                'tickvals': list(range(len(vals))),
                                'ticktext': [(x) if len(str(x)) < 10 else str(x)[:8] + '...' for x in vals]},
                        yaxis={"fixedrange": True,},           
                        yaxis_title=None,
                        xaxis_title=None,
                        title=dict(font=dict(size=15, color="black"), automargin=True, x=0.5),
                        title_font_family="Segoe UI Semibold",
                        hoverlabel=dict(font_family="Segoe UI", bgcolor=get_colours_hover()[is_from]),
                        font_family="Segoe UI",
                        hovermode="x",
                        plot_bgcolor=default_bg_color,
                        margin=dict(t=0, b=0, l=0, r=0))
                     .update_traces(
                      marker={"color": colour_tuple[is_from]},
                      customdata=vals, 
                      hovertemplate="%{customdata}<br>%{y} flights",
                     ),
            config={"modeBarButtonsToRemove": ["zoomIn2d", "zoomOut2d", "pan2d", "zoom2d", "autoScale2d", "resetScale2d","lasso2d", "select2d"],
                                "displaylogo": False,},
            style={"height": default_chart_height}
        )

def get_histogram_airline(flight_data):
    # Flattening the airline_name column if it contains lists
    flat_airline_data = flight_data.explode('airline_name')
    vals = flat_airline_data['airline_name'].value_counts().index.tolist()
    fig = px.histogram(flat_airline_data, x="airline_name", title="Airlines")
    fig.update_layout(
        xaxis={'categoryorder': 'total descending', 'range': [-0.5, 10.5 if len(vals) >= 10 else len(vals) + 0.5], 
               'tickvals': list(range(len(vals))),
               'ticktext': [(x) if len(str(x)) < 10 else str(x)[:8] + '...' for x in vals]},
        yaxis={"fixedrange": True,},
        dragmode="pan",
        yaxis_title=None,
        xaxis_title=None,
        title=dict(font=dict(size=15, color="black"), automargin=True, x=0.5),
        title_font_family="Segoe UI Semibold",
        hoverlabel=dict(font_family="Segoe UI", bgcolor=neutral_colour_hover),
        font_family="Segoe UI",
        hovermode="x",
        plot_bgcolor=default_bg_color,
        margin=dict(t=0, b=0, l=0, r=0)
    )
    fig.update_traces(marker_color=get_neutral_colour(), 
                      customdata=vals, 
                      hovertemplate="%{customdata}<br>%{y} flights")

    return dcc.Graph(
        id='airline-hist',
        figure=fig,
        config={"modeBarButtonsToRemove": ["zoomIn2d", "zoomOut2d", "pan2d", "zoom2d", "autoScale2d", "resetScale2d","lasso2d", "select2d"],
                                "displaylogo": False,},
        style={"height": default_chart_height}
    )