from dash import dcc, html
import plotly.graph_objects as go
import pandas as pd

def get_line_chart(df):
    # Ensure 'departure_time' is in the DataFrame
    if 'departure_time' not in df.columns:
        raise ValueError("DataFrame must contain a 'departure_time' column")

    # Dropdown options
    dropdown_options = [{'label': col, 'value': col} for col in ['price', 'stops']]

    # Initial y_column
    initial_y_column = dropdown_options[0]['value']

    # Initial chart
    fig = create_figure(df, initial_y_column)

    layout = html.Div([
        dcc.Dropdown(
            id='y-axis-dropdown',
            options=dropdown_options,
            value=initial_y_column
        ),
        dcc.Graph(
            id='line-chart',
            figure=fig
        )
    ])

    return layout

def create_figure(df, y_column):
    # Convert 'departure_time' to datetime if it's not already
    if not pd.api.types.is_datetime64_any_dtype(df['departure_time']):
        df['departure_time'] = pd.to_datetime(df['departure_time'])

    # Group by day and calculate the mean for each day
    df_daily_mean = df.groupby(df['departure_time'].dt.date)[y_column].mean().reset_index()
    df_daily_mean.columns = ['departure_time', y_column]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_daily_mean['departure_time'], y=df_daily_mean[y_column], mode='lines+markers', name='Line Plot', line=dict(width=2)))

    fig.update_layout(
        title='Line Chart',
        xaxis_title='Departure Time',
        yaxis_title=y_column,
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False)
    )

    return fig

# Example usage in your Dash app:
# app.layout = get_line_chart(flight_data)
