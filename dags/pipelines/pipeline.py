from datetime import datetime, timedelta

from airflow import DAG

from common.tasks import python_operator
from common.task_utils import MOSCOW_TZ

default_args = {
    'owner': 'Mark Sherman',
    'email': ['marshann2012@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    "text_annotation",
    default_args=default_args,
    schedule=timedelta(days=1),
    start_date=datetime(2021, 1, 1, tzinfo=MOSCOW_TZ),
    catchup=False,
    tags=["NLP", "news"],
)

with dag:

    update_dataset_start, update_dataset_end = python_operator(
        job_name="update_dataset",
        script_path="src/jobs/update_NewSHead_dataset.py dataset/nhnet {{ ds }} "
                    "--dataset-files train.json valid.json test.json",
        sla=timedelta(minutes=5),
    )

    process_dataset_start, process_dataset_end = python_operator(
        job_name="process_dataset",
        script_path="src/jobs/process_NewSHead_dataset.py dataset/nhnet {{ ds }} --dataset-files test.json",
        sla=timedelta(minutes=5)
    )

    dag.doc_md = """
    Text annotation pipeline
    """
    update_dataset_end >> process_dataset_start
