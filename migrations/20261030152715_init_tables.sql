-- +goose Up
-- +goose StatementBegin

create table if not exists region (
	id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	region text not null unique
);

create table if not exists country (
	id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	country text not null unique
)

CREATE TABLE IF NOT EXISTS place (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    city TEXT NOT NULL,
    region_id int not null,
    country_id int not null,

    CONSTRAINT unique_place unique (city, region, country),

	CONSTRAINT fk_region_id
	FOREIGN KEY (region_id)
	REFERENCES region(id),

	CONSTRAINT fk_country_id
	FOREIGN KEY (country_id)
	REFERENCES country(id),
);

CREATE TABLE IF NOT EXISTS source (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    source_name TEXT NOT NULL UNIQUE,
    source_url text
);

CREATE TABLE IF NOT EXISTS weather (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    place_id INTEGER NOT NULL,
    temperature_cel_2m DOUBLE PRECISION,
    wind_speed_ms_10m DOUBLE PRECISION,
    relative_humidity_2m DOUBLE PRECISION,
    measure_timestamp timestamp not null,
    rain_mm DOUBLE PRECISION,
    source_id INTEGER NOT NULL,
    created_at timestamp not null default current_timestamp,
    updated_at timestamp,

    CONSTRAINT fk_weather_place
        FOREIGN KEY (place_id)
        REFERENCES place(id),

    CONSTRAINT fk_weather_source
        FOREIGN KEY (source_id)
        REFERENCES source(id),

	CONSTRAINT weather_measurement_unique
		UNIQUE (city_id, source_id, measure_timestamp)
);
-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
drop table if exists city, weather, source;
-- +goose StatementEnd
