import datetime
import pendulum

from airflow import DAG
from airflow.models import Variable
from airflow.providers.google.cloud.operators.bigquery import (
    BigQueryExecuteQueryOperator,
)

# DAG steps:
# - Init BQ connections
# - Create model for training

# region Connections/variables

# BigQuery
bq_conn_id = Variable.get("bq_conn_id")
bq_dataset = Variable.get("bq_dataset")
model_name = "model"
model_name_wd = "model_wd"
model_name_bucketed = "model_bucketed"

dag_params = {
    "target_model_name": f"`{bq_dataset}.{model_name}`",
    "target_model_name_wd": f"`{bq_dataset}.{model_name_wd}`",
    "target_model_name_bucketed": f"`{bq_dataset}.{model_name_bucketed}"
}
# endregion Connections/variables

with DAG(
    dag_id="bike_model_training_pipeline",
    schedule_interval="0 6 * * *",
    start_date=pendulum.datetime(2023, 2, 12, tz="UTC"),
    catchup=False,
    dagrun_timeout=datetime.timedelta(minutes=60),
    template_searchpath="/opt/airflow/dags/include",
    params=dag_params,
    tags=["bikes"],
):
    # region Tasks
    bq_create_model_task = BigQueryExecuteQueryOperator(
        task_id="load_model",
        gcp_conn_id=bq_conn_id,
        use_legacy_sql=False,
        sql="warehouse/bqml-models/bqml_bike_model.sql",
    )

    bq_create_model_wd_task = BigQueryExecuteQueryOperator(
        task_id="load_model_wd",
        gcp_conn_id=bq_conn_id,
        use_legacy_sql=False,
        sql="warehouse/bqml-models/bqml_bike_model_wd.sql"
    )

    bq_create_model_bucketed_task = BigQueryExecuteQueryOperator(
        task_id="load_model_bucketed",
        gcp_conn_id=bq_conn_id,
        use_legacy_sql=False,
        sql="warehouse/bqml-models/bqml_bike_model_bucketed.sql"
    )

    # endregion Tasks

    bq_create_model_task >> bq_create_model_wd_task >> bq_create_model_bucketed_task
