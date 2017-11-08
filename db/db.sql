CREATE DATABASE nasa;

CREATE TABLE IF NOT EXISTS nasa.neo(
	neo_reference_id BIGINT PRIMARY KEY NOT NULL,
	close_approach_date DATE,
	name VARCHAR,
	is_potentially_hazardous BOOLEAN,
	miss_distance_km DOUBLE
);