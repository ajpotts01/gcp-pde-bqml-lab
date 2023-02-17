create or replace model
  {{ params.target_model_name_wd }}
options
  (input_label_cols=['duration'],
    model_type='linear_reg') AS
select
  duration,
  start_station_name,
if(
    extract(dayofweek from start_date) between 2 and 6,
    'weekday',
    'weekend'
  ) as day_of_week,
  cast(
    extract(hour from start_date) 
    as string
  ) as hour_of_day
from
  `bigquery-public-data`.london_bicycles.cycle_hire