with source as (
    select * from TAXI_PROJECT.RAW.RAW_TAXI_TRIPS
),

staged as (
    select
        vendor_id,
        cast(pickup_datetime as timestamp) as pickup_datetime,
        cast(dropoff_datetime as timestamp) as dropoff_datetime,
        passenger_count,
        trip_distance,
        ratecode_id,
        store_and_fwd_flag,
        pu_location_id,
        do_location_id,
        payment_type,
        fare_amount,
        extra,
        mta_tax,
        tip_amount,
        tolls_amount,
        improvement_surcharge,
        total_amount,
        congestion_surcharge,
        airport_fee
    from source
)

select * from staged
where pickup_datetime >= '2020-01-01'
  and pickup_datetime <= current_timestamp()