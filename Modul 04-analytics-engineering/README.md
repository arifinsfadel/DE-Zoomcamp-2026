Homework module 4




Question 1. Q1: dbt run --select int_trips_unioned builds which models? (1 point)
stg_green_tripdata, stg_yellow_tripdata, and int_trips_unioned
Any model with upstream and downstream dependencies
int_trips_unioned only
int_trips_unioned, int_trips, and fct_trips

✅ Answer:
int_trips_unioned only

In dbt, when you use the --select1 (or shorthand -s) flag without any additional operators and followed by a specific model name, dbt will execute only that specific model.

Question 2. Q2: New value 6 appears in payment_type. What happens on dbt test? (1 point)
dbt skips the test
dbt fails the test with non-zero exit code
dbt passes with warning
dbt updates the configuration

✅ Answer: dbt fails the test with non-zero exit code



Question 3. Q3: Count of records in fct_monthly_zone_revenue? (1 point)
12,998
14,120
12,184
15,421

✅ Answer: dbt will fail the test, returning a non-zero exit code.



Question 4. Q4: Zone with highest revenue for Green taxis in 2020? (1 point)
East Harlem North
Morningside Heights
East Harlem South
Washington Heights South

✅ Answer: East Harlem North




Question 5. Q5: Total trips for Green taxis in October 2019? (1 point)
500,234
350,891
384,624
421,509

✅ Answer: 384,624



Question 6. Q6: Count of records in stg_fhv_tripdata (filter dispatching_base_num IS NULL)? (1 point)
42,084,899
43,244,693
22,998,722
44,112,187

✅ Answer: 43,244,693
