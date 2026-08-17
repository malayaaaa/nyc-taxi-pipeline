with trips as (
    select * from {{ ref('fct_trips') }}
)

select
    cast(pickup_datetime as date) as trip_date,
    day(cast(pickup_datetime as date)) as day_of_month,
    count(*) as trip_count,
    round(avg(fare_amount), 2) as avg_fare,
    round(avg(trip_distance), 2) as avg_distance,
    round(avg(trip_duration_minutes), 2) as avg_duration_minutes,
    round(avg(cost_per_mile), 2) as avg_cost_per_mile
from trips
group by trip_date
order by trip_date