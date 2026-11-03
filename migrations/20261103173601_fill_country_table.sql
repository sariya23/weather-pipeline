-- +goose Up
-- +goose StatementBegin
insert into country (country) values
	('Russia');
-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
delete from country;
-- +goose StatementEnd
