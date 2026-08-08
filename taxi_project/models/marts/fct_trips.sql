with staging as (
    select * from {{ ref('stg_taxi_trips') }}
),

calculated as (
    select
        vendor_id,
        pickup_datetime,
        dropoff_datetime,
        datediff('minute', pickup_datetime, dropoff_datetime) as trip_duration_minutes,
        passenger_count,
        trip_distance,
        pu_location_id,
        do_location_id,
        payment_type,
        fare_amount,
        total_amount,
        case
            when trip_distance > 0 then round(total_amount / trip_distance, 2)
            else null
        end as cost_per_mile
    from staging
)

select * from calculated
where trip_duration_minutes >= 0