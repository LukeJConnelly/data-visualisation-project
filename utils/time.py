from datetime import datetime, timedelta
import pandas as pd
import re
import datetime

def get_date_time_options(time_data):
    unique_dates = sorted(time_data.dt.date.dropna().unique())
    date_counts = time_data.dt.date.value_counts().reset_index()
    date_counts.columns = ['date', 'count']
    date_options = pd.DataFrame({'label': pd.to_datetime(date_counts['date']).dt.strftime('%Y-%m-%d'),
                                 'value': date_counts['date'],
                                 'count': date_counts['count']})
    time_options = generate_time_options(time_data)

    return date_options, time_options

def generate_time_options(time_data, interval_minutes=60):
    start_time = datetime(2000, 1, 1, 0, 0)
    end_time = datetime(2000, 1, 2, 0, 0)

    time_options = []
    current_time = start_time
    while current_time < end_time:
        rounded_time = current_time.replace(minute=0, second=0, microsecond=0)
        time_str = rounded_time.strftime('%H')
        count = time_data[time_data.dt.hour == rounded_time.hour].count()
        time_options.append({'label': time_str, 'value': time_str, 'count': count})
        current_time += timedelta(minutes=interval_minutes)

    time_df = pd.DataFrame(time_options)
    return time_df

def convert_duration_to_hours(duration_str):
    # Regular expression to extract days, and optionally hours, minutes, and seconds
    regex_pattern = r"(\d+)\s*days(?:\s*(\d+):(\d+):(\d+))?"

    match = re.search(regex_pattern, duration_str)
    if match:
        days = match.group(1)
        hours = match.group(2) if match.group(2) else 0
        minutes = match.group(3) if match.group(3) else 0
        seconds = match.group(4) if match.group(4) else 0
    else:
        print("Pattern not found in the string.")

    return int(days) * 24 * 60 + int(hours) * 60 + int(minutes)
