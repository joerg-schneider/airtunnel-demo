from datetime import datetime

from airflow.models import DAG

from airtunnel import PySparkDataAsset
from airtunnel.operators.archival import DataAssetArchiveOperator, IngestArchiveOperator
from airtunnel.operators.ingestion import IngestOperator
from airtunnel.operators.loading import StagingToReadyOperator
from airtunnel.operators.transformation import PySparkTransformationOperator
from airtunnel.sensors.ingestion import SourceFileIsReadySensor

student = PySparkDataAsset("student_pyspark")
programme = PySparkDataAsset("programme_pyspark")
enrollment = PySparkDataAsset("enrollment_pyspark")
enrollment_summary = PySparkDataAsset("enrollment_summary_pyspark")

with DAG(
    dag_id="university_pyspark",
    schedule_interval=None,
    start_date=datetime(year=2019, month=9, day=1),
) as dag:
    ingested_ready_tasks = set()

    # a common stream of tasks for all ingested assets:
    for ingested_asset in (student, programme, enrollment):
        source_is_ready = SourceFileIsReadySensor(
            # we reduce the poke interval to only 3 seconds so that our example runs complete faster
            # do not do in production!! :)
            asset=ingested_asset,
            poke_interval=3,
            no_of_required_static_pokes=2,
        )
        ingest = IngestOperator(asset=ingested_asset)
        transform = PySparkTransformationOperator(asset=ingested_asset)
        archive = DataAssetArchiveOperator(asset=ingested_asset)
        staging_to_ready = StagingToReadyOperator(asset=ingested_asset)
        ingest_archival = IngestArchiveOperator(asset=ingested_asset)

        dag >> source_is_ready >> ingest >> transform >> archive >> staging_to_ready >> ingest_archival

        ingested_ready_tasks.add(staging_to_ready)

    # upon having loaded the three ingested assets, connect the aggregation downstream to them:
    build_enrollment_summary = PySparkTransformationOperator(asset=enrollment_summary)
    build_enrollment_summary.set_upstream(ingested_ready_tasks)

    staging_to_ready = StagingToReadyOperator(asset=enrollment_summary)

    dag >> build_enrollment_summary >> staging_to_ready
