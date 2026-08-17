# NYC Taxi Trip Data Pipeline

An end-to-end data engineering pipeline that ingests, transforms, and visualizes NYC Yellow Taxi trip data using Python, Snowflake, and dbt.

## What this project does

- Ingests ~3 million raw taxi trip records (May 2026) from NYC TLC's public dataset into Snowflake
- Cleans and transforms the data using dbt into staging, fact, and aggregate models
- Joins trip data with NYC taxi zone lookup data to analyze fares by borough
- Visualizes key metrics in Looker Studio: daily trip volume, average fare by borough, and peak hours by day/hour

## Architecture
![Architecture Diagram](screenshots/architecture_diagram.png)

## Tools used

- **Python** — data extraction and loading (pandas, snowflake-connector-python)
- **Snowflake** — cloud data warehouse
- **dbt** — data transformation and testing
- **Looker Studio** — dashboard visualization
- **Git/GitHub** — version control

## Project structure
taxi/
├── data/ # raw data files (gitignored)
├── screenshots/ # dashboard chart images
├── ingest.py # loads taxi trip data into Snowflake
├── load_zones.py # loads taxi zone lookup into Snowflake
└── taxi_project/ # dbt project
└── models/
├── staging/
│ ├── stg_taxi_trips.sql
│ └── stg_taxi_zones.sql
└── marts/
├── fct_trips.sql
├── agg_daily_summary.sql
├── agg_fare_by_borough.sql
└── agg_peak_hours.sql

## How to run this

1. Clone this repo
2. Create a `.env` file with your Snowflake credentials (see `.env.example`)
3. Install dependencies: `pip install pandas pyarrow snowflake-connector-python python-dotenv dbt-snowflake`
4. Run `python3 ingest.py` and `python3 load_zones.py` to load raw data
5. `cd taxi_project` and run `dbt run` to build all models
6. Run `dbt test` to validate data quality (7/7 tests passing)

## Dashboard

View the live interactive dashboard [here](https://datastudio.google.com/reporting/383e095f-d720-4357-ad55-37f3dd818c55).

## Visualizations

### Daily Trip Volume
![Daily Trip Volume](screenshots/daily_trip_volume.png)

### Average Fare by Borough
![Average Fare by Borough](screenshots/fare_by_borough.png)

### Peak Hours Heatmap
![Peak Hours Heatmap](screenshots/peak_hours_heatmap.png)

## Key insights

- Weekend early mornings (12–2 AM) see significantly higher trip volume than weekday mornings
- EWR (Newark Airport) trips have the highest average fare, as expected for long-distance airport runs
- Weekday evening rush hours (5–9 PM) show consistent peak demand