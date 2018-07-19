from datetime import datetime, timedelta
from airflow.models import DAG  # Import the DAG class
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.sensors import TimeDeltaSensor

yesterday = datetime.combine(
        datetime.today() - timedelta(1), datetime.min.time())

default_args = {
    'owner': 'you',
    'depends_on_past': False,
    'start_date': yesterday,
    # You want an owner and possibly a team alias
    'email': ['monna.lisa.smile0210@gmail.com', 'monna_lisa_smile0210@yahoo.co.jp'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'pool': 'default',
}

dag = DAG(
    dag_id='share_price_data',
    description="This describes data pipeline on google cloud",
    default_args=default_args,
    schedule_interval=timedelta(days=1)) 

scrayping_af = BashOperator(task_id='scrapying_ds',
	bash_command='python ./manage_work.py',
    dag=dag)



transform_af = BashOperator(task_id='transform_ds',
	bash_command='python ./transform.py',
    dag=dag)

upload_af = BashOperator(task_id='upload_ds',
	bash_command='python ./upload.py',
    dag=dag)


transform_af.set_upstream(scrayping_af)
upload_af.set_upstream(transform_af)
