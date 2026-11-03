-- +goose Up
-- +goose StatementBegin
insert into region (region) values
	('Moscow'), ('Saint Petersburg'), ('Tatarstan');
-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
delete from region;
-- +goose StatementEnd
