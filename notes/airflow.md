# Introduction to Apache Airflow

## Table of Contents

- [What is Airflow](#what-is-airflow)
- [Installation and Setup](#installation-and-setup)
- [Core Concepts](#core-concepts)
- [Writing DAGs](#writing-dags)
- [Operators](#operators)
- [Dependencies](#dependencies)
- [Scheduling](#scheduling)
- [XComs](#xcoms)
- [Variables and Connections](#variables-and-connections)
- [Hooks](#hooks)
- [Airflow CLI](#airflow-cli)
- [Web UI Overview](#web-ui-overview)
- [Testing DAGs](#testing-dags)
- [Best Practices](#best-practices)
- [Practice Exercises](#practice-exercises)
- [Summary](#summary)
- [Next Steps](#next-steps)
- [Additional Resources](#additional-resources)

---

## What is Airflow

Apache Airflow is an open-source platform for developing, scheduling, and monitoring batch-oriented workflows. It uses Python code to define workflows as Directed Acyclic Graphs (DAGs), making them versionable, testable, and collaborative.

Key features:

- Workflows defined as Python code (DAGs)
- Rich scheduling with cron expressions and timetables
- Web-based UI for monitoring and managing workflows
- Extensive library of operators for external systems
- Built-in retries, alerts, and SLAs
- Horizontal scalability with Celery, Kubernetes, or Dask executors

---

## Installation and Setup

```python
# Install Airflow using pip with constraints
# pip install apache-airflow==2.8.0 \
#   --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.8.0/constraints-3.11.txt"

# Set the Airflow home directory (default is ~/airflow)
# export AIRFLOW_HOME=~/airflow

# Initialize the database, create admin user, start services
# airflow db init
# airflow users create --username admin --role Admin --email admin@example.com --password admin
# airflow webserver --port 8080   (terminal 1)
# airflow scheduler               (terminal 2)
```

```python
# Docker Compose setup (recommended for development)
# curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.8.0/docker-compose.yaml'
# mkdir -p ./dags ./logs ./plugins
# echo -e "AIRFLOW_UID=$(id -u)" > .env
# docker compose up airflow-init
# docker compose up -d
# Access web UI at http://localhost:8080 (airflow/airflow)
```

---

## Core Concepts

```python
from airflow import DAG
from datetime import datetime, timedelta

# DAG: a collection of tasks with dependencies
# "Directed" = defined execution order
# "Acyclic" = no circular dependencies

default_args = {
    "owner": "data_team",
    "depends_on_past": False,
    "email_on_failure": True,
    "retries": 3,                            # retry failed tasks 3 times
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    dag_id="my_first_dag",
    default_args=default_args,
    description="A simple tutorial DAG",
    schedule=timedelta(days=1),              # run daily
    start_date=datetime(2025, 1, 1),
    catchup=False,                           # don't run missed intervals
    tags=["tutorial"],
)

# TASKS: individual units of work (instances of Operators)
# OPERATORS: templates defining what work to do
# EXECUTION DATE (logical_date): the date a DAG run covers (NOT when it runs)
# A daily DAG for 2025-01-15 runs AFTER that day ends
```

---

## Writing DAGs

```python
# Traditional DAG definition
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def extract():
    return {"data": [1, 2, 3]}

def transform(**kwargs):
    ti = kwargs["ti"]
    data = ti.xcom_pull(task_ids="extract_task")  # get data from previous task
    return [x * 2 for x in data["data"]]

def load(**kwargs):
    ti = kwargs["ti"]
    data = ti.xcom_pull(task_ids="transform_task")
    print(f"Loading {len(data)} records")

with DAG("etl_pipeline", start_date=datetime(2025, 1, 1),
         schedule="@daily", catchup=False) as dag:

    extract_task = PythonOperator(task_id="extract_task", python_callable=extract)
    transform_task = PythonOperator(task_id="transform_task", python_callable=transform)
    load_task = PythonOperator(task_id="load_task", python_callable=load)

    extract_task >> transform_task >> load_task  # set dependencies
```

```python
# Modern TaskFlow API with @dag and @task decorators (Airflow 2.0+)
from airflow.decorators import dag, task
from datetime import datetime

@dag(dag_id="etl_taskflow", start_date=datetime(2025, 1, 1),
     schedule="@daily", catchup=False, tags=["etl"])
def etl_pipeline():

    @task()
    def extract():
        # Return value is automatically pushed to XCom
        return {"users": ["Alice", "Bob", "Charlie"]}

    @task()
    def transform(raw_data: dict):
        # Input automatically pulled from XCom
        return [name.upper() for name in raw_data["users"]]

    @task()
    def load(transformed_data: list):
        for user in transformed_data:
            print(f"Loading user: {user}")

    # TaskFlow handles XCom passing automatically
    raw = extract()
    transformed = transform(raw)
    load(transformed)

etl_pipeline()  # instantiate the DAG
```

---

## Operators

```python
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
from datetime import datetime

with DAG("operator_examples", start_date=datetime(2025, 1, 1),
         schedule="@daily", catchup=False) as dag:

    # BashOperator - run shell commands
    bash_task = BashOperator(
        task_id="run_script",
        bash_command="echo 'Hello from Bash' && date",
        env={"MY_VAR": "value"},
    )

    # PythonOperator - run Python functions
    def my_function(name, **kwargs):
        execution_date = kwargs["ds"]  # date string YYYY-MM-DD
        print(f"Hello {name}! Running for {execution_date}")

    python_task = PythonOperator(
        task_id="run_python",
        python_callable=my_function,
        op_kwargs={"name": "World"},
    )

    # EmailOperator - send emails
    email_task = EmailOperator(
        task_id="send_report",
        to=["team@example.com"],
        subject="Daily Report - {{ ds }}",  # Jinja templating
        html_content="<h1>Report for {{ ds }}</h1>",
    )

    bash_task >> python_task >> email_task
```

```python
from airflow import DAG
from airflow.sensors.filesystem import FileSensor
from airflow.sensors.external_task import ExternalTaskSensor
from datetime import datetime

with DAG("sensor_examples", start_date=datetime(2025, 1, 1),
         schedule="@daily", catchup=False) as dag:

    # FileSensor - wait for a file to appear
    wait_for_file = FileSensor(
        task_id="wait_for_file",
        filepath="/data/incoming/data.csv",
        poke_interval=60,          # check every 60 seconds
        timeout=3600,              # give up after 1 hour
        mode="reschedule",         # frees worker slot between checks
    )

    # ExternalTaskSensor - wait for a task in another DAG
    wait_for_upstream = ExternalTaskSensor(
        task_id="wait_for_upstream",
        external_dag_id="upstream_dag",
        external_task_id="final_task",
        allowed_states=["success"],
    )
```

---

## Dependencies

```python
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.utils.task_group import TaskGroup
from datetime import datetime

with DAG("dependency_examples", start_date=datetime(2025, 1, 1),
         schedule="@daily", catchup=False) as dag:

    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end")

    task_a = EmptyOperator(task_id="task_a")
    task_b = EmptyOperator(task_id="task_b")
    task_c = EmptyOperator(task_id="task_c")

    # >> means "runs before", << means "runs after"
    start >> [task_a, task_b]    # parallel execution
    [task_a, task_b] >> task_c   # task_c waits for both
    task_c >> end

    # Fan-out pattern with list comprehension
    parallel_tasks = [EmptyOperator(task_id=f"p_{i}") for i in range(3)]
    start >> parallel_tasks >> end
```

```python
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.utils.task_group import TaskGroup
from datetime import datetime

with DAG("task_group_example", start_date=datetime(2025, 1, 1),
         schedule="@daily", catchup=False) as dag:

    start = EmptyOperator(task_id="start")

    # Task Groups organize related tasks visually in the UI
    with TaskGroup("extract_group") as extract:
        EmptyOperator(task_id="extract_users")
        EmptyOperator(task_id="extract_orders")

    with TaskGroup("transform_group") as transform:
        clean = EmptyOperator(task_id="clean_data")
        enrich = EmptyOperator(task_id="enrich_data")
        clean >> enrich  # dependencies within a group

    end = EmptyOperator(task_id="end")

    start >> extract >> transform >> end
```

---

## Scheduling

```python
from airflow import DAG
from datetime import datetime, timedelta

# Cron expression format:
# ┌──── minute (0-59)
# │ ┌──── hour (0-23)
# │ │ ┌──── day of month (1-31)
# │ │ │ ┌──── month (1-12)
# │ │ │ │ ┌──── day of week (0-6, Sunday=0)

dag_daily = DAG("daily", schedule="0 6 * * *",       # daily at 6 AM
                start_date=datetime(2025, 1, 1), catchup=False)

dag_weekly = DAG("weekly", schedule="0 0 * * 1",     # every Monday midnight
                 start_date=datetime(2025, 1, 1), catchup=False)

dag_monthly = DAG("monthly", schedule="0 0 1 * *",   # first of each month
                  start_date=datetime(2025, 1, 1), catchup=False)

# Preset schedule strings
# @once, @hourly, @daily, @weekly, @monthly, @quarterly, @yearly

# timedelta scheduling
dag_freq = DAG("frequent", schedule=timedelta(minutes=30),
               start_date=datetime(2025, 1, 1), catchup=False)

# Manual trigger only
dag_manual = DAG("manual", schedule=None,
                 start_date=datetime(2025, 1, 1), catchup=False)
```

---

## XComs

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

with DAG("xcom_examples", start_date=datetime(2025, 1, 1),
         schedule="@daily", catchup=False) as dag:

    def push_data(**kwargs):
        ti = kwargs["ti"]
        ti.xcom_push(key="user_count", value=42)   # push explicitly
        return {"processed": True}                   # return value auto-pushed

    def pull_data(**kwargs):
        ti = kwargs["ti"]
        count = ti.xcom_pull(task_ids="push_task", key="user_count")
        result = ti.xcom_pull(task_ids="push_task")  # pulls return_value
        print(f"Count: {count}, Result: {result}")

    push_task = PythonOperator(task_id="push_task", python_callable=push_data)
    pull_task = PythonOperator(task_id="pull_task", python_callable=pull_data)
    push_task >> pull_task

# With TaskFlow API, XCom passing is automatic through function arguments
# Keep XCom data small (< 48KB for default backend)
# For large data, store externally and pass the reference
```

---

## Variables and Connections

```python
from airflow.models import Variable

# Variables store key-value pairs accessible from any DAG
# Set via CLI: airflow variables set my_key my_value
# Set via UI: Admin > Variables

api_endpoint = Variable.get("api_endpoint")
config = Variable.get("pipeline_config", deserialize_json=True)
optional = Variable.get("optional_var", default_var="default")

Variable.set("last_run_status", "success")

# In Jinja templates: {{ var.value.api_endpoint }}
# JSON values: {{ var.json.pipeline_config.batch_size }}
```

```python
# Connections store credentials for external systems
# Set via CLI:
# airflow connections add 'my_postgres' \
#   --conn-type 'postgres' --conn-host 'localhost' \
#   --conn-login 'user' --conn-password 'pass' --conn-port 5432

# Use in operators via conn_id parameter
from airflow.providers.postgres.operators.postgres import PostgresOperator

query_task = PostgresOperator(
    task_id="run_query",
    postgres_conn_id="my_postgres",
    sql="SELECT count(*) FROM users;",
)

# Access connection details programmatically
from airflow.hooks.base import BaseHook
conn = BaseHook.get_connection("my_postgres")
print(conn.host, conn.login, conn.port)
```

---

## Hooks

```python
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.decorators import dag, task
from datetime import datetime

@dag(start_date=datetime(2025, 1, 1), schedule="@daily", catchup=False)
def hook_examples():

    @task()
    def query_database():
        hook = PostgresHook(postgres_conn_id="my_postgres")
        records = hook.get_records("SELECT id, name FROM users LIMIT 10")
        df = hook.get_pandas_df("SELECT * FROM users")
        return df.to_dict()

    @task()
    def upload_to_s3(data: dict):
        from airflow.providers.amazon.aws.hooks.s3 import S3Hook
        hook = S3Hook(aws_conn_id="my_aws")
        hook.load_string(string_data=str(data), key="output/data.json",
                         bucket_name="my-bucket", replace=True)

    db_data = query_database()
    upload_to_s3(db_data)

hook_examples()
```

---

## Airflow CLI

```python
# DAG management
# airflow dags list                          # list all DAGs
# airflow dags trigger my_dag                # manually trigger
# airflow dags pause/unpause my_dag          # toggle scheduling
# airflow dags test my_dag 2025-01-01        # test run for a date

# Task management
# airflow tasks list my_dag                  # list tasks in a DAG
# airflow tasks test my_dag my_task 2025-01-01  # test a single task
# airflow tasks clear my_dag -t my_task      # clear for re-run

# Database, users, variables, connections
# airflow db init / upgrade / check
# airflow users list / create
# airflow variables list / get / set
# airflow connections list / add
```

---

## Web UI Overview

```python
# The Airflow Web UI provides:
#
# DAGs View: lists all DAGs with schedule, owner, recent run status
# Grid View: DAG runs as columns, tasks as rows, color-coded states
# Graph View: visual task dependency graph
# Gantt View: timeline showing task duration and parallelism
# Calendar View: run history on a calendar
#
# Task Instance (click on a task):
# - View logs, XCom values, rendered templates
# - Clear state for re-execution, mark success/failed
#
# Admin Menu:
# - Variables, Connections, Pools (concurrency limits), XComs
```

---

## Testing DAGs

```python
# Test from command line:
# airflow dags test my_dag 2025-01-01
# airflow tasks test my_dag extract_task 2025-01-01

import pytest
from airflow.models import DagBag

def test_dag_loaded():
    """Verify the DAG file has no import errors."""
    dag_bag = DagBag(dag_folder="dags/", include_examples=False)
    assert len(dag_bag.import_errors) == 0

def test_dag_structure():
    """Verify the DAG has expected tasks."""
    dag_bag = DagBag(dag_folder="dags/", include_examples=False)
    dag = dag_bag.get_dag("etl_pipeline")
    assert dag is not None
    task_ids = [t.task_id for t in dag.tasks]
    assert "extract_task" in task_ids
    assert "transform_task" in task_ids

# Test task functions independently
def test_transform_function():
    def transform(data):
        return [name.upper() for name in data["users"]]
    assert transform({"users": ["Alice"]}) == ["ALICE"]
```

---

## Best Practices

1. Keep DAG files lean - avoid heavy computation at module level

2. Use TaskFlow API for Python-based tasks

3. Set catchup=False unless you need historical backfills

4. Use Variables for config, Connections for credentials - never hardcode

5. Make tasks idempotent: running twice produces the same result

6. Make tasks atomic: each task does one well-defined thing

7. Set appropriate retries, retry_delay, and execution_timeout

8. Use Task Groups for organization in large DAGs

9. Tag DAGs for filtering: tags=["production", "etl"]

10. Use Pools to limit concurrency for resource-constrained tasks

---

## Practice Exercises

1. **Simple ETL**: Create a DAG that extracts data from a file, transforms it, and loads results using the TaskFlow API.

2. **Sensor Pipeline**: Build a DAG with a FileSensor that waits for a file, processes it, and sends a notification.

3. **Parallel Processing**: Design a DAG with task groups that processes multiple sources in parallel and merges results.

4. **Parameterized DAG**: Create a manually triggered DAG with parameters for source, date range, and processing mode.

5. **Multi-DAG Workflow**: Create two DAGs where the second uses ExternalTaskSensor to wait for the first.

---

## Summary

Apache Airflow is a powerful workflow orchestration platform that defines data pipelines as Python code. Key takeaways:

- DAGs define workflows as directed acyclic graphs of tasks with dependencies
- The TaskFlow API simplifies DAG creation and XCom handling with decorators
- Operators (Bash, Python, Email, Sensors) define what each task does
- Dependencies use `>>` and `<<` operators for clear task ordering
- Scheduling supports cron expressions, timedelta intervals, and presets
- XComs pass small data between tasks; use external storage for large datasets
- Variables store configuration; Connections store external system credentials
- Hooks provide programmatic interfaces to external systems
- The Web UI provides monitoring, debugging, and management capabilities

---

## Next Steps

- Explore advanced executors (Celery, Kubernetes) for distributed execution
- Learn about custom operators and plugins
- Study DAG versioning and CI/CD for Airflow
- Investigate managed services (AWS MWAA, Google Cloud Composer, Astronomer)
- Explore dynamic DAG generation patterns

---

## Additional Resources

- [Apache Airflow Official Documentation](https://airflow.apache.org/docs/)
- [Airflow GitHub Repository](https://github.com/apache/airflow)
- [Astronomer Guides](https://docs.astronomer.io/learn)
- [Best Practices Guide](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html)
- [Awesome Apache Airflow](https://github.com/jghoman/awesome-apache-airflow)
