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
    "pegasus_finetuning",
    default_args=default_args,
    schedule=timedelta(days=1),
    start_date=datetime(2021, 1, 1, tzinfo=MOSCOW_TZ),
    catchup=False,
    tags=["NLP", "news"],
)

with dag:
    finetuning_start, finetuning_end = python_operator(
        job_name="finetune_model",
        script_path="src/jobs/model/train_model.py",
        sla=timedelta(minutes=5),
    )

    dag.doc_md = """
    Text annotation pipeline
    """