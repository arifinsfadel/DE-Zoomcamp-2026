Module 7: Streaming Data with Redpanda & PyFlink

In this module, we’re getting into streaming data using a combination of Redpanda and PyFlink.

⚙️ Tech Stack Overview
Redpanda
Think of Redpanda as a simpler, faster alternative to Kafka. It’s fully Kafka-compatible, but built in C++—so no JVM, no ZooKeeper, and way less overhead. It’s especially nice to run in Docker since the setup is much lighter.
PyFlink
PyFlink is the Python interface for Apache Flink. It lets you build streaming (and batch) data pipelines using Python, while still getting the power and scalability Flink is known for. Great option if you don’t want to deal with Java or Scala.
📝 Homework Overview

For this homework, the focus is on building a basic streaming pipeline using Kafka-style messaging with Redpanda and processing it with PyFlink.

Even though we’re using Redpanda, it works just like Kafka under the hood—so any Kafka client will work without changes.

📊 Dataset

We’ll be working with the Green Taxi Trip data for October 2025:

green_tripdata_2025-10.parquet


Question 1. Redpanda Version

What version of Redpanda are you running?

First, make sure your Redpanda container is running and accessible. You can jump into the container and check the version using the rpk CLI:

docker exec -it workshop-redpanda-1 rpk version

✅ Answer:
The Redpanda version that running on is v25.3.9



Question 2. Sending data to Redpanda

Create a topic called green-trips:
docker exec -it workshop-redpanda-1 rpk topic create green-trips
Now write a producer to send the green taxi data to this topic.
Read the parquet file and keep only these columns:

    lpep_pickup_datetime
    lpep_dropoff_datetime
    PULocationID
    DOLocationID
    passenger_count
    trip_distance
    tip_amount
    total_amount

Convert each row to a dictionary and send it to the green-trips topic. You'll need to handle the datetime columns - convert them to strings before serializing to JSON.
Measure the time it takes to send the entire dataset and flush:
from time import time
t0 = time()
# send all rows ...
producer.flush()

t1 = time()
print(f'took {(t1 - t0):.2f} seconds')

How long did it take to send the data?

✅ Answer:
It needs around 10 seconds to sending data to redpanda


Explanation:

1. Create the Kafka topic (green-trips)
docker exec -it workshop-redpanda-1 rpk topic create green-trips
2. Create Producer python file Q2 Producer,
3. Run and check the result
uv run python src/producers/producer_green.py
The time printed in the terminal is our answer.


Question 3. Consumer - trip distance

Write a Kafka consumer that reads all messages from the green-trips topic (set auto_offset_reset='earliest').
Count how many trips have a trip_distance greater than 5.0 kilometers.

How many trips have trip_distance > 5?

✅ Answer:
There are 8506 trips with trip_distance more than 5. 

Explanation

Create Consumer File: (Q3 Consumer) 

Run:

uv run python src/consumers/consumer_green.py

The Trips > 5.0 km  is our answer.

    Note: consumer_timeout_ms=10000 makes the script exit automatically instead of hanging forever.


Question 4. Tumbling window - pickup location

Create a Flink job that reads from green-trips and uses a 5-minute tumbling window to count trips per PULocationID.
Write the results to a PostgreSQL table with columns: window_start, PULocationID, num_trips.
After the job processes all data, query the results:

SELECT PULocationID, num_trips
FROM <your_table>
ORDER BY num_trips DESC
LIMIT 3;

Which PULocationID had the most trips in a single 5-minute window?

✅ Answer:
PULocationID with the most trips in a single 5-minute window is 74

Explanation

 1. Create Table

    docker exec -it workshop-postgres-1 psql -U postgres -d postgres -c "
    CREATE TABLE q4_pickup_counts (
        window_start TIMESTAMP,
        PULocationID INTEGER,
        num_trips BIGINT,
        PRIMARY KEY (window_start, PULocationID)
    );
    "

2.  Create a flink job (Q4 Job) and run:

    docker exec -it workshop-jobmanager-1 flink run \
        -py /opt/src/job/q4_tumbling_location.py \
        --pyFiles /opt/src -d

    If any error related to no file detected, try:

    MSYS_NO_PATHCONV=1 \
        docker exec -it workshop-jobmanager-1 flink run \
        -py /opt/src/job/q4_tumbling_location.py -d

3.  Query the table via terminal:

    docker exec -it workshop-postgres-1 psql -U postgres -d postgres -c "
    SELECT PULocationID, num_trips
    FROM q4_pickup_counts
    ORDER BY num_trips DESC
    LIMIT 3;
    "

Question 5. Session window - longest streak

Create another Flink job that uses a session window with a 5-minute gap on PULocationID, using lpep_pickup_datetime as the event time with a 5-second watermark tolerance.
A session window groups events that arrive within 5 minutes of each other. When there's a gap of more than 5 minutes, the window closes.
Write the results to a PostgreSQL table and find the PULocationID with the longest session (most trips in a single session).

How many trips were in the longest session?

✅ Answer:
The answer is 81

Explanation:

1. Create Table

docker exec -it workshop-postgres-1 psql -U postgres -d postgres -c "
CREATE TABLE q5_session_counts (
    window_start TIMESTAMP,
    window_end   TIMESTAMP,
    PULocationID INTEGER,
    num_trips    BIGINT,
    PRIMARY KEY (window_start, window_end, PULocationID)
);
"

2. Create a flink job (Q5 Job: workshop/src/job/q5_session_location.py) and run:

docker exec -it workshop-jobmanager-1 flink run \
    -py /opt/src/job/q5_session_location.py \
    --pyFiles /opt/src -d

If any error related to no py file detected, try:

MSYS_NO_PATHCONV=1 \
    docker exec -it workshop-jobmanager-1 flink run \
    -py /opt/src/job/q5_session_location.py -d

3. Query the table via terminal:

docker exec -it workshop-postgres-1 psql -U postgres -d postgres -c "
SELECT pulocationid, num_trips, window_start, window_end,
      EXTRACT(EPOCH FROM (window_end - window_start))/60 AS duration_minutes
FROM q5_session_counts
ORDER BY num_trips DESC
LIMIT 5;
"


Question 6. Tumbling window - largest tip

Create a Flink job that uses a 1-hour tumbling window to compute the total tip_amount per hour (across all locations).

Which hour had the highest total tip amount?

✅ Answer:
The answer is 2025-10-16 18:00:00


Explanation

1.  Create Table

    docker exec -it workshop-postgres-1 psql -U postgres -d postgres -c "
    CREATE TABLE q6_tip_by_hour (
        window_start     TIMESTAMP,
        total_tip_amount DOUBLE PRECISION,
        PRIMARY KEY (window_start)
    );
    "

2.  Create a flink job (Q6 Job: workshop/src/job/q6_tip_by_hour.py) and run:

    docker exec -it workshop-jobmanager-1 flink run \
        -py /opt/src/job/q6_tip_by_hour.py \
        --pyFiles /opt/src -d

    If any error related to no py file detected, try:

    MSYS_NO_PATHCONV=1 \
        docker exec -it workshop-jobmanager-1 flink run \
        -py /opt/src/job/q6_tip_by_hour.py -d

3.  Query the table via terminal:

    docker exec -it workshop-postgres-1 psql -U postgres -d postgres -c "
    SELECT window_start, ROUND(total_tip_amount::numeric, 2) AS total_tip
    FROM q6_tip_by_hour
    ORDER BY total_tip_amount DESC
    LIMIT 3;
    "
