from feast import FeatureStore
import feature_definitions as fd
    
# Load the feature store from the current path
fs = FeatureStore(repo_path=".")

# Deploy the feature store to Snowflake
print("Deploying feature store to Snowflake...")
fs.apply([fd.driver, fd.driver_stats_fv, fd.driver_trips_fv, fd.driver_orders_fv, fd.driver_stats_fs])