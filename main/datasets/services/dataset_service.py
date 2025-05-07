from django.db import connection
from main.datasets.models import DatasetType, Dataset
import uuid

from main.datasets.serializers import DatasetTypeSerializer

def sql_type(dtype: str) -> str:
    return {
        "float": "DOUBLE PRECISION",
        "int": "BIGINT",
        "text": "TEXT"
    }.get(dtype, "TEXT")

def create_dataset_table(dataset_type: DatasetTypeSerializer, well_id: uuid.UUID) -> str:
    table_name = f"{dataset_type.name}_{str(well_id).replace('-', '')}"

    if not dataset_type.columns.exists():
        raise ValueError("DatasetType must have at least one column defined.")

    columns_sql = ",\n".join([
        f"{col.mnemonic} {sql_type(col.data_type)}"
        for col in dataset_type.columns.all()
    ])

    create_sql = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            timestamp BIGINT NOT NULL,
            {columns_sql}
        );
    """

    hypertable_sql = f"""
        SELECT create_hypertable('{table_name}', 'timestamp', if_not_exists => TRUE);
    """

    with connection.cursor() as cursor:
        cursor.execute(create_sql)
        cursor.execute(hypertable_sql)
        Dataset.objects.get_or_create(
            dataset_type=dataset_type,
            well_id=well_id,
            defaults={"table_name": table_name}
        )

    return table_name


def insert_dataset_row(dataset_type: DatasetType, well_id: uuid.UUID, data: dict):
    table_name = f"{dataset_type.name}_{str(well_id).replace('-', '')}"
    columns = ", ".join(data.keys())
    values = [data[key] for key in data]
    placeholders = ", ".join(["%s"] * len(values))

    with connection.cursor() as cursor:
        cursor.execute(
            f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})",
            values
        )
