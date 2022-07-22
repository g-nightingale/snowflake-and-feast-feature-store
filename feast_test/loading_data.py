# From command line...
# feast materialize 2021-04-07T00:00:00 2021-04-08T00:00:00

# Or to materialise incrementally
# feast materialize-incremental 2021-04-08T00:00:00
# feast materialize-incremental 2022-07-19T00:00:00

# Unlike materialize, materialize-incremental automatically 
# determines the start time from which to load features from 
# batch sources of each feature view. The first time 
# materialize-incremental is executed it will set the start 
# time to the oldest timestamp of each data source, and the 
# end time as the one provided by the user. 

# Subsequent runs of materialize-incremental will then set 
# the start time to the end time of the previous run, thus 
# only loading new data that has arrived into the online store.