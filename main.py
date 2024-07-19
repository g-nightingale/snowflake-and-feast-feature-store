from feast import FeatureStore
import feature_definitions as fd
    
# Load the feature store from the current path
fs = FeatureStore(repo_path=".")

# Deploy the feature store to Snowflake
print("Deploying feature store to Snowflake...")
fs.apply([fd.driver, fd.driver_stats_fv, fd.driver_trips_fv, fd.driver_orders_fv, fd.driver_stats_fs])


import tensorflow as tf
EXPORT_PATH = "/models"
model = 100

# Serving function that passes through keys
@tf.function(input_signature=[{
    'is_male': tf.TensorSpec([None,], dtype=tf.string, name='is_male'),
    'mother_age': tf.TensorSpec([None,], dtype=tf.float32, name='mother_age'),
    'plurality': tf.TensorSpec([None,], dtype=tf.string, name='plurality'),
    'gestation_weeks': tf.TensorSpec([None,], dtype=tf.float32, name='gestation_weeks'),
    'key': tf.TensorSpec([None,], dtype=tf.string, name='key')
}])

def keyed_prediction(inputs):
    feats = inputs.copy()
    key = feats.pop('key') # get the key from input
    output = model(feats) # invoke model
    return {'key': key, 'babyweight': output}

# Save model with serving signature
model.save(EXPORT_PATH, 
           signatures={'serving_default': keyed_prediction})

# Serving function that does not require a key
@tf.function(input_signature=[{
    'is_male': tf.TensorSpec([None,], dtype=tf.string, name='is_male'),
    'mother_age': tf.TensorSpec([None,],  dtype=tf.float32, name='mother_age'),
    'plurality': tf.TensorSpec([None,], dtype=tf.string, name='plurality'),
    'gestation_weeks': tf.TensorSpec([None,], dtype=tf.float32, name='gestation_weeks')
}])

def nokey_prediction(inputs):
    output = model(inputs) # invoke model
    return {'babyweight': output}

# Save model with both signatures
model.save(EXPORT_PATH, 
           signatures={'serving_default': nokey_prediction,
                       'keyed_prediction': keyed_prediction
})

