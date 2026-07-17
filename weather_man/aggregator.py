# weather_man/aggregator.py
import os
from . import utils

# Scans directory and processes extremes for the requested year
def process_yearly_extremes(year, files_dir):
    all_rows = []
    if not os.path.exists(files_dir):
        print(f"Error: Directory '{files_dir}' does not exist.")
        return

    for f in os.listdir(files_dir):
        if f.lower().endswith('.txt') and f'_{year}_' in f:
            all_rows.extend(utils.parse_weather_file(os.path.join(files_dir, f)))

    if not all_rows:
        print(f"No weather files/records found for year {year}.")
        return

    high_temp, low_temp, max_humid = -999, 999, -999
    high_date, low_date, humid_date = "", "", ""

    for r in all_rows:
        if r['max_temp'] is not None and r['max_temp'] > high_temp:
            high_temp, high_date = r['max_temp'], r['date']
        if r['min_temp'] is not None and r['min_temp'] < low_temp:
            low_temp, low_date = r['min_temp'], r['date']
        if r['max_humid'] is not None and r['max_humid'] > max_humid:
            max_humid, humid_date = r['max_humid'], r['date']

    print(f"Highest: {utils.format_temp(high_temp)} on {utils.format_date(high_date)}")
    print(f"Lowest: {utils.format_temp(low_temp)} on {utils.format_date(low_date)}")
    print(f"Humid: {max_humid}% on {utils.format_date(humid_date)}")

# Searches for a file matching the specific year and month number
def find_monthly_file(year, month_num, files_dir):
    if not os.path.exists(files_dir):
        return None
    month_abbr = utils.MONTH_ABBRS[month_num - 1].lower()
    suffix = f"_{year}_{month_abbr}.txt"
    for f in os.listdir(files_dir):
        if f.lower().endswith(suffix):
            return os.path.join(files_dir, f)
    return None

# Processes and displays calculations of monthly averages
def process_monthly_averages(year, month_num, files_dir):
    filepath = find_monthly_file(year, month_num, files_dir)
    if not filepath:
        print(f"No weather files found for {utils.MONTH_NAMES[month_num - 1]} {year}.")
        return

    rows = utils.parse_weather_file(filepath)
    max_temps = [r['max_temp'] for r in rows if r['max_temp'] is not None]
    min_temps = [r['min_temp'] for r in rows if r['min_temp'] is not None]
    mean_humids = [r['mean_humid'] for r in rows if r['mean_humid'] is not None]

    if max_temps:
        print(f"Highest Average: {utils.format_temp(round(sum(max_temps) / len(max_temps)))}")
    if min_temps:
        print(f"Lowest Average: {utils.format_temp(round(sum(min_temps) / len(min_temps)))}")
    if mean_humids:
        print(f"Average Humidity: {round(sum(mean_humids) / len(mean_humids))}%")

# Draws colored daily maximum/minimum horizontal bar charts
def process_monthly_charts(year, month_num, files_dir):
    filepath = find_monthly_file(year, month_num, files_dir)
    if not filepath:
        print(f"No weather files found for {utils.MONTH_NAMES[month_num - 1]} {year}.")
        return

    rows = utils.parse_weather_file(filepath)
    rows.sort(key=lambda r: int(r['date'].split('-')[2]) if r['date'] else 999)

    print(f"{utils.MONTH_NAMES[month_num - 1]} {year}")
    for r in rows:
        try:
            day_num = int(r['date'].split('-')[2])
        except (ValueError, IndexError):
            continue

        if r['max_temp'] is not None:
            red_bar = '+' * max(0, r['max_temp'])
            print(f"{day_num:02d} \033[91m{red_bar}\033[0m {utils.format_temp(r['max_temp'])}")
        if r['min_temp'] is not None:
            blue_bar = '+' * max(0, r['min_temp'])
            print(f"{day_num:02d} \033[94m{blue_bar}\033[0m {utils.format_temp(r['min_temp'])}")
