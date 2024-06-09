DROP DATABASE IF EXISTS :"db_name";
CREATE DATABASE :"db_name" WITH ENCODING 'UTF8';
DROP USER IF EXISTS :"user";
CREATE USER :"user" WITH PASSWORD :'password';
ALTER DATABASE :"db_name" OWNER TO :"user";
ALTER SCHEMA public owner to :"user";
GRANT ALL PRIVILEGES ON DATABASE :"db_name" TO :"user";
GRANT USAGE ON SCHEMA public TO :"user";
GRANT CREATE ON SCHEMA public TO :"user";
GRANT ALL PRIVILEGES ON DATABASE :"db_name" TO :"user";

\c :"db_name";
DROP TABLE IF EXISTS film_scores;
CREATE TABLE IF NOT EXISTS film_scores (
    window_start BIGINT NOT NULL,
    film_id VARCHAR(32) NOT NULL,
    title VARCHAR(128) NOT NULL,
    scores_sum INTEGER NOT NULL,
	scores_count INTEGER NOT NULL,
    unique_scores_count INTEGER NOT NULL,
    PRIMARY KEY (window_start, film_id)
);
GRANT ALL PRIVILEGES ON TABLE film_scores TO :"user";