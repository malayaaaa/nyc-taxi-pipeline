select *
from {{ ref('fct_trips') }}
where fare_amount < 0
   or (fare_amount > 500 and trip_distance < 5)