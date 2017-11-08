# Grove Data Engineering - Neo Challenge

## Part 1 - ETL

For this ETL, I utilized a straightforward Python script to do the API querying, data cleaning, and loading. For the database, I used an AWS RDS PostgreSQL instance that I spun up specifically for this exercise, and the schema is contained in db/db.sql.

The script can be run as follows:
```
python etl.py --start-date YYYY-MM-DD --db-user DB_USER --db-password DB_PASSWORD --api-key API_KEY
```

The script will backfill from the provided start date if there are no records in the table, start from the date of the last record if there are records in the table, and exit with a warning if no start date is provided.

I chose to use (neo_reference_id, close_approach_date) as a compound primary key upon realizing that some neo_reference_ids appear multiple times (i.e. they approached Earth multiple times).

Testing is provided by the nosetests framework and can be done simply by running
```
nosetests
```
in the root directory of the repo.

## Part 2 - Visualization

I used an instance of Airbnb's open source data visualization tool Superset in order to create a time series line chart of average miss distance of NEOs over time starting from 1/1/2017. In order to make the chart less noisy and make it easier to observe trends, I chose to resample on a weekly basis rather than display each day's data point. I also, of course, made sure to filter for objects for which `is_potentially_hazardous_asteroid = true`.

![alt text](https://github.com/ananya77041/neo-challenge/neo_avg_miss_dist_time.png "Average Miss Distance of Potentially Hazardous NEOs over Time")
