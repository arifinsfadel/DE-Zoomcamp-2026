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


