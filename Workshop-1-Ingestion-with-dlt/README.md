Homework Workshop 1: Ingestion with dlt for Data Engineering Zoomcamp 2026
Module — dlt Workshop: Build Your Own Pipeline
Overview

This repository contains my solutions for the DLT Workshop from the DataTalksClub Zoomcamp. In this module, I learned how to:

    Build and execute a dlt pipeline
    Inspect pipeline results using the dlt Dashboard
    Interact with my pipeline via the dlt MCP Server agent
    Explore and visualize the loaded data using a Marimo Notebook

The exercises focused on querying the Yellow Taxi dataset loaded through the taxi_pipeline.
Technologies Used

    dlt: For ingestion, schema creation, and incremental loading.
    DuckDB / BigQuery (depending on setup): As the destination warehouse.
    dlt Dashboard: For exploring pipeline runs and tables.
    dlt MCP Server: To ask questions about the pipeline programmatically.
    Marimo Notebook: For running SQL queries and building visualizations.


After completing the setup, you should have a working NYC taxi data pipeline.
📝 Homework
Question 1. 

    What is the start date and end date of the dataset? (1 point)
    a. 2009-01-01 to 2009-01-31
    b. 2009-06-01 to 2009-07-01
    c. 2024-01-01 to 2024-02-01
    d. 2024-06-01 to 2024-07-01 

✅ Answer:
The answer is 2009-01-01 to 2009-01-31

Explanation:
To identify the dataset period, I used the following aggregation query:

    ProSELECT
    MIN(trip_pickup_date_time) AS min_date,
    MAX(trip_pickup_date_time) AS max_date
    FROM nyc_taxi.trips;
 The query results show that the earliest pickup date (min_date) is 2009-06-01, 
 and the latest (max_date) is 2009-07-01. Therefore, the dataset covers trips from June 1, 2009, to July 1, 2009.   

Question 2. 

    What proportion of trips are paid with credit card? (1 point)
    a. 16.66%
    b. 26.66%
    c. 36.66%
    d. 46.66% 
    

✅ Answer:
The answer is 26.66%.

Explanation:
The proportion of credit card payments can be calculated using COUNT, GROUP BY, and the window function SUM(COUNT(*)) OVER():

    SELECT
    payment_type,
    COUNT(*) AS count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) AS percentage
    FROM nyc_taxi.trips
    GROUP BY payment_type
    ORDER BY count DESC;

  
Here, COUNT(*) counts the number of trips per payment type, while SUM(COUNT(*)) OVER() 
calculates the total number of trips across all payment types. From the results, out of 10,000 trips, 
2,666 were paid by credit card, giving a percentage of 26.66%.


Question 3. 

    What is the total amount of money generated in tips? (1 point)
    a. $4,063.41
    b. $6,063.41
    c. $8,063.41
    d. $10,063.41 

✅ Answer:
The answer is $6,063.41

Explanation :
The total tips can be calculated using the SUM() aggregation function:

    SELECT ROUND(SUM(tip_amount), 2) AS total_tips
    FROM nyc_taxi.trips;

The tip_amount column represents the tip for each trip. Using SUM() aggregates all tips, and ROUND(..., 2) 
formats the result to two decimal places for currency representation. The total amount collected in tips is $6,063.41.
