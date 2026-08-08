import pandas as pd
import snowflake.connector
from dotenv import load_dotenv
import os

# 1. Load credentials from .env
load_dotenv()

# 2. Read the Parquet file
print("Reading data file...")
df = pd.read_parquet("data/yellow_tripdata_2026-05.parquet")
print(f"Rows loaded: {len(df)}")

# 3. Clean the data
print("Cleaning data...")
df.columns = [col.lower().strip().replace(" ", "_") for col in df.columns]

df = df.rename(columns={
    "tpep_pickup_datetime": "pickup_datetime",
    "tpep_dropoff_datetime": "dropoff_datetime",
    "vendorid": "vendor_id",
    "ratecodeid": "ratecode_id",
    "pulocationid": "pu_location_id",
    "dolocationid": "do_location_id"
})

df = df.dropna(subset=["pickup_datetime", "dropoff_datetime", "total_amount"])
df = df[df["trip_distance"] > 0]
df = df[df["total_amount"] > 0]
df = df[df["passenger_count"] > 0]

columns_to_keep = [
    "vendor_id", "pickup_datetime", "dropoff_datetime",
    "passenger_count", "trip_distance", "ratecode_id",
    "store_and_fwd_flag", "pu_location_id", "do_location_id",
    "payment_type", "fare_amount", "extra", "mta_tax",
    "tip_amount", "tolls_amount", "improvement_surcharge",
    "total_amount", "congestion_surcharge", "airport_fee"
]
df = df[columns_to_keep]
print(f"Rows after cleaning: {len(df)}")
df["pickup_datetime"] = df["pickup_datetime"].astype(str)
df["dropoff_datetime"] = df["dropoff_datetime"].astype(str)

# 4. Connect to Snowflake
print("Connecting to Snowflake...")
conn = snowflake.connector.connect(
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database=os.getenv("SNOWFLAKE_DATABASE"),
    schema=os.getenv("SNOWFLAKE_SCHEMA")
)
cursor = conn.cursor()

# 5. Load data into Snowflake in batches
print("Loading data into Snowflake...")
batch_size = 10000
total_rows = len(df)
batches = (total_rows // batch_size) + 1

for i in range(batches):
    batch = df.iloc[i * batch_size : (i + 1) * batch_size]
    if batch.empty:
        continue
    rows = [tuple(row) for row in batch.itertuples(index=False, name=None)]
    cursor.executemany(
        """
        INSERT INTO TAXI_PROJECT.RAW.RAW_TAXI_TRIPS (
            vendor_id, pickup_datetime, dropoff_datetime,
            passenger_count, trip_distance, ratecode_id,
            store_and_fwd_flag, pu_location_id, do_location_id,
            payment_type, fare_amount, extra, mta_tax,
            tip_amount, tolls_amount, improvement_surcharge,
            total_amount, congestion_surcharge, airport_fee
        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """,
        rows
    )
    print(f"  Inserted batch {i+1}/{batches} ({len(rows)} rows)")

# 6. Confirm and close
cursor.execute("SELECT COUNT(*) FROM TAXI_PROJECT.RAW.RAW_TAXI_TRIPS")
count = cursor.fetchone()[0]
print(f"✅ Done! Total rows in Snowflake: {count}")

cursor.close()
conn.close()