-- +goose Up
-- +goose StatementBegin
insert into city (city, longitude, latitude) values
('Moscow', 37.6063916, 55.625578),
('Kazan', 49.1115022, 55.7946485),
('Saint Petersburg', 30.1586551, 59.9606739);
-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
delete from city;
-- +goose StatementEnd
