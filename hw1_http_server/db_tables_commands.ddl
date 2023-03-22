CREATE TABLE examples (name text not null, age int);

INSERT INTO examples (name, age) VALUES ('Matthew', 64), ('Valeria', 45);

CREATE EXTENSION "uuid-ossp";

CREATE TABLE IF NOT EXISTS token (username TEXT PRIMARY KEY, token uuid);

INSERT INTO token VALUES ('admin', uuid_generate_v4());