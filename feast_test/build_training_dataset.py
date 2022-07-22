from feast import FeatureStore
import pandas as pd
from datetime import datetime

# Define feature references
feature_refs = [
    "driver_trips:average_daily_rides",
    "driver_trips:maximum_daily_rides",
    "driver_trips:rating",
    "driver_trips:rating:trip_completed",
]

# Create an entity dataframe  
# An entity dataframe is the target dataframe on which you would like to join feature values.

entity_df = """SELECT event_timestamp, driver_id FROM FEAST_TEST.PUBLIC.feast_test_feast_driver_hourly_stats"""
# entity_df = pd.DataFrame.from_dict({"driver_id": [1001, 1002, 1003, 1004, 1005],})
# entity_df["event_timestamp"] = pd.to_datetime("now", utc=True)

fs = FeatureStore(repo_path=".")


# Get historical features
# This method launches a job that executes a point-in-time join of features from the offline store onto the entity dataframe. 
# Once completed, a job reference will be returned. This job reference can then be converted to a Pandas dataframe by calling to_df().
training_df = fs.get_historical_features(
    features=[
        "driver_hourly_stats:conv_rate",
        "driver_hourly_stats:acc_rate"
    ],
    entity_df=entity_df
).to_df()

print(training_df.head())