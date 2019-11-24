# airtunnel demo project

Welcome to the [airtunnel](https://github.com/joerg-schneider/airtunnel) demo project.

## Prerequisites
To get started, make sure you have **at least Python 3.6** installed on your system
and are familiar with the basics of [Apache Airflow](https://airflow.apache.org/) and 
[Python virtual environments](https://docs.python.org/3/library/venv.html). Also check out
the [airtunnel documentation](https://joerg-schneider.github.io/airtunnel).

## Initial Setup

1. Clone this repository to your local computer and take note of the absolute path. For example, 
I cloned mine to: `/Users/Joerg/programming/airtunnel-demo`

2. For a quick start, we have provided an example Airflow config file within this demo repo under 
`airflow-home/airflow.cfg.example`. Duplicate this in the same folder and name it `airflow.cfg`

3. Adjust your own `airflow.cfg`, by replacing all five `<ABSOLUTE-PATH-TO-YOUR-AIRTUNNEL-DEMO-FOLDER>` placeholders
with your own absolute paths to the demo repo you cloned. For example, my `airflow.cfg` begins like this:
    ```
    [core]
    dags_folder = <ABSOLUTE-PATH-TO-YOUR-AIRTUNNEL-DEMO-FOLDER>/airtunnel-demo/dags
    sql_alchemy_conn = sqlite:///<ABSOLUTE-PATH-TO-YOUR-AIRTUNNEL-DEMO-FOLDER>/airtunnel-demo/airflow-home/airflow.db
    ```
    (etc.)
4. From a terminal, switch into the `airtunnel-demo` folder and then create a new Python virtual env with airtunnel
in it:

    ```
    # we create a new virtual environment called airtunnel-env
    python -m venv airtunnel-env
    # we activate it:
    source airtunnel-env/bin/activate
    # we install airtunnel in it - this will also install Airflow & Pandas & PyArrow
    pip install airtunnel
    ```
    (alternatively any other means of creating and activating a Python venv will do, i.e. from PyCharm!)
   
    *For the next steps, please keep this venv activated!*
    
5. Set your AIRFLOW_HOME environment variable to the absolute path ending at the `airflow-home` folder of the demo 
repository you cloned. For example, the command for my path is: 
`export AIRFLOW_HOME=/Users/Joerg/programming/airtunnel-demo/airflow-home`

6. Test your setup by initializing the Airflow database. *With AIRFLOW_HOME set and the venv activated*, run in the
shell:
`airflow initdb`

    This should have created the database file `airflow.db` in the `airtunnel-demo/airflow-home` folder!

## Run the airtunnel demo

1. In a terminal, with the active airtunnel venv and the `AIRFLOW_HOME` set, start the webserver with: 
`airflow webserver`

2. In a second terminal window, with the active airtunnel venv and the `AIRFLOW_HOME` set, start the scheduler with:
`airflow scheduler`

3. Navigate to the (hopefully running) Airflow webserver at: http://localhost:8080. You should see the example
airtunnel DAG called "university"

4. Set the "university" DAG to "On" and trigger a run manually be clicking "Trigger DAG".

5. It should start processing the dummy data we already have provided with the repo under `data_store/ingest/landing`


When the demo run has finished, your local data store should look like:

```
├── archive
├── ingest
│   ├── archive
│   │   ├── enrollment
│   │   │   └── 2019-11-24T06_55_03.655207+00_00
│   │   │       └── enrollment_1.csv
│   │   ├── programme
│   │   │   └── 2019-11-24T06_55_03.655207+00_00
│   │   │       ├── programme_1.csv
│   │   │       └── programme_2.csv
│   │   └── student
│   │       └── 2019-11-24T06_55_03.655207+00_00
│   │           └── student.csv
│   └── landing
│       ├── enrollment
│       ├── programme
│       └── student
├── ready
│   ├── enrollment
│   │   └── enrollment.parquet.gzip
│   ├── enrollment_summary
│   │   └── enrollment_summary.parquet.gzip
│   ├── programme
│   │   └── programme.parquet.gzip
│   └── student
│       └── student.parquet.gzip
└── staging
    ├── pickedup
    │   ├── enrollment
    │   ├── programme
    │   └── student
    └── ready
```

You can see, the data associated with the three example input data assets has been ingested and archived under the
timestamp of the run and the final output data has been prepared within `ready` as parquet.gzip files.

**Congrats, you have successfully used airtunnel!**

## airtunnel and PySpark

To check out airtunnel with its PySpark capabilities, have a look at 
[this branch with an example](https://github.com/joerg-schneider/airtunnel-demo/tree/pyspark).