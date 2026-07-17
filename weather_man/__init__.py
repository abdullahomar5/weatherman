# weather_man/__init__.py

# Expose public functions from utils module
from .utils import (
    MONTH_NAMES,
    MONTH_ABBRS,
    format_temp,
    format_date,
    parse_weather_file,
    get_city_dir,
    get_available_years
)

# Expose public functions from aggregator module
from .aggregator import (
    process_yearly_extremes,
    process_monthly_averages,
    process_monthly_charts
)
