Module 3: Data Warehouse

Overview

This repository contains my solutions for Module 3 of the Data Engineering Zoomcamp. In this module, I explored data warehousing and analytics using Google BigQuery, covering data ingestion, external vs materialized tables, and dataset/schema management. I analyzed query performance using bytes processed and applied partitioning and clustering strategies to optimize query efficiency and reduce storage and compute costs.
Tech Stack

    Google Cloud Storage (GCS) — Cloud object storage for raw data
    Google BigQuery — Serverless data warehouse for analytics, partitioning, and clustering

HomeWork:

Question 1

What is count of records for the 2024 Yellow Taxi Data? (1 point)
a. 65,623
b. 840,402
c. 20,332,093
d. 85,431,289 

✅ Answer: select count(1) from ny_taxi.external_yellow_tripdata_2024;
20,332,093

Question 2:

Write a query to count the distinct number of PULocationIDs for the entire dataset on both the tables. What is the estimated amount of data that will be read when this query is executed on the External Table and the Table?

    18.82 MB for the External Table and 47.60 MB for the Materialized Table
    0 MB for the External Table and 155.12 MB for the Materialized Table
    2.14 GB for the External Table and 0MB for the Materialized Table
    0 MB for the External Table and 0MB for the Materialized Table
✅ Answer: 0 MB for the External Table and 155.12 MB for the Materialized Table
-- External Table
SELECT COUNT(DISTINCT(PULocationID)) FROM `.nytaxi.external_yellow_tripdata_2024`;

-- Materialized Table
SELECT COUNT(DISTINCT(PULocationID)) FROM `.nytaxi.yellow_tripdata_2024`;

Question 3

Write a query to retrieve the PULocationID from the table (not the external table) in BigQuery. Now write a query to retrieve the PULocationID and DOLocationID on the same table.
Why are the estimated number of Bytes different? (1 point)

a. BigQuery is a columnar database, and it only scans the specific columns requested in the query. Querying two columns (PULocationID, DOLocationID) requires reading more data than querying one column (PULocationID), leading to a higher estimated number of bytes processed.
b. BigQuery duplicates data across multiple storage partitions, so selecting two columns instead of one requires scanning the table twice, doubling the estimated bytes processed.
c. BigQuery automatically caches the first queried column, so adding a second column increases processing time but does not affect the estimated bytes scanned.
d. When selecting multiple columns, BigQuery performs an implicit join operation between them, increasing the estimated bytes processed 

✅ Answer: The answer is (a)
-- Scanning only PULocationID
SELECT PULocationID FROM `.nytaxi.yellow_tripdata_2024`;

-- Scanning PULocationID and DOLocationID
SELECT PULocationID, DOLocationID FROM `.nytaxi.yellow_tripdata_2024`;

Question 4

How many records have a fare_amount of 0? (1 point)
a. 128,210
b. 546,578
c. 20,188,016
d. 8,333 
✅ Answer:8,333
select count(1) from ny_taxi.external_yellow_tripdata_2024
where fare_amount = 0;

Question 5

What is the best strategy to make an optimized table in Big Query if your query will always filter based on tpep_dropoff_datetime and order the results by VendorID (Create a new table with this strategy) (1 point)
a. Partition by tpep_dropoff_datetime and Cluster on VendorID
b. Cluster on by tpep_dropoff_datetime and Cluster on VendorID
c. Cluster on tpep_dropoff_datetime Partition by VendorID
d. Partition by tpep_dropoff_datetime and Partition by VendorID 
✅ Answer: Partition by tpep_dropoff_datetime and Cluster on VendorID

CREATE OR REPLACE TABLE `ny_taxi.yellow_tripdata_2024_partitioned_clustered`
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID 
AS SELECT * FROM `ny_taxi.yellow_tripdata_2024`;

Question 6

Write a query to retrieve the distinct VendorIDs between tpep_dropoff_datetime 2024-03-01 and 2024-03-15 (inclusive). Use the materialized table you created earlier in your from clause and note the estimated bytes. Now change the table in the from clause to the partitioned table you created for question 5 and note the estimated bytes processed. What are these values? (1 point)
a. 12.47 MB for non-partitioned table and 326.42 MB for the partitioned table
b. 310.24 MB for non-partitioned table and 26.84 MB for the partitioned table
c. 5.87 MB for non-partitioned table and 0 MB for the partitioned table
d. 310.31 MB for non-partitioned table and 285.64 MB for the partitioned table 

✅ Answer: 
SELECT DISTINCT(VendorID) FROM `ny_taxi.yellow_tripdata_2024`
WHERE DATE(tpep_dropoff_datetime) BETWEEN '2024-03-01' AND '2024-03-15';

The estimated bytes processed for this query is 310.24 MB 

SELECT DISTINCT(VendorID) FROM `ny_taxi.yellow_tripdata_2024_partitioned_clustered`
WHERE DATE(tpep_dropoff_datetime) BETWEEN '2024-03-01' AND '2024-03-15';

The estimated bytes processed for this query is 26.84 MB 

Question 7

Where is the data stored in the External Table you created? (1 point)
a. Big Query
b. Container Registry
c. GCP Bucket
d. Big Table 

✅ Answer: External tables point to data stored outside of BigQuery's internal storage. In this case, the data resides in Google Cloud Storage (GCS) Bucket.(https://docs.cloud.google.com/bigquery/docs/external-tables)

Question 8

It is best practice in Big Query to always cluster your data: (1 point)
a. True
b. False 

✅ Answer:False
Why it isn’t always "Best Practice"

    Small Tables: If your table is small (typically less than 10 GB), the overhead of clustering might not provide any noticeable performance gains.

    Query Patterns: Clustering only helps if you frequently filter or aggregate based on the specific columns you’ve clustered. If your query patterns are unpredictable or don't use those columns, clustering adds no value.

    Maintenance: While Big Query handles automatic re-clustering, it is still a design choice that requires understanding your data's cardinality.
