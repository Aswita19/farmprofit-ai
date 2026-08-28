import pandas as pd


REQUIRED_COLUMNS = [
    "timestamp",
    "soil_moisture",
    "air_temperature",
    "humidity",
    "water_used"
]


def load_sensor_data(uploaded_file):
    df = pd.read_csv(uploaded_file)

    missing = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing required columns: {', '.join(missing)}"
        )

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    return df.sort_values("timestamp")


def sensor_summary(df):
    return {
        "avg_soil_moisture": df["soil_moisture"].mean(),
        "avg_temperature": df["air_temperature"].mean(),
        "avg_humidity": df["humidity"].mean(),
        "total_water_used": df["water_used"].sum(),
        "latest_soil_moisture": df["soil_moisture"].iloc[-1],
    }

