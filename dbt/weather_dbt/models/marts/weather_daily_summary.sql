{{ config(materialized='table') }}

select
id,
observation_date,
max_temperature - min_temperature as daily_temperature_fluctuation,
max_temperature - lag(max_temperature) over (order by observation_date) as temp_change_vs_yesterday
from {{ ref('stg_weather') }}
order by observation_date