from airflow import DAG
from datetime import datetime, timedelta
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.operators.dummy_operator import DummyOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.utcnow(),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=3)
}

dag = DAG(
    'sample_k', default_args=default_args, schedule_interval=timedelta(minutes=6))

start = DummyOperator(task_id='task-0', dag=dag)

passing = KubernetesPodOperator(namespace='airflow',
                          image="python:3.9-alpine3.12",
                          cmds=["python","-c"],
                          arguments=["print('hello, python:3.9-alpine3.12')"],
                          labels={"foo": "bar"},
                          task_id="task-1",
                          get_logs=True,
                          dag=dag
                          )

failing = KubernetesPodOperator(namespace='airflow',
                          image="python:3.8.6-alpine3.12",
                          cmds=["python","-c"],
                          arguments=["print('hello, python:3.8.6-alpine3.12')"],
                          labels={"foo": "bar"},
                          task_id="task-2",
                          get_logs=True,
                          dag=dag
                          )

passing.set_upstream(start)
failing.set_upstream(start)