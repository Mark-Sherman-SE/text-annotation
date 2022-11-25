from datetime import datetime, timedelta
from textwrap import dedent

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator


def test_cuda_support():
    import torch
    print("Is cuda available:", torch.cuda.is_available())
    #if torch.cuda.is_available():
    print("CUDA version:", torch.version.cuda)


default_args={
    'depends_on_past': False,
    'email': ['marshann2012@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    "text_annotation_old",
    default_args=default_args,
    schedule=timedelta(days=1),
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=['NLP', "news"],
    ) as dag:

    t1 = BashOperator(
    task_id='print_date',
    bash_command='date',
    )

    t2 = BashOperator(
        task_id='sleep',
        depends_on_past=False,
        bash_command='sleep 5',
        retries=3,
    )
    templated_command = dedent(
        """
        {% for i in range(5) %}
            echo "{{ ds }}"
            echo "{{ macros.ds_add(ds, 7)}}"
        {% endfor %}
        """
    )

    t3 = BashOperator(
        task_id='templated',
        depends_on_past=False,
        bash_command=templated_command,
    )

    check_cuda = PythonOperator(
        task_id='check_cuda_support',
        python_callable=test_cuda_support,
    )

    t4 = BashOperator(
        task_id='check_videocard',
        depends_on_past=False,
        bash_command='nvidia-smi',
    )

    dag.doc_md = """
    This is a documentation placed anywhere
    """
    
    t1 >> [t2, t3]
    [t2, t3] >> check_cuda
    check_cuda >> t4
