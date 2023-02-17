create or replace model
    {{ params.target_model_name_bucketed }}
options
    (input_label_cols=['duration'],
     model_type='linear_reg') as
select
    duration,
    start_station_name,
    if(
        extract(dayofweek from start_date) between 2 and 6,
        'weekday',
        'weekend'
    ) as day_of_week,
    ml.bucketize(
        extract(hour from start_date),
        [5, 10, 17]
    ) as hour_of_day
from
    `bigquery-public-data`.london_bicycles.cycle_hire



