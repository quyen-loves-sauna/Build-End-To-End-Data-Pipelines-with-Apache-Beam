from airflow import models
from datetime import datetime, timedelta
from airflow.contrib.operators.dataflow_operator import DataFlowPythonOperator

default_args = {
    'owner' : 'Airflow',
    'start_date' : datetime(2024, 0o5, 13),
    'retries' : 1,
     'retry_delay' : timedelta(seconds=50),
     'dataflow_default_options': {
         'project' : 'southern-flash-422709-m3',
         'region' : 'us-central1',
         'runner' : 'DataFlowRunner'
     }
}

with models.DAG('food_orders_dag', default_args=default_args,
                schedule_interval = '@daily',
                catchup=False
                ) as dag:
    t1 = DataFlowPythonOperator(task_id='beamtask',
                                py_file='gs://us-central1-demo-1fdf8dab-bucket/code_written_python_3.py',
                                options={'input' : 'gs://daily_food_orders_python_to_bq/subfolder/food_daily.csv'})

