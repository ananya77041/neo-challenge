# Grove Data Engineering - Neo Challenge

## Part 1 - ETL

For this ETL, I utilized a straightforward Python script to do the API querying, data cleaning, and loading. For the database, I used an AWS RDS PostgreSQL instance that I spun up specifically for this exercise, and the schema is contained in db/db.sql.

I chose to use (neo_reference_id, close_approach_date) as a compound primary key upon realizing that some neo_reference_ids appear multiple times (i.e. they approached Earth multiple times).

## Part 2 - Visualization

I used an instance of Airbnb's open source data visualization tool Superset in order to create a time series line chart of average miss distance of NEOs over time starting from 1/1/2017. In order to make the chart less noisy and make it easier to observe trends, I chose to resample on a weekly basis rather than display each day's data point.
