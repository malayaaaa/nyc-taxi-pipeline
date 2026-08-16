with trips as (
    select * from {{ ref('fct_trips') }}
),

hourly as (
    select
        dayname(pickup_datetime) as day_of_week,
        hour(pickup_datetime) as hour_of_day,
        cast(pickup_datetime as date) as trip_date,
        count(*) as trip_count
    from trips
    group by day_of_week, hour_of_day, trip_date
),

day_counts as (
    select
        day_of_week,
        count(distinct trip_date) as num_days
    from hourly
    group by day_of_week
),

aggregated as (
    select
        hourly.day_of_week,
        hourly.hour_of_day,
        sum(hourly.trip_count) as total_trips,
        day_counts.num_days,
        round(sum(hourly.trip_count) / day_counts.num_days, 0) as avg_trips
    from hourly
    left join day_counts
        on hourly.day_of_week = day_counts.day_of_week
    group by hourly.day_of_week, hourly.hour_of_day, day_counts.num_days
)

select
    day_of_week,
    case day_of_week
        when 'Mon' then 1
        when 'Tue' then 2
        when 'Wed' then 3
        when 'Thu' then 4
        when 'Fri' then 5
        when 'Sat' then 6
        when 'Sun' then 7
    end as day_order,
    hour_of_day,
    case
        when hour_of_day = 0 then '12 AM'
        when hour_of_day < 12 then hour_of_day || ' AM'
        when hour_of_day = 12 then '12 PM'
        else (hour_of_day - 12) || ' PM'
    end as hour_label,
    avg_trips as trip_count,
    total_trips,
    num_days
from aggregated
order by day_order, hour_of_day