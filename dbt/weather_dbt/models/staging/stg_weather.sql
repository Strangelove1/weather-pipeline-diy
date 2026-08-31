select
    id,
    obs_date as observation_date,
    max_temp as max_temperature,
    min_temp as min_temperature,
    precipitation_sum,
    loaded_at
from {{source('raw', 'raw_weather_data')}}