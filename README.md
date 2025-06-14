# F1 Driver Signature Analysis & Performance Dissector

![F1 Driver Analysis](https://img.shields.io/badge/F1-Driver%20Analysis-red)
![Streamlit App](https://img.shields.io/badge/Streamlit-App-blue)
![FastF1](https://img.shields.io/badge/FastF1-Data-green)

A Streamlit web application that analyzes and compares Formula 1 drivers' driving styles using telemetry data.

## Features

- **Session Selection**: Choose any F1 season (2018-2023), Grand Prix, and session type
- **Driver Comparison**: Compare two drivers' telemetry data and driving styles
- **Style Metrics Analysis**: Insights on:
  - Braking aggressiveness
  - Throttle application smoothness
  - Cornering consistency
  - Gear shift frequency
- **Visual Comparisons**: Bar charts and radar plots for style fingerprints
- **Performance Metrics**: Lap time comparisons and key insights

## Installation

1. Clone this repository
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
3. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

## Usage

1. Select a season, Grand Prix, and session type from the sidebar
2. Click "Load Session Data" to fetch telemetry data
3. Select two drivers to compare
4. Click "Analyze Drivers" to generate the comparison

## Data Source

This application uses the [FastF1](https://github.com/theOehrly/Fast-F1) Python package to access official Formula 1 timing data.

## Requirements

- Python 3.8+
- Streamlit
- FastF1
- Pandas
- NumPy
- Plotly

## Screenshots
