# Weather Man Python Project

A modular Python command-line utility and interactive terminal wizard that parses historical weather logs to compile statistics, averages, and console-based temperature charts.

This project replaces the Ruby implementation described in the original assignment, adhering to clean and readable Python standard library concepts (such as file I/O, loops, list comprehensions, and dictionaries).

---

## Directory Structure

The codebase is organized as a modular Python package:

```text
/
├── weatherman.py             # Main entry script (interactive UI and CLI argument router)
├── README.md                 # Project documentation
└── weather_man/              # Python Package
    ├── __init__.py           # Package initializer (defines public package APIs)
    ├── utils.py              # Helper utility module (parsing, formatting, folder lookups)
    └── aggregator.py         # Calculation module (extremes, averages, and charts reports)
```

---

## Features

1. **Interactive Mode**: Running the script without arguments launches a terminal wizard that guides you through selecting a city, year, and month.
2. **Dynamic Year Limits**: The script automatically scans the chosen city's folder, detects the range of available years, and warns the user if they input an unavailable year (`Error: No data added at that time.`).
3. **ANSI Colored Bar Charts**: Prints horizontal plus sign (`+`) temperature charts in the terminal (Red for Daily Highs, Blue for Daily Lows).
4. **Dynamic Column Parsing**: Adapts to different column header names (like `PKT` or `GST`) seamlessly.
5. **No External Dependencies**: Built entirely using the Python standard library (no `pandas` or `csv` packages needed).

---

## How to Run

Open your terminal in the project directory and execute:

### 1. Interactive Mode
```bash
python3 weatherman.py
```
This launches the step-by-step menu.

### 2. Command Line Interface (CLI) Mode

#### Yearly Extremes (`-e`)
Finds the highest temperature, lowest temperature, and most humid day for the specified year:
```bash
python3 weatherman.py -e 2002 lahore_weather
```

#### Monthly Averages (`-a`)
Calculates average high temperature, average low temperature, and average humidity for the specified month:
```bash
python3 weatherman.py -a 2005/6 lahore_weather
```

#### Monthly Bar Charts (`-c`)
Draws high and low daily temperature bar charts in color:
```bash
python3 weatherman.py -c 2011/3 Murree_weather
```
