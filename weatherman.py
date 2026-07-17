#!/usr/bin/env python3
import sys
import os
import weather_man

# Prompts the user interactively and outputs weather reports
def run_interactive():
    print("=== Weather Man Interactive Terminal ===")
    
    # 1. Ask for city name and validate it
    while True:
        city = input("Enter city name (e.g., lahore, dubai, murree): ").strip()
        city_dir = weather_man.get_city_dir(city)
        if city_dir:
            break
        print(f"Error: Could not find directory matching '{city}' in the current folder.")

    # Get available years for this city
    years = weather_man.get_available_years(city_dir)
    if not years:
        print("Error: No weather data files found in this directory.")
        return
    min_year, max_year = years[0], years[-1]
    print(f"Available data years for this city: {min_year}-{max_year}")

    # 2. Ask for year and check if we have data for it
    while True:
        year_input = input(f"Enter year ({min_year}-{max_year}): ").strip()
        if not (year_input.isdigit() and len(year_input) == 4):
            print("Error: Enter a valid 4-digit year.")
            continue
        
        # Verify the year is within available years list
        year_val = int(year_input)
        if year_val < min_year or year_val > max_year or year_val not in years:
            print("Error: No data added at that time.")
            continue  # Loop back without prompting for month
        
        year = year_input
        break

    # 3. Ask for month and validate it (1 to 12)
    while True:
        month = input("Enter month (1-12): ").strip()
        if month.isdigit() and 1 <= int(month) <= 12:
            month_num = int(month)
            break
        print("Error: Enter a valid month number (1-12).")

    # 4. Ask which report selection the user wants to see
    print("\nSelect Report Option:")
    print("  1. All Reports (Extremes, Averages, and Charts)")
    print("  2. Yearly Extremes only (-e)")
    print("  3. Monthly Averages only (-a)")
    print("  4. Monthly Bar Charts only (-c)")
    while True:
        choice = input("Enter choice (1-4, default 1): ").strip() or "1"
        if choice in ("1", "2", "3", "4"):
            break
        print("Error: Enter a number from 1 to 4.")

    # Print the report banner header
    print("\n" + "=" * 50)
    city_display = os.path.basename(city_dir).replace('_weather', '').capitalize()
    print(f"WEATHER REPORT FOR: {city_display}")
    print(f"YEAR: {year} | MONTH: {weather_man.MONTH_NAMES[month_num - 1]}")
    print("=" * 50 + "\n")

    # Process and show output based on selection choice
    if choice in ("1", "2"):
        print("--- Yearly Extremes ---")
        weather_man.process_yearly_extremes(year, city_dir)
        print()
    if choice in ("1", "3"):
        print("--- Monthly Averages ---")
        weather_man.process_monthly_averages(year, month_num, city_dir)
        print()
    if choice in ("1", "4"):
        print("--- Monthly Bar Charts ---")
        weather_man.process_monthly_charts(year, month_num, city_dir)
        print()

# CLI and main launcher
def main():
    # If run with no parameters, start interactive mode
    if len(sys.argv) < 2:
        run_interactive()
        sys.exit(0)

    # CLI Command validation check
    if len(sys.argv) < 4:
        print("Usage (CLI Mode): python weatherman.py [option] [date_parameter] [files_directory]")
        print("Options:")
        print("  -e [year]        For a given year display the highest temp, lowest temp, and most humid day.")
        print("  -a [year/month]  For a given month display the average highest temp, average lowest temp, and average humidity.")
        print("  -c [year/month]  For a given month draw horizontal bar charts on the console.")
        sys.exit(1)

    option, date_param, files_dir = sys.argv[1], sys.argv[2], sys.argv[3]

    # Handle yearly extremes CLI option
    if option == '-e':
        weather_man.process_yearly_extremes(date_param, files_dir)
    # Handle monthly averages and monthly charts CLI options
    elif option in ('-a', '-c'):
        try:
            year, month = date_param.split('/')
            month_num = int(month)
        except ValueError:
            print("Error: Invalid date parameter. Expected format YYYY/MM.")
            sys.exit(1)

        if option == '-a':
            weather_man.process_monthly_averages(year, month_num, files_dir)
        else:
            weather_man.process_monthly_charts(year, month_num, files_dir)
    else:
        print(f"Error: Invalid option '{option}'. Must be one of -e, -a, or -c.")
        sys.exit(1)

if __name__ == '__main__':
    main()
