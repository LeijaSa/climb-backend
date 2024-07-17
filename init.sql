-- init.sql
CREATE TABLE IF NOT EXISTS location (
    id SERIAL PRIMARY KEY,
    name VARCHAR(30) NOT NULL,
    location VARCHAR(40) NOT NULL
);
CREATE TABLE IF NOT EXISTS boulder_problem (
    id SERIAL PRIMARY KEY,
    description VARCHAR(550) NOT NULL,
    grade VARCHAR(5) NOT NULL,
    state VARCHAR(15) NOT NULL,
    add_date DATE DEFAULT CURRENT_DATE NOT NULL,
    location_id INTEGER NOT NULL,
    CONSTRAINT fk_location FOREIGN KEY(location_id) REFERENCES location(id)
);