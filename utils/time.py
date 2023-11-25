from datetime import datetime, timedelta
import pandas as pd

def get_date_time_options(time_data):
    unique_dates = sorted(time_data.dt.date.dropna().unique())
    date_options = [{'label': pd.to_datetime(date).strftime('%Y-%m-%d'), 'value': date} for date in unique_dates]
    time_options = generate_time_options(30)

    return date_options, time_options
    
def generate_time_options(interval_minutes=30):
    start_time = datetime(2000, 1, 1, 0, 0)
    end_time = datetime(2000, 1, 2, 0, 0)

    time_options = []
    current_time = start_time
    while current_time < end_time:
        time_str = current_time.strftime('%H:%M')
        time_options.append({'label': time_str, 'value': time_str})
        current_time += timedelta(minutes=interval_minutes)

    return time_options