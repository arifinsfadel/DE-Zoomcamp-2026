Module 5: Data Batch with PySpark
Tech Stack

PySpark : Python API for Apache Spark, enabling distributed, large-scale data processing using Python. It allows data engineers and scientists to work with familiar syntax while leveraging Spark's SQL, DataFrame, and Machine Learning modules for big data tasks.
📝 Homework

In this homework, i learned on how to do partitioning, cleaning, transforming and also load data using PySpark. We use Yellow 2025-11 data from the official website:

# for yellow taxi data
!curl -o yellow_tripdata_2025-11.parquet https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2025-11.parquet

# lookup table for zone id
!curl -o taxi_zone_lookup.csv https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv

Question 1. Install Spark and PySpark
