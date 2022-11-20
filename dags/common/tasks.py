import datetime
from typing import Tuple, Optional, List

from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.models.baseoperator import BaseOperator
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.utils.task_group import TaskGroup

from common.task_utils import AIRFLOW_CWD, create_task_id


def python_operator(
    job_name: str,
    script_path: str,
    sla: datetime.timedelta,
    input_data: Optional[List[str]] = None,
    output_data: Optional[List[str]] = None,
    dag: Optional[DAG] = None,
    task_group: Optional[TaskGroup] = None,
    cwd: Optional[str] = AIRFLOW_CWD
):
    job_start = BashOperator(
        task_id=job_name,
        bash_command="python {} ".format(script_path),
        cwd=cwd,
        dag=dag,
        task_group=task_group
    )

    return default_operator(
        job_name,
        job_start,
        sla,
        dag,
        task_group
    )


def bash_operator(
    job_name: str,
    script_path: str,
    sla: datetime.timedelta,
    input_data: Optional[List[str]] = None,
    output_data: Optional[List[str]] = None,
    dag: Optional[DAG] = None,
    task_group: Optional[TaskGroup] = None,
    cwd: Optional[str] = AIRFLOW_CWD
):
    job_start = BashOperator(
        task_id=job_name,
        bash_command="{} ".format(script_path),
        cwd=cwd,
        dag=dag,
        task_group=task_group
    )

    return default_operator(
        job_name,
        job_start,
        sla,
        dag,
        task_group
    )


def default_operator(
    job_name: str,
    job: BaseOperator,
    sla: datetime.timedelta,
    dag: Optional[DAG] = None,
    task_group: Optional[TaskGroup] = None
):
    start_run = EmptyOperator(
        task_id=create_task_id(job_name, "start_run"), dag=dag, task_group=task_group
    )

    check_success_run = EmptyOperator(
        task_id=create_task_id(job_name, "check_success_run"),
        dag=dag,
        trigger_rule="none_failed_or_skipped",
        task_group=task_group
    )

    end_run = EmptyOperator(
        task_id=create_task_id(job_name, "end_run"),
        dag=dag,
        sla=sla,
        task_group=task_group
    )
    start_run >> job >> check_success_run >> end_run
    return start_run, end_run

