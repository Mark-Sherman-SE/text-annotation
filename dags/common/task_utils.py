import pendulum
from pendulum import DateTime

AIRFLOW_CWD = "/opt/airflow"
MOSCOW_TZ = pendulum.timezone("Europe/Moscow")


def localize(utc_datetime: DateTime) -> DateTime:
    return MOSCOW_TZ.convert(utc_datetime)


def create_task_id(base_name, detail):
    return "{}_{}".format(base_name, detail) if base_name is not None else detail
