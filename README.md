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

-This application uses the [FastF1](https://github.com/theOehrly/Fast-F1) Python package to access official Formula 1 timing data.
-For Documentation:[FastF1].(https://docs.fastf1.dev/)

## Requirements

- Python 3.8+
- Streamlit
- FastF1
- Pandas
- NumPy
- Plotly

## Screenshots
![Screenshot 2025-06-14 195038](https://github.com/user-attachments/assets/b4370cea-e0e7-495c-98e2-f5c8395ae8e5)
![Screenshot 2025-06-14 195104](https://github.com/user-attachments/assets/e09267f6-ed8c-4dc8-9791-8cadd3511c23)
![Screenshot 2025-06-14 195356](https://github.com/user-attachments/assets/b68bd5ec-c9da-4f9e-8e83-4d2e2e41f9ed)
![Screenshot 2025-06-14 195429](https://github.com/user-attachments/assets/5e4439db-6193-4aaa-8511-8c0236dcb69a)
![Screenshot 2025-06-14 195417](https://github.com/user-attachments/assets/4e208be6-b7d8-490c-8c33-9bdff377b785)
![Screenshot 2025-06-14 195442](https://github.com/user-attachments/assets/749e0627-2a8a-4174-b037-ba89bee0f269)





