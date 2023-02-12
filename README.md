# Simple ML pipeline using BigQuery and Airflow
Simple BigQuery ML pipeline in Python from the official Google Professional Data Engineer certification material.

These are actually possible to do directly through Qwiklabs/Cloud Skills Boost, but the labs boil down to getting you to just run mostly pre-written code. I'm taking a different approach in reading the lab material, and writing pieces myself. In some cases I've gone as far as writing infrastructure as code with Terraform, but for the most part I'm only writing code that would use GCP components tested on the exam - with their open source equivalents if the managed version is too expensive (e.g. Airflow).

Original lab is [here on Cloud Skills Boost](https://www.cloudskillsboost.google/course_sessions/2358822/labs/344843). The pipeline uses BigQuery ML via SQL, and Apache Airflow 2.5.1.

The `pipelines` folder is broken down into folders for all necessary pipeline components:
- `main`, for all DAG definitions
- `include`, for any supplementary files:
    - `warehouse` for either straight SQL scripts (`warehouse/sql`), or BQML definitions (`warehouse/bqml-models`)
    - `functions` for any Python code used for Python operators.

Steps to run locally:
1. Clone the repo
2. Create and activate a Python virtual environment
3. Run `pip install -r requirements.txt` from the `pipelines` directory
4. Build the custom Airflow image (+ GCP extensions) with `docker build . -t extended_airflow`
5. Create a folder to run a standalone Airflow server (I prefer creating an `airflow` folder under `pipelines`)
6. Copy the `dags` folder to the new `airflow` folder
7. Run Airflow from the `airflow` folder: `docker run -p 8080:8080 -v /$(pwd):/opt/airflow extended_airflow:latest standalone`

Recommended steps to run on GCP:
1. Create BigQuery datasets in EU called `bike_model` and `bike_model_dev`
2. Set up a service account with BigQuery permissions (at least job user) and generate a JSON key
3. Create a Postgres database in GCP and record the address
4. Create a VM (you probably need a large one, at least - micro instances across clouds CAN run Airflow for simple examples, but will generally run out of memory or disk space depending on the Docker image size)
5. Log in to the VM
6. Install Docker and git if needed
7. Clone the repo
8. Create a `.env` file in the `pipelines` folder containing `AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://user:password@address.from.step.1`
9. Run `docker-compose up` from `pipelines` - you should not need to copy any dags anywhere.

Alternatively, use Cloud Composer if you can afford it!

In both local or cloud cases:
1. Configure the following variables in Airflow:
    - `bq_conn_id`: `google_cloud_default`
    - `bq_dataset`: the dataset from GCP step 1 (I like to use `bike_model_dev` locally, and `bike_model` in the cloud)
2. Go to Connections and find `google_cloud_default` - it should already exist
3. Enter the JSON key from GCP step 2