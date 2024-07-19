from datetime import datetime, timedelta
import yaml
from feast import FeatureStore, Entity, FeatureService, FeatureView, Field, SnowflakeSource
from feast.types import Float32, Int64
import pandas as pd

project_name = yaml.safe_load(open("feature_store.yaml"))["project"]

# Create entity
driver = Entity(
    name="driver",
    join_keys=["driver_id"],
)

# Create data sources
driver_orders_source = SnowflakeSource(
    database=yaml.safe_load(open("feature_store.yaml"))["offline_store"]["database"],
    table="driver_orders",
    warehouse="COMPUTE_WH",
    timestamp_field="event_timestamp"
)

driver_stats_source = SnowflakeSource(
    database=yaml.safe_load(open("feature_store.yaml"))["offline_store"]["database"],
    table=f"feast_test_feast_driver_hourly_stats",
    warehouse="COMPUTE_WH",
    timestamp_field="event_timestamp",
    created_timestamp_column="created",
)

# Create feature views
driver_orders_fv = FeatureView(
    name="driver_orders",
    entities=[driver],
    ttl=timedelta(weeks=52),
    schema=[
        Field(name="trip_completed", dtype=Int64),
    ],
    batch_source=driver_orders_source,
    online=True
)

driver_stats_fv = FeatureView(
    name="driver_hourly_stats",
    entities=[driver],
    ttl=timedelta(weeks=52),
    schema=[
        Field(name="conv_rate", dtype=Float32),
        Field(name="acc_rate", dtype=Float32),
        # Field(name="avg_daily_trips", dtype=Int64),
    ],
    batch_source=driver_stats_source,
    online=True
)

driver_trips_fv = FeatureView(
    name="driver_avg_daily_trips",
    entities=[driver],
    ttl=timedelta(weeks=52),
    schema=[
        Field(name="avg_daily_trips", dtype=Int64),
    ],
    batch_source=driver_stats_source,
    online=True
)

# Create feature services
driver_stats_fs = FeatureService(name="driver_activity", features=[driver_stats_fv, driver_trips_fv, driver_orders_fv])
