-- +goose Up
-- +goose StatementBegin
INSERT INTO place (city, region_id, country_id)
SELECT
    v.city,
    r.id,
    c.id
FROM (
    VALUES
        ('Moscow', 'Moscow', 'Russia'),
        ('Kazan', 'Tatarstan', 'Russia'),
        ('Saint Petersburg', 'Saint Petersburg', 'Russia')
) AS v(city, region_name, country_name)
JOIN region r ON r.region = v.region_name
JOIN country c ON c.country = v.country_name;
-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
delete from country;
-- +goose StatementEnd
