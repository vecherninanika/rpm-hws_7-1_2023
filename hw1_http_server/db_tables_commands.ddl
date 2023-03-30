CREATE EXTENSION "uuid-ossp";

CREATE TABLE examples (id uuid primary key default uuid_generate_v4(),
                       name text not null,
                       age int);

INSERT INTO examples (name, age) VALUES ('Matthew', 64), ('Valeria', 45);

CREATE TABLE IF NOT EXISTS token (username TEXT PRIMARY KEY, token uuid);

INSERT INTO token VALUES ('admin', 'a1b2c3d4-a1b2-c3d4-e5f6-a1b2c3a1b2c3');
