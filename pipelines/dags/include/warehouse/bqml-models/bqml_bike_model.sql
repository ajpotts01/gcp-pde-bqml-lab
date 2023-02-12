create or replace model
    {{ params.target_model_name }}
options
    (input_label_cols=['duration'],
     model_type='linear_reg') as
select
    duration,
    start_station_name,
    cast(extract(dayofweek from start_date) as string) as day_of_week,
    cast(extract(hour from start_date) as string) as hour_of_day
from
    `bigquery-public-data.london_bicycles.cycle_hire`
