# TRT Intermodal Live Truck-to-Rail Conversion App

This Streamlit app flags truck lanes that may be attractive for rail/intermodal conversion.

## Files

- `app.py` — main Streamlit application
- `requirements.txt` — Python packages needed by Streamlit Cloud

## Deploy on Streamlit Cloud

1. Upload both files to your GitHub repository.
2. Go to Streamlit Cloud.
3. Create a new app from your repo.
4. Set the main file path to:

```txt
app.py
```

## Live Data Setup

The app currently supports:

1. Demo live-ready data
2. CSV upload
3. DAT-ready mode
4. SONAR-ready mode

To add API keys in Streamlit Cloud:

```toml
DAT_API_KEY = "your_dat_key_here"
SONAR_API_KEY = "your_sonar_key_here"
```

## CSV Format

Required columns:

- Origin
- Destination
- Truck Rate
- Rail Rate

Optional columns:

- Truck Miles
- Truck Transit Days
- Rail Transit Days

## Next Upgrade

The next step is to replace the placeholder functions:

- `dat_truck_manual_rail_data()`
- `sonar_truck_rail_data()`

with the exact API endpoint and payload from your DAT or SONAR subscription.
