Module 5: Data Platforms with Bruin

Tech Stack

Bruin : a data pipeline orchestration tool that helps manage, schedule, and run data workflows (such as SQL or Python transformations) in a structured and reproducible way.
Setup

    Install Bruin CLI: curl -LsSf https://getbruin.com/install/cli | sh
    Initialize the zoomcamp template: bruin init zoomcamp my-pipeline
    Configure your .bruin.yml with a DuckDB connection
    Follow the tutorial in the main module README

After completing the setup, you should have a working NYC taxi data pipeline.

📝 Homework
Question 1. Bruin Pipeline Structure

    In a Bruin project, what are the required files/directories?

        bruin.yml and assets/
        .bruin.yml and pipeline.yml (assets can be anywhere)
        .bruin.yml and pipeline/ with pipeline.yml and assets/
        pipeline.yml and assets/ only

✅ Answer:
The answer is .bruin.yml and pipeline/ with pipeline.yml and assets/

Explanation:
A Bruin project follows a clearly defined directory structure that allows the CLI to properly identify environments, pipelines, and dependencies.
At the project root level, the .bruin.yml file is required. This file acts as the main configuration layer where global settings, environment connections (such as DuckDB, BigQuery, or Snowflake), and shared parameters are defined.
Each pipeline must live inside its own pipeline/ directory. Within that directory, a pipeline.yml file defines the pipeline metadata, execution logic, and variables. Additionally, every pipeline folder must contain an assets/ directory. This directory stores the actual transformation logic, such as SQL scripts or Python files, along with their metadata definitions.
Without this structure, Bruin cannot properly register and execute the pipeline.

Question 2. Materialization Strategies

    You're building a pipeline that processes NYC taxi data organized by month based on pickup_datetime. Which incremental strategy is best for processing a specific interval period by deleting and inserting data for that time period? append - always add new rows replace - truncate and rebuild entirely time_interval - incremental based on a time column view - create a virtual table only

✅ Answer:
The answer is time_interval - incremental based on a time column

Explanation:
The time_interval strategy is the most appropriate option when processing time-partitioned data, such as NYC taxi trips organized by pickup_datetime.

This strategy deletes records within a specified time range and reloads only that interval. For example, if the pipeline processes monthly data, it will replace only the selected month rather than rebuilding the entire table. This makes it both efficient and scalable for large time-series datasets.

In comparison:
- append simply adds new rows and does not manage updates or reprocessing.
- replace rebuilds the entire table, which is inefficient for large datasets.
- view creates a virtual table without materializing physical data.

For time-based incremental workloads, time_interval is the most suitable and efficient approach.

Question 3. Pipeline Variables

    You have the following variable defined in pipeline.yml:

    variables:
     taxi_types:
       type: array
       items:
         type: string
       default: ["yellow", "green"]

    How do you override this when running the pipeline to only process yellow taxis?

        bruin run --taxi-types yellow
        bruin run --var taxi_types=yellow
        bruin run --var 'taxi_types=["yellow"]'
        bruin run --set taxi_types=["yellow"]

✅ Answer:
The answer is bruin run --var 'taxi_types=["yellow"]'

Explanation :
The concept follows the format --var KEY=VALUE

    The --var flag: Bruin uses the --var option in the CLI to override custom variables defined in pipeline.yml at runtime
    Handling arrays: Because the taxi_types variable is defined as an array, the override value must be written in a list format that Bruin can parse. Wrapping the array in single quotes (for example, 'taxi_types=["yellow"]') ensures the shell passes the entire bracketed value correctly to the Bruin CLI

Bruin allows runtime variable overrides using the --var flag in the CLI.
Since taxi_types is defined as an array in pipeline.yml, the override must respect the expected data type. Therefore, the value needs to be passed in array format.
Wrapping the parameter in single quotes ensures that the shell correctly interprets the entire array expression and passes it to Bruin without parsing errors.
Using this command limits execution to processing only yellow taxi data.

Question 4. Running with Dependencies

    You've modified the ingestion/trips.py asset and want to run it plus all downstream assets. Which command should you use?

        bruin run ingestion.trips --all
        bruin run ingestion/trips.py --downstream
        bruin run pipeline/trips.py --recursive
        bruin run --select ingestion.trips+

✅ Answer:
The answer is bruin run ingestion/trips.py --downstream

Explanation:
When an asset is modified and its dependent transformations must also be executed, the --downstream flag should be used.
This flag instructs Bruin to run the selected asset along with all assets that depend on it. It ensures that the dependency graph remains consistent and that downstream transformations reflect the updated logic.
This approach is particularly useful after modifying ingestion or staging layers that feed into multiple transformations.

    You want to ensure the pickup_datetime column in your trips table never has NULL values. Which quality check should you add to your asset definition?

        name: unique
        name: not_null
        name: positive
        name: accepted_values, value: [not_null]

✅ Answer:
The answer is name: not_null

Explanation:
Common data quality checks in Bruin include:

    not_null – Ensures a column does not contain NULL values.
    unique – Ensures all values in a column are unique (no duplicates).
    accepted_values – Ensures column values belong to a predefined list (e.g., ["yes", "no"]).
    min – Ensures the column value is greater than or equal to a specified minimum.
    max – Ensures the column value is less than or equal to a specified maximum.
    non-negative – Ensures verify that the values of the column are all non negative (positive or zero)
    positive – Ensures numeric values are greater than zero.
    pattern – Ensures that the values of the column match a specified regular expression.
    
To guarantee that the pickup_datetime column never contains NULL values, the appropriate quality check is not_null.

This validation rule ensures data completeness for critical fields. Other checks serve different purposes:
1. unique validates absence of duplicates
2. accepted_values restricts values to a predefined list
3. positive ensures numeric values are greater than zero

Since the requirement is to prevent NULL values, not_null is the correct configuration.

Question 6. Lineage and Dependencies

    After building your pipeline, you want to visualize the dependency graph between assets. Which Bruin command should you use?

        bruin graph
        bruin dependencies
        bruin lineage
        bruin show

✅ Answer:
The answer is bruin lineage

Explanation:
The bruin lineage command generates a visualization of asset dependencies within the pipeline.

This feature is useful for understanding upstream and downstream relationships, validating transformation flow, and troubleshooting dependency issues. It provides a clear representation of how assets are connected throughout the pipeline.

Question 7. First-Time Run

    You're running a Bruin pipeline for the first time on a new DuckDB database. What flag should you use to ensure tables are created from scratch?

        --create
        --init
        --full-refresh
        --truncate

✅ Answer:
The answer is --full-refresh

Explanation
When running a pipeline for the first time on a new DuckDB database, the --full-refresh flag ensures that all assets are rebuilt from scratch.

This flag ignores incremental logic and forces complete table creation. It is particularly important when initializing a new environment or applying structural schema changes.

Using --full-refresh guarantees a clean and fully materialized state for the database.
