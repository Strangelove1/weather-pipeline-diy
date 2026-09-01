Select *
from {{ref('stg_weather')}}
where max_temperature - min_temperature < 0