CREATE SCHEMA IF NOT EXISTS nasa;

CREATE TABLE IF NOT EXISTS nasa.neo(
	neo_reference_id BIGINT NOT NULL,
	close_approach_date DATE,
	name VARCHAR,
	is_potentially_hazardous BOOLEAN,
	miss_distance_km DOUBLE PRECISION,
	PRIMARY KEY(neo_reference_id, close_approach_date)
);