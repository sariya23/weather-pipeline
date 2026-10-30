-- +goose Up
-- +goose StatementBegin
insert into source (source_name, source_url) values ('open-meteo', 'https://open-meteo.com/')
-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
delete from source where source_name='open-meteo';
-- +goose StatementEnd
