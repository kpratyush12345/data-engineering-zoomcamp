CREATE TABLE IF NOT EXISTS green_trips_processed (
    lpep_pickup_datetime TIMESTAMP,
    lpep_dropoff_datetime TIMESTAMP,
    PULocationID INTEGER,
    DOLocationID INTEGER,
    passenger_count DOUBLE PRECISION,
    trip_distance DOUBLE PRECISION,
    tip_amount DOUBLE PRECISION,
    total_amount DOUBLE PRECISION
);

CREATE TABLE IF NOT EXISTS green_trips_aggregated (
    window_start TIMESTAMP,
    window_end TIMESTAMP,
    PULocationID INTEGER,
    num_trips BIGINT,
    total_passengers DOUBLE PRECISION,
    total_amount DOUBLE PRECISION,
    PRIMARY KEY (window_start, PULocationID)
);

CREATE TABLE IF NOT EXISTS green_trips_q4 (
    window_start TIMESTAMP,
    PULocationID INTEGER,
    num_trips BIGINT,
    PRIMARY KEY (window_start, PULocationID)
);

CREATE TABLE IF NOT EXISTS green_trips_q5 (
    session_start TIMESTAMP,
    session_end TIMESTAMP,
    PULocationID INTEGER,
    num_trips BIGINT,
    PRIMARY KEY (session_start, PULocationID)
);

CREATE TABLE IF NOT EXISTS green_trips_q6 (
    window_start TIMESTAMP,
    total_tip_amount DOUBLE PRECISION,
    PRIMARY KEY (window_start)
);
