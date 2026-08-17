with trips as (
    select * from {{ ref('fct_trips') }}
),

zones as (
    select * from {{ ref('stg_taxi_zones') }}
),

joined as (
    select
        zones.borough,
        trips.fare_amount
    from trips
    left join zones
        on trips.pu_location_id = zones.locationid
)

select
    case when borough = 'Unknown' then 'Other' else borough end as borough,
    count(*) as trip_count,
    round(avg(fare_amount), 2) as avg_fare
from joined
where borough is not null
group by case when borough = 'Unknown' then 'Other' else borough end
order by avg_fare desc