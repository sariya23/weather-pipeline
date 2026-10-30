-- +goose Up
-- +goose StatementBegin


CREATE TABLE IF NOT EXISTS city (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    city TEXT NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    latitude DOUBLE PRECISION NOT NULL
);

CREATE TABLE IF NOT EXISTS source (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    source_name TEXT NOT NULL,
    source_url text
);

CREATE TABLE IF NOT EXISTS weather (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    city_id INTEGER NOT NULL,
    temperature_cel_2m DOUBLE PRECISION NOT NULL,
    wind_speed_10m DOUBLE PRECISION NOT NULL,
    relative_humidity_2m DOUBLE PRECISION NOT NULL,
    measure_timestamp timestamp not null,
    source_id INTEGER NOT NULL,
    created_at timestamp not null default current_timestamp,
    updated_at timestamp,

    CONSTRAINT fk_weather_city
        FOREIGN KEY (city_id)
        REFERENCES city(id),

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
