# weather_man/utils.py
import os

# Lists of full month names and 3-letter abbreviations
MONTH_NAMES = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

MONTH_ABBRS = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
]

# Formats temperature value. Single digit positive numbers get a leading zero.
def format_temp(temp):
    if temp is None:
        return "N/A"
    return f"{temp:02d}C" if 0 <= temp < 10 else f"{temp}C"

# Converts a computer date format (YYYY-MM-DD) into a human readable format (Month Day)
def format_date(date_str):
    if not date_str:
        return "N/A"
    parts = date_str.split('-')
    if len(parts) == 3:
        try:
            month_idx = int(parts[1]) - 1
            day = int(parts[2])
            if 0 <= month_idx < 12:
                return f"{MONTH_NAMES[month_idx]} {day}"
        except ValueError:
            pass
    return date_str

# Reads and parses a weather data file into a list of day dictionaries
def parse_weather_file(filepath):
    rows = []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('<!--') or line.startswith('#'):
                    continue
                parts = [p.strip() for p in line.split(',')]
                if not parts or parts[0] in ("PKT", "GST", "MST") or len(parts) < 9:
                    continue
                if parts[0].count('-') != 2:
                    continue
                try:
                    rows.append({
                        'date': parts[0],
                        'max_temp': int(parts[1]) if parts[1] else None,
                        'min_temp': int(parts[3]) if parts[3] else None,
                        'max_humid': int(parts[7]) if parts[7] else None,
                        'mean_humid': int(parts[8]) if parts[8] else None
                    })
                except ValueError:
                    pass
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
    return rows

# Looks up a matching city folder path based on case-insensitive input
def get_city_dir(city_name):
    if os.path.isdir(city_name):
        return os.path.abspath(city_name)
    
    for item in os.listdir('.'):
        if os.path.isdir(item) and city_name.lower() in item.lower():
            return os.path.abspath(item)
    return None

# Extracts all unique years of data available inside a directory
def get_available_years(city_dir):
    years = set()
    for f in os.listdir(city_dir):
        if f.lower().endswith('.txt'):
            parts = f.replace('.', '_').split('_')
            for p in parts:
                if p.isdigit() and len(p) == 4:
                    years.add(int(p))
    return sorted(list(years))
