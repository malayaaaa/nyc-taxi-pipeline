with trips as (
    select * from {{ ref('fct_trips') }}
),

hourly as (
    select
        dayname(pickup_datetime) as day_of_week,
        hour(pickup_datetime) as hour_of_day,
        count(*) as trip_count
    from trips
    group by day_of_week, hour_of_day
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
    trip_count
from hourly
order by day_order, hour_of_day