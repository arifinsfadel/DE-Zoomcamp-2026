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

Checking Spark Version with PySpark (Local Setup)

When you first install PySpark, a quick way to make sure everything is working is by creating a Spark session and checking the installed Spark version.

Here’s a simple example:

import pyspark
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .master("local[*]") \
    .appName("NY Taxi") \
    .config("spark.ui.port", "4040") \
    .getOrCreate()

# to know your spark version
print(f"Spark version: {spark.version}")

print(spark.version)

What’s going on here?
SparkSession.builder → used to configure and create a Spark session
.master("local[*]") → runs Spark locally using all available CPU cores
.appName("test") → sets the app name (you’ll see this in the Spark UI)
.getOrCreate() → creates a new session if none exists, or reuses an existing one

✅ Answer: 

When you run this, you should see something like:

4.1.1

That means PySpark is set up correctly, and you're running Spark version 4.1.1.


Question 2. Yellow November 2025
Read the November 2025 Yellow into a Spark Dataframe. Repartition the Dataframe to 4 partitions and save it to parquet. What is the average size of the Parquet (ending with .parquet extension) Files that were created (in MB)? Select the answer which most closely matches.
In this step, the goal is pretty straightforward: load the November 2025 yellow taxi dataset into Spark, split it into a few partitions, and save it back as parquet files. After that, we check roughly how big each file ends up being.

df = spark.read.parquet("yellow_tripdata_2025-11.parquet")
df.repartition(4).write.parquet("yellow_nov_2025_repartitioned")

spark.read.parquet() → loads the parquet file into a Spark DataFrame
.repartition(4) → reshuffles the data into 4 partitions (so we’ll get 4 output files)
.write.parquet() → saves the result back in parquet format


After writing the data, you’ll see 4 parquet files in the output folder.
Each file is around 24.4 MB, so the closest answer is:
✅ Answer: 

25MB


Q3.Count records

How many taxi trips were there on the 15th of November? Consider only trips that started on the 15th of November.

For this task, we want to find out how many taxi trips happened on a specific day—November 15th, 2025—based on the pickup timestamp.

Here’s the code:

from pyspark.sql.functions import col

df = spark.read.parquet("yellow_tripdata_2025-11.parquet")

df.filter(col("tpep_pickup_datetime").like("2025-11-15%")) \
  .count()

What’s going on here?
col("tpep_pickup_datetime") → references the pickup datetime column
.like("2025-11-15%") → filters rows where the date starts with 2025-11-15
% acts as a wildcard, so it matches any time on that day
.count() → returns the total number of matching rows


✅ Answer: Number of trips that started on the 15th November is 162,604

Q4. Longest trip

What is the length of the longest trip in the dataset in hours?

In this step, the goal is to figure out the longest taxi trip in the dataset. To do that, we calculate the time difference between pickup and dropoff, then convert it into hours.

Here’s the code:

from pyspark.sql.functions import col, unix_timestamp

df = spark.read.parquet("yellow_tripdata_2025-11.parquet")

# Calculate trip duration in hours
df_with_duration = df.withColumn(
    "duration_hours",
    (unix_timestamp(col("tpep_dropoff_datetime")) -
     unix_timestamp(col("tpep_pickup_datetime"))) / 3600
)

# Get the longest trip
longest = df_with_duration.agg({"duration_hours": "max"}).collect()[0][0]
print(f"Longest trip: {longest:.2f} hours")

What’s happening here?
unix_timestamp() → converts the datetime columns into seconds
Subtracting dropoff and pickup → gives the trip duration in seconds
Dividing by 3600 → converts seconds into hours
.agg({"duration_hours": "max"}) → finds the maximum trip duration



✅ Answer:
The longest hours trip duration in dataset is 90.6

Q5.User Interface

Spark's User Interface which shows the application's dashboard runs on which local port?

When working with Spark, there’s a built-in web interface that helps you monitor what’s going on—jobs, stages, tasks, storage, and more. It’s super useful for debugging or just understanding how your job is running.
By default, the Spark UI runs on: Port 4040


Other Spark Ports:
Port 	Purpose
4040 	Spark UI (application)
7077 	Spark Master (standalone cluster)
8080 	Cluster Manager UI
8081 	Worker UI
✅ Answer:
By default, Spark's User Interface will run on port 4040. Access via browser at http://localhost:4040. We can see the port when creating Local Spark Session.


Q6. Least frequent pickup location zone

Load the zone lookup data into a temp view in Spark. Using the zone lookup data and the Yellow November 2025 data, what is the name of the LEAST frequent pickup location Zone?

In this task, the goal is to figure out which pickup zone has the fewest taxi trips. To do that, we need to combine the main taxi dataset with the taxi zone lookup table so we can map location IDs to actual zone names.

SQL Approach
SELECT z.Zone, COUNT(*) as trip_count
FROM yellow y
JOIN zones z ON y.PULocationID = z.LocationID
GROUP BY z.Zone
ORDER BY trip_count ASC
LIMIT 1;

PySpark Approach
# Load zones dataset
df_zones = spark.read \
    .option("header", "true") \
    .csv("taxi_zone_lookup.csv")

df_zones.createOrReplaceTempView("zones")
df_yellow.createOrReplaceTempView("yellow")

result = spark.sql("""
    SELECT z.Zone, COUNT(*) as trip_count
    FROM yellow y
    JOIN zones z ON y.PULocationID = z.LocationID
    GROUP BY z.Zone
    ORDER BY trip_count ASC
    LIMIT 1
""")

What’s happening here?
join the taxi data with the zone lookup table using LocationID
Then  group by zone name to count how many trips happened in each area
After that, we sort ascending to get the smallest count first
Finally, limit to 1 to grab the least frequent zone

Top 5 Least Frequent Zones:
| Zone                                          | Trip Count |
| --------------------------------------------- | ---------- |
| Governor's Island/Ellis Island/Liberty Island | 1          |
| Eltingville/Annadale/Prince's Bay             | 1          |
| Arden Heights                                 | 1          |
| Port Richmond                                 | 3          |
| Rikers Island                                 | 4          |

✅ Answer:
Governor's Island/Ellis Island/Liberty Island, Arden Heights
