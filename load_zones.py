import pandas as pd
import snowflake.connector
from dotenv import load_dotenv
import os

load_dotenv()

print("Reading zone lookup file...")
df = pd.read_csv("data/taxi_zone_lookup.csv")
df.columns = [col.lower().strip() for col in df.columns]
df = df.where(pd.notnull(df), None)

conn = snowflake.connector.connect(
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database=os.getenv("SNOWFLAKE_DATABASE"),
    schema=os.getenv("SNOWFLAKE_SCHEMA")
)
cursor = conn.cursor()

cursor.execute("""
    CREATE OR REPLACE TABLE TAXI_PROJECT.RAW.TAXI_ZONE_LOOKUP (
        locationid NUMBER,
        borough VARCHAR,
        zone VARCHAR,
        service_zone VARCHAR
    )
""")

rows = [tuple(row) for row in df.itertuples(index=False, name=None)]
cursor.executemany(
    "INSERT INTO TAXI_PROJECT.RAW.TAXI_ZONE_LOOKUP (locationid, borough, zone, service_zone) VALUES (%s,%s,%s,%s)",
    rows
)

cursor.execute("SELECT COUNT(*) FROM TAXI_PROJECT.RAW.TAXI_ZONE_LOOKUP")
print(f"✅ Loaded {cursor.fetchone()[0]} zones")

cursor.close()
conn.close()