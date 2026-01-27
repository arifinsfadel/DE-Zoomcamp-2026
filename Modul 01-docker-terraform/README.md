Module 1: Docker & Data Ingestion Using Postgres

Question 1. Understanding Docker Images

    Q1: Run docker with the python:3.13 image. Use an entrypoint bash to interact with the container. What's the version of pip in the image?

    Creating a Docker image Python 3.13
    
You can run python:3.13 with docker and interactive terminal flag (-it)

docker run -it --rm --entrypoint=bash python:3.13 


    Check the pip version

pip --version

Answer: The pip version of the Python 3.13 Docker image is 25.3
<img width="840" height="396" alt="CaptureiDEZC26-01-01 (26-1-2026)" src="https://github.com/user-attachments/assets/f38a4f26-e311-4537-bc36-d77f24ab7dd0" />

Question 2. Understanding Docker Networking and Docker-Compose

    Given the following docker-compose.yaml, what is the hostname and port that pgadmin should use to connect to the postgres database?


    Create docker-compose.yaml fill the file with the existing script from the question

services:
  db:
    container_name: postgres
    image: postgres:17-alpine
    environment:
      POSTGRES_USER: "postgres"
      POSTGRES_PASSWORD: "postgres"
      POSTGRES_DB: "ny_taxi"
    ports:
      - "5433:5432"
    volumes:
      - vol-pgdata:/var/lib/postgresql/data

  pgadmin:
    container_name: pgadmin
    image: dpage/pgadmin4:latest
    environment:
      PGADMIN_DEFAULT_EMAIL: "pgadmin@pgadmin.com"
      PGADMIN_DEFAULT_PASSWORD: "pgadmin"
    ports:
      - "8080:80"
    volumes:
      - vol-pgadmin_data:/var/lib/pgadmin

volumes:
  vol-pgdata:
    name: vol-pgdata
  vol-pgadmin_data:
    name: vol-pgadmin_data

    Run the docker-compose.yaml

docker compose up -d

    Run pgadmin4 Access pgAdmin in browser by browsing to http://localhost:8080, and login into pgadmin using PGADMIN_DEFAULT_EMAIL and PGADMIN_DEFAULT_PASSWORD state in the docker-compose.yaml file.

    Create new server Register the server connection refers to our configuration on the docker-compose.yaml:

    hostname : db
    port     : 5432
    username : postgres
    password : postgres

<img width="723" height="571" alt="CaptureiDEZC26-01-02 (26-1-2026)" src="https://github.com/user-attachments/assets/2f59a0aa-c697-4f8d-a094-6a92055c0b6a" />

Answer: Based on the docker-compose.yaml, the answer is db:5432

Data Ingestion to Answer Q3-Q6

To prepare the data needed for answering Question 3 to Question 6, I implemented a containerized data pipeline using Docker. The goal of this ingestion is to reliably download CSV data, process it in batches using Python, and load it into a PostgreSQL database for further analysis to answer the question.
 <img width="592" height="429" alt="image" src="https://github.com/user-attachments/assets/25998f03-2bbb-42d7-91de-fc305c366356" />


 This workflow follows a two-phase approach:

    Development Phase Purpose: Explore and validate ingestion logic safely What happened here:
        Inspect CSV data
        Testing database connection
        Experiment with batch size logic
        Prototype insert logic data Output: converted notebook script (.ipynb) into python script (.py) → pipeline.py

    Production Phase Purpose: Load data in a repeatable, deterministic, and scalable way What happened here:
        pipeline.py reads raw CSV files
        Data is inserted into PostgreSQL in batches
        Script runs via Docker container
        Can be scheduled or orchestrated later

Output
Data ingestion completed successfully. 
<img width="1284" height="611" alt="image" src="https://github.com/user-attachments/assets/fc4187c1-e15c-49dd-8d6f-b5b12628da1e" />


Question 3. Counting Short Trips

    Q3 : For the trips in November 2025 (lpep_pickup_datetime between '2025-11-01' and '2025-12-01', exclusive of the upper bound), how many trips had a trip_distance of less than or equal to 1 mile?`

Query: 

select 
	COUNT(*) as total_trip
from 
	green_taxi_data 
where 
	  lpep_pickup_datetime >= '2025-11-01'
  and
	  lpep_pickup_datetime < '2025-12-01'
  and 
    trip_distance <= 1;

Answer <img width="865" height="546" alt="image" src="https://github.com/user-attachments/assets/928f16ea-c964-4b26-87ef-fdc5eb61c0df" />

Question 4. Longest Trip for Each Day

    Q4: Which was the pick up day with the longest trip distance? Only consider trips with trip_distance less than 100 miles (to exclude data errors).

Query: 

select 
	lpep_pickup_datetime, trip_distance
from 
	green_taxi_data  
where 
  	trip_distance < 100
order by 
	trip_distance desc
limit 1;

Answer

<img width="832" height="537" alt="image" src="https://github.com/user-attachments/assets/63f95c24-afb4-491c-8dd2-e996073ec520" />

Question 5. Biggest Pickup Zone

    Q5: Which was the pickup zone with the largest total_amount (sum of all trips) on November 18th, 2025?

Query: 

SELECT 
    z."Zone",
    SUM(g.passenger_count) AS total_passengers
FROM 
    green_taxi_data g
JOIN 
    zones z ON g."PULocationID" = z."LocationID"
WHERE 
    CAST(g.lpep_pickup_datetime AS DATE) = '2025-11-01'
GROUP BY 
    z."Zone"
ORDER BY 
    total_passengers DESC
LIMIT 3;

select 
	z."Zone" as pickup_zone,
	sum(g.total_amount) as total_amount
from 
	green_taxi_data g
join
	zones z
on 
	g."PULocationID" = z."LocationID"
where 
		lpep_pickup_datetime >= '2025-11-18' 
	and 
		lpep_pickup_datetime < '2025-11-19'
group by pickup_zone
order by total_amount desc
limit 1;

Answer
<img width="786" height="579" alt="image" src="https://github.com/user-attachments/assets/73956305-bfd6-4efe-bb8b-583bbcf84aab" />

Question 6. Largest Tip

    Q6: For the passengers picked up in the zone named "East Harlem North" in November 2025, which was the drop off zone that had the largest tip?

Query: 
